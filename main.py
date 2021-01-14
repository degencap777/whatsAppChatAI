from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random
import json

import torch

from ai.model import NeuralNet
from ai.nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('ai/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.model"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def send_message(driver, msg):
    box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
    box.send_keys(msg)
    driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()


def receiver(driver, name):
    latest_message = None
    while True:
        for x in driver.find_elements_by_class_name("_1dB-m"):
            el1 = x.find_elements_by_class_name("copyable-text")
            author = str(el1.__getitem__(0).get_attribute("data-pre-plain-text"))
            if author.endswith(f"{name}: "):
                el2 = el1.__getitem__(0).find_element_by_class_name("_1wlJG")
                el3 = el2.find_element_by_class_name("_1VzZY")
                if latest_message == str(el3.text):
                    print(latest_message)
                    latest_message = str(el3.text)
                    print(str(el3.text))
                    message_manager(driver=driver, message=latest_message)


def message_manager(driver, message):
    message = message.lower()
    print(message)
    if message == "quit":
        send_message(driver=driver, msg="Beendet")
        exit()

    message = tokenize(message)
    X = bag_of_words(message, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                send_message(driver=driver, msg=random.choice(intent['responses']))
    else:
        send_message(driver=driver, msg="I dont unterstand...")


def find_user(driver):
    try:
        name = input("Type your contact name here: ")

        user = driver.find_element_by_xpath(f"//span[@title='{name}']")
        user.click()
        return name
    except NoSuchElementException:
        print("User not found. Please retry")
        return find_user(driver=driver)


driver = webdriver.Chrome("C:\\Users\\lariv\\AppData\\Local\\Google\\Chrome\\User Data\\chromedriver.exe")
driver.get("https://web.whatsapp.com")
logged_in = False
while not logged_in:
    found = False
    for x in driver.find_elements_by_class_name("landing-title"):
        found = True
    if not found:
        logged_in = True
name = find_user(driver=driver)
receiver(driver=driver, name=name)
