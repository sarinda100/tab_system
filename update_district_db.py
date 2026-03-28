from app import get_db_connection

def setup_district_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS bulk_inventory")
    
    cursor.execute("""
    CREATE TABLE bulk_inventory (
        id INT AUTO_INCREMENT PRIMARY KEY,
        district VARCHAR(50) NOT NULL,
        item_name VARCHAR(100) NOT NULL,
        good_qty INT DEFAULT 0,
        defective_qty INT DEFAULT 0,
        remark TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY unique_item_district (district, item_name)
    )
    """)
    
    # 🔴 උඹේ දිස්ත්‍රික්ක 9
    districts = ['Anuradhapura', 'Badulla', 'Batticaloa', 'Colombo', 'Gampaha', 'Kegalle', 'Polonnaruwa', 'Ratnapura', 'Trincomalee']
    items = ['Stylus Pen', 'Rugged Pouch', 'Delivery Bag']
    
    sql = "INSERT INTO bulk_inventory (district, item_name, good_qty, defective_qty, remark) VALUES (%s, %s, 0, 0, '')"
    
    for d in districts:
        for i in items:
            cursor.execute(sql, (d, i))
            
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database updated with your 9 Districts successfully!")

if __name__ == '__main__':
    setup_district_inventory()