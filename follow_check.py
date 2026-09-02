#!/usr/bin/env python3
"""Check whether Instagram accounts follow a configured account back.

The script uses Selenium for browser automation. Instagram's page structure can
change over time, so selectors may require maintenance.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

ACCOUNT_USERNAME = os.getenv("INSTAGRAM_USERNAME")
ACCOUNT_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


def login_instagram(driver: webdriver.Firefox) -> None:
    """Log in using environment-configured credentials."""
    if not ACCOUNT_USERNAME or not ACCOUNT_PASSWORD:
        raise RuntimeError("Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")

    driver.get("https://www.instagram.com/accounts/login/")
    username_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys(ACCOUNT_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(ACCOUNT_PASSWORD, Keys.RETURN)
    WebDriverWait(driver, 15).until(EC.url_contains("instagram.com"))


def write_user_list(filename: str, users: list[str]) -> None:
    Path(filename).write_text("\n".join(users) + "\n", encoding="utf-8")


def create_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def check(users: list[str] | None = None) -> None:
    """Check selected accounts or the full following list."""
    if users:
        check_certain_users(users)
        return

    driver = create_driver()
    users_follow_back: list[str] = []
    users_dont_follow_back: list[str] = []
    users_not_found: list[str] = []

    try:
        login_instagram(driver)
        driver.get(f"https://www.instagram.com/{ACCOUNT_USERNAME}/following")

        scroll_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_aano"))
        )
        previous_count = -1

        while True:
            user_divs = driver.find_elements(By.CSS_SELECTOR, "div._aacl._aaco._aacu._aacx._aada")
            current_count = len(user_divs)
            if current_count == previous_count:
                break
            previous_count = current_count

            for element in user_divs:
                username = element.text.strip().split("\n")[0]
                if not username:
                    continue
                try:
                    element.click()
                    WebDriverWait(driver, 10).until(EC.url_contains(username))
                    driver.back()
                    users_follow_back.append(username)
                except (NoSuchElementException, StaleElementReferenceException):
                    users_not_found.append(username)

            scroll_div.send_keys(Keys.END)

        write_user_list("users_follow_back.txt", sorted(set(users_follow_back)))
        write_user_list("users_dont_follow_back.txt", sorted(set(users_dont_follow_back)))
        write_user_list("users_not_found.txt", sorted(set(users_not_found)))
    finally:
        driver.quit()


def check_certain_users(users: list[str]) -> None:
    driver = create_driver()
    try:
        login_instagram(driver)
        for username in users:
            driver.get(f"https://www.instagram.com/{username}/following/")
            print(f"Checked @{username}")
    finally:
        driver.quit()


if __name__ == "__main__":
    check()
