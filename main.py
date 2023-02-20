# Python
from typing import Any

# Other
import requests
from requests.models import Response

# Flask
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from flask.app import Flask as FlaskApp

# Local
from models.pokemon import (
    Pokemon,
    Name,
    Base
)

app: FlaskApp = Flask(__name__)
app.config['SECRET_KEY'] = "fsdfsdfsdfsdfsdfsdfsd"
pokemons: list[Pokemon] = []


@app.route("/home")
def home_page() -> str:
    return "Welcome to my first page!"


@app.route("/")
def main_page() -> str:
    return render_template(
        'index.html',
        ctx_lst=pokemons
    )


@app.route('/info', methods=['GET', 'POST'])
def info_pok():
    if request.method == 'POST':
        pokemon = None
        name_pock = request.form['name_pock']
        for pok in pokemons:
            if name_pock.lower() == pok.name.english.lower():
                pokemon = pok
                return render_template('info_pock.html', pokemon=pokemon)
        flash('Incorrect name', category='Error')
    return redirect(url_for('main_page'))


@app.route("/num")
def get_nubmers() -> str:
    result: str = ""
    for i in range(1, 2001):
        result += f"<h2>{i}</h2>"

    return result


if __name__ == '__main__':
    URL: str = (
        'https://raw.githubusercontent.'
        'com/fanzeyi/pokemon.json/'
        'master/pokedex.json'
    )
    response: Response = \
        requests.get(URL)
    data: list[dict] = response.json()

    pokemon: dict[str, Any]
    for pokemon in data:
        base = Base(
            *list(pokemon.get('base').values())
        )
        name = Name(
            *list(pokemon.get('name').values())
        )
        pkm = Pokemon(
            id=pokemon.get('id'),
            name=name,
            type=pokemon.get('type'),
            base=base
        )
        pokemons.append(pkm)

    app.run(
        port=8080,
        debug=True
    )
