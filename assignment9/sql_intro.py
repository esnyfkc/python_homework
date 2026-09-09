import sqlite3

def add_publisher(cursor, name):
    try:
        cursor.execute(
            "INSERT INTO publishers (name) VALUES (?)",
            (name,)
        )
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")

def add_magazine(cursor, name, publisher_name):
    cursor.execute(
        "SELECT publisher_id FROM publishers WHERE name = ?",
        (publisher_name,)
    )

    result = cursor.fetchone()

    if result is None:
        print(f"Publisher {publisher_name} was not found.")
        return

    publisher_id = result[0]

    try:
        cursor.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
            (name, publisher_id)
        )
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")

def add_subscriber(cursor, name, address):
    cursor.execute(
        """
        SELECT subscriber_id
        FROM subscribers
        WHERE name = ? AND address = ?
        """,
        (name, address)
    )

    result = cursor.fetchone()

    if result is not None:
        print(f"{name} at {address} is already in the database.")
        return

    try:
        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)",
            (name, address)
        )
    except sqlite3.IntegrityError:
        print(f"{name} at {address} is already in the database.")


def add_subscription(cursor, subscriber_name, magazine_name, expiration_date):
    # Find subscriber ID
    cursor.execute(
        "SELECT subscriber_id FROM subscribers WHERE name = ?",
        (subscriber_name,)
    )
    subscriber = cursor.fetchone()

    if subscriber is None:
        print(f"Subscriber {subscriber_name} was not found.")
        return

    # Find magazine ID
    cursor.execute(
        "SELECT magazine_id FROM magazines WHERE name = ?",
        (magazine_name,)
    )
    magazine = cursor.fetchone()

    if magazine is None:
        print(f"Magazine {magazine_name} was not found.")
        return

    subscriber_id = subscriber[0]
    magazine_id = magazine[0]

    try:
        cursor.execute(
            """
            INSERT INTO subscriptions
            (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
            """,
            (subscriber_id, magazine_id, expiration_date)
        )
    except sqlite3.IntegrityError:
        print(
            f"{subscriber_name} is already subscribed to {magazine_name}."
        )
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
            FOREIGN KEY (publisher_id) 
                REFERENCES publishers (publisher_id)
        )
    """)

    # Create subscribers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            UNIQUE (name, address)
        )
    """)

    # Create subscriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id)
                REFERENCES subscribers (subscriber_id),
            FOREIGN KEY (magazine_id)
                REFERENCES magazines (magazine_id),
            UNIQUE (subscriber_id, magazine_id)
        )
    """)


    # Add publishers
    add_publisher(cursor, "Penske Media Corporation")
    add_publisher(cursor, "Condé Nast")
    add_publisher(cursor, "Hearst Magazines")

    # Add magazines
    add_magazine(cursor, "Rolling Stone", "Penske Media Corporation")
    add_magazine(cursor, "Vogue", "Condé Nast")
    add_magazine(cursor, "Cosmopolitan", "Hearst Magazines")

    # Add subscribers
    add_subscriber(cursor, "Elif Yumuk", "123 Main St")
    add_subscriber(cursor, "Keith Schikore", "431 Northlake St")
    add_subscriber(cursor, "Esin Yufkaci", "2880 Scott Blv")

    # Add subscriptions
    add_subscription(cursor, "Elif Yumuk", "Rolling Stone", "2027-01-01")
    add_subscription(cursor, "Elif Yumuk", "Vogue", "2027-02-02")
    add_subscription(cursor, "Elif Yumuk", "Cosmopolitan", "2027-03-03")

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
        SELECT magazines.*
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