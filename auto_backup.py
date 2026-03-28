import os
import datetime

# 🔴 උඹේ Database විස්තර මෙතන දාපන්
DB_USER = 'root'
DB_PASS = 'tabcore123'  # මෙතනට MySQL පාස්වර්ඩ් එක දාපන් (උදා: 'Admin@123')
DB_NAME = 'tabcore_db'          # Database එකේ නම වෙනස් නම් හදපන්

# අද දිනය සහ වෙලාව අරගෙන ලස්සනට ෆයිල් නමක් හදනවා (උදා: backup_2026-03-24.sql)
date_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_path = f"/root/tab_system/backups/backup_{date_str}.sql"

# MySQL Dump එක (බැකප් එක) ගන්න කමාන්ඩ් එක
dump_cmd = f"mysqldump -u {DB_USER} -p'{DB_PASS}' {DB_NAME} > {backup_path}"

# කමාන්ඩ් එක රන් කරනවා
print("⏳ Starting database backup...")
os.system(dump_cmd)
print(f"✅ Backup Successful! Saved as: {backup_path}")
