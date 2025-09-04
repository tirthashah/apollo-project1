# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time


# def apollo_login_with_temp_profile():
#     # ✅ Chrome Options बनाएं
#     options = webdriver.ChromeOptions()

#     # ✅ User Data folder use करें (ताकि extension properly load हो)
#     options.add_argument(r"--user-data-dir=C:\Users\X1\AppData\Local\Google\Chrome\User Data")
#     options.add_argument(r'--profile-directory=Default')  

#     # ✅ Apollo extension path दें (manifest.json वाला फोल्डर path)
#     options.add_argument(r"--load-extension=C:\Users\X1\Downloads\apollo_extension")

#     # ✅ Chrome driver create करें
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     driver.maximize_window()
#     driver.get("https://www.linkedin.com/login")

#     wait = WebDriverWait(driver, 20)

#     try:
#         # ✅ Login process
#         email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
#         email_input.send_keys("brijeshshah19@gmail.com")

#         password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
#         password_input.send_keys("NextGen@1")

#         login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
#         login_btn.click()

#         time.sleep(15)  # Extension और LinkedIn load होने का समय
#         print("✅ LinkedIn login successful! Apollo.io extension should be visible now.")

#     except Exception as e:
#         print(f"❌ Error occurred: {e}")
#     finally:
#         pass
#         # driver.quit()  # अगर test के बाद browser बंद करना हो तो uncomment करें


# if __name__ == "__main__":
#     apollo_login_with_temp_profile()




from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to your ChromeDriver
service = Service("C:/Users/X1/Selenium/apollo/chromedriver.exe")

options = Options()

# Add unpacked extension (IMPORTANT: forward slashes /)
options.add_argument("load-extension=C:/Users/X1/Downloads/apollo_extension")

# Prevent Chrome "disable developer mode extension" popup
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com")
