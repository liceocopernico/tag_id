import flet as ft
from reader import TagReader
from tagmanagement import Tag,Roster,Rosters
from configurations import TagColor,genConfig
from classroom import Desk,Classroom

config=genConfig()



@ft.component
def TagApp(tag_reader: TagReader,rosters: Rosters):
    
    #rosters,_=ft.use_state(Rosters())
    
    if not tag_reader.active:
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


@ft.component
def DeskView(classroom:Classroom,desk: Desk)->ft.Control:
    
    def remove_desk(e):
        classroom.remove_desk(desk.coordinates[0],desk.coordinates[1])
    
    def get_desk_student():
        
        
        
        student=next((x for x in classroom.distributed_students if x[1]==desk), None)
        
        if student!=None:
            return [ft.Image(src=f"images/{student[0][4]}",
                                        width=150,
                                        height=150,
                                        fit=ft.BoxFit.SCALE_DOWN,
                                        border_radius=10
                                )]
        else:
            return [ft.Text(f"Vacant")]
            
           
    def desk_controls():
        controls=[]
        if classroom.edit:
           controls=[ft.IconButton(icon=ft.Icons.DELETE,on_click=remove_desk),
                     ft.IconButton(icon=ft.Icons.UPDATE_SHARP,on_click=desk.toggle_usage)
                     ]
        else:
            if desk.used:
                controls=get_desk_student()
            else:
                controls=[]
        return controls
    

    return ft.Container(
                        bgcolor=ft.Colors.AMBER_100 if desk.used else ft.Colors.GREY_300,
                        border_radius=5,
                        height = 100 if classroom.edit else 150 ,
                        width  = 100 if classroom.edit else 200 ,
                        content=ft.Column(
                                controls=desk_controls(),
                                

                                ))
                        

@ft.component
def ClassroomView(classroom: Classroom):
    columns=config.CLASSROOMGRID[1]
    rows=config.CLASSROOMGRID[0]
    
    def add_desk(e):
       if classroom.edit:
         classroom.add_desk(e.control.data[0],e.control.data[1])
       
     
    grid=ft.Column(controls=[])
         
    for x in range(columns):
        row=ft.Row(controls=[])
        grid.controls.append(row)
        for y in range(rows):
            
            if (x,y) in classroom.desks:
                row.controls.append(DeskView(classroom,classroom.desks[(x,y)]))
            else:
                row.controls.append(ft.Container(
                                    height=100,
                                    width=100,
                                    content=ft.Text(f"{x},{y}") if classroom.edit else ft.Text(""),
                                    border=ft.Border.all(3, ft.Colors.LIGHT_GREEN_ACCENT) if classroom.edit else ft.Border.all(0, ft.Colors.WHITE),
                                    on_click=add_desk,
                                    data=(x,y),
                                    ink=True
                                ))
    
    return grid
    
   
           

@ft.component
def ClassroomApp(classroom:Classroom):
    def toggle_edit(e):
        classroom.edit=not classroom.edit
     
     
     
    async def show_distribution(e):
        classroom.distributed_students
        
    async def save_file(e):
        try:
            filename=await ft.FilePicker().save_file(
                                                 dialog_title="Save students map",
                                                 file_type=ft.FilePickerFileType.CUSTOM,
                                                 allowed_extensions=["svg"],
                                                 file_name="students_map.svg"
                                                 ) 
            classroom.save_map(filename)
        except Exception as e:
            print(e)
        
   
    return ft.Container(
        content=ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[ft.Row(controls=[
                                                ft.IconButton(ft.Icons.EDIT, on_click=toggle_edit),
                                                ft.IconButton(ft.Icons.ROLLER_SHADES, on_click=classroom.grade.add_distribution),
                                                ft.IconButton(ft.Icons.SHOW_CHART, on_click=show_distribution),
                                                ft.IconButton(ft.Icons.SAVE, on_click=save_file )
                                                ]),

                                ClassroomView(classroom)
                              ]))

                                 


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