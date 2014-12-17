# To Use:
# 1. Install IPython
# 2. $ python manage.py shell
# 3. %run -i example_data.py

import random
from datetime import datetime, timedelta

from expo_track.item.constants import *
from expo_track.person.constants import *

# Administrator account
admin_person = models.Person(given_name='Admin')
admin_user = models.User(name='admin',
                         password='123456',
                         person=admin_person)
db.session.add(admin_user)

# Give admin all permissions
perm_names = [ p.name for p in models.Permission.query.all() ]
for pname in perm_names:
    admin_user.grant_permission(pname)

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
    # Will update status to something different possibility in action loop
    radio = models.Item(name=name, description=desc, status=0, tracking_number=barcode)
    items.append(radio)
    db.session.add(radio)

# Ranom people and names from:
# http://www.generatedata.com/
example_people = [
    {"name": "Sierra Cotton", "address": "5095 Vitae, St.", "city": "Fort Smith", "region": "AR", "postal_code": "72748", "phone_number": "(190) 891-9585", "email_address": "vitae.diam.Proin@ligula.org"},
    {"name": "Cheryl Bridges", "address": "P.O. Box 829, 2967 Ornare, Av.", "city": "Pocatello", "region": "ID", "postal_code": "80965", "phone_number": "(485) 639-4755", "email_address": "fringilla@In.edu"},
    {"name": "Hedda Drake", "address": "629 Et Ave", "city": "San Jose", "region": "CA", "postal_code": "96261", "phone_number": "(672) 832-8491", "email_address": "arcu.Vivamus.sit@loremluctus.co.uk"},
    {"name": "Daryl Lowe", "address": "P.O. Box 420, 9630 Urna, St.", "city": "Los Angeles", "region": "CA", "postal_code": "95611", "phone_number": "(651) 203-8908", "email_address": "aliquam.iaculis.lacus@egetmetus.org"},
    {"name": "Mia Combs", "address": "7596 Felis Road", "city": "Gaithersburg", "region": "MD", "postal_code": "49013", "phone_number": "(279) 108-7747", "email_address": "pede.ac.urna@arcuvelquam.co.uk"},
    {"name": "Kaitlin Browning", "address": "Ap #442-285 Nec Avenue", "city": "Springfield", "region": "MA", "postal_code": "54992", "phone_number": "(614) 131-1260", "email_address": "consequat@DonecestNunc.co.uk"},
    {"name": "Prescott Cooper", "address": "270-1590 Scelerisque, Av.", "city": "Dallas", "region": "TX", "postal_code": "64049", "phone_number": "(116) 207-1989", "email_address": "eu.lacus@Phasellus.org"},
    {"name": "Gillian Holt", "address": "2959 Eu Rd.", "city": "Covington", "region": "KY", "postal_code": "26233", "phone_number": "(493) 935-8852", "email_address": "lacinia.mattis@euultrices.ca"},
    {"name": "Isabelle Hobbs", "address": "2627 Enim, Rd.", "city": "Mesa", "region": "AZ", "postal_code": "85522", "phone_number": "(788) 844-0529", "email_address": "nunc.interdum.feugiat@mauris.edu"},
    {"name": "Aretha Brooks", "address": "191-6357 Suspendisse Rd.", "city": "Pittsburgh", "region": "PA", "postal_code": "73468", "phone_number": "(130) 140-6835", "email_address": "vel@et.ca"},
    {"name": "Graham Rhodes", "address": "970-2462 Lacus. Street", "city": "Philadelphia", "region": "PA", "postal_code": "80247", "phone_number": "(820) 427-7363", "email_address": "a.neque@molestie.com"},
    {"name": "Olga Wilder", "address": "P.O. Box 573, 9567 Arcu. Street", "city": "Madison", "region": "WI", "postal_code": "62744", "phone_number": "(554) 530-1619", "email_address": "Nullam.scelerisque.neque@augue.net"},
    {"name": "Mechelle Steele", "address": "698-4684 Aenean Av.", "city": "Fairbanks", "region": "AK", "postal_code": "99607", "phone_number": "(696) 407-3830", "email_address": "quis@nibh.co.uk"},
    {"name": "Erin Cameron", "address": "P.O. Box 310, 4354 Dictum Av.", "city": "Frederick", "region": "MD", "postal_code": "65636", "phone_number": "(384) 797-3378", "email_address": "at.fringilla.purus@Curabiturvel.edu"},
    {"name": "Duncan Reyes", "address": "634-8651 Non Street", "city": "Seattle", "region": "WA", "postal_code": "39076", "phone_number": "(554) 370-5671", "email_address": "Cras@ac.co.uk"},
    {"name": "Harrison Lane", "address": "P.O. Box 202, 2905 Diam St.", "city": "Joliet", "region": "IL", "postal_code": "66365", "phone_number": "(648) 433-1267", "email_address": "bibendum@lobortisrisus.edu"},
    {"name": "Shelly Sawyer", "address": "4468 Vulputate Road", "city": "Bridgeport", "region": "CT", "postal_code": "51585", "phone_number": "(934) 497-7874", "email_address": "tincidunt.neque.vitae@Morbiquisurna.edu"},
    {"name": "Pandora Goff", "address": "Ap #126-857 Tempor Rd.", "city": "Jefferson City", "region": "MO", "postal_code": "17416", "phone_number": "(988) 985-4171", "email_address": "Sed@Aeneanmassa.com"},
    {"name": "Debra Kelley", "address": "P.O. Box 839, 9887 Semper Ave", "city": "Sterling Heights", "region": "MI", "postal_code": "85096", "phone_number": "(342) 222-6330", "email_address": "mus.Proin@ullamcorperDuis.edu"},
    {"name": "Burke Hughes", "address": "P.O. Box 276, 5764 Donec Street", "city": "Jackson", "region": "MS", "postal_code": "43882", "phone_number": "(547) 335-1842", "email_address": "molestie.Sed.id@nequeNullam.ca"},
]

people_per_team = len(example_people) / len(teams_dict.keys())
people = []
for team in teams_dict.values():
    for count in range(people_per_team):
        curr_person = example_people.pop()

        given, family = curr_person['name'].split()
        person = models.Person(given_name=given, family_name=family)

        contact_type = random.randrange(len(CONTACT_TYPES))
        curr_address = "%s\n%s, %s %s" % ('\n'.join(curr_person['address'].split(', ')), 
                curr_person['city'], curr_person['region'], curr_person['postal_code'])
        contact = models.Contact(type=contact_type, 
                address=curr_address, phone_number=curr_person['phone_number'], 
                email_address=curr_person['email_address'])
        person.contacts.append(contact)

        people.append(person)
        db.session.add(person)

num_actions = 100
time_beg = datetime.now()-timedelta(hours=num_actions+1)

# Add some random actions
for count in range(num_actions):
    which_item = random.randrange(len(items))
    status_type = random.randrange(len(STATUS_TYPES.keys()))
    which_person = random.randrange(len(people))
    dt = time_beg + timedelta(hours=count) + timedelta(minutes=random.randrange(59))
    action = models.Action(item=items[which_item], status=status_type, person=people[which_person], event=linux_expo, date=dt)
    # Set current status to latest status item
    items[which_item].status = status_type
    db.session.add(action)

db.session.commit()
