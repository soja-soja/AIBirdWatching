# install the required package using: 
# pip install SpeechRecognitio pyaudio

import speech_recognition as sr     # import the library
 
r = sr.Recognizer()                 # initialize recognizer
with sr.Microphone() as source:     # mention source it will be either Microphone or audio files.
    print("Speak Anything :")
    audio = r.listen(source)        # listen to the source
    try:
        text = r.recognize_google(audio,language='en-US' )    # use recognizer to convert our audio into text part.
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize your voice")    # In case of voice not recognized  clearly