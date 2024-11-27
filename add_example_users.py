from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash
from setup_db import User, Task, Group
import uuid
import datetime

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

# Add example groups
group1 = Group(group_id=str(uuid.uuid4()), group_name='Maths', user_id=user1.id)
group2 = Group(group_id=str(uuid.uuid4()), group_name='Science', user_id=user2.id)
group3 = Group(group_id=str(uuid.uuid4()), group_name='History', user_id=user1.id)
group4 = Group(group_id=str(uuid.uuid4()), group_name='Art', user_id=user2.id)
group5 = Group(group_id=str(uuid.uuid4()), group_name='School', user_id=user1.id)
group6 = Group(group_id=str(uuid.uuid4()), group_name='Personal', user_id=user2.id)

sessionDb.add(group1)
sessionDb.add(group2)
sessionDb.add(group3)
sessionDb.add(group4)
sessionDb.add(group5)
sessionDb.add(group6)

print("Groups added successfully")

# Add example tasks
tasks = [
    Task(task_id=str(uuid.uuid4()), name='Maths Exam', details='Complete the maths exam by next week', due_date=datetime.datetime(2024, 12, 5), user_id=user1.id, group_id=group1.group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Science Project', details='Submit the science project report', due_date=datetime.datetime(2024, 12, 6), user_id=user2.id, group_id=group2.group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='History Essay', details='Write an essay on World War II', due_date=datetime.datetime(2024, 12, 7), user_id=user1.id, group_id=group3.group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Art Assignment', details='Create a painting for the art class', due_date=datetime.datetime(2024, 12, 8), user_id=user2.id, group_id=group4.group_id, completed=False, repeat='none', important=False),
    Task(task_id=str(uuid.uuid4()), name='School Homework', details='Complete the school homework', due_date=datetime.datetime(2024, 12, 9), user_id=user1.id, group_id=group5.group_id, completed=False, repeat='weekly', important=False),
    Task(task_id=str(uuid.uuid4()), name='Workout', details='Go for a workout session', due_date=datetime.datetime(2024, 12, 10), user_id=user2.id, group_id=group6.group_id, completed=False, repeat='daily', important=True),
    Task(task_id=str(uuid.uuid4()), name='School Project', details='Work on the school project', due_date=datetime.datetime(2024, 12, 11), user_id=user1.id, group_id=group5.group_id, completed=False, repeat='monthly', important=True),
    Task(task_id=str(uuid.uuid4()), name='Reading', details='Read a book for personal development', due_date=datetime.datetime(2024, 12, 12), user_id=user2.id, group_id=group6.group_id, completed=False, repeat='weekly', important=False),
    Task(task_id=str(uuid.uuid4()), name='Grocery Shopping', details='Buy groceries for the week', due_date=datetime.datetime(2024, 12, 13), user_id=user1.id, group_id=group6.group_id, completed=False, repeat='weekly', important=False),
    Task(task_id=str(uuid.uuid4()), name='Doctor Appointment', details='Visit the doctor for a check-up', due_date=datetime.datetime(2024, 12, 14), user_id=user2.id, group_id=group6.group_id, completed=False, repeat='none', important=True),
    Task(task_id=str(uuid.uuid4()), name='Team Meeting', details='Attend the team meeting at work', due_date=datetime.datetime(2024, 12, 15), user_id=user1.id, group_id=group5.group_id, completed=False, repeat='monthly', important=True),
    Task(task_id=str(uuid.uuid4()), name='Yoga Class', details='Participate in the yoga class', due_date=datetime.datetime(2024, 12, 16), user_id=user2.id, group_id=group6.group_id, completed=False, repeat='daily', important=False)
]

for task in tasks:
    sessionDb.add(task)

print("Tasks added successfully")

sessionDb.commit()