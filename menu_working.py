import sqlite3
import json
from datetime import datetime

COFFEE_MACHINE_DB = 'menu_data/menu.sqlite'
TABLE_NAME_FOR_DRINKS = 'drinks'
TABLE_NAME_FOR_INGREDIENTS = 'ingredients'


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def initialize_connection(func, *args):
    conn = create_connection(COFFEE_MACHINE_DB)

    if conn is not None:
        try:
            with conn:
                return func(conn, *args)
        finally:
            conn.close()
    else:
        print('Error! cannot create the database connection')

              
def create_menu(conn, table_name, menu_list):
    
    sql_create_menu = f""" CREATE TABLE IF NOT EXISTS {table_name}
                            (
                                name TEXT NOT NULL UNIQUE,
                                amount INTEGER NOT NULL,
                                [timestamp] REAL DEFAULT {datetime.now().timestamp()}
                            )
                        """

    sql_insert_data = f'REPLACE INTO {table_name}(name, amount) VALUES (?,?)'
    
    try:
        cur = conn.cursor()
        cur.execute(sql_create_menu)
        cur.executemany(sql_insert_data, menu_list)
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()   
        

def update_menu(conn, table_name1, table_name2, item_name1, item_name2):
            
    sql_update_table1 = f"""UPDATE {table_name1}
                        SET amount = (amount - 1),
                            timestamp = {datetime.now().timestamp()}
                        WHERE name LIKE ?"""
    
    sql_update_table2 = f"""UPDATE {table_name2}
                        SET amount = (amount - 1),
                            timestamp = {datetime.now().timestamp()}
                        WHERE name LIKE ?"""
                  
    try:
        cur = conn.cursor()
        cur.execute(sql_update_table1, (item_name1,))
        cur.execute(sql_update_table2, (item_name2,))
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close() 
      

def menu(conn, table_name1, table_name2):
                 
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT name FROM {table_name1}')
        data1 = cur.fetchall()
        cur.execute(f'SELECT name FROM {table_name2}')
        data2 = cur.fetchall()
    except sqlite3.Error as e:
        print(e)
        return None
    finally:
        cur.close()   
        
    return [data1, data2]


def items_amount(conn, table_name1, table_name2, item_name1, item_name2):
    
    try:
        cur = conn.cursor()
        cur.execute(f"""SELECT amount FROM {table_name1}
                        WHERE name LIKE ? """, (item_name1,))
        data1 = cur.fetchone()
        cur.execute(f"""SELECT amount FROM {table_name2}
                        WHERE name LIKE ? """, (item_name2,))
        data2 = cur.fetchone()
    except sqlite3.Error as e:
        print(e)
        return None
    finally:
        cur.close()   
        
    return [data1, data2] 
 

def selected_items(conn, table_name1, table_name2):
    
    try:
        cur = conn.cursor()
        cur.execute(f"""SELECT name, amount FROM {table_name1}
                        WHERE timestamp = (SELECT MAX(timestamp) FROM {table_name1})""")
        data1 = cur.fetchone()
        cur.execute(f"""SELECT name, amount FROM {table_name2}
                        WHERE timestamp = (SELECT MAX(timestamp) FROM {table_name2})""")
        data2 = cur.fetchone()
    except sqlite3.Error as e:
        print(e)
        return None
    finally:
        cur.close()   
        
    return [data1, data2]        
 
     
def transfer_data(func, *args):
    
     return initialize_connection(
                            func,
                            TABLE_NAME_FOR_DRINKS,
                            TABLE_NAME_FOR_INGREDIENTS,
                            *args
                        )
    
             
with open('menu_data/data.json', 'r') as f:
    data = json.load(f)
    drinks_menu = [(item, amount) for item, amount in data['drinks'].items()]
    ingredients_menu = [(item, amount) for item, amount in data['ingredients'].items()]     


def initialize_menu():
    initialize_connection(create_menu, TABLE_NAME_FOR_DRINKS, drinks_menu)
    initialize_connection(create_menu, TABLE_NAME_FOR_INGREDIENTS, ingredients_menu)

    

























