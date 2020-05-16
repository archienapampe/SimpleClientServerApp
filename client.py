import socket


def connecting():
    try:
        with socket.create_connection(('localhost', 5001)) as client_socket:
            while True:
                if drink := input('\n\nChoose your drink: ').strip():
                    if ingredient := input('Choose your ingredient: ').strip():
                        client_socket.sendall(f'{drink}\n{ingredient}'.encode())
                        break
                print('You did not choose anything')
            message = client_socket.recv(4096).decode("utf-8")
            print(message, end='\n\n')
    except ConnectionError:
        print('coffee machine is not working')
    except KeyboardInterrupt:
        print('\nclient has dropped') 


if __name__ == '__main__':
    connecting()