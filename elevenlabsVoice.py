from elevenlabs import generate, stream, set_api_key, voices, play, save
import time
import os
import json

# Function to read the JSON file and extract the token
def getToken(file_path, variable):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config.get(variable)

try:
  set_api_key(getToken('config.json', 'elevenlabsToken'))
except TypeError:
  exit("NO ELEVENLABS API KEY")

class VoiceManager:

    def __init__(self):
        all_voices = voices()

    # Convert text to speech, then save it to file. Returns the file path
    def tta(self, input_text, voice="", save_as_wave=True, subdirectory=""):
        audioSaved = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1"
        )
        if save_as_wave:
          fileName = f"___Msg{str(hash(input_text))}.wav"
        else:
          fileName = f"___Msg{str(hash(input_text))}.mp3"
        ttsFile = os.path.join(os.path.abspath(os.curdir), subdirectory, fileName)
        save(audioSaved,ttsFile)
        return ttsFile

    # Convert text to speech, then play it out loud
    def ttaPlayed(self, input_text, voice=""):
        audio = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1"
        )
        play(audio)

    # Convert text to speech, then stream it out loud
    def ttaStreamed(self, input_text, voice=""):
        audioStream = generate(
          text=input_text,
          voice=voice,
          model="eleven_monolingual_v1",
          stream=True
        )
        stream(audioStream)


if __name__ == '__main__':
    voiceManager = VoiceManager()

    voiceManager.ttaStreamed("Streamed test audio", "")
    time.sleep(2)
    voiceManager.ttaPlayed("Played test audio", "")
    time.sleep(2)
    file_path = voiceManager.tta("Saved test audio", "")
    print("Finished with all tests")

    time.sleep(30)
