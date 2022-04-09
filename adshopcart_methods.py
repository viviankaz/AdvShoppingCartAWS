import datetime
import sys
import adshopcart_locators as locators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=options)


def setUp():
    print(f'Test of ASC website started at {datetime.datetime.now()}')

    driver.maximize_window()

    # Let's wait for the browser response in general
    driver.implicitly_wait(30)

    # Navigating to the ASC website
    driver.get(locators.advantage_shopping_cart_url)

    # Three ways to indicate non-breaking space in code as follows.
    # if driver.current_url == locators.advantage_shopping_cart_url and driver.title == ' Advantage Shopping':
    # if driver.current_url == locators.advantage_shopping_cart_url and driver.title == '\xa0Advantage Shopping':
    if driver.current_url == locators.advantage_shopping_cart_url and driver.title == '\u00A0Advantage Shopping':
        print(f'We are at ASC homepage -- {driver.current_url}. The title of ASC homepage -- {driver.title}')
    else:
        print(f"Fail to navigate to homepage of ASC. Please check your code. ")


def tearDown():
    if driver is not None:
        print(f'Test of ASC website completed at {datetime.datetime.now()}')
        driver.close()
        driver.quit()


def register_new_account():
    assert driver is not None
    assert driver.current_url == locators.advantage_shopping_cart_url
    assert driver.find_element(By.ID, "hrefUserIcon").is_displayed()
    driver.find_element(By.ID, "hrefUserIcon").click()
    sleep(4)
    driver.find_element(By.LINK_TEXT, "CREATE NEW ACCOUNT").click()
    sleep(0.25)
    driver.find_element(By.XPATH, "//input[@name='usernameRegisterPage']").send_keys(locators.user_name)
    driver.find_element(By.XPATH, "//input[@name='emailRegisterPage']").send_keys(locators.email)
    driver.find_element(By.XPATH, "//input[@name='passwordRegisterPage']").send_keys(locators.password)
    driver.find_element(By.XPATH, "//input[@name='confirm_passwordRegisterPage']").send_keys(locators.password)

    driver.find_element(By.XPATH, "//input[@name='first_nameRegisterPage']").send_keys(locators.first_name)
    driver.find_element(By.XPATH, "//input[@name='last_nameRegisterPage']").send_keys(locators.last_name)
    driver.find_element(By.XPATH, "//input[@name='phone_numberRegisterPage']").send_keys(locators.phone_number)

    Select(driver.find_element(By.XPATH, "//select[@name='countryListboxRegisterPage']")).select_by_visible_text("Canada")
    driver.find_element(By.XPATH, "//input[@name='cityRegisterPage']").send_keys(locators.city)
    driver.find_element(By.XPATH, "//input[@name='addressRegisterPage']").send_keys(locators.street_address)
    driver.find_element(By.XPATH, "//input[@name='state_/_province_/_regionRegisterPage']").send_keys(locators.province)
    driver.find_element(By.XPATH, "//input[@name='postal_codeRegisterPage']").send_keys(locators.postal_code)

    sleep(0.5)
    if not driver.find_element(By.XPATH, "//input[@name='i_agree']").is_selected():
        assert not driver.find_element(By.ID, "register_btnundefined").is_enabled()
        driver.find_element(By.XPATH, "//input[@name='i_agree']").click()

    driver.find_element(By.ID, "register_btnundefined").click()
    sleep(1)
    print(f"-----Create new user account passed-----. Username created: {locators.user_name}")


def check_new_user_info():
    # check my account for user_name.
    assert driver.find_element(By.XPATH, f"//span[text()='{locators.user_name}']") is not None
    driver.find_element(By.ID, "hrefUserIcon").click()
    sleep(0.25)
    element = driver.find_element(By.XPATH, "//label[contains(., 'My account')]")
    driver.execute_script("arguments[0].click();", element)
    sleep(1)
    assert driver.find_element(By.XPATH, f"//label[contains(., '{locators.full_name}')]").is_displayed()
    assert driver.find_element(By.XPATH, f"//h3[contains(., 'Account details')]/../div/div/label[contains(., '{locators.full_name}')]").is_displayed()
    print(f"My account page is good with right full name displayed: {locators.full_name}")

    # check my order is empty
    driver.find_element(By.ID, "hrefUserIcon").click()
    sleep(0.25)
    element = driver.find_element(By.XPATH, "//label[contains(., 'My orders')]")
    driver.execute_script("arguments[0].click();", element)
    assert driver.find_element(By.XPATH, "//label[text()=' - No orders - ']").is_displayed()
    print(f"My orders page is good with no order. Username: {locators.user_name}")

    print(f"-----Check new user account and order page passed----- Username: {locators.user_name}")


def sign_out():
    driver.find_element(By.ID, "hrefUserIcon").click()
    sleep(0.25)
    element = driver.find_element(By.XPATH, "//label[contains(., 'Sign out')]")
    driver.execute_script("arguments[0].click();", element)
    sleep(3)
    print(f"-----Sign out passed----- from username: {locators.user_name}")


def sign_in_with_right_credentials(username, password):
    assert driver is not None
    assert driver.find_element(By.ID, "hrefUserIcon").is_displayed()
    driver.find_element(By.ID, "hrefUserIcon").click()
    sleep(2)
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    driver.find_element(By.ID, "sign_in_btnundefined").click()
    assert driver.find_element(By.XPATH, f"//span[text()='{username}']") is not None
    print(f"-----Sign in passed----- username: {username}")


def sign_in_with_wrong_credentials(username, password):
    assert driver is not None
    assert driver.find_element(By.ID, "hrefUserIcon").is_displayed()
    driver.find_element(By.ID, "hrefUserIcon").click()
    sleep(2)
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    driver.find_element(By.ID, "sign_in_btnundefined").click()
    assert driver.find_element(By.XPATH, "//label[text()='Incorrect user name or password.']") is not None
    print(f"-----Sign in with wrong credential passed----- wrong credentials : {username}")


def delete_account():
    driver.find_element(By.ID, "hrefUserIcon").click()
    sleep(0.25)
    element = driver.find_element(By.XPATH, "//label[contains(., 'My account')]")
    driver.execute_script("arguments[0].click();", element)
    sleep(0.25)
    driver.find_element(By.XPATH, "//button[contains(., 'Delete Account')]").click()
    sleep(5)
    # driver.find_element(By.XPATH, "//div[text()='YES']").click()
    driver.find_element(By.XPATH, "//div[@class='deletePopupBtn deleteRed']").click()
    sleep(6)
    print(f"-----Delete user account passed----- deleted user account : {locators.user_name}")


def check_categories():
    assert driver is not None
    assert driver.current_url == locators.advantage_shopping_cart_url
    # assert driver.find_element(By.XPATH, "//span[text()='SPEAKERS']").is_displayed()
    # assert driver.find_element(By.XPATH, "//span[text()='TABLETS']").is_displayed()
    # assert driver.find_element(By.XPATH, "//span[text()='LAPTOPS']").is_displayed()
    # assert driver.find_element(By.XPATH, "//span[text()='MICE']").is_displayed()
    # assert driver.find_element(By.XPATH, "//span[text()='HEADPHONES']").is_displayed()

    driver.find_element(By.XPATH, "//span[text()='SPEAKERS']").click()
    sleep(0.25)
    assert driver.current_url == locators.speaker_category_url
    assert driver.find_element(By.XPATH, "//h3[contains(., 'SPEAKERS')]").is_displayed()
    driver.find_element(By.XPATH, "//a[@href='#/']").click()
    sleep(0.25)
    assert driver.current_url == locators.advantage_shopping_cart_url

    driver.find_element(By.XPATH, "//span[text()='TABLETS']").click()
    sleep(0.25)
    assert driver.current_url == locators.tablets_category_url
    assert driver.find_element(By.XPATH, "//h3[contains(., 'TABLETS')]").is_displayed()
    driver.find_element(By.XPATH, "//a[@href='#/']").click()
    sleep(0.25)
    assert driver.current_url == locators.advantage_shopping_cart_url

    driver.find_element(By.XPATH, "//span[text()='LAPTOPS']").click()
    sleep(0.25)
    assert driver.current_url == locators.laptops_category_url
    assert driver.find_element(By.XPATH, "//h3[contains(., 'LAPTOPS')]").is_displayed()
    driver.find_element(By.XPATH, "//a[@href='#/']").click()
    sleep(0.25)
    assert driver.current_url == locators.advantage_shopping_cart_url

    driver.find_element(By.XPATH, "//span[text()='MICE']").click()
    sleep(0.25)
    assert driver.current_url == locators.mice_category_url
    assert driver.find_element(By.XPATH, "//h3[contains(., 'MICE')]").is_displayed()
    driver.find_element(By.XPATH, "//a[@href='#/']").click()
    sleep(0.25)
    assert driver.current_url == locators.advantage_shopping_cart_url

    driver.find_element(By.XPATH, "//span[text()='HEADPHONES']").click()
    sleep(0.25)
    assert driver.current_url == locators.headphone_category_url
    assert driver.find_element(By.XPATH, "//h3[contains(., 'HEADPHONES')]").is_displayed()
    driver.find_element(By.XPATH, "//a[@href='#/']").click()
    sleep(0.25)
    assert driver.current_url == locators.advantage_shopping_cart_url

    print("-----Check categories passed-----Navigate to urls successfully")


def check_main_logo():
    assert driver is not None
    assert driver.find_element(By.XPATH, "//*[local-name()='svg' and @id='Layer_1']/*[local-name()='path']").is_displayed()
    assert driver.find_element(By.XPATH, "//span[text()='dvantage']").is_displayed()
    assert driver.find_element(By.XPATH, "//span[text()='DEMO']").is_displayed()
    print("-----Check main logo passed-----Displayed properly")


def check_top_navi_menu():
    assert driver is not None
    assert driver.current_url == locators.advantage_shopping_cart_url
    driver.find_element(By.XPATH, "//a[text()='SPECIAL OFFER']").click()
    sleep(1)
    driver.find_element(By.XPATH, "//a[text()='POPULAR ITEMS']").click()
    sleep(1)
    driver.find_element(By.XPATH, "//a[text()='CONTACT US']").click()
    sleep(1)
    driver.find_element(By.XPATH, "//a[text()='OUR PRODUCTS']").click()
    sleep(1)
    print("-----Check top navi menu passed-----Clickable")


def check_contact_form():
    assert driver is not None
    assert driver.current_url == locators.advantage_shopping_cart_url

    # check title, that send is disabled at the beginning.
    assert driver.find_element(By.XPATH, "//h1[text()='CONTACT US']").is_displayed()
    assert not driver.find_element(By.ID, "send_btnundefined").is_enabled()

    # fill in mandatory fields.
    driver.find_element(By.NAME, "subjectTextareaContactUs").send_keys(locators.subject)
    driver.find_element(By.NAME, "emailContactUs").send_keys(locators.email)
    assert driver.find_element(By.ID, "send_btnundefined").is_enabled()

    # fill in optional fields.
    Select(driver.find_element(By.NAME, "categoryListboxContactUs")).select_by_visible_text("Laptops")
    Select(driver.find_element(By.NAME, "productListboxContactUs")).select_by_visible_text("HP ENVY - 17t Touch Laptop")

    # click send button and check behavior
    driver.find_element(By.ID, "send_btnundefined").click()
    sleep(0.5)
    assert driver.find_element(By.XPATH, "//a[text()=' CONTINUE SHOPPING ']").is_displayed()

    print(f"-----Check contact form passed-----Submitted message with email: {locators.email}, subject: {locators.subject}")



