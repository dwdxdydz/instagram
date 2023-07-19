#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime


def send_reels(users, num_reels = 3):
    firefox_options = Options()

    profile_path = '{Your Profile Path}'
    firefox_options.add_argument('-profile')
    firefox_options.add_argument('-headless')
    firefox_options.add_argument(profile_path)

    driver = webdriver.Firefox(options=firefox_options)

    driver.get("https://www.instagram.com/reels")

    username_mapping = {
        'ajit': '_its_ajitpal',
    }

    mapped_users = [username_mapping.get(user, user) for user in users]

    # Wait for the page to load

    for i in range(0, num_reels):
        try:
            sleep(1)
            share_button_lines = driver.find_elements(By.CSS_SELECTOR, 'line[fill="none"][stroke="currentColor"][stroke-linejoin="round"][stroke-width="2"][x1="22"][x2="9.218"][y1="3"][y2="10.083"]')
            share_button_line = share_button_lines[i]
            share_button_line.click()
            # print("Clicked on share button:", i)

            for user in mapped_users:
                recipients_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...']")))
                recipients_input.send_keys(user)
                photo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'x1lliihq')][text()='{user}']")))
                photo.click()

            # Click on the send button
            send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div._aagz")))
            send_button.click()
            print(f'Sent {i+1} reels to {users}')

            # Scroll down
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DOWN)
        except Exception as e:
            print("Exception occurred:", str(e))


    driver.quit()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Send reels to Instagram users.')
    parser.add_argument('--users', metavar='user', type=str, nargs='+', help='List of users to send reels')
    parser.add_argument('--reels', metavar='num_reels', type=int, default=3, help='Number of reels to send (default: 3)')

    args = parser.parse_args()

    print("Running the script at:", datetime.datetime.now())
    print("Users:", args.users)
    print("Number of reels:", args.reels)

    send_reels(args.users, args.reels)

