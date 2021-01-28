from collections import defaultdict, Counter


def load_foods(input_filename):
    foods = []

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip("\n")
            ingredients_and_allergens = line.split()
            ingredients = set()
            allergens = set()
            parse_allergens = False

            for item in ingredients_and_allergens:
                if item == "(contains":
                    parse_allergens = True
                    continue

                if not parse_allergens:
                    ingredients.add(item)
                else:
                    item = item[:-1]  # always either a comma or closing paren
                    allergens.add(item)
            foods.append((ingredients, allergens))

    return foods


def get_known_ingredient_allergens(ingredient_allergen):
    known_ingredients = defaultdict(list)

    for allergen, ingredients in ingredient_allergen.items():
        if len(ingredients) == 1:
            known_ingredients[allergen] = list(ingredients)[0]

    return known_ingredients


def gather_all_ingredients(foods):
    ingredients_counter = Counter()

    for ingredients, _ in foods:
        for ingredient in ingredients:
            ingredients_counter[ingredient] += 1

    return ingredients_counter


def get_non_allergen_ingredient_count(foods, known_ingredients):
    total = 0

    ingredients_counter = gather_all_ingredients(foods)

    for ingredient, count in ingredients_counter.items():
        if ingredient not in known_ingredients:
            total += count

    return total


if __name__ == "__main__":
    foods = load_foods("input_day21.txt")
    ingredient_allergen = {}  # maps from allergen -> possible ingredients

    for food in foods:
        ingredients, allergens = food
        for allergen in allergens:
            if allergen in ingredient_allergen:
                ingredient_allergen[allergen] = ingredient_allergen[allergen].intersection(ingredients)
            else:
                ingredient_allergen[allergen] = ingredients

    # now iterate on removing known ingredients
    known_ingredients = get_known_ingredient_allergens(ingredient_allergen)

    while len(known_ingredients.values()) < len(ingredient_allergen):
        for allergen, ingredients in ingredient_allergen.items():
            if len(ingredients) > 1:
                ingredient_allergen[allergen] = ingredients.difference(known_ingredients.values())
        known_ingredients = get_known_ingredient_allergens(ingredient_allergen)

    sorted_allergens = sorted(known_ingredients.keys())
    canonical_ingredient_list = ",".join([known_ingredients[allergen] for allergen in sorted_allergens])
    print(canonical_ingredient_list)
    # print(get_non_allergen_ingredient_count(foods, known_ingredients.values()))
