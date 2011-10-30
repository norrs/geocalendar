#GeoCalendar

A simple calendar system to create events on for a local geocaching group in Trondheim, Norway.

How it's supposed to work:

Create events with a title, description and a secret picture you upload who should be unlocked by the secret keyword (passphrase) that you will be able to find in geocaches in Trondheim, Norway.

When you have gathered all the secret pictures, you should get a bigger picture (like a puzzle) :-)
(btw: you have to edit the pictures yourself and let them look as a puzzle-brick or how you type it)

# Install

* Install virtualenv (on debian/ubuntu: apt-get install python-virtualenv ) 
* virtualenv --no-site-packages /path/to/store/your/virtualenv/geocalendar
* source /path/to/virtualenv/geocalendar/bin/activate

* Use this one liner
* * pip install Django south django-uni-form Markdown PIL django-filebrowser-no-grappelli 

## Initialize database first time

* python manage.py syncdb  
** comment: this create the basic django db + your super user
* python manage.py migrate
** comment: installs the geocal-app sql

## Update translation strings:

Havent added translation yet, this is on the todo

* Add or change translatable strings in template or python code
* python manage.py makemessage -l nb_NO to generate keys in norwegian language file
* Edit locale/nb_NO/LC_MESSAGES/django.po and add your translations
* python manage.py compilemessages

Your new translations are now ready to use :)


