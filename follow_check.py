from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from login_data import username, password
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# The username and password of the account whose followers who want check!!
username = 'Instagram username of the account'
password = 'Password of the same account'

def login_instagram(driver):
    # Navigate to the Instagram login page
    driver.get("https://www.instagram.com/accounts/login/")

    # Wait until the username input field is visible
    username_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
    username_input.send_keys(username)

    password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    password_input.send_keys(password)

    password_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.url_contains("instagram.com"))
    sleep(5)
    print('login successful !!')

def write_user_list_to_file(filename, user_list):
    with open(filename, 'w') as file:
        for user in user_list:
            file.write(user + '\n')

def check(users = None):

    users_you_follow = []
    users_dont_follow_back = []
    users_follow_back = []
    users_not_found = []

    if users is not None:
        check_certain_user(users)
        return

    firefox_options = Options()
    firefox_options.add_argument('-headless')

    driver = webdriver.Firefox(options=firefox_options)
    print('Starting webdriver ....')

    login_instagram(driver)

    driver.get(f"https://www.instagram.com/{username}/following")
    sleep(5)

    print('on the following page!!')

    # Find the <div> element to scroll within
    scroll_div = driver.find_element(By.CLASS_NAME, '_aano')

    # Scroll down the <div> element to load more content
    prev_user_count = 0
    curr_user_count = -1
    while curr_user_count != prev_user_count:
        prev_user_count = curr_user_count

        # Get the current number of user divs
        html_code = driver.page_source
        soup = BeautifulSoup(html_code, 'html.parser')
        user_divs = soup.find_all('div', class_='x9f619 xjbqb8w x1rg5ohu x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1')
        curr_user_count = len(user_divs)

        # Print the newly loaded usernames
        for div in user_divs[curr_user_count - prev_user_count:]:
            current_user = div.text

            if current_user.endswith("Verified"):
                print(f"{current_user} is a verified account. Checking terminated.")
                print("Users who follow you back:")
                print(users_follow_back)
                print("Users who don't follow you back:")
                print(users_dont_follow_back)
                prev_user_count = curr_user_count
                break

            users_you_follow.append(current_user)

            sleep(2)
            # Scroll to the covered element
            covered_element = driver.find_element(By.CLASS_NAME, 'x1qjc9v5')
            driver.execute_script("arguments[0].scrollIntoView();", covered_element)

            try:
                # Visit the user's profile
                profile_link = driver.find_element(By.PARTIAL_LINK_TEXT, current_user)
                profile_link.click()
                sleep(3.5)
            except NoSuchElementException:
                print(f"User '{current_user}' not found. Continuing...")
                users_not_found.append(f'{current_user}')
                continue

            link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._alvs._a6hd')
            link_elements[1].click()  # Select the second element (index 1)
            sleep(3.5)

            # Get the first user in the following window
            first_user_div = driver.find_element(By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x1rg5ohu.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1')
            first_user = first_user_div.text

            driver.back()

            if first_user == username:
                # The user follows you back
                users_follow_back.append(current_user)
                print(f"{current_user} follows you back!")
            else:
                users_dont_follow_back.append(current_user)
                print(f"{current_user} does not follow you back!")

            # Go back to the list of users you follow
            driver.back()
            sleep(3)

            try:
                scroll_div = driver.find_element(By.CLASS_NAME, '_aano')
                scroll_div.send_keys(Keys.END)
                sleep(3)
            except StaleElementReferenceException:
                print("StaleElementReferenceException occurred. Retrying...")
                continue

        if curr_user_count == prev_user_count:
            break
        
        scroll_div.send_keys(Keys.END)
        sleep(3)

    # Close the webdriver
    driver.quit()

    write_user_list_to_file('users_follow_back.txt', users_follow_back)
    write_user_list_to_file('users_not_found.txt', users_not_found)
    write_user_list_to_file('users_dont_follow_back.txt', users_dont_follow_back)

    print(f'You follow total of {len(users_you_follow)} users')
    print(f'Total of {len(users_dont_follow_back)} don\'t follow you back!!')
    print(f'Total {len(users_not_found)} are not found')


def check_certain_user(*args):
    firefox_options = Options()
    firefox_options.add_argument('-headless')

    driver = webdriver.Firefox(options=firefox_options)

    login_instagram(driver)

    for user in args:
        driver.get(f"https://www.instagram.com/{user}/following/")
        sleep(5)

        # Get the first user in the following window
        first_user_div = driver.find_element(By.CSS_SELECTOR, 'div.x9f619.xjbqb8w.x1rg5ohu.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1')
        first_user = first_user_div.text

        if first_user == username:
            print(f'{user} follow back {username}!!')
        else:
            print(f'{user} doesn\'t follow back {username}!!')

    # Close the webdriver
    driver.quit()

if __name__ == '__main__':
    check()

