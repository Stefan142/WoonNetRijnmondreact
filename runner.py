from helper import WoonnetBot
from selenium.webdriver.common.by import By
import time

def account_runner(username: str, password: str) -> None:
    """
    Function which handles the entire workflow of the project for the 
    account specified in the parameters.
    """
    bot = WoonnetBot(username, password)
    bot.open_website("https://www.woonnetrijnmond.nl/inloggeninschrijven/")
    bot.login()
    bot.click_element(By.CSS_SELECTOR, "a.header-nav__button--home")  # Ga Naar aanbod
    bot.wait_random()
    bot.react_to_houses(type_woning="DirectKans")
    time.sleep(10)
    bot.close()
    time.sleep(10)