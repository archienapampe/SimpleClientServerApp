import socket
import json
import logging


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
    
def accept_connection(server_socket):
    while True:
            try:
                client_socket, addr = server_socket.accept()
                log.info(f'{client_socket=}, {addr=}')
                print('Connection from', addr)
            except socket.error:
                print('lets buy some drink!!!')
            except KeyboardInterrupt:
                server_socket.close()
                break
            else:
                client_socket.setblocking(True)
                send_message(client_socket)
    
def send_message(client_socket):
    client_socket.sendall(f'{json.dumps(menu, indent=16)}'.encode())
    while True:
        try:
            choice_drinks = client_socket.recv(4096).decode('utf-8')
            if menu['drinks'][choice_drinks] == 0:
                client_socket.sendall(f'Sorry, but I have no {choice_drinks}'.encode())
                break
            menu['drinks'][choice_drinks] -= 1
            log.info(f"{choice_drinks=} | {menu['drinks'][choice_drinks]} items left")
            
            choice_ingredients = client_socket.recv(4096).decode('utf-8')
            if menu['ingredients'][choice_ingredients] == 0:
                client_socket.sendall(f'Sorry, but I have no {choice_ingredients}'.encode())
                break
            menu['ingredients'][choice_ingredients] -= 1
            log.info(f"{choice_ingredients=} | {menu['ingredients'][choice_ingredients]} items left")
        except KeyError:
            client_socket.sendall('Sorry, I cannot make it'.encode())
            break
        
        client_socket.sendall(f'take your {choice_drinks} with {choice_ingredients}'.encode())
        break
    client_socket.close()


if __name__ == '__main__':
    log = logging.getLogger('Coffee machine')
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('logging.log', 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    
    accept_connection(server_socket)
               
    
   

    