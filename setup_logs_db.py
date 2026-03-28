from app import get_db_connection

def setup_audit_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # කවුද අප්ඩේට් කළේ කියලා බලන්න අලුත් ටේබල් එක හදනවා
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100),
        district VARCHAR(50),
        item_name VARCHAR(100),
        good_qty_changed INT,
        defective_qty_changed INT,
        remark TEXT,
        action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Audit Trail (inventory_logs) table created successfully!")

if __name__ == '__main__':
    setup_audit_table()
