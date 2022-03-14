from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

import backend.ingredients.queries as ingredient_queries
import backend.auth.queries as auth_queries

from backend.ingredients.forms import RegisterForm
from backend.ingredients.queries import *
ingredient = Blueprint('ingredient', __name__, template_folder='templates', url_prefix='/ingredient')


@ingredient.route('/new', methods=['GET', 'POST'])
def new():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        ingredientName = form.ingredientName.data
        check_ingredient = fetchIngredient(ingredientName)

        usergroup = form.usergroup.data

        fetchedusergroup = fetchUserGroup(usergroup) # TODO bør være en dropdown der brukeren kan velge
        fetchedusergroup_ID = fetchedusergroup.iduserGroup

        if check_ingredient: #Sjekker om ingrediens finnes.
            flash("Ingrediens er allerede registrert", "danger")
            print("Ingrediens er allerede registrert")
            return render_template('newingredient.html', form=form, heading="Registrer ny ingrediens") #vet ikke om heading trengs?

        ingredient_queries.insert_to_ingredients(ingredientName)

        fetchedingredientID = fetchIngredient(ingredientName)  # TODO Fetch ingredientID from new or existing
        ingredientID = fetchedingredientID.idingredient

        price = form.price.data
        unit = form.unit.data


        auth_queries.insert_to_usergroup_has_ingredient(fetchedusergroup_ID, ingredientID, price, unit)

        flash('Ingrediensen er registrert!!')
        return redirect(url_for("ingredient.new"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('newingredient.html', form=form)
