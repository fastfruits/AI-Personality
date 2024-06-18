import time
from azureSTT import STTManager
from gpt import GPTManager
from elevenlabsVoice import VoiceManager
from audio import AudioManager
import json
import ui
import threading
from queue import Queue

personality = ui.characterP
voice = ui.voice
recordingQ = ui.recording_queue
characterQ = ui.character_queue

def getToken(file_path, variable):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config.get(variable)

VOICE = voice # Replace this with the name of your voice on Elevenlabs
 
BACKUP_FILE = "chatbackup.txt"

voiceManager = VoiceManager()
sTTManager = STTManager()
gptManager = GPTManager()
audioManager = AudioManager()


def runProgram():
    while ui.characterP == "":
        if not characterQ.empty():
            ui.characterP = characterQ.get()

        if not recordingQ.empty():
            ui.recording = recordingQ.get()
        
        
        if ui.recording:
            time.sleep(0.1)
            ui.personalityPopup()
            ui.button_callbackF()
            print(personality)
            continue
    
    FIRST_SYSTEM_MESSAGE = {"role": "system", "content":
    ui.characterP + "While responding, you must obey the following rules: 1) Provide short responses, about 1 paragraph. "
    }

    gptManager.chat_history.append(FIRST_SYSTEM_MESSAGE)

    while True:
        if not recordingQ.empty():
            ui.recording = recordingQ.get()
        
        
        if not ui.recording:
            time.sleep(0.1)
            continue

        print("Now listening:")

            # Get audio from mic
        micResult = sTTManager.sttCont()
            
        if micResult == '':
            print("No input from microphone  ")
            continue

            # Send to OpenAi
        gptResult = gptManager.chatHistory(micResult)
            
            # Write the results to txt file
        with open(BACKUP_FILE, "w") as file:
            file.write(str(gptManager.chat_history))

        elevenlabsOutput = voiceManager.tta(gptResult, VOICE, False)

        audioManager.playAudio(elevenlabsOutput, True, True, True)


        print("\nREADY FOR NEXT INPUT")

background_thread = threading.Thread(target=runProgram, daemon=True)
background_thread.start()

ui.createWindow()
