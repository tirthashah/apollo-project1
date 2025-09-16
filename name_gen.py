import time
import json
import pandas as pd
import os
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------
# CONFIG
# -----------------------
BASE_FOLDER = r"C:/Users/X1/Selenium/apollo"  # Change if needed
RESULT_FILE = "result.xlsx"  # File to store all results

# -----------------------
# CLI arguments
# -----------------------
parser = argparse.ArgumentParser()
parser.add_argument("--account", required=True, help="Account name (case-insensitive)")
parser.add_argument("--action", choices=["view", "follow", "connect", "both", "open_profile"], required=True)
parser.add_argument("--file", required=True, help="CSV/Excel input file name (inside BASE_FOLDER)")
args = parser.parse_args()

# -----------------------
# Load accounts.json
# -----------------------
with open("accounts.json", "r") as f:
    accounts = json.load(f)

# Normalize account name
account_name = None
for key in accounts.keys():
    if key.lower() == args.account.lower():
        account_name = key
        break
if not account_name:
    raise ValueError(f"Invalid account '{args.account}'. Choose from {list(accounts.keys())}")

file_name = args.file
action_to_do = args.action

# -----------------------
# LinkedIn Actions
# -----------------------
class LinkedInActions:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        

    def load_existing_results(self):
        if os.path.exists(RESULT_FILE):
            try:
                df = pd.read_excel(RESULT_FILE)
                return df
            except:
                return pd.DataFrame()
        return pd.DataFrame()

    def append_results_to_file(self, new_results_df):
        existing_df = self.load_existing_results()
        combined_df = pd.concat([existing_df, new_results_df], ignore_index=True) if not existing_df.empty else new_results_df
        try:
            combined_df.to_excel(RESULT_FILE, index=False)
        except PermissionError:
            print("⚠️ Close result.xlsx before writing!")
            return

    def open_profile(self, url):
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        print(f"👁 Viewed: {url}")

    

    def follow(self, url):
            """Follow only the specific profile opened via URL."""
            print(f"⏳ Attempting to follow profile: {url}")
            self.open_profile(url)
            time.sleep(2)

            try:
                # 1. Locate the main profile header (top section)
                profile_header = self.driver.find_element(By.XPATH, "//div[contains(@class,'pv-top-card')]")

                # 2. Look for Follow button directly in profile header
                follow_btn = profile_header.find_elements(By.XPATH, ".//button[.//span[normalize-space()='Follow']]")
                if follow_btn:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", follow_btn[0])
                    self.driver.execute_script("arguments[0].click();", follow_btn[0])
                    print(f"✅ Followed (direct button) for profile: {url}")
                    time.sleep(2)
                    return True

                # 3. If not found, check More menu inside header
                more_btn = profile_header.find_elements(By.XPATH, ".//button[contains(., 'More')]")
                if more_btn:
                    self.driver.execute_script("arguments[0].click();", more_btn[0])
                    time.sleep(2)
                    follow_in_more = profile_header.find_elements(
                        By.XPATH, ".//div[@role='menu']//span[normalize-space()='Follow']/ancestor::button"
                    )
                    if follow_in_more:
                        self.driver.execute_script("arguments[0].click();", follow_in_more[0])
                        print(f"✅ Followed (inside More menu) for profile: {url}")
                        time.sleep(2)
                        return True

            except Exception as e:
                print(f"⚠️ Follow failed for profile: {url} | {e}")

            print(f"⚠️ No Follow button found for profile: {url}")
            return False



    def connect_with_note(self, url, first_name=""):
        self.open_profile(url)
        time.sleep(2)
        connected = False
        try:
            connect_btns = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label,'Connect') or .//span[normalize-space()='Connect']]")
            if connect_btns:
                self.driver.execute_script("arguments[0].click();", connect_btns[0])
                connected = True
        except:
            pass

        if not connected:
            print(f"⚠️ No Connect button for {url}")
            return False

        time.sleep(2)
        try:
            add_note_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Add a note') or contains(text(),'Add a note')]")))
            add_note_btn.click()
            note_area = self.wait.until(EC.presence_of_element_located((By.XPATH, "//textarea")))
            message = f"Hi {first_name or 'there'}, I'd love to connect with you!"
            note_area.send_keys(message)
            send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label,'Send now') or span[text()='Send']]")))
            self.driver.execute_script("arguments[0].click();", send_btn)
            print(f"✅ Connected with note: {url}")
            return True
        except:
            print(f"⚠️ Could not send note: {url}")
            return False

# -----------------------
# Main job
# -----------------------
def run_job():
    file_path = os.path.join(BASE_FOLDER, file_name)
    if file_path.lower().endswith(".csv"):
        df_input = pd.read_csv(file_path)
    elif file_path.lower().endswith((".xlsx", ".xls")):
        df_input = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide CSV or Excel.")

    user_data_dir = accounts[account_name]
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)
    actions = LinkedInActions(driver, wait)

    # Add tracking columns
    df_input["RunFromAccount"] = account_name
    df_input["RunFromFile"] = file_name
    df_input["URL Opened"] = "❌"
    df_input["Followed"] = "❌"
    df_input["Connected"] = "❌"
    df_input["Note Sent"] = "❌"
    df_input["Processed Time"] = ""

    for idx, row in df_input.iterrows():
        url = row.get("Person Linkedin Url")
        first = row.get("First Name", "")

        df_input.at[idx, "Processed Time"] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

        # Open profile
        try:
            actions.open_profile(url)
            df_input.at[idx, "URL Opened"] = "✅"
        except:
            df_input.at[idx, "URL Opened"] = "❌"

        # Follow
        if action_to_do in ["follow", "both"]:
            df_input.at[idx, "Followed"] = "✅" if actions.follow(url) else "❌"

        # Connect
        if action_to_do in ["connect", "both"]:
            connected = actions.connect_with_note(url, first)
            df_input.at[idx, "Connected"] = "✅" if connected else "❌"
            df_input.at[idx, "Note Sent"] = "✅" if connected else "❌"

        # Save each profile result
        actions.append_results_to_file(df_input.iloc[[idx]])

    driver.quit()
    print("👍 Job done!")

# -----------------------
# Run
# -----------------------
run_job()
