from app import db

searchRes = []
searchItems = [] #yes this is needed

#---------------------------------------------  LOGIN PAGE  ---------------------------------------------------
def login_search(username: str, password: str) -> (bool, int):
    conn = db.connect()
    query = 'SELECT * FROM LoginInfo WHERE username="{}" AND password="{}"'.format(username, password)
    queryResults = conn.execute(query).fetchall()
    conn.close()

    print('here:')
    print(queryResults)

    if len(queryResults) > 0:
        return (True, queryResults[0][2])
    else:
        return (False, 0)


#-------------------------------------------- REGISTER PAGE ---------------------------------------------------
def register_insert(username: str, password: str, admin: int) -> None:
    """ Adds new user to database
    Args:
        username (str): username to insert
        password (str): password to insert
        admin (int): 1 if admin, 0 else
    
    Returns:
        None
    """

    conn = db.connect()
    query = 'INSERT INTO LoginInfo VALUES ("{}", "{}", {});'.format(username, password, admin)
    conn.execute(query)
    conn.close()


#--------------------------------------------- EVAN'S CODE ----------------------------------------------------
def fetch_roster(net_id=""):
    """ Fetches information from Roster table by given net_id

    Args:
        net_id (str): Targeted net_id

    Returns:
        all rows as an array of dictionaries
    """

    conn = db.connect()
    query = 'SELECT * FROM Roster WHERE net_id LIKE "%%{n}%%" ORDER BY last_name, first_name;'.format(n=net_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    student_list = []
    for result in query_results:
        item = {
            "net_id": result[0],
            "first_name": result[1],
            "last_name": result[2],
            "grade": result[3],
            "section":result[4]
        }
        student_list.append(item)

    print("\nFETCH ROSTER QUERY:\n" + query)

    return student_list

def update_roster(net_id, first_name, last_name, grade, section):
    """Updates Roster entry based on given `net_id`

    Args:
        net_id (str): Targeted net_id
        first_name (str): Updated first_name
        last_name (str): Updated last_name
        grade (int): Updated grade
        section (str): Updated section

    Returns:
        None
    """

    if net_id == "":
        print("NO NETID FOR UPDATE")
        return
    
    conn = db.connect()
    if first_name == "" or last_name == "" or grade == "" or section == "":
        query = 'SELECT * FROM Roster WHERE net_id = "{n}"'.format(n=net_id)
        query_results = conn.execute(query).fetchall()
        if first_name == "":
            first_name = query_results[0][1]
        if last_name == "":
            last_name = query_results[0][2]
        if grade == "":
            grade = query_results[0][3]
        if section == "":
            section = query_results[0][4]

    query = 'UPDATE Roster '\
            'SET first_name = "{fn}", last_name = "{ln}", grade = {g}, section = "{s}" '\
            'WHERE net_id = "{n}";'.format(fn=first_name, ln=last_name, g=grade, s=section, n=net_id)
    conn.execute(query)
    conn.close()

    print("\nUPDATE ROSTER QUERY:\n" + query)


def insert_new_student(net_id, first_name, last_name, grade, section):
    """Insert new student row to Roster table.

    Args:
        net_id (str): Student NetID
        first_name (str): Student first name
        last_name (str): Student last name
        grade (int): Student grade
        section (str): Student section

    Returns:
        None
    """

    if net_id == "":
        print("NO NETID FOR INSERT")
        return

    if first_name == "":
        first_name = "NULL"
    else:
        first_name = '"' + first_name + '"'
    
    if last_name == "":
        last_name = "NULL"
    else:
        last_name = '"' + last_name + '"'

    if section == "":
        section = "NULL"
    else:
        section = '"' + section + '"'

    if grade == "":
        grade = "NULL"
    
    conn = db.connect()
    query = 'INSERT INTO Roster '\
            'VALUES ("{n}", {fn}, {ln}, {g}, {s});'.format(n=net_id, fn=first_name, ln=last_name, g=grade, s=section)
    conn.execute(query)
    conn.close()

    print("\nINSERT ROSTER QUERY:\n" + query)


def remove_student_by_netid(net_id):
    """ remove entries based on instrument ID. 
    
    Args:
        net_id (str): NetID of student to be removed
    
    Returns:
        None
    """
    conn = db.connect()
    query = 'DELETE FROM Roster '\
            'WHERE net_id = "{n}";'.format(n=net_id)
    conn.execute(query)
    conn.close()

    print("\nDELETE ROSTER QUERY:\n" + query)


def advanced_query_roster():
    """ Query to find all instruments that are not currently in inventory

    Returns:
        all resulting rows as an array of dictionaries
    """
    conn = db.connect()
    query = '(SELECT i.instrumentid AS instrument_id, i.instrument_type, m.send_date AS date_out '\
            'FROM Maintenance m JOIN Instruments i ON i.instrumentid = m.instrumentid '\
            'WHERE m.return_date IS NULL) '\
            'UNION '\
            '(SELECT i.instrumentid AS instrument_id, i.instrument_type, r.date_out '\
            'FROM Rentals r JOIN Instruments i ON i.instrumentid = r.instrument_id '\
            'WHERE r.date_in IS NULL) '\
            'ORDER BY date_out '\
            'LIMIT 15;'
    query_results = conn.execute(query).fetchall()
    conn.close()
    student_list = []
    for result in query_results:
        item = {
            "instrument_id": result[0],
            "instrument_type": result[1],
            "date_out": result[2]
        }
        student_list.append(item)

    return student_list

#------------------------------------------- JIMMY'S CODE ----------------------------------------------

def fetch_instruments() -> dict:
    """ Fetches all rows of the Instruments table

    Returns:
        all rows as an array of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * FROM Instruments ORDER BY instrumentid;").fetchall()
    conn.close()
    instrument_list = []
    for result in query_results:
        item = {
            "instrumentid": result[0],
            "brand": result[1],
            "instrument_type": result[2]
        }
        instrument_list.append(item)

    return instrument_list


def find_maintenance_stats() -> dict:
    """ Fetches all rows of the Instruments table

    Returns:
        all rows as an array of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT i.instrumentid, i.instrument_type, COUNT(m.maintenance_id) AS maintCnt, SUM(m.cost) AS totCost FROM Instruments i JOIN Maintenance m USING(instrumentid) GROUP BY i.instrumentid, i.instrument_type ORDER BY totCost DESC;").fetchall()
    conn.close()
    m_list = []
    for result in query_results:
        item = {
            "instrumentid": result[0],
            "instrument_type": result[1],
            "maintCnt": result[2],
            "totCost" : result[3]
        }
        m_list.append(item)

    return m_list


def update_instrument(instrumentid: int, instrument_type: str, brand: str) -> None:
    """Updates instrument entry based on given `instrumentid`

    Args:
        instrumentid (int): Targeted instrumentid
        instrument_type (str): Updated type
        brand (str): Updated brand

    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE Instruments SET instrument_type = "{}", brand = "{}" WHERE instrumentid = {};'.format(instrument_type, brand, instrumentid)
    print(query)
    conn.execute(query)
    conn.close()


def insert_new_instrument(instrumentid: int, instrument_type: str, brand: str) ->  None:
    """Insert new instrument row to Instruments table.

    Args:
        instrument_type (str): Instrument type
        brand (str): Instrument brand

    Returns:
        None
    """

    conn = db.connect()
    query = 'INSERT INTO Instruments VALUES ({}, "{}", "{}");'.format(instrumentid, brand, instrument_type)
    conn.execute(query)
    conn.close()


def remove_instrument_by_id(instrumentid: int) -> None:
    """ remove entries based on instrument ID """
    conn = db.connect()
    query = 'DELETE FROM Instruments WHERE instrumentid={};'.format(instrumentid)
    conn.execute(query)
    conn.close()


def search_instrument_by_id(instrumentid: int) -> dict:
    conn = db.connect()
    query = 'SELECT * FROM Instruments WHERE instrumentid={};'.format(instrumentid)
    queryResults = conn.execute(query)
    conn.close()
    searchItemList = []
    for result in queryResults:
        item = {
            'instrumentid': result[0],
            'brand': result[1],
            'instrument_type': result[2]
        }
        searchItemList.append(item)

    return searchItemList

    #--------------------------------------------- ALEX'S CODE --------------------------------------------------

def fetch_maintenance() -> dict:
    """ Fetches all rows of the Instruments table

    Returns:
        all rows as an array of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * FROM Maintenance ORDER BY maintenance_id;").fetchall()
    conn.close()
    maintenance_list = []
    for result in query_results:
        item = {
            "maintenance_id": result[5],
            "instrumentid": result[0],
            "send_date": result[1],
            "return_date": result[2],
            "maintenance_location": result[3],
            "cost": result[4]
        }
        maintenance_list.append(item)

    return maintenance_list

def search_maintenance(maintenance_id:int) -> None:
    conn = db.connect()
    query  = 'SELECT * FROM Maintenance where maintenance_id = {};'.format(maintenance_id)
    print(query)
    query_results = conn.execute(query)
    conn.close()
    searchRes.clear()
    for result in query_results:
        item = {
            "maintenance_id": result[5],
            "instrumentid": result[0],
            "send_date": result[1],
            "return_date": result[2],
            "maintenance_location": result[3],
            "cost": result[4]
        }
        searchRes.append(item)

def update_maintenance(instrumentid: int, send_date: str, return_date: str, maintenance_location: str, cost: int, maintenance_id: int) -> None:
    """Updates instrument entry based on given `instrumentid`

    Args:
        instrumentid (int): id of instrument maintained
        send_date (str): Date sent out for maintenance format yyyy-mm-dd
        return_date (str): Date instrument returned from maintenance
        maintenance_location (str): location of maintenance facility
        cost (int): cost of maintenance
        maintenance_id (int): targeted maintenance_id

    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE Maintenance SET instrumentid = {}, send_date = "{}", return_date = "{}", maintenance_location = "{}", cost = {} WHERE maintenance_id = {};'.format(instrumentid, send_date, return_date, maintenance_location, cost, maintenance_id)
    print(query)
    conn.execute(query)
    conn.close()


def insert_new_maintenance(instrumentid: int, send_date: str, return_date: str, maintenance_location:str, cost:int, maintenance_id:int) ->  None:
    """Insert new maintenance record to Maintenance table.

    Args:
        instrumentid (int): id of instrument maintained
        send_date (str): Date sent out for maintenance format yyyy-mm-dd
        return_date (str): Date instrument returned from maintenance
        maintenance_location (str): location of maintenance facility
        cost (int): cost of maintenance

    Returns:
        None
    """

    conn = db.connect()
    query = 'INSERT INTO Maintenance VALUES ({}, "{}", "{}", "{}", {}, {});'.format(instrumentid, send_date, return_date, maintenance_location, cost, maintenance_id)
    print(query)
    conn.execute(query)
    conn.close()


def remove_maintenance_by_id(maintenance_id: int) -> None:
    """ remove entries based on maintenance_id """
    
    conn = db.connect()
    query = 'DELETE FROM Maintenance WHERE maintenance_id={};'.format(maintenance_id)
    print(query)
    conn.execute(query)
    conn.close()

def advanced_query_maintenance() -> dict:
    """ Fetches results of advanced query
    
    Returns:
        All rows as array of dictionaries
    """
    conn = db.connect()
    query_results = conn.execute("Select o.section, count(o.net_id) num_members from Roster o where o.net_id not in (select distinct e.net_id from Rentals e where date_in = null) group by o.section order by num_members desc").fetchall()
    conn.close()
    adv_list = []
    for result in query_results:
        item = {
            "section": result[0],
            "num_members": result[1],
        }
        adv_list.append(item)

    return adv_list

#-------------------------------------------------------- ANDY'S CODE --------------------------------------------------

def fetch_rentals() -> dict:
    """ Fetches all rows of the Rentals table

    Returns:
        all rows as an array of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * FROM Rentals ORDER BY rental_id;").fetchall()
    conn.close()
    rental_list = []
    for result in query_results:
        item = {
            "rental_id": result[0],
            "instrument_id": result[1],
            "net_id": result[2],
            "date_out": result[3],
            "date_in": result[4]
        }
        rental_list.append(item)

    return rental_list


def fetch_advanced_query() -> dict:
    """Fetches results of advanced query"""
    conn = db.connect()
    query_results = conn.execute("SELECT i.instrument_type, COUNT(r.rental_id) AS RentalCount FROM Instruments i JOIN Rentals r ON (instrumentid) GROUP BY i.instrument_type ORDER BY RentalCount DESC").fetchall()
    conn.close()
    query_list = []
    for result in query_results:
        item = {
            "instrument_type": result[0],
            "RentalCount": result[1]
        }
        query_list.append(item)
    return query_list


def update_rental(rental_id: int, instrument_id: int, net_id: str, date_out: str, date_in: str) ->  None:
    """Updates instrument entry based on given `instrumentid`

    Args:
        instrumentid (int): Targeted instrumentid
        instrument_type (str): Updated type
        brand (str): Updated brand

    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE Rentals SET instrument_id = {}, net_id = "{}", date_out = "{}", date_in = "{}" WHERE rental_id = {};'.format(instrument_id, net_id, date_out, date_in, rental_id)
    print(query)
    conn.execute(query)
    conn.close()


def insert_new_rental(rental_id: int, instrument_id: int, net_id: str, date_out: str, date_in: str) ->  None:
    """Insert new Rental row to Rentals table.

    Args:
        rental_id (int): Distinct rental ID
        instrument_id (int): Distinct instrument ID
        net_id (str): Student's NetID
        date_out (str): Beginning date of rental
        date_in (str): date of rental return

        

    Returns:
        None
    """

    conn = db.connect()
    query = 'INSERT INTO Rentals VALUES ({}, {}, "{}", "{}", "{}");'.format(rental_id, instrument_id, net_id, date_out, date_in)
    print(query)
    conn.execute(query)
    conn.close()


def remove_rental_by_id(rental_id: int) -> None:
    """ remove entries based on rental ID """
    conn = db.connect()
    query = 'DELETE FROM Rentals WHERE rental_id={};'.format(rental_id)
    conn.execute(query)
    conn.close()

searchres = []

def search(rental_id: int) -> None:
    """Searches database for entry by rental ID
    
    Args:
        rental_id (int): The rental ID to be found"""
    
    
    conn = db.connect()

    search_result = conn.execute('SELECT * FROM Rentals WHERE rental_id={n};'.format(n=rental_id))

    conn.close()
    searchres.clear()
    for result in search_result:
        item = {
            "rental_id": result[0],
            "instrument_id": result[1],
            "net_id": result[2],
            "date_out": result[3],
            "date_in": result[4]
        }
        searchres.append(item)
