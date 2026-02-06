from dataclasses import dataclass, field
from datastore import DataStore
from data_models import tagReader
import asyncio
import aioesphomeapi
from ping3 import ping
from datetime import datetime
import flet as ft
from tagmanagement import Tag,Roster
import random




@ft.observable
@dataclass
class TagReader:
    name: str
    database: DataStore
    reader_data: tagReader = field(init=False)
    current_roster: Roster = field(init=False)
    last_tag: str=""
    online: bool=False
    active:bool=False
    connected: bool=False
    test: str="test"
    logic: aioesphomeapi.ReconnectLogic |None = None
    rand_seed:int=random.randint(10,20)
        
    def __post_init__(self):
        self.reader_data=self.database.get_tag_reader(self.name)
        self.current_roster=None
             
    def current_roster_update(self,code):
       
        self.current_roster=Roster(code=code,database=self.database)
        
             
             
    def flush_roster(self):
        self.current_roster=None
                  
    def connect_reader(self):
        
        self.active=True
        reader_loop=asyncio.get_event_loop()
               
        try:
            reader_loop.create_task(self.is_online())
            reader_loop.create_task(self.get_reading())
            

        except KeyboardInterrupt:
            self.active=False
            pass
       
    def set_last_scan(self,time):
        self.reader_data.last_scan=time
        self.reader_data.save()
        
    def record_scan(self,tag_id):
        
           
        index= len(self.current_roster.tags) if self.current_roster else 0
        future_tag=self.current_roster.get_tag(tag_id) if self.current_roster else None
        current_tag: Tag= future_tag if future_tag else Tag(tag_id=tag_id,ord=index,database=self.database)
        
        
        
        if current_tag.registered:
            new_tag_scan=self.database.add_tag_scan(current_tag.data,self.reader_data)
            if not self.current_roster:
                self.current_roster=Roster(self.database)
            new_tag_roster=self.database.add_tag_roster(current_tag.data,self.current_roster.roster_data)      
            if not new_tag_roster:
                
                self.database.remove_tagscan_roster(current_tag.data,self.current_roster.roster_data)
                self.current_roster.remove_tag(current_tag)
            else:
                self.current_roster.add_tag(current_tag)
                
    async def get_reading(self):
        cli = aioesphomeapi.APIClient(self.reader_data.ip_address, 6053, None, noise_psk=self.reader_data.secret)
        
        
        def on_srv_stub(test):
           pass
                
        def on_srv_call1(esphome_data):
            print(esphome_data)
            if self.active:
                self.set_last_scan(datetime.now())
                if esphome_data.service=='esphome.tag_scanned':
                    print(esphome_data.data['tag_id'])
                    self.last_tag=esphome_data.data['tag_id']
                    self.record_scan(self.last_tag)
        
        async def on_disconnect(expected_disconnect: bool) -> None:
            print(expected_disconnect)
            print("DISCONNECTION")
            self.connected=False
            pass

        async def on_connect() -> None:
            print("CONNECTION")
            self.connected=True
            cli.subscribe_home_assistant_states_and_services(
            on_state=on_srv_stub,
            on_service_call=on_srv_call1,
            on_state_sub=on_srv_stub,
            on_state_request=on_srv_stub,
        )
            pass
        async def on_connect_error(test) -> None:
            print("CONNECTION ERROR")
            
            self.connected=False
            pass
        
        self.logic=aioesphomeapi.ReconnectLogic(
            client=cli,
            on_connect=on_connect,
            on_disconnect=on_disconnect,
            on_connect_error=on_connect_error,
            name=self.reader_data.name
            )
        
        #await cli.connect(login=True)
        await self.logic.start()
        await asyncio.sleep(5)
        
          
    async def is_online(self):
        print(f"reader rand seed {self.rand_seed}")
        while self.active:
        
            alive=ping(self.reader_data.ip_address,timeout=0.1)
            if self.logic:
                print(self.logic._connection_state)
            if alive:
                self.online=True
                self.reader_data.last_seen=datetime.now()
                self.reader_data.save()
                print(f"{self.name} is online")
                
            else:
                self.online=False
                
            await asyncio.sleep(3)
