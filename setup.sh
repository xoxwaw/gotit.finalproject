#!/usr/bin/env bash
virtualenv venv --python=/usr/local/bin/python3.7
source venv/bin/activate
pip install -r requirements.txt
mysql.server restart

# specify these fields
db_name="YOUR MAIN DATABASE NAME"
db_test="YOUR TEST DATABASE NAME"
db_user="YOUR MYSQL USERNAME"
db_password="YOUR MYSQL PASSWORD"
jwt_secret="YOUR JWT SECRET KEY"

# create db
mysql -u root -e "CREATE DATABASE IF NOT EXISTS $db_name;"
mysql -u root -e "CREATE DATABASE IF NOT EXISTS $db_test;"
mysql -u root -e "CREATE USER IF NOT EXISTS '$db_user'@'localhost';";
mysql -u root -e "ALTER USER '$db_user'@'localhost' IDENTIFIED BY '$db_password';"
mysql -u root -e "GRANT ALL PRIVILEGES ON $db_name.* To '$db_user'@'localhost';"
mysql -u root -e "GRANT ALL PRIVILEGES ON $db_test.* To '$db_user'@'localhost';"

# append to env
echo "DB_NAME=$db_name" >> ./main/config/.env
echo "DB_TEST=$db_test" >> ./main/config/.env
echo "DB_USER=$db_user" >> ./main/config/.env
echo "DB_PASSWORD=$db_password" >> ./main/config/.env
echo "JWT_SECRET_KEY=$jwt_secret" >> ./main/config/.env

echo "main/config/.env" >> ./.gitignore

