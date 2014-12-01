==========
Expo Track
==========

A web application of tracking the usage of physical items during conferences and expo by support staff.

Setup
-----

Create a Python virtual environment::

    $ virtualenv env/

Load environment::

    $ source env/bin/activate

Install requirements::

    $ pip install -r requirements.txt

Ensure development server works::

    $ python manage.py runserver

Installation
------------

Install nginx::

    $ apt-get install nginx uwsgi uwsgi-plugin-python

Install server configs::

    rm /etc/nginx/sites-enabled/default
    cp server/nginx_site /etc/nginx/sites-enabled/expo_track
    cp server/uwsgi.ini /etc/uwsgi/apps-enabled/expo_track.ini

Restart nginx and uwsgi.
