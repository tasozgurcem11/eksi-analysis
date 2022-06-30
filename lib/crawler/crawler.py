import os
import time
import logging

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def log(message, log_level='info'):
    if log_level == 'info':
        logging.info(message)

    elif log_level == 'warning':
        logging.warning(message)

    elif log_level == 'error':
        logging.error(message)

    print(message)


def generate_options(args):
    """
    Generate options for Chrome
    :return:
    """
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    if not args.local:
        options.add_argument("--headless")
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-in-process-stack-traces")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--output=/dev/null")
    options.add_argument("--no-sandbox")
    return options


def generate_prefs(options):
    """
    Generate prefs for Chrome
    :param options:
    :return:
    """
    prefs = {"download.default_directory": os.getenv('CRAWL_DOWNLOAD_PATH'),
             "directory_upgrade": True,
             "profile.default_content_settings.popups": 0,
             "download.prompt_for_download": "false",
             }
    options.add_experimental_option("prefs", prefs)
    return options


def crawl_eksi(args):

    # Create Selenium Settings and Options
    options = generate_options(args)
    options = generate_prefs(options)

    if args.local:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    else:
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',  options=options)

    driver.implicitly_wait(10)

    # Load website
    log_message = f'Loading website for {os.getenv("CRAWL_WEBSITE")}'
    log(log_message)
    print(os.getenv('CRAWL_WEBSITE'))
    driver.get(os.getenv('CRAWL_WEBSITE'))
    time.sleep(5)

    # Add Email
    log_message = f'Getting all the titles'
    log(log_message)

    data_dict_list = []
    for i in range(5):
        time.sleep(3)

        if i == 0:
            driver.find_element(By.XPATH, '//*[@id="onetrust-close-btn-container"]/button').click()
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="quick-index-continue-link"]').click()
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, '//*[@id="interstitial-close-link-tag"]').click()
            except:
                pass

        elif i > 1:
            driver.find_element(By.XPATH, '//*[@id="partial-index"]/div[3]/a[3]').click()

        time.sleep(3)

        titles = driver.find_elements(By.XPATH, '//*[@id="partial-index"]/ul')
        time.sleep(5)

        entry_list = titles[0].text.split('\n')

        # Get all the entries by their title and #
        for i in range(0, len(entry_list), 2):
            print(entry_list[i], entry_list[i + 1])

            data_dict = {
                'title': entry_list[i],
                'entries': entry_list[i + 1]
            }
            data_dict_list.append(data_dict)

        time.sleep(2)

    driver.quit()

    return pd.DataFrame(data_dict_list)
