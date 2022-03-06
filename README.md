# 2 Many Gittars

2 Many Gittars is a marketplace for guitars, amps and other items related to guitars. This web application is created using Flask and PostgreSQL-database. It is possible to test on [Heroku](https://tsoha-2manygittars.herokuapp.com). SQL-tables can be found [here](https://github.com/sampsaoinonen/tsoha-martketplace/blob/main/SQL/schema.sql)

https://tsoha-2manygittars.herokuapp.com

ADMIN - account info is in LABTOOL (3rd review reply)

## Plans at the Beginning

### Features
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

## Current state 20.2

Basic functionalities are working pretty good and layout is almost there. User profile pages, commenting and deleting ads/messages are still in progress. The project has took so much more work than I thought but I hope the biggest challenges are behind(Like search function and uploading images).

- :ballot_box_with_check: a user can create an account as either ”user” or ”admin”. Admin not possible yet.
- :ballot_box_with_check: a user can log in and log out
- :ballot_box_with_check: a user can search and view ads (with or without logging in)
- :black_square_button: a logged user has a profile where user can write description of himself/herself
- :black_square_button: a logged user can comment a profile and the owner can delete comments
- :black_square_button: a logged user can rate a profile based on how trade went
- :ballot_box_with_check: a logged user can create an ad with a picture(optional)
- :black_square_button: a logged user can comment an ad
- :ballot_box_with_check: a logged user can send a message to another registered user
- :ballot_box_with_check: a logged user can view and delete messages. Delete not possible yet.
- :black_square_button: a logged user can remove user's own ad
- :black_square_button: a logged user can view list of user's own ad history
- :black_square_button: an admin can remove any comment
- :black_square_button: an admin can remove any ad
- :black_square_button: an admin can remove any user profile

## Final version

- :white_check_mark: a user can have an account as either ”user” or ”admin”
- :white_check_mark: a user can log in and log out
- :white_check_mark: a user can search and view ads (with or without logging in)
- :white_check_mark: a logged user has a profile where user can write description of himself/herself
- :white_check_mark: a logged user can comment a profile and the owner can delete comments
- :white_check_mark: a logged user can rate a profile based on how trade went  :guitar: User can comment about the trade in sellers profile
- :white_check_mark: a logged user can create an ad with a picture(optional)
- :white_check_mark: a logged user can comment an ad
- :white_check_mark: a logged user can send a message to another registered user
- :white_check_mark: a logged user can view and send messages.
- :white_check_mark: a logged user can remove user's own ad
- :black_square_button: a logged user can view list of user's own ad history   :guitar: This never happened 
- :white_check_mark: an admin can remove any comment
- :white_check_mark: an admin can remove any ad
- :white_check_mark: an admin can remove any user profile

## Final Conlusions

The app is pretty close what was planned at first. "Ad history" was forgotten but everything else is included there. Thinking the workload now this project has way too much different functions and it took me a lot of time to accomplish. Still there are missing features like the app never deletes old ads, deleting messages not possible etc. which are needed.