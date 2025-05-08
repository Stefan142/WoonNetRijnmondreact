import requests
import time
import numpy as np
import tempfile
import shutil
import os
import signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException


class WoonnetBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_data_dir = tempfile.mkdtemp()

        # Configure Firefox options
        firefox_options = Options()
        # firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument('--headless')
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.set_preference("dom.webdriver.enabled", False)  # Bypass detection
        firefox_options.set_preference("useAutomationExtension", False)
        firefox_options.set_preference(
            "general.useragent.override", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0",
        )

        # Initialize the WebDriver
        service = Service("/usr/local/bin/geckodriver")  # Explicitly specify the path to geckodriver
        self.driver = webdriver.Firefox(service=service, options=firefox_options)

    def wait_random(self):
        """Random waiting time, reduces likelihood of bot detection."""
        time.sleep(np.random.uniform(1, 1.5))

    def open_website(self, url: str) -> None:
        """Assigns a website to the state of the driver."""
        self.wait_random()
        self.driver.get(url)

    def login(self) -> None:
        """Login step of the workflow."""
        try:
            # Wait for the username input field to be present
            self.click_element(By.ID, "username")
            self.wait_random()
            input_username = self.driver.find_element(By.ID, "username")
            self.wait_random()
            input_password = self.driver.find_element(By.ID, "password")
            self.wait_random()
            input_username.send_keys(self.username)
            self.wait_random()
            input_password.send_keys(self.password)
            self.wait_random()
            self.driver.find_element(By.CSS_SELECTOR, "a.js-submit-button.inloggen-btn").click()
        except TimeoutException:
            print(self.driver.page_source)
            raise TimeoutError("TimeoutException: Unable to locate the username field.")


    def click_element(self, by_method: By, identifier: str) -> None:
        """Click a certain element based on an identifier to navigate to the next page."""
        self.wait_random()
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((by_method, identifier))
        )
        self.wait_random()
        element.click()


    def click_element_if_contains_text(self, by_method: By, identifier: str, text_to_match: str, i: int) -> bool:
        """
        Scrolls the original element into view, ensures it remains interactable, 
        and clicks the parent <a> container if the specified text is found in the element.
        This is a specific method because of the difficult interactivity at this stage of 
        the workflow.
        """
        self.wait_random()
        try:
            # Locate the <a> container that contains the desired text in its child elements
            parent_a = self.driver.find_elements(
                By.XPATH,
                f"//a[contains(., '{text_to_match}')]"
            )[i]

            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", parent_a)
            self.wait_random()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(parent_a))

            # Click the <a> container using javascript (needed for this instance).
            self.driver.execute_script("arguments[0].click();", parent_a)
            return True
        except Exception as e:
            print(f"Error: {e}")
            print(f"No element found containing text: {text_to_match}")
            return False


    def close(self):
        """
        Properly closes the WebDriver and cleans up resources.
        """
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error while quitting the WebDriver: {e}")
        finally:
            # Clean up the temporary user data directory
            shutil.rmtree(self.user_data_dir, ignore_errors=True)

            # Ensure the browser process is terminated
            os.system("pkill -f firefox")


    def react_to_houses(self, type_woning: str, max_houses: int=2) -> None:
        """
        Reacts to houses based on the specified type (e.g., WoningLoting).
        """
        i = 0
        while i < max_houses:
            # Click on a house based on the type (e.g., WoningLoting)
            success = self.click_element_if_contains_text(By.CLASS_NAME, "box--obj__type", type_woning, i)
            if not success:
                print(f"No more houses found with type: {type_woning}")
                break

            # Perform additional actions after clicking the house
            try:
                print("Attempting to click 'Perfect!' button...")
                self.click_element(By.PARTIAL_LINK_TEXT, "Perfect!")
                print("'Perfect!' button clicked successfully.")
            except Exception as e:
                print(f"Error clicking 'Perfect!' button: {e}")
                break

            # Scroll the "Plaats reactie" button into view before clicking it
            try:
                # Locate the button using its attributes
                command_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[name='Command'][value='plaats-einkomen']"))
                )
                # Scroll the button into view
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", command_element)
                self.wait_random()
                # Click the button
                self.driver.execute_script("arguments[0].click();", command_element)
                print("Clicked the 'Plaats reactie' button successfully.")
            except Exception as e:
                print(f"Error clicking 'Plaats reactie' button: {e}")
                print("Current page HTML for debugging:")
                print(self.driver.page_source)
                break

            # Navigate back to the list of houses
            try:
                self.click_element(By.CSS_SELECTOR, "a.header-nav__button--home")
            except Exception as e:
                print(f"Error navigating back to 'Aanbod': {e}")
                break

            i += 1
        print(f"Reacted to {i} houses of type: {type_woning}")
