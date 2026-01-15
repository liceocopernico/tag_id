from peewee import *
import datetime

class grade(Model):
    name=CharField(unique=True)
    session=DateTimeField(default=datetime.datetime.now)
    
class classroom(Model):
    room_code=CharField(unique=True)
    name=CharField()
    seats=IntegerField(default=21)
    

class tagReader(Model):
    name=CharField(unique=True)
    ip_address=CharField()
    last_seen=DateTimeField(default=datetime.datetime.now)
    last_scan=DateTimeField(default=datetime.datetime.now)
    location=ForeignKeyField(classroom,backref='tag_readers')
    secret=CharField()

class user(Model):
    username=CharField(unique=True)
    role=CharField(default='user')
    login_count=IntegerField(default=0)
    last_log=DateTimeField(default=datetime.datetime.now)
    access_token=CharField(default='')
    grade=ForeignKeyField(grade,backref='students')
    picture=CharField(default='test_student.png')
    name=CharField(default='test')
    surname=CharField(default='test')
    
class tag(Model):
    tag_id=CharField(unique=True)
    user=ForeignKeyField(user,backref='tags')
    
class timeTable(Model):
    classroom=ForeignKeyField(classroom,backref='timetable')
    grade=ForeignKeyField(grade,backref='timetable')
    day=CharField()
    hour=IntegerField()
    
class tagScan(Model):
    tag=ForeignKeyField(tag,backref='tag_scans')
    tagReader=ForeignKeyField(tagReader,backref='tag_scans')
    date=DateTimeField(default=datetime.datetime.now)
    
class roster(Model):
    code=CharField(unique=True)
    name=CharField(default='volunteers')
    date=DateTimeField(default=datetime.datetime.now)
    

class tagRoster(Model):    
    tag=ForeignKeyField(tag,backref='student_roaster')
    roster=ForeignKeyField(roster,backref='student_roaster')
    date=DateTimeField(default=datetime.datetime.now)
    class Meta:
        indexes = (
              (('tag', 'roster'), True),
        )

    