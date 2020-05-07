import socket
from ast import literal_eval


def connecting():
    try:
        with socket.create_connection(('localhost', 5001)) as client_socket:
            drinks_menu, ingredients_menu = literal_eval(client_socket.recv(4096).decode("utf-8"))
            print('\n\nDRINKS MENU', end='\n\n')
            for drink in drinks_menu:
                print(drink[0])
            print('\n\n')
            print('INGREDIENTS MENU', end='\n\n')
            for ingredient in ingredients_menu:
                print(ingredient[0])
            print('\n\n')
            
            while True:
                drinks_left, ingredient_left = literal_eval(client_socket.recv(4096).decode("utf-8"))
                print(f'{drinks_left[1]} {drinks_left[0]} left')
                print(f'{ingredient_left[1]} {ingredient_left[0]} left', end='\n\n')
    except (KeyboardInterrupt, ConnectionError):
        print('coffee machine has dropped or server is not working')
    
            
if __name__ == '__main__':
    connecting()   