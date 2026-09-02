import sqlite3

def add_publisher(cursor, name):
    try:
        cursor.execute(
            "INSERT INTO publishers (name) VALUES (?)",
            (name,)
        )
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")

def add_magazine(cursor, name, publisher_id):
    try:
        cursor.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
            (name, publisher_id)
        )
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")

def add_subscriber(cursor, name, address):
    cursor.execute(
        "SELECT * FROM subscribers WHERE name = ? AND address = ?",
        (name, address)
    )

    results = cursor.fetchall()

    if len(results) > 0:
        print(f"{name} at {address} is already in the database.")
        return

    try:
        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)",
            (name, address)
        )
    except sqlite3.Error as e:
        print("Error adding subscriber:", e)


def add_subscription(cursor, subscriber_id, magazine_id, expiration_date):
    cursor.execute(
        """
        SELECT * FROM subscriptions
        WHERE subscriber_id = ? AND magazine_id = ?
        """,
        (subscriber_id, magazine_id)
    )

    results = cursor.fetchall()

    if len(results) > 0:
        print("This subscription is already in the database.")
        return

    try:
        cursor.execute(
            """
            INSERT INTO subscriptions
            (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
            """,
            (subscriber_id, magazine_id, expiration_date)
        )
    except sqlite3.Error as e:
        print("Error adding subscription:", e)

try:
    # Connect to database
    conn = sqlite3.connect("../db/magazines.db")
    # Turn on foreign key checking
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    
    # Create publishers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Create magazines table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id)
        )
    """)

    # Create subscribers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    # Create subscriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers (subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (magazine_id)
        )
    """)


    # Add publishers
    add_publisher(cursor, "Penske Media Corporation")
    add_publisher(cursor, "Condé Nast")
    add_publisher(cursor, "Hearst Magazines")

    # Add magazines
    add_magazine(cursor, "Rolling Stone", 1)
    add_magazine(cursor, "Vogue", 2)
    add_magazine(cursor, "Cosmopolitan", 3)

    # Add subscribers
    add_subscriber(cursor, "Elif Yumuk", "123 Main St")
    add_subscriber(cursor, "Keith Schikore", "431 Northlake St")
    add_subscriber(cursor, "Esin Yufkaci", "2880 Scott Blv")

    # Add subscriptions
    add_subscription(cursor, 1, 1, "2027-01-01")
    add_subscription(cursor, 1, 2, "2027-02-02")
    add_subscription(cursor, 2, 3, "2027-03-03")

    # Query 1: Retrieve all information from the subscribers table
    cursor.execute("SELECT * FROM subscribers")
    results = cursor.fetchall()

    print("\nAll Subscribers:")
    for row in results:
        print(row)


    # Query 2: Retrieve all magazines sorted by name
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    results = cursor.fetchall()

    print("\nMagazines Sorted by Name:")
    for row in results:
        print(row)


    # Query 3: Find magazines for a particular publisher
    cursor.execute("""
        SELECT magazines.name, publishers.name
        FROM magazines
        JOIN publishers
        ON magazines.publisher_id = publishers.publisher_id
        WHERE publishers.name = ?
    """, ("Condé Nast",))

    results = cursor.fetchall()

    print("\nMagazines published by Condé Nast:")
    for row in results:
        print(row)

    conn.commit()

    print("Database setup and queries completed successfully.")

except sqlite3.Error as e:
    print("Database error:", e)

finally:
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")