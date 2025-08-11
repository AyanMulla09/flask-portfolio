import os
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import MySQLDatabase, SqliteDatabase, Model, CharField, TextField, DateTimeField, DoesNotExist, AutoField
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

base_url = "/"

# Database configuration
if os.getenv("TESTING") == 'true':
    print("Running in test mode, using SQLite in-memory database")
    mydb = SqliteDatabase(':memory:')
else:
    # Try MySQL first, fallback to SQLite if MySQL is not available
    try:
        mydb = MySQLDatabase(
            os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=3306
        )
        # Test the connection
        mydb.connect()
        print("Connected to MySQL database")
    except Exception as e:
        print(f"MySQL connection failed: {e}")
        print("Falling back to SQLite database")
        mydb = SqliteDatabase('portfolio.db')
        mydb.connect()

class TimelinePost(Model):
    id = AutoField()
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb

# Connect to database and create tables
if not mydb.is_closed():
    mydb.close()
mydb.connect()
mydb.create_tables([TimelinePost], safe=True)
print("Database tables created successfully")

navigation_items = [
    {'name': 'Home', 'url': base_url + '#profile', 'active': False},
    {'name': 'Experience', 'url': base_url + '#work-experience', 'active': False},
    {'name': 'Education', 'url': base_url + '#education', 'active': False},
    {'name': 'Hobbies', 'url': '/hobbies', 'active': False},
    {'name': 'Visited Places', 'url': base_url + '#visited-places', 'active': False},
    {'name': 'Timeline', 'url': '/timeline', 'active': False},
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
        'title': 'Data Scientist Intern',
        'company': 'CeADAR - Ireland\'s Centre for AI',
        'duration': 'May 2025 - Present',
        'achievements': [
            'Built an automated research pipeline using LangGraph to discover, filter, and analyze academic papers from arXiv for research gap identification',
            'Integrated LLMs for intelligent topic generation and full-text analysis',
            'Engineered modular workflows using Python, Pydantic, and PDF processing tools for scalable, state-driven orchestration',
            'Designed multi-stage AI relevance filters and structured output pipelines to generate CSV/JSON research insights'
        ]
    },
    {
        'title': 'Production Engineering Fellow',
        'company': 'Major League Hacking X Meta',
        'duration': 'June 2025 - Present',
        'achievements': [
            'Selected for the competitive MLH Fellowship in collaboration with Meta to gain hands-on experience in production engineering',
            'Participated in weekly training sessions, programming challenges, and deep dives with Meta engineers on topics like scalability, CI/CD, and observability',
            'Built and maintained infrastructure components using Linux, Python, Docker, and monitoring tools',
            'Collaborated in an agile team to develop reliable backend systems and debug production-level issues with other fellows'
        ]
    },
    {
        'title': 'Product Support Engineer',
        'company': 'VMobi Solutions Private Limited',
        'duration': 'Oct. 2022 - July 2024',
        'achievements': [
            'Utilized expertise in Networking, configuring web servers, and managing control panels to provide technical support to customers',
            'Automated email workflows to improve message handling and reduce manual errors',
            'Identified and resolved technical issues pertaining to the product, DNS records, and SMTP configurations',
            'Collaborated with developers to enhance customer experience; earned 500+ CSATs in 6 months'
        ]
    },
    {
        'title': 'Project Intern',
        'company': 'IMA-PG',
        'duration': 'Aug. 2021 - April 2022',
        'achievements': [
            'Collected and cleaned live machine data via PLC; stored results in a SQL database',
            'Built real-time dashboards with PHP and Chart.js to monitor packaging machine KPIs',
            'Deployed interface for global technician use and implemented alerting for proactive issue detection',
            'Successfully published a research paper based on the project performed during the internship'
        ]
    }
]

# Education data structure
education = [
    {
        "degree": "Master of Science in Computer Science",
        "school": "University College Dublin",
        "duration": "September 2024 - September 2025 (Expected)",
        "achievements": [
            "Specializing in advanced computer science topics including machine learning, data science, and software engineering",
            "Maintaining strong academic performance while gaining practical industry experience",
            "Actively participating in research projects and academic initiatives"
        ]
    },
    {
        "degree": "Bachelor of Engineering in Information Technology",
        "school": "University of Mumbai",
        "duration": "August 2018 - July 2022",
        "achievements": [
            "Completed comprehensive IT program covering software engineering, database systems, and networking",
            "Gained foundational knowledge in programming, data structures, algorithms, and system design",
            "Developed strong technical foundation that enabled successful transition to advanced studies and professional roles"
        ]
    }
]

# Projects data structure
projects = [
    {
        "name": "NewsFlash",
        "description": "AI-powered news aggregation and sentiment analysis platform",
        "technologies": ["Python", "Flask", "OpenAI API", "News API", "Natural Language Processing"],
        "achievements": [
            "Built an intelligent news aggregation system that collects articles from multiple sources",
            "Implemented AI-powered sentiment analysis to categorize news as positive, negative, or neutral",
            "Developed a clean, responsive web interface for browsing categorized news content",
            "Integrated multiple APIs to provide comprehensive news coverage and analysis"
        ],
        "github_url": "#",  # Add actual GitHub URL if available
        "demo_url": "#"     # Add actual demo URL if available
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
                         title="Ayan Mulla - Software Developer",
                         url=os.getenv("URL"),
                         name="Ayan Mulla",
                         role="Data Scientist & Software Engineer",
                         about_text="Passionate Data Scientist and Software Engineer with experience in machine learning, AI research, and production systems. Currently pursuing a Master's in Computer Science at University College Dublin while working as a Data Scientist Intern at CeADAR and Production Engineering Fellow at MLH x Meta. Skilled in Python, cloud technologies, and building scalable applications that solve real-world problems.",
                         work_experiences=work_experiences,
                         education=education,
                         projects=projects,
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
def map_page():  # Changed from hobbies_page
    return render_template('map.html',
                         title="Places I've Visited",
                         url=os.getenv("URL"),
                         visited_locations=visited_locations,  # Pass correct data
                         navigation=get_navigation('/map'))

@app.route('/api/timeline_post', methods=['POST'])
def timeline_post():
    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        content = request.form.get('content', '').strip()
        
        # Enhanced validation
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters long')
        elif len(name) > 50:
            errors.append('Name must be less than 50 characters')
        
        if not email:
            errors.append('Email is required')
        elif '@' not in email or '.' not in email.split('@')[-1]:
            errors.append('Please enter a valid email address')
        elif len(email) > 100:
            errors.append('Email is too long')
        
        if not content or len(content) < 10:
            errors.append('Content must be at least 10 characters long')
        elif len(content) > 500:
            errors.append('Content must be less than 500 characters')
        
        if errors:
            return {
                'error': 'Validation failed',
                'details': errors
            }, 400
        
        # Create the post
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        
        return {
            'success': True,
            'message': 'Post created successfully',
            'post': model_to_dict(timeline_post)
        }, 201
        
    except Exception as e:
        print(f"Error creating timeline post: {e}")
        return {
            'error': 'Internal server error',
            'message': 'Failed to create post. Please try again.'
        }, 500

@app.route('/api/timeline_posts', methods=['GET'])
def get_timeline_posts():
    try:
        posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        return {
            'success': True,
            'timeline_posts': [model_to_dict(p) for p in posts],
            'count': len(posts)
        }
    except Exception as e:
        print(f"Error fetching timeline posts: {e}")
        return {
            'error': 'Internal server error',
            'message': 'Failed to load posts. Please try again.',
            'timeline_posts': []
        }, 500
@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        post = TimelinePost.get(TimelinePost.id == post_id)
        post_data = model_to_dict(post)
        post.delete_instance()

        return {
            'success': True,
            'message': f'Timeline post deleted successfully',
            'deleted_post': post_data,
            'deleted_id': post_id
        }, 200

    except DoesNotExist:
        return {
            'error': 'Not found',
            'message': f'Timeline post with ID {post_id} not found'
        }, 404
    except Exception as e:
        print(f"Error deleting timeline post {post_id}: {e}")
        return {
            'error': 'Internal server error',
            'message': f'Failed to delete timeline post. Please try again.'
        }, 500

@app.route('/timeline')
def timeline_page():
    return render_template('timeline.html',
                         title="Timeline",
                        navigation=get_navigation('/timeline'),)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

