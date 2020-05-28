# Flask Item-Category APIs
Final project training for Got It Internship, 2020

## Description

This application is the final project for the training course. It is a 
Web API Server that provides a number of APIs to interact with items 
and categories in storage, along with authentications for those APIs.

## Installation 
`git clone` this repository.

You should have a MySQL Database running in your machine. This project runs on MySQL 8.0.18.
For MacOS, after you have [Homebrew](https://brew.sh/) installed, run following commands: 

### MYSQL setup
`brew install mysql@8.0.18`

`brew tap homebrew/services `

And start the mysql server by running 

`mysql.server start`

Login to MySQL CLI

`mysql -u root`

Inside the mysql cli, you now should create 2 databases. The one for testing can be referenced in Testing Section.


`CREATE DATABASE IF NOT EXISTS final_project;`

**Optionally**, you can create a separate user for this application. 

`CREATE USER IF NOT EXISTS 'final_project_user'@'localhost';`

`ALTER USER 'final_project_user'@'localhost' IDENTIFIED BY 'example_password';`

`GRANT ALL PRIVILEGES ON final_project.* To 'final_project_user'@'localhost';`

Or you can just use the root user with or without password.
To set your root password:

`mysqladmin -u root password 'yourpassword'`

### Application Environment Setup

You should create an `.env` file inside a folder with the environment name for each environment setup inside `envs` folder.
For example, an `.env` for a `dev` environment should be placed as `envs/dev/.env`.

 A `.env` file example can be referred by `.env.example`. Inside the environment config file `.env`,
you can specify the environment. Change the user and password for the 
database if you happen to change those in the steps above.

### Virtual environment

This project use Python version 3.7.7. You should have `virtualenv` on your machine.
Or install if you have not:

`pip3 install virtualenv`

Then create a new virtual environment

`virtualenv venv --python=/usr/local/bin/python3.7`

Then activate the virtual environment

`source venv/bin/activate`

`pip install -r requirements.txt`

You have now successfully configured the necessary environment for 
the app to run.

## Start the server

You can easily start the server by running the script `run_server.sh`

`bash run_server.sh`

## Available APIs
By default, to test on local machine, the server runs on port 8000. You can 
test these APIs on Postman.

- `POST /register`: register new user, request body contains `username` and `password`
- `POST /auth`: get access_token for user, request body contains `username` and `password`. 
**Currently, access_token is reset every hour, so to get authorization for 
unsafe APIs, you should call this API every hour or so to get the new token.**
- `PUT /password`: change a user's password, headers contains `Authorization: access_token` and `Content-Type: application/json`.
Request body contains `old_password` and `new_password`

- `GET /categories?name=&creator_id=`: get categories by filter
- `GET /categories/<id>`: get a specific category by id
- `GET /items?name=&category_id=&creator_id=`: get items by filter
- `GET /items/<id>`: get a specific item by id
- `POST /categories/`: create a new category, headers include access_token(as above)
and request body is a json contains `name`, `description`(optional)
- `POST /items/`: create a new item, headers include access_token, 
and request body is a json contains `name`, `description`(optional), and 
`category_id`(optional)
- `PUT /categories/<id>`: update/modify a category, headers include access_token,
and request body is a json contains `name`, `description`(optional)
- `PUT /items/<id>`: update/modify an item, headers include access_token,
and request body is a json contains `name`, `description`(optional), 
and `category_id`(optional)
- `DELETE /items/<id>`: delete an item, headers include access_token
- `DELETE /categories/<id>`: delete a category, headers include access_token

## TESTING

In order to run tests, you should create a database for testing

`CREATE DATABASE IF NOT EXISTS test_final_project;`

**Optionally**, if you have created a user for this project, you should also give permission to alter
the database for this user

`GRANT ALL PRIVILEGES ON test_final_project.* To 'final_project_user'@'localhost';`

To test the application, run `bash run_tests.sh`

You can also check the test coverage by running `coverage report -m` in the CLI.


## LICENSE

[MIT](https://github.com/xoxwaw/gotit.finalproject/blob/master/LICENSE)












