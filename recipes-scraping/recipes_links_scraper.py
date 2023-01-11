from bs4 import BeautifulSoup
import requests
from collections import deque

RECIPE_SITE_URL = "https://www.recepty.cz"
RECIPE_SITE_LIST_PAGE = "/food"
RECIPE_URL_CAT = "/recept"


def get_all_recipes_links(soup):
    links = soup.select(".search-results__wrapper a")
    recipe_sites = set()
    for link in links:
        if RECIPE_URL_CAT in link['href']:
            if "nejnovejsi" in link['href']:
                continue
            recipe_sites.add(link['href'])
    return recipe_sites


def add_recipes_links(target_set, subpage, max_paginator):
    LAST_PAGINATOR_VAL = 79
    for i in range(1, max_paginator, 1):
        url = RECIPE_SITE_URL+subpage+"/"+i.__str__()
        content = requests.get(url)
        soup = BeautifulSoup(content.text, "html.parser")
        recipes_urls = get_all_recipes_links(soup)
        for url in recipes_urls:
            target_set.add(url)


if __name__ == '__main__':
    recipes_links = set()
    add_recipes_links(recipes_links, "/food", 79)
    add_recipes_links(recipes_links, "/recept/nejnovejsi", 634)
    with open("recipes_links.txt", "w") as f:
        for recipe_url in recipes_links:
            f.write(recipe_url+"\n")
        f.close()
