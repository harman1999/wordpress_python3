#!/bin/python3

import socket, os, sys, shutil ,subprocess ,mysql.connector ,fileinput ,getpass 

subprocess.call('yum -y update', shell=True)

#### Install packages ####
subprocess.call('yum install -y httpd httpd-tools mod_http2 bluez-obexd php mod_dnssd nginx-filesystem nginx php-fpm php-common mysql php-pecl-json mariadb mariadb-server mariadb-backup mariadb-common mariadb-cracklib-password-check mariadb-errmsg mariadb-gssapi-server mariadb-server-utils perl-DBD-MySQL php-pear gcc php-mysqlnd MySQL-python postfix', shell=True)
#### Install packages through pip ####
subprocess.call('pip install python3-wget ', shell=True)
# Create postfix dir
subprocess.call('mkfifo /var/spool/postfix/public/pickup', shell=True)
#### Start applications ####
subprocess.call('systemctl start httpd', shell=True)
subprocess.call('systemctl start mariadb.service', shell=True)
subprocess.call('systemctl start postfix', shell=True)
#### enable all application ####
subprocess.call('systemctl enable httpd', shell=True)
subprocess.call('systemctl enable mariadb.service', shell=True)
subprocess.call('systemctl enable postfix', shell=True)

while True:
    doc_root = input("Please enter your doc root /var/www/html/:")
    default_doc_root = "/var/www/html/"
    if doc_root == "":
        doc_root = default_doc_root
        print(default_doc_root)
    else:
        os.makedirs(default_doc_root+doc_root, exist_ok=True)
        default_doc_root += doc_root
        print("your doc root is "+default_doc_root)
##### Install wordpress.zip ####
    os.system("wget https://wordpress.org/latest.zip")

#### Unzip wordpress file ####
    os.system("unzip latest.zip")

#### Copy wordpress to document root ####
    subprocess.call("cp -r   wordpress/* "+default_doc_root, shell=True)

#### Rename wp-congig.php ####
    os.system("mv "+default_doc_root+"/wp-config-sample.php  "+default_doc_root+"/wp-config.php")

##### Remove zip file ####
    shutil.rmtree('wordpress')
    os.remove('latest.zip')
    print("")
#### Database ####
    database = input("Please enter your db : ")
#### Check mysql is working ####
    if database == '':
        db_connection = mysql.connector.connect(
          host= "localhost",
          user= "root",
        )

#### Creating database_cursor to perform SQL operation ####
        db_cursor = db_connection.cursor()
        db_cursor.execute("CREATE DATABASE database1")
        db_cursor.execute("GRANT ALL PRIVILEGES ON database1. * TO 'root'@'localhost'")

#### Get list of all databases ####
        db_cursor.execute("SHOW DATABASES")

#### Print all databases ####
        for db in db_cursor:
            print(db)
        filename = doc_root+'/wp-config.php'

        db = {
            "define( 'DB_NAME', 'database_name_here' );" : "define( 'DB_NAME', 'database1' );"
        }   

        for line in fileinput.input(filename, inplace=True):
            line = line.rstrip('\w\n')
            print(db.get(line, line))
    else: 
#### Check mysql is working ####
        db_connection = mysql.connector.connect(
          host= "localhost",
          user= "root",
        )    
        db_cursor = db_connection.cursor()
        db_cursor.execute('CREATE DATABASE ' + database )
        db_cursor.execute("GRANT ALL PRIVILEGES ON "+database+". * TO 'root'@'localhost'")
#### Get list of all databases ####
        db_cursor.execute("SHOW DATABASES")

#### Print all databases ####
        for db in db_cursor:
            print(db)


        filename = default_doc_root+'/wp-config.php'

        db = {
            "define( 'DB_NAME', 'database_name_here' );" : "define( 'DB_NAME'," '\''+str(database)+'\''+" );",
        }

        for line in fileinput.input(filename, inplace=True):
            line = line.rstrip('\w\n')
            print(db.get(line, line))

    newuser = input("Please if you create new user :")
    if newuser == '':
        print("Default user is root")
        for db in db_cursor:
            print(db)
        filename = doc_root+'/wp-config.php'

        db = {
            "define( 'DB_USER', 'username_here' );" : "define( 'DB_USER', 'root' );" ,
            "define( 'DB_PASSWORD', 'password_here' );" : "define( 'DB_PASSWORD', '' );"
        }

        for line in fileinput.input(filename, inplace=True):
            line = line.rstrip('\w\n')
            print(db.get(line, line))
    else:
        newuser_password = getpass.getpass("Please enter your New user password:")
        db_connection = mysql.connector.connect(
          host= "localhost",
          user= "root",
        )
#### Creating database_cursor to perform SQL operation ####
        db_cursor = db_connection.cursor()
        db_cursor.execute("create user '"+newuser+"'@'localhost' identified by '"+newuser_password+"';")
        db_cursor.execute("GRANT ALL privileges ON *.* TO '"+newuser+"'@'localhost'")
#### Get list of all databases ####
        db_cursor.execute("SELECT User FROM mysql.user")

#### Print all databases ####
    #for db in db_cursor:
        #print(db)
        print("Your user is :"+newuser+"\n And is password is :"+newuser_password)
        print("")
        filename = default_doc_root+'/wp-config.php'

        db = {
            "define( 'DB_USER', 'username_here' );" : "define( 'DB_USER'," '\''+str(newuser)+'\''+" );",
            "define( 'DB_PASSWORD', 'password_here' );" : "define( 'DB_PASSWORD', '"+newuser_password+"' );"
        }

        for line in fileinput.input(filename, inplace=True):
            line = line.rstrip('\w\n')
            print(db.get(line, line))


    print("")

#### Change premissions ####
    os.system("chmod +x wp-cli.phar")

#### Move wp-cli ####
    os.system("mv wp-cli.phar /bin/wp")

#### Create dir ####
    os.makedirs(default_doc_root+'test', exist_ok=True)

#### Download wp core ####
    os.system('cd '+default_doc_root+'test\nwp core download --allow-root')

#### Copy WP file to doc root ####
    subprocess.call("cp -r "+default_doc_root+'test/*  ' +default_doc_root , shell=True)

#### Delete dir which are created ####
    shutil.rmtree(default_doc_root+'test')
    print("")

#### Update information ####
    Url = input("Please enter your Url :")
    if Url != "" :
        print(Url)
    else:
        Url = "localhost"

    Title = input("Please enter your Title :")
    if Title != "" :
        print(Title)
    else:
        Title = "Example"

    Admin_user= input("Please enter your Admin user :")
    if Admin_user != "" :
        print(Admin_user)
    else:
        Admin_user = "root"

    Admin_password = input("Please enter your Admin password :")
    if Admin_password != "" :
        print(Admin_password)
    else:
        Admin_password = "1234"

    Email = input("Please enter your Email :")
    if Email != "" :
        print(Email)
    else:
        Email = "info@example.com"
    

    os.system('cd '+default_doc_root+' ; wp core install --url='+Url+' --title='+Title+' --admin_user='+Admin_user+' --admin_password='+Admin_password+' --admin_email='+Email+' --allow-root')    

    print("Your url is :"+Url)
    print("Your title is :"+Title)
    print("Your admin user is :"+Admin_user)
    print("Your admin password is:"+Admin_password)
    print("Your email is :"+Email)
#### Httpd restart ####
    subprocess.call('systemctl start httpd', shell=True)
#### create loop ####    
    repeat =input("repeat this again yes or no :")
    if repeat != "yes":
        break
