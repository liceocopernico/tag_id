import svg
from textwrap import dedent
from configurations import genConfig

config=genConfig()



def draw_desk(x,y,width,height,color):
    return svg.Rect(
                x=x, y=y,
                width=width, height=height,
                stroke="black",
                fill=color,
                stroke_width=5,
            )

def draw_student_label(text,x,y,padx,pady):
    return svg.Text(x=x+padx, y=y+pady, class_=["small"], text=text)

def export_svg(classroom_elements,all_elements,date):
    
    empty_space=100
    deskx=220
    desky=120
    
    dimx=2*empty_space*config.CLASSROOMGRID[0]
    dimy=1.5*empty_space*config.CLASSROOMGRID[1]
    
    body=svg.SVG(width=dimx,height=dimy,elements=[
        svg.Style(
                text=dedent("""
                    .small { font: italic 35px sans-serif; }
                    .heavy { font: bold 30px sans-serif; }

                    /* Note that the color of the text is set with the    *
                    * fill property, the color property is for HTML only */
                    .Rrrrr { font: italic 40px serif; fill: red; }
                """),
            ),
    ])
    
    
    
    
    for element in all_elements.values():
        
        busy_element=next((x for x in classroom_elements if x[1]==element), None)
        xpos=element.coordinates[1]*deskx+empty_space
        ypos=element.coordinates[0]*desky+empty_space
        if busy_element!=None:
            
            
        
            body.elements.append(draw_desk(xpos,ypos,deskx,desky,'orange'))
            body.elements.append(draw_student_label(f"{busy_element[0][2].title()}",xpos ,ypos+desky*0.5,30,0))
        else:
           
        
            body.elements.append(draw_desk(xpos,ypos,deskx,desky,'gray'))
    
        body.elements.append(svg.Text(x=empty_space, y=dimy-empty_space, class_=["small"], text=f"Configuration date time {date}"))
        
    return body
    