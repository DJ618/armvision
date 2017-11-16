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
resetX = 0
resetY = 150
resetZ = 100

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
        global uarm
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
        trys = 5
        while(len(cards) == 0 and trys >= 0):
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
            trys = trys - 1
        return cards

#function for turning the pump on/off asynchronously
def togglePump(onOff):
    uarm.set_pump(onOff)

def printLocation():
    print("x,y,z")
    print("%d, %d, %d" % (x,y,z))

def move0ToStorage():
    global resetX, resetY, resetZ
    uarm.set_position(-190, 200, 190)
    sleep(3)
    togglePump(True)
    sleep(1)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)
    uarm.set_position(-110, 250, 90)
    sleep(3)
    togglePump(False)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)

def move1ToStorage():
    global resetX, resetY, resetZ
    uarm.set_position(-20, 270, 200)
    sleep(3)
    togglePump(True)
    sleep(1)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)
    uarm.set_position(-10, 270, 90)
    sleep(3)
    togglePump(False)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)

def move2ToStorage():
    global resetX, resetY, resetZ
    uarm.set_position(110, 250, 180)
    sleep(3)
    togglePump(True)
    sleep(1)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)
    uarm.set_position(70, 260, 80)
    sleep(3)
    togglePump(False)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)

def move2FromStorageTo0():
    global resetX, resetY, resetZ
    uarm.set_position(70, 260, 80)
    sleep(3)
    togglePump(True)
    sleep(1)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)
    uarm.set_position(-190, 200, 190)
    sleep(3)
    togglePump(False)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)

def move0FromStorageTo2():
    global resetX, resetY, resetZ
    uarm.set_position(-110, 250, 90)
    sleep(3)
    togglePump(True)
    sleep(1)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)
    uarm.set_position(110, 250, 180)
    sleep(3)
    togglePump(False)
    uarm.set_position(resetX, resetY, resetZ)
    sleep(3)


#main menu for the user
def menu():
    global x,y,z,useArm,num_cards
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
                currentCards.sort(key=lambda tup: tup[1]);
                print(currentCards)
                print("sorting...")
                #build configuration space with repsect to how many cards
                #start location
                #x = 0
                #y = 150
                #z = 100
                if(num_cards == 1):
                    print("1 card is already sorted")
                elif(num_cards == 2):
                    print("2 card config")
                    if(currentCards[0][0] < currentCards[0][1]):
                        move0ToStorage()
                        move2ToStorage()
                        move2FromStorageTo0()
                        move0FromStorageTo2()

                elif(num_cards == 3):
                    print("3 card config")
                    #location of array[0] = -190 200 190
                    #location of array[1] = -20 270 200
                    #location of array[2] = 110 250 180

                    #location of storage[0] = = -110 250 90
                    #location of storage[1] = -10 270 90
                    #location of storage[2] = = 70 260 80

                #work with 3 cards for now
                #sort the array, find ending locations

            elif(choice == 3):
                print("Shutting down..\n")
                break
        except:
            choice = -1

#function for manually controlling robot
def manualControl():
    global x,y,z
    while(1):
        printLocation()
        cmd = str(input(">"))
        if(cmd == 'w'):
            x = x + 10
        elif(cmd == 's'):
            x = x - 10
        elif(cmd == 'a'):
            y = y - 10
        elif(cmd == 'd'):
            y = y + 10
        elif(cmd == 'r'):
            z = z + 10
        elif(cmd == 'f'):
            z = z - 10
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
