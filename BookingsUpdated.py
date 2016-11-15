#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Python2C_Comm.py
#  
#  Copyright 2016 raja <raja@raja-Inspiron-N5110>
#  
#  This program is not a free software; you can not redistribute it and/or modify
#  it. 
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#Author @ raja sumant
#Airways ticket booking client
#Python supports multiprocess
#Caution: Don't run this python program on idle as it uses easygui which is tkinter.
#Note: All rights reserved. Do not replicate code with out proper permission.


from easygui import * #Using easygui(tkinter) for creating interactive gui
import hashlib # Used to encrypt the password in md5.
import sys # importing system to make system calls.
import socket # socket programming involved to communicate between server and client.
import _mysql
import MySQLdb as mdb # DB is required so the python uses MySQLdb.
import subprocess as sp

#First we need to establish a connection with DB. This has been done manually for time being. 

def DB_Con():
	
	try:
		#
		con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

		cur = con.cursor()
		cur.execute("SELECT VERSION()")

		ver = cur.fetchone()
    
		print "Database version : %s " % ver
    
	except mdb.Error, e:
  
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

#def DB_Close():
	
	#if con:    
        #con.close()

def Login(uname,passwd,FlightChoice):
	
	p2=sp.Popen(["./C_Booking",uname,passwd,FlightChoice])
	
	
#Note: Register should be present in server. This is for testing purpose only
def Register(uname, passwd):
	#print uname,passwd
	p2=sp.Popen(["./TCP_Client_Send",'2',uname,passwd])
	


def Userprofile():
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(("localhost", 5000))
	FlightDate=client_socket.recv(512)
	#con = mdb.connect('localhost', 'testuser', 'test623', 'Userdb');
	#cur = con.cursor()
	
	msg = "Enter your personal information"
	title = "Select Your Flight and DOJ"
		
	
	#cur.execute("SELECT * FROM ListOfFlights")
	#fieldNames = cur.fetchall()
	#con.commit()
	#con.close()
	
	PersonalData = ["Name","Street Address","City","State","ZipCode"]
	#fieldNames.append(PersonalData)
	flightValues = []  # we start with blanks for the values
	DataValues = [] # we start with blanks for the values
	flightValues = choicebox(msg,title,FlightDate)
	DataValues = multenterbox(msg,title, PersonalData)

# make sure that none of the fields was left blank
	while 1:
		if DataValues == None: break
		errmsg = ""
		for i in range(len(DataValues)):
			if DataValues[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % PersonalData[i])
			if errmsg == "": break # no problems found
			DataValues = multenterbox(errmsg, title, PersonalData, flightValues)
	print "Reply was:", DataValues
	UserInsert(flightValues,DataValues)
	
def UserInsert(fieldNames,fieldValues):	
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(("localhost", 5000))
	while 1:
		data = client_socket.send(fieldNames+fieldValues)
	
	
def AdminLogin(uname,passwd):
	
	p3=sp.Popen(["./C",'3',uname,passwd])
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(("localhost", 5000))
	while 1:
		Login_correct = client_socket.recv(512)
	if (Login_correct == "AdminProfile"):
		client_socket.close()
		Adminprofile()

def AdminProfile():
	
	msgbox("Hello Admin! Press OK to continue")
	msg = "Add or Delete"
	title = "Admin Profile"
	fieldNames = ["Add Flight details","Delete Flight details"]#Admin needs to send SQL command to add or delete
	fieldValues = []  # we start with blanks for the values
	fieldValues = multpasswordbox(msg,title, fieldNames)
	while 1:
		
		if fieldValues == None: break
		errmsg = ""
		for i in range(len(fieldNames)):
			if fieldValues[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
			if errmsg == "": break # no problems found
			fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
	AdminAddDelete(fieldValues)

def AdminAddDelete(fieldValues):
	
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(("localhost", 5000))
	while 1:
		data = client_socket.send(fieldValues)
	

while 1:
	
	msgbox("Welcome to ABC Airlines! Press ok to continue!")
	DB_Con()
	msg ="Please make a choice."
	title = "Login/Register"
	choices = ["Booking", "AdminLogin","Register/Sign Up"]
	choice = choicebox(msg, title, choices)

	# note that we convert choice to string, in case
	# the user cancelled the choice, and we got None.
	msgbox("You chose: " + str(choice), "Redirecting...")
	
	# if - else statements go here according to the choice
	if choice=="Booking" :
		FlightData=[]
		with open('/home/surya/FlightData.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			FlightData=FlightData+row

		msgbox("Please Login!")
		msg = "Enter your User Name and Password"
		title = "Login Page"
		fieldNames = ["UserName,Password"]
		fieldValues = []  # we start with blanks for the values
		fieldValues = multpasswordbox(msg,title, fieldNames)
		md5_object = hashlib.md5()
		md5_object.update(fieldNames[1].encode('utf-8'))
		PWD = md5_object.hexdigest() # This is the md5 encrypted password.
		#msgbox("Hello, please enter your login details.")
		while 1:
			if fieldValues == None: break
			errmsg = ""
			for i in range(len(fieldNames)):
				if fieldValues[i].strip() == "":
					errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
			if errmsg == "": break # no problems found
			fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
		msg = "Make a choice"
		title = "Welcome to Flight Selection!"
		FlightChoice = choicebox(msg,title,FlightData)
		Login(fieldValues[0],PWD,FlightChoice)
		
	elif choice=="Register/Sign Up":
		
		msgbox("Please sign up!")
		msg = "Enter your User Name and Password"
		title = "Register/Sign Up"
		fieldNames = ["UserName","Password"]
		fieldValues = []  # we start with blanks for the values
		fieldValues = multpasswordbox(msg,title, fieldNames)
		

# make sure that none of the fields was left blank
		while 1:
			if fieldValues == None: break
			errmsg = ""
			for i in range(len(fieldNames)):
				if fieldValues[i].strip() == "":
					errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
			if errmsg == "": break # no problems found
			fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
		#print type(fieldNames)
		#print "Reply was:", fieldValues
		
		#Do the md5 encryption of the password
		md5_object = hashlib.md5()
		md5_object.update(fieldNames[1].encode('utf-8'))
		PWD = md5_object.hexdigest() # This is the md5 encrypted password.
		
		
		Register(fieldValues[0],PWD)
	
	elif choice=="AdminLogin":
		msgbox("Please Login!")
		msg = "Enter your User Name and Password"
		title = "Login Page"
		fieldNames = ["UserName","Password"]
		fieldValues = []  # we start with blanks for the values
		fieldValues = multpasswordbox(msg,title, fieldNames)
		md5_object = hashlib.md5()
		md5_object.update(fieldNames[1].encode('utf-8'))
		PWD = md5_object.hexdigest() # This is the md5 encrypted password.
		#msgbox("Hello, please enter your login details.")
		while 1:
			if fieldValues == None: break
			errmsg = ""
			for i in range(len(fieldNames)):
				if fieldValues[i].strip() == "":
					errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
			if errmsg == "": break # no problems found
			fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
		AdminLogin(fieldValues[0],PWD)
		
	#DB_Close()
	
	msg = "Do you want to continue?"
	title = "Please Confirm"
	if ccbox(msg, title):     # show a Continue/Cancel dialog
		pass  # user chose Continue
	else:
		sys.exit(0)           # user chose Cancel

