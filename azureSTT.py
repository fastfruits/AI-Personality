import azure.cognitiveservices.speech as speechsdk
import json
import ui

recordingQ = ui.recording_queue

class STTManager:
    speechConfig = None
    audioConfig = None
    speechRecog = None

    def getToken(file_path, variable):
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config.get(variable)
    
    token = getToken('config.json', 'azureToken')
    reg = getToken('config.json', 'azureRegion')
    def __init__(self):
        try:
            self.speechConfig = speechsdk.SpeechConfig(subscription = self.token, region = self.reg)
        except TypeError:
            exit("NO AZURE API KEY")
        
        self.speechConfig.speech_recognition_language="en-US"
        
    def sttMic(self):
        
        self.audioConfig = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speechRecog = speechsdk.SpeechRecognizer(speech_config=self.speechConfig, audio_config=self.audioConfig)

        print("Speak into your microphone.")
        speech_recognition_result = self.speechRecog.recognize_once_async().get()
        text_result = speech_recognition_result.text

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

        print("We got the following text: {text_result}")
        return text_result

    def sttCont(self, stop_key='p'):
        self.speechRecog = speechsdk.SpeechRecognizer(speech_config=self.speechConfig)

        done = False

        def recognized(evt: speechsdk.SpeechRecognitionEventArgs):
            print('RECOGNIZED: {}'.format(evt))
        self.speechRecog.recognized.connect(recognized)

        def stopRecog(evt: speechsdk.SessionEventArgs):
            print('CLOSING speech recognition {}'.format(evt))
            nonlocal done
            done = True

        self.speechRecog.session_stopped.connect(stopRecog)
        self.speechRecog.canceled.connect(stopRecog)

        all_results = []
        def finalResult(evt):
            all_results.append(evt.result.text)
        self.speechRecog.recognized.connect(finalResult)

        result_future = self.speechRecog.start_continuous_recognition_async()
        result_future.get()
        print('Continuous Speech Recognition')

        while not done:    
            if not recordingQ.empty():
                ui.recording = recordingQ.get()

            if not ui.recording:
                print("\nEnding speech recognition")
                self.speechRecog.stop_continuous_recognition_async()
                break  
            
        final_result = " ".join(all_results).strip()
        print(f"\nHeres the results\n{final_result}")
        return final_result