# 2 Many Gittars

2 Many Gittars is a marketplace for guitars, amps and other items related to guitars. This web application will be created using Flask and PostgreSQL-database. It will be deployed on Heroku.


## Features
- a user can create an account as either ”user” or ”admin”
- a user can log in and log out
- a user can search and view ads (with or without logging in)
- a logged user has a profile where user can write description of himself/herself
- a logged user can comment a profile and the owner can delete comments
- a logged user can rate a profile based on how trade went
- a logged user can create an ad with a picture(optional)
- a logged user can comment an ad
- a logged user can send a message to another registered user
- a logged user can view and delete messages
- a logged user can remove user's own ad
- a logged user can view list of user's own ad history
- an admin can remove any comment
- an admin can remove any ad
- an admin can remove any user profile

## Current state (6.2)

Registering, logging in and out are working. So is "add new ad" - page though is not adding anything to the database yet. The overall appearence of the webpage is coming together. 

The app is possible to test on https://tsoha-2manygittars.herokuapp.com

### Working on at the moment:

- adding ads with pictures into the database
- using and showing info from categories-table