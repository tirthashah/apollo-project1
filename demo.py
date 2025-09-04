import time
import csv
import psutil
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------------
# File Paths
# -----------------------------
csv_file_path = r"C:/Users/X1/Downloads/one_data.csv"     # Input CSV
output_file = r"C:/Users/X1/Downloads/connection_results.csv"  # Output CSV

# -----------------------------
# LinkedIn Credentials
# -----------------------------
linkedin_email = "brijeshshah19@gmail.com"
linkedin_password = "NextGen@1"

# -----------------------------
# Choose account
# -----------------------------
def is_chrome_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
            return True
    return False

while True:
    account = input("Which account do you want to open? (Brijesh/Tirtha): ").strip().capitalize()
    if account in ["Brijesh", "Tirtha"]:
        break
    print("❌ Invalid input! Please choose either 'Brijesh' or 'Tirtha'.")

# -----------------------------
# Chrome Options
# -----------------------------
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

if account == "Brijesh":
    if is_chrome_running():
        print("⚠️ Please close all Chrome windows before running Brijesh (default profile).")
        sys.exit()
    user_data_dir = r"C:\SeleniumProfile"  # Brijesh profile
    profile_directory = "Default"
elif account == "Tirtha":
    user_data_dir = r"C:\SeleniumProfile\Tirtha"  # Tirtha profile
    profile_directory = "Default"

options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_directory}")

# -----------------------------
# Initialize WebDriver
# -----------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# -----------------------------
# Open LinkedIn feed depending on account
# -----------------------------
if account == "Brijesh":
    driver.get("https://www.linkedin.com/feed/")
    print("✅ Brijesh LinkedIn feed opened in the same tab")
elif account == "Tirtha":
    driver.get("https://www.google.com")  # initial tab
    linkedin_url = "https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin"
    driver.execute_script(f"window.open('{linkedin_url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    print("✅ Tirtha LinkedIn feed opened in a new tab")

time.sleep(5)

# -----------------------------
# Login (if required)
# -----------------------------
try:
    email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    email_input.send_keys(linkedin_email)

    password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password_input.send_keys(linkedin_password)

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_btn.click()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Login successful!")
except:
    print("Login skipped (already logged in or using stored session)")

# -----------------------------
# Process CSV LinkedIn URLs
# -----------------------------
results = []

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        linkedin_url = row.get('Person Linkedin Url')
        first_name = row.get('First Name', '').strip() or "there"
        company = row.get('Company', '').strip() or "your company"
        status = "❌ Failed"
        
        if not linkedin_url:
            status = "⚠️ No URL"
            results.append({**row, "Status": status})
            continue

        print(f"\n➡️ Processing profile: {linkedin_url}")
        try:
            driver.get(linkedin_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)

            # Skip if it's a company page
            try:
                driver.find_element(By.XPATH, "//div[contains(@class,'org-top-card-summary')]")
                status = "⏭️ Skipped (Company)"
                print(status)
                results.append({**row, "Status": status})
                continue
            except:
                pass

            connected = False

            # Try inside "More"
            try:
                more_button_xpath = "(//span[contains(text(),'More')])[2]"
                more_button = wait.until(EC.element_to_be_clickable((By.XPATH, more_button_xpath)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_button)
                driver.execute_script("arguments[0].click();", more_button)
                print("✅ Opened 'More' menu")
                time.sleep(5)

                connect_inside_xpath = "(//span[@class='display-flex t-normal flex-1'][normalize-space()='Connect'])[2]"
                connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, connect_inside_xpath)))
                driver.execute_script("arguments[0].click();", connect_button)
                print(f"✅ Clicked 'Connect' (inside More) for: {linkedin_url}")
                time.sleep(5)
                connected = True
            except:
                print("⚠️ Connect not found inside More, checking outside...")

            # Try outside
            if not connected:
                try:
                    connect_outside_xpath = "(//span[@class='artdeco-button__text'][normalize-space()='Connect'])[2]"
                    connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, connect_outside_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", connect_button)
                    driver.execute_script("arguments[0].click();", connect_button)
                    print(f"✅ Clicked 'Connect' (outside More) for: {linkedin_url}")
                    time.sleep(5)
                    connected = True
                except:
                    status = "⚠️ No 'Connect' option"
                    print(status)
                    results.append({**row, "Status": status})
                    continue

            # Add note if Connect was clicked
            if connected:
                try:
                    add_note_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add a note']")))
                    add_note_btn.click()
                    time.sleep(5)

                    message = (
                        f"Hi {first_name}, I’ve been following {company} and truly admire the way you’re growing the team and product. "
                        f"At NextGenSoft, we help organizations scale faster with cloud-native architecture & DevOps while keeping reliability in focus. "
                        f"I’d be glad to connect, exchange a few ideas, and learn about your growth journey."
                    )

                    note_textarea = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='message']")))
                    note_textarea.clear()
                    note_textarea.send_keys(message)
                    time.sleep(100)  # Type pause, adjust as needed

                    # send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send now']")))
                    # send_btn.click()
                    # time.sleep(5)

                    status = "✅ Connected with Note"
                    print(f"🎯 Connection request sent with note to: {linkedin_url}")
                except Exception as e:
                    status = "⚠️ Could not send note"
                    print(f"{status}: {e}")

        except Exception as e:
            status = f"❌ Error opening profile ({e})"

        results.append({**row, "Status": status})

# -----------------------------
# Save results into CSV
# -----------------------------
with open(output_file, mode='w', newline='', encoding='utf-8') as out:
    fieldnames = list(results[0].keys())
    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"\n🎉 All done! Results saved into: {output_file}")
time.sleep(3)
driver.quit()
