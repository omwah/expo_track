# Import all models from blueprints directories into one name space
from .user.models import User, Permission
from .event.models import Event, Location, Team
from .item.models import Item, Action
from .person.models import Person, Address, Phone, Email
