from bs4 import BeautifulSoup
import requests
import json

RECIPE_SITE_URL = "https://www.recepty.cz"


def get_JSON_LD_of_recipe(recipe_url):
    html = requests.get(recipe_url)
    soup = BeautifulSoup(html.text, "html.parser")
    rdf_data = soup.select_one("script[type='application/ld+json']")
    json_content = json.loads(rdf_data.contents[0].string)
    return json_content


if __name__ == '__main__':
    with open("recipes_links.txt", "r") as f:
        with open("recipes.json", "w", encoding="utf-8") as rf:
            rf.write("[\n")
            for recipe in f.readlines():
                # Get rid of new line symbol
                recipe_trimmed = recipe[0:len(recipe)-1]
                recipe_url = RECIPE_SITE_URL+recipe_trimmed
                recipeDict = get_JSON_LD_of_recipe(recipe_url)
                rf.write(json.dumps(recipeDict, ensure_ascii=False)+",\n")
            rf.write("]\n")
            rf.close()
        f.close()

