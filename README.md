<pre>
A simple pythonic way of job searching through indeed advance search, on Django framework.
Help on using this app is included inside of application.

Programming languages and tools
...............................
Django 3.2.5
Python 3.8.10
PostgreSQL 12.7
jQuery v3.5.1
Bootstrap v4.5.2


Tested environment
...................
Ubuntu 20.04.2 LTS (Focal Fossa)


Notes before installation
...........................
1)
Before all, you have to have Python3 and virtualenv module installed 
on your system.

2)
If you donot have postgres database installed, you can replace 
database parameter in settings.py as following:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


Installation and launching program
..................................
In terminal run following commands:

git clone https://github.com/bm-zi/jobfinder
cd jobfinder
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

In browser, go to url 127.0.0.1:8000


</pre>