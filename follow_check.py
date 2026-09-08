#!/usr/bin/env python3
"""Check whether Instagram accounts follow a configured account back.

The script uses Selenium for browser automation. Instagram's page structure can
change over time, so selectors may require maintenance.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

def login_instagram(driver: webdriver.Firefox) -> None:
    """Log in using environment-configured credentials."""
    account_username = os.getenv("INSTAGRAM_USERNAME")
    account_password = os.getenv("INSTAGRAM_PASSWORD")
    if not account_username or not account_password:
        raise RuntimeError("Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")

    driver.get("https://www.instagram.com/accounts/login/")
    username_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys(account_username)
    driver.find_element(By.NAME, "password").send_keys(account_password, Keys.RETURN)
    WebDriverWait(driver, 15).until(EC.url_contains("instagram.com"))


def write_user_list(filename: str, users: list[str]) -> None:
    Path(filename).write_text("\n".join(users) + "\n", encoding="utf-8")


def create_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def username_and_follows_you(item) -> tuple[str, bool] | None:
    """Extract a username and its follow-back status from a following-list item."""
    links = item.find_elements(By.CSS_SELECTOR, "a[href^='/']")
    if not links:
        return None

    href = links[0].get_attribute("href").rstrip("/")
    username = href.rsplit("/", 1)[-1]
    if not username or username in {"accounts", "explore", "reels"}:
        return None
    return username, "follows you" in item.text.casefold()


def check(users: list[str] | None = None) -> None:
    """Check selected accounts or the full following list."""
    if users:
        check_certain_users(users)
        return

    driver = create_driver()
    users_follow_back: list[str] = []
    users_dont_follow_back: list[str] = []

    try:
        login_instagram(driver)
        account_username = os.getenv("INSTAGRAM_USERNAME")
        if not account_username:  # Kept for type narrowing and direct calls to this function.
            raise RuntimeError("Set INSTAGRAM_USERNAME in .env")
        driver.get(f"https://www.instagram.com/{account_username}/following")

        scroll_div = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_aano"))
        )
        seen_users: set[str] = set()

        while True:
            items = driver.find_elements(By.CSS_SELECTOR, "div[role='dialog'] li")
            new_users = 0
            for item in items:
                try:
                    result = username_and_follows_you(item)
                except StaleElementReferenceException:
                    continue
                if result is None:
                    continue
                username, follows_you = result
                if username in seen_users:
                    continue
                seen_users.add(username)
                new_users += 1
                (users_follow_back if follows_you else users_dont_follow_back).append(username)

            if new_users == 0:
                break

            scroll_div.send_keys(Keys.END)

        write_user_list("users_follow_back.txt", sorted(set(users_follow_back)))
        write_user_list("users_dont_follow_back.txt", sorted(set(users_dont_follow_back)))
    finally:
        driver.quit()


def check_certain_users(users: list[str]) -> None:
    driver = create_driver()
    try:
        login_instagram(driver)
        for username in users:
            driver.get(f"https://www.instagram.com/{username}/")
            body = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            status = "follows you" in body.text.casefold()
            print(f"@{username}: {'follows you' if status else 'does not follow you'}")
    finally:
        driver.quit()


if __name__ == "__main__":
    check()
