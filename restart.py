from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from plyer import notification

# for firefox browser
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os

# NOTE for chrome browser
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# NOTE If the router page is secured, then fill up your credentials by using the below format:
# router_ip= "login_username:login_password@ip_of_router"

# NOTE fillup router login credential
router_ip = "http://192.168.1.1/"
router_username = "your_router_username"
router_password = "your_router_password"

# to debug set level to debug
logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {name:<5} - {levelname:<8} - {message}",
    style="{",
    filename="%slog" % __file__[:-2],
    filemode="a",
)

# disable logging for webdriver
os.environ["WDM_LOG"] = str(logging.NOTSET)


class web_driver:
    options = Options()
    options.add_argument("-headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    # set log path for firefox at log_path='/dev/null'
    # Disable logs in windows, at  log_path='nul'
    os_log_path = "/dev/null" if os.name == "posix" else "NUL"

    # for firefox browser
    browser = webdriver.Firefox(
        options=options,
        service=FirefoxService(GeckoDriverManager().install(), log_path=os_log_path),
    )
    # NOTE for chrome browser
    # browser = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))


def reboot_it(ip_adr):
    sucess_msg = "Router has been successfully restarted."
    failed_msg = "Router could not be restarted."
    try:
        logging.info("Accessing the router login page")
        web_driver.browser.get(ip_adr)
        sleep(1)

        # credential form
        web_driver.browser.find_element(By.ID, "Frm_Username").send_keys(
            router_username
        )
        web_driver.browser.find_element(By.ID, "Frm_Password").send_keys(
            router_password
        )

        # login_btn
        login_btn = web_driver.browser.find_element(By.ID, "LoginId")
        login_btn.click()
        sleep(2)

        # Management & Diagnosis btn
        logging.info("Navigating to the advanced menu")
        advanced_btn = web_driver.browser.find_element(By.CSS_SELECTOR, "#mgrAndDiag")
        advanced_btn.click()

        # System Management btn
        sys_tools = web_driver.browser.find_element(By.XPATH, '//*[@id="devMgr"]')
        sys_tools.click()
        sleep(1)

        # reboot_btn
        reboot_btn = web_driver.browser.find_element(By.XPATH, '//*[@id="Btn_restart"]')
        reboot_btn.click()

        # accept browser_alert
        sleep(1)
        check = web_driver.browser.find_element(By.XPATH, '//*[@id="confirmOK"]')
        sleep(1)
        check.click()
        logging.info("Please wait while the router restarts")
        # web_driver.browser.switch_to.alert.accept()

        # close browser and logs the result
        logging.info(sucess_msg)
        quit_driver()

        # sends user notification
        ping("⏳  Restarting the router! ", sucess_msg)

    except Exception as e:
        logging.critical(f"{failed_msg} because of the following error {e}".strip())
        ping("⚠️  Restarting the router failed!", f"{failed_msg} due to an error {e}")
        quit_driver()


def quit_driver():
    logging.warning("Terminating the WebDriver session\n")
    web_driver.browser.quit()


def ping(header, msg):
    notification.notify(
        title=header, message=msg, timeout=10, app_name="Restart Router"
    )


def main():
    try:
        reboot_it(router_ip)
    except KeyboardInterrupt:
        quit_driver()


if __name__ == "__main__":
    main()
