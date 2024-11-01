from selenium.webdriver.common.by import By

class LoginLocators:
    USERNAME_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//*[@id='root']/div/section[2]/div/div/div[1]/form/div[3]/button")
    LOGOUT_BUTTON = (By.XPATH, "//*[@id='root']/div/main/section/div/article/div[2]/ul/li[5]/button")