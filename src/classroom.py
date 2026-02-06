from dataclasses import dataclass, field
from datastore import DataStore
from data_models import user,desk,classroom,deskStudent,grade
import flet as ft
from combinatorial_utils import get_list_derangment,pad_list
from exports import export_svg
import time


@ft.observable
@dataclass
class Desk:
    room:classroom
    database: DataStore
    coordinates:tuple=(0,0)
    data:desk=field(init=False)
    color:tuple=field(init=False)
    used:bool=True
    callback:callable=None
        
    def __post_init__(self):
        self.color=(255,0,0)
        data=self.database.get_desk(self.room,self.coordinates[0],self.coordinates[1])
        if data:
            self.data=data
            self.used=data.used
        else:
            self.data=self.database.add_desk(self.room,self.coordinates[0],self.coordinates[1])
    def toggle_usage(self):
        self.used=not self.used
        self.data.used=not self.data.used
        if self.callback:
           self.callback() 
        self.data.save() 


@ft.observable
@dataclass
class Grade:
    name: str
    database: DataStore
    data:grade=field(init=False)
    distribution:list=field(init=False)
    students:list=field(init=False)
    callback:callable=None
    
    def __post_init__(self):
        data=self.database.get_grade(self.name)
        if data:
            self.data=data
            self.distribution=self.database.get_current_distribution(data)
            self.students=sorted([[student.id,student.username,student.name,student.surname,student.picture] for student in data.students if student.role=='user'],key=lambda x: x[0])
            
        else:
            self.data=self.database.add_grade(self.name)
            
    def add_distribution(self):
        
        if not self.distribution[0]:
           distribution=get_list_derangment(len(self.students))
        else:
           distribution=get_list_derangment(len(self.students),self.distribution[0])
         
        self.distribution[0]=distribution
        
        
        if self.distribution[1]:
            self.distribution[1].current=False
            self.distribution[1].save()
        
        self.distribution[1]=self.database.add_grade_distribution(self.data,distribution)
        
        if self.callback:
           self.callback() 
    
    def get_distribution(self):
        return self.database.get_current_distribution(self.data)[0]
    
    def get_students(self):
        return self.students
    
    
    
        
@ft.observable
@dataclass
class Classroom:
    code:str
    database: DataStore
    grade_name:str
    name:str="test"
    desks:dict[tuple[int,int]:desk]=field(default_factory=dict)
    data:classroom=field(init=False)
    grade:Grade=field(init=False)
    distributed_students:list=field(init=False)
    edit:bool=False
    
    def __post_init__(self):
        data=self.database.get_classroom(self.code)
        if data:
            self.data=data
            self.name=data.name
            self.code=data.room_code
            self.desks={(desk.x,desk.y):Desk(coordinates=(desk.x,desk.y),database=self.database,room=self.data,callback=self.update_distributed_students) for desk in data.desks}
            self.grade=Grade(name=self.grade_name,database=self.database,callback=self.update_distributed_students)
            self.distributed_students=self.get_distributed_students()
        else:
            self.database.add_classroom(self.code,self.name)
        
    def add_desk(self,x,y):
        self.desks[(x,y)]=Desk(coordinates=(x,y),database=self.database,room=self.data,callback=self.update_distributed_students)
    
    def get_used_desks(self):
        return sorted( [[10*desk.coordinates[0]+desk.coordinates[1],desk] for desk in self.desks.values() if desk.used],key =lambda x: x[0])
    
    def remove_desk(self,x,y):
        self.database.remove_desk(self.data,x,y)
        del self.desks[(x,y)]
    
    def update_distributed_students(self):
        self.distributed_students=self.get_distributed_students()
    
    def save_map(self,filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        file=export_svg(self.distributed_students,self.desks,timestr)
        
        
        with open(filename,"w") as f:
            f.write(str(file)   )
        
        
    def get_distributed_students(self):
        students=self.grade.get_students()
        used_desks=pad_list(topad=self.get_used_desks(),origin=students,padelement=[0,0])
        distribution=pad_list(topad=self.grade.get_distribution(),origin=students,padelement=0)
         
          
        
        return [[students[i],used_desks[distribution[i]][1]] for i in range(len(students))    ]
    
    