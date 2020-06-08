###
### @author Anirudh Kotamraju
###

#Imports
import face_recognition
import numpy as np
import cv2 #headless version
import os
import tkinter as tk
import PIL
from PIL import ImageTk
from tkinter import *

#Styling and functionality changes based on device.
hasTwoCameras = False
isPC = False

#Maximum number of people face recognition should recognize.
NUM_PEOPLE_TO_SHOW = 1

#Stores known faces.
known_face_encodings = []
known_face_names = []

#List of members' names.
members = []

#Adds a person to the database.
def addPerson(name):
    this_image = face_recognition.load_image_file("Images/" + name)
    members.append(name.split(".")[0])
    try:
        this_encoding = face_recognition.face_encodings(this_image)[0]
        known_face_names.append(name.split(".")[0])
        known_face_encodings.append(this_encoding)

    except IndexError:
        os.remove("Images/" + name)  # Remove most recently added member
        members.remove(name.split(".")[0])

        # Retake photo since first once was invalid
        badPhotoPopup = tk.Tk()
        badPhotoPopup.title("Invalid Photo.")
        label2 = tk.Label(badPhotoPopup,
                          text="Your photo was invalid. Please close this window and try taking another photo.")
        label2.pack(side="top", fill="x", pady=10)

        badPhotoPopup.mainloop()
        makePopup()



#Add the members to the members list based on .jpg images in the Images folder (Format: username.jpg)
def updateMembers():
    members = []
    for filename in os.listdir("Images/"):
        if filename.endswith(".jpg"):
            addPerson(filename)


updateMembers()



###########################                         
# Face recognition and UI #
##########################

#Current video stream
cap = cv2.VideoCapture(0)

#Use front facing camera if there are two cameras.
if(hasTwoCameras):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 



#Create window.
root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
root.configure(background = "#1E3155")
screen_width = root.winfo_screenwidth();
screen_height = root.winfo_screenheight();
root.geometry(str(screen_width) + "x" + str(screen_height))
root.title("1072 Attendance")

#Styling for top message
top_message = "Tips: Keep Face Still, Show Complete Face."
topTextFont = "Courier"
topTextFontSize = 20
topTextX = 500
topTextY = 5

#Place text at top of window.
if(isPC):
    topTextX = 400
    topTextY = 5
    
text = tk.Label(root, text=top_message, bg = "#1E3155" , fg="white")
text.config(font=(topTextFont, topTextFontSize))
text.place(x = topTextX, y = topTextY)

#Place the video feed.
lmain = Label(root)
if(isPC):
    lmain.place(x = 180, y = 50)
else:
    lmain.pack(side=TOP, fill=X, expand=YES)

lmain.configure(background="#1E3155")


#Current locations and encodings of visible faces.
face_locations = []
face_encodings = []
face_names = []
currentName = "None yet"

#Stores the last seen frame.
current_frame = None

#Determines if the popup is open.
popup_open = False

#Shows a frame of the face recognition
def show_frame():
    global process_this_frame
    global current_frame
    global currentName
    process_this_frame = True


    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if (isPC):
        frame = cv2.resize(frame, (0, 0), fx=1.6, fy=1.5)
    current_frame = frame


    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Processing every other frame
    if process_this_frame:
        # Determine what faces are in the photo
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


        global NUM_PEOPLE_TO_SHOW
        counter = 0

        # Reset what faces are in the photo
        face_names = []
        for face_encoding in face_encodings:
            if(counter < NUM_PEOPLE_TO_SHOW):
                # See if the face is a match for the known face(s)
                # global currentName already globalized at top


                #CAN MODIFY TOLERANCE IF GO TO METHOD
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Use the closest person
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                else:
                    name = "None Yet"

                currentName = name
                # Add to what names are in the photo
                face_names.append(name)
                counter += 1

    #Skip every other frame for processing efficiency.
    process_this_frame = not process_this_frame

    # Display the results
    personCounter = 0
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if (not popup_open):
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (82, 50, 29), 2)  # bgr not rgb
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (82, 50, 29), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        personCounter += 1

    if(personCounter == 0):
        currentName = "None yet"

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)


    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)

    lmain.after(10, show_frame) #PLEASE. DONT. INCLUDE. PARENTHESES for show_frame()



#Styling for popup to add a new user.
popup_height = 200
popup_width = 400
popup_message = "Please enter your username and press enter to take a new photo of yourself. Eg: 22anirudhk. Make sure to line up your face. Once clicking Submit, it will take a little time to add you to the database.  "


#Username entered when a person wasn't recognized properly.
username_entry = ""

#Widget that represents the entry text box when a person wasn't recognized properly.
myEntryBox = None

myPopup = None

#Updates the databse
def updateDatabase():
    print("UPDATED DATABASE OF PHOTOS.")

#Popup method that takes a picture.
def takePicture():
    global popup_counter
    global popup_open
    global cap
    global lmain
    global current_frame
    global currentName

    username_entry = myEntryBox.get()
    cv2.imwrite("Images/" + username_entry + ".jpg", current_frame)
    currentName = username_entry
    checkIn()
    updateMembers()
    on_closing()


#Makes the popup UI.
def makePopup():
    global popup_message
    global popup_open
    global myEntryBox
    global myPopup

    popup_open = True

    popup = tk.Tk()
    popup.title("Uh oh.")

    myPopup = popup


    label = tk.Label(popup, text = popup_message)
    label.pack(side = "top", fill = "x", pady = 10)

    myEntryBox = Entry(popup)
    myEntryBox.pack()

    submit_button = tk.Button(popup, text="Take Picture + Submit + Check In", command=takePicture)  # if you include parentheses it runs on load
    submit_button.pack()

    popup.protocol("WM_DELETE_WINDOW", on_closing)
    popup.mainloop()

#Defines protocol when closing the popup
def on_closing():
    global popup_open
    popup_open = False
    myPopup.destroy()



#Checks a person in.
def checkIn():
    global currentName
    global text

    email = currentName + "@students.harker.org"

    isCheckingIn = 'true'

    if(currentName != "Unknown" and (currentName != "None yet")):



        # osOutput = os.popen(
        #     "node logger.js %s %s" % (email, isCheckingIn))  # like os.system but STORES output in variable
        # valsList = []
        # for val in osOutput:  # iterate over output line-by-line
        #     valsList.append(val.replace("\n", ""))
        programOutput = 0 #float(valsList[-1])  # last value printed is final output  #CHANGE THIS BACK

        if (programOutput == 1):
            checked_in_popup = tk.Tk()
            checked_in_popup.title("Hello.")

            def this_popup_closed():
                checked_in_popup.destroy()

            label = tk.Label(checked_in_popup, text="You're Already Checked In.")
            label.pack(side="top", fill="x", pady=10)

            submit_button = tk.Button(checked_in_popup, text="   Ok.  ",
                                      command=this_popup_closed)  # if you include parentheses it runs on load

            submit_button.pack()
        else:
            text.configure(text = currentName + " checked in.")

            if(isPC):
                text.place(x=500, y=topTextY)
            else:
                text.place(x=585, y=topTextY)

    else:
        photoNotRecognized = tk.Tk()
        photoNotRecognized.title("Invalid Photo.")

        def next_popup_closed():
            photoNotRecognized.destroy()


        label2 = tk.Label(photoNotRecognized,
                          text="Your photo was invalid. Please close this window and try checking in again.")
        label2.pack(side="top", fill="x", pady=10)

        submit_button = tk.Button(photoNotRecognized, text="   Ok.  ",
                                  command=next_popup_closed)  # if you include parentheses it runs on load

        submit_button.pack()

        photoNotRecognized.mainloop()
    # os.system('"C:/Windows/System32/send_data.exe"')


print(screen_width)
print(screen_height)

#Check in button styling.
if(isPC):
    check_in_button = tk.Button(root, text="Check In", padx=10, pady=5, fg="black", bg="#ffffff",
                                font="Verdana 25 bold", command=checkIn)  # if you include parentheses it runs on load
    check_in_button.place(x=screen_width / 2 - 175, y=710)
    check_in_button.config(height=2, width=15)
    # Incorrect person button styling.
    not_correct_person_button = tk.Button(root, text="Not Correct Person?", padx=10, pady=5, fg="black",
                                          font="Verdana 13 bold", bg="#ffffff",
                                          command=makePopup)  # if you include parentheses on commandName it runs on load
    not_correct_person_button.place(x=screen_width - 325, y=740)
else:
    check_in_button = tk.Button(root, text="Check In", padx=10, pady=5, fg="black", bg="#263D42",
                                font="Verdana 25 bold", command=checkIn)  # if you include parentheses it runs on load
    check_in_button.place(x=570, y=710)
    check_in_button.config(height=2, width=15)
    # Incorrect person button styling.
    not_correct_person_button = tk.Button(root, text="Not Correct Person?", padx=10, pady=5, fg="black",
                                          font="Verdana 13 bold", bg="#263D42",
                                          command=makePopup)  # if you include parentheses on commandName it runs on load
    not_correct_person_button.place(x=1250, y=740)




#Runs UI for everything. Very important.
show_frame()
root.mainloop()