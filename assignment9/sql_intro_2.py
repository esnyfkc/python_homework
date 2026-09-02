import sqlite3
import pandas as pd


try:
    conn = sqlite3.connect("../db/lesson.db")

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

    df = pd.read_sql_query(sql_statement, conn)

    print(df.head())

    df["total"] = df["quantity"] * df["price"]

    print("\nDataFrame with total:")
    print(df.head())

    summary_df = df.groupby("product_id").agg({
    "line_item_id": "count",
    "total": "sum",
    "product_name": "first"
    })

    print("\nGrouped Summary:")
    print(summary_df.head())

    summary_df = summary_df.sort_values(by="product_name")

    print("\nSorted Summary:")
    print(summary_df.head())

    summary_df.to_csv("order_summary.csv")

    print("\norder_summary.csv created successfully.")

except sqlite3.Error as e:
    print("Database error:", e)

finally:
    if 'conn' in locals():
        conn.close()