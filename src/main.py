from dataclasses import dataclass, field
from ping3 import ping
import flet as ft
from tagmanagement import Rosters
from reader import TagReader
from views import TagReaderView,RosterView,RostersView
from configurations import TagColor,genConfig

config=genConfig()
    
@ft.component
def App():
    tag_reader,_=ft.use_state(TagReader(config.DEFAULT_READER))
    rosters,_=ft.use_state(Rosters())
    connected,set_connected=ft.use_state(False)
    
    if not connected:
        set_connected(True)
        tag_reader.connect_reader()
    
    
    return ft.Container(
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Row(controls=[
                        TagReaderView(tag_reader),
                            ft.FloatingActionButton(
                                icon=ft.Icons.DELETE_ROUNDED,
                                content="Svuota",
                                on_click=lambda e:(tag_reader.flush_roster(),rosters.update()),
                                disabled=True if not tag_reader.current_roster else False,
                                disabled_elevation=0,
                                elevation=5,
                                bgcolor=TagColor.BUTTON,
                                foreground_color=TagColor.TEXT_LIGHT,
                                shape=ft.RoundedRectangleBorder(radius=3)
                                )
                ]),
                ft.Row(controls=[RostersView(rosters,tag_reader)]),
                
                ft.Row(controls=[RosterView(tag_reader.current_roster,rosters),]),
                             
                
                
                ]))
    
    
ft.run(lambda page: page.render(App))