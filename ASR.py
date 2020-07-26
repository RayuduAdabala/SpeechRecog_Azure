import azure.cognitiveservices.speech as speechsdk
import time

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
def SpeechRecog():
    speech_key, service_region = "speech_key", "service_region"

    weatherfilename = "recorded.wav"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
    all_results = []
    def handle_final_result(a):
        all_results.append(a)
# Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('\nSESSION STOPPED {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: handle_final_result(evt.result.text))
    print(all_results)
    # print('Say a few words\n\n')
    speech_recognizer.start_continuous_recognition()
    time.sleep(30)
    speech_recognizer.stop_continuous_recognition()

    speech_recognizer.session_started.disconnect_all()
    speech_recognizer.recognized.disconnect_all()
    speech_recognizer.session_stopped.disconnect_all()
    all_results
    with open('your_file.txt', 'w') as f:
        for item in all_results:
            f.write("%s\n" % item)
