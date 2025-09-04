# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # Dynamically get the default Chrome user data directory (adjust if not Windows)
# # username = "X1"  # Gets your current Windows username
# user_data_dir = f"C:\SeleniumProfile"

# options = Options()
# options.add_argument(f"--user-data-dir={user_data_dir}")  # Path to default Chrome user data
# options.add_argument("--profile-directory=Default")        # Targets the default profile
# options.add_argument("--remote-debugging-port=9222")       # Needed to attach
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get("https://www.linkedin.com/feed/")
# time.sleep(5)

# try:
#     wait = WebDriverWait(driver, 20)
#     # Note: If already logged in via the profile, these steps might not run or could error—check manually
#     email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
#     email_input.send_keys("brijeshshah19@gmail.com")

#     password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
#     password_input.send_keys("NextGen@1")

#     login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
#     login_btn.click()
#     print("Login attempted. Waiting for home page...")

#     # wait.until(EC.url_contains("linkedin.com/feed"))

#     # print("✅ Feed page opened.")

#     # === Click the Apollo.io icon ===
#     apollo_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Apollo.io']")))
#     apollo_icon.click()
#     print("✅ Apollo.io icon clicked!")

#     # Wait a bit to see the result
#     time.sleep(20)


#     time.sleep(500)
# except Exception as e:
#     print(f"Login error: {e}")
#     driver.quit()
#     # exit()


# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # Use a raw string for Windows path
# user_data_dir = r"C:\SeleniumProfile"

# options = Options()
# options.add_argument(f"--user-data-dir={user_data_dir}")
# options.add_argument("--profile-directory=Default")
# options.add_argument("--start-maximized")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# try:
#     driver.get("https://www.linkedin.com/feed/")
#     wait = WebDriverWait(driver, 30)

#     # === If login page appears ===
#     if "login" in driver.current_url.lower():
#         email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
#         email_input.send_keys("brijeshshah19@gmail.com")

#         password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
#         password_input.send_keys("NextGen@1")

#         login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
#         login_btn.click()

#         wait.until(EC.url_contains("linkedin.com/feed"))
#         print("✅ Logged in successfully.")

#     print("✅ Feed page opened. Looking for Apollo.io...")

#     # === Locate and click Apollo.io icon ===
#     apollo_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Apollo')]")))
    
#     # Scroll into view
#     driver.execute_script("arguments[0].scrollIntoView(true);", apollo_icon)
#     time.sleep(1)

#     # Click with JS (works even if overlay blocks it)
#     driver.execute_script("arguments[0].click();", apollo_icon)

#     print("✅ Apollo.io icon clicked!")

#     time.sleep(20)

# except Exception as e:
#     print(f"❌ Error: {e}")
# finally:
#     driver.quit()




# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # === Setup Chrome with saved profile (persistent session) ===
# user_data_dir = r"C:\SeleniumProfile"   # keep same folder so Apollo session is saved
# options = Options()
# options.add_argument(f"--user-data-dir={user_data_dir}")
# options.add_argument("--profile-directory=Default")
# options.add_argument("--remote-debugging-port=9222")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get("https://www.linkedin.com/feed/")

# wait = WebDriverWait(driver, 30)

# try:
#     # === Step 1: Click Apollo icon inside LinkedIn ===
#     apollo_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Apollo.io']")))
#     apollo_icon.click()
#     print("✅ Apollo icon clicked")
#     time.sleep(5)

#     # === Step 2: If Apollo login page appears (manual login + verify) ===
#     try:
#         login_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
#         print("⚠️ Please login to Apollo manually (and complete human verification)...")
#         # Wait for you to finish login manually
#         while True:
#             try:
#                 # Once Apollo popup main UI is visible → break
#                 wait.until(EC.presence_of_element_located(
#                     (By.XPATH, "//div[contains(@class,'apollo-extension')]")
#                 ))
#                 print("✅ Apollo login completed, continuing...")
#                 break
#             except:
#                 time.sleep(3)
#     except:
#         print("✅ Already logged into Apollo, continuing...")

#     # === Step 3: Click the 3-dot button inside Apollo popup ===
#     three_dot_btn = wait.until(EC.element_to_be_clickable(
#         (By.XPATH, "/html/body/div/div[1]/div/div/div/div[1]/div/div[1]/button")
#     ))
#     three_dot_btn.click()
#     print("✅ 3-dot button clicked")

#     time.sleep(2)

#     # === Step 4: Click the menu item ===
#     menu_item = wait.until(EC.element_to_be_clickable(
#         (By.XPATH, "/html/body/div/div[1]/div/div/div/div[4]/div[2]/div[1]/div[1]/ul/div[1]/li/div")
#     ))
#     menu_item.click()
#     print("✅ Dropdown item clicked successfully")

#     time.sleep(10)

# except Exception as e:
#     print(f"❌ Error: {e}")
# finally:
#     driver.quit()



import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# === Persistent Chrome profile (stores LinkedIn + Apollo sessions) ===
user_data_dir = r"C:\SeleniumProfile"   # Keep SAME folder for all runs
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.linkedin.com/feed/")

wait = WebDriverWait(driver, 30)

try:
    # === Step 1: Ensure LinkedIn is open (session already stored here) ===
    print(" LinkedIn opened with stored session (if first time, login manually + CAPTCHA).")
    time.sleep(5)

    # === Step 2: Click Apollo icon inside LinkedIn ===
    apollo_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Apollo.io']")))
    apollo_icon.click()
    print(" Apollo icon clicked")
    time.sleep(5)

    # === Step 3: Handle Apollo login only first time ===
    try:
        login_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        print(" Apollo login required. Please enter email, password, and solve CAPTCHA manually...")
        # Wait until Apollo’s main UI loads → means login success
        while True:
            try:
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'apollo-extension')]")
                ))
                print(" Apollo login completed. Session saved for next runs.")
                break
            except:
                time.sleep(3)
    except:
        print(" Apollo already logged in. Continuing...")

    # === Step 4: Click the 3-dot button inside Apollo popup ===
    three_dot_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[1]/div/div/div/div[1]/div/div[1]/button")
    ))
    three_dot_btn.click()
    print(" 3-dot button clicked")

    time.sleep(2)

    # === Step 5: Click the menu item ===
    menu_item = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div/div[1]/div/div/div/div[4]/div[2]/div[1]/div[1]/ul/div[1]/li/div")
    ))
    menu_item.click()
    print(" Dropdown item clicked successfully")

    time.sleep(10)

except Exception as e:
    print(f" Error: {e}")
finally:
    driver.quit()



