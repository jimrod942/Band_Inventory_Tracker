from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

SEARCH_STRING = ""
ADMIN_KEY = 'h4rryb0u53r'
LOGIN_USERNAME = ""
LOGIN_PASSWORD = ""
LOGIN_ADMIN = False

#---------------------------------------------- HOMEPAGE CODE ------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def render_page():
    """ returns rendered homepage """
    global LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_ADMIN
    print("page reloaded:")
    print(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_ADMIN)

 

    return render_template("Homepage.html", username=LOGIN_USERNAME, unreturned = db_helper.fetch_unreturnedRentals(), seniors = db_helper.fetch_uupperclassmen(), reps = db_helper.fetch_numberRepairs())


@app.route("/signout", methods=["POST"])
def signout():
    global LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_ADMIN

    print(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_ADMIN)

    LOGIN_USERNAME = ""
    LOGIN_PASSWORD = ""
    LOGIN_ADMIN = False

    print("\nsigned out:")
    print(LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_ADMIN)

    return LOGIN_USERNAME


#---------------------------------------------- LOGIN PAGE ---------------------------------------------------

@app.route("/Login")
def login_page():
    """ returns rendered login page """

    return render_template("Login.html")


@app.route("/login_search", methods=["POST"])
def login_search():
    """ checks that user exists in the database """

    data = request.get_json()

    result = db_helper.login_search(data['username'], data['password'])

    global LOGIN_USERNAME, LOGIN_PASSWORD, LOGIN_ADMIN
    
    if result[0]:
        LOGIN_USERNAME = data['username']
        LOGIN_PASSWORD = data['password']
        LOGIN_ADMIN = result[1]

    return render_template("Homepage.html", username=LOGIN_USERNAME)


#--------------------------------------------- REGISTER PAGE -------------------------------------------------

@app.route("/Register")
def register_page():
    return render_template("Register.html")


@app.route("/register_insert", methods=["POST"])
def register_insert():

    data = request.get_json()

    isAdmin = 0
    if data['admin'] == ADMIN_KEY:
        isAdmin = 1

    try:
        db_helper.register_insert(data['username'], data['password'], isAdmin)
        result = {'success': True, 'response': 'New User Registered'}
    except:
        result = {'success': False, 'response': 'oopsies'}

    return jsonify(result)


#---------------------------------------------- EVAN'S CODE --------------------------------------------------

@app.route("/student_delete/<string:net_id>", methods=['POST'])
def delete_roster(net_id):
    """ recieved post requests for entry delete """

    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

    try:
        db_helper.remove_student_by_netid(net_id)
        result = {'success': True, 'response': 'Removed student'}
    except:
        result = {'success': False, 'response': 'oopsies'}

    return jsonify(result)


@app.route("/student_update/<string:net_id>", methods=['POST'])
def update_roster(net_id):
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

    data = request.get_json()

    try:
        db_helper.update_roster(data['net_id'], data['first_name'], data['last_name'], data['grade'], data['section'])
        result = {'success': True, 'response': 'Roster updated'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    return jsonify(result)


@app.route("/student_insert", methods=['POST'])
def insert_roster():
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

    data = request.get_json()
    
    try:
        db_helper.insert_new_student(data['net_id'], data['first_name'], data['last_name'], data['grade'], data['section'])
        result = {'success': True, 'response': 'Student inserted'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
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

    global SEARCH_STRING, LOGIN_ADMIN
    curr_netid = SEARCH_STRING
    admin = "false"

    if LOGIN_ADMIN:
        admin = "true"

    items = db_helper.fetch_roster(net_id=curr_netid)
    aq_items = db_helper.advanced_query_roster()

    if curr_netid == "":
        curr_netid = "NetID"

    return render_template("roster.html", items=items, curr_netid=curr_netid, aq_items=aq_items, admin=admin)

#----------------------------------------------------JIMMY'S CODE----------------------------------------------

@app.route("/instrument_delete/<int:instrumentid>", methods=['POST'])
def delete_instruments(instrumentid):
    """ recieved post requests for entry delete """

    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

    try:
        db_helper.remove_instrument_by_id(instrumentid)
        result = {'success': True, 'response': 'Removed instrument'}
    except:
        result = {'success': False, 'response': 'oopsies'}

    return jsonify(result)


@app.route("/instrument_update/<int:instrumentid>", methods=['POST'])
def update_instruments(instrumentid):
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

    data = request.get_json()

    try:
        db_helper.update_instrument(data['instrumentid'], data['instrument_type'], data['brand'])
        result = {'success': True, 'response': 'Instrument Updated'}
    except:
        result = {'success': False, 'response': 'oopsie'}
    
    return jsonify(result)


@app.route("/instrument_insert", methods=['POST'])
def insert_instruments():
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

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

    global LOGIN_ADMIN, LOGIN_USERNAME
    admin = "false"

    if LOGIN_ADMIN:
        admin = "true"
        
    items = db_helper.fetch_instruments()
    advQItems = db_helper.find_maintenance_stats()
    return render_template("instruments.html", items=[items, advQItems, db_helper.searchItems], admin=admin)

#---------------------------------------------------- ALEX'S CODE -----------------------------------------------------

@app.route("/maintenance_delete/<int:maintenance_id>", methods=['POST'])
def delete_maintenance(maintenance_id):
    """ recieved post requests for entry delete """

    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

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
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

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
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

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

    global LOGIN_ADMIN
    admin = "false"

    if LOGIN_ADMIN:
        admin = "true"

    fetchCurr = db_helper.fetch_maintenance()
    fetchAdv = db_helper.advanced_query_maintenance()
    return render_template("Maintenance.html", currTableState=fetchCurr, advq=fetchAdv, searchCurr=db_helper.searchRes, admin=admin)

#-------------------------------------------------------- ANDY'S CODE -------------------------------------------------

@app.route("/rental_delete/<int:rental_id>", methods=['POST'])
def delete_rentals(rental_id):
    """ recieved post requests for entry delete """

    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

    try:
        db_helper.remove_rental_by_id(rental_id)
        result = {'success': True, 'response': 'Removed rental'}
    except:
        result = {'success': False, 'response': 'stinky'}

    return jsonify(result)


@app.route("/rental_update/<int:rental_id>", methods=['POST'])
def update_rentals(rental_id):
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

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
    global LOGIN_ADMIN
    if not LOGIN_ADMIN:
        print("\nADMIN FAILED\n")
        return ""

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

    global LOGIN_ADMIN
    admin = "false"

    if LOGIN_ADMIN:
        admin = "true"

    items = db_helper.fetch_rentals()
    query = db_helper.fetch_advanced_query()
    
    return render_template("Rentals.html", items=items , sr=db_helper.searchres, aqres=query, admin=admin)

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
