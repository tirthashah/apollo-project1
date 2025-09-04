# import time
# import csv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from webdriver_manager.chrome import ChromeDriverManager

# # ✅ Use uploaded CSV file
# csv_file_path = r"C:/Users/X1/Downloads/one_data.csv"

# # LinkedIn credentials
# linkedin_email = "brijeshshah19@gmail.com"
# linkedin_password = "NextGen@1"

# # Chrome options
# user_data_dir = r"C:\SeleniumProfile"
# options = Options()
# options.add_argument(f"--user-data-dir={user_data_dir}")  # Optional custom profile
# options.add_argument("--profile-directory=Default")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")

# # Initialize WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# wait = WebDriverWait(driver, 20)

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

#     # Wait until feed/home loads
#     wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#     print("Login successful!")
# except Exception as e:
#     print(f"Login error: {e}")
#     time.sleep(5)

# # -----------------------------
# # Function to scroll down the page
# # -----------------------------
# def scroll_down():
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)

# # -----------------------------
# # 2️⃣ Process CSV LinkedIn URLs
# # -----------------------------
# with open(csv_file_path, mode='r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         linkedin_url = row.get('Person Linkedin Url')
#         if not linkedin_url:
#             print("No LinkedIn URL found in row.")
#             continue

#         print(f"\nProcessing profile: {linkedin_url}")
#         try:
#             # Step 1: Go to the profile
#             driver.get(linkedin_url)
#             wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#             time.sleep(2)

#             # Step 2: Scroll down
#             scroll_down()

#             # Step 3: Click the Follow button if present
#             follow_button_xpath = "//button[contains(@class, 'artdeco-button') and .//span[text()='Follow']]"
#             try:
#                 follow_button = wait.until(EC.element_to_be_clickable((By.XPATH, follow_button_xpath)))
#                 button_text = follow_button.find_element(By.XPATH, ".//span").text.strip()
#                 if button_text == "Follow":
#                     ActionChains(driver).move_to_element(follow_button).click(follow_button).perform()
#                     print(f"Successfully followed: {linkedin_url}")
#                     time.sleep(2)
#                 else:
#                     print(f"Already following: {linkedin_url}")
#             except:
#                 print(f"No Follow button for: {linkedin_url}")

#         except Exception as e:
#             print(f"Error opening profile {linkedin_url}: {e}")

# # -----------------------------
# # 3️⃣ Close browser
# # -----------------------------
# time.sleep(10)  # Keep open for review
# driver.quit()