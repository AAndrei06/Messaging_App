import socket
import threading
import tkinter
import sys
import os

host = socket.gethostbyname(socket.gethostname())
port = 55555
BUFFER_SIZE = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

done = True

def share_to_all(message):
    for client in clients:
        client.send(message)

def handle(client):
    global done
    while done:
        try:
            message = client.recv(BUFFER_SIZE)
            share_to_all(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            share_to_all('\n{} a iesit din chat!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break



def receive():
    global done
    while done:
        client, address = server.accept()
        client.send('nIcKnamE682342'.encode('ascii'))
        nickname = client.recv(BUFFER_SIZE).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        share_to_all("\n{} sa alaturat!".format(nickname).encode('ascii'))
        client.send('\nConectat la server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

    sys.exit(0)

receive_thread = threading.Thread(target = receive)
receive_thread.start()

def close_all():
    done = False
    server.close()
    window.destroy()
    os._exit(1)


window = tkinter.Tk()
window.geometry("400x300")
window.title("Start Server")
confirmation = tkinter.Label(master = window,font = ("Arial Black",20,"bold"),text = "Serverul este pornit,\nputeti deschide aplicatia\nde mesagerie!\n👍 ")
confirmation.place(x = 20,y = 20)
button_close = tkinter.Button(master = window,font = ("Arial",16,"bold"),text = "Opreste serverul",command = close_all)
button_close.place(x = 90,y = 200)

window.mainloop()

