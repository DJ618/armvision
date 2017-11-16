import sys, os, threading
from time import sleep
from vision.armvision import *
from pyuf.uf.wrapper.uarm_api import UarmAPI
from pyuf.uf.utils.log import *
import cv2

num_training_cards = 3
useCam = True
showCards = False
num_cards = 4
useArm = True
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
x = 0
y = 150
z = 100

def initApp():
    global useArm, num_cards, showCards, useCam
    if(len(sys.argv)>1):
        for item in sys.argv[1:]:
            flag = str(item)
            if(flag == "-noarm"):
                useArm = False
                print("Disabling arm")
            elif(flag[0:6] =="-cards"):
                num_cards = int(flag[6])
                print("Expecting %d cards" % num_cards)
            elif(flag== "-nocam"):
                useCam = False;
                print("Disabling webcam, using internal images")
            elif(flag== "-showcards"):
                showCards = True
                print("Showing card recognition")
            else:
                print("Uknown flag: %s" % flag)
                sys.exit()

    if(useArm):
        #logger_init(logging.VERBOSE)
        #logger_init(logging.DEBUG)
        logger_init(logging.INFO)
        print('setup uarm ...')
        #uarm = UarmAPI(dev_port = '/dev/ttyUSB0')
        #uarm = UarmAPI(filters = {'hwid': 'USB VID:PID=0403:6001'})
        uarm = UarmAPI() # default by filters: {'hwid': 'USB VID:PID=0403:6001'}
        print('sleep 2 sec ...')
        sleep(2)
        print('device info: ')
        print(uarm.get_device_info())
    menu()

#card vision functions
def detectCards():
    global num_cards, showCards, num_training_cards
    print("Training AI recognition..")
    #get_training(training_labels_filename, training_image_filename, num_training_cards)
    # training = get_training('./vision/train.tsv', './vision/train.png', 56)
    training = get_training('./vision/train.tsv', './vision/train.png', num_training_cards)
    print("AI trained\n")
    if(training != None):
        cards = []
        while(len(cards) == 0):
        #read/take image
            print("Getting image")
            if(useCam == True):
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                #show capture
                # cv2.imshow('frame', rgb)
                if os.path.isfile('./vision/currentcapture.jpg'):
                    os.remove('./vision/currentcapture.jpg')
                cv2.imwrite('./vision/currentcapture.jpg', frame)
                cap.release()
                im = cv2.imread('./vision/currentcapture.jpg')
            else:
                im = cv2.imread('./vision/test.jpg')

            #transpose and flip if need be
            width = im.shape[0]
            height = im.shape[1]
            # if width < height:
            #   im = cv2.transpose(im)
            #   im = cv2.flip(im,1)

            print("Collecting data")
            try:
                cards = [find_closest_card(training,c) for c in getCards(im,num_cards)]
                print("Probable cards:")
                print(cards)
                if(showCards == True):
                    print("Showing rendered results")
                    try:
                        # Debug: uncomment to see registered images
                        for i,c in enumerate(getCards(im,num_cards)):
                          card = find_closest_card(training,c,)
                          cv2.imshow(str(card),c)
                        cv2.waitKey(0)
                    except:
                        print("Unable to retreive card images")
            except:
                print("Unable to detect any cards")
        return cards

#function for turning the pump on/off asynchronously
def togglePump(onOff):
    uarm.set_pump(onOff)

#main menu for the user
def menu():
    global x,y,z,useArm
    #start at start position
    if(useArm):
        uarm.set_position(x, y, z)
    choice = -1
    while(choice != 3):
        try:
            choice = int((input("----------\n1) Manual Control\n2) AI Mode\n3) Quit\n----------\n")))
            if(choice == 1):
                if(useArm):
                    print("Transfer to manual controls...\n")
                    manualControl()
                else:
                    print("Arm control disabled\n")
            elif(choice == 2):
                print("AI Mode enabled\n")
                currentCards = detectCards();
                #for now, work with 3 cards
                #array location <-> physical location from left to right

                #p: 2,5,10
                #c: 2,5,10

                #p:
                #c:

                #p:
                #c:
                
            elif(choice == 3):
                print("Shutting down..\n")
                break
        except:
            choice = -1

#function for manually controlling robot
def manualControl():
    global x,y,z
    while(1):
        cmd = str(input(">"))
        if(cmd == 'w'):
            x = x + 10
            print("x:%d\n"%x)
        elif(cmd == 's'):
            x = x - 10
            print("x:%d\n"%x)
        elif(cmd == 'a'):
            y = y - 10
            print("y:%d\n"%y)
        elif(cmd == 'd'):
            y = y + 10
            print("y:%d\n"%y)
        elif(cmd == 'r'):
            z = z + 10
            print("z:%d\n"%z)
        elif(cmd == 'f'):
            z = z - 10
            print("z:%d\n"%z)
        elif(cmd == 'c'):
            threads = []
            t = threading.Thread(target = togglePump(True))
            threads.append(t)
            t.start()
        elif(cmd == 'v'):
            uarm.set_pump(False)
        elif(cmd == 'q'):
            break
        uarm.set_position(x, y, z)

if __name__ == "__main__":
    initApp()
