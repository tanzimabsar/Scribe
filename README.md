# Scribe

Simple CRUD Application designed to help with digital asset license management.

This application allows users to store licenses of digital assets they own. It is meant to be used for situations where an individual owns the rights to a given asset and wants to maintain the licensees and when those licenses expire. As of now, the application takes record of entities such as an audio file and meta data associated with that.

The technical specification for this application is all outlined in the link below:

[Design Specification Documenation](https://1drv.ms/w/s!AhBJjeUDAfyAkRmQc9UC6ORDGx1_?e=HIxYsI)

# Tests

Tests are located within the test_client.py file where any new additions to the core business logic (ammended to service.py) are to be tested with the rest of the application. For testing purposes, a new SQLITE database is created and torn down after the tests have been completed. 

Credentials for the development version of this application are stored in a config.ini with the following paramaters:

```
[dev]
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
PG_USER=
PG_PASSWORD=
```
