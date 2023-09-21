from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


#init driver - setup
options= Options()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
action=ActionChains(driver)

#step1 : Launch of the application URL(https://www.bt.com/)
driver.get("https://www.bt.com/")
driver.maximize_window()
time.sleep(3)

#step2 : Close accept Cookie pop-up if it appears
iframe=driver.find_element(by=By.TAG_NAME,value="IFRAME")
driver.switch_to.frame(iframe)
cookie=driver.find_element(by=By.XPATH,value="//a[text()='Accept all cookies']")
action.click(cookie).perform()
driver.switch_to.parent_frame()
time.sleep(3)

#step3 : Hover to Mobile menu
mobile=driver.find_element(by=By.XPATH , value= "//span[text()='Mobile']")
action.move_to_element(mobile).perform()

#step4: From mobile menu, select Mobile phones
time.sleep(3)
phones=driver.find_element(by=By.XPATH, value= "//a[@href='https://www.bt.com/products/mobile/phones/']")
action.click(phones).perform()

#step5: Verify the numbers of banners present below “See Handset details” should not be less than 3
parent_div = driver.find_element(by=By.XPATH , value= "//div[@class='flexpay_flexpaycard_container__GnRx9']")
count_of_divs = len(parent_div.find_elements(by=By.XPATH, value="./div"))
print("| INFO : Numbers of banners present below “See Handset details” : {} |".format(count_of_divs))
if count_of_divs < 3:
    raise Exception("Numbers of banners present below 'See Handset details' is < 3")

#step6: Scroll down and click View SIM only deals
time.sleep(3)
sim_deals=driver.find_element(by=By.XPATH, value= "//a[text()='View SIM only deals']")
driver.execute_script("arguments[0].scrollIntoView(true);",sim_deals)
time.sleep(5)
action.click(sim_deals).perform()

#step7 :Validate the title for new page
if driver.title:
   print('Title: ' ,driver.title)
   print('| INFO : New Page Title Validated |')
   time.sleep(3)
else:
   print('| INFO : New Page Title Invalid |')
   raise Exception("New Page Title Invalid")


#step8 : Validate “30% off and double data” was 125GB 250GB Essential Plan, was £27 £18.90 per month
val=driver.find_element(by=By.XPATH,value="//span[normalize-space()='was 125GB']/following-sibling::div[normalize-space()='250GB']/ancestor::div[contains(@class,'simo-card-ee_plan_details')]//span[normalize-space()='was £27']/following-sibling::div/sub[text()='£']/parent::div[text()='18']/ancestor::div[contains(@class,'simo-card-ee_text_container')]/preceding-sibling::div[normalize-space()='30% off and double data']")
if val:
    print("Expected String Present")
else:
   print("Expected String not Present")

#step9 : Close the browser & exit / teardown
driver.quit()
