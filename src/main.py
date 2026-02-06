import flet as ft
from views import TagApp,ClassroomApp
from configurations import genConfig
from router import RouterState

import asyncio

config=genConfig()

@ft.component
def AppBar():
            
    return ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("Class manager"),
        center_title=False,
        bgcolor=ft.Colors.BLUE_GREY_400,
        actions=[ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED,
                               on_click=lambda: asyncio.create_task(ft.context.page.push_route("/classroom"))
                        ),
            ft.IconButton(ft.Icons.FILTER_3,
                          on_click=lambda: asyncio.create_task(ft.context.page.push_route("/tags"))),],
    )


@ft.component
def App():
    
    app_state, _ = ft.use_state(RouterState(route=ft.context.page.route))
    
    
    ft.context.page.on_route_change = app_state.route_change
    ft.context.page.on_view_pop =     app_state.view_popped
      

    views=[ft.View(route="/",
                   appbar=AppBar(),
                   controls=[],)]
    match app_state.route:
                case "/classroom":
                    print("I'm inside classroom view")
                    views+=[ft.View(
                         route="/classroom",
                         appbar=AppBar(),
                         controls=[ClassroomApp(app_state.classroom)])]
                case "/tags":
                    print("I'm inside tags view")
                    views+=[ft.View(
                            route="/tags",
                            appbar=AppBar(),
                            controls=[TagApp(app_state.reader,app_state.rosters)]), ]
                
                             
    return views


    
ft.run(lambda page: page.render_views(App))   


