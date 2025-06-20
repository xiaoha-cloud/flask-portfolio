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

@app.route('/')
def index():
    return render_template('index.html',
                         title="MLH Fellow",
                         url=os.getenv("URL"),
                         name="Ace Perez",
                         role="Software Developer",
                         about_text="As a proficient expert in AWS and cloud-based solutions, I am specialized in developing advanced data analytics and DevOp solutions for scalable, distributed systems. My skill set is particularly strong in collaborative teamwork and problem-solving within Agile environments. I am keen to contribute my expertise to projects and collaborate with a team of skilled professionals.",
                         work_experiences=work_experiences,
                         education=education,

                         hobbies=hobbies)

@app.route('/hobbies')
def hobbies_page():
    return render_template('hobbies.html',
                         title="My Hobbies",
                         url=os.getenv("URL"),
                         hobbies=hobbies)
