## SETUP:

1) Run `pip install -r requirements.txt` to install all required modules.

2) This uses the Microsoft Azure TTS, Elevenlabs, and OpenAi services. You'll need to set up an account with these services and generate an API key from them. Then add these keys to the configEX.json file and rename the file to just config.json so that the .gitignore file safeguards your keys.

3) After setting up an account with OpenAi you will need to pay for at least $1 in credits so that your account is given the permission to use the GPT-4 model for running the app.

4) Create an account with ElevenLabs and an Ai voice on the website. Open up character.py and replace the VOICE variable with the name of your Ai voice.

## Using the Program

1) Run `character.py'

2) Once it's running enter a personality for the ai and then click on the start button and Azure Speech-to-text will listen to your microphone and transcribe it into text.

3) Once you're done talking click on the end button. After talking you should wait ~2 seconds to allow Azure to properly record everything.

4) After the mp3 file plays you can click on the start button to continue the conversation.
