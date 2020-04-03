import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5001))

message = client_socket.recv(4096).decode("utf-8")
print(message)
client_socket.send((input()).encode())
client_socket.send((input()).encode())
message = client_socket.recv(4096).decode("utf-8")
print(message)


        
  


