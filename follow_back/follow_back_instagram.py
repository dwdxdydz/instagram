#!/usr/bin/python3

from bs4 import BeautifulSoup
from lxml import html
import os

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

following_file = os.path.join(script_dir, 'following.html')
follower_file = os.path.join(script_dir, 'followers.html')

with open(following_file, 'r') as file:
    following = html.parse(file)

with open(follower_file, 'r') as file:
    follower = html.parse(file)

following_page = html.tostring(following)
follower_page = html.tostring(follower)

following_soup = BeautifulSoup(following_page, features="html.parser")
follower_soup = BeautifulSoup(follower_page, features="html.parser")

following_list = following_soup.find_all("a", {"target": "_blank"})
follower_list = follower_soup.find_all("a", {"target": "_blank"})

following_list_stored = []
follower_list_stored = []

for following_account_raw in following_list:
    for following_account in following_account_raw:
        following_list_stored.append(following_account)

for follower_account_raw in follower_list:
    for follower_account in follower_account_raw:
        follower_list_stored.append(follower_account)

count = 0
print("The usenames below don't follow you back: \n")

for account_check in following_list_stored:
    if account_check not in follower_list_stored:
        print(account_check)
        count += 1


print(f'\n\nTotal users who don\'t follow you back = {count}')
