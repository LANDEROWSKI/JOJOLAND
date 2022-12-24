import sqlite3

db = sqlite3.connect('database.db')


def Crear_Tabla():
    db.execute("""
    create table if not exists usuarios
    (id integer primary key autoincrement, user text not null, correo text not null, password not null)
    
    """)


Crear_Tabla()
