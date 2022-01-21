# Comparte Ride
API developed with python, django and django-rest-framework, making use of good programming practices and relying on docker technology.

# Idea
An API is developed with the ability to manage a car ride sharing platform.

# Functionalities
Create a user, send verification email, verify a user, login and logout, create a circle of friends, memberships, manage a ride, rate a ride and other functionalities necessary to complement the application

# How to run it?
In order to run the project we only need to have docker and docker-compose installed on our computer.
Once we have them installed, we proceed to place the next comands in the terminal

**docker-compose -f local.yml build**

**docker-compose -f local.yml up**

As soon as this is done we can access the API at localhost: 8000

# Queries

All available queries are found in the file ComparteRide.postman_collection.json which we must import from postman