# Online Judge

This project is an online judging system for automating the code testing in competitions. It supports code submissions in C, C++, Java and Python. This judge compiles and executes the submitted code to check for correctness based on pre-constructed testcases. Competition organizers can also configure memory and time restrictions as hard limits for the code thus ensuring fairness for participants. It also features a web based dashboard for ease of management of the competition.


## Installation 

#### 1. Create virtualenv

```sh
$ sudo pip3 install virtualenv
$ virtualenv -p python3 newenv
$ source newenv/bin/activate
$ cd newenv
```

#### 2. Clone project
```sh
$ git clone https://github.com/RushabhK/Online-Judge.git
$ cd Online-Judge
```

#### 3. Install Django requirements
```
$ pip install -r requirements.txt
```

#### 4. Install MySql
```
$ sudo apt-get update
$ sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev
$ sudo mysql_install_db
$ sudo mysql_secure_installation
```

#### 5. Create Database and user
```
$ mysql -u root -p
> CREATE DATABASE judge_database;	
> CREATE USER judge_user@localhost IDENTIFIED BY 'password';
> use judge_database;
> GRANT ALL PRIVILEGES ON judge_database TO judge_user@'localhost';
> FLUSH PRIVILEGES;
> exit
```

#### 6. Install mysqlclient package for django
```
$ pip install django mysqlclient
```

#### 7. Create models, generate & run migration files by:
```
$ python manage.py makemigrations
$ python manage.py migrate
```

#### 8. Create admin to create questions adn setup the test:
```
$ python manage.py createsuperuser
$ python manage.py runserver
```
##### Go to URL/admin, login and add questions


#### 9. Install Docker
i. Download .deb file of docker(For Ubuntu)
ii. Install command:
```
sudo dpkg -i /path_to_deb_file
```

#### 10. Enable docker container to run without sudo
```
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
```
Logout and again login to apply changes

#### 11. Build Docker Image
```
$ cd Judge
$ docker build -t judge_image .
```

#### 12. Setup Contest
i. Set test time settings in Backend/settings.py (DURATION and START_TIME)
ii. Set memory limit in Judge/scripts/constants.py (MEMORY_LIMIT)

#### 13. Start Server
```
$ python manage.py runserver
```