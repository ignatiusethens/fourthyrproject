import http.server
import sqlite3
import urllib.parse
import uuid
import os
try:
    import libsql_experimental
    LIBSQL_AVAILABLE = True
    LIBSQL_ERROR = ""
except Exception as e:
    LIBSQL_AVAILABLE = False
    LIBSQL_ERROR = str(e)

import hashlib
from http import cookies

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Connect to Turso Cloud DB if credentials exist, otherwise local SQLite
def get_db_connection():
    turso_url = os.getenv("TURSO_DATABASE_URL")
    turso_token = os.getenv("TURSO_AUTH_TOKEN")
    
    if turso_url and turso_token and LIBSQL_AVAILABLE:
        conn = libsql_experimental.connect(turso_url, auth_token=turso_token)
    else:
        conn = sqlite3.connect(DATABASE)
        
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class handler(http.server.BaseHTTPRequestHandler):
    
    def get_current_user(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return None
            
        c = cookies.SimpleCookie(cookie_header)
        admin_token = c.get('admin_token')
        if admin_token and admin_token.value == "authenticated":
            return {'is_admin': 1}
        return None

    def render_template(self, template_name, context=None):
        if context is None:
            context = {}
            
        try:
            with open(os.path.join(TEMPLATES_DIR, template_name), 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = "<h2>Template not found</h2>"
            
        context.setdefault('title', 'Portal')
        context.setdefault('extra_css', '')
        context.setdefault('alert', '')
        
        user = self.get_current_user()
        if user and user['is_admin'] == 1:
            auth_links = f'''
                <li><a href="/admin">Admin Dashboard</a></li>
                <li><a href="/admin/logout" class="btn-secondary">Log Out</a></li>
            '''
        else:
            auth_links = ''
        context['auth_links'] = auth_links
        
        try:
            with open(os.path.join(TEMPLATES_DIR, 'base.html'), 'r', encoding='utf-8') as base:
                html = base.read()
        except FileNotFoundError:
            return "<html><body><h1>Missing base.html</h1></body></html>".encode('utf-8')
            
        html = html.replace('{{content}}', content)
        
        for key, value in context.items():
            html = html.replace(f'{{{{{key}}}}}', str(value))
                
        import re
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
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        if path.startswith('/static/'):
            if path.endswith('.css'):
                self.serve_static(path.lstrip('/'), 'text/css')
            return

        user = self.get_current_user()

        if path == '/' or path == '/index':
            self.send_html(self.render_template('index.html', {'title': 'Home'}))
            
        elif path == '/admin/login':
            self.send_html(self.render_template('admin_login.html', {'title': 'Admin Login'}))
            
        elif path == '/admin/logout':
            self.send_redirect('/', session_id='', admin_logout=True)
            
        elif path == '/profile':
            ctx = {
                'title': 'Career Profiling',
                'math_grade': 'Select Grade',
                'english_grade': 'Select Grade',
                'sciences_grade': 'Select Grade',
                'humanities_grade': 'Select Grade',
                'm_score': '50',
                'interests': 'Select Area'
            }
            if 'msg' in query and query['msg'][0] == 'success':
                ctx['alert'] = '<div class="alert alert-success">Profile processed successfully!</div>'
                
            self.send_html(self.render_template('profile.html', ctx))
            
        elif path == '/recommendations':
                
            math = user['math_grade']
            sciences = user['sciences_grade']
            interests = user['interests']
            grade_map = {'A':12, 'A-':11, 'B+':10, 'B':9, 'B-':8, 'C+':7, 'C':6, 'C-':5, 'D+':4, 'D':3, 'D-':2, 'E':1}
            def map_grade(g): return grade_map.get(g, 0)
            
            recs = ""
            level_msg = ""
            if not math or not sciences or math == 'Select Grade':
                recs = "<p style='text-align:center;'>Please update your profile to see recommendations.</p>"
                mean_grade = 0
            else:
                total_pts = map_grade(math) + map_grade(sciences) + map_grade(user['english_grade']) + map_grade(user['humanities_grade'])
                mean_grade = total_pts / 4.0
                
        elif path == '/recommendations':
            self.send_redirect('/profile')
            
        elif path == '/scholarships':
            search = query.get('q', [''])[0]
            try:
                conn = get_db_connection()
                if search:
                    cursor = conn.execute("SELECT * FROM scholarships WHERE name LIKE ? OR description LIKE ?", (f'%{search}%', f'%{search}%'))
                else:
                    cursor = conn.execute("SELECT * FROM scholarships")
                scholarships = cursor.fetchall()
                conn.close()
            except sqlite3.OperationalError:
                scholarships = []
            
            s_html = ""
            for s in scholarships:
                s_html += f"""
                    <div class="card card-red">
                        <h3>{s['name']}</h3>
                        <p><strong>Provider:</strong> {s['provider']}</p>
                        <p>{s['description']}</p>
                        <p><small>Deadline: {s['deadline']}</small></p>
                        <a href="{s['link']}" target="_blank" class="btn-primary" style="margin-top:1rem; padding: 0.5rem 1rem;">Apply Now &rarr;</a>
                    </div>
                """
            if not scholarships:
                s_html += "<p style='grid-column: 1/-1; text-align:center;'>No scholarships found matching your query.</p>"
                
            self.send_html(self.render_template('scholarships.html', {
                'title': 'Scholarships',
                'scholarships_list': s_html,
                'search_query': search
            }))
            
        elif path == '/admin':
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
                
            try:
                conn = get_db_connection()
                scholarships = conn.execute("SELECT * FROM scholarships").fetchall()
                total_users = conn.execute("SELECT COUNT(id) FROM users").fetchone()[0]
                stem_users = conn.execute("SELECT COUNT(id) FROM users WHERE interests='STEM'").fetchone()[0]
                arts_users = conn.execute("SELECT COUNT(id) FROM users WHERE interests='Arts_Sports'").fetchone()[0]
                social_users = conn.execute("SELECT COUNT(id) FROM users WHERE interests='Social_Sciences'").fetchone()[0]
                conn.close()
            except sqlite3.OperationalError:
                scholarships = []
                total_users = stem_users = arts_users = social_users = 0
            
            t_html = ""
            for s in scholarships:
                t_html += f"""
                    <tr>
                        <td>{s['id']}</td>
                        <td>{s['name']}</td>
                        <td>{s['provider']}</td>
                        <td>{s['deadline']}</td>
                        <td>
                            <a href="/admin/edit_scholarship?id={s['id']}" style="color:var(--color-green); margin-right:1rem;">Edit</a>
                            <a href="/admin/delete_scholarship?id={s['id']}" style="color:var(--color-red);">Delete</a>
                        </td>
                    </tr>
                """
                
            ctx = {
                'title': 'Admin Dashboard', 
                'scholarships_table': t_html,
                'total_users': total_users,
                'stem_users': stem_users,
                'arts_users': arts_users,
                'social_users': social_users
            }
            if 'msg' in query and query['msg'][0] == 'added':
                 ctx['alert'] = '<div class="alert alert-success">Scholarship Added!</div>'
            elif 'msg' in query and query['msg'][0] == 'deleted':
                 ctx['alert'] = '<div class="alert alert-success">Scholarship Deleted!</div>'
            elif 'msg' in query and query['msg'][0] == 'edited':
                 ctx['alert'] = '<div class="alert alert-success">Scholarship Updated!</div>'
            elif 'msg' in query and query['msg'][0] == 'vercel_error':
                 turso_url = os.getenv("TURSO_DATABASE_URL")
                 debug = f"LIBSQL={LIBSQL_AVAILABLE} / URL_SET={'YES' if turso_url else 'NO'} / ERR={LIBSQL_ERROR}"
                 ctx['alert'] = f'<div class="alert alert-error">Data Error: {debug}</div>'
                 
            self.send_html(self.render_template('admin.html', ctx))
            
        elif path == '/admin/delete_scholarship':
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
            
            s_id = query.get('id', [''])[0]
            if s_id:
                try:
                    conn = get_db_connection()
                    conn.execute("DELETE FROM scholarships WHERE id = ?", (s_id,))
                    conn.commit()
                    conn.close()
                    self.send_redirect('/admin?msg=deleted')
                except sqlite3.OperationalError:
                    self.send_redirect('/admin?msg=vercel_error')
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
                s = conn.execute("SELECT * FROM scholarships WHERE id = ?", (s_id,)).fetchone()
                conn.close()
                if not s:
                    return self.send_redirect('/admin')
                    
                ctx = {
                    'title': 'Edit Scholarship',
                    'id': s['id'],
                    'name': s['name'],
                    'provider': s['provider'],
                    'description': s['description'],
                    'eligibility_criteria': s['eligibility_criteria'],
                    'deadline': s['deadline'],
                    'link': s['link']
                }
                self.send_html(self.render_template('edit_scholarship.html', ctx))
            except sqlite3.OperationalError:
                self.send_redirect('/admin?msg=vercel_error')
            
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = urllib.parse.parse_qs(post_data)
        
        def get_val(key):
            return form_data.get(key, [''])[0]

        if path == '/admin/login':
            password = get_val('password')
            correct_password = os.getenv("ADMIN_PASSWORD", "admin123")
            if password == correct_password:
                self.send_redirect('/admin', admin_token="authenticated")
            else:
                self.send_html(self.render_template('admin_login.html', {
                    'title': 'Admin Login',
                    'alert': '<div class="alert alert-error">Invalid password.</div>'
                }))

        elif path == '/profile':
            math = get_val('math_grade')
            eng = get_val('english_grade')
            sci = get_val('sciences_grade')
            hum = get_val('humanities_grade')
            ints = get_val('interests')
            personality = get_val('personality')
            hobby = get_val('hobby')
            
            # Anonymous logging for Admin Analytics
            try:
                import uuid
                conn = get_db_connection()
                fake_uname = str(uuid.uuid4())[:8]
                conn.execute("""
                    INSERT INTO users (username, password, email, math_grade, english_grade, sciences_grade, humanities_grade, interests)
                    VALUES (?, 'none', 'none', ?, ?, ?, ?, ?)
                """, (fake_uname, math, eng, sci, hum, ints))
                conn.commit()
                conn.close()
            except Exception:
                pass # Fail silently if DB is read-only or errors out
                
            grade_map = {'A':12, 'A-':11, 'B+':10, 'B':9, 'B-':8, 'C+':7, 'C':6, 'C-':5, 'D+':4, 'D':3, 'D-':2, 'E':1}
            def map_grade(g): return grade_map.get(g, 0)
            
            recs = ""
            level_msg = ""
            if not math or not sci or math == 'Select Grade':
                recs = "<p style='text-align:center;'>Please select valid grades to see recommendations.</p>"
                mean_grade = 0
            else:
                total_pts = map_grade(math) + map_grade(eng) + map_grade(sci) + map_grade(hum)
                mean_grade = total_pts / 4.0
                
                # Expand recommendation logic based on new form inputs
                if mean_grade >= 7.0: # C+ and above: Degree level
                    level_msg = "<div class='alert alert-success' style='text-align:center; background-color: #e8f5e9; color: #2e7d32; border-color: #c8e6c9;'><strong>Qualification: Degree Level (University)</strong><br>You qualify for University Degree placement!</div>"
                    
                    if ints == 'STEM':
                        if hobby == 'Building things':
                            recs += """
                                <div class="card card-black">
                                    <h3>BSc. Civil / Mechanical Engineering</h3>
                                    <p>Highly suited for your interest in building and STEM capabilities.</p>
                                </div>
                            """
                        else:
                            recs += """
                                <div class="card card-black">
                                    <h3>BSc. Computer Science / Software Eng.</h3>
                                    <p>Premium pathway for tech-savvy individuals aiming for digital innovation.</p>
                                </div>
                                <div class="card card-green">
                                    <h3>Bachelor of Medicine & Surgery (MBChB)</h3>
                                    <p>High-demand healthcare career requiring strong science foundations.</p>
                                </div>
                            """
                    elif ints == 'Social_Sciences':
                        recs += """
                            <div class="card card-black">
                                <h3>Bachelor of Commerce / Economics</h3>
                                <p>Perfect for corporate, banking, and strategic management roles.</p>
                            </div>
                            <div class="card card-green">
                                <h3>Bachelor of Education (Arts/Science)</h3>
                                <p>Prepares you for a teaching and educational administration career.</p>
                            </div>
                        """
                    else: 
                        recs += """
                            <div class="card card-green">
                                <h3>BA. in Graphic Design / Fine Arts</h3>
                                <p>University degree emphasizing creative media and visual arts.</p>
                            </div>
                            <div class="card card-red">
                                <h3>BSc. in Sports Science</h3>
                                <p>Focuses on human physiology, athletic performance, and sports management.</p>
                            </div>
                        """
                elif mean_grade >= 5.0: # Diploma level
                    level_msg = "<div class='alert alert-success' style='text-align:center; background-color: #fff3e0; color: #e65100; border-color: #ffe0b2;'><strong>Qualification: Diploma Level</strong><br>You qualify for TVET Diploma courses.</div>"
                    if ints == 'STEM':
                        recs += """
                            <div class="card card-green">
                                <h3>Diploma in Information Technology</h3>
                                <p>Hands-on IT networking, support, and basic development skills.</p>
                            </div>
                            <div class="card card-red">
                                <h3>Diploma in Clinical Medicine / Pharmacy Tech</h3>
                                <p>Mid-level pathway into healthcare and clinical services.</p>
                            </div>
                        """
                    elif ints == 'Social_Sciences':
                        recs += """
                            <div class="card card-black">
                                <h3>Diploma in Business Management</h3>
                                <p>Foundational business, HR, and accounting principles.</p>
                            </div>
                            <div class="card card-green">
                                <h3>Diploma in Social Work & Community Development</h3>
                                <p>A pathway to NGO, community service, and governmental social roles.</p>
                            </div>
                        """
                    else:
                        recs += """
                            <div class="card card-red">
                                <h3>Diploma in Journalism & Mass Media</h3>
                                <p>Media production, reporting, and broadcasting skills.</p>
                            </div>
                        """
                else: # Artisan/Certificate level
                    level_msg = "<div class='alert alert-success' style='text-align:center; background-color: #e1f5fe; color: #0277bd; border-color: #b3e5fc;'><strong>Qualification: Certificate/Artisan Level</strong><br>You qualify for high-demand technical TVET Certificate courses.</div>"
                    if ints == 'STEM':
                        recs += """
                            <div class="card card-black">
                                <h3>Artisan in Plumbing / Electrical Wiring</h3>
                                <p>Highly demanded technical skills for the construction industry.</p>
                            </div>
                            <div class="card card-green">
                                <h3>Certificate in ICT</h3>
                                <p>Basic computer operation and technician qualifications.</p>
                            </div>
                        """
                    else:
                        recs += """
                            <div class="card card-red">
                                <h3>Certificate in Catering & Hospitality</h3>
                                <p>Skills for the hotel, tourism, and food service industry.</p>
                            </div>
                            <div class="card card-black">
                                <h3>Artisan in Tailoring & Dressmaking</h3>
                                <p>Creative technical pathway into fashion and textiles.</p>
                            </div>
                        """
            
            ctx = {
                'title': 'Your Recommendations',
                'recommendations_list': recs,
                'level_msg': level_msg,
                'math_grade': math or '-',
                'english_grade': eng or '-',
                'sciences_grade': sci or '-',
                'humanities_grade': hum or '-',
                'interests': ints or '-',
                'mean_grade': f"{mean_grade:.2f}" if math and math != 'Select Grade' else '-'
            }
            self.send_html(self.render_template('recommendations.html', ctx))
            
        elif path == '/admin/add_scholarship':
            user = self.get_current_user()
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
                
            try:
                conn = get_db_connection()
                conn.execute("""
                    INSERT INTO scholarships (name, provider, description, eligibility_criteria, deadline, link)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (get_val('name'), get_val('provider'), get_val('description'), get_val('eligibility_criteria'), get_val('deadline'), get_val('link')))
                conn.commit()
                conn.close()
                self.send_redirect('/admin?msg=added')
            except sqlite3.OperationalError:
                 self.send_redirect('/admin?msg=vercel_error')
                 
        elif path == '/admin/edit_scholarship':
            user = self.get_current_user()
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
                
            s_id = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('id', [''])[0]
            if not s_id:
                return self.send_redirect('/admin')
                
            try:
                conn = get_db_connection()
                conn.execute("""
                    UPDATE scholarships 
                    SET name=?, provider=?, description=?, eligibility_criteria=?, deadline=?, link=?
                    WHERE id=?
                """, (get_val('name'), get_val('provider'), get_val('description'), get_val('eligibility_criteria'), get_val('deadline'), get_val('link'), s_id))
                conn.commit()
                conn.close()
                self.send_redirect('/admin?msg=edited')
            except sqlite3.OperationalError:
                 self.send_redirect('/admin?msg=vercel_error')
            
        else:
            self.send_error(404, "Not Found")
