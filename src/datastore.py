from peewee import SqliteDatabase,IntegrityError,DoesNotExist,MySQLDatabase
from data_models import *
from configurations import genConfig 
import random
import json as j
import datetime


class DataStore:
    def __init__(self):


        config=genConfig()
        self.parameters=config
        match config.DB_TYPE:
            case 'sqlite':
                self.db=SqliteDatabase(config.DB_PATH)
            case 'mariadb':
                self.db=MySQLDatabase(config.DB_NAME, user=config.DB_USER, password=config.DB_PWD,
                         host=config.DB_HOST, port=config.DB_PORT,charset='utf8')
        self.db.bind(self.parameters.DB_TABLES)
        
        
    
    def init_db(self):
        db = self.db.create_tables(self.parameters.DB_TABLES)
        return db
    
    def add_table(self,table):
        db=self.db.create_tables([table])
        return db
        
    def add_grade_distribution(self,grade:grade,distribution:list):
        json_distribution=j.dumps(distribution)
        try:
            new_grade_distribution=gradeDistribution.create(grade=grade,distribution=json_distribution)
        except IntegrityError:
            return False
        return new_grade_distribution
    
    def get_current_distribution(self,grade:grade):
        try:
            current_distribution=gradeDistribution.get(gradeDistribution.grade==grade,gradeDistribution.current==True)
        except DoesNotExist:
            return [None,None]
        return [j.loads(current_distribution.distribution),current_distribution]
   
    
    def add_desk(self,classroom:classroom,x:int,y:int):
        try:
            new_desk=desk.create(classroom=classroom,x=x,y=y)
        except IntegrityError:
            return False
        return new_desk

    def remove_desk(self,classroom:classroom,x:int,y:int):
        try:
            qr=desk.delete().where(desk.classroom==classroom,desk.x==x,desk.y==y)
            qr.execute()
        except DoesNotExist:
            print("Desk not found")
            return False
        return True
    
    def get_desk(self,classroom:classroom,x:int,y:int):
        try:
            data=(desk.select().where(desk.classroom==classroom,desk.x==x,desk.y==y))
            if len(data)>0:
                return data[0]
            else: return None
        except DoesNotExist:
            return None
        
        
    def get_desks(self,classroom:classroom):
        return None
    
    def add_desk_student(self,desk:desk,student:user):
        try:
            new_desk_student=deskStudent.create(desk=desk,student=student)
        except IntegrityError:
            return False
        return new_desk_student 
    
            
    def add_classroom(self,room_code,name,seats=22):
        try:
            new_classroom=classroom.create(room_code=room_code,name=name,seats=seats)
        except IntegrityError:
            return False
        return new_classroom
       
    
    def get_classroom(self,code):  
        try:
            classroom_data=classroom.get(classroom.room_code==code)
        except DoesNotExist:
            return None
        return classroom_data
    
    
    def add_tag_reader(self,name,ip_address,location: classroom,secret):
        try:
            new_tag_reader=tagReader.create(name=name,ip_address=ip_address,location=location,secret=secret)
        except IntegrityError:
            return False
        return new_tag_reader
    
    def get_tag_reader(self,name):
        try:
            tag_reader=tagReader.get(tagReader.name==name)
        except DoesNotExist:
            return None
        return tag_reader
    
    def add_tag(self,tag_id,user:user):
        try:
            new_tag=tag.create(tag_id=tag_id,user=user)
        except IntegrityError:
            return False
        return new_tag
    
    def get_tag(self,tag_id):
        try:
            tag_data=tag.get(tag.tag_id==tag_id)
        except DoesNotExist:
            return None
        return tag_data
    
    
    def add_grade(self,name):
        try:
            new_grade=grade.create(name=name)
        except IntegrityError:
            return False
        return new_grade
    
    def get_grade(self,name):
        try:
            grade_data=grade.get(grade.name==name)
        except DoesNotExist:
            return None
        return grade_data
    
      
    def add_user(self,username:str,grade:grade,surname:str='test',name:str='test',picture:str='test_student.png'):
        try:
            new_user=user.create(username=username,grade=grade,role='user',name=name,surname=surname,picture=picture)
        except IntegrityError:
            return False
        return new_user
    
    def get_user(self,username):
        try:
            user_data=user.get(user.username==username)
        except DoesNotExist:
            return None
        return user_data
    
    def add_tag_scan(self,tag:tag,tag_reader:tagReader):
        try:
            new_tag_scan=tagScan.create(tag=tag,tagReader=tag_reader)
        except IntegrityError:
            return False
        return new_tag_scan
    
    def add_roster(self,name):
        
        code=str(datetime.datetime.now().timestamp())
        try:
            new_roster=roster.create(code=code,name=name)
        except IntegrityError:
            return False
        return new_roster
       
    def get_roster(self,code):
        try:
            roster_data=roster.get(roster.code==code)
        except DoesNotExist:
            return None
        return roster_data
    
    def get_rosters(self):
        try:
            rosters=roster.select()
        except DoesNotExist:
            return None
        return rosters
    
     
    def add_tag_roster(self,tag:tag,roster:roster):
        try:
            new_tag_roster=tagRoster.create(tag=tag,roster=roster)
        except IntegrityError:
            return False
        return new_tag_roster
    
    
    def get_roster_tags(self,code):
        try:
            current_roster=roster.get(roster.code==code)
            tags=tagRoster.select(tagRoster.roster,tagRoster.tag).where(tagRoster.roster==current_roster).order_by(tagRoster.date)
        except DoesNotExist:
            return None
        return tags
    
    
    def get_tag_roster(self,tag:tag,roster:roster):
        try:
            tagscan_roster_data=tagRoster.get(tagRoster.tag==tag,tagRoster.roster==roster)
        except DoesNotExist:
            return None
        return tagscan_roster_data
    
    def remove_tagscan_roster(self,tag:tagScan,roster:roster):
        to_remove=self.get_tag_roster(tag,roster)
        to_remove.delete_instance()
        
        
            