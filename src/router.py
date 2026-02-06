from dataclasses import dataclass, field
import flet as ft
from configurations import genConfig
from reader import TagReader
from classroom import Classroom,Grade
from datastore import DataStore
from tagmanagement import Rosters


config=genConfig()


@ft.observable
@dataclass
class RouterState:
    route:str
    torender: bool=False
    database:DataStore = DataStore()
    reader:TagReader=field(init=False)
    classroom:Classroom=field(init=False)
    rosters: Rosters=field(init=False)
    
    
    def __post_init__(self):
        self.reader=TagReader(config.DEFAULT_READER,database=self.database)
        self.classroom=Classroom(name="first classroom",code="1.1",database=self.database,grade_name="1C")
        self.rosters=Rosters(database=self.database)
        
    
    async def route_change(self, e: ft.RouteChangeEvent):
        
        print("Route changed from:", self.route, "to:", e.route)
        self.route = e.route
        troute = ft.TemplateRoute(self.route)
              
        if troute.match("/lab/:id"):
            pass
                        
            
    async def view_popped(self, e: ft.ViewPopEvent):
        print("View popped")
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route(views[-2].route)

    def set_render(self):
        self.torender=True