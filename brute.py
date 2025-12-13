from selenium import webdriver
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By
import time

#s = Service(executable_path="/usr/local/bin/geckodriver.txt")
#driver = webdriver.Firefox(service=s)
driver = webdriver.Firefox()

website = "http://127.0.0.1:5000/login"

driver.get(website)

title=""

passwords = ["ssdad", "sniff", "pass", "xxx"] 
i = 0

for passw in passwords:
        print(f"Aktuelles Passwort: {passw}")
        time.sleep(0.1)
        res = driver.find_elements(By.CLASS_NAME, "form-control")
        print(f"Die länge: {len(res)}")
        assert(len(res) == 2)

        res[0].clear()
        res[0].send_keys("Musma")
        res[1].clear()
        res[1].send_keys(passw)

        button = driver.find_elements(By.CLASS_NAME, "btn")
        assert len(button) == 2
        button[0].click()
        print("Titlepage lautet:", driver.title)
        i =+ 1
        if driver.title != "Login Page":
                print("Passwd got FUUND:", passw)
                break

driver.quit()