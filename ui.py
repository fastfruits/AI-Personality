import tkinter as tk
from queue import Queue

characterP = ""
voice = "Voice1"
recording = False
recording_queue = Queue()
character_queue = Queue()

window = tk.Tk()
window.geometry("400x400")
window.title("AI-Personality")
window.configure(bg="#009CFF")
window.resizable(False, False)

def button_callbackT():
    recording_queue.put(True)

def button_callbackF():
    recording_queue.put(False)

def createWindow():
    label.pack()
    personality.pack()
    enterChar.pack()
    startButton.pack(side=tk.LEFT)
    endButton.pack(side=tk.RIGHT)

    frame1.pack()
    frame2.pack()
    window.mainloop()

def startRecording():
    recording = True
    print(recording)

def endRecording():
    recording = False
    print(recording)

def setCharacterP():
    character_queue.put(personality.get())
    characterP = personality.get()
    print(characterP)


frame1 = tk.Frame(
    master=window,
    width=100, 
    height=200,
    bg="#009CFF"
)
label = tk.Label(frame1, 
    text="Welcome to AI-Personality!", 
    bg="#009CFF", 
    fg="white"
)
personality = tk.Entry(frame1, 
    width=100, 
)
enterChar = tk.Button(frame1, 
    width = 50,
    height = 5,
    bg="#009CFF", 
    text="Enter Character Personality",
    fg="white",
    command=setCharacterP
)

frame2 = tk.Frame(
    master=window,
    width=200, 
    height=200
)
startButton = tk.Button(frame2, 
    text="Start", 
    command=button_callbackT,  
    bg="#009CFF", 
    fg="white",
    width=25,
    height=15
)
endButton = tk.Button(frame2, 
    text="End", 
    command=button_callbackF, 
    bg="#009CFF", 
    fg="white",
    width=25,
    height=15
)
def personalityPopup():
    popup = tk.Toplevel(window)
    popup.title("Warning!")
    popup.geometry("300x200")
    popup.configure(bg="#f0f0f0")

    label = tk.Label(popup, text="Please enter a personality into the enter box first.", bg="#f0f0f0")
    label.pack(pady=20)

    close_button = tk.Button(popup, text="Close", command=popup.destroy, bg="#4CAF50", fg="white")
    close_button.pack(pady=10)