# QAnon Backend

## Usage
Before running the server, create a `.env` file in the `backend` directory with the following keys defined:
```
NEO_USER=
NEO_PASS=
NEO_URI=
```

With the corresponding values to connect to your database.


Install the python dependencies and run the server. You first need to be within the `backend` directory before running these commands:
```
$ pip3 install -r requirements.txt
$ python manage.py runserver
```

**Note:** For production, populate `SECRET_KEY` in the configuration file to include a hash stored in an environment variable.

### Repository Structure

- `api/views/` - Contains API endoints
- `api/models/` - Defines and instantiates database connection. May need to change because of the nature of creating Neo4J instance classes and their compatibility with Flask.
- `api/__init__.py` - startup script.
- `api/core.py` - contains core functionality, such as error handlers
- `config.py` - contains Configuration objects for the application.
- `manage.py` - Includes command line interface definitions.

### Learn More

- [Flask](http://flask.pocoo.org/) - Flask Documentation
- [Flask Tutorial](http://flask.pocoo.org/docs/1.0/tutorial/)
