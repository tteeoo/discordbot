class chat:
    shown = True

def openconsole():
    global command
    command = input('>>> ')
    if(command=='togglechat'):
        togglechat()
    else:
        print('ERROR: Unrecognized Command')
        openconsole()

def togglechat():
    chat.shown = not chat
    print(f'chat set to {chat.shown}')
    openconsole()

if(__name__ == '__main__'):
    print('Running rngBot terminal')
    openconsole()
