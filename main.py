from ansiescape import esc8fg, esc
import requests
import bs4
from time import sleep
import datetime

# Current day as an integer for use with finding the right menu
current_day = datetime.date.today().day

url = r"https://menus.sodexomyway.com/BiteMenu/Menu?menuId=15340&locationId=55929001&whereami=https://tcnj.sodexomyway.com/dining-near-me/atrium-at-eickhoff"
page = requests.get(url)
soup = bs4.BeautifulSoup(page.content, 'html.parser')

# The website has a different menu for each day. This finds the current day's menu
menu_today = soup.find(id=f"menuid-{current_day}-day")

# Finds the different menu's per block (breakfast, brunch, lunch, etc.)
menu_blocks = menu_today.select('div[class*="accordion-block "]')

# Main print
for block in menu_blocks:
    # Finds the block block_title
    block_title = block.find("span", class_="accordion-copy").text.lower()
    block_title = block_title[0].upper() + block_title[1:]

    print(esc(1) + "-"*50 + " " + block_title + " " + "-"*125 + esc(0), end="\n\n")

    stations = block.select('div[class="bite-menu-course"]')
    meals = block.select('ul[class="bite-menu-item"]')

    i = 21
    for pair in zip(stations[1:], meals[1:]):
        print("\t", esc(1), pair[0].get_text(strip=True), esc(0), sep="")
        for meal in pair[1].select('div[class="col-xs-9"]'):
            print("\t- ", esc8fg(i), meal.get_text(strip=True), esc(0), sep="")
            i += 1
        print("\n")
