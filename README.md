# Install LAMP  and setup latest version of Wordpress

# %Notes%
####1. This will only work on Ubuntu systems.
####2. Tested on Ubuntu 18.04 and 19.04

# How to run this
```
sudo python3 lamp_ubuntu.py
``
##-------------Script Execution Flow--------------
#####Script will  ask you to  enter your dbname:
   -  if you press Return without entering any name a database with "wp_db" will be created.
   - Otherwise a database will be created with a name whatever you will enter.

#####Script will ask you to enter your username and password:
  -  if you press Return without entering any name a default  user `debian-sys-maint` and its default password will be used
  -  Otherwise a username will be created with a password whatever you will enter


##### Script will  ask you to  enter your Title:
   -  if you press Return without entering any name a default  Title "Example"
   - Otherwise a Title will be created  whatever you will enter


#####Script will  ask you to  enter your Admin user:
   -  if you press Return without entering any name a default  admin user "root"
   - Otherwise a Admin user will be created  whatever you will enter


#####Script will  ask you to  enter your Admin_password:
  -  if you press Return without entering any name a default  Admin_password "1234"
  - Otherwise a Admin_password will be created  whatever you will enter

#####Script will  ask you to  enter your Email:
  -  if you press Return without entering any name a default Email "info@example.com"
  - Otherwise a Email will be created  whatever you will enter
