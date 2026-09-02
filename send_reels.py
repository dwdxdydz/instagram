#!/usr/bin/env python3
"""Send Instagram reels to selected usernames using Selenium."""

import argparse
import os
from datetime import datetime

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()


def create_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument("-headless")
    profile_path = os.getenv("FIREFOX_PROFILE_PATH")
    if profile_path:
        options.add_argument("-profile")
        options.add_argument(profile_path)
    return webdriver.Firefox(options=options)


def send_reels(users: list[str], num_reels: int = 3) -> None:
    if not users:
        raise ValueError("At least one Instagram username is required")
    if num_reels < 1:
        raise ValueError("num_reels must be at least 1")

    driver = create_driver()
    try:
        driver.get("https://www.instagram.com/reels/")

        for index in range(num_reels):
            try:
                share_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "svg"))
                )
                if index >= len(share_buttons):
                    print(f"No share control available for reel {index + 1}; stopping.")
                    break

                share_buttons[index].click()
                for username in users:
                    search = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...']"))
                    )
                    search.clear()
                    search.send_keys(username)
                    result = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//*[normalize-space()='{username}']"))
                    )
                    result.click()

                send_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Send']"))
                )
                send_button.click()
                print(f"Sent reel {index + 1} to {', '.join(users)}")
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.DOWN)
            except Exception as exc:
                print(f"Could not send reel {index + 1}: {exc}")
    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send reels to Instagram users")
    parser.add_argument("--users", nargs="+", required=True)
    parser.add_argument("--reels", type=int, default=3)
    args = parser.parse_args()

    print(f"Started: {datetime.now().isoformat(timespec='seconds')}")
    send_reels(args.users, args.reels)
