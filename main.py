from flask import Flask, request
from functions.time_series import handler as series
from functions.update import handler as update
from functions.new_series import handler as new_series
from functions.painel import handler as painel
from functions.lethality import handler as lethality
from functions.simulator import handler as simulate
from functions.state_table import handler as state_table
from functions.region_pie import handler as region_pie
from functions.tests import handler as test_series
from functions.test_100k_per_uf import handler as test_100k
from functions.series_100k_per_uf import handler as serie_100k

app = Flask(__name__)


@app.route('/update', methods=['POST'])
def _update():
    return update()


@app.route('/series', methods=['POST'])
def _series():
    body = request.get_json()
    return series(body)


@app.route('/new_series', methods=['POST'])
def _new_series():
    body = request.get_json()
    return new_series(body)


@app.route('/covid_painel', methods=['POST'])
def _covid_painel():
    body = request.get_json()
    return painel(body)


@app.route('/simulator', methods=['POST'])
def _simulate():
    body = request.get_json()
    return simulate(body)


@app.route('/lethality', methods=['POST'])
def _lethality():
    body = request.get_json()
    return lethality(body)


@app.route('/state_table', methods=['POST'])
def _state_table():
    return state_table()


@app.route('/region_pie', methods=['POST'])
def _region_pie():
    body = request.get_json()
    return region_pie(body)


@app.route('/test_series', methods=['POST'])
def _test_series():
    body = request.get_json()
    return test_series(body)


@app.route('/test_100k_per_uf', methods=['POST'])
def _test_100k():
    return test_100k()


@app.route('/series_100k_per_uf', methods=['POST'])
def _serie_100k():
    return serie_100k()


app.run()
