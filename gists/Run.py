from sys import platform
import cv2
from gtts import gTTS 
import os 
import numpy as np
import asyncio
import speech_recognition as sr     # import the library
import logging
import sys
# ==============================
import logging
import os
import sys
from argparse import ArgumentParser
from math import exp as exp
from time import time

import cv2
try:
    from openvino.inference_engine import IENetwork, IEPlugin
except:
    print('No openvino found, Install it!')






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




def initiateMYRIAD():

   

    logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
    log = logging.getLogger()


    model_xml = args.model
    model_bin = os.path.splitext(model_xml)[0] + ".bin"

    device = 'MYRIAD' #CPU, GPU, FPGA or MYRIAD
    plugin_dir = None

    # ------------- 1. Plugin initialization for specified device and load extensions library if specified -------------
    plugin = IEPlugin(device=device, plugin_dirs=plugin_dir)
    # if args.cpu_extension and 'CPU' in args.device:
    #     plugin.add_cpu_extension(args.cpu_extension)

    # -------------------- 2. Reading the IR generated by the Model Optimizer (.xml and .bin files) --------------------
    log.info("Loading network files:\n\t{}\n\t{}".format(model_xml, model_bin))
    net = IENetwork(model=model_xml, weights=model_bin)

    # ---------------------------------- 3. Load CPU extension for support specific layer ------------------------------
    if plugin.device == "CPU":
        supported_layers = plugin.get_supported_layers(net)
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(plugin.device, ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
            sys.exit(1)

    # assert len(net.inputs.keys()) == 1, "Sample supports only YOLO V3 based single input topologies"
    # assert len(net.outputs) == 3, "Sample supports only YOLO V3 based triple output topologies"
    # exec_net = plugin.load(network=net, num_requests=2)
    # plugin = IEPlugin(device=args.device, plugin_dirs=None)
    return net,plugin


def applyModelWithVoice(image):
    global h,w,net
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
#     print('>>>>> ' , blob.shape)
    # pass the blob through the network and obtain the detections and
    # predictions
#     print("[INFO] computing object detections...")
    if args.device=='CPU':
        start_time = time()
        net.setInput(blob)
        detections = net.forward()
        det_time = time() - start_time
    else:
        
        start_time = time()
        detections = exec_net.infer({'data': blob})['detection_out']
        det_time = time() - start_time
    

    if args.type.lower()=='hybrid':
        print('HYBRID TODO....')
        # TODO: first  run net and then retrained model if class is bird!

    cv2.putText(image, 'Inference Time: ({:.3f})seconds'.format(det_time), (30, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (5 ,44 ,101), 2)
    
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

    input_stream = 0 if args.input == "cam" else args.input
    
    cv2.namedWindow("Bird Watcher")
    vc = cv2.VideoCapture(input_stream)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
        (h, w) = frame.shape[0] , frame.shape[1]
    else:
        rval = False


    lastObjLen = 0    
    while vc.isOpened():
        cv2.imshow("Bird Watcher", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            code = 'exit'
            break

        seenObj, frame = applyModelWithVoice(frame)


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

def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-mc", "--modelCaffe", help="Path to an .caffemodel file with a trained model.", required=False, type=str)
    parser.add_argument("-p", "--modelproto", help="Path to an .prototxt file with a trained model.", required=False, type=str)

    parser.add_argument("-m", "--model", help="Path to an .xml file with a trained model.", required=False, type=str)
    
    parser.add_argument("-i", "--input", help="Path to a image/video file. (Specify 'cam' to work with camera)",
                        required=False, type=str, default="cam")
    parser.add_argument("-d", "--device",
                        help="Specify the target device to infer on; CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device specified (CPU by default)", default="CPU",  required=False,
                        type=str)
    parser.add_argument("-t", "--type", help="Type: hybrid or normal", default="normal",  required=False, type=str)
    
    parser.add_argument("-pt", "--prob_threshold", help="Probability threshold for detections filtering",
                        default=0.5, type=float)
    return parser



if __name__ == '__main__':

    args = build_argparser().parse_args()
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
    confidence_thr = float(args.prob_threshold)
    CLASSES = ["background", "hummingbird" , "blue jay", "Fedex"]
    
    if args.device=='CPU':
        # shared_dir = 'SOJA_reTrained_Model/'
        # net = cv2.dnn.readNetFromCaffe(shared_dir+ '/MobileNetSSD_deploy.prototxt' , shared_dir+ '/MobileNetSSD_birds_soja.caffemodel')
        # net = cv2.dnn.readNetFromCaffe(shared_dir+ '/MobileNetSSD_SOJA_deploy.prototxt' , shared_dir+ '/MobileNetSSD_birds_soja.caffemodel')
        net = cv2.dnn.readNetFromCaffe(args.modelproto , args.modelCaffe)
        # ===========================================================================================
    elif args.device=='MYRIAD':
        net,plugin = initiateMYRIAD()
        exec_net = plugin.load(network=net)#, num_requsts=2)


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
