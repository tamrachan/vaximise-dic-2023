from tkinter import * 
from tkinter import messagebox
import sqlite3

root = Tk()
root.title('Vaximise login system')
root.iconbitmap('C:/Users/tamra/OneDrive/Documents/Python GUI/Images/100.ico')
root.geometry("500x500")
root.configure(bg='#333333')

#Connects to database
conn = sqlite3.connect('vaximise_db.db')
c = conn.cursor()
count=0
c.execute(""" CREATE TABLE IF NOT EXISTS login(
	username varchar(20) NOT NULL,
	password varchar(20) NOT NULL
	)""")
#Insert admin details
'''c.execute(""" INSERT INTO login
	(username, password)
	VALUES ('admin','admin')
	""")
conn.commit()
'''

def open():
	root.pack()

def login():
	conn = sqlite3.connect('vaximise_db.db')
	c = conn.cursor()
	
	
	c.execute("SELECT * FROM login where username=? AND password=?", 
		(username_input.get(), password_input.get())
		)
	row=c.fetchone()
	
	if row:
		open()
		frame.destroy()
	elif username_input.get()=="" and password_input.get()=="":
		messagebox.showerror('Invalid login', 'Please enter in a username and password.')
	elif username_input.get()=="":
		messagebox.showerror('Invalid login', 'Please enter in a username.')
	elif password_input.get()=="":
		messagebox.showerror('Invalid login', 'Please enter in a password.')
	elif username_input.get()!= "admin" or password_input.get()!= "admin":
		messagebox.showerror('Invalid login', 'Login failed. Try again.')
		
		
		
def counter():
	#Only allows you to attempt entry 5 times - limits brute force
	global count
	if count<5:
		if username_input.get()=="admin" and password_input.get()=="admin":
			open()
			frame.destroy()
		elif username_input.get()=="" and password_input.get()=="":
			login()
		elif username_input.get()=="":
			login()
		elif password_input.get()=="":
			login()
		elif username_input.get()!= "admin" or password_input.get()!= "admin":
			login()
			count = count + 1
	else:
		login_button.configure(text=f'Limit reached. Try again tomorrow.')

#Creating the login page
frame = Frame(bg='#333333')

login_label = Label(frame, text="Login to Vaximise", bg='#333333', fg="#FFFFFF", font=("Arial",30))
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)

username_label = Label(frame, text="Username:", bg='#333333', fg='#FFFFFF', font=("Arial",16))
username_label.grid(row=1, column=0)
username_input = Entry(frame, font=("Arial",16))
username_input.grid(row=1, column=1, pady=20)

password_label = Label(frame, text="Password:", bg='#333333', fg='#FFFFFF', font=("Arial",16))
password_label.grid(row=2, column=0)
password_input = Entry(frame, font=("Arial",16),show="*")
password_input.grid(row=2, column=1, pady=20)
count=0
login_button = Button(frame, text="Login", bg='#333333', fg='#FFFFFF', font=("Arial",16), command=counter)
login_button.grid(row=3, column=0, columnspan=2, pady=30)
	
#Displays the login page
frame.pack()

root = Frame()

conn = sqlite3.connect('vaximise_db.db')
c = conn.cursor()

#Creates the table for the first time
c.execute(""" CREATE TABLE IF NOT EXISTS organisations(
	organisation text NOT NULL,
	country text NOT NULL,
	population integer NOT NULL,
	no_vaccinated integer NOT NULL,
	not_vaccinated integer,
	percentage_not_vaccinated decimal
	)""")


def update():
	conn = sqlite3.connect('vaximise_db.db')
	c = conn.cursor()

	record_id = delete_box.get()
	#Sets the new values onto the database
	c.execute("""UPDATE organisations SET
		organisation = :organisation, 
		country = :country,
		population = :population,
		no_vaccinated = :no_vaccinated,
		not_vaccinated = :not_vaccinated,
		percentage_not_vaccinated = :percentage_not_vaccinated

		WHERE oid = :oid""",
		{
		'organisation': organisation_editor.get(),
		'country': country_editor.get(),
		'population': population_editor.get(),
		'no_vaccinated': no_vaccinated_editor.get(),
		'not_vaccinated': (int(population_editor.get())-int(no_vaccinated_editor.get())),
		'percentage_not_vaccinated': (round((int(population_editor.get())-int(no_vaccinated_editor.get()))/int(population_editor.get())*100, 1)),
		'oid': record_id
		})

	conn.commit()
	conn.close()
	editor.destroy()

#Updates a record
def edit():
	global editor
	if delete_box.get()=="":
		messagebox.showerror('No ID selected', 'Please select the ID of the record to edit.')
		
	else:
		editor = Tk()
		editor.title('Update a record')
		editor.iconbitmap('C:/Users/tamra/OneDrive/Documents/Python GUI/Images/100.ico')
		editor.geometry("700x200")
		editor.configure(bg='#333333')
		
		conn = sqlite3.connect('vaximise_db.db')
		c = conn.cursor()


		record_id = delete_box.get()
		#Query the database, oid is the unique identifier like MAC address
		c.execute("SELECT * FROM organisations WHERE oid = " + record_id)
		records = c.fetchall() #can also do fetchone or fetchmany(num)

		#Loop through results
		
		global organisation_editor
		global country_editor
		global population_editor
		global no_vaccinated_editor

		#Create input boxes
		organisation_editor = Entry(editor, width=30, font=("Arial",15))
		organisation_editor.grid(row=0, column=1, padx=20)
		country_editor = Entry(editor, width=30, font=("Arial",15))
		country_editor.grid(row=1, column=1)
		population_editor = Entry(editor, width=30, font=("Arial",15))
		population_editor.grid(row=2, column=1)
		no_vaccinated_editor = Entry(editor, width=30, font=("Arial",15))
		no_vaccinated_editor.grid(row=3, column=1)

		#Create labels for input boxes
		organisation_label = Label(editor, text="Organisation:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
		organisation_label.grid(row=0, column=0)
		country_label = Label(editor, text="Country:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
		country_label.grid(row=1, column=0)
		population_label = Label(editor, text="Population:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
		population_label.grid(row=2, column=0)
		no_vaccinated_label = Label(editor, text="Number of people vaccinated:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
		no_vaccinated_label.grid(row=3, column=0)

		for record in records:
			organisation_editor.insert(0, record[0])
			country_editor.insert(0, record[1])
			population_editor.insert(0, record[2])
			no_vaccinated_editor.insert(0, record[3])

		#Save edited record button
		save_btn = Button(editor, text="Save Record", command=update)
		save_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

#Allows you to delete a record
def delete():
	conn = sqlite3.connect('vaximise_db.db')
	c = conn.cursor()
	if delete_box.get()=="":
		messagebox.showerror('No ID selected', 'Please select the ID of the record to delete.')
	else:
		c.execute("DELETE from organisations WHERE oid = " + delete_box.get())
		delete_box.delete(0, END)
		conn.commit()
		conn.close()
		query()

def submit():
	conn = sqlite3.connect('vaximise_db.db')
	c = conn.cursor() 
	#makes sure all fields are filled out
	if organisation.get()=="" and country.get()=="" and population.get()=="" and no_vaccinated.get()=="":
		messagebox.showerror('No input', 'Please fill in all fields.')
	elif organisation.get()=="":
		messagebox.showerror('No input', 'Please fill in the organisation field.')
	elif country.get()=="":
		messagebox.showerror('No input', 'Please fill in the country field.')
	elif population.get()=="":
		messagebox.showerror('No input', 'Please fill in the population field.')
	elif no_vaccinated.get()=="":
		messagebox.showerror('No input', 'Please fill in the no. vaccinated field.')
	else:
		c.execute("INSERT INTO organisations VALUES (:organisation, :country, :population, :no_vaccinated, :not_vaccinated, :percentage_not_vaccinated)",
		{
			'organisation': organisation.get(),
			'country': country.get(),
			'population': population.get(),
			'no_vaccinated': no_vaccinated.get(),
			'not_vaccinated': int(population.get())-int(no_vaccinated.get()),
			'percentage_not_vaccinated': round((int(population.get())-int(no_vaccinated.get()))/int(population.get())*100, 1)
		})
		conn.commit()
		conn.close()
		organisation.delete(0, END)
		country.delete(0, END)
		population.delete(0, END)
		no_vaccinated.delete(0, END)

	

#Prints the records onto the screen
def query():
	conn = sqlite3.connect('vaximise_db.db')
	c = conn.cursor()

	#Query the database, oid is the unique identifier (like a MAC address)
	c.execute("SELECT *, oid FROM organisations")
	records = c.fetchall() #can also do fetchone or fetchmany(num) but this fetches all records

	#Loop through results
	print_records = ''
	for record in records:
		print_records += str(record[6]) + "    " + str(record[0]) + "  " + str(record[1]) + "\n" #Record[0] is first name

	query_label = Label(root, text=print_records)
	query_label.grid(row=14, column=0, columnspan=2)
	conn.commit()
	conn.close()

#Create input boxes
root.configure(bg='#333333')
organisation = Entry(root, width=30)
organisation.grid(row=0, column=1, padx=20)
country = Entry(root, width=30)
country.grid(row=1, column=1)
population = Entry(root, width=30)
population.grid(row=2, column=1)
no_vaccinated = Entry(root, width=30)
no_vaccinated.grid(row=3, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

#Create labels for input boxes
organisation_label = Label(root, text="Organisation:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
organisation_label.grid(row=0, column=0)
country_label = Label(root, text="Country:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
country_label.grid(row=1, column=0)
population_label = Label(root, text="Population:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
population_label.grid(row=2, column=0)
no_vaccinated_label = Label(root, text="Number of people vaccinated:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
no_vaccinated_label.grid(row=3, column=0)

delete_box_label = Label(root, text="Select ID:", bg='#333333', fg="#FFFFFF", font=("Arial",15))
delete_box_label.grid(row=9, column=0, pady=5)


submit_btn = Button(root, text="Add Record To Database", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Create a query button
query_btn = Button(root, text="Show Records", fg="Red", command=query)
query_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

#Create a delete button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=131)

#Create an update button
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

def calculate_columns():
	calculate = Tk()
	calculate.title('Rankings')
	calculate.iconbitmap('C:/Users/tamra/OneDrive/Documents/Python GUI/Images/100.ico')
	calculate.geometry("700x200")
	calculate.configure(bg='#333333')
	conn = sqlite3.connect('vaximise_db.db')
	c = conn.cursor() 

	#Orders the records from the least vaccinated to the most vaccinated countries
	c.execute("SELECT *, oid FROM organisations ORDER BY percentage_not_vaccinated DESC")
	records = c.fetchall() 

	print_records_1 = ''
	print_records_2 = ''
	print_records_3 = ''

	#Displays the organisation, the country and the % not vaccinated
	title_label_1 = Label(calculate, text="Organisation:\t", bg='#333333', fg="#FFFFFF", font=("Arial",15))
	title_label_1.grid(row=1, column=0, columnspan=2)
	
	title_label_2 = Label(calculate, text="Country:\t", bg='#333333', fg="#FFFFFF", font=("Arial",15))
	title_label_2.grid(row=1, column=2, columnspan=2)

	title_label_3 = Label(calculate, text="Not vaccinated:\t", bg='#333333', fg="Red", font=("Arial",15))
	title_label_3.grid(row=1, column=4, columnspan=2)
	for record in records:
		print_records_1 += str(record[0]) + "\t\n" 
		print_records_2 += str(record[1]) + "\t\n"
		print_records_3 += str(record[5]) + "%" + "\t\n"

	query2_label_1 = Label(calculate, text=print_records_1, bg='#333333', fg="#FFFFFF", font=("Arial",15))
	query2_label_1.grid(row=2, column=0, columnspan=2)

	query2_label_2 = Label(calculate, text=print_records_2, bg='#333333', fg="#FFFFFF", font=("Arial",15))
	query2_label_2.grid(row=2, column=2, columnspan=2)

	query2_label_3 = Label(calculate, text=print_records_3, bg='#333333', fg="Red", font=("Arial",15))
	query2_label_3.grid(row=2, column=4, columnspan=2)

	conn.commit()
	conn.close()

calculate_btn = Button(root, text="View all", command=calculate_columns)
calculate_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

conn.commit()
conn.close()
root.mainloop()