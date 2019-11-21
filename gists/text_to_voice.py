# Code from :
# https://www.geeksforgeeks.org/convert-text-speech-python/
# slightly modified to work both on Linux and windows systems


# install the required package using:
# pip install gTTS

from gtts import gTTS 
import os 
  
# The text that you want to convert to audio 
mytext = 'Welcome to geeksforgeeks!'
  
# Language in which you want to convert 
language = 'en'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=mytext, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  
myobj.save("welcome.mp3") 
  
# Playing the converted file 
from sys import platform
if 'linux' in platform:
    os.system("mpg321 welcome.mp3") 
if 'win' in platform:
    os.system('welcome.mp3')