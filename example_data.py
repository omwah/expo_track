# To Use:
# 1. Install IPython
# 2. $ python manage.py shell
# 3. %run -i example_data.py

# Administrator account
admin_person = models.Person(given_name='Admin')
admin_user = models.User(name='admin',
                         password='123456',
                         person=admin_person,
                         can_edit_items = True,
                         can_perform_action = True,
                         can_edit_people = True,
                         can_edit_events = True,
                         can_edit_locations = True,
                         can_edit_teams = True)
db.session.add(admin_user)

linux_expo = models.Event(name="Southern California Linux Expo",
                          description="SCALE's mission is to provide educational opportunities on the topic of Open Source software. Open Source software is any software that meets the litmus test of the OSI (Open Source Initiative)")
db.session.add(linux_expo)

room_names = [ "La Jolla",
               "Carmel",
               "Los Angeles A",
               "Los Angeles B",
               "Los Angeles C",
               "Century AB",
               "Century CD",
               "Marina",
               "Bel Air",
               "Plaza A",
               "Newport A",
               "Catalina A",
               "Catalina B",
               "Catalina C",
               "Catalina D",
               "Santa Monica A",
               "Santa Monica B",
               "San Lorenzo A",
               "San Lorenzo B",
               "San Lorenzo C",
               "San Lorenzo D",
               "San Lorenzo E",
               "San Lorenzo F",
               "Lobby" ]
     
rooms_dict = {}
for room_name in room_names:
    room = models.Location(name=room_name, event=linux_expo)
    rooms_dict[room_name] = room
    db.session.add(room)

teams = { "Audio Visual": "Catalina B",
          "Network Operations": "Catalina A",
          "Registration": "Lobby",
          "Tech": None }

teams_dict = {}
for team_name, room_name in teams.items():
    room = None
    if room_name != None:
        room = rooms_dict[room_name]
    team = models.Team(name=team_name, primary_location=room)
    teams_dict[team_name] = team
    db.session.add(team)

items = []
for radio_num in range(1, 61):
    barcode = 1000 + radio_num
    name = "Radio #%02.d" % radio_num
    desc = "Etekcity Radio"
    radio = models.Item(name=name, description=desc, tracking_number=barcode)
    items.append(radio)
    db.session.add(radio)

# Random people from 
# http://listofrandomnames.com/
random_names = [ "Kenton Blackwood",
                 "Delphine Dilbeck",
                 "Kellye Mello",
                 "Jayson Gaylor",
                 "Brooks Rone",
                 "Rubi Brumit",
                 "Ila Arvidson",
                 "Carita Sillman",
                 "Elida Winget",
                 "John Hartford",
                 "Rosa Carrier",
                 "Chanel Mcivor",
                 "Cassidy Garbarino",
                 "Lorrie Mcnamee",
                 "Euna Schutt",
                 "Regan Hocking",
                 "January Escareno",
                 "Carola Schenck",
                 "Lyndsay Mackowiak",
                 "Reyes Luedke",]

people_per_team = len(random_names) / len(teams_dict.keys())
people = []
for team in teams_dict.values():
    for count in range(people_per_team):
        curr_name = random_names.pop()
        given, family = curr_name.split()
        person = models.Person(given_name=given, family_name=family)
        people.append(person)
        db.session.add(person)

# Add some random actions
import random
from expo_track.item.constants import *
for count in range(100):
    which_item = random.randrange(len(items))
    action_type = random.randrange(len(ACTION_TYPES.keys()))
    which_person = random.randrange(len(people))
    action = models.Action(item=items[which_item], type=action_type, person=people[which_person], event=linux_expo)
    db.session.add(action)

db.session.commit()