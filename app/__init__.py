import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Data structures for dynamic content
work_experiences = [
    {
        'title': 'Senior Software Developer',
        'company': 'TechCorp Solutions',
        'duration': 'January 2020 - Present',
        'achievements': [
            'Led the development of cloud-native applications using AWS services, resulting in 40% improved scalability',
            'Implemented CI/CD pipelines using GitHub Actions and AWS CodePipeline',
            'Mentored junior developers and conducted code reviews to maintain high code quality'
        ]
    },
    {
        'title': 'Software Developer',
        'company': 'DataTech Systems',
        'duration': 'June 2017 - December 2019',
        'achievements': [
            'Developed and maintained data analytics platforms serving over 100,000 users',
            'Optimized database queries resulting in 60% faster response times',
            'Collaborated with cross-functional teams to deliver features on schedule'
        ]
    }
]

# Education data structure - will be populated by other team members
education = [
    {
        "degree": "Master of Science in Software Engineering",
        "school": "University of Technology",
        "duration": "August 2077 - May 2077",
        "achievements": [
            "Specialized in Cloud Computing and Distributed Systems",
            "Thesis: 'Optimizing Cloud-Based Data Processing for Large-Scale Applications'",
            "Participated in various hackathons and coding competitions"
        ]
    },
    {
        "degree": "Bachelor of Science in Computer Science",
        "school": "Tech University",
        "duration": "August 1337 - May 1337",
        "achievements": [
            "Graduated with Honors",
            "Relevant Coursework: Data Structures, Algorithms, Database Systems, Cloud Computing",
            "Capstone Project: Developed a cloud-based application for real-time data analytics"
        ]
    }
]
hobbies = [
    {
        'name': 'Photography',
        'description': 'Passionate about capturing moments and exploring different perspectives through the lens.',
        'details': 'I specialize in landscape and street photography. My favorite time to shoot is during golden hour, and I love experimenting with long exposure techniques.',
        'icon_color': '#1C539F'
    },
    {
        'name': 'Hiking',
        'description': 'Love exploring nature trails and challenging myself with different terrains.',
        'details': 'I regularly explore local trails and have completed several challenging mountain hikes. My goal is to hike at least one new trail every month.',
        'icon_color': '#d4851a'
    },
    {
        'name': 'Open Source',
        'description': 'Contributing to open source projects and building side projects.',
        'details': 'I actively contribute to various open source projects, mainly focusing on Python and JavaScript libraries. I believe in the power of community-driven development.',
        'icon_color': '#0c59ff'
    }
]
visited_locations = [
    {
        "name": "Paris, France",
        "coords": [48.8566, 2.3522],
        "description": "Visited the Eiffel Tower and Louvre Museum"
    },
    {
        "name": "Tokyo, Japan",
        "coords": [35.6762, 139.6503],
        "description": "Explored Shibuya and enjoyed authentic sushi"
    },
    {
        "name": "New York, USA",
        "coords": [40.7128, -74.0060],
        "description": "Saw Times Square and Central Park"
    },
    {
        "name": "Sydney, Australia",
        "coords": [-33.8688, 151.2093],
        "description": "Visited the Opera House and Bondi Beach"
    },
    {
        "name": "Bermuda Triangle",
        "coords": [25.0000, -71.0000],
        "description": "Met some aliens and they were friendly! They even gave me a ride in their spaceship."
    }
]


@app.route('/')
def index():
    return render_template('index.html',
                         title="MLH Fellow",
                         url=os.getenv("URL"),
                         name="Luke Skywalker",
                         role="Software Developer",
                         about_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                         work_experiences=work_experiences,
                         education=education,
                         hobbies=hobbies,
                         visited_locations=visited_locations
                         )

@app.route('/hobbies')
def hobbies_page():
    return render_template('hobbies.html',
                         title="My Hobbies",
                         url=os.getenv("URL"),
                         hobbies=hobbies)
