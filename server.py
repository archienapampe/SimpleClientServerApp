import socket
import threading

from config import logging, LOGGER_CONFIG
from menu_working import (
            menu,
            selected_items,
            items_amount,
            update_menu,
            transfer_data,
            initialize_menu
            )

lock = threading.Lock()
event = threading.Event()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind(('localhost', 5001))
server_socket.settimeout(3)
server_socket.listen()


def accept_connection(server_socket, lock, event):
    while True:
        try:
            try:
                client_socket, _ = server_socket.accept()
            except socket.timeout:
                print('lets buy some drink!')
            else:
                client_socket.setblocking(True)
                if not lock.locked():
                    lock.acquire()
                    th = threading.Thread(target=show_menu, args=(client_socket, event)) 
                    log.info('coffee machine has started')
                    th.start()
                else:
                    log.info(f'client has connected')
                    send_message(client_socket, event)
        except KeyboardInterrupt:
                server_socket.close()
                break
        

def show_menu(client_socket, event):
    client_socket.sendall(f'{transfer_data(menu)}'.encode())
    while True: 
        event.clear()
        event.wait()
        client_socket.sendall(f'{transfer_data(selected_items)}'.encode())
        

def send_message(client_socket, event): 
    while True:
        try:
            choice_drink, choice_ingredient = client_socket.recv(4096).decode('utf-8').split('\n')
        except ValueError:
            log.info('client have bought nothing')
            break
        else:
            try:
                drinks_amount, ingredients_amount = transfer_data(items_amount, choice_drink, choice_ingredient)
            except TypeError:
                client_socket.sendall('Coffee machine database has some problems, please restart server'.encode())
                break
            else:
                if any((drinks_amount == [], ingredients_amount == [])):  
                    log.error(f'client has ordered non-existent drink \u2013 {choice_drink=}, {choice_ingredient=}')
                    client_socket.sendall('Sorry, I cannot make it'.encode())
                    break
                else:
                    if all((drinks_amount[0][0], ingredients_amount[0][0])):
                        transfer_data(update_menu, choice_drink, choice_ingredient)
                        event.set()
                        log.info(f'client has ordered {choice_drink} with {choice_ingredient}')
                        client_socket.sendall(f'Take your {choice_drink} with {choice_ingredient}'.encode())
                        break
                    else:
                        log.warning(f'coffe machine has no {choice_drink} or {choice_ingredient}')
                        client_socket.sendall(f'coffe machine has no {choice_drink} or {choice_ingredient}'.encode())
                        break
        
    log.info('client has disconnected')
    client_socket.close()
    

if __name__ == '__main__':
    log = logging.getLogger('Coffee machine')
    log.setLevel(LOGGER_CONFIG['level'])
    fh = logging.FileHandler(LOGGER_CONFIG['file'], 'w', 'utf-8')
    fh.setFormatter(LOGGER_CONFIG['formatter'])
    log.addHandler(fh)
    
    initialize_menu()
    accept_connection(server_socket, lock, event)