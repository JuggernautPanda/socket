import MySQLdb
import csv

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
cur = con.cursor()
cur.execute("SELECT * FROM FlightData")
rows = cur.fetchall()

with open('/tmp/FlightData.csv','w') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)


# Contents of FlightData table should be as follows:
# FlightName,Date : 
# FlightName can be a string like : AS200 From NewYork To WashingtonDC
# Date can be a string like : 17th Nov, 18th Nov ,etc.