import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
import datetime
import time
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

# Database connection
if os.getenv("TESTING") == "true":
    db = SqliteDatabase(':memory:')
else:
    db = MySQLDatabase(
        os.getenv("MYSQL_DATABASE", "myportfoliodb"),
        user=os.getenv("MYSQL_USER", "myportfolio"),
        password=os.getenv("MYSQL_PASSWORD", "mypassword"),
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=3306
    )

# TimelinePost model definition
class TimelinePost(Model):
    id = AutoField()
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

# Initialize database connection
def init_db():
    try:
        db.connect()
        db.create_tables([TimelinePost], safe=True)
        print(f"Database connection successful: {db}")
    except Exception as e:
        print(f"Database connection failed: {e}")

# Only initialize database if not in testing mode
if os.getenv("TESTING") != "true":
    init_db()

# Rate limiting storage
rate_limit_storage = {}

# Ensure db connection per request
@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

base_url = "/"

navigation_items = [
    {'name': 'Home', 'url': base_url + '#profile', 'active': False},
    {'name': 'Experience', 'url': base_url + '#work-experience', 'active': False},
    {'name': 'Education', 'url': base_url + '#education', 'active': False},
    {'name': 'Hobbies', 'url': '/hobbies', 'active': False},
    {'name': 'Timeline', 'url': '/timeline', 'active': False},
    {'name': 'Visited Places', 'url': base_url + '#visited-places', 'active': False},
]

def get_navigation(current_page):
    nav_items = []
    for item in navigation_items:
        nav_item = item.copy()
        nav_item['active'] = (nav_item['url'] == current_page)
        nav_items.append(nav_item)
    return nav_items

# Data structures for dynamic content
work_experiences = [
    {
        'title': 'Site Reliability Engineer',
        'company': 'MLH Fellowship',
        'duration': 'June 2025 - Present',
        'achievements': [
            'Selected for highly competitive MLH Fellowship (2.5% acceptance rate)',
            'Focused on open-source DevOps and reliability engineering',
            'Collaborating in mentored pod for production-grade backend/SRE projects'
        ]
    },
    {
        'title': 'Google Summer of Code Contributor',
        'company': 'Google Summer of Code, CHAOSS/Augur Project',
        'duration': 'June 2025 - Present',
        'achievements': [
            'Accepted into GSoC, Google-sponsored open-source program',
            'Enhanced LDA/HDP topic modeling pipelines and metadata versioning',
            'Developed visualization using Python (Gensim, pyLDAvis) and PostgreSQL'
        ]
    },
    {
        'title': 'Software Engineer',
        'company': 'Quantum Harbour IT Systems Limited',
        'duration': 'March 2025 - March 2025',
        'achievements': [
            'Designed and implemented core features including dynamic inspection forms with SwiftUI',
            'Developed camera/photo upload, DWG and file handling, offline data storage',
            'Used Swift, MVVM architecture, and Core Data for iOS development'
        ]
    },
    {
        'title': 'Graduate Teaching Assistant',
        'company': 'National University of Ireland Galway',
        'duration': 'October 2024 - December 2024',
        'achievements': [
            'Supported students in completing Java coding assignments',
            'Debugged complex software development problems during lab sessions',
            'Assisted with two modules (CT and CT)'
        ]
    }
]

education = [
    {
        "degree": "MSc in Software Development",
        "school": "National University of Ireland Galway",
        "duration": "2023 - 2025",
        "achievements": [
            "Relevant Coursework: Computing Architecture & Operating Systems, Internet Programming",
            "Algorithmics & Logical Methods, Programming I, Databases, Software Engineering",
            "Object Oriented Software Design & Development, Computer Networks and Data Communications",
            "Principles of Machine Learning, Programming and Tools of AI, Graphics & Image Processing"
        ]
    }
]

hobbies = [
    {
        'name': 'Hackathons',
        'description': 'Love participating in coding competitions and hackathons.',
        'details': 'Achieved 3rd Prize in iTwin Good Championship by developing smart parking management system. Experience with React Native, AWS, and real-time data processing.',
        'icon_color': '#d4851a'
    },
    {
        'name': 'Open Source',
        'description': 'Contributing to open source projects and building side projects.',
        'details': 'Active contributor to Google Summer of Code with CHAOSS/Augur Project. Working on LDA/HDP topic modeling pipelines and visualization using Python.',
        'icon_color': '#0c59ff'
    }
]

visited_locations = [
]

@app.route('/')
def index():
    return render_template('index.html',
                         title="MLH Fellow",
                         url=os.getenv("URL"),
                         name="JIAHONG LIN",
                         role="Site Reliability Engineer",
                         about_text="I am a passionate software engineer with expertise in full-stack development, machine learning, and DevOps. Currently working as a Site Reliability Engineer at MLH Fellowship and contributing to Google Summer of Code with CHAOSS/Augur Project. I specialize in Python, React, TypeScript, and cloud technologies including AWS and Railway. Testing SSH connection with updated RSA key!",
                         work_experiences=work_experiences,
                         education=education,
                         hobbies=hobbies,
                         navigation=get_navigation('/'),
                         visited_locations=visited_locations
                         )

@app.route('/hobbies')
def hobbies_page():
    return render_template('hobbies.html',
                         title="My Hobbies",
                         url=os.getenv("URL"),
                         hobbies=hobbies,
                         navigation=get_navigation('/hobbies'))

@app.route('/map')
def map_page():
    return render_template('map.html',
                         title="Places I've Visited",
                         url=os.getenv("URL"),
                         visited_locations=visited_locations,
                         navigation=get_navigation('/map'))

@app.route('/timeline')
def timeline_page():
    return render_template('timeline.html',
                         title="Timeline",
                         url=os.getenv("URL"),
                         navigation=get_navigation('/timeline'))

# POST endpoint to create a timeline post
@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    # Rate limiting: 1 request per minute per IP (disabled during testing)
    if os.getenv("TESTING") != "true":
        global rate_limit_storage
        client_ip = request.remote_addr
        current_time = time.time()
        
        # Clean old entries (older than 1 minute)
        rate_limit_storage = {ip: timestamp for ip, timestamp in rate_limit_storage.items() 
                             if current_time - timestamp < 60}
        
        # Check if this IP has made a request in the last minute
        if client_ip in rate_limit_storage:
            return jsonify({
                'error': 'Rate limit exceeded. Please wait 1 minute before making another request.',
                'rate_limit': '1 request per minute'
            }), 429
        
        # Record this request
        rate_limit_storage[client_ip] = current_time
    
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')
    
    # Validate input
    if not name or name.strip() == '':
        return jsonify({'error': 'Invalid name'}), 400
    
    if not content or content.strip() == '':
        return jsonify({'error': 'Invalid content'}), 400
    
    # Basic email validation
    if not email or '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'Invalid email'}), 400
    
    timeline_post = TimelinePost.create(
        name=name,
        email=email,
        content=content
    )
    return model_to_dict(timeline_post), 201

# GET endpoint to retrieve all timeline posts
@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return jsonify([model_to_dict(post) for post in posts])

# DELETE endpoint to delete a timeline post by id
@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        post = TimelinePost.get(TimelinePost.id == post_id)
        post.delete_instance()
        return jsonify({'message': f'Timeline post {post_id} deleted successfully'}), 200
    except TimelinePost.DoesNotExist:
        return jsonify({'error': f'Timeline post with ID {post_id} not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete timeline post: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
