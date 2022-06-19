from tkinter import *
from socket import *
import _thread

# INITIALIZING SERVER CONNECTIONS
def initialize_client():
    #initialize socket
    s=socket(AF_INET, SOCK_STREAM)
    #config details of server
    host='localhost'   #192.168.1.5(to use between devices in the same network)
    port=1234
    #connect to server
    s.connect((host,port))

    return s


#update the chat log
def update_chat(msg, state):
    global chatlog
    
    chatlog.config(state=NORMAL)
    #update the message in the window
    if state==0:
        chatlog.insert(END,"YOU: " + msg)
    else:
        chatlog.insert(END, "OTHER: "+ msg)
    chatlog.config(state=DISABLED)
    #show the latest messgaes
    chatlog.yview(END)


#FUNCTION TO SEND MESSAGE
def send(): 
    global textbox
    #get the message
    msg=textbox.get("0.0",END)
    #update the chatlog
    update_chat(msg,0)
    #send the msg to the client
    s.send(msg.encode("ascii"))
    #update the textbox
    textbox.delete("0.0",END)

#function to receive msg
def receive():
    while 1:
        try:
            data=s.recv(1024)
            msg=data.decode('ascii')
            if msg!="":
                update_chat(msg,1)
        except:
            pass
    





# GUI FUNCTION
def GUI():
    global chatlog
    global textbox

#initialize tkinter object.
    gui=Tk()
#set title for the window.
    gui.title("CLIENT CHAT")
#set the size for the window
    gui.geometry("380x430")
# Adding the icon to the application
    gui.iconbitmap(True,"chatbot_icon.ico")

#text space to display the msg
    chatlog=Text(gui,bg="white")
    chatlog.config(state=DISABLED)
#button to send msgs.
    sendButton=Button(gui,bg="orange",fg="red",text="SEND",command=send)
#Textbox to type messages.
    textbox=Text(gui,bg="white")
#place to type messages.
    textbox=Text(gui,bg="white")

#place the components in the window.
    chatlog.place(x=6,y=6,height=386,width=370)
    textbox.place(x=6,y=401,height=20,width=265)
    sendButton.place(x=300,y=401,height=20,width=50)

#create thread to capture messages continuosly
    _thread.start_new_thread(receive, ())

#to keep th window in loop
    gui.mainloop()


if __name__=="__main__":
    chatlog=textbox=None
    s=initialize_client()
    GUI()