# INTRODUCTION

There is 2 type application in this repository. Console and Web application please select one of that to test crawler.

## SETUP for Console Application 
This part much easier to test application instead of WEB Application

    	Clone:
    git clone https://github.com/vergili/LinkedinTest linkedin 
    
    cd linkedin/console
    virtualenv env 
    source env/bin/activate 
    pip install -U pip 
    pip install -U distribute 
    pip install -r requirements.txt

Please change your database connection in linkedin.py

    python linkedin.py


####Screen from running for microsoft 
![alt tag](https://github.com/vergili/LinkedinTest/tree/master/console/print_screen.png)


## SETUP for WEB Application 

    	Clone:
    git clone https://github.com/vergili/LinkedinTest linkedin 
    
    cd linkedin
    virtualenv env 
    source env/bin/activate 
    pip install -U pip 
    pip install -U distribute 
    pip install -r requirements.txt
    
    
  
### Create database and your admin account:

Change SQLALCHEMY_DATABASE_URI for your database connection  in loctube/config.py

    python manage.py initdb
 
### Start: 
    
	python manage.py run

Open: http://localhost:5000/admin/linkedin

user: admin
pass: 123456


NOTE:  Please write company name as linkedin public company url 
       
example:  http://www.linkedin.com/company/linkedin
here company name is linkedin

Then crawler will find public company name and will find first 10 emplooyes. 
After that it will find other company employees with first 10 member public url....
Since some compmany like linkedin has a lot of employees crawling will take long time. 


