"# urbarn-inventory" 

Sistem Inventori dengan fitur mengikuti studi kasus test case

Menggunakan Flask, Python3.7
=======================================
[Features]
Owner/admin - CRUD - User, Product, Category, Location,
            - DW - Balance, Transfer, User, Product, Category,
                   Location, Role
Manager - CRUD - Product, Category, Location
        - CRU  - User
        - DW - Balance, Transfer, User, Product, Category,
               Location, Role
Staff   - CRUD - Product, Category, Location

Owner mengatur permission user berdasarkan role
Fitur tertentu hanya bisa diakses role tertentu
Download laporan dalam bentuk csv
=======================================
[Admin (origin)]
username luthfipratamaps
password justatest

[Email system]
insert email address and password at .flaskenv file
to use email feature
email account less secure app must be toggled on
=======================================
Open terminal prompt

note: Copy and Enter to terminal

[1] installation and preparation
cd inventory
python3 -m venv venv &&
source venv/bin/activate &&
pip3 install -r requirements.txt &&
flask db init &&
flask db migrate &&
flask db upgrade &&
flask shell 

[2] initial data
from app import db
from app.models import Role, User, Location

roles = ['admin','manager','staff']

for r in roles:
    query = Role(name=r)
    db.session.add(query)
    db.session.commit()



u = User(username='luthfipratamaps', email='luthfipratamaps@gmail.com', role_id=1)
u.set_password('justatest')
db.session.add(u)
db.session.commit()

l = Location(name='Main Warehouse')
db.session.add(l)
db.session.commit()

[3] exit flask shell
Press 'ctrl + d' to exit flask shell

[4] run the app
flask run