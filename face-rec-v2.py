###
### @author Anirudh Kotamraju
###

#Imports
import numpy as np
import cv2 #use headless
import os
import tkinter as tk
import PIL
from PIL import ImageTk
import time
from tkinter import *
import threading


#Variables to be set based on device
# CHANGE_IF_NEEDED
hasTwoCameras = False
is_PC = False

#Stores any known faces
known_face_encodings = []
known_face_names = []

#List of all known  1072 members
members = []

#Amount of people to show when running the face rec
# CHANGE_IF_NEEDED
NUM_PEOPLE_TO_SHOW = 1 

#People who've already checked in
checked_in_people = []

# CHANGE_IF_NEEDED
wait_time = 2 #Time before scanning another face.

frame = None
current_name = "None yet"

already_seen_people = [] #They tried to check in a second time and already got a message saying they checked in.


#Base for UI
root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
root.configure(background = "#1E3155")
screen_width = root.winfo_screenwidth();
screen_height = root.winfo_screenheight();
root.geometry(str(screen_width) + "x" + str(screen_height))

# CHANGE_IF_NEEDED
root.title("Attendance")

#Styling for top message
# CHANGE_IF_NEEDED

message_text = "Tips: Keep Face Still, Show Complete Face."
message_font = "Courier"
message_font_size = 20
message_X = 500
message_Y = 5

if(is_PC):
    # CHANGE_IF_NEEDED
    message_X = 400
    message_Y = 5

text = tk.Label(root, text=message_text, bg = "#1E3155" , fg="white")
text.config(font=(message_font, message_font_size))
text.place(x = message_X, y = message_Y)


#Widget that stores the video
lmain = Label(root)
import face_recognition
#Place the video
if(is_PC):
    # CHANGE_IF_NEEDED
    lmain.place(x = 180, y = 50)
else:
    # CHANGE_IF_NEEDED
    lmain.pack(side=TOP, fill=X, expand=YES)
lmain.configure(background="#1E3155")


#Adds a person to the databse
def add_person(name):
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
        bad_photo_popup = tk.Tk()
        bad_photo_popup.title("Invalid Photo.")
        label2 = tk.Label(bad_photo_popup,
                          text="Your photo was invalid. Please close this window and try taking another photo.")
        label2.pack(side="top", fill="x", pady=10)

        bad_photo_popup.mainloop()
        make_popup()



#Add the members to the members list based on .jpg images in the Images folder
def update_members():
    members = []
    for filename in os.listdir("Images/"):
        if filename.endswith(".jpg"):
            add_person(filename)


update_members()


#Create the popup with user options.
def make_popup():
    global current_name
    global popup_open
    global wait_time
    global text
    popup = tk.Tk()
    popup_open = True

    # CHANGE_IF_NEEDED
    if(is_PC): #Fix these
        popup_w = 700
        popup_h = 540 #Fix
        popup_x = 200
        popup_y = 200
    else:
        popup_w = 700
        popup_h = 442 #fix
        popup_x = 450
        popup_y = 200

    popup.geometry('%dx%d+%d+%d' % (popup_w, popup_h, popup_x, popup_y))
    popup.configure(background="#1E3155")
    popup.title("Check In Options")

    def close_popup():
        popup.destroy()

    def on_closing():
        global popup_open
        popup_open = False
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", on_closing)
    popup.geometry()

    def remove_current_name():
        global already_seen_people
        already_seen_people.pop(0)  # Remove first name

    def check_out():
        global popup_open
        global current_name


        email = current_name + "@students.harker.org"
        print(email + "is checking out.")

        isCheckingIn = 1 #to check out

        osOutput = os.popen(
            "node Server/logger.js %s %s" % (email, isCheckingIn))  # like os.system but STORES output in variable
        valsList = []
        for val in osOutput:  # iterate over output line-by-line
            valsList.append(val.replace("\n", ""))
        print(valsList)

        popup_open = False
        already_seen_people.append(current_name)

        timer = threading.Timer(wait_time, remove_current_name)
        timer.start()
        close_popup()


    def checkIn():
        global popup_open
        global current_name


        email = current_name + "@students.harker.org"
        print(email + "is checking in.")
        isCheckingIn = 0 #to check in

        osOutput = os.popen(
            "node Server/logger.js %s %s" % (email, isCheckingIn))  # like os.system but STORES output in variable
        vals_list = []
        for val in osOutput:  # iterate over output line-by-line
            vals_list.append(val.replace("\n", ""))
        print(vals_list)

        popup_open = False
        already_seen_people.append(current_name)

        timer = threading.Timer(wait_time, remove_current_name)
        timer.start()
        close_popup()

    # Adds a person to the databse
    def addPersonDatabase():
        global current_name
        global popup_open
        global current_frame

        def addPicture():
            global current_name
            global current_frame
            global popup_open

            name = current_name
            this_encoding = face_recognition.face_encodings(current_frame)[0]
            known_face_names.append(name.split(".")[0])
            known_face_encodings.append(this_encoding)

            username_entry = myEntryBox.get()
            cv2.imwrite("Images/" + username_entry + ".jpg", current_frame)
            current_name = username_entry
            checkIn()
            update_members()


            popup_open = False
            already_seen_people.append(current_name)

            timer = threading.Timer(wait_time, remove_current_name)
            timer.start()

            take_picture_popup.destroy()
            close_popup()

        def on_closing():
            global popup_open
            take_picture_popup.destroy()
            popup_open = False


        take_picture_popup = tk.Tk()
        take_picture_popup.title("Uh oh.")
        take_picture_popup.configure(background="#1E3155")


        # CHANGE_IF_NEEDED
        label = tk.Label(take_picture_popup, text="Please enter your username and press enter. You will be updated in the database.",
                         font="Verdana 15 bold", fg="white")
        label.pack(side="top", fill="x", pady=10)
        label.configure(background = "#1E3155")

        myEntryBox = Entry(take_picture_popup)
        myEntryBox.pack()

        submit_button = tk.Button(take_picture_popup, text="Submit + Check In.",
                                  command=addPicture, padx=10, pady=5, fg="black", bg="#ffffff",
                                font="Verdana 15 bold")  # if you include parentheses it runs on load
        submit_button.pack()

        take_picture_popup.protocol("WM_DELETE_WINDOW", on_closing)
        take_picture_popup.mainloop()



    def close_and_rescan():
        global popup_open
        close_popup()
        popup_open = False

    # CHANGE_IF_NEEDED
    label = tk.Label(popup, text=("Are you " + current_name + "?"), font="Verdana 25 bold", fg = "white")
    label.pack(side="top", fill="x", pady=10)
    label.configure(background="#1E3155")

    # CHANGE_IF_NEEDED
    if(is_PC):
        first_button_x = 190
        first_button_y = 100

        second_button_x = 175 #Fix
        second_button_y = 210 #Fix

        third_button_x = 250
        third_button_y = 320 #Fix

        fourth_button_x = 249
        fourth_button_y = 430 #Fix
    else:
        first_button_x = 235
        first_button_y = 85

        second_button_x = 225 #Fix
        second_button_y = 175 #Fix

        third_button_x = 280
        third_button_y = 265 #Fix

        fourth_button_x = 280
        fourth_button_y = 355 #Fix

    submit_button = tk.Button(popup, text="Yes, Check In.", padx=10, pady=5, fg="black", bg="#ffffff",
                                font="Verdana 25 bold", command=checkIn)  # if you include parentheses it runs on load

    submit_button.place(x = first_button_x , y = first_button_y)

    submit_button = tk.Button(popup, text="Yes, Check Out.", padx=10, pady=5, fg="black", bg="#ffffff",
                              font="Verdana 25 bold", command=check_out)  # if you include parentheses it runs on load

    submit_button.place(x=second_button_x, y=second_button_y)

    submit_button = tk.Button(popup, text="Rescan",padx=10, pady=5, fg="black", bg="#ffffff",
                                font="Verdana 25 bold", command=close_and_rescan)  # if you include parentheses it runs on load
    submit_button.place(x=third_button_x, y=third_button_y)


#Current video stream
cap = cv2.VideoCapture(0) #You may need to change the index of the camera if you have multiple cameras

if(hasTwoCameras):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Use front facing camera




#Current locations and encodings of visible faces.
face_locations = []
face_encodings = []
face_names = []


#Stores the last seen frame.
current_frame = None

#Determines if the popup is open.
popup_open = False



#Read a frame of the video feed to try and recognize a face.
def show_frame():

    global process_this_frame
    global current_frame
    global current_name
    global popup_open
    process_this_frame = True


    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if (is_PC):
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

                # Use the closest person
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if(not popup_open):
                        current_name = name
                    if(not popup_open and (not current_name in already_seen_people)):
                        make_popup()

                else:
                    name = "None yet"

                if(not popup_open):
                    current_name = name
                # Add to what names are in the photo
                face_names.append(name)
                counter += 1

    # to skip over the other frames
    process_this_frame = not process_this_frame

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk

    if(not popup_open):
        lmain.configure(image=imgtk)


    lmain.after(10, show_frame)
    #Don't include parentheses for show_frame.





#Username entered when a person wasn't recognized properly.
username_entry = ""

#Widget that represents the entry text box when a person wasn't recognized properly.
myEntryBox = None

myPopup = None

#Defines protocol when closing the popup
def on_closing():
    global popup_open
    popup_open = False
    myPopup.destroy()


print(screen_width)
print(screen_height)

#Runs UI for everything. Very important.
show_frame()
root.mainloop()

print("Please call Anirudh to start up the software again.")
