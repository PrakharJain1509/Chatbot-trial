import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('website_data.db')
cursor = conn.cursor()

# Clear the data from the website_content table
cursor.execute('DELETE FROM website_content')
conn.commit()

# Close the database connection
conn.close()

print("Data in the 'website_content' table has been cleared.")
