from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Driver:
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument(f"user-agent={desired_capabilities}")

    def get_driver(self):
        driver = webdriver.Remote(
            command_executor="http://chromedriver:4444/wd/hub",
            desired_capabilities=self.desired_capabilities,
            options=self.options,
        )
        try:
            yield driver
        finally:
            driver.quit()
