from docx import Document
from docx.shared import Inches, Pt
import io
import json
import csv
import os
import re
import pymysql
import pymysql.cursors
import openpyxl  # ADDED: Excel Support
from openpyxl.styles import Font # ADDED: For Template styling
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, KeepTogether
from io import BytesIO
import pytz
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session, send_file

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()  # .env ෆයිල් එක කියවීම මෙතනින් පටන් ගන්නවා

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
@app.before_request
def check_maintenance_mode():
    if os.path.exists('update.txt'):
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>System Maintenance</title>
            <style>
                body { background: #080f1c; color: #ddeeff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; text-align: center; }
                .box { background: #0f2040; padding: 40px; border-radius: 16px; border: 1px solid #00d4ff; box-shadow: 0 10px 30px rgba(0,212,255,0.1); max-width: 400px;}
                h1 { color: #00d4ff; margin-bottom: 10px; font-size: 24px;}
                p { color: #4a6a8a; font-size: 14px; line-height: 1.6; }
                .loader { border: 4px solid #1a3050; border-top: 4px solid #00d4ff; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 20px auto; }
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        </head>
        <body>
            <div class="box">
                <div class="loader"></div>
                <h1>🛠️ System Updating</h1>
                <p>TABCORE is currently undergoing scheduled maintenance and upgrades. <br><br>Please check back in a few minutes. Your data is safe!</p>
            </div>
        </body>
        </html>
        """, 503

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30) 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )
class User(UserMixin):
    def __init__(self, id, username, name, role):
        self.id = id
        self.username = username
        self.name = name
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user: return User(user['id'], user['username'], user['name'], user['role'])
    return None

# --- STRICT BACKEND VALIDATIONS & EXCEL FIXES ---

def clean_imei(imei_str):
    if not imei_str: return ""
    imei_str = str(imei_str).strip().upper()
    if 'E+' in imei_str:
        try: return "{:.0f}".format(float(imei_str))
        except: return imei_str
    return re.sub(r'[^0-9]', '', imei_str)

def is_valid_imei(imei_str):
    if not imei_str: return False
    return bool(re.fullmatch(r'^\d{15}$', str(imei_str)))

def format_and_validate_sn(sn_str, brand=""):
    if not sn_str: return None
    clean_sn = str(sn_str).replace(" ", "").upper()
    if 'E+' in clean_sn:
        try: clean_sn = "{:.0f}".format(float(clean_sn))
        except: pass
    clean_sn = re.sub(r'[^A-Z0-9]', '', clean_sn)
    
    # --- BRAND SPECIFIC SERIAL NUMBER VALIDATION ---
    brand_lower = str(brand).lower()
    
    if 'samsung' in brand_lower:
        if len(clean_sn) == 11:
            return clean_sn
        return None
    elif 'lenovo' in brand_lower:
        if len(clean_sn) == 8:
            return clean_sn
        return None
    else:
        # වෙනත් බ්‍රෑන්ඩ් වලට සාමාන්‍ය විදියට
        if 8 <= len(clean_sn) <= 15:
            return clean_sn
        return None

# Ã°Å¸â€Â´ ADDED: Asset Number Validation (Strictly 5 digits)
def is_valid_asset_no(asset_str):
    if not asset_str: return True # Allow empty, but if provided, must be exactly 5 digits
    return bool(re.fullmatch(r'^\d{5}$', str(asset_str)))

# --- HELPERS ---

def log_device_history(tablet_id, action, performed_by, status_changed_to=None, notes=None):
    conn = get_db_connection(); cursor = conn.cursor()
    cursor.execute("INSERT INTO device_history (tablet_id, action, performed_by, status_changed_to, notes) VALUES (%s, %s, %s, %s, %s)", (tablet_id, action, performed_by, status_changed_to, notes))
    conn.commit(); conn.close()

def log_system_audit(action, performed_by, details=None):
    conn = get_db_connection(); cursor = conn.cursor()
    cursor.execute("INSERT INTO system_audit (action, performed_by, details) VALUES (%s, %s, %s)", (action, performed_by, details))
    conn.commit(); conn.close()

def safe_excel_text(val):
    if not val or val == '-': return '-'
    return f'="{val}"'

# --- DATABASE INIT ---

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE tablets ADD COLUMN pouch_status VARCHAR(50) DEFAULT 'Missing'")
        cursor.execute("ALTER TABLE tablets ADD COLUMN pen_status VARCHAR(50) DEFAULT 'Missing'")
        conn.commit()
    except: pass 

    cursor.execute("CREATE TABLE IF NOT EXISTS device_history (id INT AUTO_INCREMENT PRIMARY KEY, tablet_id INT NOT NULL, action VARCHAR(50) NOT NULL, performed_by VARCHAR(100) NOT NULL, status_changed_to VARCHAR(50), notes TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (tablet_id) REFERENCES tablets(id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS system_audit (id INT AUTO_INCREMENT PRIMARY KEY, action VARCHAR(100) NOT NULL, performed_by VARCHAR(100) NOT NULL, details TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("CREATE TABLE IF NOT EXISTS settings (id INT PRIMARY KEY, batch_target INT DEFAULT 540)")
    cursor.execute("CREATE TABLE IF NOT EXISTS district_targets (district_name VARCHAR(100) PRIMARY KEY, target_count INT DEFAULT 0)")
    
    valid_districts = ['Colombo', 'Gampaha', 'Batticaloa', 'Trincomalee', 'Anuradhapura', 'Polonnaruwa', 'Badulla', 'Ratnapura', 'Kegalle']
    format_strings = ','.join(['%s'] * len(valid_districts))
    cursor.execute(f"DELETE FROM district_targets WHERE district_name NOT IN ({format_strings})", valid_districts)

    cursor.execute("SELECT COUNT(*) as c FROM district_targets")
    if cursor.fetchone()['c'] == 0:
        default_districts = [('Colombo', 108), ('Gampaha', 77), ('Batticaloa', 54), ('Trincomalee', 40), ('Anuradhapura', 7), ('Polonnaruwa', 12), ('Badulla', 81), ('Ratnapura', 106), ('Kegalle', 58)]
        cursor.executemany("INSERT INTO district_targets (district_name, target_count) VALUES (%s, %s)", default_districts)

    cursor.execute("INSERT IGNORE INTO settings (id, batch_target) VALUES (1, 540)")
    conn.commit(); conn.close()

def create_default_admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO users (username, password, name, role) VALUES (%s, %s, %s, %s)", ('admin', hashed_pw, 'Sarinda', 'Admin'))
        conn.commit()
    conn.close()

# --- AUTH ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember') == 'yes' 

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'], user['name'], user['role'])
            login_user(user_obj, remember=remember_me)
            log_system_audit("User Login", user['name'], f"User '{username}' logged in.")
            return redirect(url_for('dashboard'))
        error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    log_system_audit("User Logout", current_user.name, f"User '{current_user.username}' logged out.")
    logout_user()
    return redirect(url_for('login'))

# --- DASHBOARD ---

@app.route('/')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM tablets WHERE is_deleted = 0")
    total = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as pending FROM tablets WHERE status IN ('Pending', 'Locked') AND is_deleted = 0")
    pending = cursor.fetchone()['pending']
    cursor.execute("SELECT COUNT(*) as inspected FROM tablets WHERE status IN ('Passed', 'Minor Issues', 'Defective') AND is_deleted = 0")
    inspected = cursor.fetchone()['inspected']
    cursor.execute("SELECT COUNT(*) as defective FROM tablets WHERE status = 'Defective' AND is_deleted = 0")
    defective = cursor.fetchone()['defective']
    cursor.execute("SELECT * FROM tablets WHERE is_deleted = 0 ORDER BY id DESC LIMIT 5")
    recent = cursor.fetchall()
    cursor.execute("SELECT batch_target FROM settings WHERE id = 1")
    res = cursor.fetchone(); batch_target = res['batch_target'] if res else 540
    pipeline_percentage = round((inspected / batch_target) * 100, 1) if batch_target > 0 else 0

    cursor.execute("SELECT COUNT(*) as c FROM tablets WHERE DATE(registered_at) = CURDATE()"); today_total = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(DISTINCT tablet_id) as c FROM device_history WHERE action = 'Inspected' AND DATE(timestamp) = CURDATE()"); today_inspected = cursor.fetchone()['c']

    cursor.execute("SELECT COUNT(*) as c FROM tablets WHERE LOWER(brand) LIKE '%samsung%'"); samsung_count = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) as c FROM tablets WHERE LOWER(brand) LIKE '%lenovo%'"); lenovo_count = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(*) as c FROM tablets WHERE LOWER(charger_status) LIKE '%missing%' OR LOWER(cable_status) LIKE '%missing%' OR LOWER(simpin_status) LIKE '%missing%'"); missing_acc = cursor.fetchone()['c']
    cursor.execute("SELECT COUNT(DISTINCT inspected_by) as c FROM tablets WHERE inspected_by IS NOT NULL AND inspected_by != ''"); active_techs = cursor.fetchone()['c']

    cursor.execute("SELECT u.name as inspected_by, COUNT(t.id) as count FROM users u LEFT JOIN tablets t ON u.name = t.inspected_by AND t.status IN ('Passed', 'Minor Issues', 'Defective') GROUP BY u.name")
    user_data = cursor.fetchall(); user_labels = [row['inspected_by'] for row in user_data]; user_counts = [row['count'] for row in user_data]

    cursor.execute("SELECT DATE(registered_at) as date_val, COUNT(id) as count FROM tablets WHERE status IN ('Passed', 'Minor Issues', 'Defective') GROUP BY DATE(registered_at) ORDER BY date_val DESC LIMIT 7")
    daily_data = cursor.fetchall(); daily_labels = [str(row['date_val']) for row in daily_data]; daily_counts = [row['count'] for row in daily_data]
    daily_labels.reverse(); daily_counts.reverse()

    cursor.execute("""
        SELECT dt.district_name, dt.target_count, COUNT(t.id) as inspected_count
        FROM district_targets dt LEFT JOIN tablets t ON dt.district_name = t.district AND t.status IN ('Passed', 'Minor Issues', 'Defective')
        WHERE dt.target_count > 0 GROUP BY dt.district_name, dt.target_count ORDER BY (dt.target_count - COUNT(t.id)) DESC
    """)
    district_progress_data = cursor.fetchall()

    district_stats = []
    for dp in district_progress_data:
        target = dp['target_count']; inspected_count = dp['inspected_count']; remaining = max(0, target - inspected_count); percentage = min(100, round((inspected_count / target) * 100)) if target > 0 else 0
        district_stats.append({'name': dp['district_name'], 'target': target, 'inspected': inspected_count, 'remaining': remaining, 'percentage': percentage})

    conn.close()
    return render_template('dashboard.html', total_tablets=total, pending=pending, inspected=inspected, defective=defective, today_total=today_total, today_inspected=today_inspected, samsung_count=samsung_count, lenovo_count=lenovo_count, missing_acc=missing_acc, active_techs=active_techs, batch_target=batch_target, pipeline_percentage=pipeline_percentage, recent_tablets=recent, user_labels=json.dumps(user_labels), user_counts=json.dumps(user_counts), daily_labels=json.dumps(daily_labels), daily_counts=json.dumps(daily_counts), district_stats=district_stats)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    error = None
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            # --- 1. BULK UPLOAD SECTION (Excel/CSV) ---
            file = request.files['file']
            
            if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
                return render_template('register.html', error="Please upload a valid CSV (.csv) or Excel (.xlsx) file.")
            
            try:
                rows_data = []
                
                if file.filename.endswith('.csv'):
                    content = file.stream.read()
                    try: decoded_content = content.decode('utf-8-sig')
                    except: decoded_content = content.decode('cp1252', errors='ignore')
                    csv_input = csv.DictReader(io.StringIO(decoded_content, newline=None))
                    for raw_row in csv_input:
                        row = {str(k).strip(): str(v).strip() for k, v in raw_row.items() if k}
                        rows_data.append(row)
                
                elif file.filename.endswith('.xlsx'):
                    wb = openpyxl.load_workbook(file, data_only=True)
                    ws = wb.active
                    sheet_rows = list(ws.rows)
                    if len(sheet_rows) > 0:
                        headers = [str(cell.value).strip() if cell.value is not None else '' for cell in sheet_rows[0]]
                        for sheet_row in sheet_rows[1:]:
                            row_dict = {}
                            for i, cell in enumerate(sheet_row):
                                if i < len(headers) and headers[i]:
                                    val = cell.value
                                    if val is None:
                                        val_str = ""
                                    elif isinstance(val, float) and val.is_integer():
                                        val_str = str(int(val))
                                    else:
                                        val_str = str(val)
                                    row_dict[headers[i]] = val_str.strip()
                            rows_data.append(row_dict)

                conn = get_db_connection()
                cursor = conn.cursor()
                success_count = 0
                duplicate_count = 0
                invalid_imei_count = 0
                invalid_sn_count = 0
                invalid_asset_count = 0
                
                for row in rows_data:
                    raw_sn = row.get('Serial Number', row.get('S/N', ''))
                    raw_imei = row.get('IMEI Number', row.get('IMEI', ''))
                    raw_asset = str(row.get('Asset No', row.get('Asset Number', ''))).strip() 
                    if raw_asset == 'None': raw_asset = ''
                    if not raw_sn or not raw_imei: continue 
                    
                    imei = clean_imei(raw_imei)
                    if not is_valid_imei(imei):
                        invalid_imei_count += 1
                        continue

                    sn = format_and_validate_sn(raw_sn, row.get('Brand', ''))
                    if not sn:
                        invalid_sn_count += 1
                        continue
                        
                    asset_no_clean = re.sub(r'[^0-9]', '', raw_asset)
                    if raw_asset and not is_valid_asset_no(asset_no_clean):
                        invalid_asset_count += 1
                        continue

                    cursor.execute("SELECT id FROM tablets WHERE serial_number = %s OR imei_number = %s", (sn, imei))
                    if cursor.fetchone():
                        duplicate_count += 1
                        continue 
                        
                    sql = "INSERT INTO tablets (district, brand, model, serial_number, asset_no, imei_number, charger_status, cable_status, simpin_status, pouch_status, pen_status, doc_status, registered_by, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'Bulk','Bulk',%s,%s,'Pending')" 
                    cursor.execute(sql, (row.get('District', ''), row.get('Brand', ''), row.get('Model', ''), sn, asset_no_clean, imei, row.get('Charger Status') or 'Good', row.get('Cable Status') or 'Good', row.get('Simpin Status') or 'Good', row.get('Doc Status') or 'Good', current_user.name))
                    tid = cursor.lastrowid
                    conn.commit()
                    log_device_history(tid, "Registered (Bulk)", current_user.name, "Pending", "Bulk registered via File Upload")
                    success_count += 1
                    
                conn.close()
                msg = f"Bulk Upload Complete: {success_count} added. {duplicate_count} duplicates skipped."
                if invalid_imei_count > 0: msg += f" {invalid_imei_count} skipped due to INVALID IMEI."
                if invalid_sn_count > 0: msg += f" {invalid_sn_count} skipped due to INVALID S/N."
                if invalid_asset_count > 0: msg += f" {invalid_asset_count} skipped due to INVALID ASSET NO."
                flash(msg, "success" if (invalid_imei_count == 0 and invalid_sn_count == 0 and invalid_asset_count == 0) else "error")
                return redirect(url_for('dashboard'))
            except Exception as e:
                error = f"Error processing Upload file: {str(e)}"

        else:
            # --- 2. MANUAL FORM SUBMISSION SECTION ---
            d = request.form
            raw_sn = d.get('serial_number', '').strip()
            raw_imei = d.get('imei_number', '').strip()
            asset_no = d.get('asset_no', '').strip() 
            
            if raw_sn and raw_imei:
                imei = clean_imei(raw_imei)
                if not is_valid_imei(imei):
                    return render_template('register.html', error="Validation Error: IMEI Number must be EXACTLY 15 digits! No letters or spaces allowed.")

                try:
                    brand = d.get('brand', '')
                    sn = format_and_validate_sn(raw_sn, brand)
                    
                    if not sn:
                        if 'samsung' in brand.lower():
                            error = "Validation Error: Samsung Serial Number must be EXACTLY 11 characters!"
                        elif 'lenovo' in brand.lower():
                            error = "Validation Error: Lenovo Serial Number must be EXACTLY 8 characters!"
                        else:
                            error = "Validation Error: Serial Number must be between 8-15 characters."
                    
                    elif asset_no and (len(asset_no) != 5 or not asset_no.isdigit()):
                        error = f"Error: Asset Number '{asset_no}' is invalid. It must be exactly 5 digits (e.g., 12345)!"
                    
                    else:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        
                        cursor.execute("""
                            SELECT serial_number, imei_number, asset_no 
                            FROM tablets 
                            WHERE serial_number = %s OR imei_number = %s OR (asset_no = %s AND asset_no != '')
                        """, (sn, imei, asset_no))
                        
                        existing_device = cursor.fetchone()

                        if existing_device:
                            if existing_device['serial_number'] == sn:
                                error = f"Error: Serial Number '{sn}' is already registered in the system!"
                            elif existing_device['imei_number'] == imei:
                                error = f"Error: IMEI Number '{imei}' is already registered!"
                            elif asset_no and existing_device['asset_no'] == asset_no:
                                error = f"Error: Asset Number '{asset_no}' is already assigned to another device!"
                        else:
                            sql = "INSERT INTO tablets (district, brand, model, serial_number, asset_no, imei_number, charger_status, cable_status, simpin_status, pouch_status, pen_status, doc_status, registered_by, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'Bulk','Bulk',%s,%s,'Pending')" 
                            cursor.execute(sql, (d['district'], brand, d.get('model',''), sn, asset_no, imei, d['charger_status'], d['cable_status'], d['simpin_status'], d['doc_status'], current_user.name))
                            tid = cursor.lastrowid
                            conn.commit()
                            log_device_history(tid, "Registered", current_user.name, "Pending", "Manual Registration")
                            flash(f"Device {sn} registered successfully!", "success")
                            return redirect(url_for('dashboard'))
                except Exception as e: 
                    error = f"Database Error: {str(e)}"
                finally: 
                    if 'conn' in locals() and conn.open:
                        conn.close()

    return render_template('register.html', error=error)

# --- INSPECTION QUEUE ---

@app.route('/inspection')
@login_required
def inspection_queue():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tablets SET status = 'Pending' WHERE status = 'Locked' AND registered_at <= DATE_SUB(NOW(), INTERVAL 2 DAY)")
    conn.commit()
    cursor.execute("SELECT * FROM tablets WHERE status IN ('Pending', 'Locked') AND is_deleted = 0 ORDER BY id ASC")
    tablets = cursor.fetchall()
    conn.close()
    return render_template('queue.html', tablets=tablets)

@app.route('/inspect/<int:id>', methods=['GET', 'POST'])
@login_required
def inspect_device(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, inspected_by FROM tablets WHERE id = %s", (id,))
    tablet_check = cursor.fetchone()
    if not tablet_check:
        conn.close()
        return redirect(url_for('inspection_queue'))
    if tablet_check['status'] == 'Locked' and tablet_check['inspected_by'] != current_user.name:
        conn.close()
        flash(f"Access Denied! This device is currently being inspected by {tablet_check['inspected_by']}.", "error")
        return redirect(url_for('inspection_queue'))
    if request.method == 'POST':
        verdict = request.form.get('verdict')
        battery_drain_time = request.form.get('battery_drain_time', '-')
        checklist = {k: v for k, v in request.form.items() if k not in ['verdict', 'battery_drain_time']}
        cursor.execute("UPDATE tablets SET status = %s, inspected_by = %s, inspection_data = %s, battery_drain_time = %s WHERE id = %s", (verdict, current_user.name, json.dumps(checklist), battery_drain_time, id))
        conn.commit()
        log_device_history(id, "Inspected", current_user.name, verdict, f"Verdict: {verdict}")
        conn.close()
        return redirect(url_for('inspection_queue'))
    if tablet_check['status'] == 'Pending':
        cursor.execute("UPDATE tablets SET status = 'Locked', inspected_by = %s WHERE id = %s", (current_user.name, id))
        conn.commit()
        log_device_history(id, "Locked for Inspection", current_user.name, "Locked", "Technician opened for inspection")
    cursor.execute("SELECT * FROM tablets WHERE id = %s", (id,))
    tablet = cursor.fetchone()
    conn.close()
    return render_template('inspect.html', tablet=tablet)

@app.route('/verified')
@login_required
def verified_records():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # පේජ් ගාණ හදන්න මුළු ගණන ගන්නවා
    cursor.execute("SELECT COUNT(*) as total FROM tablets WHERE status IN ('Passed', 'Minor Issues') AND is_deleted = 0")
    total_records = cursor.fetchone()['total']
    total_pages = (total_records + per_page - 1) // per_page
    if total_pages == 0: total_pages = 1

    # ටැබ්ලට් 50ක් විතරක් ගන්නවා
    cursor.execute("SELECT * FROM tablets WHERE status IN ('Passed', 'Minor Issues') AND is_deleted = 0 ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    tablets = cursor.fetchall()
    conn.close()
    
    return render_template('records.html', tablets=tablets, title="Verified Records", color="var(--green)", page=page, total_pages=total_pages)

@app.route('/defects')
@login_required
def defect_records():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # මුළු Defect ගාණ අරන් පේජ් ගාණ හදනවා
    cursor.execute("SELECT COUNT(*) as total FROM tablets WHERE status = 'Defective' AND is_deleted = 0")
    total_records = cursor.fetchone()['total']
    total_pages = (total_records + per_page - 1) // per_page
    if total_pages == 0: total_pages = 1

    # ටැබ්ලට් 50න් 50 ගන්නවා
    cursor.execute("SELECT * FROM tablets WHERE status = 'Defective' AND is_deleted = 0 ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    tablets = cursor.fetchall()
    conn.close()
    
    # 🔴 මෙතන අන්තිමට page=page, total_pages=total_pages දාලා තියෙනවා!
    return render_template('records.html', tablets=tablets, title="Issues / Defects", color="var(--red)", page=page, total_pages=total_pages)

@app.route('/accessories')
@login_required
def accessories_log():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # උඩ තියෙන චාට් එකට ඕන Accessories ගණන් ටික
    cursor.execute("SELECT COUNT(*) as chargers FROM tablets WHERE LOWER(charger_status) != 'missing' AND is_deleted = 0")
    chargers = cursor.fetchone()['chargers']
    cursor.execute("SELECT COUNT(*) as cables FROM tablets WHERE LOWER(cable_status) != 'missing' AND is_deleted = 0")
    cables = cursor.fetchone()['cables']
    cursor.execute("SELECT COUNT(*) as simpins FROM tablets WHERE LOWER(simpin_status) != 'missing' AND is_deleted = 0")
    simpins = cursor.fetchone()['simpins']
    cursor.execute("SELECT COUNT(*) as pouches FROM tablets WHERE LOWER(pouch_status) != 'missing' AND is_deleted = 0")
    pouches = cursor.fetchone()['pouches']
    cursor.execute("SELECT COUNT(*) as pens FROM tablets WHERE LOWER(pen_status) != 'missing' AND is_deleted = 0")
    pens = cursor.fetchone()['pens']
    
    # පේජ් ගාණ හදන්න මුළු ගණන ගන්නවා
    cursor.execute("SELECT COUNT(*) as total FROM tablets WHERE is_deleted = 0")
    total_records = cursor.fetchone()['total']
    total_pages = (total_records + per_page - 1) // per_page
    if total_pages == 0: total_pages = 1
    
    # ටැබ්ලට් 50ක් විතරක් ගන්නවා
    cursor.execute("SELECT id, serial_number, asset_no, brand, district, charger_status, cable_status, simpin_status, pouch_status, pen_status, registered_by FROM tablets WHERE is_deleted = 0 ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    tablets = cursor.fetchall()    
    conn.close()
    
    return render_template('accessories.html', tablets=tablets, chargers=chargers, cables=cables, simpins=simpins, pouches=pouches, pens=pens, page=page, total_pages=total_pages)
# --- EXPORT ROUTES ---

@app.route('/export_accessories')
@login_required
def export_accessories():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, district, brand, serial_number, asset_no, charger_status, cable_status, simpin_status, pouch_status, pen_status, doc_status, registered_by FROM tablets ORDER BY id ASC")
    tablets = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Tablet ID', 'District', 'Brand', 'Serial Number', 'Asset No', 'Charger', 'Data Cable', 'SIM Pin', 'Rugged Pouch', 'Stylus Pen', 'Delivery Note', 'Registered By'])
    
    for t in tablets:
        safe_sn = safe_excel_text(t.get('serial_number'))
        writer.writerow([
            f"T-{t['id']}", t.get('district','-'), t.get('brand','-'), safe_sn, t.get('asset_no', '-'),
            t.get('charger_status','-'), t.get('cable_status','-'), t.get('simpin_status','-'),
            t.get('pouch_status','-'), t.get('pen_status','-'), t.get('doc_status','-'), t.get('registered_by','-')
        ])
        
    log_system_audit("Accessories Export", current_user.name, "Exported accessories detailed report to CSV.")
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=Tabcore_Accessories_Report.csv"})

@app.route('/export')
@login_required
def export_data():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tablets ORDER BY id ASC")
    tablets = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    base_headers = ['ID', 'Dist', 'Brand', 'Model', 'S/N', 'Asset No', 'IMEI', 'Status', 'Reg.By', 'Insp.By', 'Bat. Drain']
    item_names = ['Display', 'Touch', 'Battery', 'Cam', 'WiFi', 'BT', 'GPS', 'Speaker', 'Mic', 'Port', 'Pwr', 'SIM', 'Notes']
    item_keys = ['display', 'touch', 'battery', 'cameras', 'wifi', 'bt', 'gps', 'speaker', 'mic', 'charging', 'p_btn', 'sim']
    writer.writerow(base_headers + item_names)
    
    for t in tablets:
        safe_sn = safe_excel_text(t.get('serial_number'))
        safe_imei = safe_excel_text(t.get('imei_number'))

        row = [f"T-{t['id']}", t.get('district','-'), t.get('brand','-'), t.get('model','-'), safe_sn, t.get('asset_no', '-'), safe_imei, t.get('status','-'), t.get('registered_by','-'), t.get('inspected_by','-'), t.get('battery_drain_time', '-')]
        details = {}
        if t.get('inspection_data'):
            try: details = json.loads(t['inspection_data'])
            except: pass
        
        for key in item_keys:
            raw_val = details.get(key, '-')
            val = str(raw_val).lower() if raw_val != '-' else '-'
            if val == 'pass': val = 'P'
            elif val == 'minor' or val == 'partial': val = 'M'
            elif val == 'fail': val = 'F'
            else: val = raw_val
            row.append(val)
            
        row.append(details.get('inspector_notes', '-'))
        writer.writerow(row)
        
    log_system_audit("Data Export", current_user.name, "Exported full tablet database to CSV.")
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=Tabcore_Full_Report.csv"})

@app.route('/export_filtered', methods=['GET'])
@login_required
def export_filtered():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    district = request.args.get('district', '')
    brand = request.args.get('brand', '')
    status = request.args.get('status', '')
    inspector = request.args.get('inspector', '')
    
    query = "SELECT * FROM tablets WHERE status NOT IN ('Pending', 'Locked') AND is_deleted = 0"
    params = []
    filename_parts = ["Tabcore", "Filtered"]
    
    if district and district != 'All Districts':
        query += " AND district = %s"
        params.append(district)
        filename_parts.append(district)
    if brand and brand != 'All Brands':
        query += " AND brand = %s"
        params.append(brand)
        filename_parts.append(brand)
    if status and status != 'All Statuses':
        query += " AND status = %s"
        params.append(status)
        filename_parts.append(status)
    if inspector and inspector != 'All Inspectors':
        query += " AND inspected_by = %s"
        params.append(inspector)
        filename_parts.append(inspector.replace(" ", ""))
        
    query += " ORDER BY id ASC"
    cursor.execute(query, params)
    tablets = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    base_headers = ['ID', 'District', 'Brand', 'Model', 'Serial Number', 'Asset No', 'IMEI', 'Status', 'Registered By', 'Inspected By', 'Battery Drain Time']
    item_names = ['Display', 'Touch', 'Battery', 'Cameras', 'WiFi', 'Bluetooth', 'GPS', 'Speaker', 'Mic', 'Charging Port', 'Power/Vol Buttons', 'SIM Tray', 'Inspector Notes']
    item_keys = ['display', 'touch', 'battery', 'cameras', 'wifi', 'bt', 'gps', 'speaker', 'mic', 'charging', 'p_btn', 'sim']
    writer.writerow(base_headers + item_names)
    
    for t in tablets:
        safe_sn = safe_excel_text(t.get('serial_number'))
        safe_imei = safe_excel_text(t.get('imei_number'))

        row = [f"T-{t['id']}", t.get('district','-'), t.get('brand','-'), t.get('model','-'), safe_sn, t.get('asset_no', '-'), safe_imei, t.get('status','-'), t.get('registered_by','-'), t.get('inspected_by','-'), t.get('battery_drain_time', '-')]
        details = {}
        if t.get('inspection_data'):
            try: details = json.loads(t['inspection_data'])
            except: pass
            
        for key in item_keys:
            raw_val = details.get(key, '-')
            val = str(raw_val).lower() if raw_val != '-' else '-'
            if val == 'pass': val = 'Pass'
            elif val == 'minor' or val == 'partial': val = 'Minor Issue'
            elif val == 'fail': val = 'Fail'
            else: val = raw_val
            row.append(val)
            
        row.append(details.get('inspector_notes', '-'))
        writer.writerow(row)
        
    filename = "_".join(filename_parts) + ".csv"
    log_system_audit("Filtered Data Export", current_user.name, f"Exported filtered report.")
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename={filename}"})

@app.route('/export_sinhala_word')
def export_sinhala_word():
    # පේජ් එකෙන් එවන Filters ටික ගන්නවා (GET method එක නිසා request.args පාවිච්චි කරනවා)
    target_district = request.args.get('district', 'All Districts')
    target_brand = request.args.get('brand', 'All Brands')
    target_status = request.args.get('status', 'All Statuses')

    conn = get_db_connection()
    # Pymysql වල dictionary විදියට දත්ත ගන්න මෙන්න මේකයි පාවිච්චි කරන්නේ 👇
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = "SELECT * FROM tablets WHERE 1=1"
    params = []
    
    if target_district != 'All Districts':
        query += " AND district = %s"
        params.append(target_district)
    if target_brand != 'All Brands':
        query += " AND brand = %s"
        params.append(target_brand)
    if target_status != 'All Statuses':
        query += " AND status = %s"
        params.append(target_status)
        
    cursor.execute(query, tuple(params))
    tablets = cursor.fetchall()
    conn.close()

    defective_tablets = []
    good_count = 0
    for t in tablets:
        issues = []
        # DB එකේ තියෙන Status එක අනුව චෙක් කරනවා
        if t.get('status') == 'Defective' or t.get('status') == 'Fail':
            issues.append("දෘඩාංග දෝෂ සහිතයි (අලුත්වැඩියා කළ යුතුය)")
        
        # Accessories චෙක් කිරීම (ඔයාගේ DB fields වලට අනුව)
        # මෙතන t['details'] කියන්නේ JSON එකක් නම් ඒක Dictionary එකක් විදියට ගන්නවා
        det = t.get('details', {})
        if isinstance(det, str): # සමහරවිට DB එකෙන් එන්නේ String එකක් විදියට නම්
            import json
            try: det = json.loads(det)
            except: det = {}

        if det.get('battery') == 'fail': issues.append("බැටරි දෝෂ සහිතයි")
        if det.get('display') == 'fail': issues.append("තිරය (Screen) දෝෂ සහිතයි")

        if issues:
            defective_tablets.append({
                'asset': t.get('asset_no', '-'), 
                'sn': t.get('serial_number', '-'), 
                'issue': " | ".join(issues)
            })
        else:
            good_count += 1

    # Word Document එක සෑදීම
    doc = Document()
    doc.add_heading('දිස්ත්‍රික්ක අතර හුවමාරු කරන ලද ටැබ්ලට් පරිගණක වල තත්ත්ව පරීක්ෂණ වාර්තාව', level=1)
    doc.add_paragraph(f"දිස්ත්‍රික්කය: {target_district}")
    doc.add_paragraph(f"පරීක්ෂා කරන ලද මුළු ටැබ්ලට් සංඛ්‍යාව: {len(tablets)}")
    doc.add_paragraph("\nපහත වගුවේ දැක්වෙන ටැබ්ලට් පරිගණක වල දෝෂ පවතින බව නිරීක්ෂණය විය:")

    if defective_tablets:
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Asset No'
        hdr_cells[1].text = 'Serial Number'
        hdr_cells[2].text = 'පවතින දෝෂය'
        
        for dt in defective_tablets:
            row_cells = table.add_row().cells
            row_cells[0].text = str(dt['asset'])
            row_cells[1].text = str(dt['sn'])
            row_cells[2].text = dt['issue']
    else:
        doc.add_paragraph("දෝෂ සහිත ටැබ්ලට් කිසිවක් වාර්තා වී නොමැත.")

    doc.add_paragraph(f"\nඒ අනුව, ඉහත දෝෂ සහිත ටැබ්ලට් හැර ඉතිරි ටැබ්ලට් පරිගණක {good_count} ක ප්‍රමාණය ක්ෂේත්‍ර කටයුතු සඳහා යොදාගත හැකි බව නිර්දේශ කරමි.")
    doc.add_paragraph("\n........................\nපරීක්ෂා කළ නිලධාරියා")

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name='Quality_Inspection_Report.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
@app.route('/export_single/<int:id>')
@login_required
def export_single(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tablets WHERE id = %s", (id,))
    t = cursor.fetchone()
    conn.close()
    if not t: return redirect(url_for('dashboard'))
    
    output = io.StringIO()
    writer = csv.writer(output)
    base_headers = ['ID', 'Dist', 'Brand', 'Model', 'S/N', 'Asset No', 'IMEI', 'Status', 'Reg.By', 'Insp.By']
    item_names = ['Display', 'Touch', 'Battery', 'Cam', 'WiFi', 'BT', 'GPS', 'Speaker', 'Mic', 'Port', 'Pwr', 'SIM', 'Notes']
    item_keys = ['display', 'touch', 'battery', 'cameras', 'wifi', 'bt', 'gps', 'speaker', 'mic', 'charging', 'p_btn', 'sim']
    writer.writerow(base_headers + item_names)
    
    safe_sn = safe_excel_text(t.get('serial_number'))
    safe_imei = safe_excel_text(t.get('imei_number'))

    row = [f"T-{t['id']}", t.get('district','-'), t.get('brand','-'), t.get('model','-'), safe_sn, t.get('asset_no', '-'), safe_imei, t.get('status','-'), t.get('registered_by','-'), t.get('inspected_by','-'), t.get('battery_drain_time', '-')]
    details = {}
    if t.get('inspection_data'):
        try: details = json.loads(t['inspection_data'])
        except: pass
        
    for key in item_keys:
        raw_val = details.get(key, '-')
        val = str(raw_val).lower() if raw_val != '-' else '-'
        if val == 'pass': val = 'P'
        elif val == 'minor' or val == 'partial': val = 'M'
        elif val == 'fail': val = 'F'
        else: val = raw_val
        row.append(val)
        
    row.append(details.get('inspector_notes', '-'))
    writer.writerow(row)
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f"attachment;filename=Tabcore_T-{id}_Report.csv"})

# Ã°Å¸â€Â´ Ã Â¶â€¦Ã Â¶Â½Ã Â·â€Ã Â¶Â­Ã Â·Å  Smart Excel Template Download Ã Â¶â€˜Ã Â¶Å¡ Ã°Å¸â€Â´
@app.route('/download_template')
@login_required
def download_template():
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Bulk_Upload"
        headers = ['District', 'Brand', 'Model', 'Serial Number', 'IMEI Number', 'Asset No', 'Charger Status', 'Cable Status', 'Simpin Status', 'Pouch Status', 'Pen Status', 'Doc Status']
        ws.append(headers)
        
        # Header Ã Â¶â€˜Ã Â¶Å¡ Ã Â¶Â½Ã Â·Æ’Ã Â·Å Ã Â·Æ’Ã Â¶Â±Ã Â¶Â§ Bold Ã Â¶Å¡Ã Â¶Â»Ã Â¶Â±Ã Â·Å Ã Â¶Â±
        for cell in ws[1]:
            cell.font = Font(bold=True)
            
        # Ã°Å¸â€Â´ Ã Â¶Â´Ã Â¶Â§Ã Â·Å Ã Â¶Â§Ã Â¶Â¸ Ã Â·â‚¬Ã Â·ÂÃ Â¶Â¯Ã Â¶Å“Ã Â¶Â­Ã Â·Å  Ã Â¶Å¡Ã Â·â€˜Ã Â¶Â½Ã Â·Å Ã Â¶Â½: Ã Â¶Â¸Ã Â·â€Ã Â·â€¦Ã Â·â€ E Column Ã Â¶â€˜Ã Â¶Å¡Ã Â¶Â¸ (IMEI) 'Text' Ã Â¶Å¡Ã Â¶Â»Ã Â¶Â½Ã Â·Â Ã Â·Æ’Ã Â·Å¡Ã Â·â‚¬Ã Â·Å  Ã Â¶Å¡Ã Â¶Â»Ã Â¶Â±Ã Â·â‚¬Ã Â·Â
        for i in range(1, 1000):
            ws[f"E{i}"].number_format = '@'

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return Response(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment;filename=Tabcore_Bulk_Template.xlsx"})
    except:
        # Ã Â¶ÂºÃ Â¶Â¸Ã Â·Å  Ã Â·â€žÃ Â·â„¢Ã Â¶ÂºÃ Â¶Å¡Ã Â·â€™Ã Â¶Â±Ã Â·Å  openpyxl Ã Â·â‚¬Ã Â·ÂÃ Â¶Â© Ã Â¶Å¡Ã Â·â€¦Ã Â·Å¡ Ã Â¶Â±Ã Â·ÂÃ Â¶Â­Ã Â·Å Ã Â¶Â±Ã Â¶Â¸Ã Â·Å  Ã Â¶Â´Ã Â¶Â»Ã Â¶Â« CSV Ã Â¶â€˜Ã Â¶Å¡ Ã Â¶Â¯Ã Â·â„¢Ã Â¶Â±Ã Â·â‚¬Ã Â·Â
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['District', 'Brand', 'Model', 'Serial Number', 'IMEI Number', 'Asset No', 'Charger Status', 'Cable Status', 'Simpin Status', 'Pouch Status', 'Pen Status', 'Doc Status'])
        return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=Tabcore_Bulk_Template.csv"})

# --- ADMIN ROUTES & OTHERS ---

@app.route('/officers', methods=['GET', 'POST'])
@login_required
def officers():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form.get('password'))
        try:
            cursor.execute("INSERT INTO users (username, password, name, role) VALUES (%s, %s, %s, %s)", (request.form.get('username'), hashed_pw, request.form.get('name'), request.form.get('role')))
            conn.commit()
            log_system_audit("User Created", current_user.name, f"Created new user '{request.form.get('username')}' with role '{request.form.get('role')}'.")
        except: pass 
        return redirect(url_for('officers'))
    cursor.execute("SELECT * FROM users ORDER BY id ASC")
    users_list = cursor.fetchall()
    conn.close()
    return render_template('officers.html', users=users_list)

@app.route('/delete_officer/<int:id>', methods=['POST'])
@login_required
def delete_officer(id):
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
    deleted_user = cursor.fetchone()
    cursor.execute("DELETE FROM users WHERE id = %s AND id != %s", (id, current_user.id))
    conn.commit()
    if deleted_user:
        log_system_audit("User Deleted", current_user.name, f"Deleted user '{deleted_user['username']}'.")
    conn.close()
    return redirect(url_for('officers'))

@app.route('/reset_password/<int:id>', methods=['POST'])
@login_required
def reset_password(id):
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    
    new_password = request.form.get('new_password')
    if not new_password:
        flash("Password cannot be empty.", "error")
        return redirect(url_for('officers'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
    target_user = cursor.fetchone()
    
    if target_user:
        hashed_pw = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_pw, id))
        conn.commit()
        log_system_audit("Password Reset", current_user.name, f"Admin reset password for user '{target_user['username']}'.")
        flash(f"Password for {target_user['username']} reset successfully!", "success")
    else:
        flash("User not found.", "error")

    conn.close()
    return redirect(url_for('officers'))

@app.route('/force_unlock/<int:id>', methods=['POST'])
@login_required
def force_unlock(id):
    if current_user.role != 'Admin': return redirect(url_for('inspection_queue'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tablets SET status = 'Pending', inspected_by = NULL WHERE id = %s", (id,))
    conn.commit()
    log_device_history(id, "Force Unlocked", current_user.name, "Pending", "Admin force unlocked the device")
    log_system_audit("Device Force Unlocked", current_user.name, f"Admin unlocked tablet T-{id}.")
    conn.close()
    return redirect(url_for('inspection_queue'))

@app.route('/undo_inspection/<int:id>', methods=['POST'])
@login_required
def undo_inspection(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT status, inspected_by FROM tablets WHERE id = %s", (id,))
    tablet = cursor.fetchone()
    
    if not tablet:
        conn.close()
        return redirect(url_for('dashboard'))
        
    # Security Check: Admin ට ඕන එකක් පුළුවන්. User ට පුළුවන් එයා Inspect කරපු ඒවා විතරයි.
    if current_user.role != 'Admin' and current_user.name != tablet['inspected_by']:
        flash("🚫 Access Denied! You can only undo your own inspections.", "error")
        conn.close()
        return redirect(request.referrer or url_for('dashboard'))
        
    cursor.execute("UPDATE tablets SET status = 'Pending', inspected_by = NULL, inspection_data = NULL, battery_drain_time = '-' WHERE id = %s", (id,))
    conn.commit()
    
    log_device_history(id, "Inspection Undone", current_user.name, "Pending", "User reversed the inspection decision. Moved back to Queue.")
    conn.close()
    
    flash(f"✅ Device T-{id} inspection undone! Back in the Inspection Queue.", "success")
    return redirect(url_for('inspection_queue'))

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    if not query: return jsonify([])
    conn = get_db_connection()
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute("SELECT id, brand, model, serial_number, asset_no, imei_number, status, inspected_by FROM tablets WHERE serial_number LIKE %s OR imei_number LIKE %s OR asset_no LIKE %s OR CONCAT('T-', id) LIKE %s LIMIT 5", (search_term, search_term, search_term, search_term))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

@app.route('/reports', methods=['GET'])
@login_required
def reports():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    district = request.args.get('district', '')
    brand = request.args.get('brand', '')
    status = request.args.get('status', '')
    inspector = request.args.get('inspector', '')
    
    # --- අලුතින් එකතු කළ Pagination Settings ---
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    
    cursor.execute("SELECT name FROM users ORDER BY name ASC")
    users = cursor.fetchall()
    
    # Base Query එක (Filters ටිකට අදාලව)
    base_query = " FROM tablets WHERE status NOT IN ('Pending', 'Locked') AND is_deleted = 0"
    params = []
    
    if district and district != 'All Districts':
        base_query += " AND district = %s"
        params.append(district)
    if brand and brand != 'All Brands':
        base_query += " AND brand = %s"
        params.append(brand)
    if status and status != 'All Statuses':
        base_query += " AND status = %s"
        params.append(status)
    if inspector and inspector != 'All Inspectors':
        base_query += " AND inspected_by = %s"
        params.append(inspector)
        
    # සම්පූර්ණ ටැබ්ලට් ගණන හොයාගන්නවා පේජ් ගාණ හදන්න (Total Records for Pagination)
    count_query = "SELECT COUNT(*) as total" + base_query
    cursor.execute(count_query, params)
    total_records = cursor.fetchone()['total']
    
    # මුළු පිටු ගණන ගණනය කිරීම
    total_pages = (total_records + per_page - 1) // per_page
    if total_pages == 0: 
        total_pages = 1
        
    # මේ පිටුවට අදාල ටැබ්ලට් 50 විතරක් ගන්නවා (LIMIT & OFFSET)
    query = "SELECT *" + base_query + " ORDER BY id DESC LIMIT %s OFFSET %s"
    paginated_params = params + [per_page, offset]
    
    cursor.execute(query, paginated_params)
    tablets = cursor.fetchall()
    
    for t in tablets:
        t['details'] = {}
        if t['inspection_data']:
            try: t['details'] = json.loads(t['inspection_data'])
            except: pass
    conn.close()
    
    # Template එකට අලුත් parameters යවනවා (page, total_pages, total_records)
    return render_template('reports.html', tablets=tablets, req=request.args, users=users, page=page, total_pages=total_pages, total_records=total_records)

@app.route('/history')
@login_required
def history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            DATE_FORMAT(registered_at, '%Y-%m') as batch_month,
            COUNT(*) as total,
            SUM(CASE WHEN status IN ('Passed', 'Minor Issues', 'Defective') THEN 1 ELSE 0 END) as inspected,
            SUM(CASE WHEN status = 'Minor Issues' THEN 1 ELSE 0 END) as minor_issues,
            SUM(CASE WHEN status = 'Defective' THEN 1 ELSE 0 END) as defective,
            SUM(CASE WHEN status = 'Passed' THEN 1 ELSE 0 END) as dispatched
        FROM tablets
        GROUP BY batch_month
        ORDER BY batch_month DESC
    """)
    batches = cursor.fetchall()
    conn.close()
    return render_template('history.html', batches=batches)

@app.route('/tablet/<int:id>')
@login_required
def tablet_timeline(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tablets WHERE id = %s", (id,))
    tablet = cursor.fetchone()
    
    if not tablet:
        conn.close()
        return redirect(url_for('dashboard'))
        
    # ?? ??????? ?????? ?? ????? (Inspection Data ?? HTML ??? ??????? ??????? ?????? ??? ??)
    if tablet['inspection_data']:
        try:
            tablet['details'] = json.loads(tablet['inspection_data'])
        except:
            tablet['details'] = {}
    else:
        tablet['details'] = {}
        
    cursor.execute("SELECT * FROM device_history WHERE tablet_id = %s ORDER BY timestamp DESC", (id,))
    history_logs = cursor.fetchall()
    conn.close()
    
    return render_template('timeline.html', tablet=tablet, history=history_logs)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        for key, val in request.form.items():
            if key.startswith('target_'):
                dist_name = key.replace('target_', '')
                try:
                    t_val = int(val)
                    cursor.execute("UPDATE district_targets SET target_count = %s WHERE district_name = %s", (t_val, dist_name))
                except:
                    pass
        
        new_target = request.form.get('batch_target')
        if new_target:
            cursor.execute("UPDATE settings SET batch_target = %s WHERE id = 1", (new_target,))
            
        conn.commit()
        log_system_audit("Settings Updated", current_user.name, "Admin updated System Settings & District Targets.")
        flash("Settings and District Targets updated successfully!", "success")
        return redirect(url_for('settings'))

    cursor.execute("SELECT batch_target FROM settings WHERE id = 1")
    res = cursor.fetchone()
    target = res['batch_target'] if res else 540
    
    cursor.execute("SELECT * FROM district_targets ORDER BY district_name ASC")
    district_targets = cursor.fetchall()
    
    conn.close()
    return render_template('settings.html', batch_target=target, district_targets=district_targets)

@app.route('/audit')
@login_required
def audit(): 
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_audit ORDER BY timestamp DESC LIMIT 100")
    logs = cursor.fetchall()
    conn.close()
    return render_template('audit.html', logs=logs)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tablet(id):
    if current_user.role != 'Admin': 
        return redirect(url_for('dashboard'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        d = request.form
        raw_sn = d.get('serial_number', '').strip()
        raw_imei = d.get('imei_number', '').strip()
        asset_no = d.get('asset_no', '').strip()
        
        imei = clean_imei(raw_imei)
        if not is_valid_imei(imei):
            flash("⛔ Update Failed: IMEI Number must be EXACTLY 15 digits!", "error")
            return redirect(url_for('edit_tablet', id=id))

        sn = format_and_validate_sn(raw_sn)
        if not sn:
            flash("⛔ Update Failed: Serial Number must be at least 8 alphanumeric characters.", "error")
            return redirect(url_for('edit_tablet', id=id))

        # 🔴 ADDED: Validate Asset No in Edit Submission
        if asset_no and not is_valid_asset_no(asset_no):
            flash("⛔ Update Failed: Asset Number must be EXACTLY 5 digits! Only numbers allowed.", "error")
            return redirect(url_for('edit_tablet', id=id))

        cursor.execute("SELECT id FROM tablets WHERE (serial_number = %s OR imei_number = %s) AND id != %s", (sn, imei, id))
        if cursor.fetchone():
            flash(f"⛔ Serial Number '{sn}' or IMEI '{imei}' already exists in another record!", "error")
            return redirect(url_for('edit_tablet', id=id))
            
        district = d.get('district')
        brand = d.get('brand')
        model = d.get('model', '')
        charger = d.get('charger_status')
        cable = d.get('cable_status')
        simpin = d.get('simpin_status')
        doc = d.get('doc_status')
        battery_drain_time = d.get('battery_drain_time', '-')
       
        verdict = d.get('verdict')
        inspection_data_json = None
        if verdict:
            # 🔴 අර pen, pouch දෙක checklist එකෙනුත් අයින් කළා
            checklist = {k: v for k, v in d.items() if k not in ['district', 'brand', 'model', 'serial_number', 'asset_no', 'imei_number', 'charger_status', 'cable_status', 'simpin_status', 'doc_status', 'verdict', 'battery_drain_time']}
            inspection_data_json = json.dumps(checklist)
            
            sql = """UPDATE tablets SET 
                     district=%s, brand=%s, model=%s, serial_number=%s, asset_no=%s, imei_number=%s, 
                     charger_status=%s, cable_status=%s, simpin_status=%s, doc_status=%s,
                     status=%s, inspection_data=%s, battery_drain_time=%s 
                     WHERE id=%s"""
            cursor.execute(sql, (district, brand, model, sn, asset_no, imei, charger, cable, simpin, doc, verdict, inspection_data_json, battery_drain_time, id))
        else:
            sql = """UPDATE tablets SET 
                     district=%s, brand=%s, model=%s, serial_number=%s, asset_no=%s, imei_number=%s, 
                     charger_status=%s, cable_status=%s, simpin_status=%s, doc_status=%s, battery_drain_time=%s 
                     WHERE id=%s"""
            cursor.execute(sql, (district, brand, model, sn, asset_no, imei, charger, cable, simpin, doc, battery_drain_time, id))
            
        conn.commit()
        
        log_device_history(id, "Data Edited", current_user.name, verdict, "Admin updated device details and inspection data.")
        log_system_audit("Device Edited", current_user.name, f"Admin updated data for tablet T-{id}.")
        conn.close()
        
        flash("✅ Device data updated successfully!", "success")
        return redirect(url_for('tablet_timeline', id=id))
        
    cursor.execute("SELECT * FROM tablets WHERE id = %s", (id,))
    tablet = cursor.fetchone()
    conn.close()
    if not tablet: return redirect(url_for('dashboard'))
    
    if tablet['inspection_data']:
        try:
            tablet['details'] = json.loads(tablet['inspection_data'])
        except:
            tablet['details'] = {}
    else:
        tablet['details'] = {}
        
    return render_template('edit.html', tablet=tablet)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_tablet(id):
    if current_user.role != 'Admin': 
        return redirect(url_for('dashboard'))
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tablets SET is_deleted = 1 WHERE id = %s", (id,))
        conn.commit()
        log_system_audit("Device Deleted", current_user.name, f"Admin deleted tablet T-{id} from the system permanently.")
        flash(f"Ã°Å¸â€”â€˜Ã¯Â¸Â Device T-{id} deleted successfully.", "success")
    except Exception as e:
        flash(f"Ã¢ÂÅ’ Error deleting device: {str(e)}", "error")
    finally:
        conn.close()
        
    return redirect(request.referrer or url_for('reports'))

@app.route('/nuke_ghosts')
@login_required
def nuke_ghosts():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("DELETE FROM device_history WHERE tablet_id IN (1, 2, 3);")
        cursor.execute("DELETE FROM tablets WHERE id IN (1, 2, 3);")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        flash("Ã°Å¸â€™Â¥ Ghost records (T-1, T-2, T-3) nuked successfully!", "success")
    except Exception as e:
        flash(f"Ã¢ÂÅ’ Error nuking ghosts: {str(e)}", "error")
    finally:
        conn.close()
    return redirect(url_for('dashboard'))

@app.route('/performance')
@login_required
def performance():
    if current_user.role != 'Admin': 
        return redirect(url_for('dashboard'))
        
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, role FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT registered_by, COUNT(id) as count FROM tablets GROUP BY registered_by")
    reg_data = {row['registered_by']: row['count'] for row in cursor.fetchall() if row['registered_by']}

    cursor.execute("""
        SELECT inspected_by,
               COUNT(id) as total_inspected,
               SUM(CASE WHEN status = 'Passed' THEN 1 ELSE 0 END) as passed,
               SUM(CASE WHEN status = 'Minor Issues' THEN 1 ELSE 0 END) as minor,
               SUM(CASE WHEN status = 'Defective' THEN 1 ELSE 0 END) as defective
        FROM tablets
        WHERE inspected_by IS NOT NULL AND inspected_by != ''
        GROUP BY inspected_by
    """)
    insp_data = {row['inspected_by']: row for row in cursor.fetchall()}
    conn.close()

    perf_data = []
    
    max_reg = 0
    max_defects = 0

    for u in users:
        name = u['name']
        r_count = reg_data.get(name, 0)
        i_info = insp_data.get(name, {'total_inspected':0, 'passed':0, 'minor':0, 'defective':0})
        
        defects = int(i_info['defective'] or 0)
        
        if r_count > max_reg: max_reg = r_count
        if defects > max_defects: max_defects = defects

        total_activity = r_count + int(i_info['total_inspected'] or 0)
        
        perf_data.append({
            'name': name,
            'role': u['role'],
            'registered': r_count,
            'inspected': int(i_info['total_inspected'] or 0),
            'passed': int(i_info['passed'] or 0),
            'minor': int(i_info['minor'] or 0),
            'defective': defects,
            'total_activity': total_activity,
            'badges': [] 
        })

    for user in perf_data:
        if user['registered'] == max_reg and max_reg > 0:
            user['badges'].append('Speedster Ã¢Å¡Â¡')
        if user['defective'] == max_defects and max_defects > 0:
            user['badges'].append('Eagle Eye Ã°Å¸Â¦â€¦')

    perf_data.sort(key=lambda x: x['total_activity'], reverse=True)

    return render_template('performance.html', perf_data=perf_data)

@app.route('/export_performance_summary')
@login_required
def export_performance_summary():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, role FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT registered_by, COUNT(id) as count FROM tablets GROUP BY registered_by")
    reg_data = {row['registered_by']: row['count'] for row in cursor.fetchall() if row['registered_by']}
    cursor.execute("""
        SELECT inspected_by, COUNT(id) as total_inspected,
               SUM(CASE WHEN status = 'Passed' THEN 1 ELSE 0 END) as passed,
               SUM(CASE WHEN status = 'Minor Issues' THEN 1 ELSE 0 END) as minor,
               SUM(CASE WHEN status = 'Defective' THEN 1 ELSE 0 END) as defective
        FROM tablets WHERE inspected_by IS NOT NULL AND inspected_by != '' GROUP BY inspected_by
    """)
    insp_data = {row['inspected_by']: row for row in cursor.fetchall()}
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Staff Name', 'Role', 'Registered Count', 'Inspected Count', 'Passed', 'Minor Issues', 'Defective', 'Total Activity'])
    
    for u in users:
        n = u['name']
        r_count = reg_data.get(n, 0)
        i = insp_data.get(n, {'total_inspected':0, 'passed':0, 'minor':0, 'defective':0})
        total = r_count + int(i['total_inspected'] or 0)
        writer.writerow([n, u['role'], r_count, i['total_inspected'], i['passed'], i['minor'], i['defective'], total])
    
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=Tabcore_Staff_Performance.csv"})

@app.route('/generate_handover_pdf', methods=['GET'])
@login_required
def generate_handover_pdf():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        from datetime import datetime
        import io

        district = request.args.get('district', ''); brand = request.args.get('brand', ''); status = request.args.get('status', '')
        conn = get_db_connection(); cursor = conn.cursor()
        query = "SELECT id, serial_number, asset_no, imei_number, brand, district, status, charger_status, cable_status, simpin_status, pouch_status, pen_status FROM tablets WHERE status != 'Pending'"
        params = []
        if district and district != 'All Districts': query += " AND district = %s"; params.append(district)
        if brand and brand != 'All Brands': query += " AND brand = %s"; params.append(brand)
        if status and status != 'All Statuses': query += " AND status = %s"; params.append(status)
        query += " ORDER BY id ASC"; cursor.execute(query, params); tablets = cursor.fetchall(); conn.close()

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=100, bottomMargin=50)
        elements = []; styles = getSampleStyleSheet()

        dist_name = district.upper() if district and district != 'All Districts' else 'ALL DISTRICTS'
        header_text = f"ICT DIVISION | STORES HANDOVER REPORT - {dist_name}"
        
        def draw_header_footer(canvas, doc):
            canvas.saveState()
            canvas.setFillColor(colors.HexColor("#1a2a6c"))
            canvas.rect(0, doc.pagesize[1] - 75, doc.pagesize[0], 75, fill=1, stroke=0)
            canvas.setFillColor(colors.white)
            canvas.setFont("Helvetica-Bold", 16)
            canvas.drawCentredString(doc.pagesize[0] / 2, doc.pagesize[1] - 35, "DEPARTMENT OF CENSUS AND STATISTICS")
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawCentredString(doc.pagesize[0] / 2, doc.pagesize[1] - 55, header_text)
            
            canvas.setFillColor(colors.black)
            canvas.setFont("Helvetica-Oblique", 8)
            canvas.drawString(30, 20, f"Generated via TabCore System | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            canvas.drawRightString(doc.pagesize[0] - 30, 20, f"Page {doc.page}")
            canvas.restoreState()

        total = len(tablets)
        passed = sum(1 for t in tablets if t['status'] == 'Passed')
        defective = sum(1 for t in tablets if t['status'] == 'Defective')
        locked = sum(1 for t in tablets if t['status'] == 'Locked')
        minor = sum(1 for t in tablets if t['status'] == 'Minor Issues')

        summary_data = [
            ["INSPECTION SUMMARY:"],
            [f"Total Handed Over: {total}   |   Defective: {defective}   |   Locked: {locked}   |   Minor Issues: {minor}   |   Passed: {passed}"]
        ]
        summary_table = Table(summary_data, colWidths=[535])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0f0f0")),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 15))

        data = [['T-ID', 'Asset No', 'District', 'Brand', 'Serial No', 'IMEI Number', 'Status', 'Accessories']]
        for t in tablets:
            mis = []; dam = []
            # 🔴 BULLETPROOF ACCESSORY CHECK (UPDATED)
            acc_keys = [('charger_status', 'Chg'), ('cable_status', 'Cbl'), ('simpin_status', 'Pin')]
            for k, label in acc_keys:
                val = str(t.get(k, '')).lower().strip()
                if 'missing' in val: mis.append(label)
                elif 'damage' in val: dam.append(label)

            if not mis and not dam: acc_text = "Full Set"
            else:
                parts = []
                if mis: parts.append("No: " + ",".join(mis))
                if dam: parts.append("Dmg: " + ",".join(dam))
                acc_text = " | ".join(parts)

            data.append([f"T-{t['id']}", t.get('asset_no') or '-', t.get('district') or '-', t.get('brand') or '-', t['serial_number'], t.get('imei_number') or '-', t['status'], acc_text])

        table = Table(data, colWidths=[35, 45, 55, 50, 85, 90, 50, 125], repeatRows=1)
        t_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a2a6c")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9f9f9")]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ])
        table.setStyle(t_style)
        elements.append(table)
        elements.append(Spacer(1, 10))# 🔴 පරණ Legend එක වෙනුවට මේක දාපන්
        elements.append(Paragraph("<font size=8 color='red'>* Accessories Legend: Chg=Charger, Cbl=Cable, Pin=SIM Pin</font>", styles['Normal']))

        signature_block = KeepTogether([
            Spacer(1, 30),
            Paragraph("<b>Handed Over By (ICT):</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Received By (Stores):</b>", styles['Normal']),
            Spacer(1, 15),
            Paragraph("Name: ........................................... &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Name: ...........................................", styles['Normal']),
            Spacer(1, 15),
            Paragraph("Sign & Date: ................................ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Sign & Date: ................................", styles['Normal'])
        ])
        elements.append(signature_block)

        doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
        buffer.seek(0)
        return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": f"attachment;filename=Handover_Report.pdf"})
    except Exception as e: return f"Error: {str(e)}"

@app.route('/generate_full_inspection_pdf', methods=['GET'])
@login_required
def generate_full_inspection_pdf():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        from datetime import datetime
        import json, io

        district = request.args.get('district', '')
        brand    = request.args.get('brand', '')
        status   = request.args.get('status', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM tablets WHERE status NOT IN ('Pending', 'Locked')"
        params = []
        if district and district != 'All Districts': query += " AND district = %s"; params.append(district)
        if brand    and brand    != 'All Brands':    query += " AND brand = %s";    params.append(brand)
        if status   and status   != 'All Statuses':  query += " AND status = %s";   params.append(status)
        query += " ORDER BY id ASC"
        cursor.execute(query, params)
        tablets = cursor.fetchall()
        conn.close()

        if not tablets:
            return "No inspected tablets found for this filter!"

        buffer   = io.BytesIO()
        doc      = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                                     rightMargin=20, leftMargin=20,
                                     topMargin=90, bottomMargin=40)
        elements = []
        styles   = getSampleStyleSheet()

        dist_name   = district.upper() if district and district != 'All Districts' else 'ALL DISTRICTS'
        report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ── Header / Footer ──────────────────────────────────────────────
        def draw_header_footer(canvas_obj, doc_obj):
            canvas_obj.saveState()
            W = doc_obj.pagesize[0]
            H = doc_obj.pagesize[1]

            # Blue header bar
            canvas_obj.setFillColor(colors.HexColor("#1a2a6c"))
            canvas_obj.rect(0, H - 75, W, 75, fill=1, stroke=0)

            canvas_obj.setFillColor(colors.white)
            canvas_obj.setFont("Helvetica-Bold", 15)
            canvas_obj.drawCentredString(W/2, H - 32, "DEPARTMENT OF CENSUS AND STATISTICS")
            canvas_obj.setFont("Helvetica-Bold", 9)
            
            part_name = "PART 1: IDENTITY & SUMMARY" if doc_obj.page % 2 != 0 else "PART 2: HARDWARE & REMARKS"
            canvas_obj.drawCentredString(W/2, H - 50, f"FULL INSPECTION REPORT — {dist_name}  |  {part_name}")
            
            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(colors.HexColor("#aaccee"))
            canvas_obj.drawCentredString(W/2, H - 65, f"Generated: {report_date}")

            # Footer
            canvas_obj.setFillColor(colors.black)
            canvas_obj.setFont("Helvetica-Oblique", 7)
            canvas_obj.drawString(20, 15, "Generated via TabCore System  |  Dept. of Census & Statistics")
            canvas_obj.drawRightString(W - 20, 15, f"Page {doc_obj.page}")
            canvas_obj.restoreState()

        # ── Summary dashboard ─────────────────────────────────────────────
        total    = len(tablets)
        passed   = sum(1 for t in tablets if t['status'] == 'Passed')
        defective= sum(1 for t in tablets if t['status'] == 'Defective')
        minor    = sum(1 for t in tablets if t['status'] == 'Minor Issues')

        dash = Table(
            [["DISTRICT STATUS DASHBOARD:"],
             [f"Total: {total}   |   Passed: {passed}   |   Minor Issues: {minor}   |   Defective: {defective}"]],
            colWidths=[800])
        dash.setStyle(TableStyle([
            ('BACKGROUND',   (0,0),(-1,-1), colors.HexColor("#f0f4ff")),
            ('BOX',          (0,0),(-1,-1), 1, colors.HexColor("#1a2a6c")),
            ('FONTNAME',     (0,0),(-1,0),  'Helvetica-Bold'),
            ('FONTNAME',     (0,1),(-1,1),  'Helvetica'),
            ('FONTSIZE',     (0,0),(-1,-1), 9),
            ('TOPPADDING',   (0,0),(-1,-1), 6),
            ('BOTTOMPADDING',(0,0),(-1,-1), 6),
            ('LEFTPADDING',  (0,0),(-1,-1), 10),
        ]))
        
        elements.append(dash)
        elements.append(Spacer(1, 12))

        # ── Chunk Data Logic (20 Items per Page Set) ──────────────────────
        CHUNK_SIZE = 20
        for i in range(0, len(tablets), CHUNK_SIZE):
            batch = tablets[i:i + CHUNK_SIZE]

            # ════════════════════════════════════════════════════════════════
            #  PAGE 1 — Identity + Summary 
            # ════════════════════════════════════════════════════════════════
            p1_header = ['T-ID', 'Asset No', 'Serial Number', 'IMEI Number',
                         'Brand', 'District', 'Inspector', 'Insp. Date',
                         'Battery Drain', 'Status']

            p1_data  = [p1_header]
            p1_cmds  = [
                ('BACKGROUND',   (0,0),(-1,0),  colors.HexColor("#1a2a6c")),
                ('TEXTCOLOR',    (0,0),(-1,0),  colors.whitesmoke),
                ('FONTNAME',     (0,0),(-1,0),  'Helvetica-Bold'),
                ('FONTSIZE',     (0,0),(-1,0),  8),
                ('FONTSIZE',     (0,1),(-1,-1), 7.5),
                ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
                ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
                ('GRID',         (0,0),(-1,-1), 0.5, colors.grey),
                ('TOPPADDING',   (0,0),(-1,-1), 5),
                ('BOTTOMPADDING',(0,0),(-1,-1), 5),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#f7f9ff")]),
            ]

            for row_idx, t in enumerate(batch, 1):
                inspector = t.get('inspected_by') or '-'
                insp_date = '-'
                if t.get('inspection_data'):
                    raw_date = t.get('registered_at')
                    if raw_date:
                        try: insp_date = str(raw_date)[:10]
                        except: insp_date = '-'

                drain_raw = str(t.get('battery_drain_time') or '-').strip()
                if drain_raw != '-':
                    try:
                        mins = int(''.join(filter(str.isdigit, drain_raw)))
                        if   mins > 60: rating = f"{mins} min ✓"
                        elif mins >= 45: rating = f"{mins} min ~"
                        else:            rating = f"{mins} min ✗"
                    except:
                        rating = drain_raw
                else:
                    rating = 'Not Tested'

                st = t['status']
                if   st == 'Passed':       p1_cmds.append(('TEXTCOLOR',(9,row_idx),(9,row_idx), colors.HexColor("#15803d")))
                elif st == 'Defective':    p1_cmds.append(('TEXTCOLOR',(9,row_idx),(9,row_idx), colors.HexColor("#b91c1c")))
                elif st == 'Minor Issues': p1_cmds.append(('TEXTCOLOR',(9,row_idx),(9,row_idx), colors.HexColor("#b45309")))

                p1_data.append([
                    f"T-{t['id']}", t.get('asset_no') or '-', t['serial_number'],
                    t.get('imei_number') or '-', t.get('brand') or '-', t.get('district') or '-',
                    inspector, insp_date, rating, st
                ])

            # පළවෙනි පිටුවේ පළල (Widths) හරියටම 800px වෙන්න හැදුවා
            p1_table = Table(p1_data, colWidths=[45, 70, 110, 120, 65, 75, 95, 75, 75, 70], repeatRows=1)
            p1_table.setStyle(TableStyle(p1_cmds))
            elements.append(p1_table)

            # Legend for Page 1
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("<font size=7.5 color='#555555'>* Battery Drain Legend: ✓ = Good (>60 min) &nbsp; ~ = Moderate (45–60 min) &nbsp; ✗ = Poor (&lt;45 min)</font>", styles['Normal']))

            elements.append(PageBreak())

            # ════════════════════════════════════════════════════════════════
            #  PAGE 2 — Hardware Details
            # ════════════════════════════════════════════════════════════════
            p2_header = ['T-ID','S/N','Dsp','Tch','Bat','Cam','WiF','BT',
                         'GPS','Spk','Mic','Pwr','SIM','Prt','Accessories','Notes']
            p2_data   = [p2_header]
            p2_cmds   = [
                ('BACKGROUND',   (0,0),(-1,0),  colors.HexColor("#1a2a6c")),
                ('TEXTCOLOR',    (0,0),(-1,0),  colors.whitesmoke),
                ('FONTNAME',     (0,0),(-1,0),  'Helvetica-Bold'),
                ('FONTSIZE',     (0,0),(-1,0),  7.5),
                ('FONTSIZE',     (0,1),(-1,-1), 6.5),
                ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
                ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
                ('GRID',         (0,0),(-1,-1), 0.5, colors.grey),
                ('TOPPADDING',   (0,0),(-1,-1), 4),
                ('BOTTOMPADDING',(0,0),(-1,-1), 4),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#f7f9ff")]),
            ]

            # 🔴 පරණ Database Keys ටික ආයෙත් දැම්මා (එතකොට P/M/F හරියට වැටෙනවා)
            hw_keys = ['display','touch','battery','cameras','wifi','bt',
                       'gps','speaker','mic','p_btn','sim','charging']

            for row_idx, t in enumerate(batch, 1):
                det = {}
                if t.get('inspection_data'):
                    try: det = json.loads(t['inspection_data'])
                    except: pass

                hw_vals = []
                for col_idx, k in enumerate(hw_keys, 2):
                    v    = str(det.get(k, '-')).lower()
                    char = ('P' if v == 'pass' else
                            'M' if v in ['minor','partial'] else
                            'F' if v == 'fail' else '-')
                    hw_vals.append(char)

                    bg = (colors.HexColor("#d4edda") if char == 'P' else
                          colors.HexColor("#fff3cd") if char == 'M' else
                          colors.HexColor("#f8d7da") if char == 'F' else
                          colors.white)
                    p2_cmds.append(('BACKGROUND',(col_idx, row_idx),(col_idx, row_idx), bg))

                mis, dam = [], []
                for key, lbl in [('charger_status','Chg'),('cable_status','Cbl'),('simpin_status','Pin')]:
                    val = str(t.get(key,'')).lower().strip()
                    if 'missing' in val: mis.append(lbl)
                    elif 'damage' in val: dam.append(lbl)

                if not mis and not dam:
                    acc = "Full Set"
                else:
                    parts = []
                    if mis: parts.append("No:" + ",".join(mis))
                    if dam: parts.append("Dmg:" + ",".join(dam))
                    acc = " | ".join(parts)
                    p2_cmds.append(('BACKGROUND',(14,row_idx),(14,row_idx), colors.HexColor("#fff5f5")))

                notes = str(det.get('inspector_notes','') or '-')[:50] 

                p2_data.append([f"T-{t['id']}", t['serial_number'][:13]] + hw_vals + [acc, notes])

            # දෙවෙනි පිටුවේ පළලත් (Widths) හරියටම 800px වෙන්න හැදුවා (Full page)
            p2_table = Table(p2_data, colWidths=[45, 100, 30,30,30,30,30,30,30,30,30,30,30,30, 140, 155], repeatRows=1)
            p2_table.setStyle(TableStyle(p2_cmds))
            elements.append(p2_table)

            # Legend for Page 2 (12 Checklist එකේ විස්තරේ සහ අනිත් ඒවා)
            elements.append(Spacer(1, 8))
            legend_text = (
                "<font size=7.5 color='#555555'>"
                "<b>Hardware Guide:</b> Dsp=Display | Tch=Touch | Bat=Battery | Cam=Camera | WiF=Wi-Fi | BT=Bluetooth | "
                "GPS=GPS | Spk=Speaker | Mic=Mic | Pwr=Power Btn | SIM=SIM Slot | Prt=Charging Port<br/>"
                "<b>Verdict:</b> P=Pass &nbsp; M=Minor Issue &nbsp; F=Fail &nbsp;|&nbsp; "
                "<b>Accessories:</b> Chg=Charger, Cbl=Cable, Pin=SIM Pin"
                "</font>"
            )
            elements.append(Paragraph(legend_text, styles['Normal']))

            if i + CHUNK_SIZE < len(tablets):
                elements.append(PageBreak())

        # ── Build PDF ─────────────────────────────────────────────────
        doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
        buffer.seek(0)
        return Response(buffer, mimetype='application/pdf',
                        headers={"Content-Disposition": f"attachment;filename={dist_name}_Inspection_Report.pdf"})

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/generate_defect_report_pdf', methods=['GET'])
@login_required
def generate_defect_report_pdf():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        from datetime import datetime
        import json, io

        district = request.args.get('district', '')
        brand    = request.args.get('brand', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # මෙතනින් Passed, Pending, Locked ඔක්කොම අයින් කරලා, අවුල් තියෙන ඒවා විතරක් ගන්නවා
        query = "SELECT * FROM tablets WHERE status IN ('Minor Issues', 'Defective')"
        params = []
        if district and district != 'All Districts': query += " AND district = %s"; params.append(district)
        if brand    and brand    != 'All Brands':    query += " AND brand = %s";    params.append(brand)
        query += " ORDER BY id ASC"
        
        cursor.execute(query, params)
        tablets = cursor.fetchall()
        conn.close()

        if not tablets:
            return "No defective or missing items found for this filter! (All Passed)"

        buffer   = io.BytesIO()
        doc      = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                                     rightMargin=20, leftMargin=20,
                                     topMargin=90, bottomMargin=40)
        elements = []
        styles   = getSampleStyleSheet()

        dist_name   = district.upper() if district and district != 'All Districts' else 'ALL DISTRICTS'
        report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ── Header / Footer ──────────────────────────────────────────────
        def draw_header_footer(canvas_obj, doc_obj):
            canvas_obj.saveState()
            W = doc_obj.pagesize[0]
            H = doc_obj.pagesize[1]

            canvas_obj.setFillColor(colors.HexColor("#b91c1c")) # මේකේ Header එක රතු පාටින් එන්නේ (Action Report නිසා)
            canvas_obj.rect(0, H - 75, W, 75, fill=1, stroke=0)

            canvas_obj.setFillColor(colors.white)
            canvas_obj.setFont("Helvetica-Bold", 15)
            canvas_obj.drawCentredString(W/2, H - 32, "DEPARTMENT OF CENSUS AND STATISTICS")
            canvas_obj.setFont("Helvetica-Bold", 9)
            canvas_obj.drawCentredString(W/2, H - 50, f"DEFECT & SHORTAGE ACTION REPORT — {dist_name}")
            
            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(colors.HexColor("#fecaca"))
            canvas_obj.drawCentredString(W/2, H - 65, f"Generated: {report_date}")

            canvas_obj.setFillColor(colors.black)
            canvas_obj.setFont("Helvetica-Oblique", 7)
            canvas_obj.drawString(20, 15, "Generated via TabCore System  |  Dept. of Census & Statistics")
            canvas_obj.drawRightString(W - 20, 15, f"Page {doc_obj.page}")
            canvas_obj.restoreState()

        # ── Data Extraction Logic ─────────────────────────────────────────────
        def get_defect_details(t):
            defects = []
            det = {}
            if t.get('inspection_data'):
                try: det = json.loads(t['inspection_data'])
                except: pass
            
            # Hardware චෙක් කරනවා
            hw_map = {'display':'Display', 'touch':'Touch', 'battery':'Battery', 
                      'cameras':'Camera', 'wifi':'Wi-Fi', 'bt':'Bluetooth', 
                      'gps':'GPS', 'speaker':'Speaker', 'mic':'Mic', 
                      'p_btn':'Power Btn', 'sim':'SIM Slot', 'charging':'Charging Port'}
            
            for k, lbl in hw_map.items():
                val = str(det.get(k, '')).lower()
                if val in ['fail', 'minor', 'partial']:
                    defects.append(f"{lbl} ({val.title()})")
                    
            # Accessories චෙක් කරනවා
            for k, lbl in [('charger_status','Charger'), ('cable_status','Cable'), ('simpin_status','SIM Pin')]:
                val = str(t.get(k, '')).lower().strip()
                if 'missing' in val: defects.append(f"{lbl} Missing")
                elif 'damage' in val: defects.append(f"{lbl} Damaged")
            
            return ", ".join(defects) if defects else "Status Issue (Check Notes)"

        # ── Chunk Data Logic (20 Items per Page) ──────────────────────
        CHUNK_SIZE = 20
        # අලුතින් දාපු කෑල්ල: අකුරු පේළි කැඩෙන්න Paragraph Style එකක් හදනවා
        style_defect = styles["Normal"]
        style_defect.fontSize = 8
        style_defect.leading = 10  # පේළි අතර පරතරය

        for i in range(0, len(tablets), CHUNK_SIZE):
            batch = tablets[i:i + CHUNK_SIZE]

            header = ['T-ID', 'S/N', 'Asset', 'Dist.', 'Status', 'Defects & Shortages']
            data  = [header]
            cmds  = [
                ('BACKGROUND',   (0,0),(-1,0),  colors.HexColor("#b91c1c")), # Header red
                ('TEXTCOLOR',    (0,0),(-1,0),  colors.whitesmoke),
                ('FONTNAME',     (0,0),(-1,0),  'Helvetica-Bold'),
                ('FONTSIZE',     (0,0),(-1,0),  9),
                ('FONTSIZE',     (0,1),(-1,-1), 8),
                ('ALIGN',        (0,0),(4,-1),  'CENTER'), # මුල් ටික මැදට
                ('ALIGN',        (5,0),(5,-1),  'LEFT'),   # විස්තරේ වම් පැත්තට
                ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
                ('GRID',         (0,0),(-1,-1), 0.5, colors.grey),
                ('TOPPADDING',   (0,0),(-1,-1), 6),
                ('BOTTOMPADDING',(0,0),(-1,-1), 6),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor("#fff5f5")]),
            ]

            for row_idx, t in enumerate(batch, 1):
                st = t['status']
                if st == 'Defective':    cmds.append(('TEXTCOLOR',(4,row_idx),(4,row_idx), colors.HexColor("#b91c1c")))
                elif st == 'Minor Issues': cmds.append(('TEXTCOLOR',(4,row_idx),(4,row_idx), colors.HexColor("#b45309")))

                defect_str = get_defect_details(t)
# අලුතින් දාපු කෑල්ල: String එක Paragraph එකක් කරනවා
                p_defect = Paragraph(defect_str, style_defect)


                data.append([
                    f"T-{t['id']}", 
                    t['serial_number'], 
                    t.get('asset_no') or '-', 
                    t.get('district') or '-', 
                    st,
                    p_defect
                ])

            # Total width = 800
            table = Table(data, colWidths=[40, 90, 45, 60, 60, 505], repeatRows=1)
            table.setStyle(TableStyle(cmds))
            elements.append(table)

            if i + CHUNK_SIZE < len(tablets):
                elements.append(PageBreak())

        doc.build(elements, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
        buffer.seek(0)
        return Response(buffer, mimetype='application/pdf',
                        headers={"Content-Disposition": f"attachment;filename={dist_name}_Defect_Action_Report.pdf"})

    except Exception as e:
        return f"Error: {str(e)}"

# TRASH BIN LOGIC (SOFT DELETE MANAGEMENT)
# ==========================================

@app.route('/trash')
@login_required
def trash():
    if current_user.role != 'Admin':
        flash('Permission denied. Admin access required.', 'error')
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # is_deleted = 1 ????? ??????? ??? ?????? Trash ??? ???? ????
    cursor.execute("SELECT * FROM tablets WHERE is_deleted = 1 ORDER BY id DESC")
    deleted_tablets = cursor.fetchall()
    conn.close()
    
    return render_template('trash.html', tablets=deleted_tablets)

@app.route('/restore/<int:id>', methods=['POST'])
@login_required
def restore_tablet(id):
    if current_user.role != 'Admin':
        return redirect(url_for('dashboard'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # is_deleted = 0 ???? ????? ????????? (Restore)
        cursor.execute("UPDATE tablets SET is_deleted = 0 WHERE id = %s", (id,))
        conn.commit()
        
        # Audit Log ??? ?????? (??? standard ????)
        log_system_audit("Device Restored", current_user.name, f"Admin restored tablet T-{id} from Trash Bin.")
        
        flash(f"? Device T-{id} restored successfully! It is back in the system.", "success")
    except Exception as e:
        flash(f"? Error restoring device: {str(e)}", "error")
    finally:
        if 'conn' in locals():
            conn.close()

    return redirect(url_for('trash'))

# ... (උඹේ අනිත් කෝඩ් ටික උඩින් තියෙනවා) ...

# 🔴 අර මම දුන්න Factory Reset කෝඩ් කෑල්ල මෙතනින් පේස්ට් කරපන් 🔴
@app.route('/factory_reset_db')
@login_required
def factory_reset_db():
    if current_user.role != 'Admin':
        flash("Access Denied! Only Admins can reset the database.", "error")
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. ලොක් එක තාවකාලිකව අරිනවා
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # 2. ටේබල් ඔක්කොම හිස් කරනවා
        cursor.execute("TRUNCATE TABLE tablets;")
        cursor.execute("TRUNCATE TABLE device_history;")
        cursor.execute("TRUNCATE TABLE inventory_logs;")
        
        # 3. දිස්ත්‍රික්ක වල බඩු ගාණ ආයේ බිංදුවට කරනවා
        cursor.execute("UPDATE bulk_inventory SET good_qty=0, defective_qty=0, remark='';")
        
        # 4. ලොක් එක ආයේ දානවා
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        conn.commit()
        conn.close()
        
        flash("🔥 System Factory Reset Successful! All data cleared and reset to zero.", "success")
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f"Error resetting database: {str(e)}", "error")
        return redirect(url_for('dashboard'))

# 🔴 app.py එකේ අන්තිම පේළි ටික 🔴

# ==========================================
# 📦 BULK INVENTORY MANAGEMENT (DISTRICT-WISE)
# ==========================================

@app.route('/inventory')
@login_required
def inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    # සම්පූර්ණ ලැයිස්තුව දිස්ත්‍රික්ක අනුව
    cursor.execute("SELECT * FROM bulk_inventory ORDER BY district ASC, item_name ASC")
    inventory_data = cursor.fetchall()
    
    # මුළු ලංකාවේම එකතුව (Top Cards වලට)
    cursor.execute("SELECT item_name, SUM(good_qty) as total_good FROM bulk_inventory GROUP BY item_name")
    totals = cursor.fetchall()
    conn.close()
    return render_template('inventory.html', inventory_data=inventory_data, totals=totals)

@app.route('/update_inventory', methods=['POST'])
@login_required
def update_inventory():
    district = request.form['district']
    item_name = request.form['item_name']
    good_qty_change = int(request.form['good_qty'])
    defective_qty_change = int(request.form['defective_qty'])
    remark = request.form.get('remark', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 🔴 1. ඍණ තොග (Negative Stock) චෙක් කිරීම (Good සහ Defective දෙකටම)
    cursor.execute("SELECT good_qty, defective_qty FROM bulk_inventory WHERE district=%s AND item_name=%s", (district, item_name))
    current_stock = cursor.fetchone()

    if current_stock:
        new_good = current_stock['good_qty'] + good_qty_change
        new_defective = current_stock['defective_qty'] + defective_qty_change

        # Good Qty එක 0 ට වඩා අඩු වෙනවද බලනවා
        if new_good < 0:
            conn.close()
            flash(f"❌ Error: Cannot reduce GOOD stock below zero! Current good stock is {current_stock['good_qty']}.", "danger")
            return redirect(url_for('inventory'))
            
        # Defective Qty එක 0 ට වඩා අඩු වෙනවද බලනවා
        if new_defective < 0:
            conn.close()
            flash(f"❌ Error: Cannot reduce DEFECTIVE stock below zero! Current defective stock is {current_stock['defective_qty']}.", "danger")
            return redirect(url_for('inventory'))

    # 🟢 2. තොගය අප්ඩේට් කිරීම (සෑම දෙයක්ම හරි නම්)
    cursor.execute("""
        UPDATE bulk_inventory 
        SET good_qty = good_qty + %s, 
            defective_qty = defective_qty + %s, 
            remark = %s 
        WHERE district=%s AND item_name=%s
    """, (good_qty_change, defective_qty_change, remark, district, item_name))

    # 🔴 3. Audit Trail එකට රෙකෝඩ් එකක් දානවා
    cursor.execute("""
        INSERT INTO inventory_logs (username, district, item_name, good_qty_changed, defective_qty_changed, remark)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (current_user.username, district, item_name, good_qty_change, defective_qty_change, remark))

    conn.commit()
    conn.close()
    
    flash(f"✅ {district} District - Stock updated successfully! (Logged)", "success")
    return redirect(url_for('inventory'))

@app.route('/export_inventory_pdf', methods=['POST'])
@login_required
def export_inventory_pdf():
    district = request.form.get('district')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bulk_inventory WHERE district=%s ORDER BY item_name ASC", (district,))
    inv_data = cursor.fetchall()
    conn.close()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=15, spaceAfter=5)
    elements.append(Paragraph("TABCORE ENTERPRISE SYSTEM", title_style))
    # 🔴 PDF එකේ Title එකට දිස්ත්‍රික්කේ නම වැටෙනවා
    elements.append(Paragraph(f"INVENTORY HANDOVER DOCUMENT - {district.upper()} DISTRICT", title_style))
    elements.append(Spacer(1, 20))

    tz = pytz.timezone('Asia/Colombo')
    current_time = datetime.now(tz).strftime('%Y-%m-%d %I:%M %p')
    elements.append(Paragraph(f"<b>Date & Time:</b> {current_time}", styles['Normal']))
    elements.append(Paragraph(f"<b>Generated By:</b> {current_user.username}", styles['Normal']))
    elements.append(Paragraph(f"<b>Handover Location:</b> {district} District Office", styles['Normal']))
    elements.append(Spacer(1, 20))

    data = [['ITEM NAME', 'GOOD (✅)', 'DEFECTIVE (❌)', 'TOTAL QTY', 'REMARKS']]
    for item in inv_data:
        good = item['good_qty']
        defective = item['defective_qty']
        data.append([item['item_name'], str(good), str(defective), str(good + defective), item['remark'] or '-'])

    table = Table(data, colWidths=[130, 70, 80, 70, 180])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white])
    ]))
    elements.append(table)

    sig_data = [['Handed Over By:', 'Received By:', 'Authorized By:'],
                ['__________________', '__________________', '__________________'],
                ['Name / Signature', 'Name / Signature', 'Name / Signature'],
                ['Date: ....................', 'Date: ....................', 'Date: ....................']]
    
    sig_table = Table(sig_data, colWidths=[170, 170, 170])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15)
    ]))

    elements.append(KeepTogether([Spacer(1, 60), sig_table]))
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"Handover_{district}_{current_time}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    create_tables() 
    create_default_admin()
    print("TabCore Server is running on Port 80...")
    from waitress import serve
    serve(app, host='0.0.0.0', port=80)

