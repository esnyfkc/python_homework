import sqlite3

conn = None

try:
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    # Task 1
    # Find the total price of the first 5 orders

    print("\nTask 1:")

    query = """
    SELECT orders.order_id,
           SUM(products.price * line_items.quantity) AS total_price
    FROM orders
    JOIN line_items
        ON orders.order_id = line_items.order_id
    JOIN products
        ON line_items.product_id = products.product_id
    GROUP BY orders.order_id
    ORDER BY orders.order_id
    LIMIT 5;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for order_id, total_price in results:
        print(order_id, f"{total_price:.2f}")


    # Task 2
    # Find the average order price for each customer

    print("\nTask 2:")

    query = """
    SELECT customers.customer_name,
           AVG(order_totals.total_price) AS average_total_price
    FROM customers
    LEFT JOIN (
        SELECT orders.customer_id AS customer_id_b,
               SUM(products.price * line_items.quantity) AS total_price
        FROM orders
        JOIN line_items
            ON orders.order_id = line_items.order_id
        JOIN products
            ON line_items.product_id = products.product_id
        GROUP BY orders.order_id, orders.customer_id
    ) AS order_totals
        ON customers.customer_id = order_totals.customer_id_b
    GROUP BY customers.customer_id, customers.customer_name;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for customer_name, average_total_price in results:
        if average_total_price is not None:
            print(customer_name, f"{average_total_price:.2f}")
        else:
            print(customer_name, "No orders")


    # Task 3
    # Create a new order for Perez and Sons
    # Miranda Harris is creating the order
    # The order has 10 of each of the 5 cheapest products

    print("\nTask 3:")

    # Find Perez and Sons
    cursor.execute("""
        SELECT customer_id
        FROM customers
        WHERE customer_name = 'Perez and Sons';
    """)

    row = cursor.fetchone()

    if row is None:
        raise ValueError("Customer 'Perez and Sons' not found")

    customer_id = row[0]


    # Find Miranda Harris
    cursor.execute("""
        SELECT employee_id
        FROM employees
        WHERE first_name = 'Miranda'
          AND last_name = 'Harris';
    """)

    row = cursor.fetchone()

    if row is None:
        raise ValueError("Employee 'Miranda Harris' not found")

    employee_id = row[0]


    # Find the 5 cheapest products
    cursor.execute("""
        SELECT product_id
        FROM products
        ORDER BY price
        LIMIT 5;
    """)

    products = cursor.fetchall()

    if len(products) < 5:
        raise ValueError("Fewer than 5 products found")


    # Start the transaction
    conn.execute("BEGIN")

    try:
        # Add the new order
        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id)
            VALUES (?, ?)
            RETURNING order_id;
        """, (customer_id, employee_id))

        order_id = cursor.fetchone()[0]


        # Add the 5 products to the order
        for product in products:
            product_id = product[0]

            cursor.execute("""
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, ?);
            """, (order_id, product_id, 10))


        # Save the transaction
        conn.commit()

    except sqlite3.Error:
        conn.rollback()
        raise


    # Show the items in the new order
    cursor.execute("""
        SELECT line_items.line_item_id,
               line_items.quantity,
               products.product_name
        FROM line_items
        JOIN products
            ON line_items.product_id = products.product_id
        WHERE line_items.order_id = ?;
    """, (order_id,))

    results = cursor.fetchall()

    for line_item_id, quantity, product_name in results:
        print(line_item_id, quantity, product_name)


    # Task 4
    # Find employees with more than 5 orders

    print("\nTask 4:")

    query = """
    SELECT employees.employee_id,
           employees.first_name,
           employees.last_name,
           COUNT(orders.order_id) AS order_count
    FROM employees
    JOIN orders
        ON employees.employee_id = orders.employee_id
    GROUP BY employees.employee_id,
             employees.first_name,
             employees.last_name
    HAVING COUNT(orders.order_id) > 5;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for employee_id, first_name, last_name, order_count in results:
        print(employee_id, first_name, last_name, order_count)


except (sqlite3.Error, ValueError) as e:
    print("Error:", e)

finally:
    if conn:
        conn.close()