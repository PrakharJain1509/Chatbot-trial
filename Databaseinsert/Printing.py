import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('website_data.db')
cursor = conn.cursor()

# Retrieve all data from the website_content table
cursor.execute('SELECT * FROM website_content')
data_rows = cursor.fetchall()

# Print the retrieved data
for row in data_rows:
    print(f"ID: {row[0]}")
    print(f"URL: {row[1]}")
    print(f"Text Content: {row[2]}")
    print(f"Hyperlinks: {row[3]}")
    print()

# Close the database connection
conn.close()
