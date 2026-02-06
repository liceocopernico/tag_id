from dataclasses import dataclass, field
from datastore import DataStore
from data_models import user,roster,tag
from datetime import datetime
import flet as ft




@ft.observable
@dataclass
class User:
    first_name: str
    last_name: str

    def update(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name


@ft.observable
@dataclass
class Tag:
    tag_id: str
    database: DataStore
    data: tag=field(init=False)
    registered: bool=False
    owner: user=field(init=False)
    ord: int=0
    
    def __post_init__(self):
        current_tag:tag=self.database.get_tag(self.tag_id)
        if isinstance(self.__ord,property):
            self.__ord = 0 
        if current_tag:
            self.registered=True
            self.data=current_tag
            self.owner=current_tag.user
        else:
            print("Tag not registered")    
            
    @property
    def ord(self):
        return self.__ord
    
    @ord.setter
    def ord(self,new_ord):
        self.__ord=new_ord
        


@ft.observable
@dataclass
class Roster:
    database: DataStore
    code: str= ''
    name: str= field(init=False)
    tags: list[Tag] = field(default_factory=list)
    roster_data: roster = field(init=False)
    
    
    def __post_init__(self):
        
        if self.code:
            self.roster_data=self.database.get_roster(self.code)
            self.name=self.roster_data.name
            self.tags=[Tag(database=self.database,tag_id=data.tag.tag_id,ord=idx) for idx,data in enumerate(self.database.get_roster_tags(self.code))]

        else:
            self.name=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            self.roster_data=self.database.add_roster(self.name)
   
    def add_tag(self,tag:tag):
        self.tags.append(tag)
     
    def remove_tag(self,tag:Tag):
                       
        try:
            self.tags.remove(tag) 
        except Exception as e:
            print(e)
            print(f"{len(self.tags)} it seems I didn't remove anything")        
   
    def reorder_tags(self):
        self.tags=sorted(self.tags,key=lambda tag: tag.ord)
   
    def update(self,name):
        self.name=name
        self.roster_data.name=name
        self.roster_data.save()
        
    def get_tag(self,tag_id):
        return next((tag for tag in self.tags if tag.tag_id==tag_id), None)


@ft.observable
@dataclass
class Rosters:
    database: DataStore
    past_rosters: list[Roster] = field(default_factory=list)

    def __post_init__(self):
        self.past_rosters=self.database.get_rosters()
        
    def update(self):
        self.past_rosters=self.database.get_rosters()
    