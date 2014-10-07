# INTRODUCTION



## SETUP 

	Clone:
    git clone https://github.com/vergili/loctube loctube
    
    $ virtualenv env 
    $ source env/bin/activate 
    $ pip install -U pip 
    $ pip install -U distribute 
    $ pip install -r requirements.txt
    
    
  
### Create database and your admin account:

Change SQLALCHEMY_DATABASE_URI for your database connection  in loctube/config.py

    python manage.py initdb
 
### Start: 
    
	python manage.py run

Open:http://127.0.0.1:5000  

