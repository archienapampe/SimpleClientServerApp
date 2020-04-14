import socket


with socket.create_connection(('localhost', 5001)) as client_socket:
    message = client_socket.recv(4096).decode("utf-8")
    print(message)
    try:
        while True:
            drink = input('Choose your drink: ').strip()
            if drink:
                ingredient = input('Choose your ingredient: ').strip()
                if ingredient:
                    client_socket.sendall(f'{drink}\n{ingredient}'.encode())
                    break
            print('You did not choose anything')
        message = client_socket.recv(4096).decode("utf-8")
        print(message)
    except KeyboardInterrupt:
        client_socket.close()
        
