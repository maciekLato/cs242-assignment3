*Regarding sql injections in flask
From stackoverflow: http://stackoverflow.com/questions/6501583/sqlalchemy-sql-injection
If you have any "special" characters (such as semicolons or apostrophes) in your data, they will be automatically quoted for you by the SQLEngine object, so you don't have to worry about quoting. This also means that unless you deliberately bypass SQLAlchemy's quoting mechanisms, SQL-injection attacks are basically impossible.

*Regarding XSS
From the flask documentation: http://flask.pocoo.org/docs/security/
Flask configures Jinja2 to automatically escape all values unless explicitly told otherwise. This should rule out all XSS problems caused in templates.
I made sure to properly protect my attribute tags to prevent any vulnerabilities with Jinja templating.

Regarding the DB schema:
see apps.models.py