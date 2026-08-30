from datetime import timedelta
from cookie_clicker_handler import CookieClickerHandler

seconds = int(input("Enter the seconds between product/upgrade checks: "))

handler = CookieClickerHandler()
handler.PURCHASE_TIME_DELTA = timedelta(seconds = seconds)

cookies_per_second = handler.play_game()
print(f"Cookies per second: {cookies_per_second}")