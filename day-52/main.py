from InstaFollower import *
"""
Day 51 - Intermediate+ Instagram Follower Bot

Goal:
- log into Instagram (or Share-a-Naan)
    - save your login info popup
        - div class 'naan-popup-dismiss', text 'Not now'
            - click it
    - turn on notifications popup
        - button class 'naan-popup-dismiss', test 'Not now'
            - click it
- search for and go to the account you are interested in
- click the followers button
- for each follower, click their follow button
"""

# USERNAME = 'bfutrel@gmail.com'
# PASSWORD = 'yPPSy99K4eEq4lfQ'
# SIMILAR_ACCOUNT = 'rordongamsay'
# PROFILE_NAME = '@bfutrel'
# BASE_URL = ''
# LOGIN_URL = f'{BASE_URL}/login'

insta_follower = InstaFollower()

insta_follower.login()
followers = insta_follower.find_followers()

for follower in followers:
    insta_follower.follow(follower)