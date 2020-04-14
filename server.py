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
                log.info(f'{addr=}')
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
            choice_drink, choice_ingredient = client_socket.recv(4096).decode('utf-8').split('\n')
            if all((menu['drinks'][choice_drink], menu['ingredients'][choice_ingredient])):
                menu['drinks'][choice_drink] -= 1
                menu['ingredients'][choice_ingredient] -= 1
                log.info(f'client ordered {choice_drink} with {choice_ingredient}')
                client_socket.sendall(f'Take your {choice_drink} with {choice_ingredient}'.encode())
                break
            else:
                client_socket.sendall(f'I have not enough {choice_drink} or {choice_ingredient}'.encode())
                break
        except KeyError:
            client_socket.sendall('Sorry, I cannot make it'.encode())
            break
        except ValueError:
            break
    client_socket.close()


if __name__ == '__main__':
    log = logging.getLogger('Coffee machine')
    log.setLevel(logging.INFO)
    fh = logging.FileHandler('ordering.log', 'w', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    
    accept_connection(server_socket)
               
    
   

    