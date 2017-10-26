#Setup:
python ./pyuf/setup.py install
<br/>
Required software:
Python3, pip
<br/>

#Required packages:
pip install uarm
pip install opencv-python
<br/>
<br/>
#Use of arm.py
python arm.py <flags>
  flags:
        * -noarm
            * Will disable the robotic arm aspect of the application.
        * -nocam
            * Will disable the camera aspect of the application and use internal
              images instead.
        * -cards<n>
            * Tells the AI how many cards to expect for now, this feature may
              be consumed with improved functionality later.
              NOTE: There exists no space between the "s" in cards, and the num.
<br/>
<br/>
#Card Recognition using OpenCV
Code from the blog post
http://arnab.org/blog/so-i-suck-24-automating-card-games-using-opencv-and-python
Usage:
  ./card_img.py filename num_cards training_image_filename training_labels_filename num_training_cards
Example:
  ./card_img.py test.JPG 4 train.png train.tsv 56
Note: The recognition method is not very robust; please see SIFT / SURF for a good algorithm.

<br/>
<br/>
#UFACTORY
Git repo for an API wrapper to the uarm.
https://github.com/uArm-Developer/pyuf/