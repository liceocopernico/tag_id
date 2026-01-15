import flet as ft
from reader import TagReader
from tagmanagement import Tag,Roster,Rosters
from configurations import TagColor


@ft.component
def TagView(tag: Tag,roster:Roster)->ft.Control:
   is_tag_over, set_is_tag_over = ft.use_state(False)

   
   def on_item_accept(e: ft.DragTargetEvent):
       tag.ord,e.src.data.ord=e.src.data.ord,tag.ord
       roster.reorder_tags()
       set_is_tag_over(False)
       
       

   return ft.Draggable(
                group="items",
                data=tag,
                content=ft.DragTarget(
                    group="items",
                    data=tag,
                    on_accept=on_item_accept,
                    on_will_accept=lambda e: set_is_tag_over(e.accept),
                    on_leave=lambda: set_is_tag_over(False),
                    content=ft.Container(
                        alignment=ft.Alignment.TOP_CENTER,
                        border_radius=10,
                        border=ft.Border.all(2, ft.Colors.GREY_500),
                        content=ft.Column(
                        controls=[
                                ft.Image(
                                        src=f"images/{tag.owner.picture}",
                                        width=200,
                                        height=200,
                                        fit=ft.BoxFit.SCALE_DOWN,
                                ),])))
                )

        
@ft.component
def TagReaderView(tag_reader: TagReader)->ft.Control:
       
    return ft.Container(
                bgcolor=TagColor.BACKGROUND,
                alignment=ft.Alignment.CENTER,
                border_radius=3,
                border=ft.Border.all(2, ft.Colors.GREY_500),
                padding=15,
                content=ft.Row(
                controls=[  ft.Text(f"Lettore: {tag_reader.name} ",
                                    weight=ft.FontWeight.BOLD,
                                    size=20),
                            ft.Text(f"Ultima scansione: {tag_reader.last_tag}",
                                    weight=ft.FontWeight.BOLD,
                                    size=20),
                            ft.Container(border_radius=10,
                                         height=20,
                                         width=20,
                                         bgcolor=ft.Colors.GREEN if tag_reader.online else ft.Colors.RED,
                                         ),
                            ft.Container(border_radius=10,
                                         height=20,
                                         width=20,
                                         bgcolor=ft.Colors.GREEN if tag_reader.connected else ft.Colors.RED,
                                         )
                                                 
                      ]
            
            ),
                expand=3)

@ft.component
def RosterView(roster: Roster,rosters:Rosters)->ft.Control:
    if roster:
       
          
       return ft.Column(
           controls=[
               ft.Container(
                
                content=ft.TextField(
                    value=roster.name,
                    cursor_color=ft.Colors.RED_300,
                    border=ft.InputBorder.NONE,
                    text_size=30,
                    prefix_icon=ft.Icons.EDIT,
                    on_submit=lambda e: (roster.update(e.control.value),rosters.update()),
                    )),
                ft.GridView(
                     expand=1,
                     max_extent=220,
                     child_aspect_ratio=1.0,
                     spacing=15,
                     run_spacing=5,
                     runs_count=5,
                     height=2500,
                     auto_scroll=True,
                     controls=[TagView(tag,roster) for tag in roster.tags],)
                
                ],
           expand=2
           )   
    else:
        return ft.Column(controls=[ft.Container(
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text("Nessuna lista di prenotazione presente",
                                            weight=ft.FontWeight.BOLD,
                                            size=30))
                                  ]
                                   
                                   )
                            
 
@ft.component
def RostersView(rosters: Rosters,tag_reader: TagReader)->ft.Control:
    return ft.Container(
        content=ft.Dropdown(
             options=[
                 ft.DropdownOption(
                         content=ft.ListTile(
                                    leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                                    title=ft.Text(roster.name),
                                    subtitle=f"Codice {roster.code}",
                                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                                    trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),),
                         key=roster.code,
         ) for roster in rosters.past_rosters],
             focused_border_color=ft.Colors.RED,
             autofocus=True,
             on_select=lambda e : tag_reader.current_roster_update(e.control.value)
             )
        ) 