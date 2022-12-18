import socket
import threading
import tkinter
from tkinter import simpledialog
import time
from tkinter import colorchooser

nickname = ""
my_message = ""
BUFFER_SIZE = 2048

hours = 0
minutes = 0
seconds = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()), 55555))

def send_messages():
	my_message = typing_area.get()
	message_to_send = f"\n# {nickname}: {my_message}"
	client.send(message_to_send.encode('ascii'))
	typing_area.delete(0,tkinter.END)

def modify():
	global seconds
	global minutes
	global hours
	while True:
		time.sleep(0.97)
		seconds +=1
		if seconds == 60:
			seconds = 0
			minutes += 1
		if minutes == 60:
			minutes = 0
			hours += 1
		timer.configure(text = f"{hours}:{minutes}:{seconds}")

main_thread = threading.Thread(target = modify)

window_color = '#BFBFBF'

def close_app():
	client.close()
	window.destroy()

def color_choose():
	global window_color
	window_color = colorchooser.askcolor(title = "Alege culoarea aplicatiei")
	copyright.configure(bg = window_color[1])
	timer.configure(bg = window_color[1])
	window.configure(bg = window_color[1])



window = tkinter.Tk()
window.geometry('750x590')
window.title("Messaging App")
window.configure(bg = window_color)
nickname = simpledialog.askstring("Nume","Alege un nume: ")
color_button = tkinter.Button(window,text = "Alege o culoare",font = ("consolas",12,"bold"),command = color_choose)
color_button.place(x = 530,y = 5)
close_button = tkinter.Button(window,text = "Inchide Aplicatia",font = ("Arial Black",12,"bold"),command = close_app)
close_button.place(x = 200,y = 5)
timer = tkinter.Label(window,bg = window_color,font = ("Arial",14,"bold"),text = f"{hours}:{minutes}:{seconds}")
timer.place(x = 100,y = 5)
main_thread.start()
messages_area = tkinter.Text(window,height = 19,width = 54,font = ("consolas",16,"bold"),yscrollcommand = True)
messages_area.place(x = 45,y = 40)
typing_area = tkinter.Entry(window,width = 40,font = ("consolas",18,"bold"))
typing_area.place(x = 45,y = 520)
send_button = tkinter.Button(window,font = ("consolas",12,"bold"),text = "Trimite",command = send_messages)
send_button.place(x = 580,y = 520)
copyright = tkinter.Label(window,font = ("consolas",8,"bold"),bg = window_color,text = "Copyright © 2022 Andrei's Software-All Rights Reserved \nCEO - Arseni Andrei ")
copyright.place(x = 200,y = 560)

def receive():
	while True:
		try:
			message = client.recv(BUFFER_SIZE).decode('ascii')
			if message == 'nIcKnamE682342':
				client.send(nickname.encode('ascii'))
			else:
				messages_area.insert(tkinter.END,message)
		except:
			client.close()
			break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

window.mainloop()
