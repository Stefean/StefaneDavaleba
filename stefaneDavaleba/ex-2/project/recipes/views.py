from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Recipe
import random

RECIPES = [
    {"id": 1, "slug": "khinkali", "name": "ხინკალი", "category": "main",
    "minutes": 90, "vegetarian": False,
    "ingredients": ["ფქვილი", "საქონლის ხორცი", "ღორის ხორცი",
    "ხახვი", "კვლიავი"]},
    {"id": 2, "slug": "khachapuri", "name": "ხაჭაპური", "category":
    "bakery", "minutes": 60, "vegetarian": True,
    "ingredients": ["ფქვილი", "იმერული ყველი", "კვერცხი", "კარაქი"]},
    {"id": 3, "slug": "lobiani", "name": "ლობიანი", "category": "bakery",
    "minutes": 75, "vegetarian": True,
    "ingredients": ["ფქვილი", "ლობიო", "ხახვი", "კარაქი"]},
    {"id": 4, "slug": "pkhali", "name": "ფხალი", "category": "snack",
    "minutes": 30, "vegetarian": True,
    "ingredients": ["ისპანახი", "ნიგოზი", "ნიორი", "ქინძი"]},
    {"id": 5, "slug": "churchkhela", "name": "ჩურჩხელა", "category":
    "dessert", "minutes": 240, "vegetarian": True,
    "ingredients": ["ნიგოზი", "ყურძნის წვენი", "ფქვილი"]},
    {"id": 6, "slug": "chakapuli", "name": "ჩაქაფული", "category":
    "main", "minutes": 120, "vegetarian": False,
    "ingredients": ["ცხვრის ხორცი", "ტყემალი", "ტარხუნა", "თეთრიღვინო"]},
]

def page(title, body):
    return HttpResponse(f"<h1>{title}</h1>{body}<hr><a href='/recipes/'>← ყველა რეცეპტი </a>")

def recipe_list(request):
    recipes = RECIPES

    category = request.GET.get("category")
    if category:
        recipes = [r for r in recipes if r["category"] == category]

    max_time = request.GET.get("max_time")
    if max_time:        
        max_time_int = int(max_time)
        recipes = [r for r in recipes if r["minutes"] <= max_time_int]

    vegetarian = request.GET.get("vegetarian")
    if vegetarian == "yes" or vegetarian == "კი" :
        recipes = [r for r in recipes if r["vegetarian"] == True]
    elif vegetarian == "no" or vegetarian == "არა":
        recipes = [r for r in recipes if r["vegetarian"] == False]

    lines = [
        f'<li><a href="/recipes/{recipe["id"]}/">{recipe["name"]}</a> — მომზადების დრო: {recipe["minutes"]} წთ</li>' for recipe in recipes
    ]

    html = f"<ul>{''.join(lines)} </ul>"
    return page("რეცეპტების სია", html)

def find_recipe(pk):
    for recipe in RECIPES:
        if recipe["id"] == int(pk):
            return recipe

    return None

def category_detail(request, name):
    result = [r for r in RECIPES if r["category"] == name]
    if not result:
        raise Http404("There is no such category")

    recipe = result[0]
    ingredient_lines = [f"<li>{ing}</li>" for ing in recipe["ingredients"]]
    ingredient_html = f"<ul>{''.join(ingredient_lines)}</ul>"

    body = f"საჭმელი: {recipe['name']} ,მომზადების დრო: {recipe['minutes']}, კატეგორია: {recipe['category']}, ვეგეტარიანული: {'კი' if recipe['vegetarian'] else 'არა'}, ინგრედიენტები: {ingredient_html} "

    return HttpResponse(body)

def search(request):
    q = request.GET.get("q").strip()
    if not q:
        return HttpResponse("Write valid ingredient")
    results = [r for r in RECIPES if q.lower() in str(r["ingredients"]).lower()]
    if not results:
        raise Http404("No recipe found with this ingredient")
    items = [f"<li><a href='/recipes/{r['id']}'>{r['name']}</a></li>" for r in results]
    html = f"<h1>ძიების შედეგები: {q}</h1><ul>{''.join(items)}</ul><br><a href='/recipes/'>ყველა რეცეპტი</a>"
    return HttpResponse(html)

def random_recipe(request):
    if not RECIPES:
        raise Http404("No recipe found")

    recipe = random.choice(RECIPES)

    recipe_id = recipe["id"]

    return redirect(f"/recipes/{recipe_id}")

def recipe_by_slug(request, slug):
    result = [r for r in RECIPES if slug == r["slug"]]
    
    if not result:
        raise Http404("No recipe found with such slug")

    
    recipe = result[0]
    
    items = [f"<li>{ing}</li>" for ing in recipe.get("ingredients", [])]
    html = f"<h1>{recipe['name']}</h1><h3>ინგრედიენტები:</h3><ul>{''.join(items)}</ul><br><a href='/recipes/'>ყველა რეცეპტი</a>"
    return HttpResponse(html)

def recipe_detail(request, pk):
    recipe = find_recipe(pk)

    if recipe == None:
        raise Http404("No recipe found")

    ingredient_lines = [f"<li>{ing}</li>" for ing in recipe["ingredients"]]
    ingredient_html = f"<ul>{"".join(ingredient_lines)}</ul>"

    body = f"საჭმელი: {recipe["name"]} ,მომზადების დრო: {recipe["minutes"]}, კატეგორია: {recipe["category"]}, ვეგეტარიანული: {"კი" if recipe["vegetarian"] else "არა"}, ინგრედიენტები: {ingredient_html} "

    return HttpResponse(body)

