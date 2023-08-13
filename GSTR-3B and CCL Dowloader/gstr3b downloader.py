from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tkinter import Tk, Label, Entry, Button, Variable
from PIL import ImageTk, Image

from time import sleep

user = 'BALAJIPACKPLAST'
passW = 'Balaji@2023'

driver = webdriver.Chrome()
driver.get("https://services.gst.gov.in/services/login")

try:

    user_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"username\"]"))) #driver.find_element(By.XPATH, "//*[@id=\"username\"]")
    user_ele.send_keys(user)


finally:
    print('ok')

passW_ele = driver.find_element(By.XPATH, "//*[@id=\"user_pass\"]")
passW_ele.send_keys(passW)


captchaImg_ele = driver.find_element(By.XPATH, "//*[@id=\"imgCaptcha\"]")
with open('captcha.png', 'wb') as file:
    file.write(captchaImg_ele.screenshot_as_png)

def ledger():
    services_ele = driver.find_element(By.XPATH, "/html/body/div[1]/ng-include[2]/nav/div/div/ul/li[2]/a")
    services_ele.click()

    ledger_ele = driver.find_element(By.XPATH, "/html/body/div[1]/ng-include[2]/nav/div/div/ul/li[2]/ul/li[2]/a")
    ledger_ele.click()

    #---- Fro Cash Ledger ----------
    cashLedger_ele = driver.find_element(By.XPATH. "/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div/ul/li[1]/a")
    cashLedger_ele.click()

    cashLedger_ele_inner = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div/li[1]/a")
    cashLedger_ele_inner.click()

    fromData_ele = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[3]/div/div[1]/div[1]/form/div/div[1]/div/input")
    toData_ele = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[3]/div/div[1]/div[1]/form/div/div[2]/div/input")
    goButton_ele = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[3]/div/div[1]/div[1]/form/div/div[3]/button")




def submitCaptcha():
    global driver
    captcha = img_e.get()
    print("captcha=", captcha)
    root.destroy()
    captcha_ele = driver.find_element(By.XPATH, "//*[@id=\"captcha\"]")
    captcha_ele.send_keys(captcha)

    submit_ele = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div/div/div/div/form/div[6]/div/button")
    submit_ele.submit()

    sleep(1)
    aler_ele = driver.find_element(By.XPATH, "/html/body/adhr-table/div/div/div/div[2]/a[2]")
    aler_ele.click()

    ledger()

sleep(1)

root = Tk()

img = ImageTk.PhotoImage(Image.open('captcha.png'))
img_l = Label(root, image=img)
img_l.grid(row=0, column=0, padx=4)

img_e = Entry(root)
img_e.grid(row=0, column=1)

b = Button(root, text='Submit', command=submitCaptcha)
b.grid(row=0, column=2, padx=4)



root.mainloop()