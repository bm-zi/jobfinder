<pre>

About jobfinder
...............
This app is a nify and simple web-based tool to customize the job 
searching, built on Django framework and uses the indeed advanced job 
search engine.

No API programming or Django REST framework used in this application. 
This application uses Python mechanize module to automate submitting 
forms for advance search on indeed website and then the web scraping
Python modules help to process response pages and get a reusable text 
format from job search ressults. 
The job search information are stored in the database and then Django 
server provides a CRUD web-based application with a user-friendly 
interface.


Help
....
Help on using this app is included inside of application. 
After having application installed access to help menu is provided.

Programming Languages and Database
..................................
Django 3.2.5
Python 3.8.10
PostgreSQL 12.7
jQuery v3.5.1
Bootstrap v4.5.2


Tested Environment
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
