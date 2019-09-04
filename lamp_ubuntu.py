#############################################################################################################################################
#!/bin/python3                                                                                                                              #
# Name: Lamp_wordpress.py                                                                                                                   #
# Author: Harmandeep Singh                                                                                                                  #
# Profile: DevOps Engineer                                                                                                                  #
# Email: harmandeep04061999@gmail.com                                                                                                       #
#                                                                                                                                           #
#############################################################################################################################################
##################################################### Import Module For Using LAMP ##########################################################
#############################################################################################################################################
import socket, os, sys, shutil ,subprocess  ,fileinput ,getpass                                                                             #
##################################################### Install Module ########################################################################
#############################################################################################################################################
subprocess.call(' apt-get install python3-mysql.connector',shell=True)                                                                      #
##################################################### Import Mysql Module ###################################################################
import mysql.connector                                                                                                                      #
############################################################################################################################################# 
##################################################### Install Ubuntu Packages ###############################################################
#############################################################################################################################################
subprocess.call('apt update ', shell=True)                                                                                                  #
subprocess.call('apt-get install -y apache2 mysql-server python-mysqldb  php php-mysql ', shell=True)                                       #
#############################################################################################################################################
##################################################### Start and enable applications for Ubuntu  #############################################
#############################################################################################################################################
subprocess.call('systemctl start apache2 ', shell=True)                                                                                     #
subprocess.call('systemctl start mysql ', shell=True)                                                                                       #
subprocess.call('systemctl enable apache2', shell=True)                                                                                     #
subprocess.call('systemctl enable mysql', shell=True)                                                                                       #
#############################################################################################################################################
##################################################### Check Mysql User and Password #########################################################
#############################################################################################################################################
mysql_passwd= subprocess.getoutput(" grep password  /etc/mysql/debian.cnf |awk '{print $3}'|head -n1")                                      #
mysql_user = subprocess.getoutput(" grep user  /etc/mysql/debian.cnf |awk '{print $3}'|head -n1")                                           #
#############################################################################################################################################
##################################################### Create Mysql Database And User ########################################################
#############################################################################################################################################
database = input("Please enter your db : ")                                                                                                 #
if database != "" :                                                                                                                         #
    print(database)                                                                                                                         #
else:                                                                                                                                       #
    database = "wp_database"                                                                                                                #
newuser = input("Please if you create new user :")                                                                                          #
if newuser != "":                                                                                                                           #
    newuser_password = getpass.getpass("Please enter your New user password:")                                                              #
    db_connection = mysql.connector.connect(                                                                                                #
    host= "localhost",                                                                                                                      #
    user= mysql_user,                                                                                                                       #
    passwd= mysql_passwd                                                                                                                    #
    )                                                                                                                                       # 
    db_cursor = db_connection.cursor()                                                                                                      # 
    db_cursor.execute('CREATE DATABASE ' + database )                                                                                       # 
    db_cursor.execute("create user '"+newuser+"'@'localhost' identified by '"+newuser_password+"';")                                        #
    db_cursor.execute("GRANT ALL PRIVILEGES ON "+database+". * TO '"+newuser+"'@'localhost'")                                               #
##################################################### List of all databases #################################################################
    db_cursor.execute("SHOW DATABASES")                                                                                                     #
    print("Your New user is :"+ mysql_user +"\nAnd password is : "+mysql_user)                                                              #
    for db in db_cursor:                                                                                                                    #
            print(db)                                                                                                                       #
#############################################################################################################################################
else:                                                                                                                                       #
#############################################################################################################################################
###################################################### Create Only Mysql Database ###########################################################
#############################################################################################################################################
    newuser_password = mysql_passwd                                                                                                         #
    newuser = mysql_user                                                                                                                    #
    db_connection = mysql.connector.connect(                                                                                                #
    host= "localhost",                                                                                                                      #
    user= mysql_user,                                                                                                                       # 
    passwd= mysql_passwd                                                                                                                    #
    )                                                                                                                                       # 
    db_cursor = db_connection.cursor()                                                                                                      #
    db_cursor.execute('CREATE DATABASE ' + database )                                                                                       #
#####################################################  List of all databases ################################################################ 
    db_cursor.execute("SHOW DATABASES")                                                                                                     #
    print("Your New user is :"+ mysql_user +"\nAnd password is : "+mysql_user)                                                              #
    for db in db_cursor:                                                                                                                    #
            print(db)                                                                                                                       #
#############################################################################################################################################
###################################################### Install Wordpress.Zip ################################################################
#############################################################################################################################################
os.system("wget https://wordpress.org/latest.zip")                                                                                          #
###################################################### Unzip Wordpress ######################################################################
os.system("unzip latest.zip")                                                                                                               #
###################################################### Copy wordpress to document root ######################################################
subprocess.call("cp -r   wordpress/*  /var/www/html ", shell=True)                                                                          #
###################################################### Rename wp-congig.php #################################################################
os.system("mv /var/www/html/wp-config-sample.php   /var/www/html/wp-config.php")                                                            #
###################################################### Remove zip file ######################################################################
shutil.rmtree('wordpress')                                                                                                                  #
os.remove('latest.zip')                                                                                                                     #
print("")                                                                                                                                   #
###################################################### Edit Wordpress #######################################################################
filename = '/var/www/html/wp-config.php'                                                                                                    #
db = {                                                                                                                                      #
    "define( 'DB_USER', 'username_here' );" : "define( 'DB_USER'," '\''+str(newuser)+'\''+" );",                                            #
    "define( 'DB_PASSWORD', 'password_here' );" : "define( 'DB_PASSWORD', '"+newuser_password+"' );",                                       # 
    "define( 'DB_NAME', 'database_name_here' );" : "define( 'DB_NAME'," '\''+str(database)+'\''+" );"                                       #
}                                                                                                                                           #
for line in fileinput.input(filename, inplace=True):                                                                                        #
    line = line.rstrip('\w\n')                                                                                                              #
    print(db.get(line, line))                                                                                                               #
###################################################### Change premissions Wp-Cli ############################################################
os.system("wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar")
os.system("chmod +x wp-cli.phar")                                                                                                           #
###################################################### Move Wp-Cli ##########################################################################
os.system("mv wp-cli.phar /bin/wp")                                                                                                         #
###################################################### Create Directory For Testing #########################################################
os.makedirs('/var/www/html/test', exist_ok=True)                                                                                            #
###################################################### Download Wp Core #####################################################################
os.system('cd /var/www/html/test\nwp core download --allow-root')                                                                           #
###################################################### Copy WP Core file to doc root ########################################################
subprocess.call("cp -r   /var/www/html/test/*  /var/www/html ", shell=True)                                                                 #
###################################################### Delete Test Directory ################################################################
shutil.rmtree('/var/www/html/test')                                                                                                         #
print("")                                                                                                                                   #
#############################################################################################################################################
###################################################### Update Wordpress Information #########################################################
#############################################################################################################################################
Url = "localhost"                                                                                                                       #
Title = input("Please enter your Title :")                                                                                                  #
if Title != "" :                                                                                                                            #
        print(Title)                                                                                                                        #
else:                                                                                                                                       #
    Title = "Example"                                                                                                                       # 
Admin_user= input("Please enter your Admin user :")                                                                                         #
if Admin_user != "" :                                                                                                                       #
    print(Admin_user)                                                                                                                       #
else:                                                                                                                                       #
    Admin_user = "root"                                                                                                                     #
Admin_password = input("Please enter your Admin password :")                                                                                #
if Admin_password != "" :                                                                                                                   #
    print(Admin_password)                                                                                                                   #
else:                                                                                                                                       # 
    Admin_password = "1234"                                                                                                                 #
Email = input("Please enter your Email :")                                                                                                  #
if Email != "" :                                                                                                                            # 
    print(Email)                                                                                                                            #
else:                                                                                                                                       #
    Email = "info@example.com"                                                                                                              #
###################################################### Wordpress Install Website ############################################################
os.system('cd /var/www/html/ ; wp core install --url='+Url+' --title='+Title+' --admin_user='+Admin_user+' --admin_password='+Admin_password+' --admin_email='+Email+' --allow-root')                                                                                                     # 
###################################################### Output of Wordpress information ######################################################
print("Your url is :"+Url)                                                                                                                  #
print("Your title is :"+Title)                                                                                                              #
print("Your admin user is :"+Admin_user)                                                                                                    #
print("Your admin password is:"+Admin_password)                                                                                             #
print("Your email is :"+Email)                                                                                                              #
###################################################### Restart Apache2 ######################################################################
subprocess.call('systemctl restart apache2 ', shell=True)                                                                                   #
#############################################################################################################################################
#    U     U      BBBBBB      U     U      NN      N      TTTTTTTTTT      U     U                      11  888888               4     4     #
#    U     U      B    B      U     U      N N     N          T           U     U                      11 8      8              4     4     #
#    U     U      B    B      U     U      N  N    N          T           U     U                      11 8      8              4     4     # 
#    U     U      BBBBBB      U     U      N   N   N          T           U     U     ============     11 88888888              4444444     #
#    U     U      B    B      U     U      N    N  N          T           U     U                      11 8      8    O O O           4     # 
#    U     U      B    B      U     U      N     N N          T           U     U     ============     11 8      8    0   0           4     #
#     U U U       BBBBBB       U U U       N      NN          T            U U U                       11  888888     O O 0           4     #
#############################################################################################################################################
#############################################################################################################################################
#    U     U      BBBBBB      U     U      NN      N      TTTTTTTTTT      U     U                      11  99999                 4     4    #
#    U     U      B    B      U     U      N N     N          T           U     U                      11 9     9                4     4    #
#    U     U      B    B      U     U      N  N    N          T           U     U                      11 9     9                4     4    #
#    U     U      BBBBBB      U     U      N   N   N          T           U     U     ============     11  999999                4444444    #
#    U     U      B    B      U     U      N    N  N          T           U     U                      11       9      O O O           4    #
#    U     U      B    B      U     U      N     N N          T           U     U     ============     11       9      0   0           4    #
#     U U U       BBBBBB       U U U       N      NN          T            U U U                       11       9      O O 0           4    #
#############################################################################################################################################

