from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

SEARCH_STRING = ""

#---------------------------------------------- HOMEPAGE CODE ------------------------------------------------

@app.route("/")
def render_page():
    """ returns rendered homepage """

    return render_template("Homepage.html")

#---------------------------------------------- EVAN'S CODE --------------------------------------------------

@app.route("/student_delete/<string:net_id>", methods=['POST'])
def delete_roster(net_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_student_by_netid(net_id)
        result = {'success': True, 'response': 'Removed student'}
    except:
        result = {'success': False, 'response': 'oopsies'}

    print("RESULT:\n" + result['response'], end='\n\n')
    return jsonify(result)


@app.route("/student_update/<string:net_id>", methods=['POST'])
def update_roster(net_id):

    data = request.get_json()
    print(data)

    try:
        db_helper.update_roster(data['net_id'], data['first_name'], data['last_name'], data['grade'], data['section'])
        result = {'success': True, 'response': 'Roster updated'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    print("RESULT:\n" + result['response'], end='\n\n')
    return jsonify(result)


@app.route("/student_insert", methods=['POST'])
def insert_roster():
    data = request.get_json()
    
    try:
        db_helper.insert_new_student(data['net_id'], data['first_name'], data['last_name'], data['grade'], data['section'])
        result = {'success': True, 'response': 'Student inserted'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    print("RESULT:\n" + result['response'], end='\n\n')
    return jsonify(result)


@app.route("/student_search", methods=['POST'])
def search_roster():
    data = request.get_json()
    
    global SEARCH_STRING
    SEARCH_STRING = data['net_id']

    return ""


@app.route("/Roster")
def roster_page():
    """ returns rendered homepage """

    global SEARCH_STRING
    curr_netid = SEARCH_STRING

    items = db_helper.fetch_roster(net_id=curr_netid)
    aq_items = db_helper.advanced_query()

    if curr_netid == "":
        curr_netid = "NetID"

    return render_template("roster.html", items=items, curr_netid=curr_netid, aq_items=aq_items)

#----------------------------------------------------JIMMY'S CODE----------------------------------------------

@app.route("/instrument_delete/<int:instrumentid>", methods=['POST'])
def delete_instruments(instrumentid):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_instrument_by_id(instrumentid)
        result = {'success': True, 'response': 'Removed instrument'}
    except:
        result = {'success': False, 'response': 'oopsies'}

    return jsonify(result)


@app.route("/instrument_update/<int:instrumentid>", methods=['POST'])
def update_instruments(instrumentid):

    data = request.get_json()
    print(data)

    try:
        db_helper.update_instrument(data['instrumentid'], data['instrument_type'], data['brand'])
        result = {'success': True, 'response': 'Instrument Updated'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    return jsonify(result)


@app.route("/instrument_insert", methods=['POST'])
def insert_instruments():
    data = request.get_json()
    
    try:
        db_helper.insert_new_instrument(data['instrumentid'], data['instrument_type'], data['brand'])
        result = {'success': True, 'response': 'Instrument Inserted'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    return jsonify(result)


@app.route("/instrument_search/<int:instrumentid>", methods=['POST'])
def search_instruments(instrumentid):
    data = request.get_json()

    db_helper.searchItems = db_helper.search_instrument_by_id(data['instrumentid'])

@app.route("/Instruments")
def instruments_page():
    """ returns rendered homepage """

    items = db_helper.fetch_instruments()
    advQItems = db_helper.find_maintenance_stats()
    return render_template("instruments.html", items=[items, advQItems, db_helper.searchItems])

#---------------------------------------------------- ALEX'S CODE -----------------------------------------------------

@app.route("/maintenance_delete/<int:maintenance_id>", methods=['POST'])
def delete_maintenance(maintenance_id):
    """ recieved post requests for entry delete """
    print("deleting")
    try:
        db_helper.remove_maintenance_by_id(maintenance_id)
        result = {'success': True, 'response': 'Removed maintenance'}
    except:
        result = {'success': False, 'response': 'Remove failed'}
    print(result)
    return jsonify(result)


@app.route("/maintenance_update/<int:maintenance_id>", methods=['POST'])
def update_maintenance(maintenance_id):

    data = request.get_json()
    print(data)

    try:
        db_helper.update_maintenance(data['instrumentid'], data['send_date'], data['return_date'], data["maintenance_location"], data["cost"], data["maintenance_id"])
        result = {'success': True, 'response': 'Maintenance Updated'}
    except:
        result = {'success': False, 'response': 'Update failed'}
    
    return jsonify(result)


@app.route("/maintenance_insert", methods=['POST'])
def insert_maintenance():
    data = request.get_json()
    
    try:
        db_helper.insert_new_maintenance(data['instrumentid'], data['send_date'], data['return_date'], data["maintenance_location"], data["cost"], data["maintenance_id"])
        result = {'success': True, 'response': 'Maintenance Inserted'}
    except:
        result = {'success': False, 'response': 'Insert failed'}
    
    return jsonify(result)

@app.route("/maintenance_search/<int:maintenance_id>", methods=['POST'])
def search_maintenance(maintenance_id):
    data = request.get_json()
    print(data)
    try:
        db_helper.search_maintenance(data['maintenance_id'])
        result = {'success': True, 'response': 'Maintenance Searched'}
    except:
        result = {'success': False, 'response': 'Search failed'}
    
    return jsonify(result)

@app.route("/Maintenance")
def maintenance_page():
    """ returns rendered homepage """
    fetchCurr = db_helper.fetch_maintenance()
    fetchAdv = db_helper.advanced_query()
    return render_template("Maintenance.html", currTableState=fetchCurr, advq=fetchAdv, searchCurr=db_helper.searchRes)

#-------------------------------------------------------- ANDY'S CODE -------------------------------------------------

@app.route("/rental_delete/<int:rental_id>", methods=['POST'])
def delete_rentals(rental_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_rental_by_id(rental_id)
        result = {'success': True, 'response': 'Removed rental'}
    except:
        result = {'success': False, 'response': 'stinky'}

    return jsonify(result)


@app.route("/rental_update/<int:rental_id>", methods=['POST'])
def update_rentals(rental_id):

    data = request.get_json()
    print(data)

    try:
        db_helper.update_rental(data['rental_id'], data['instrument_id'], data['net_id'], data['date_out'], data['date_in'])
        result = {'success': True, 'response': 'Rental Updated'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    return jsonify(result)


@app.route("/rental_insert", methods=['POST'])
def insert_rentals():
    data = request.get_json()
    
    print(data)
    try:
        db_helper.insert_new_rental(data['rental_id'], data['instrument_id'], data['net_id'], data['date_out'], data['date_in'])
        result = {'success': True, 'response': 'Rental Inserted'}
    except:
        result = {'success': False, 'response': 'uh oh'}
    
    return jsonify(result)


@app.route("/Rentals")
def rentals_page():
    """ returns rendered homepage """
    items = db_helper.fetch_rentals()
    query = db_helper.fetch_advanced_query()
    
    return render_template("Rentals.html", items=items , sr=db_helper.searchres, aqres=query)

@app.route("/rental_search", methods=["POST"])
def search_rentals():
    data = request.get_json()

    print(data)

    try:
        db_helper.search(data['rental_id'])
        result = {'success': True, 'response': 'Search Completed'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    print(db_helper.searchres)
    return jsonify(result)
