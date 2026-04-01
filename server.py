import http.server
import socketserver
import sqlite3
import urllib.parse
import uuid
import os
import hashlib
from http import cookies
import cgi

PORT = 8000
DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class PortalRequestHandler(http.server.BaseHTTPRequestHandler):
    
    def get_current_user(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return None
            
        c = cookies.SimpleCookie(cookie_header)
        session_id = c.get('session_id')
        if session_id:
            conn = get_db_connection()
            result = conn.execute("SELECT u.* FROM users u JOIN sessions s ON u.id = s.user_id WHERE s.session_id = ?", (session_id.value,)).fetchone()
            conn.close()
            return result
        return None

    def render_template(self, template_name, context=None):
        if context is None:
            context = {}
            
        try:
            with open(f"templates/{template_name}", 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = "<h2>Template not found</h2>"
            
        context.setdefault('title', 'Portal')
        context.setdefault('extra_css', '')
        context.setdefault('alert', '')
        
        user = self.get_current_user()
        if user:
            if user['is_admin'] == 1:
                auth_links = f'''
                    <li><a href="/admin">Admin Dashboard</a></li>
                    <li><a href="/logout" class="btn-secondary">Log Out</a></li>
                '''
            else:
                auth_links = f'''
                    <li><a href="/profile">My Profile</a></li>
                    <li><a href="/recommendations">Recommendations</a></li>
                    <li><a href="/logout" class="btn-secondary">Log Out</a></li>
                '''
        else:
            auth_links = f'''
                <li><a href="/login" class="btn-login">Log In</a></li>
            '''
        context['auth_links'] = auth_links
        
        try:
            with open('templates/base.html', 'r', encoding='utf-8') as base:
                html = base.read()
        except FileNotFoundError:
            return "<html><body><h1>Missing base.html</h1></body></html>".encode('utf-8')
            
        html = html.replace('{{content}}', content)
        
        for key, value in context.items():
            html = html.replace(f'{{{{{key}}}}}', str(value))
                
        # Clean up any unreplaced template vars
        import re
        html = re.sub(r'{{.*?}}', '', html)
        
        return html.encode('utf-8')

    def send_redirect(self, url, session_id=None):
        self.send_response(302)
        self.send_header('Location', url)
        if session_id:
            self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
        self.end_headers()

    def send_html(self, html):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html)

    def serve_static(self, file_path, content_type):
        try:
            with open(file_path, 'rb') as f:
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
            
        elif path == '/login':
            self.send_html(self.render_template('login.html', {'title': 'Log In'}))
            
        elif path == '/register':
            self.send_html(self.render_template('register.html', {'title': 'Register'}))
            
        elif path == '/logout':
            if user:
                conn = get_db_connection()
                conn.execute("DELETE FROM sessions WHERE user_id = ?", (user['id'],))
                conn.commit()
                conn.close()
            # Delete cookie by setting expiry
            self.send_response(302)
            self.send_header('Location', '/')
            self.send_header('Set-Cookie', 'session_id=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/')
            self.end_headers()
            
        elif path == '/profile':
            if not user:
                return self.send_redirect('/login')
                
            ctx = {
                'title': 'My Profile',
                'math_grade': user['math_grade'] or 'Select Grade',
                'english_grade': user['english_grade'] or 'Select Grade',
                'sciences_grade': user['sciences_grade'] or 'Select Grade',
                'humanities_grade': user['humanities_grade'] or 'Select Grade',
                'interests': user['interests'] or 'Select Area'
            }
            if 'msg' in query and query['msg'][0] == 'success':
                ctx['alert'] = '<div class="alert alert-success">Profile updated successfully!</div>'
                
            self.send_html(self.render_template('profile.html', ctx))
            
        elif path == '/recommendations':
            if not user:
                return self.send_redirect('/login')
                
            math = user['math_grade']
            sciences = user['sciences_grade']
            interests = user['interests']
            
            recs = ""
            if not math or not sciences:
                recs = "<p style='text-align:center;'>Please update your profile to see recommendations.</p>"
            else:
                # Rule based logic
                if interests == 'STEM' and (math in ['A','A-','B+','B'] and sciences in ['A','A-','B+','B']):
                    recs += """
                        <div class="card card-green">
                            <h3>BSc. Computer Science</h3>
                            <p>University Level Degree focusing on software development and algorithm design.</p>
                            <span class="badge badge-green">Recommended</span>
                        </div>
                        <div class="card card-red">
                            <h3>BSc. Medicine & Surgery</h3>
                            <p>For students with exceptional grades in Biology and Chemistry.</p>
                            <span class="badge badge-green">Recommended</span>
                        </div>
                    """
                elif interests == 'Social_Sciences':
                    recs += """
                        <div class="card card-black">
                            <h3>BA. Law (LLB)</h3>
                            <p>University Level Degree focusing on the Kenyan Legal System.</p>
                        </div>
                        <div class="card card-red">
                            <h3>BA. Economics</h3>
                            <p>For students strong in Humanities and Mathematics.</p>
                        </div>
                    """
                else:
                    recs += """
                        <div class="card card-green">
                            <h3>Diploma in Business Information Technology</h3>
                            <p>TVET level course offering hands on IT and Business skills.</p>
                        </div>
                        <div class="card card-black">
                            <h3>Artisan in Plumbing / Electricals</h3>
                            <p>Highly demanded technical skills through local TVETs.</p>
                        </div>
                    """
                    
            ctx = {
                'title': 'Recommendations',
                'recommendations_list': recs,
                'math_grade': math or '-',
                'english_grade': user['english_grade'] or '-',
                'sciences_grade': sciences or '-',
                'humanities_grade': user['humanities_grade'] or '-',
                'interests': interests or '-'
            }
            self.send_html(self.render_template('recommendations.html', ctx))
            
        elif path == '/scholarships':
            search = query.get('q', [''])[0]
            conn = get_db_connection()
            if search:
                cursor = conn.execute("SELECT * FROM scholarships WHERE name LIKE ? OR description LIKE ?", (f'%{search}%', f'%{search}%'))
            else:
                cursor = conn.execute("SELECT * FROM scholarships")
                
            scholarships = cursor.fetchall()
            conn.close()
            
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
                s_html = "<p style='grid-column: 1/-1; text-align:center;'>No scholarships found matching your query.</p>"
                
            self.send_html(self.render_template('scholarships.html', {
                'title': 'Scholarships',
                'scholarships_list': s_html,
                'search_query': search
            }))
            
        elif path == '/admin':
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
                
            conn = get_db_connection()
            scholarships = conn.execute("SELECT * FROM scholarships").fetchall()
            conn.close()
            
            t_html = ""
            for s in scholarships:
                t_html += f"""
                    <tr>
                        <td>{s['id']}</td>
                        <td>{s['name']}</td>
                        <td>{s['provider']}</td>
                        <td>{s['deadline']}</td>
                        <td><a href="/admin/delete_scholarship?id={s['id']}" style="color:var(--color-red);">Delete</a></td>
                    </tr>
                """
                
            ctx = {'title': 'Admin Dashboard', 'scholarships_table': t_html}
            if 'msg' in query and query['msg'][0] == 'added':
                 ctx['alert'] = '<div class="alert alert-success">Scholarship Added!</div>'
            elif 'msg' in query and query['msg'][0] == 'deleted':
                 ctx['alert'] = '<div class="alert alert-success">Scholarship Deleted!</div>'
                 
            self.send_html(self.render_template('admin.html', ctx))
            
        elif path == '/admin/delete_scholarship':
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
                
            s_id = query.get('id', [''])[0]
            if s_id:
                conn = get_db_connection()
                conn.execute("DELETE FROM scholarships WHERE id = ?", (s_id,))
                conn.commit()
                conn.close()
            self.send_redirect('/admin?msg=deleted')
            
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        form_data = urllib.parse.parse_qs(post_data)
        
        # Helper to get form value
        def get_val(key):
            return form_data.get(key, [''])[0]

        if path == '/register':
            username = get_val('username')
            email = get_val('email')
            password = hash_password(get_val('password'))
            
            conn = get_db_connection()
            try:
                conn.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
                conn.commit()
                # Auto login
                user_id = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()['id']
                session_id = str(uuid.uuid4())
                conn.execute("INSERT INTO sessions (session_id, user_id) VALUES (?, ?)", (session_id, user_id))
                conn.commit()
                self.send_redirect('/profile', session_id)
            except sqlite3.IntegrityError:
                self.send_html(self.render_template('register.html', {
                    'title': 'Register',
                    'alert': '<div class="alert alert-error">Username or Email already exists.</div>'
                }))
            finally:
                conn.close()
                
        elif path == '/login':
            username = get_val('username')
            password = hash_password(get_val('password'))
            
            conn = get_db_connection()
            # Note: The admin password hash will be checked correctly. But admin added loosely initially didn't have hash. We will fix admin pwd.
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            
            if user and (user['password'] == password or user['password'] == get_val('password')): # temporary fallback for dummy admin
                session_id = str(uuid.uuid4())
                conn.execute("INSERT INTO sessions (session_id, user_id) VALUES (?, ?)", (session_id, user['id']))
                conn.commit()
                conn.close()
                if user['is_admin'] == 1:
                    self.send_redirect('/admin', session_id)
                else:
                    self.send_redirect('/profile', session_id)
            else:
                conn.close()
                self.send_html(self.render_template('login.html', {
                    'title': 'Log In',
                    'alert': '<div class="alert alert-error">Invalid credentials.</div>'
                }))
                
        elif path == '/profile':
            user = self.get_current_user()
            if not user:
                return self.send_error(403, "Not logged in")
                
            math = get_val('math_grade')
            eng = get_val('english_grade')
            sci = get_val('sciences_grade')
            hum = get_val('humanities_grade')
            ints = get_val('interests')
            
            # Avoid invalid updates
            if len(math) > 2: math = None
            if len(eng) > 2: eng = None
            if len(sci) > 2: sci = None
            if len(hum) > 2: hum = None
            
            conn = get_db_connection()
            conn.execute("""
                UPDATE users 
                SET math_grade=?, english_grade=?, sciences_grade=?, humanities_grade=?, interests=?
                WHERE id=?
            """, (math, eng, sci, hum, ints, user['id']))
            conn.commit()
            conn.close()
            
            self.send_redirect('/profile?msg=success')
            
        elif path == '/admin/add_scholarship':
            user = self.get_current_user()
            if not user or user['is_admin'] != 1:
                return self.send_error(403, "Forbidden")
                
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO scholarships (name, provider, description, eligibility_criteria, deadline, link)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (get_val('name'), get_val('provider'), get_val('description'), get_val('eligibility_criteria'), get_val('deadline'), get_val('link')))
            conn.commit()
            conn.close()
            self.send_redirect('/admin?msg=added')
            
        else:
            self.send_error(404, "Not Found")

if __name__ == "__main__":
    handler = PortalRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"Serving at http://localhost:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        print(f"Error starting server: {e}")
