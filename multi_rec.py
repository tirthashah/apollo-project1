import time
import json
import pandas as pd
import random  # Added for random delays
import os  # Added to check if file exists
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import argparse

#  Gemini (LangChain) imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage


# Initialize Gemini Model

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key="AIzaSyAfF0US-6dhORnzwUfEgRfZu0CaaefAiH4",  # 🔹 Replace with your actual Google API Key
    temperature=0.8
)


# Load accounts

with open("accounts.json", "r") as f:
    accounts = json.load(f)


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--account", choices=list(accounts.keys()), required=True)
parser.add_argument("--action", choices=["follow", "connect", "both"], required=True)
args = parser.parse_args()

account_name = args.account
choice = args.action
user_data_dir = accounts[account_name]


# Chrome driver with stability options

options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 40)

# LinkedIn Actions
class LinkedInActions:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def load_existing_results(self):
        if os.path.exists("result.xlsx"):
            try:
                existing_df = pd.read_excel("result.xlsx")
                print(f"📊 Found existing results with {len(existing_df)} records")
                return existing_df
            except Exception as e:
                print(f"⚠️ Could not read existing results: {e}")
                return pd.DataFrame()
        else:
            print("📊 No existing results found. Creating new file.")
            return pd.DataFrame()

    def append_results_to_file(self, new_results_df):
        existing_df = self.load_existing_results()
        combined_df = (
            new_results_df if existing_df.empty
            else pd.concat([existing_df, new_results_df], ignore_index=True)
        )

        # Always save only to result.xlsx
        try:
            combined_df.to_excel("result.xlsx", index=False)
            print(f"💾 Total records in result.xlsx: {len(combined_df)}")
        except PermissionError:
            # If Excel is open, close it first and overwrite
            print("⚠️ result.xlsx is open. Trying to overwrite...")

            try:
                os.remove("result.xlsx")  # delete locked file
                combined_df.to_excel("result.xlsx", index=False)
                print(f"✅ Overwritten result.xlsx with {len(combined_df)} records")
            except Exception as e:
                print(f"❌ Could not overwrite result.xlsx: {e}")

    def process_profiles(self, csv_file):
        df = pd.read_csv(csv_file)

        df["URL Opened"] = "❌"
        df["Followed"] = "❌"
        df["Connected"] = "❌"
        df["Note Sent"] = "❌"  
        df["Processed Time"] = ""
        df["Batch"] = f"Batch_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"

        total_profiles = len(df)
        print(f" Processing {total_profiles} profiles with random delays between each...")

        for index, row in df.iterrows():
            profile_number = index + 1
            print(f"\n Processing Profile {profile_number}/{total_profiles}")

            url = row.get("Person Linkedin Url")
            if not url:
                print(" No URL found")
                continue

            df.at[index, "Processed Time"] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                df.at[index, "URL Opened"] = "✅"
                print(f" Opened profile: {url}")
                time.sleep(10)
            except Exception as e:
                print(f"Could not open URL: {url} (Error: {str(e)})")
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
                        add_note_btn = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Add a note') or contains(text(), 'Add a note')]"))
                        )
                        add_note_btn.click()
                        time.sleep(5)

                        try:
                            parent_div = wait.until(
                                EC.presence_of_element_located((By.XPATH, "(//div[@class='relative'])[1]"))
                            )
                        except:
                            parent_div = driver

                        try:
                            message_box = parent_div.find_element(By.XPATH, ".//div")
                        except:
                            message_box = parent_div

                        note_area = message_box.find_element(By.XPATH, ".//textarea")

                        # AI generated note using Gemini
                        details = {
                            "first_name": str(row.get("First Name", "") or "").strip() or "there",
                            "company": str(row.get("Company", "") or "").strip() or "your company",
                            "title": str(row.get("Title", "") or "").strip() or "your field",
                            "location": str(row.get("Location", "") or "").strip() or "your area"
                        }
                        system_prompt = (
                            "You are a LinkedIn connection assistant. "
                            "Strictly follow these rules:\n"
                            "1. Message length must be between 170 and 190 characters.\n"
                            "2. Start with a greeting using the person’s first name.\n"
                            "3. Always include their first name, title, and company naturally in the message.\n"
                            "4. Mention something positive or interesting about their company in 1 short line.\n"
                            "5. Introduce my company, NextGenSoft, as a partner that helps startups and growing businesses scale faster with cloud-native architecture and DevOps solutions.\n"
                            "6. Tone: warm, professional, conversational.\n"
                            "7. End with a friendly call-to-connect.\n"
                            "8. Do not write like an email — no 'Best regards', no signatures.\n"
                            "9. Output only the final message."
                        )

                        user_prompt = (
                            f"Write a concise LinkedIn connection note for {details['first_name']}, "
                            f"{details['title']} at {details['company']}."
                        )
                       


                        try:
                            response = gemini([
                                SystemMessage(content=system_prompt),
                                HumanMessage(content=user_prompt)
                            ])
                            message = response.content.strip()
                        except Exception as gemini_err:
                            print(f"⚠️ Gemini failed: {str(gemini_err)}")
                            message = f"Hi {details['first_name']}, let's connect!"

                        df.at[index, "Message Sent"] = message

                        note_area.clear()
                        note_area.send_keys(message)
                        time.sleep(7)

                        send_btn = wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Send now') or span[text()='Send']]"))
                        )
                        driver.execute_script("arguments[0].click();", send_btn)  # safer click 

                        # 🔹 Mark connection success WITH note
                        df.at[index, "Connected"] = "✅"
                        df.at[index, "Note Sent"] = "✅"
                        print(f"✅ Connected WITH note sent: '{message}' for {url}")
                        time.sleep(10)

                    except Exception as e:
                        print(f"⚠️ Note/send failed: {url} (Error: {str(e)})")
                        try:
                            send_without_note = driver.find_element(
                                By.XPATH, "//button[contains(@aria-label, 'Send without a note') or contains(text(), 'Send without a note')]"
                            )
                            send_without_note.click()

                            #  Mark connection success WITHOUT note
                            df.at[index, "Connected"] = "✅"
                            df.at[index, "Note Sent"] = "❌"
                            df.at[index, "Message Sent"] = "Sent without note"
                            print(f"✅ Connected WITHOUT note: {url}")
                            time.sleep(10)
                        except:
                            pass

            # Save after each profile
            current_profile_df = df.iloc[[index]]
            self.append_results_to_file(current_profile_df)
            print(f"✅ Profile {profile_number} completed and added to results.")

            if index < len(df) - 1:
                wait_minutes = 5
                print(f"⏳ Waiting {wait_minutes} minutes before next profile...")
                for minute in range(wait_minutes, 0, -1):
                    print(f"⏳ {minute} minutes remaining...")
                    print()
                    time.sleep(60)
                print("✅ Wait complete. Processing next profile...")

        print("🔹 Current batch completed!")
        self.append_results_to_file(df)
        final_df = self.load_existing_results()
        print(f"📊 Total records in result.xlsx: {len(final_df)}")

# Run

actions = LinkedInActions(driver, wait)
csv_file = r"C:/Users/X1/Downloads/one_data.csv"
actions.process_profiles(csv_file)
driver.quit()
print("👍 Done!")
