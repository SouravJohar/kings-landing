import sqlite3 as db
import random
import string
from faker import Faker

conn = db.connect("database/kingsbase.db")
c = conn.cursor()

month = "may"
dates_start_from = "01-05-2018"

flight_numbers = [
    'KL101',
    'KL102',
    'KL103',
    'KL104',
    'KL105',
    'KL201',
    'KL202',
    'KL203',
    'KL204',
    'KL205',
    'KL301',
    'KL302',
    'KL303',
    'KL304',
    'KL305',
    'KL401',
    'KL402',
    'KL403',
    'KL404',
    'KL405',
]

cities = {
    "Jaipur": "JAI",
    "Chennai": "MAA",
    "Mumbai": "BOM",
    "Cochin": "COK",
    'Trichy': 'TRZ',
    'Bangalore': 'BLR',
    'Hyderabad': 'HYD',
    'Coimbatore': 'CBJ',
    'New Delhi': 'DEL',
    'Kolkata': 'CCU',
    'Bhopal': 'BHO',
    'Daman': 'NNB',
    'Goa': 'GOI',
    'Indore': 'IDR',
    'Singapore': 'SIN',
    'Los Angeles': 'LAX',
    'Atlanta': 'ATL',
    'Dubai': 'DXB',
    'London': 'LHR',
    'Frankfurt': 'FRA'
}



# for flight in flight_numbers:
#     types = random.choice(['A320','A380','B777','B747'])
#     c.execute('insert into airplanes(flight_no,aircraft_type,capacity,economy,business,first_class)values(?,?,?,?,?,?)',(flight,types,"None","None","None","None"))
#     conn.commit()
# c.execute("UPDATE airplanes SET capacity = CASE WHEN aircraft_type = 'A320' THEN 180 WHEN aircraft_type = 'A380' THEN 540 WHEN aircraft_type = 'B777' THEN 350 WHEN aircraft_type = 'B747' THEN 420  END");
# conn.commit()
# c.execute("UPDATE airplanes SET economy = CASE WHEN aircraft_type = 'A320' THEN 150 WHEN aircraft_type = 'A380' THEN 400 WHEN aircraft_type = 'B777' THEN 300 WHEN aircraft_type = 'B747' THEN 330  END");
# conn.commit()
# c.execute("UPDATE airplanes SET business = CASE WHEN aircraft_type = 'A320' THEN 30 WHEN aircraft_type = 'A380' THEN 100 WHEN aircraft_type = 'B777' THEN 40 WHEN aircraft_type = 'B747' THEN 70  END");
# conn.commit()
# c.execute("UPDATE airplanes SET first_class = CASE WHEN aircraft_type = 'A320' THEN 0 WHEN aircraft_type = 'A380' THEN 40 WHEN aircraft_type = 'B777' THEN 10 WHEN aircraft_type = 'B747' THEN 20  END");
# conn.commit()
# n = 35
# from_ = "Frankfurt"
# to = "Dubai"
# c.execute('insert into airplane_transits values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
#           (n, "07-05-2018", from_,  to, cities[from_], cities[to], '6h 10m', '16:15', '22:25', 'KL301'))
# conn.commit()
# n = 12
# traveller = ["johar.sourav97@gmail.com","preethamtk@gmail.com","palsmadhu@yahoo.com","mukitigerchase@gmail.com "]
# c.execute('insert into travel values(?,?,?,?)',(n,"None",False,traveller[3]))
# conn.commit()
alpha = list(string.ascii_uppercase)
num = [1,2,3,4,5,6,7,8,9,0]

f = Faker()
def make_name(pax_no):
    pas = []
    for i in range(pax_no):
        name = f.name()
        pas.append(name)
    return ",".join(pas)
transitid = [id for id in range(1,36)]
travelid = [id for id in range(1,13)]


for trav in travelid:
    tran = random.choice(transitid)
    letter1 = random.choice(alpha)
    letter2 = random.choice(alpha)
    letter3 = random.choice(alpha)
    num1 = random.choice(num)
    num2 = random.choice(num)
    pnr = letter1 + letter2 + letter3 + str(num1) + str(num2)
    s = [0,0,0]
    seats = random.randint(0,2)
    no_pax = random.randint(1,5)
    s[seats] = no_pax
    c.execute('insert into journeys values(?,?,?,?,?,?,?,?)',(trav,pnr,no_pax,make_name(no_pax),s[0],s[1],s[2],tran))
    conn.commit()
