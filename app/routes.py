from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/instrument_delete/<int:instrumentid>", methods=['POST'])
def delete(instrumentid):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_instrument_by_id(instrumentid)
        result = {'success': True, 'response': 'Removed instrument'}
    except:
        result = {'success': False, 'response': 'oopsies'}

    return jsonify(result)


@app.route("/instrument_update/<int:instrumentid>", methods=['POST'])
def update(instrumentid):

    data = request.get_json()
    print(data)

    try:
        db_helper.update_instrument(data['instrumentid'], data['instrument_type'], data['brand'])
        result = {'success': True, 'response': 'Instrument Updated'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    return jsonify(result)


@app.route("/instrument_insert", methods=['POST'])
def insert():
    data = request.get_json()
    
    try:
        db_helper.insert_new_instrument(data['instrumentid'], data['instrument_type'], data['brand'])
        result = {'success': True, 'response': 'Instrument Inserted'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    return jsonify(result)


@app.route("/instrument_search/<int:instrumentid>", methods=['POST'])
def search(instrumentid):
    data = request.get_json()

    db_helper.searchItems = db_helper.search_instrument_by_id(data['instrumentid'])

@app.route("/")
def homepage():
    """ returns rendered homepage """

    items = db_helper.fetch_instruments()
    advQItems = db_helper.find_maintenance_stats()
    return render_template("instruments.html", items=[items, advQItems, db_helper.searchItems])