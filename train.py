

import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face-Recognition-Based-Attendance-System")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
#window.geometry('1280x720')
window.configure(background='Black')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

#path = "profile.jpg"


# Font is a tuple of (font_family, size_in_points, style_modifier_string)


message = tk.Label(window, text="Face-Detection-Based-Attendance-System", bg="Grey", fg="white", width=50, height=2, font=('times', 30)) 
message.place(x=100, y=1)

lbl = tk.Label(window, text="Enter ID", width=20, height=2, fg="black", bg="cadetblue", font=('times', 15, ' bold ')) 
lbl.place(x=200, y=110)

txt = tk.Entry(window, width=20, bg="cadetblue", fg="black", font=('times', 15, ' bold '))
txt.place(x=500, y=115)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="black", bg="cadetblue", height=2, font=('times', 15, ' bold ')) 
lbl2.place(x=200, y=200)

txt2 = tk.Entry(window, width=20, bg="cadetblue", fg="black", font=('times', 15, ' bold ' ))
txt2.place(x=500, y=215)

lbl3 = tk.Label(window, text="Notification:", width=20, fg="black", bg="cadetblue", height=2, font=('times', 15,' bold ')) 
lbl3.place(x=200, y=300)

message = tk.Label(window, text="", bg="cadetblue", fg="black", width=50, height=2, activebackground="cadetblue", font=('times', 15, ' bold ')) 
message.place(x=500, y=300)

lbl3 = tk.Label(window, text="Attendance:", width=20, fg="black", bg="cadetblue", height=2, font=('times', 15,' bold ')) 
lbl3.place(x=200, y=500)

message2 = tk.Label(window, text="", fg="black", bg="cadetblue", activeforeground="green", width=50, height=3, font=('times', 15, ' bold ')) 
message2.place(x=500, y=500)

 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids
    
def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer() 
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cam = cv2.VideoCapture(0)
    # create a dataframe to hold the student id,name,date and time
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            #  a confidence less than 50 indicates a good face recognition
            if conf < 60:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                row2 = [Id, aa, date, timeStamp]
                #   open the attendance file for update
                with open('AttendanceFile.csv', 'a+') as csvFile2:
                    writer2 = csv.writer(csvFile2)
                    writer2.writerow(row2)
                csvFile2.close()
                # print attendance updated on the notification board of the GUI
                res = 'ATTENDANCE UPDATED WITH DETAILS'
                message2.configure(text=res)

            else:
                Id = 'Unknown'
                tt = str(Id)
                #  store the unknown images in the images unknown folder
                if conf > 65:
                    noOfFile = len(os.listdir("ImagesUnknown")) + 1
                    cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", img[y:y + h, x:x + w])
                    res = 'Id UNKNOWN, ATTENDANCE NOT UPDATED'
                    message2.configure(text=res)
            # To avoid duplication in the attendance file.
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
            # show the student id and name
            cv2.putText(img, str(tt), (x, y + h - 10), font, 0.8, (255, 255, 255), 1)
            cv2.imshow('FACE RECOGNIZER', img)
        if cv2.waitKey(1000) == ord('q'):
            break

        cam.release()
        cv2.destroyAllWindows()
        #print(attendance)
        res=attendance
        message2.configure(text= res)
  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="black"  ,bg="cadetblue"  ,width=20  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=750, y=110)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="black"  ,bg="cadetblue"  ,width=20  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=750, y=200)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="black"  ,bg="cadetblue"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=50, y=400)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="black"  ,bg="cadetblue"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=350, y=400)
trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="black"  ,bg="cadetblue"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=650, y=400)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="cadetblue"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=950, y=400)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 24))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Prathamesh", "superscript")
copyWrite.configure(state="disabled",fg="White"  )
copyWrite.pack(side="left")
copyWrite.place(x=900, y=600)
 
 
window.mainloop()