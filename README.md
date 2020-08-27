# FaceMeIn

Welcome to Anirudh's Improved Attendance System which utilizes Facial Recognition to check in members.

## Note:
1. You will need to ssh into the server in order to modify the attendance database contents.
1. You will also need to modify Server/db.js to connect to the correct mongodb server.


# Version 2
The camera feed runs and once a face is recognized, a popup is shown asking if they would like to check in. They can check-in or rescan. In the future, QR functionality will be added as a third option.

## Setup
1. Modify variables immediately after imports to fit the desired device.
1. Add .jpg images into Images folder. Their username to check in will be in the format: "username.jpg"
1. Go to terminal.
   1. Navigate to this folder.
   1. Enter   pip3 -r install requirements.txt
1. Run with python3 face-rec-v2.py
1. Modify any positioning and styling variables to look how you would like your device. 
   1. Look for the "CHANGE_IF_NEEDED" in the file.



# Version 1 (not recommended)
The camera feed runs and a blue box is placed around a recognized face. If the user desires to check in, they press a button.
If they are not recognized properly, they have the option to take a photo and enter their username, which will then check them in. If a user enter someone else's username for their own face, the administrator 
can find out through looking at new pictures added.

## Setup
1. Modify variables at top of face-rec
1. Add .jpg images into Images folder. Their username to check in will be in the format: "username.jpg"
1. Go to terminal.
   1. Navigate to this folder.
   1. Enter   pip3 -r install requirements.txt
1. Run with python3 face-rec.py
1. Modify any positioning and styling variables to look how you would like your device. 


Please let me know if there are any problems.

~Anirudh
