# Status types
STATUS_CHECK_IN = 0
STATUS_CHECK_OUT = 1
STATUS_MISSING = 2
STATUS_FOUND = 3

STATUS_TYPES = {
        STATUS_CHECK_IN:  'Checked In',
        STATUS_CHECK_OUT: 'Checked Out',
        STATUS_MISSING:   'Missing',
        STATUS_FOUND:     'Found' 
}

# The reverse action of each status code
STATUS_OPPOSITES = { 
        STATUS_CHECK_IN: STATUS_CHECK_OUT,
        STATUS_CHECK_OUT: STATUS_CHECK_IN,
        STATUS_MISSING: STATUS_FOUND,
        STATUS_FOUND: STATUS_MISSING,
}
