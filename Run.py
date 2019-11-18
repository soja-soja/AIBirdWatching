from sys import platform
import cv2
from gtts import gTTS 
import os 
import numpy as np
import asyncio
import speech_recognition as sr     # import the library
import logging
import sys


logFormatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S') #filename='app.log', filemode='w',

rootLogger = logging.getLogger()

rootLogger.setLevel(logging.INFO)


fileHandler = logging.FileHandler("{}.log".format('app'))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)





code = ''
h =w= 0
net=None
confidence_thr = 0.5

commandToSay = 'say'

def detect(r, audio):
    global code
    try:
        # print('in context!!!!')
        text = r.recognize_google(audio,language='en-US' )    # use recognizer to convert our audio into text part.
        code=text
        logging.info("Command: {}".format(text))
        if text.strip().lower() in ['stop', 'exit', 'done']:
            stop_listening(wait_for_stop=False)
            exit()
        # myobj = gTTS(text=text, lang='en', slow=False) 
        # myobj.save("command.mp3") 

        # if 'linux' in platform:
        #     os.system("mpg321 command.mp3") 
        # if 'win' in platform:
        #     os.system('command.mp3')
      
    except sr.UnknownValueError: 
        logging.warning("Google Speech Recognition could not understand audio") 
      
    except sr.RequestError as e: 
        logging.error("Could not request results from Google Speech Recognition service\n{0}".format(e)) 












def applySSDwithVoice(image):
    global h,w,net
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
#     print('>>>>> ' , blob.shape)
    # pass the blob through the network and obtain the detections and
    # predictions
#     print("[INFO] computing object detections...")
    net.setInput(blob)
    
    detections = net.forward()
    
    seenObj = []
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        
        if confidence > confidence_thr:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
#             print("[INFO] {}".format(label))
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            seenObj.append("a {} with {:.2f}% confidence".format(CLASSES[idx], confidence * 100))


            
    return seenObj, image
    
    
    
# =============== intialize_SSD ==================

def webcam():
#     asyncio.ensure_future(get_chat_id("django"))
    
    global code,h,w




    
    cv2.namedWindow("Bird Watcher")
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
        (h, w) = frame.shape[0] , frame.shape[1]
    else:
        rval = False


    lastObjLen = 0    
    while rval:
        cv2.imshow("Bird Watcher", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            code = 'exit'
            break
        seenObj, frame = applySSDwithVoice(frame)
        if  len(seenObj)>0 and code == commandToSay: #len(seenObj) != lastObjLen and
            seenObj.insert(-1, ' and ')
            myobj = gTTS(text='I see '+ ' , '.join(seenObj), lang='en', slow=False) 
            myobj.save("context.mp3") 

            if 'linux' in platform:
                os.system("mpg321 context.mp3") 
            if 'win' in platform:
                os.system('context.mp3 -q   ')

            code = ''

        lastObjLen = len(seenObj)
    vc.release()
    cv2.destroyWindow("Bird Watcher")




#  ======================================
r = sr.Recognizer()                 # initialize recognizer
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening




# while code != 'exit' or text != 'exit':
# with sr.Microphone() as source:     # mention source it will be either Microphone or audio files.
logging.info("Voice Assistant: <On>")
stop_listening = r.listen_in_background(m, callback=detect  )        # listen to the source




# ============================== Default MobileNetSSD model =================================
# CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
#     "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
#     "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
#     "sofa", "train", "tvmonitor"]
# shared_dir = 'object-detection-deep-learning/object-detection-deep-learning/'
# net = cv2.dnn.readNetFromCaffe(shared_dir+ '/MobileNetSSD_deploy.prototxt.txt' , shared_dir+ '/MobileNetSSD_deploy.caffemodel')

# ============================== SOJA ReTrained MobileNetSSD model ==========================
CLASSES = ["background", "hummingbird" , "Fedex"]
shared_dir = 'SOJA_reTrained_Model/'
# net = cv2.dnn.readNetFromCaffe(shared_dir+ '/MobileNetSSD_deploy.prototxt' , shared_dir+ '/MobileNetSSD_birds_soja.caffemodel')
net = cv2.dnn.readNetFromCaffe(shared_dir+ '/MobileNetSSD_SOJA_deploy.prototxt' , shared_dir+ '/MobileNetSSD_birds_soja.caffemodel')
# ===========================================================================================


COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
       
logging.info("Loading model...")


webcam()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.gather(
#    webcam(),
#    Smart(),
# ))
# loop.close()