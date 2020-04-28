import socket
import json
import logging
import threading

lock = threading.Lock()
event = threading.Event()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind(('localhost', 5001))
server_socket.settimeout(3)
server_socket.listen()

menu = {
        'drinks': {
            'coffee': 2,
            'cappucino': 2
            },
        
        'ingredients': {
            'milk': 2,
            'sugar': 2
            }
        }


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
    while True:
        client_socket.sendall(f'{json.dumps(menu, indent=16)}'.encode()) 
        event.wait()
    
                    
def send_message(client_socket, event): 
    while True:
        try:
            choice_drink, choice_ingredient = client_socket.recv(4096).decode('utf-8').split('\n')
            drink = menu['drinks'][choice_drink]
            ingredient = menu['ingredients'][choice_ingredient]
        except KeyError:
            log.error(f'client has ordered non-existent drink \u2013 {choice_drink=}, {choice_ingredient=}')
            client_socket.sendall('Sorry, I cannot make it'.encode())
            break
        except ValueError:
            log.info('client have bought nothing')
            break
        else:
            if all((drink, ingredient)):
                menu['drinks'][choice_drink] -= 1
                menu['ingredients'][choice_ingredient] -= 1
                log.info(f'client has ordered {choice_drink} with {choice_ingredient}')
                client_socket.sendall(f'Take your {choice_drink} with {choice_ingredient}'.encode())
                break
            else:
                log.warning(f'coffe machine has no {choice_drink} or {choice_ingredient}')
                client_socket.sendall(f'I have no {choice_drink} or {choice_ingredient}'.encode())
                break
    event.set()
    event.clear()
    log.info('client has disconnected')
    client_socket.close()
    

if __name__ == '__main__':
    log = logging.getLogger('Coffee machine')
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('ordering.log', 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    
    accept_connection(server_socket, lock, event)
    