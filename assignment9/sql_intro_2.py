import os
import sqlite3
import pandas as pd


try:
    # Connect to the lesson database
    conn = sqlite3.connect("../db/lesson.db")

    # Join line_items and products
    sql_statement = """
        SELECT
            line_items.line_item_id,
            line_items.quantity,
            line_items.product_id,
            products.product_name,
            products.price
        FROM line_items
        JOIN products
        ON line_items.product_id = products.product_id
    """

    # Load SQL results into a DataFrame
    df = pd.read_sql_query(sql_statement, conn)

    print("First 5 rows:")
    print(df.head())

    # Add total column
    df["total"] = df["quantity"] * df["price"]

    print("\nDataFrame with total:")
    print(df.head())

    # Group by product_id
    summary_df = df.groupby("product_id").agg({
        "line_item_id": "count",
        "total": "sum",
        "product_name": "first"
    })

    print("\nGrouped Summary:")
    print(summary_df.head())

    # Sort by product name
    summary_df = summary_df.sort_values(by="product_name")

    print("\nSorted Summary:")
    print(summary_df.head())

    # Save CSV inside the assignment9 directory
    output_file = os.path.join(
        os.path.dirname(__file__),
        "order_summary.csv"
    )

    summary_df.to_csv(output_file)

    print(f"\nCSV saved to: {output_file}")

except sqlite3.Error as e:
    print("Database error:", e)

finally:
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")