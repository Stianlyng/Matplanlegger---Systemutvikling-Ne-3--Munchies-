from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup
from sqlalchemy import *


# Add default values to recipe availability
def insert_to_recipeavalilability():
    session = loadSession()
    avail1 = RecipeAvailability(avilableFor="All")
    avail2 = RecipeAvailability(avilableFor="Group")
    avail3 = RecipeAvailability(avilableFor="User")
    session.add_all([avail1, avail2, avail3])
    session.commit()
    session.close()


# Add recipe
def insert_to_recipe(name, shortDescription, description, image, userGroup, recipeAvailability, weeklymenu):
    session = loadSession()
    new_recipe = Recipe(name=name, shortDescription=shortDescription, description=description, image=image,
                        userGroup_iduserGroup=userGroup, recipeAvailability_idrecipeAvailability=recipeAvailability,
                        weeklyMenu_idweeklyMenu=weeklymenu)
    session.add(new_recipe)
    session.commit()
    session.close()


def fetch_recipe_where_recipeId_equals(recipeId):
    session = loadSession()
    session.close()
    return session.query(Recipe).where(Recipe.idRecipe == recipeId).first()

def fetch_recipeID_where_name_equals(name):
    session = loadSession()
    session.close()
    return session.query(Recipe.idRecipe).where(Recipe.name == name).first()

# Add to recipe_has_ingredient
def insert_to_recipe_has_ingredient(recipe, ingredient, quantity):
    session = loadSession()
    new_recipeIngredient = RecipeHasIngredient(recipe_idRecipe=recipe, ingredient_idingredient=ingredient,
                                               quantity=quantity)
    session.add(new_recipeIngredient)
    session.commit()
    session.close()


# Add to recipe_has_weeklyMenu
def insert_to_recipe_has_weeklymenu(recipe, year, week, expectedConsumption, actualConsumption):
    session = loadSession()
    new_recipeWeeklymenu = RecipeHasWeeklyMenu(recipe_idRecipe=recipe, weeklyMenu_year=year, weeklyMenu_weekNum=week,
                                               expectedConsumption=expectedConsumption,
                                               actualConsumption=actualConsumption)
    session.add(new_recipeWeeklymenu)
    session.commit()
    session.close()


def fetch_all_recipes():
    session = loadSession()
    session.close()
    return session.query(Recipe).all()

def fetch_all_recipes_to_group(group_id):
    session = loadSession()
    session.close()
    return session.query(Recipe).where(Recipe.userGroup_iduserGroup == group_id).all()


def remove_from_recipe_has_ingredient(recipeID, ingredient_id):
    session = loadSession()
    session.query(RecipeHasIngredient).filter(
        and_(RecipeHasIngredient.recipe_idRecipe == recipeID, RecipeHasIngredient.ingredient_idingredient == ingredient_id)).delete(
        synchronize_session=False)
    session.commit()
    session.close()


