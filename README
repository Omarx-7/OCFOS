One-day build for the OCF Full-Stack Engineer task: member profiles, city/domain
events with RSVPs, event-based member matching, and an admin-moderated
introduction workflow.

Stack: Flask + Flask-SQLAlchemy + MySQL

Setup


Create a MySQL database, then create a .env file in the project root:

   DB_USERNAME=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_NAME=ocf_platform
   SECRET_KEY=any_random_string


Install dependencies:


   pip install -r requirements.txt


Create the tables — either run schema.sql against your database, or:


python   from Website import ocfapp, db
   app = ocfapp()
   with app.app_context():
       db.create_all()


Seed test data:


   python Website/seed.py


Run the app:

   python ocfapp.py

Visit http://127.0.0.1:5000.

Demo path

Home → choose Member or Admin → browse events → RSVP → view connection
recommendations → request an introduction → Admin approves it.


Project structure

ocfapp.py          entrypoint
Website/
  __init__.py       app factory
  config.py         DB config, loaded from .env
  models.py         Member, Project, Event, RSVP, Introduction
  views.py          all routes
  seed.py           standalone script that populates test data
  templates/        Jinja templates
test_app.py         pytest suite
