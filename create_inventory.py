from app import get_db_connection

def setup_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS bulk_inventory")

    cursor.execute("""
    CREATE TABLE bulk_inventory (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(100) NOT NULL,
        good_qty INT DEFAULT 0,
        defective_qty INT DEFAULT 0,
        remark TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """)

    sql = "INSERT INTO bulk_inventory (item_name, good_qty, defective_qty, remark) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, [
        ('Stylus Pen', 0, 0, ''),
        ('Rugged Pouch', 0, 0, ''),
        ('Delivery Bag', 0, 0, '')
    ])

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ bulk_inventory table created successfully!")

if __name__ == '__main__':
    setup_inventory()
