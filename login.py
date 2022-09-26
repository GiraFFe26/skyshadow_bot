from selenium import webdriver
import chromedriver_binary
from fake_useragent import UserAgent
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


class login:
    def __init__(self, mail, password):
        self.ua = UserAgent()
        self.delay = 3
        self.mail = mail
        self.password = password
        self.pause = 0.5

    def driver_start(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"user-agent={self.ua.random}")
        #chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=1")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("disable-infobars")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://login.live.com/login.srf')
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'loginfmt')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.NAME, 'loginfmt').send_keys(self.mail)
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        try:
            driver.find_element(By.ID, 'idSIButton9').click()
        except NoSuchElementException:
            driver.close()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument(f"user-agent={self.ua.random}")
            # chrome_options.add_argument("--headless")
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("window-size=1920x1080")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--log-level=1")
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("disable-infobars")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get('https://login.live.com/login.srf')
            try:
                WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'loginfmt')))
            except TimeoutException:
                time.sleep(self.delay)
            driver.find_element(By.NAME, 'loginfmt').send_keys(self.mail)
            time.sleep(self.pause)
            try:
                WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
            except TimeoutException:
                time.sleep(self.delay)
            driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(self.pause)
        try:
            error = driver.find_element(By.ID, 'usernameError')
            driver.find_element(By.ID, 'lightbox').screenshot('ERROR.png')
            return error.text, driver.close()
        except NoSuchElementException:
            pass
        time.sleep(self.pause)
        try:
            error = driver.find_element(By.ID, 'idTD_Error').text + '\n' + driver.find_element(By.ID, 'error_Info').text
            try:
                driver.find_element(By.ID, 'lightbox').screenshot('ERROR2.png')
            except NoSuchElementException:
                driver.find_element(By.ID, 'inner').screenshot('ERROR2.png')
            return error, driver.close()
        except NoSuchElementException:
            pass
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'passwd')))
        except TimeoutException:
            time.sleep(self.delay)
        try:
            driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        except NoSuchElementException:
            try:
                WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'inner')))
            except TimeoutException:
                time.sleep(self.delay)
            driver.find_element(By.ID, 'inner').save_screenshot('ENTERED.PNG')
            return 'screen_accept', driver.close()
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(self.pause)
        try:
            error = driver.find_element(By.ID, 'passwordError')
            driver.find_element(By.ID, 'lightbox').screenshot('ERROR1.png')
            return error.text, driver.close()
        except NoSuchElementException:
            pass
        time.sleep(self.pause)
        try:
            error = driver.find_element(By.ID, 'idTD_Error').text + '\n' + driver.find_element(By.ID, 'error_Info').text
            try:
                driver.find_element(By.ID, 'lightbox').screenshot('ERROR2.png')
            except NoSuchElementException:
                driver.find_element(By.ID, 'inner').screenshot('ERROR2.png')
            return error, driver.close()
        except NoSuchElementException:
            pass
        time.sleep(self.pause)
        try:
            driver.find_element(By.ID, 'lightbox')
            try:
                WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
            except TimeoutException:
                time.sleep(self.delay)
            try:
                driver.find_element(By.ID, 'idSIButton9').click()
            except ElementNotInteractableException:
                driver.find_element(By.ID, 'idLbl_SAOTCAS_TD_Cb').click()
                driver.save_screenshot('ENTERED.png')
                return 'screen_accept', driver.close()
            time.sleep(7)
            driver.save_screenshot('ENTERED.png')
            return 'no_accept', driver.close()
        except NoSuchElementException:
            try:
                driver.find_element(By.ID, 'inner').screenshot('ENTERED.png')
                buttons = driver.find_element(By.ID, 'iProofList').find_elements(By.CLASS_NAME, 'radio')[:-1]
                return 'accept', len(buttons), driver.close()
            except NoSuchElementException:
                driver.find_element(By.ID, 'iLandingViewAction').click()
                try:
                    WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'iProofList')))
                except TimeoutException:
                    time.sleep(self.delay)
                driver.find_element(By.ID, 'inner').screenshot('ENTERED.png')
                buttons = driver.find_element(By.ID, 'iProofList').find_elements(By.CLASS_NAME, 'radio')[:-1]
                return 'accept', len(buttons), driver.close()

    def accept(self, num):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"user-agent={self.ua.random}")
        #chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=1")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("disable-infobars")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://login.live.com/login.srf')
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'loginfmt')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.NAME, 'loginfmt').send_keys(self.mail)
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        try:
            driver.find_element(By.ID, 'idSIButton9').click()
        except NoSuchElementException:
            return 'Microsoft page_source loading error\nПопробуйте ещё раз', driver.close()
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'passwd')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.CLASS_NAME, 'radio')))
        except TimeoutException:
            time.sleep(self.delay)
        time.sleep(self.pause)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        buttons_soup = soup.find('div', id='iProofList').find_all('div', class_='radio')[:-1]
        print(buttons_soup)
        button = buttons_soup[num - 1].text
        if 'Письмо' in button:
            return 'Напишите Ваш email полностью', 1, driver.close()
        elif 'SMS' in button:
            return 'Введите последние 4 цифры номера телефона', 2, driver.close()
        elif 'Authenticator' in button:
            buttons = driver.find_element(By.ID, 'iProofList').find_elements(By.NAME, 'proof')[:-1]
            buttons[num - 1].click()
            try:
                WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'iPollSessionTitle')))
            except TimeoutException:
                time.sleep(self.delay)
            return driver.find_element(By.ID, 'iPollSessionTitle').text, 3, driver.close()

    def accept_1(self, num, info):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"user-agent={self.ua.random}")
        # chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=1")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("disable-infobars")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://login.live.com/login.srf')
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'loginfmt')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.NAME, 'loginfmt').send_keys(self.mail)
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        try:
            driver.find_element(By.ID, 'idSIButton9').click()
        except NoSuchElementException:
            return 'Microsoft page_source loading error\nПопробуйте ещё раз', driver.close()
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'passwd')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.CLASS_NAME, 'radio')))
        except TimeoutException:
            time.sleep(self.delay)
        time.sleep(self.pause)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        buttons = driver.find_element(By.ID, 'iProofList').find_elements(By.NAME, 'proof')[:-1]
        buttons_soup = soup.find('div', id='iProofList').find_all('div', class_='radio')[:-1]
        button = buttons_soup[num - 1].text
        if 'Письмо' in button:
            buttons[num - 1].click()
            time.sleep(5)
            driver.find_element(By.ID, 'iProofEmail').send_keys(info)
            time.sleep(5)
            driver.find_element(By.ID, 'iSelectProofAction').click()
            time.sleep(10)
        if 'SMS' in button:
            buttons[num - 1].click()
            time.sleep(5)
            driver.find_element(By.ID, 'iProofPhone').send_keys(info)
            time.sleep(5)
            driver.find_element(By.ID, 'iSelectProofAction').click()
            time.sleep(10)
        driver.close()

    def accept_2(self, num, info):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"user-agent={self.ua.random}")
        # chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=1")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("disable-infobars")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://login.live.com/login.srf')
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'loginfmt')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.NAME, 'loginfmt').send_keys(self.mail)
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        try:
            driver.find_element(By.ID, 'idSIButton9').click()
        except NoSuchElementException:
            return 'Microsoft page_source loading error\nПопробуйте ещё раз', driver.close()
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.NAME, 'passwd')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.NAME, 'passwd').send_keys(self.password)
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(self.pause)
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.CLASS_NAME, 'radio')))
        except TimeoutException:
            time.sleep(self.delay)
        time.sleep(self.pause)
        try:
            buttons = driver.find_element(By.ID, 'iProofList').find_elements(By.CLASS_NAME, 'radio')[:-1]
        except NoSuchElementException:
            try:
                WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'idSIButton9')))
            except TimeoutException:
                time.sleep(self.delay)
            time.sleep(self.pause)
            driver.find_element(By.ID, 'idSIButton9').click()
            time.sleep(7)
            driver.save_screenshot('ENTERED.png')
            return 'no_accept', driver.close()
        button = buttons[num - 1]
        button.click()
        driver.find_element(By.ID, 'iSelectProofAlternate').click()
        try:
            WebDriverWait(driver, self.delay).until(ec.element_to_be_clickable((By.ID, 'iOttText')))
        except TimeoutException:
            time.sleep(self.delay)
        driver.find_element(By.ID, 'iOttText').send_keys(info)
        time.sleep(self.pause)
        driver.find_element(By.ID, 'iVerifyCodeAction').click()
        time.sleep(2)
        driver.save_screenshot('ENTERED.png')
        return 'no_accept', driver.close()

