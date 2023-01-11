import json
import re

import requests

import utils


def get_all_unique(recipes, param_name):
    values_set = set()
    for recipe in recipes:
        values_set.add(recipe[param_name])
    return values_set


def save_empty_mapping(list_keys, filename):
    with open(filename, "w", encoding="utf-8") as f:
        mapping = dict()
        for key in list_keys:
            mapping[key] = ""
        json_content = json.dumps(mapping, indent=4, ensure_ascii=False)
        f.write(json_content)


def parse_ingredient_string(ingredient):
    ingredient_text = utils.remove_diacritics(ingredient)
    ingredient_text = ingredient_text.lower()
    ingredient_text = ingredient_text.replace("-", " ")
    ingredient_text = ingredient_text.replace("   ", " ")
    ingredient_text = ingredient_text.replace("  ", " ")
    ingredient_text = utils.remove_brackets_with_content(ingredient_text)
    ingredient_text = utils.remove_quantity(ingredient_text)
    ingredient_text = utils.remove_prepositions_parts(ingredient_text)
    ingredient_text = re.sub("[^\w\s]", "", ingredient_text)
    ingredient_text = ingredient_text.replace(' ', " ")
    return ingredient_text


def parse_recipe_name(recipe_name):
    recipe_text = utils.remove_diacritics(recipe_name)
    recipe_text = recipe_text.lower()
    recipe_text = recipe_text.replace("-", " ")
    recipe_text = recipe_text.replace("   ", " ")
    recipe_text = recipe_text.replace("  ", " ")
    recipe_text = recipe_text.replace(".", "")
    recipe_text = recipe_text.replace(",", "")
    recipe_text = recipe_text.replace("-", "")
    recipe_text = recipe_text.replace(":", "")
    recipe_text = recipe_text.replace("/", "")
    recipe_text = recipe_text.replace("\\", "")

    recipe_text = recipe_text.replace('„', "")
    recipe_text = recipe_text.replace('“', "")
    recipe_text = recipe_text.replace('‟', "")
    recipe_text = recipe_text.replace('”', "")
    recipe_text = recipe_text.replace("’", "")
    recipe_text = recipe_text.replace('"', "")
    recipe_text = recipe_text.replace('❝', "")
    recipe_text = recipe_text.replace('❞', "")
    recipe_text = recipe_text.replace('⹂', "")
    recipe_text = recipe_text.replace('＂', "")
    recipe_text = recipe_text.replace(' ', " ")

    recipe_text = re.sub("[^\w\s]", "", recipe_text)

    recipe_text = utils.remove_brackets_with_content(recipe_text)
    return recipe_text


def get_ingredients(recipes):
    ingredients = set()
    for recipe in recipes:
        for ingredient in recipe["recipeIngredient"]:
            ingredient_text = parse_ingredient_string(ingredient)
            ingredients.add(ingredient_text)
    ingredients = list(ingredients)
    ingredients.sort()
    return ingredients


def save_slug_mapping(list_keys, filename):
    mapping = dict()
    for key in list_keys:
        mapping[key] = utils.text_to_slug(key)
    with open(filename, "w", encoding="utf-8") as f:
        json_string = json.dumps(mapping, indent=4, ensure_ascii=False)
        f.write(json_string)


category_mapping_file = open("categories_mapping.json", "r", encoding="utf-8")
category_mapping = json.loads(category_mapping_file.read())
category_mapping_file.close()


def get_recipe_category(recipe):
    return category_mapping[recipe["recipeCategory"]]


def transform_recipe(recipe):
    new_recipe = dict()
    new_recipe["@context"] = {
        "label": "https://www.w3.org/2000/01/rdf-schema#label",
        "isRecommendedForCourse": "http://purl.org/heals/food/isRecommendedForCourse",
        "hasIngredient": "http://purl.org/heals/food/hasIngredient",
        "hasCookTime": "http://purl.org/heals/food/hasCookTime",
        "serves": "http://purl.org/heals/food/serves"
    }
    recipe_name = parse_recipe_name(recipe["name"])
    new_recipe["@id"] = utils.text_to_slug(recipe_name)
    new_recipe["label"] = {
        "@value": recipe["name"],
        "@language": "cz"
    }
    new_recipe["@type"] = "Recipe"
    new_recipe["isRecommendedForCourse"] = {
        "@id": "http://purl.org/heals/food/" + get_recipe_category(recipe)
    }
    ingredients = list()
    for ingredient in recipe["recipeIngredient"]:
        if ingredient == "":
            continue
        ingr_dict = dict()
        ingr_dict["@id"] = "http://purl.org/heals/ingredient/" + utils.text_to_slug(parse_ingredient_string(ingredient))
        ingredients.append(ingr_dict)
    new_recipe["hasIngredient"] = ingredients
    new_recipe["hasCookTime"] = {
        "@value": recipe["totalTime"][2:len(recipe["totalTime"]) - 1],
        "@type": "http://www.w3.org/2001/XMLSchema#integer"
    }
    new_recipe["serves"] = {
        "@value": recipe["recipeYield"].split(" ")[0],
        "@type": "http://www.w3.org/2001/XMLSchema#integer"
    }
    return new_recipe


def save_recipes_as_json_ld(recipes, filename):
    wrapper = list()
    for recipe in recipes:
        wrapper.append(transform_recipe(recipe))
    with open(filename, "w", encoding="utf-8") as f:
        json_content = json.dumps(wrapper, ensure_ascii=False, indent=4)
        f.write(json_content)


def convert_jsonld_to_turtle_localhost():
    converter_url = "http://localhost/easyrdf/examples/converter.php"
    with open("recipes_rdf.json", "r", encoding="utf-8") as f:
        file_content = f.read()
        result = requests.post(converter_url, data={
            "output_format": "turtle",
            "input_format": "jsonld",
            "data": file_content,
            "raw": True,
            "uri": "http://purl.org/heals/food/"
        })
        print(result.text)
        with open("recipes_turtle.ttl", "w", encoding="utf-8") as turtleFile:
            turtleFile.write(result.text)
        result.close()


if __name__ == '__main__':
    with open("recipes.json", "r", encoding="utf-8") as f:
        convert_jsonld_to_turtle_localhost()
        #recipes = json.loads(f.read())
        #print("Loaded", len(recipes), "of recipes.")
        #save_recipes_as_json_ld(recipes, "recipes_rdf.json")
