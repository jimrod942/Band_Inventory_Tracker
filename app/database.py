from app import db

searchItems = []

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