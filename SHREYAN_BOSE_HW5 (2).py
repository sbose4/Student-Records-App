from tkinter import Tk, Entry, Text, END, font, Label, Button, BOTH
import sqlite3
from tkinter.messagebox import showinfo
from datetime import datetime

# Create the main application window
app = Tk()
app.title('Student Records')
app.geometry('600x600')

# Create a custom font with your desired size and other attributes
custom_font = font.nametofont("TkDefaultFont")  # Start with the default font
custom_font.configure(size=18)  # Set the desired font size

# Set the custom font as the default font for the application
app.option_add("*Font", custom_font)

# Connect to the SQLite database and create a cursor
conn = sqlite3.connect('records.db')
cursor = conn.cursor()

# Create a 'students' table in the database if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS students (pantherid INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
conn.commit()

# Create and place labels for PantherID, Name, and Email
pantherid_label = Label(master=app, text='PantherID')
pantherid_label.grid(row=0, column=0)
name_label = Label(master=app, text='Name')
name_label.grid(row=1, column=0)
email_label = Label(master=app, text='Email')
email_label.grid(row=2, column=0)

# Create and place entry widgets for PantherID, Name, and Email
pantherid_entry = Entry(master=app)
pantherid_entry.grid(row=0, column=1)
name_entry = Entry(master=app)
name_entry.grid(row=1, column=1)
email_entry = Entry(master=app)
email_entry.grid(row=2, column=1)

# Define a function to handle adding a student record
def on_add_student_button_clicked():
    # Step-1: Obtain info from entry widgets
    pantherid = int(pantherid_entry.get())
    name = name_entry.get()
    email = email_entry.get()

    # Step-2: Insert these info into the database
    cursor.execute('INSERT INTO Students (PantherID, Name, Email) VALUES (?,?,?)', (pantherid, name, email))
    conn.commit()

    # Clear the entry fields
    pantherid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)

    # Show an information message
    showinfo(message='Student record added to the database...')

# Define a function to list student records
def on_list_student_button_clicked():
    cursor.execute('SELECT * from Students')
    records = cursor.fetchall()
    txt.delete(0.0, END)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    txt.insert(END, f'--- Student list as of {timestamp} ---\n')
    for record in records:
        txt.insert(END, f"PantherID: {record[0]}   Name:{record[1]}   Email:{record[2]}\n")

# Define a function to search for a student record
def on_search_record_button_clicked():
    # Step-1: Obtain PantherID from entry widget
    pantherid = pantherid_entry.get()

    # Step-2: Check if PantherID is entered
    if pantherid:
        # Step-3: Search for the record in the database
        cursor.execute('SELECT * FROM Students WHERE PantherID = ?', (pantherid,))
        record = cursor.fetchone()

        # Step-4: Display the record or show a message if not found
        if record:
            txt.delete(0.0, END)
            txt.insert(END, f'PantherID: {record[0]}   Name: {record[1]}   Email: {record[2]}')
        else:
            showinfo(message=f'No record was found for {pantherid}')
    else:
        showinfo(message='Please enter a PantherID to search for a record')

# Define a function to update a student record
def on_update_record_button_clicked():
    # Step-1: Obtain info from entry widgets
    pantherid = pantherid_entry.get()
    name = name_entry.get()
    email = email_entry.get()

    # Step-2: Check if PantherID, Name, and Email are entered
    if pantherid and name and email:
        # Step-3: Check if the record exists
        cursor.execute('SELECT * FROM Students WHERE PantherID = ?', (pantherid,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Step-4: Update the record in the database
            cursor.execute('UPDATE Students SET Name=?, Email=? WHERE PantherID=?', (name, email, pantherid))
            conn.commit()
            showinfo(message='Record updated successfully...')
        else:
            showinfo(message=f'No record was found for {pantherid}')
    else:
        showinfo(message='Please enter PantherID, Name, and Email to update a record')

# Define a function to delete a student record
def on_delete_record_button_clicked():
    # Step-1: Obtain PantherID from entry widget
    pantherid = pantherid_entry.get()

    # Step-2: Check if PantherID is entered
    if pantherid:
        # Step-3: Check if the record exists
        cursor.execute('SELECT * FROM Students WHERE PantherID = ?', (pantherid,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Step-4: Delete the record from the database
            cursor.execute('DELETE FROM Students WHERE PantherID=?', (pantherid,))
            conn.commit()
            showinfo(message='Record deleted successfully...')
        else:
            showinfo(message=f'No record was found for {pantherid}')
    else:
        showinfo(message='Please enter a PantherID to delete a record')

# Define a function to export records to CSV
def export_to_csv():
    # Step-1: Fetch all records from the database
    cursor.execute('SELECT * FROM Students')
    records = cursor.fetchall()

    # Step-2: Ask the user to select a file for saving
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    # Step-3: Write records to the selected file
    with open(file_path, 'w') as file:
        file.write("PantherID,Name,Email\n")
        for record in records:
            file.write(f"{record[0]},{record[1]},{record[2]}\n")

# Create buttons for adding and listing student records
button_add = Button(master=app, text='Add Student', command=on_add_student_button_clicked)
button_add.grid(row=3, column=0, columnspan=2)

button_list = Button(master=app, text='List Students', command=on_list_student_button_clicked)
button_list.grid(row=4, column=0, columnspan=2)

# Create buttons for searching, updating, and deleting student records
button_search = Button(master=app, text='Search Record', command=on_search_record_button_clicked)
button_search.grid(row=3, column=1, columnspan=2)

button_update = Button(master=app, text='Update Record', command=on_update_record_button_clicked)
button_update.grid(row=4, column=1, columnspan=2)

button_delete = Button(master=app, text='Delete Record', command=on_delete_record_button_clicked)
button_delete.grid(row=3, column=2, columnspan=2)

# Create a button for exporting records to CSV
button_export_csv = Button(master=app, text='Export to CSV', command=export_to_csv)
button_export_csv.grid(row=4, column=2, columnspan=2)

# Create a Text widget to display student records
txt = Text(master=app, height=10, width=50)
txt.grid(row=5, column=0, columnspan=2)

# Start the main application loop
app.mainloop()

