from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import threading
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(InsecureRequestWarning)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///websites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="")
    url = db.Column(db.String(200), nullable=False)
    last_checked = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    response_time = db.Column(db.Float)

def check_website(url):
    try:
        start_time = time.time()
        # Check if it's a local IP address
        is_local_ip = any(url.startswith(prefix) for prefix in ['http://192.168.', 'https://192.168.', 'http://10.', 'https://10.', 'http://172.', 'https://172.'])
        
        # Use verify=False for local IPs to handle self-signed certificates
        response = requests.get(url, timeout=10, verify=not is_local_ip)
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds
        
        website = Website.query.filter_by(url=url).first()
        if website:
            website.last_checked = datetime.now()
            website.status = 'up' if response.status_code == 200 else 'down'
            website.response_time = response_time
            db.session.commit()
    except:
        website = Website.query.filter_by(url=url).first()
        if website:
            website.last_checked = datetime.now()
            website.status = 'down'
            website.response_time = None
            db.session.commit()

def monitor_websites():
    while True:
        websites = Website.query.all()
        for website in websites:
            check_website(website.url)
        time.sleep(60)  # Check every minute

@app.route('/')
def home():
    websites = Website.query.all()
    return render_template('index.html', websites=websites)

@app.route('/add_website', methods=['POST'])
def add_website():
    url = request.form.get('url')
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Extract a default name from the URL
    default_name = url.split('//')[-1].split('/')[0]
    if default_name.startswith('www.'):
        default_name = default_name[4:]
    
    website = Website(name=default_name, url=url, last_checked=None, status='pending')
    db.session.add(website)
    db.session.commit()
    
    # Check the website immediately
    check_website(url)
    
    return jsonify({'status': 'success'})

@app.route('/delete_website/<int:id>', methods=['POST'])
def delete_website(id):
    website = Website.query.get_or_404(id)
    db.session.delete(website)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/update_name/<int:id>', methods=['POST'])
def update_name(id):
    website = Website.query.get_or_404(id)
    new_name = request.form.get('name', '').strip()
    website.name = new_name
    db.session.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create all tables with the new schema
        db.create_all()
        # Start the monitoring thread
        monitor_thread = threading.Thread(target=monitor_websites, daemon=True)
        monitor_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False) 