import socket


def connecting():
    try:
        with socket.create_connection(('localhost', 5001)) as client_socket:
            while True:
                message = client_socket.recv(4096).decode("utf-8")
                print(message)
    except (KeyboardInterrupt, ConnectionError):
        print('coffee machine has dropped or server is not working')
    
            
if __name__ == '__main__':
    connecting()