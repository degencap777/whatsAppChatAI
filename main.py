from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def send_message(driver, msg):
    box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
    box.send_keys(msg)
    driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()


def receiver(driver, name):
    latest_message = None
    while True:
        for x in driver.find_elements_by_class_name("_1dB-m"):
            el1 = x.find_element_by_class_name("copyable-text")
            author = str(el1.get_attribute("data-pre-plain-text")).split(" ")[2].replace(":", "")
            if author == name:
                el2 = el1.find_element_by_class_name("_1wlJG")
                el3 = el2.find_element_by_class_name("_1VzZY")
                if latest_message == str(el3.text):
                    latest_message = str(el3.text)


def message_manager(driver, message):
    print(f"New message received: {message.lower()}")
    print("-" * 100)


def find_user(driver):
    try:
        name = input("Type your contact name here: ")

        user = driver.find_element_by_xpath(f"//span[@title='{name}']")
        user.click()
        return name
    except NoSuchElementException:
        print("User not found. Please retry")
        return find_user(driver=driver)


if __name__ == "__main__":
    driver = webdriver.Chrome("C:\\Users\\lariv\\AppData\\Local\\Google\\Chrome\\User Data\\chromedriver.exe")
    driver.get("https://web.whatsapp.com")

    logged_in = False
    while not logged_in:
        found = None
        for x in driver.find_elements_by_class_name("_1PTz1"):
            found = True
        if not found:
            logged_in = True

    name = find_user(driver=driver)

    receiver(driver=driver, name=name)
