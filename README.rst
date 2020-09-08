** Flask Application Tutorial **

A simple Flask project from youtube channel 'Traversy Media'.

I am following the youtube tutorial 'Python Flask From Scratch' from 'Traversy Media'

( https://www.youtube.com/playlist?list=PLillGF-RfqbbbPz6GSEM9hLQObuQjNoj_ )

* The Application is build with Python and Flask and  contains 3 pages: home, about, articles.
* It supports a register page, a login page and is using python's sqlite3 as database (the tutorial implements SQL database).
* Every action that includes register, login and logout is supported by integrated flash messages.

                    ** OTHER CHANGES FROM THE ORIGINAL TUTORIAL **

## GENERAL 

1. implements SQLITE3 as data base.
2. better delimitation of resources.

/home/user/Projects/FLASK_APPLICATION_TUTORIAL/
|--- flask_application_tutorial/
|    |--- __init__.py
|    |--- db.py
|    |--- schema.sql
|    |--- home.py
|    |--- about.py
|    |--- articles.py
|    |--- my_dashboard.py
|    |--- auth.py
|    |--- forms.py
|    |--- /templates/
|         |--- includes/
|         |    |--- _formhelpers.html
|         |    |--- _messages.html
|         |    |--- _navbar.html
|         |
|         |--- articles/
|         |    |--- article.html
|         |    |--- articles.html
|         |--- auth/
|         |    |--- register.html
|         |    |--- login.html
|         |
|         |--- my_dashboard/
|         |    |--- dashboard.html
|         |    |--- add_article.html
|         |    |--- edit_article.html
|         |
|         |--- layout.html
|         |--- home.html
|         |--- about.html
|
|---- instance/
|     |--- flask_application_tutorial.userdata
|     |--- config.py
|      
|---- .flaskenv
|---- wsgi.py
|---- .gitignore
|---- licence.txt
|---- poetry.lock
|---- pyproject.toml
|---- README.rst

_______________________________________________________________________________

## ARTICLES

1. a head table similar with the one in dashboard.
2. a button to view articles.
3. a return button to prevous view, if user logged in the view will
   return to dashboard.

_______________________________________________________________________________

## DASHBOARD

1. a button to view articles.
2. a return button to prevous view.