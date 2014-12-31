# Status types
STATUS_CHECK_IN = 0
STATUS_CHECK_OUT = 1
STATUS_MISSING = 2

STATUS_TYPES = {
    STATUS_CHECK_IN:  'Checked In',
    STATUS_CHECK_OUT: 'Checked Out',
    STATUS_MISSING:   'Missing',
}

# Names for actions to perform to get something into a certains tatus
STATUS_COMMAND_NAMES = {
    STATUS_CHECK_IN:  'Check In',
    STATUS_CHECK_OUT: 'Check Out',
    STATUS_MISSING:   'Mark Missing',
}

# The state of items to allow when selecting to change an items state
STATUS_OPPOSITES = { 
    STATUS_CHECK_IN: (STATUS_CHECK_OUT, STATUS_MISSING),
    STATUS_CHECK_OUT: STATUS_CHECK_IN,
    STATUS_MISSING: (STATUS_CHECK_IN, STATUS_CHECK_OUT),
}

NULL_ACTION_PERSON_NAME = 'Removed Person'
