from app import db
from models import users
from models import friendships
from models import bestFriends

#creating the database
db.create_all()

#insert some users
db.session.add(users("Alex", "alex@alex.com", "900102030", "passwordAlex"))
db.session.add(users("Carlos", "carlos@carlos.com", "900102030", "passwordCarlos"))
db.session.add(users("Pedro", "pedro@pedro.com", "900102030", "passwordPedro"))
db.session.add(users("Jorge", "jorge@jorge.com", "900102030", "passwordJorge"))
db.session.add(users("Juan", "juan@juan.com", "900102030", "passwordJuan"))
db.session.add(users("Julia", "julia@julia.com", "900102030", "passwordJulia"))
db.session.add(users("Ana", "ana@ana.com", "900102030", "passwordAna"))




#insert some friendships
db.session.add(friendships(3, 4, "Pedro", "Jorge"))
db.session.add(friendships(1, 2, "Alex", "Carlos"))
db.session.add(friendships(3, 6, "Pedro", "Julia"))
db.session.add(friendships(1, 5, "Alex", "Juan"))
db.session.add(friendships(1, 6, "Alex", "Julia"))
db.session.add(friendships(5, 6, "Juan", "Julia"))



#insert some bestFriends
db.session.add(bestFriends(1, 6, "Alex", "Julia"))



#commit changes
db.session.commit()