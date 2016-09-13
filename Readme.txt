to set up the server:
1. install graphviz and set bin folder to system path
2. install Python 3.5, scipy, numpy, scikit, and mysql-connector
3. create a new mysql database and change the db credentials in MysqlConnection/Connector in the code correspondingly
4. load data2016.sql into the database(permission required due to privacy concerns)
5. to run the server in a host other than localhost, try configuring the run() function of HTTP/server.py
6. execute server.py

for client:
by default the app is hosted at localhost:8083. Go to this URL with chrome or firefox. 

extra-note: the project is developed using Pycharm. It can be loaded as a Pycharm project directly.
