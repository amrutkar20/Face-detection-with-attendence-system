# Face-detection-with-attendence-system
 #Code Requirements

Opencv(pip install opencv-python)

Tkinter(Available in python)

PIL (pip install Pillow)

Pandas(pip install pandas)

What steps you have to follow??

Download my Repository

Create a TrainingImage folder in a project.

Run steup.py

Project Structure

After run you need to give your face data to system so enter your ID and name in box than click on Take Images button.

It will collect 200 images of your faces, it save a images in TrainingImage folder

After that we need to train a model(for train a model click on Train Image button.

It will take 2-3 minutes for training(for 10 person data).

After training click on Automatic Attendance ,it can fill attendace by your face using our trained model (model will save in TrainingImageLabel )

it will create .csv file of attendance according to time & subject.

You can store data in database (install wampserver),change the DB name according to your in steup.py.

Manually Fill Attendace Button in UI is for fill a manually attendance (without facce recognition),it's also create a .csv and store in a database.

scrren shot
![image](https://user-images.githubusercontent.com/104386663/230852806-560eb965-4bfd-417f-a5ed-8db969fda307.png)

![image](https://user-images.githubusercontent.com/104386663/230852860-541deb37-066b-4bfd-861a-9a8f8e5b0b98.png)

