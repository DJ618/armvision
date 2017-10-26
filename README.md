_Setup:_
-------------------------------------------------------------------------------
python ./pyuf/setup.py install <br/>
<br/>
Required software: <br/>
Python3, pip, {Possibly python2.7}<br/>
NOTE: Be sure to have your python path environment variables set!<br/>
<br/>
<br/>
-------------------------------------------------------------------------------
_Required packages:_
-------------------------------------------------------------------------------
pip install uarm<br/>
pip install opencv-python
<br/>
<br/>
-------------------------------------------------------------------------------
_Use of arm.py_
-------------------------------------------------------------------------------
python arm.py <flags><br/>
  flags:<br/>
        _-noarm_<br/>
            Will disable the robotic arm aspect of the application.<br/>
        _-nocam_<br/>
            Will disable the camera aspect of the application and use internal<br/>
              images instead.<br/>
        _-showcards_<br/>
            Will show the rendered card images during execution time.<br/>
        _-cards<n>_<br/>
            Tells the AI how many cards to expect for now, this feature may
            be consumed with improved functionality later.<br/>
            NOTE: There exists no space between the "s" in cards, and the number of cards.<br/>
<br/>
<br/>
-------------------------------------------------------------------------------
_Card Recognition using OpenCV_
-------------------------------------------------------------------------------
Code from the blog post<br/>
https://arnab.org/blog/so-i-suck-24-automating-card-games-using-opencv-and-python<br/>
Usage:<br/>
  /card_img.py filename num_cards training_image_filename training_labels_filename num_training_cards<br/>
Example:<br/>
  /card_img.py test.JPG 4 train.png train.tsv 56<br/>
Note: The recognition method is not very robust; please see SIFT / SURF for a good algorithm.

<br/>
<br/>
-------------------------------------------------------------------------------
_U FACTORY_
-------------------------------------------------------------------------------
Git repo for an API wrapper to the uarm.
https://github.com/uArm-Developer/pyuf/
