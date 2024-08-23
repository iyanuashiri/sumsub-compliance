# sumsub-compliance

This project has three basic apps.

* Accounts - User authentication.
  - Registration
  - Login and Logout
* Compliances
  - Create an Applicant
  - Add ID Document
  - Get verification status
  

# Technology Stack

  * Python 3.12x
  * Django Web Framework 5.0x and Django REST Framework
  * SQLite
 
### Installation

Clone the repo
```python
$ git clone https://github.com/iyanuashiri/sumsub-compliance.git

$ cd sumsub-compliance
```

Run migrations
```python
$ python manage.py makemigrations

$ python manage.py migrate
```

Run server
```python
$ python manage.py runserver
```
Application URL
http://localhost:8000/

API Documentation link
http://localhost:8000/swagger/

Available Endpoints

POST http://localhost:8000/auth/users/ - Signup endpoint

POST http://localhost:8000/auth/token/login - Login endpoint

POST http://localhost:8000/auth/token/logout - Logout endpoint

POST http://localhost:8000/documents - Add ID Document

POST http://localhost:8000/applicants/ - Create an applicant

GET http://localhost:8000/verification-status/ - Get verification status

