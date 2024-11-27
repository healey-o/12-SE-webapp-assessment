from sqlalchemy import Column, String, Boolean, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import check_password_hash

#Create the database
Base = declarative_base()

class User(Base):
    __tablename__ = 'userdetails'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationships
    tasks = relationship('Task', back_populates='user')
    groups = relationship('Group', back_populates='user')

    # Check if the password is correct
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    details = Column(String)
    important = Column(Boolean, nullable=False)
    due_date = Column(DateTime, nullable=False)
    completed = Column(Boolean, nullable=False)
    repeat = Column(String, nullable=False)

    # Foreign keys
    user_id = Column(String, ForeignKey('userdetails.id'), nullable=False)
    group_id = Column(String, ForeignKey('groups.group_id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='tasks')
    groups = relationship('Group', back_populates='tasks')

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(String, primary_key=True, nullable=False)
    group_name = Column(String, nullable=False, unique=True)

    # Foreign keys
    user_id = Column(String, ForeignKey('userdetails.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='groups')
    tasks = relationship('Task', back_populates='groups')

engine = create_engine('sqlite:///userdata.db')
Base.metadata.create_all(engine)

print('Database created successfully.')