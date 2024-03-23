import flet as ft
import sqlite3

conexion = sqlite3.connect("db", check_same_thread=False)
cursor = conexion.cursor()

#SQL DATABASE
cursor.execute("""CREATE TABLE IF NOT EXISTS todoapp(
               Id INTEGER,
               Nombre TEXT
)""")


def main(page: ft.Page):

    page.window_width = 500
    page.window_height = 700
    page.window_resizable = False
    page.bgcolor = "#141414"
    page.window_center()


    def page_resize(e):
        print("New page size:", page.window_width, page.window_height)

    page.on_resize = page_resize


    rows = list()



    #VARIABLE TAREA
    new_task = ft.TextField(hint_text="Agregar tarea", width=400)

    #BARRA SUPERIOR
    page.appbar = ft.AppBar(bgcolor= "#303030",
                            leading=ft.Icon(ft.icons.CHECKLIST),
                            title= ft.Text("Notas", font_family="Roboto"))
    
    
    #TRAER DATOS DE LA BASE DE DATOS
    


    #RECORRER Y REARMAR LAS LISTAS PARA MOSTRAR
    for r in cursor.execute("SELECT * FROM todoapp").fetchall():

        #VARIABLES CHECKBOX, TAREA Y BOTON DE BORRAR 
        task = ft.TextField(value=str(r[1]).upper(), width=465, color="#202020", disabled=True, bgcolor= "#4B90BE")

        #FILA QUE CONTIENE LAS 3 VARIABLES
        row = (ft.Row(controls=[
            task
        ]))

        rows.append(row)





    def add_clicked(e):

        #SI TAREA NO ESTA VACIA
        if(new_task.value != ""):

            #VARIABLES CHECKBOX, TAREA Y BOTON DE BORRAR 
            task = ft.TextField(value=new_task.value.upper(), width=465, color="#202020", disabled=True, bgcolor= "#4B90BE")

            #FILA QUE CONTIENE LAS 3 VARIABLES
            row = (ft.Row(controls=[
                task
            ]))


            #AÑADE UNA TAREA A LA LISTA ROWS Y A LA BASE DE DATOS
            rows.append(row)

            #ALMACENA NUMERO DE INDICE DE FILA EN UNA VARIABLE
            rowindex = int(rows.index(row))

            #AGREGAR A BASE DE DATOS
            cursor.execute("INSERT INTO todoapp VALUES(?, ?)", (rowindex, task.value))
            conexion.commit()


            #TAREA ESTA VACIA
            new_task.value = ""
            new_task.update()


            #ACTUALIZA LA PAGINA
            page.update()


    #BORRAR TODAS LAS TAREAS
    def clearall(e):
        rows.clear()
        page.update()
        cursor.execute("DELETE FROM todoapp")
        conexion.commit()
        print(len(rows))

    #TAREA Y BOTON AGREGAR TAREA
    page.add(ft.Row(
        [new_task, ft.FloatingActionButton(icon="add", on_click=add_clicked, bgcolor="#4B90BE", scale=0.95)
         ]))
    
    #FUNCION PARA TRAER LAS TAREAS GUARDADAS DE LA BASE DE DATOS
    
    
    page.add(ft.Column(rows))
    page.auto_scroll = True
    
    #BOTON BORRAR TODAS LAS TAREAS
    page.add(ft.FloatingActionButton(icon=ft.icons.CHECK_SHARP, text="BORRAR TODO", on_click=clearall, bgcolor="#993025", scale=0.95))


ft.app(target=main)