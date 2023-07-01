from app import db
from app.models import Role, User

roles = ['admin','manager','staff']

for r in roles:
    query = Role(name=r)
    db.session.add(query)
    db.session.commit()
    
u = User(username='luthfipratamaps', email='luthfipratamaps@gmail.com', role_id=1)
u.set_password('justatest')
db.session.add(u)
db.session.commit()