
import http.server
import sqlite3
import urllib.parse
import os
import sys
import json
import re
import hashlib
import uuid
import smtplib
import random
import time
from email.mime.text import MIMEText

# Ensure api/ directory is on path so career_database is always found
sys.path.insert(0, os.path.dirname(__file__))

try:
    from career_database import CAREERS
except ImportError:
    CAREERS = []

try:
    import pg8000
    import pg8000.native
    PG_AVAILABLE = True
except ImportError:
    PG_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

GRADE_MAP = {'A':12,'A-':11,'B+':10,'B':9,'B-':8,'C+':7,'C':6,'C-':5,'D+':4,'D':3,'D-':2,'E':1,'':0}

def is_postgres():
    return bool(os.getenv("Careerdatabase_URL") and PG_AVAILABLE)

def ph():
    """SQL placeholder: %s for Postgres, ? for SQLite."""
    return "%s" if is_postgres() else "?"

def get_db_connection():
    """Return a Neon PostgreSQL connection if configured, else local SQLite."""
    db_url = os.getenv("Careerdatabase_URL")
    if db_url and PG_AVAILABLE:
        # pg8000 needs the URL parsed manually
        import urllib.parse as _up
        r = _up.urlparse(db_url)
        conn = pg8000.connect(
            host=r.hostname,
            port=r.port or 5432,
            database=r.path.lstrip('/'),
            user=r.username,
            password=r.password,
            ssl_context=True
        )
        return conn
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Ensure all required tables exist with the correct schema."""
    try:
        conn = get_db_connection()
        if is_postgres():
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                full_name TEXT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'student',
                school TEXT,
                phone TEXT,
                study_areas TEXT,
                is_verified INTEGER DEFAULT 0,
                created_at BIGINT DEFAULT 0,
                profile_data TEXT,
                last_results TEXT
            )""")
            # Add columns if they don't exist (migration)
            for col in ['profile_data TEXT', 'last_results TEXT']:
                try:
                    cur.execute(f"ALTER TABLE users ADD COLUMN {col}")
                except Exception:
                    pass
            cur.execute("""CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id INTEGER,
                created_at BIGINT
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS verification_tokens (
                token TEXT PRIMARY KEY,
                user_id INTEGER,
                expires_at BIGINT
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS scholarships (
                id SERIAL PRIMARY KEY,
                name TEXT, provider TEXT, description TEXT,
                eligibility_criteria TEXT, deadline TEXT, link TEXT,
                category TEXT DEFAULT 'General', amount TEXT DEFAULT ''
            )""")
            for col in ['category TEXT DEFAULT \'General\'', 'amount TEXT DEFAULT \'\'']:
                try:
                    cur.execute(f"ALTER TABLE scholarships ADD COLUMN {col}")
                except Exception:
                    pass
            conn.commit()
            cur.close()
        else:
            # SQLite: drop and recreate users table if it's missing new columns
            existing = conn.execute("PRAGMA table_info(users)").fetchall()
            col_names = [row[1] for row in existing]
            if existing and 'full_name' not in col_names:
                conn.execute("DROP TABLE IF EXISTS users")
                conn.execute("DROP TABLE IF EXISTS sessions")
                conn.execute("DROP TABLE IF EXISTS verification_tokens")
                conn.commit()
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT, email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL, role TEXT DEFAULT 'student',
                school TEXT, phone TEXT, study_areas TEXT,
                is_verified INTEGER DEFAULT 0, created_at INTEGER DEFAULT 0,
                profile_data TEXT, last_results TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY, user_id INTEGER, created_at INTEGER
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS verification_tokens (
                token TEXT PRIMARY KEY, user_id INTEGER, expires_at INTEGER
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS scholarships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, provider TEXT, description TEXT,
                eligibility_criteria TEXT, deadline TEXT, link TEXT,
                category TEXT DEFAULT 'General', amount TEXT DEFAULT ''
            )""")
            # Migrate existing tables to add new columns
            existing_cols = [row[1] for row in conn.execute("PRAGMA table_info(scholarships)").fetchall()]
            if 'category' not in existing_cols:
                conn.execute("ALTER TABLE scholarships ADD COLUMN category TEXT DEFAULT 'General'")
            if 'amount' not in existing_cols:
                conn.execute("ALTER TABLE scholarships ADD COLUMN amount TEXT DEFAULT ''")
            conn.commit()
        conn.close()
    except Exception:
        pass

# Run on startup — wrapped so a DB error doesn't crash the whole app
try:
    init_db()
except Exception:
    pass

def seed_scholarships():
    """Seed the scholarships table with well-known Kenyan funding opportunities if empty."""
    SEED_DATA = [
        {
            'name': 'Higher Education Loans Board (HELB) Loan & Bursary',
            'provider': 'Higher Education Loans Board (HELB)',
            'description': 'Government-backed loans and bursaries for Kenyan students in accredited universities and TVET institutions. Covers tuition, accommodation, and upkeep. Bursary component is non-repayable for needy students.',
            'eligibility_criteria': 'Kenyan citizen, admitted to a government-sponsored or self-sponsored programme at a recognised institution, demonstrated financial need',
            'deadline': '2025-09-30',
            'link': 'https://www.helb.co.ke',
            'category': 'Government',
            'amount': 'Up to KES 60,000/year (loan) + KES 8,000 bursary'
        },
        {
            'name': 'HEFoND Bursary (Higher Education Financing for Needy and Deserving Students)',
            'provider': 'Higher Education Financing for Needy and Deserving (HEFoND)',
            'description': 'A government fund targeting needy and deserving students in public universities and TVET colleges. Provides non-repayable bursaries to bridge the gap left by HELB loans for the most vulnerable students.',
            'eligibility_criteria': 'Kenyan citizen, enrolled in a public university or TVET, demonstrated financial need, household income below poverty line',
            'deadline': '2025-10-31',
            'link': 'https://www.hefond.go.ke',
            'category': 'Government',
            'amount': 'Up to KES 50,000/year (non-repayable)'
        },
        {
            'name': 'NG-CDF Bursary (National Government Constituencies Development Fund)',
            'provider': 'NG-CDF – Constituency Office',
            'description': 'Bursaries disbursed at constituency level to support secondary and tertiary students from low-income families. Each of Kenya\'s 290 constituencies allocates a portion of its NG-CDF budget to education bursaries.',
            'eligibility_criteria': 'Kenyan citizen, resident in the constituency, enrolled in secondary school, college, or university, demonstrated financial need',
            'deadline': '2025-08-31',
            'link': 'https://ngcdf.go.ke',
            'category': 'Government',
            'amount': 'KES 5,000 – KES 30,000 (varies by constituency)'
        },
        {
            'name': 'Equity Wings to Fly Scholarship',
            'provider': 'Equity Group Foundation',
            'description': 'A comprehensive scholarship covering full secondary school fees, mentorship, leadership training, and university placement support. One of Kenya\'s most prestigious merit-and-need scholarships for Form 1 entry.',
            'eligibility_criteria': 'Kenyan citizen, KCPE score of 350+ (or equivalent), joining Form 1 in a national or extra-county school, household income below KES 100,000/year',
            'deadline': '2026-02-28',
            'link': 'https://equitygroupfoundation.com/wings-to-fly',
            'category': 'Private',
            'amount': 'Full secondary school fees + stipend'
        },
        {
            'name': 'KCB Foundation Scholarship',
            'provider': 'KCB Foundation',
            'description': 'Supports talented but financially disadvantaged Kenyan students pursuing university education in priority fields including STEM, business, and social sciences. Includes mentorship and internship opportunities within the KCB Group.',
            'eligibility_criteria': 'Kenyan citizen, admitted to a public university, KCSE mean grade of B+ or above, demonstrated financial need, aged 18–25',
            'deadline': '2025-11-30',
            'link': 'https://kcbgroup.com/foundation/scholarships',
            'category': 'Private',
            'amount': 'Up to KES 100,000/year'
        },
        {
            'name': 'Mastercard Foundation Scholars Program',
            'provider': 'Mastercard Foundation / Various Partner Universities',
            'description': 'Full scholarships for academically talented yet economically disadvantaged African students to study at leading African and global universities. Includes leadership development, mentorship, and internship placements.',
            'eligibility_criteria': 'African citizen, demonstrated academic excellence, financial need, commitment to giving back to community, admitted to a partner university',
            'deadline': '2026-03-31',
            'link': 'https://mastercardfdn.org/all/scholars',
            'category': 'International',
            'amount': 'Full tuition, accommodation, living stipend, travel'
        },
        {
            'name': 'Kenya Government Presidential Scholarship',
            'provider': 'Ministry of Education, Kenya',
            'description': 'Prestigious government scholarships for top-performing Kenyan students to pursue undergraduate and postgraduate studies at leading universities locally and abroad. Awarded based on KCSE performance.',
            'eligibility_criteria': 'Kenyan citizen, KCSE grade A (plain) or equivalent, admitted to a recognised university, strong academic record',
            'deadline': '2025-07-31',
            'link': 'https://www.education.go.ke',
            'category': 'Government',
            'amount': 'Full tuition + living allowance'
        },
        {
            'name': 'CDF Bursary – County Government',
            'provider': 'County Government (varies by county)',
            'description': 'County-level bursaries for students from needy families pursuing secondary, TVET, or university education. Application is made through the county education office or ward administrator.',
            'eligibility_criteria': 'Resident of the county, enrolled in an accredited institution, demonstrated financial need, recommendation from local administration',
            'deadline': '2025-09-30',
            'link': 'https://www.cra.go.ke',
            'category': 'Government',
            'amount': 'KES 5,000 – KES 25,000 (varies by county)'
        },
        {
            'name': 'Safaricom Foundation Scholarship',
            'provider': 'Safaricom Foundation',
            'description': 'Supports bright students from disadvantaged backgrounds pursuing university education in STEM and business-related fields. Includes mentorship and potential internship at Safaricom.',
            'eligibility_criteria': 'Kenyan citizen, admitted to a public university, KCSE B+ or above, financial need, interest in technology or business',
            'deadline': '2025-10-15',
            'link': 'https://www.safaricomfoundation.org',
            'category': 'Private',
            'amount': 'Up to KES 80,000/year'
        },
        {
            'name': 'USAID Kenya Scholarship Programs',
            'provider': 'USAID Kenya',
            'description': 'Various scholarship and exchange programmes funded by USAID supporting Kenyan students in fields aligned with development priorities including health, agriculture, education, and governance.',
            'eligibility_criteria': 'Kenyan citizen, strong academic record, demonstrated community involvement, specific criteria vary by programme',
            'deadline': '2026-01-31',
            'link': 'https://www.usaid.gov/kenya',
            'category': 'International',
            'amount': 'Varies by programme'
        },
    ]
    try:
        conn = get_db_connection()
        count = db_fetchone(conn, "SELECT COUNT(id) as c FROM scholarships")
        if count and count['c'] == 0:
            for s in SEED_DATA:
                db_execute(conn, f"""INSERT INTO scholarships
                    (name, provider, description, eligibility_criteria, deadline, link, category, amount)
                    VALUES ({ph()},{ph()},{ph()},{ph()},{ph()},{ph()},{ph()},{ph()})""",
                    (s['name'], s['provider'], s['description'], s['eligibility_criteria'],
                     s['deadline'], s['link'], s['category'], s['amount']))
        conn.close()
    except Exception:
        pass

try:
    seed_scholarships()
except Exception:
    pass

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def generate_otp():
    """Generate a 6-digit OTP code."""
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, code):
    """Send a 6-digit OTP via Gmail SMTP."""
    gmail_user = os.getenv("careerapp_gmail", "")
    gmail_pass = os.getenv("careerapps_password", "")
    if not gmail_user or not gmail_pass:
        return False
    body = f"""Hi,

Your Career & Scholarship Portal verification code is:

    {code}

This code expires in 10 minutes.

If you did not create an account, please ignore this email.

— Career & Scholarship Portal Team"""
    msg = MIMEText(body)
    msg['Subject'] = f'{code} is your Career Portal verification code'
    msg['From'] = f"Career Portal <{gmail_user}>"
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_pass)
            smtp.send_message(msg)
        return True
    except Exception:
        return False

def map_grade(g):
    return GRADE_MAP.get(g, 0)

def parse_profile_cookie(cookie_header):
    """Extract profile_data dict from cookie header string."""
    for part in cookie_header.split(';'):
        part = part.strip()
        if part.startswith('profile_data='):
            try:
                return json.loads(urllib.parse.unquote(part[len('profile_data='):]))
            except Exception:
                pass
    return {}

def db_query(conn, sql, params=()):
    """Execute a query and return all rows as list of dicts."""
    if is_postgres():
        cur = conn.cursor()
        cur.execute(sql, list(params))
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
        cur.close()
        return rows
    else:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

def db_execute(conn, sql, params=()):
    """Execute a write query (INSERT/UPDATE/DELETE)."""
    if is_postgres():
        cur = conn.cursor()
        cur.execute(sql, list(params))
        conn.commit()
        cur.close()
    else:
        conn.execute(sql, params)
        conn.commit()

def db_fetchone(conn, sql, params=()):
    """Execute a query and return one row as dict."""
    if is_postgres():
        cur = conn.cursor()
        cur.execute(sql, list(params))
        cols = [d[0] for d in cur.description] if cur.description else []
        row = cur.fetchone()
        cur.close()
        return dict(zip(cols, row)) if row else None
    else:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None

def db_lastid(conn, table='users'):
    """Get last inserted ID."""
    if is_postgres():
        cur = conn.cursor()
        cur.execute("SELECT lastval()")
        row = cur.fetchone()
        cur.close()
        return row[0] if row else None
    else:
        return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


    """Extract profile_data dict from cookie header string."""
    for part in cookie_header.split(';'):
        part = part.strip()
        if part.startswith('profile_data='):
            try:
                return json.loads(urllib.parse.unquote(part[len('profile_data='):]))
            except Exception:
                pass
    return {}

def run_algorithm(profile_data):
    """Run the career recommendation algorithm.
    Returns (scored_careers, mean_grade, study_level, user_inputs)
    scored_careers = list of (score, max_score, career_dict)"""
    user_inputs = {
        'math_grade':       profile_data.get('math_grade', ''),
        'english_grade':    profile_data.get('english_grade', ''),
        'kiswahili_grade':  profile_data.get('kiswahili_grade', ''),
        'biology_grade':    profile_data.get('biology_grade', ''),
        'chemistry_grade':  profile_data.get('chemistry_grade', ''),
        'physics_grade':    profile_data.get('physics_grade', ''),
        'humanities_grade': profile_data.get('humanities_grade', ''),
    }

    activities = profile_data.get('activity', [])
    if isinstance(activities, str):
        activities = [activities]

    traits = [
        profile_data.get('work_environment', ''),
        profile_data.get('teamwork', ''),
        profile_data.get('problem_solving', ''),
        activities[0] if activities else '',
        profile_data.get('motivation', ''),
    ]

    industry_list = [i.strip() for i in profile_data.get('industry_interests', '').split(',') if i.strip()]
    education_goal = profile_data.get('education_goal', '')

    points = [map_grade(v) for v in user_inputs.values() if v]
    if not points:
        return [], 0, 'Unknown', user_inputs

    mean_grade = sum(points) / len(user_inputs)

    if mean_grade >= 7.0:
        study_level = 'University / Graduate'
    elif mean_grade >= 5.0:
        study_level = 'Diploma / TVET'
    elif mean_grade >= 3.0:
        study_level = 'Certificate'
    else:
        study_level = 'Artisan'

    # Compute max possible score for normalisation
    scored = []
    for c in CAREERS:
        if education_goal and c['level'] != education_goal:
            continue
        if mean_grade < c['min_grade']:
            continue
        subject_score  = sum(map_grade(user_inputs.get(s, '')) * 2 for s in c['subjects'])
        trait_score    = sum(c['traits'].get(t, 0) for t in traits)
        industry_score = sum(8 for ind in industry_list if ind in c.get('industries', []))
        total = subject_score + trait_score + industry_score
        scored.append((total, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Normalise scores to % match (max score of top result = 100%)
    if scored:
        max_score = max(s for s, _ in scored) or 1
        result = [(round((s / max_score) * 100), c) for s, c in scored[:8]]
    else:
        result = []

    return result, mean_grade, study_level, user_inputs


class handler(http.server.BaseHTTPRequestHandler):

    def get_current_user(self):
        cookie_header = self.headers.get('Cookie', '')
        for part in cookie_header.split(';'):
            part = part.strip()
            if part.startswith('session_id='):
                session_id = part[len('session_id='):]
                try:
                    conn = get_db_connection()
                    row = db_fetchone(conn,
                        f"SELECT u.* FROM users u JOIN sessions s ON u.id=s.user_id WHERE s.session_id={ph()}",
                        (session_id,))
                    conn.close()
                    if row:
                        return row
                except Exception:
                    pass
            if part.startswith('admin_token=') and part[len('admin_token='):] == 'authenticated':
                return {'is_admin': 1, 'full_name': 'Admin', 'email': ''}
        return None

    def render_template(self, template_name, context=None):
        if context is None:
            context = {}
        try:
            with open(os.path.join(TEMPLATES_DIR, template_name), 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = "<h2>Template not found</h2>"

        context.setdefault('title', 'Portal')
        context.setdefault('extra_css', '')
        context.setdefault('alert', '')

        user = self.get_current_user()
        if user and user.get('is_admin') == 1:
            context['auth_links'] = '''
                <a href="/admin" class="nav-link">Admin Dashboard</a>
                <a href="/admin/logout" class="nav-btn-outline">Log Out</a>'''
        elif user:
            name = user.get('full_name', 'User')
            initial = name[0].upper() if name else 'U'
            context['auth_links'] = f'''
                <a href="/dashboard" class="nav-avatar" title="{name}">{initial}</a>
                <a href="/logout" class="nav-btn-outline">Log Out</a>'''
        else:
            context['auth_links'] = '''
                <a href="/login" class="nav-link">Login</a>
                <a href="/register" class="nav-btn-primary">Start Your Career Profile</a>'''

        try:
            with open(os.path.join(TEMPLATES_DIR, 'base.html'), 'r', encoding='utf-8') as f:
                html = f.read()
        except FileNotFoundError:
            return b"<html><body><h1>Missing base.html</h1></body></html>"

        html = html.replace('{{content}}', content)
        for key, value in context.items():
            html = html.replace(f'{{{{{key}}}}}', str(value))
        html = re.sub(r'{{.*?}}', '', html)
        return html.encode('utf-8')

    def send_redirect(self, url, admin_token=None, clear_admin=False):
        self.send_response(302)
        self.send_header('Location', url)
        if admin_token:
            self.send_header('Set-Cookie', f'admin_token={admin_token}; Path=/; HttpOnly')
        elif clear_admin:
            self.send_header('Set-Cookie', 'admin_token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
        self.end_headers()

    def send_html(self, html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html)

    def serve_static(self, file_path, content_type):
        try:
            with open(os.path.join(BASE_DIR, file_path), 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path
        query  = urllib.parse.parse_qs(parsed.query)

        # Static files
        if path.startswith('/static/'):
            ext_map = {'.css': 'text/css', '.png': 'image/png',
                       '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.ico': 'image/x-icon'}
            for ext, ct in ext_map.items():
                if path.endswith(ext):
                    self.serve_static(path.lstrip('/'), ct)
                    return
            return

        user = self.get_current_user()

        if path in ('/', '/index'):
            self.send_html(self.render_template('index.html', {'title': 'Home'}))

        elif path == '/profile':
            self.send_html(self.render_template('profile_intro.html', {'title': 'Career Profiling'}))

        elif path == '/profile/step1':
            self.send_html(self.render_template('profile_step1.html', {'title': 'Step 1 – Academic Grades'}))

        elif path == '/profile/step2':
            self.send_html(self.render_template('profile_step2.html', {'title': 'Step 2 – Skills & Aptitude'}))

        elif path == '/profile/step3':
            self.send_html(self.render_template('profile_step3.html', {'title': 'Step 3 – Preferences'}))

        elif path == '/profile/step4':
            profile_data = parse_profile_cookie(self.headers.get('Cookie', ''))
            activities = profile_data.get('activity', ['-'])
            ctx = {
                'title': 'Step 4 – Final Review',
                'math_grade':        profile_data.get('math_grade', '-'),
                'english_grade':     profile_data.get('english_grade', '-'),
                'kiswahili_grade':   profile_data.get('kiswahili_grade', '-'),
                'biology_grade':     profile_data.get('biology_grade', '-'),
                'chemistry_grade':   profile_data.get('chemistry_grade', '-'),
                'physics_grade':     profile_data.get('physics_grade', '-'),
                'humanities_grade':  profile_data.get('humanities_grade', '-'),
                'problem_solving':   profile_data.get('problem_solving', '-'),
                'rating_analytical': profile_data.get('rating_analytical', '-'),
                'rating_coding':     profile_data.get('rating_coding', '-'),
                'rating_leadership': profile_data.get('rating_leadership', '-'),
                'activity':          ', '.join(activities) if isinstance(activities, list) else activities,
                'work_environment':  profile_data.get('work_environment', '-'),
                'industry_interests':profile_data.get('industry_interests', '-'),
                'relocate':          'Willing to relocate' if profile_data.get('relocate') == 'yes' else 'Not relocating',
                'budget':            profile_data.get('budget', '-'),
            }
            self.send_html(self.render_template('profile_step4.html', ctx))

        elif path == '/login':
            self.send_html(self.render_template('login.html', {'title': 'Log In'}))

        elif path == '/register':
            self.send_html(self.render_template('register.html', {'title': 'Create Account'}))

        elif path == '/dashboard':
            if not user:
                return self.send_redirect('/login')
            # If user has saved results, redirect straight to recommendations
            if user.get('last_results'):
                return self.send_redirect('/recommendations')
            self.send_html(self.render_template('dashboard.html', {
                'title': 'Dashboard',
                'user_name': user.get('full_name', 'Student')
            }))

        elif path == '/logout':
            cookie_header = self.headers.get('Cookie', '')
            for part in cookie_header.split(';'):
                part = part.strip()
                if part.startswith('session_id='):
                    sid = part[len('session_id='):]
                    try:
                        conn = get_db_connection()
                        db_execute(conn, f"DELETE FROM sessions WHERE session_id={ph()}", (sid,))
                        conn.close()
                    except Exception:
                        pass
            self.send_response(302)
            self.send_header('Location', '/')
            self.send_header('Set-Cookie', 'session_id=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
            self.end_headers()

        elif path == '/forgot-password':
            self.send_html(self.render_template('forgot_password.html', {'title': 'Forgot Password'}))

        elif path == '/verify-otp':
            token = query.get('token', [''])[0]
            email_q = query.get('email', [''])[0]
            self.send_html(self.render_template('verify_otp.html', {
                'title': 'Enter Verification Code',
                'email': email_q,
                'alert': ''
            }))

        elif path == '/resend-otp':
            email = query.get('email', [''])[0]
            try:
                conn = get_db_connection()
                u = db_fetchone(conn, f"SELECT * FROM users WHERE email={ph()}", (email,))
                if u and not u.get('is_verified'):
                    otp = generate_otp()
                    db_execute(conn, f"DELETE FROM verification_tokens WHERE user_id={ph()}", (u['id'],))
                    db_execute(conn, f"INSERT INTO verification_tokens (token, user_id, expires_at) VALUES ({ph()},{ph()},{ph()})",
                               (otp, u['id'], int(time.time()) + 600))
                    send_otp_email(email, otp)
                conn.close()
            except Exception:
                pass
            self.send_html(self.render_template('verify_otp.html', {
                'title': 'Enter Verification Code',
                'email': email,
                'alert': '<div class="alert alert-success">A new code has been sent to your email.</div>'
            }))

        elif path == '/verify':
            token = query.get('token', [''])[0]
            try:
                conn = get_db_connection()
                row = db_fetchone(conn, f"SELECT * FROM verification_tokens WHERE token={ph()}", (token,))
                if row and int(time.time()) < row['expires_at']:
                    db_execute(conn, f"UPDATE users SET is_verified=1 WHERE id={ph()}", (row['user_id'],))
                    db_execute(conn, f"DELETE FROM verification_tokens WHERE token={ph()}", (token,))
                    conn.close()
                    self.send_html(self.render_template('login.html', {
                        'title': 'Log In',
                        'alert': '<div class="alert alert-success">Email verified! You can now log in.</div>'
                    }))
                else:
                    conn.close()
                    self.send_html(self.render_template('login.html', {
                        'title': 'Log In',
                        'alert': '<div class="alert alert-error">Verification link is invalid or expired.</div>'
                    }))
            except Exception:
                self.send_redirect('/login')

        elif path == '/resend-verification':
            email = query.get('email', [''])[0]
            try:
                conn = get_db_connection()
                u = db_fetchone(conn, f"SELECT * FROM users WHERE email={ph()}", (email,))
                if u and not u['is_verified']:
                    token = str(uuid.uuid4())
                    db_execute(conn, f"INSERT INTO verification_tokens (token, user_id, expires_at) VALUES ({ph()},{ph()},{ph()})",
                               (token, u['id'], int(time.time()) + 86400))
                    send_verification_email(email, token)
                conn.close()
            except Exception:
                pass
            self.send_html(self.render_template('verify_email.html', {'title': 'Check Your Email', 'email': email}))

        elif path == '/debug-env':
            db_url = os.getenv("Careerdatabase_URL", "NOT SET")
            masked = db_url[:30] + "..." if len(db_url) > 30 else db_url
            gmail = os.getenv("careerapp_gmail", "NOT SET")
            gmail_pass = "SET" if os.getenv("careerapps_password") else "NOT SET"
            # Test DB connection
            db_status = "untested"
            try:
                conn = get_db_connection()
                db_fetchone(conn, "SELECT 1 as ok")
                conn.close()
                db_status = "OK"
            except Exception as e:
                db_status = f"ERROR: {e}"
            self.send_html(f"""<pre>
Careerdatabase_URL = {masked}
PG_AVAILABLE = {PG_AVAILABLE}
is_postgres() = {is_postgres()}
DB connection = {db_status}
GMAIL_USER = {gmail}
GMAIL_APP_PASSWORD = {gmail_pass}
</pre>""".encode())

        elif path == '/recommendations':
            if not user:
                return self.send_redirect('/login')
            saved_profile = user.get('profile_data', '')
            saved_results = user.get('last_results', '')
            if saved_profile or saved_results:
                try:
                    # Re-run algorithm from saved profile data for full page
                    if saved_profile:
                        profile_data = json.loads(saved_profile)
                        scored_careers, mean_grade, study_level, user_inputs = run_algorithm(profile_data)
                    else:
                        # Fallback: use saved results only
                        results = json.loads(saved_results)
                        cards = ''
                        for i, r in enumerate(results[:4]):
                            sel = 'rec-card-selected' if i == 0 else ''
                            cards += f'<div class="rec-program-card {sel}" onclick="selectProgram(this,{i})"><div class="rec-card-top"><a class="rec-card-title">{r["name"]}</a><span class="rec-match-badge rec-match-high">{r["match"]}% MATCH</span></div><div class="rec-card-tags"><span class="rec-tag">{r["level"]}</span></div></div>'
                        self.send_html(self.render_template('recommendations.html', {
                            'title': 'Your Career Recommendations',
                            'top_pathway': 'STEM', 'mean_grade': '-', 'comp_index': '-',
                            'study_level': '-', 'top_match': f'{results[0]["match"]}%' if results else '-',
                            'top_name': results[0]['name'] if results else '-',
                            'program_cards': cards, 'detail_html': '', 'math_grade': '-', 'english_grade': '-'
                        }))
                        return

                    # Build full page same as submit handler
                    top_pathway = 'STEM'
                    if scored_careers:
                        industries = scored_careers[0][1].get('industries', [])
                        if any(i in industries for i in ['Healthcare','SocialWork','Law','EdTech']):
                            top_pathway = 'Social Sciences'
                        elif any(i in industries for i in ['Creative','Media','Tourism']):
                            top_pathway = 'Arts & Humanities'

                    program_cards = ''
                    for i, (match_pct, c) in enumerate(scored_careers[:4]):
                        level_tag = 'University' if c['level'] == 'Degree' else 'TVET'
                        demand = 'High Demand' if match_pct >= 80 else 'Medium Demand'
                        sel = 'rec-card-selected' if i == 0 else ''
                        skills_fit = min(match_pct + 5, 99)
                        grades_fit = min(match_pct - 3, 99)
                        program_cards += f"""<div class="rec-program-card {sel}" onclick="selectProgram(this,{i})" data-index="{i}">
                            <div class="rec-card-top"><div><a class="rec-card-title">{c['name']}</a><span class="rec-card-tag">{level_tag}</span>{'<span class="rec-card-tag rec-tag-scholar">Scholarship</span>' if match_pct >= 80 else ''}</div>
                            <span class="rec-match-badge {'rec-match-high' if match_pct >= 85 else 'rec-match-med'}">{match_pct}% MATCH</span></div>
                            <div class="rec-card-tags"><span class="rec-tag">{c['level']}</span><span class="rec-tag">{demand}</span></div>
                            <div class="rec-card-fit"><span>SKILLS FIT <strong>{skills_fit}%</strong></span><span>GRADES FIT <strong>{grades_fit}%</strong></span></div>
                        </div>"""

                    detail_html = ''
                    if scored_careers:
                        _, top = scored_careers[0]
                        detail_html = f"""<div class="rec-detail-card" id="rec-detail">
                            <h3>Selected: <span style="color:#3b82f6">{top['name']}</span></h3>
                            <p style="color:#6b7280;font-size:0.88rem;margin-bottom:1.5rem;">Full-time • {top['level']} • Kenya</p>
                            <div class="rec-detail-grid">
                                <div><h5>ENTRY REQUIREMENTS</h5><ul class="rec-req-list">
                                    <li>KCSE Mean Grade: {study_level}</li>
                                    {''.join(f'<li>{s.replace("_grade","").title()}: {user_inputs.get(s,"-")}</li>' for s in top['subjects'][:3])}
                                </ul></div>
                                <div><h5>CAREER OUTCOMES</h5><div class="rec-outcome-tags">
                                    {''.join(f'<span class="rec-tag">{o}</span>' for o in ["Developer","Analyst","Engineer","Manager"][:3])}
                                </div></div>
                                <div><h5>PROJECTED COST</h5><p class="rec-cost">KES 180,000</p><small style="color:#6b7280;">Estimated Annual Tuition</small></div>
                            </div></div>"""

                    ratings = [int(profile_data.get(f'rating_{k}', 0) or 0) for k in ['analytical','coding','verbal','critical','creative','leadership']]
                    comp_index = round(sum(ratings) / (len(ratings) * 5) * 10, 1) if any(ratings) else 0

                    self.send_html(self.render_template('recommendations.html', {
                        'title': 'Your Career Recommendations',
                        'top_pathway': top_pathway,
                        'mean_grade': f"{mean_grade:.1f}" if mean_grade else '-',
                        'comp_index': f"{comp_index}/10",
                        'study_level': study_level,
                        'top_match': str(scored_careers[0][0]) + '%' if scored_careers else '-',
                        'top_name': scored_careers[0][1]['name'] if scored_careers else '-',
                        'program_cards': program_cards,
                        'detail_html': detail_html,
                        'math_grade': user_inputs.get('math_grade', '-') or '-',
                        'english_grade': user_inputs.get('english_grade', '-') or '-',
                    }))
                except Exception as e:
                    self.send_redirect('/profile')
            else:
                self.send_redirect('/profile')

        elif path == '/scholarships':
            search = query.get('q', [''])[0]
            category = query.get('cat', [''])[0]
            try:
                conn = get_db_connection()
                conditions = []
                params = []
                if search:
                    conditions.append(f"(name LIKE {ph()} OR description LIKE {ph()} OR provider LIKE {ph()} OR eligibility_criteria LIKE {ph()})")
                    params += [f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%']
                if category:
                    conditions.append(f"category = {ph()}")
                    params.append(category)
                where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
                rows = db_query(conn, f"SELECT * FROM scholarships {where} ORDER BY id", tuple(params))
                # Fetch distinct categories for filter pills
                cats = db_query(conn, "SELECT DISTINCT category FROM scholarships ORDER BY category")
                conn.close()
            except Exception:
                rows = []
                cats = []

            cat_list = [c['category'] for c in cats if c.get('category')]

            # Category filter pills
            pills_html = f'<a href="/scholarships" class="filter-pill {"filter-pill-active" if not category else ""}">All</a>'
            for c in cat_list:
                active = 'filter-pill-active' if c == category else ''
                q_part = f'?cat={urllib.parse.quote(c)}' + (f'&q={urllib.parse.quote(search)}' if search else '')
                pills_html += f'<a href="/scholarships{q_part}" class="filter-pill {active}">{c}</a>'

            CATEGORY_ICONS = {'Government': '🏛️', 'Private': '🏢', 'International': '🌍', 'General': '📋'}

            def scholarship_card(s):
                icon = CATEGORY_ICONS.get(s.get('category', 'General'), '📋')
                amount_html = f'<div class="schol-amount">💰 {s["amount"]}</div>' if s.get('amount') else ''
                deadline_html = f'<div class="schol-deadline">📅 Deadline: {s["deadline"]}</div>' if s.get('deadline') else ''
                return f"""
                <div class="schol-card">
                    <div class="schol-card-header">
                        <span class="schol-icon">{icon}</span>
                        <span class="schol-category-badge">{s.get('category','General')}</span>
                    </div>
                    <h3 class="schol-title">{s['name']}</h3>
                    <p class="schol-provider">by {s['provider']}</p>
                    <p class="schol-desc">{s['description']}</p>
                    <div class="schol-meta">
                        {amount_html}
                        {deadline_html}
                    </div>
                    <div class="schol-eligibility">
                        <strong>Eligibility:</strong> {s.get('eligibility_criteria','')}
                    </div>
                    <a href="{s['link']}" target="_blank" rel="noopener" class="btn-primary schol-btn">Apply / Learn More &rarr;</a>
                </div>"""

            s_html = "".join(scholarship_card(s) for s in rows)
            if not rows:
                s_html = "<div class='schol-empty'><p>No scholarships found matching your search.</p><a href='/scholarships' class='btn-secondary' style='margin-top:1rem;display:inline-block;'>Clear filters</a></div>"

            self.send_html(self.render_template('scholarships.html', {
                'title': 'Scholarships & Bursaries',
                'scholarships_list': s_html,
                'search_query': search,
                'filter_pills': pills_html,
                'result_count': str(len(rows)),
                'result_count_plural': 'y' if len(rows) == 1 else 'ies',
                'active_category': category,
                'clear_link': f'<a href="/scholarships" style="font-size:0.85rem;color:var(--color-red);">Clear filters</a>' if (search or category) else '',
            }))

        elif path == '/admin':
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
            try:
                conn = get_db_connection()
                scholarships  = db_query(conn, "SELECT * FROM scholarships")
                total_users   = db_fetchone(conn, "SELECT COUNT(id) as c FROM users")['c']
                stem_users    = db_fetchone(conn, "SELECT COUNT(id) as c FROM users WHERE interests='STEM'")['c']
                arts_users    = db_fetchone(conn, "SELECT COUNT(id) as c FROM users WHERE interests='Arts_Sports'")['c']
                social_users  = db_fetchone(conn, "SELECT COUNT(id) as c FROM users WHERE interests='Social_Sciences'")['c']
                conn.close()
            except Exception:
                scholarships = []
                total_users = stem_users = arts_users = social_users = 0

            t_html = "".join(f"""<tr>
                <td>{s['id']}</td><td>{s['name']}</td><td>{s['provider']}</td><td>{s['deadline']}</td>
                <td>
                    <a href="/admin/edit_scholarship?id={s['id']}" style="color:var(--color-green);margin-right:1rem;">Edit</a>
                    <a href="/admin/delete_scholarship?id={s['id']}" style="color:var(--color-red);">Delete</a>
                </td></tr>""" for s in scholarships)

            ctx = {
                'title': 'Admin Dashboard',
                'scholarships_table': t_html,
                'total_users': total_users,
                'stem_users': stem_users,
                'arts_users': arts_users,
                'social_users': social_users,
                'alert': ''
            }
            msg = query.get('msg', [''])[0]
            alerts = {'added': 'Scholarship Added!', 'deleted': 'Scholarship Deleted!', 'edited': 'Scholarship Updated!'}
            if msg in alerts:
                ctx['alert'] = f"<div class='alert alert-success'>{alerts[msg]}</div>"

            self.send_html(self.render_template('admin.html', ctx))

        elif path == '/admin/login':
            self.send_html(self.render_template('admin_login.html', {'title': 'Admin Login'}))

        elif path == '/admin/logout':
            self.send_redirect('/', clear_admin=True)

        elif path == '/admin/delete_scholarship':
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
            s_id = query.get('id', [''])[0]
            if s_id:
                try:
                    conn = get_db_connection()
                    db_execute(conn, f"DELETE FROM scholarships WHERE id={ph()}", (s_id,))
                    conn.close()
                    self.send_redirect('/admin?msg=deleted')
                except Exception:
                    self.send_redirect('/admin')
            else:
                self.send_redirect('/admin')

        elif path == '/admin/edit_scholarship':
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
            s_id = query.get('id', [''])[0]
            if not s_id:
                return self.send_redirect('/admin')
            try:
                conn = get_db_connection()
                s = db_fetchone(conn, f"SELECT * FROM scholarships WHERE id={ph()}", (s_id,))
                conn.close()
                if not s:
                    return self.send_redirect('/admin')
                self.send_html(self.render_template('edit_scholarship.html', {
                    'title': 'Edit Scholarship',
                    'id': s['id'], 'name': s['name'], 'provider': s['provider'],
                    'description': s['description'], 'eligibility_criteria': s['eligibility_criteria'],
                    'deadline': s['deadline'], 'link': s['link'],
                    'category': s.get('category', 'General'), 'amount': s.get('amount', ''),
                    'cat_gov':  'selected' if s.get('category') == 'Government'    else '',
                    'cat_priv': 'selected' if s.get('category') == 'Private'       else '',
                    'cat_intl': 'selected' if s.get('category') == 'International' else '',
                    'cat_gen':  'selected' if s.get('category', 'General') == 'General' else '',
                }))
            except sqlite3.OperationalError:
                self.send_redirect('/admin')

        else:
            self.send_error(404, "Page Not Found")

    # ------------------------------------------------------------------ POST
    def do_POST(self):
        try:
            self._handle_post()
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<pre style="color:red;padding:2rem;">POST Error: {str(e)}\n\nPath: {self.path}</pre>'.encode())

    def _handle_post(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data  = self.rfile.read(content_length).decode('utf-8')
        form_data  = urllib.parse.parse_qs(post_data)
        get_val    = lambda key: form_data.get(key, [''])[0]

        def save_step(updates, next_url):
            """Merge updates into profile cookie and redirect."""
            profile_data = parse_profile_cookie(self.headers.get('Cookie', ''))
            profile_data.update(updates)
            cookie_val = urllib.parse.quote(json.dumps(profile_data))
            self.send_response(302)
            self.send_header('Location', next_url)
            self.send_header('Set-Cookie', f'profile_data={cookie_val}; Path=/; HttpOnly')
            self.end_headers()

        if path == '/admin/login':
            password = get_val('password')
            if password == os.getenv("ADMIN_PASSWORD", "admin123"):
                self.send_redirect('/admin', admin_token="authenticated")
            else:
                self.send_html(self.render_template('admin_login.html', {
                    'title': 'Admin Login',
                    'alert': '<div class="alert alert-error">Invalid password.</div>'
                }))

        elif path == '/register':
            full_name = get_val('full_name')
            email     = get_val('email')
            password  = get_val('password')
            confirm   = get_val('confirm_password')
            role      = get_val('role') or 'student'
            school    = get_val('school')
            phone     = get_val('phone')
            study_areas = get_val('study_areas')

            if not full_name or not email or not password:
                self.send_html(self.render_template('register.html', {
                    'title': 'Create Account',
                    'alert': '<div class="alert alert-error">Please fill in all required fields.</div>'
                }))
                return
            if password != confirm:
                self.send_html(self.render_template('register.html', {
                    'title': 'Create Account',
                    'alert': '<div class="alert alert-error">Passwords do not match.</div>'
                }))
                return
            try:
                conn = get_db_connection()
                db_execute(conn, f"""INSERT INTO users (full_name, email, password, role, school, phone, study_areas, created_at)
                                VALUES ({ph()},{ph()},{ph()},{ph()},{ph()},{ph()},{ph()},{ph()})""",
                             (full_name, email, hash_password(password), role, school, phone, study_areas, int(time.time())))
                user_row = db_fetchone(conn, f"SELECT id FROM users WHERE email={ph()}", (email,))
                user_id = user_row['id']
                otp = generate_otp()
                db_execute(conn, f"INSERT INTO verification_tokens (token, user_id, expires_at) VALUES ({ph()},{ph()},{ph()})",
                             (otp, user_id, int(time.time()) + 600))
                conn.close()
                try:
                    email_sent = send_otp_email(email, otp)
                except Exception:
                    email_sent = False
                alert = ''
                if not email_sent:
                    alert = f'<div class="alert alert-success" style="background:#fff3e0;color:#e65100;border-color:#ffe0b2;">Account created! Email could not be sent. Your code is: <strong>{otp}</strong></div>'
                self.send_html(self.render_template('verify_otp.html', {'title': 'Enter Verification Code', 'email': email, 'alert': alert}))
            except Exception as e:
                err = str(e)
                if 'unique' in err.lower() or 'duplicate' in err.lower():
                    msg = 'An account with this email already exists.'
                else:
                    msg = f'Registration failed: {err}'
                self.send_html(self.render_template('register.html', {
                    'title': 'Create Account',
                    'alert': f'<div class="alert alert-error">{msg}</div>'
                }))

        elif path == '/login':
            email    = get_val('email')
            password = get_val('password')
            try:
                conn = get_db_connection()
                u = db_fetchone(conn, f"SELECT * FROM users WHERE email={ph()}", (email,))
                if u and u['password'] == hash_password(password):
                    # Block unverified users
                    if not u.get('is_verified'):
                        conn.close()
                        self.send_html(self.render_template('login.html', {
                            'title': 'Log In',
                            'alert': f'<div class="alert alert-error">Please verify your email first. <a href="/resend-verification?email={email}" style="color:#b91c1c;font-weight:700;">Resend verification email</a></div>'
                        }))
                        return
                    sid = str(uuid.uuid4())
                    db_execute(conn, f"INSERT INTO sessions (session_id, user_id, created_at) VALUES ({ph()},{ph()},{ph()})",
                                 (sid, u['id'], int(time.time())))
                    conn.close()
                    self.send_response(302)
                    self.send_header('Location', '/dashboard')
                    self.send_header('Set-Cookie', f'session_id={sid}; Path=/; HttpOnly')
                    self.end_headers()
                else:
                    conn.close()
                    self.send_html(self.render_template('login.html', {
                        'title': 'Log In',
                        'alert': '<div class="alert alert-error">Invalid email or password.</div>'
                    }))
            except Exception as e:
                self.send_html(self.render_template('login.html', {
                    'title': 'Log In',
                    'alert': f'<div class="alert alert-error">Login failed: {str(e)}</div>'
                }))

        elif path == '/verify-otp':
            email = get_val('email')
            otp = get_val('d1') + get_val('d2') + get_val('d3') + get_val('d4') + get_val('d5') + get_val('d6')
            try:
                conn = get_db_connection()
                u = db_fetchone(conn, f"SELECT * FROM users WHERE email={ph()}", (email,))
                if u:
                    row = db_fetchone(conn, f"SELECT * FROM verification_tokens WHERE user_id={ph()} AND token={ph()}", (u['id'], otp))
                    if row and int(time.time()) < row['expires_at']:
                        db_execute(conn, f"UPDATE users SET is_verified=1 WHERE email={ph()}", (email,))
                        db_execute(conn, f"DELETE FROM verification_tokens WHERE token={ph()}", (otp,))
                        conn.close()
                        self.send_html(self.render_template('login.html', {
                            'title': 'Log In',
                            'alert': '<div class="alert alert-success">✅ Email verified! You can now log in.</div>'
                        }))
                    else:
                        conn.close()
                        self.send_html(self.render_template('verify_otp.html', {
                            'title': 'Enter Verification Code',
                            'email': email,
                            'alert': '<div class="alert alert-error">Invalid or expired code. Request a new one below.</div>'
                        }))
                else:
                    conn.close()
                    self.send_html(self.render_template('verify_otp.html', {
                        'title': 'Enter Verification Code',
                        'email': email,
                        'alert': '<div class="alert alert-error">Email not found.</div>'
                    }))
            except Exception as e:
                self.send_html(self.render_template('verify_otp.html', {
                    'title': 'Enter Verification Code',
                    'email': email,
                    'alert': f'<div class="alert alert-error">Verification failed: {str(e)}</div>'
                }))

        elif path == '/forgot-password':
            email = get_val('email')
            try:
                conn = get_db_connection()
                u = db_fetchone(conn, f"SELECT * FROM users WHERE email={ph()}", (email,))
                if u:
                    token = str(uuid.uuid4())
                    db_execute(conn, f"INSERT INTO verification_tokens (token, user_id, expires_at) VALUES ({ph()},{ph()},{ph()}) ON CONFLICT(token) DO UPDATE SET expires_at=EXCLUDED.expires_at" if is_postgres() else
                               f"INSERT OR REPLACE INTO verification_tokens (token, user_id, expires_at) VALUES ({ph()},{ph()},{ph()})",
                               (token, u['id'], int(time.time()) + 3600))
                    send_verification_email(email, token)
                conn.close()
            except Exception:
                pass
            self.send_html(self.render_template('forgot_password.html', {
                'title': 'Forgot Password',
                'alert': '<div class="alert alert-success">If that email exists, a reset link has been sent.</div>'
            }))

        elif path == '/profile/step1':
            save_step({
                'math_grade':       get_val('math_grade'),
                'english_grade':    get_val('english_grade'),
                'kiswahili_grade':  get_val('kiswahili_grade'),
                'biology_grade':    get_val('biology_grade'),
                'chemistry_grade':  get_val('chemistry_grade'),
                'physics_grade':    get_val('physics_grade'),
                'humanities_grade': get_val('humanities_grade'),
            }, '/profile/step2')

        elif path == '/profile/step2':
            save_step({
                'problem_solving':   get_val('problem_solving'),
                'rating_analytical': get_val('rating_analytical'),
                'rating_coding':     get_val('rating_coding'),
                'rating_verbal':     get_val('rating_verbal'),
                'rating_critical':   get_val('rating_critical'),
                'rating_creative':   get_val('rating_creative'),
                'rating_leadership': get_val('rating_leadership'),
                'activity':          form_data.get('activity', []),
                'achievement':       get_val('achievement'),
            }, '/profile/step3')

        elif path == '/profile/step3':
            save_step({
                'work_environment':  get_val('work_environment'),
                'teamwork':          get_val('teamwork'),
                'motivation':        get_val('motivation'),
                'industry_interests':get_val('industry_interests'),
                'preferred_city':    get_val('preferred_city'),
                'relocate':          get_val('relocate'),
                'commitment':        get_val('commitment'),
                'budget':            get_val('budget'),
            }, '/profile/step4')

        elif path == '/profile/submit':
            profile_data = parse_profile_cookie(self.headers.get('Cookie', ''))
            scored_careers, mean_grade, study_level, user_inputs = run_algorithm(profile_data)

            # Save profile + results to DB if user is logged in
            current_user = self.get_current_user()
            if current_user and current_user.get('id'):
                try:
                    conn = get_db_connection()
                    db_execute(conn, f"UPDATE users SET profile_data={ph()}, last_results={ph()} WHERE id={ph()}",
                               (json.dumps(profile_data), json.dumps([{'match': m, 'name': c['name'], 'level': c['level'], 'industries': c.get('industries',[])} for m, c in scored_careers]),
                                current_user['id']))
                    conn.close()
                except Exception:
                    pass

            # Determine top pathway
            top_pathway = 'STEM'
            if scored_careers:
                top_c = scored_careers[0][1]
                industries = top_c.get('industries', [])
                if any(i in industries for i in ['Healthcare', 'SocialWork', 'Law', 'EdTech']):
                    top_pathway = 'Social Sciences'
                elif any(i in industries for i in ['Creative', 'Media', 'Tourism']):
                    top_pathway = 'Arts & Humanities'
                else:
                    top_pathway = 'STEM'

            # Build program cards HTML
            program_cards = ''
            for i, (match_pct, c) in enumerate(scored_careers[:4]):
                level_tag = 'University' if c['level'] == 'Degree' else 'TVET'
                demand = 'High Demand' if match_pct >= 80 else 'Medium Demand'
                entry_grade = f"Mean Grade {c.get('min_grade_label', 'C+')} and above"
                skills_fit = min(match_pct + 5, 99)
                grades_fit = min(match_pct - 3, 99)
                selected_class = 'rec-card-selected' if i == 0 else ''
                program_cards += f"""
                <div class="rec-program-card {selected_class}" onclick="selectProgram(this, {i})" data-index="{i}">
                    <div class="rec-card-top">
                        <div>
                            <a class="rec-card-title">{c['name']}</a>
                            <span class="rec-card-tag">{level_tag}</span>
                            {'<span class="rec-card-tag rec-tag-scholar">Scholarship</span>' if match_pct >= 80 else ''}
                        </div>
                        <span class="rec-match-badge {'rec-match-high' if match_pct >= 85 else 'rec-match-med'}">{match_pct}% MATCH</span>
                    </div>
                    <div class="rec-card-tags">
                        <span class="rec-tag">{c['level']}</span>
                        <span class="rec-tag">{demand}</span>
                    </div>
                    <div class="rec-card-fit">
                        <span>SKILLS FIT <strong>{skills_fit}%</strong></span>
                        <span>GRADES FIT <strong>{grades_fit}%</strong></span>
                    </div>
                </div>"""

            # Build selected program detail (first result)
            detail_html = ''
            if scored_careers:
                _, top = scored_careers[0]
                careers_out = ', '.join(['Fullstack Developer', 'Data Analyst', 'Engineer', 'Researcher'][:3])
                detail_html = f"""
                <div class="rec-detail-card" id="rec-detail">
                    <h3>Selected: <span style="color:#3b82f6">{top['name']}</span></h3>
                    <p style="color:#6b7280;font-size:0.88rem;margin-bottom:1.5rem;">Full-time • {top['level']} • Kenya</p>
                    <div class="rec-detail-grid">
                        <div>
                            <h5>ENTRY REQUIREMENTS</h5>
                            <ul class="rec-req-list">
                                <li>KCSE Mean Grade: {study_level}</li>
                                {''.join(f'<li>{s.replace("_grade","").title()}: {user_inputs.get(s,"-")}</li>' for s in top['subjects'][:3])}
                            </ul>
                        </div>
                        <div>
                            <h5>CAREER OUTCOMES</h5>
                            <div class="rec-outcome-tags">
                                {''.join(f'<span class="rec-tag">{o}</span>' for o in ['Developer','Analyst','Engineer','Manager'][:3])}
                            </div>
                        </div>
                        <div>
                            <h5>PROJECTED COST</h5>
                            <p class="rec-cost">KES 180,000</p>
                            <small style="color:#6b7280;">Estimated Annual Tuition</small>
                        </div>
                    </div>
                </div>"""

            # Competency index
            ratings = [int(profile_data.get(f'rating_{k}', 0) or 0) for k in ['analytical','coding','verbal','critical','creative','leadership']]
            comp_index = round(sum(ratings) / (len(ratings) * 5) * 10, 1) if ratings else 0

            ctx = {
                'title': 'Your Career Recommendations',
                'top_pathway': top_pathway,
                'mean_grade': f"{mean_grade:.1f}" if mean_grade else '-',
                'comp_index': f"{comp_index}/10",
                'study_level': study_level,
                'top_match': str(scored_careers[0][0]) + '%' if scored_careers else '-',
                'top_name': scored_careers[0][1]['name'] if scored_careers else '-',
                'program_cards': program_cards,
                'detail_html': detail_html,
                'math_grade': user_inputs['math_grade'] or '-',
                'english_grade': user_inputs['english_grade'] or '-',
            }
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Set-Cookie', 'profile_data=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
            self.end_headers()
            self.wfile.write(self.render_template('recommendations.html', ctx))

        elif path == '/admin/add_scholarship':
            user = self.get_current_user()
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
            try:
                conn = get_db_connection()
                db_execute(conn, f"""INSERT INTO scholarships (name, provider, description, eligibility_criteria, deadline, link, category, amount)
                                VALUES ({ph()},{ph()},{ph()},{ph()},{ph()},{ph()},{ph()},{ph()})""",
                             (get_val('name'), get_val('provider'), get_val('description'),
                              get_val('eligibility_criteria'), get_val('deadline'), get_val('link'),
                              get_val('category') or 'General', get_val('amount')))
                conn.close()
                self.send_redirect('/admin?msg=added')
            except Exception:
                self.send_redirect('/admin')

        elif path == '/admin/edit_scholarship':
            user = self.get_current_user()
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
            s_id = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('id', [''])[0]
            if not s_id:
                return self.send_redirect('/admin')
            try:
                conn = get_db_connection()
                db_execute(conn, f"""UPDATE scholarships
                                SET name={ph()}, provider={ph()}, description={ph()}, eligibility_criteria={ph()}, deadline={ph()}, link={ph()}, category={ph()}, amount={ph()}
                                WHERE id={ph()}""",
                             (get_val('name'), get_val('provider'), get_val('description'),
                              get_val('eligibility_criteria'), get_val('deadline'), get_val('link'),
                              get_val('category') or 'General', get_val('amount'), s_id))
                conn.close()
                self.send_redirect('/admin?msg=edited')
            except Exception:
                self.send_redirect('/admin')

        else:
            self.send_error(404, "Not Found")
