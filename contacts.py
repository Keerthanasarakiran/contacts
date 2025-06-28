import sqlite3
from sqlite3 import Error

# Create database connection
conn = None
try:
    conn = sqlite3.connect('contact_book.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)
    conn.commit()
except Error as e:
    print(f"Database error: {e}")
    exit()

while True:
    print("\n--- Contact Book Menu ---")
    print("1. Add a new contact")
    print("2. View all contacts")
    print("3. Update a contact")
    print("4. Delete a contact")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ")
    
    # Add a new contact
    if choice == '1':
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        email = input("Enter email: ")
        
        try:
            cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", 
                         (name, phone, email))
            conn.commit()
            print("Contact added successfully!")
        except Error as e:
            print(f"Error adding contact: {e}")
    
    # View all contacts
    elif choice == '2':
        try:
            cursor.execute("SELECT * FROM contacts")
            contacts = cursor.fetchall()
            
            if not contacts:
                print("No contacts found!")
            else:
                print("\n--- All Contacts ---")
                for contact in contacts:
                    print(f"ID: {contact[0]}")
                    print(f"Name: {contact[1]}")
                    print(f"Phone: {contact[2]}")
                    print(f"Email: {contact[3]}\n")
        except Error as e:
            print(f"Error retrieving contacts: {e}")
    
    # Update a contact
    elif choice == '3':
        try:
            cursor.execute("SELECT * FROM contacts")
            contacts = cursor.fetchall()
            
            if not contacts:
                print("No contacts to update!")
                continue
                
            print("\n--- Current Contacts ---")
            for contact in contacts:
                print(f"ID: {contact[0]}, Name: {contact[1]}")
            
            contact_id = input("\nEnter ID of contact to update: ")
            
            cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
            contact = cursor.fetchone()
            
            if not contact:
                print("Contact not found!")
                continue
                
            print("\nCurrent details:")
            print(f"1. Name: {contact[1]}")
            print(f"2. Phone: {contact[2]}")
            print(f"3. Email: {contact[3]}")
            
            field = input("\nWhich field to update? (1-3, or 'all'): ")
            
            if field == '1' or field.lower() == 'all':
                new_name = input("Enter new name: ")
            if field == '2' or field.lower() == 'all':
                new_phone = input("Enter new phone: ")
            if field == '3' or field.lower() == 'all':
                new_email = input("Enter new email: ")
            
            if field == '1':
                cursor.execute("UPDATE contacts SET name = ? WHERE id = ?", 
                             (new_name, contact_id))
            elif field == '2':
                cursor.execute("UPDATE contacts SET phone = ? WHERE id = ?", 
                             (new_phone, contact_id))
            elif field == '3':
                cursor.execute("UPDATE contacts SET email = ? WHERE id = ?", 
                             (new_email, contact_id))
            elif field.lower() == 'all':
                cursor.execute("""
                    UPDATE contacts 
                    SET name = ?, phone = ?, email = ? 
                    WHERE id = ?
                """, (new_name, new_phone, new_email, contact_id))
            else:
                print("Invalid field selection!")
                continue
                
            conn.commit()
            print("Contact updated successfully!")
            
        except Error as e:
            print(f"Error updating contact: {e}")
    
    # Delete a contact
    elif choice == '4':
        try:
            cursor.execute("SELECT id, name FROM contacts")
            contacts = cursor.fetchall()
            
            if not contacts:
                print("No contacts to delete!")
                continue
                
            print("\n--- Current Contacts ---")
            for contact in contacts:
                print(f"ID: {contact[0]}, Name: {contact[1]}")
            
            contact_id = input("\nEnter ID of contact to delete: ")
            
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print("Contact deleted successfully!")
            else:
                print("No contact found with that ID!")
                
        except Error as e:
            print(f"Error deleting contact: {e}")
    
    # Exit
    elif choice == '5':
        print("Goodbye!")
        conn.close()
        break
    
    else:
        print("Invalid choice. Please enter a number between 1-5.")