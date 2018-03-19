import sqlite3 as db

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

n = 5
from_ = "London"
to = "Frankfurt"

c.execute('insert into airplane_transits values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
          (n, "01-05-2018", from_,  to, cities[from_], cities[to], '1h 45m', '05:00', '06:45', 'KL204'))
conn.commit()
