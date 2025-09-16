


# follow button click code

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# ✅ CSV file path
csv_file_path = r"C:/Users/X1/Downloads/one_data.csv"

# LinkedIn credentials
linkedin_email = "brijeshshah19@gmail.com"
linkedin_password = "NextGen@1"

# Chrome options
user_data_dir = r"C:\SeleniumProfile"
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--enable-unsafe-swiftshader")  # added for your GPU warning

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# -----------------------------
# 1️⃣ Login to LinkedIn
# -----------------------------
driver.get("https://www.linkedin.com/login")
try:
    email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    email_input.send_keys(linkedin_email)

    password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password_input.send_keys(linkedin_password)

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_btn.click()

    # Wait until feed/home loads
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Login successful!")
except Exception as e:
    print(f"❌ Login error: {e}")
    time.sleep(5)

# -----------------------------
# 2️⃣ Process CSV LinkedIn URLs
# -----------------------------
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        linkedin_url = row.get('Person Linkedin Url')
        if not linkedin_url:
            print("⚠️ No LinkedIn URL found in row.")
            continue

        print(f"\n➡️ Processing profile: {linkedin_url}")
        try:
            # Step 1: Go to the profile
            driver.get(linkedin_url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(5)

            # Step 2: Locate "Follow" button dynamically by text
            follow_button_xpath = "(//span[@class='artdeco-button__text'][normalize-space()='Follow'])[2]"

            try:
                follow_button = None

                # Try multiple scroll attempts until button appears
                for i in range(3):  # max 3 scrolls
                    try:
                        follow_button = wait.until(
                            EC.visibility_of_element_located((By.XPATH, follow_button_xpath))
                        )
                        if follow_button:
                            break
                    except:
                        driver.execute_script("window.scrollBy(0, 150);")  # scroll down
                        time.sleep(5)

                if follow_button:
                    # Scroll to the Follow button
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", follow_button)
                    time.sleep(1)

                    # Wait until clickable
                    wait.until(EC.element_to_be_clickable((By.XPATH, follow_button_xpath)))

                    button_text = follow_button.text.strip()
                    if button_text == "Follow":
                        ActionChains(driver).move_to_element(follow_button).click(follow_button).perform()
                        print(f"✅ Successfully followed: {linkedin_url}")
                        time.sleep(5)
                    else:
                        print(f"⚠️ Already following: {linkedin_url}")
                else:
                    print(f"❌ Follow button not found even after scrolling: {linkedin_url}")

            except Exception as e:
                print(f"❌ No Follow button for: {linkedin_url} ({e})")

        except Exception as e:
            print(f"❌ Error opening profile {linkedin_url}: {e}")

# -----------------------------
# 3️⃣ Close browser
# -----------------------------
time.sleep(10)  # Keep open for review
driver.quit()


#send without note direct code from inside more and then click on the connect and send request without notes

# import time
# import csv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # ✅ CSV file path
# csv_file_path = r"C:/Users/X1/Downloads/one_data.csv"
# # output_file_path = r"C:/Users/X1/Downloads/one_data_results.csv"

# # LinkedIn credentials
# linkedin_email = "brijeshshah19@gmail.com"
# linkedin_password = "NextGen@1"

# # Chrome options
# user_data_dir = r"C:\SeleniumProfile"
# options = Options()
# options.add_argument(f"--user-data-dir={user_data_dir}")
# options.add_argument("--profile-directory=Default")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
# options.add_argument("--enable-unsafe-swiftshader")

# # Initialize WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# wait = WebDriverWait(driver, 15)

# # -----------------------------
# # 1️⃣ Login to LinkedIn
# # -----------------------------
# driver.get("https://www.linkedin.com/login")
# try:
#     email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
#     email_input.send_keys(linkedin_email)

#     password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
#     password_input.send_keys(linkedin_password)

#     login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
#     login_btn.click()

#     wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#     print("✅ Login successful!")
# except Exception as e:
#     print(f"❌ Login error: {e}")
#     time.sleep(5)

# # -----------------------------
# # 2️⃣ Process CSV LinkedIn URLs
# # -----------------------------
# results = []
# with open(csv_file_path, mode='r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         linkedin_url = row.get('Person Linkedin Url')
#         status = "❌ Failed"
        
#         if not linkedin_url:
#             status = "⚠️ No URL"
#             results.append({**row, "Status": status})
#             continue

#         print(f"\n➡️ Processing profile: {linkedin_url}")
#         try:
#             driver.get(linkedin_url)
#             wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#             time.sleep(3)

#             # Check if it's a company page
#             try:
#                 driver.find_element(By.XPATH, "//div[contains(@class,'org-top-card-summary')]")
#                 status = "❌ Skipped (Company)"
#                 print(status)
#                 results.append({**row, "Status": status})
#                 continue
#             except:
#                 pass  # Not a company → proceed

#             # -----------------------------
#             # 🔑 Click "More" button safely
#             # -----------------------------
#             try:
#                 driver.execute_script("window.scrollTo(0, 200);")  # just enough scroll
#                 time.sleep(10)

#                 more_button_xpath = "(//span[contains(text(),'More')])[2]"
#                 more_button = wait.until(EC.element_to_be_clickable((By.XPATH, more_button_xpath)))
                
#                 # safer click with JS
#                 driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_button)
#                 driver.execute_script("arguments[0].click();", more_button)
#                 print("✅ Opened 'More' menu")
#                 time.sleep(3)

#                 # -----------------------------
#                 # Click "Connect"
#                 # -----------------------------
#                 connect_xpath = "//div[contains(@class,'artdeco-dropdown__content')]//span[normalize-space()='Connect']"
#                 connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, connect_xpath)))
#                 driver.execute_script("arguments[0].click();", connect_button)
#                 print(f"✅ 'Connect' clicked for: {linkedin_url}")
#                 time.sleep(3)

#                 # -----------------------------
#                 # Click "Send without a note"
#                 # -----------------------------
#                 try:
#                     send_without_note_xpath = "//span[normalize-space()='Send without a note']"
#                     send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_without_note_xpath)))
#                     driver.execute_script("arguments[0].click();", send_button)
#                     status = "✅ Connected"
#                     print(f"🎉 Connection request sent: {linkedin_url}")
#                     time.sleep(3)
#                 except:
#                     status = "⚠️ Cannot find 'Send without a note'"
#                     print(f"⚠️ Send without a note not found: {linkedin_url}")
#                     time.sleep(3)

#             except Exception as e:
#                 status = "❌ No 'Connect' option"
#                 print(f"⚠️ Connect not available on: {linkedin_url} ({e})")

#         except Exception as e:
#             status = "❌ Error opening profile"
#             print(f"❌ Error: {linkedin_url} ({e})")

#         results.append({**row, "Status": status})

# # -----------------------------
# # 3️⃣ Save results to new CSV (optional)
# # -----------------------------
# # fieldnames = list(results[0].keys()) if results else []
# # with open(output_file_path, mode='w', newline='', encoding='utf-8') as out_file:
# #     writer = csv.DictWriter(out_file, fieldnames=fieldnames)
# #     writer.writeheader()
# #     writer.writerows(results)

# # print(f"\n📁 Results saved to: {output_file_path}")

# # -----------------------------
# # 4️⃣ Close browser
# # -----------------------------
# time.sleep(5)
# driver.quit()



#If condition is woking :- when the connect button shows outside the more then directly click on that and if not outside then go into more and then check 


# import time
# import csv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # CSV file path
# csv_file_path = r"C:/Users/X1/Downloads/one_data.csv"

# # LinkedIn credentials


# # Chrome options
# user_data_dir = r"C:\SeleniumProfile"
# options = Options()
# options.add_argument(f"--user-data-dir={user_data_dir}")
# options.add_argument("--profile-directory=Default")

# # Initialize WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# wait = WebDriverWait(driver, 15)


# #  Login to LinkedIn

# driver.get("https://www.linkedin.com/login")
# try:
#     email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
#     email_input.send_keys(linkedin_email)

#     password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
#     password_input.send_keys(linkedin_password)

#     login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
#     login_btn.click()

#     wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#     print(" Login successful!")
# except Exception as e:
#     print(f" Login error: {e}")
#     time.sleep(5)

# # -----------------------------
# # 2️⃣ Process CSV LinkedIn URLs
# # -----------------------------
# results = []
# with open(csv_file_path, mode='r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         linkedin_url = row.get('Person Linkedin Url')
#         status = " Failed"
        
#         if not linkedin_url:
#             status = " No URL"
#             results.append({**row, "Status": status})
#             continue

#         print(f"\n Processing profile: {linkedin_url}")
#         try:
#             driver.get(linkedin_url)
#             wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#             time.sleep(5)

#             # Skip if it's a company page
#             try:
#                 driver.find_element(By.XPATH, "//div[contains(@class,'org-top-card-summary')]")
#                 status = "Skipped (Company)"
#                 print(status)
#                 results.append({**row, "Status": status})
#                 continue
#             except:
#                 pass

#             connected = False

         
#             #  Try inside "More" first
           
#             try:
#                 more_button_xpath = "(//span[contains(text(),'More')])[2]"
#                 more_button = wait.until(EC.element_to_be_clickable((By.XPATH, more_button_xpath)))
#                 driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_button)
#                 driver.execute_script("arguments[0].click();", more_button)
#                 print("Opened 'More' menu")
#                 time.sleep(5)

#                 connect_inside_xpath = "(//span[@class='display-flex t-normal flex-1'][normalize-space()='Connect'])[2]"
#                 connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, connect_inside_xpath)))
#                 driver.execute_script("arguments[0].click();", connect_button)
#                 print(f" Clicked 'Connect' (inside More) for: {linkedin_url}")
#                 time.sleep(5)
#                 connected = True
#             except:
#                 print(" Connect not found inside More, checking outside...")

           
#             # If not inside, then try outside
           
#             if not connected:
#                 try:
#                     connect_outside_xpath = "(//span[@class='artdeco-button__text'][normalize-space()='Connect'])[2]"
#                     connect_button = wait.until(EC.element_to_be_clickable((By.XPATH, connect_outside_xpath)))
#                     driver.execute_script("arguments[0].scrollIntoView({block:'center'});", connect_button)
#                     driver.execute_script("arguments[0].click();", connect_button)
#                     print(f" Clicked 'Connect' (outside More) for: {linkedin_url}")
#                     time.sleep(5)
#                     connected = True
#                 except:
#                     status = "No 'Connect' option"
#                     print(f" Connect not available on: {linkedin_url}")
#                     results.append({**row, "Status": status})
#                     continue
#             #Send without a note (if Connect was clicked)
#             if connected:
#                 try:
#                     send_without_note_xpath = "//span[normalize-space()='Send without a note']"
#                     send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_without_note_xpath)))
#                     driver.execute_script("arguments[0].click();", send_button)
#                     time.sleep(5)
#                     status = "Connected"
#                     print(f" Connection request sent: {linkedin_url}")
#                 except:
#                     status = " Cannot find 'Send without a note'"
#                     print(f" Send without a note not found: {linkedin_url}")

#         except Exception as e:
#             status = " Error opening profile"
#             print(f" Error: {linkedin_url} ({e})")

#         results.append({**row, "Status": status})
# time.sleep(5)
# driver.quit()

#this is with note add  that person and related personalized msg given 
import time
import csv
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

# -----------------------------
# Chrome Options
# -----------------------------
user_data_dir = r"C:\SeleniumProfile"
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default")

# -----------------------------
# Initialize WebDriver
# -----------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# -----------------------------
# Login to LinkedIn
# -----------------------------
driver.get("https://www.linkedin.com/login")
try:
    email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    email_input.send_keys(linkedin_email)

    password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password_input.send_keys(linkedin_password)

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_btn.click()

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("✅ Login successful!")
except Exception as e:
    print(f"❌ Login error: {e}")
    time.sleep(5)

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
                    # ✅ Click "Add a note"
                    add_note_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add a note']")))
                    add_note_btn.click()
                    time.sleep(5)

                    # ✅ Custom message
                    message = (
    f"Hi {first_name}, I’ve been following {company} and truly admire the way you’re growing the team and product. "
    f"At NextGenSoft, we help organizations scale faster with cloud-native architecture & DevOps while keeping reliability in focus. "
    f"I’d be glad to connect, exchange a few ideas, and learn about your growth journey."
)
                    # ✅ Type into textarea
                    note_textarea = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='message']")))
                    note_textarea.clear()
                    note_textarea.send_keys(message)
                    time.sleep(100)

                    # ✅ Click Send
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

#this details should show all the  about functionlaity