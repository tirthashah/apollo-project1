# today.py
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import argparse
from openai import OpenAI  # Updated import for new API

# Set your ACTUAL OpenAI API key here (get from platform.openai.com/account/api-keys)
client = OpenAI(api_key="sk-your-actual-key-here")  # Replace this!

# -----------------------------
# Load accounts
# -----------------------------
with open("accounts.json", "r") as f:
    accounts = json.load(f)

# -----------------------------
# Parse arguments
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--account", choices=list(accounts.keys()), required=True)
parser.add_argument("--action", choices=["follow", "connect", "both"], required=True)
args = parser.parse_args()

account_name = args.account
choice = args.action
user_data_dir = accounts[account_name]

# -----------------------------
# Chrome driver with increased stability
# -----------------------------
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-notifications")  # Prevent pop-up issues
options.add_argument("--no-sandbox")  # For stability
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 40)  # Increased to 40s for slower loads

# -----------------------------
# LinkedIn Actions
# -----------------------------
class LinkedInActions:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def process_profiles(self, csv_file):
        df = pd.read_csv(csv_file)
        df["URL Opened"] = "❌"
        df["Followed"] = "❌"
        df["Connected"] = "❌"

        for index, row in df.iterrows():
            url = row.get("Person Linkedin Url")
            if not url:
                print("⚠️ No URL found")
                continue

            # Open URL
            try:
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                df.at[index, "URL Opened"] = "✅"
                time.sleep(10)
            except Exception as e:
                print(f"❌ Could not open URL: {url} (Error: {str(e)})")
                continue

            # FOLLOW
            if choice in ["follow", "both"]:
                try:
                    follow_btn = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "(//span[@class='artdeco-button__text'][normalize-space()='Follow'])[2]"))
                    )
                    ActionChains(driver).move_to_element(follow_btn).click(follow_btn).perform()
                    df.at[index, "Followed"] = "✅"
                    print(f"✅ Followed: {url}")
                    time.sleep(10)
                except Exception as e:
                    print(f"⚠️ Follow failed: {url} (Error: {str(e)})")

            # CONNECT
            if choice in ["connect", "both"]:
                connected = False
                try:
                    more_btn = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(),'More')])[2]"))
                    )
                    driver.execute_script("arguments[0].click();", more_btn)
                    time.sleep(5)

                    connect_btn = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "(//span[@class='display-flex t-normal flex-1'][normalize-space()='Connect'])[2]"))
                    )
                    driver.execute_script("arguments[0].click();", connect_btn)
                    connected = True
                    time.sleep(10)
                except:
                    pass

                if not connected:
                    try:
                        connect_btn = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Connect') or contains(., 'Connect')]"))
                        )
                        driver.execute_script("arguments[0].click();", connect_btn)
                        connected = True
                        time.sleep(10)
                    except Exception as e:
                        print(f"⚠️ Connect button not available: {url} (Error: {str(e)})")
                        connected = False

                if connected:
                    try:
                        # Add a note button
                        add_note_btn = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Add a note') or contains(text(), 'Add a note')]"))
                        )
                        add_note_btn.click()
                        time.sleep(5)

                        # Find parent relative div (your provided XPath)
                        try:
                            parent_div = wait.until(
                                EC.presence_of_element_located((By.XPATH, "(//div[@class='relative'])[1]"))
                            )
                        except:
                            parent_div = driver  # Fallback

                        # Updated: Find message box with more flexible match
                        try:
                            message_box = parent_div.find_element(By.XPATH, ".//div[contains(@class, 'connect-button') or contains(@class, 'send-invite') or contains(@class, 'message')]")
                        except:
                            message_box = parent_div  # Fallback

                        # Find textarea inside (with fallbacks)
                        note_area = message_box.find_element(By.XPATH, ".//textarea[@id='custom-message' or @name='message' or contains(@placeholder, 'message')]")

                        # Generate AI message targeting 50-100 words (~250 chars)
                        details = {
                            "first_name": row.get("First Name", "").strip() or "there",
                            "company": row.get("Company", "").strip() or "your company",
                            "title": row.get("Title", "").strip() or "your field",
                            "location": row.get("Location", "").strip() or "your area"
                        }
                        prompt = (
                            f"Create a personalized LinkedIn connection note (50-100 words, under 300 characters, engaging and professional) "
                            f"for {details['first_name']} at {details['company']}, title {details['title']}, "
                            f"in {details['location']}. Include a brief intro, shared interest, and call to connect."
                        )
                        try:
                            response = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[{"role": "user", "content": prompt}],
                                max_tokens=150,  # Targets 50-100 words
                                temperature=0.7
                            )
                            message = response.choices[0].message.content.strip()
                        except Exception as openai_err:
                            print(f"⚠️ OpenAI failed: {str(openai_err)}")
                            message = f"Hi {details['first_name']}, let's connect!"  # Fallback

                        note_area.clear()
                        note_area.send_keys(message)
                        time.sleep(5)

                        # Send button
                        send_btn = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@data-control-name='invite' or contains(@aria-label, 'Send') or contains(text(), 'Send')]"))
                        )
                        send_btn.click()
                        df.at[index, "Connected"] = "✅"
                        print(f"✅ Connected with message: '{message}' for {url}")
                        time.sleep(10)
                    except Exception as e:
                        print(f"⚠️ Note/send failed: {url} (Error: {str(e)})")
                        # Fallback: Send without note
                        try:
                            send_without_note = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Send without a note') or contains(text(), 'Send without a note')]")
                            send_without_note.click()
                            df.at[index, "Connected"] = "✅ (No note)"
                            print(f"✅ Connected without note: {url}")
                            time.sleep(10)
                        except:
                            pass

        # Save results
        df.to_excel("result.xlsx", index=False)
        print("🔹 Results saved to result.xlsx")

# -----------------------------
# Run
# -----------------------------
actions = LinkedInActions(driver, wait)
csv_file = r"C:/Users/X1/Downloads/one_data.csv"
actions.process_profiles(csv_file)
driver.quit()
print("🔹 Done!")
