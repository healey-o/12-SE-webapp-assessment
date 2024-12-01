from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash
from setup_db import User, Task, Group
import uuid
import datetime

#This file clears the database and creates example users, groups and tasks in the database
#Used to allow easy demonstration of the application and its features
#Users: 
#username: user1, password: password1
#username: user2, password: password2

engine = create_engine('sqlite:///userdata.db')
Session = sessionmaker(bind=engine)
sessionDb = Session()

# Clear the database
metadata = MetaData()
metadata.reflect(bind=engine)
for table in reversed(metadata.sorted_tables):
    sessionDb.execute(table.delete())
sessionDb.commit()

# Add example users
user1 = User(id=str(uuid.uuid4()), username='user1', password=generate_password_hash('password1'))
user2 = User(id=str(uuid.uuid4()), username='user2', password=generate_password_hash('password2'))
sessionDb.add(user1)
sessionDb.add(user2)

print("Users added successfully")

# Add example groups
groups = [
    Group(group_id=str(uuid.uuid4()), group_name='Maths', user_id=user1.id),
    Group(group_id=str(uuid.uuid4()), group_name='Science', user_id=user2.id),
    Group(group_id=str(uuid.uuid4()), group_name='History', user_id=user1.id),
    Group(group_id=str(uuid.uuid4()), group_name='Art', user_id=user2.id),
    Group(group_id=str(uuid.uuid4()), group_name='Music', user_id=user1.id),
    Group(group_id=str(uuid.uuid4()), group_name='Sports', user_id=user2.id),
    Group(group_id=str(uuid.uuid4()), group_name='School', user_id=user1.id),
    Group(group_id=str(uuid.uuid4()), group_name='School', user_id=user2.id),
    Group(group_id=str(uuid.uuid4()), group_name='Personal', user_id=user1.id),
    Group(group_id=str(uuid.uuid4()), group_name='Personal', user_id=user2.id)
]

for group in groups:
    sessionDb.add(group)

print("Groups added successfully")

# Add example tasks
tasks = [
    Task(task_id=str(uuid.uuid4()), name='Maths Exam', details='Complete the maths exam by next week', due_date=datetime.datetime(2024, 12, 5), user_id=user1.id, group_id=groups[0].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Science Project', details='Submit the science project by next month', due_date=datetime.datetime(2024, 12, 15), user_id=user2.id, group_id=groups[1].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='History Essay', details='Write an essay on World War II', due_date=datetime.datetime(2024, 12, 20), user_id=user1.id, group_id=groups[2].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Art Assignment', details='Create a painting for the art class', due_date=datetime.datetime(2024, 12, 25), user_id=user2.id, group_id=groups[3].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Music Practice', details='Practice the piano for 1 hour', due_date=datetime.datetime(2024, 12, 30), user_id=user1.id, group_id=groups[4].group_id, completed=False, repeat='daily', important=True),
    Task(task_id=str(uuid.uuid4()), name='Sports Training', details='Attend football training session', due_date=datetime.datetime(2024, 12, 10), user_id=user2.id, group_id=groups[5].group_id, completed=False, repeat='weekly', important=False),
    Task(task_id=str(uuid.uuid4()), name='School Meeting', details='Parent-teacher meeting at school', due_date=datetime.datetime(2024, 12, 12), user_id=user1.id, group_id=groups[6].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Personal Development', details='Read a book on personal development', due_date=datetime.datetime(2024, 12, 18), user_id=user2.id, group_id=groups[7].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Maths Homework', details='Complete the maths homework', due_date=datetime.datetime(2024, 12, 8), user_id=user1.id, group_id=groups[0].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Science Quiz', details='Prepare for the science quiz', due_date=datetime.datetime(2024, 12, 22), user_id=user2.id, group_id=groups[1].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='History Presentation', details='Prepare a presentation on ancient civilizations', due_date=datetime.datetime(2024, 12, 28), user_id=user1.id, group_id=groups[2].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Art Exhibition', details='Visit the art exhibition in the city', due_date=datetime.datetime(2024, 12, 14), user_id=user2.id, group_id=groups[3].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Music Theory', details='Study music theory for the upcoming test', due_date=datetime.datetime(2024, 12, 16), user_id=user1.id, group_id=groups[4].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Sports Event', details='Participate in the school sports event', due_date=datetime.datetime(2024, 12, 19), user_id=user2.id, group_id=groups[5].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='School Project', details='Work on the school group project', due_date=datetime.datetime(2024, 12, 21), user_id=user1.id, group_id=groups[6].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Personal Goal Setting', details='Set personal goals for the next year', due_date=datetime.datetime(2024, 12, 23), user_id=user2.id, group_id=groups[7].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Maths Revision', details='Revise maths topics for the final exam', due_date=datetime.datetime(2024, 12, 24), user_id=user1.id, group_id=groups[0].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Science Experiment', details='Conduct a science experiment at home', due_date=datetime.datetime(2024, 12, 26), user_id=user2.id, group_id=groups[1].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='History Research', details='Research on the history of the Renaissance', due_date=datetime.datetime(2024, 12, 27), user_id=user1.id, group_id=groups[2].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Art Class', details='Attend the art class on modern art', due_date=datetime.datetime(2024, 12, 29), user_id=user2.id, group_id=groups[3].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='Music Composition', details='Compose a piece of music for the class', due_date=datetime.datetime(2024, 12, 31), user_id=user1.id, group_id=groups[4].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Sports Practice', details='Practice basketball for the upcoming match', due_date=datetime.datetime(2024, 12, 11), user_id=user2.id, group_id=groups[5].group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='School Assignment', details='Complete the school assignment on time', due_date=datetime.datetime(2024, 12, 13), user_id=user1.id, group_id=groups[6].group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Personal Reflection', details='Reflect on personal achievements and challenges', due_date=datetime.datetime(2024, 12, 17), user_id=user2.id, group_id=groups[7].group_id, completed=False, repeat='none', important=False)
]

for task in tasks:
    sessionDb.add(task)

print("Tasks added successfully")

sessionDb.commit()