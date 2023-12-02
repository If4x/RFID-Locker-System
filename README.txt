RFID-Locker-System

by Deniz Türkmen, Sami Türkmen and Imanuel Fehse


1. Setup System
---------------
For setting up the system just run the "setup.py" script, which is located in the same path as this file.
This Script is firstly checking if the setup already has been run on the system. If not, it will create all
needed files and databases to run the program and launches a first time admin setup. Please DO NOT aboard this process!
If you do so, please delete all files, located in "/core/dbs". Then run the setup again.

2. Run system
-------------
To run the system you first have to complete the whole setup process (Step 1). After that you are able to run
the system operational so users could scan their RFID-cards and open their locker. To do so, just run the "system.py"
script, located in the same path as this file.
Now the program will start looking for a RFID-card which is scanned and open the corresponding locker to the card
if it does exist in the database.

3. Add new users locally
------------------------
To access the local User-Interface (UI) just run the "ui.py" script. It will create a graphical interface, where you're
able to search for already registered users, edit the data for an user, create new users or delete existing users.
IMPORTANT: To add a new admin username and corresponding password you have to do this on the local UI. You're not able
to do that in the Webinterface (we'll explain it to you in the next point) for safety reasons of the system. So only
authorised personal can access the UI to add a new admin which increases security.

4. Web Interface
----------------
To start the webserver just run the "server.js" file. The Webserver hosts a local Website on the IP-Address (of the system the server is running on) at
Port 8181.
Example:
The IPv4-Address of the system the server is running on is 192.168.178.69
The Website is hosted on port 8181 so the address of the Website is:
http://<Your IP-Address>:8181

5. Special Thanks
-----------------
We (the team of this project) want to give a special thanks to all the persons which helped or supported us in the
process of developing this project.
