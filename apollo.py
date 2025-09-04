import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ✅ CSV file path
csv_file_path = r"C:/Users/X1/Downloads/one_data.csv"
output_file = r"C:/Users/X1/Downloads/connection_results.csv"

# ✅ LinkedIn credentials
linkedin_email = "your_email"
linkedin_password = "your_password"

# ✅ Chrome options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# -----------------------------
# Login
# -----------------------------
driver.get("https://www.linkedin.com/login")
wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(linkedin_email)
wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(linkedin_password)
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ Login successful")

# -----------------------------
# Helper functions
# -----------------------------
def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def connect_person(url):
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        scroll_down()

        # Click "More"
        more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'More actions')]")))
        more_btn.click()
        time.sleep(5)

        # Click "Connect"
        connect_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Connect']")))
        connect_btn.click()
        time.sleep(5)

        # Click "Send without a note"
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Send without a note']")))
        send_btn.click()
        time.sleep(5)
        print(f"✅ Connection request sent: {url}")
        return "Done"
      

    except Exception as e:
        print(f"⚠️ Cannot connect to: {url} (Reason: {e})")
        return "Pending"

# -----------------------------
# Batch processing with result saving
# -----------------------------
batch_size = 5
long_wait = (3*60*60, 4*60*60)   # 3–4 hours
short_wait = (10*60, 20*60)      # 10–20 minutes

# Read all profiles
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    profiles = [row.get('Person Linkedin Url') for row in csv_reader if row.get('Person Linkedin Url')]

# Prepare results file
with open(output_file, mode='w', newline='', encoding='utf-8') as out:
    writer = csv.writer(out)
    writer.writerow(["LinkedIn URL", "Status"])  # header

    for i in range(0, len(profiles), batch_size):
        batch = profiles[i:i+batch_size]
        print(f"\n🚀 Starting batch {i//batch_size + 1}: {len(batch)} people")

        for url in batch:
            status = connect_person(url)
            writer.writerow([url, status])
            time.sleep(random.randint(5, 15))  # small delay between each profile

        if i + batch_size < len(profiles):
            # Wait 10–20 minutes between batches
            delay = random.randint(*short_wait)
            print(f"⏳ Waiting {delay//60} min before next batch...")
            time.sleep(delay)

            # After every 2 batches, take 3–4 hrs break
            if (i//batch_size + 1) % 2 == 0:
                delay = random.randint(*long_wait)
                print(f"😴 Long break {delay//3600} hrs...")
                time.sleep(delay)

print("🎉 All connection requests processed! Results saved in:", output_file)
driver.quit()
