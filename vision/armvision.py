"""
Card Recognition using OpenCV
Code from the blog post
http://arnab.org/blog/so-i-suck-24-automating-card-games-using-opencv-and-python
"""
import sys
import numpy as np
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/")
import cv2

def rectify(h):
  h = h.reshape((4,2))
  hnew = np.zeros((4,2),dtype = np.float32)

  add = h.sum(1)
  hnew[0] = h[np.argmin(add)]
  hnew[2] = h[np.argmax(add)]

  diff = np.diff(h,axis = 1)
  hnew[1] = h[np.argmin(diff)]
  hnew[3] = h[np.argmax(diff)]

  return hnew

###############################################################################
# Image Matching
###############################################################################
def preprocess(img):
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray,(5,5),2 )
  thresh = cv2.adaptiveThreshold(blur,255,1,1,11,1)
  return thresh

def imgdiff(img1,img2):
    img1 = cv2.GaussianBlur(img1,(5,5),5)
    img2 = cv2.GaussianBlur(img2,(5,5),5)
    diff = cv2.absdiff(img1,img2)
    diff = cv2.GaussianBlur(diff,(5,5),5)
    flag, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY)
    return np.sum(diff)

def find_closest_card(training,img):
    print("find_closest_card")
    features = preprocess(img)
    return sorted(training.values(), key=lambda x:imgdiff(x[1],features))[0][0]

###############################################################################
# Card Extraction
###############################################################################
def getCards(im, numcards):
  print("getCards")
  gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray,(1,1),1000)
  flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)

  # contours, im = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  (_, contours, _) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numcards]

  for card in contours:
    peri = cv2.arcLength(card,True)
    approx = rectify(cv2.approxPolyDP(card,0.02*peri,True))

    # box = np.int0(approx)
    # cv2.drawContours(im,[box],0,(255,255,0),6)
    # imx = cv2.resize(im,(1000,600))
    # cv2.imshow('a',imx)

    h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)

    transform = cv2.getPerspectiveTransform(approx,h)
    warp = cv2.warpPerspective(im,transform,(450,450))

    yield warp


def get_training(training_labels_filename,training_image_filename,num_training_cards,avoid_cards=None):
  training = {}
  labels = {}
  for line in open(training_labels_filename):
    key, num, suit = line.strip().split()
    labels[int(key)] = (num,suit)

  print("Training")

  im = cv2.imread(training_image_filename)
  for i,c in enumerate(getCards(im,num_training_cards)):
    if avoid_cards is None or (labels[i][0] not in avoid_cards[0] and labels[i][1] not in avoid_cards[1]):
      training[i] = (labels[i], preprocess(c))

  print ("Done training")
  return training


if __name__ == '__main__':
  if len(sys.argv) == 6:
    filename = sys.argv[1]
    num_cards = int(sys.argv[2])
    training_image_filename = sys.argv[3]
    training_labels_filename = sys.argv[4]
    num_training_cards = int(sys.argv[5])

    training = get_training(training_labels_filename, training_image_filename, num_training_cards)

    im = cv2.imread(filename)

    width = im.shape[0]
    height = im.shape[1]
    if width < height:
      im = cv2.transpose(im)
      im = cv2.flip(im,1)

    cards = [find_closest_card(training,c) for c in getCards(im,num_cards)]
    print (cards)

  else:
    print (__doc__)
