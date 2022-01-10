# Overview

Hello everyone, this is a project I am working on with the members of my team in our engineering school [INSA Rennes](https://www.insa-rennes.fr/). The idea is to design and build smart glasses for blind people. We named our product “iEars” because the user uses his ears to sense the environment.

The three main services of our product are:
    
    - Facial recognition.
    - Object detection.
    - Text recognition and translation.

There will be two modes for using the product:

    - First mode is image processing. 
    - Second mode is real-time processing.

So, the user has the choice to choose between image processing or real-time processing for better experience.  

# Team members

[AL JADD Mohammed](https://www.linkedin.com/in/aljadd/) (the project coordinator)

[AIT JILALI Nouhaila](https://www.linkedin.com/in/nouhaila-ait-jilali-a751951b7/)

[EL NABAOUI Nouhaila](https://www.linkedin.com/in/nouhaila-el-nabaoui-b43b8b19b/)

[EL-ASRI Nossaiba](https://www.linkedin.com/in/nossaiba-el-asri-725b331b2/)

YE Langze

BENJELOUN Bouthaina

OUASSOU Ahmed

# Project stages

**1st stage :**

        The first stage of our project is to expose the three deep learning models as a Restful API so that the user (Raspberry PI model 3) gets the prediction after sending an HTTP request containing an image.

*In this stage we will build the following models :*

        - Use Tesseract and train it for handwritting.
        - YOLOv4 for three classes : (Person, Laptop, Phone).
        - Facial recognition for our group members (one face per image identification).


**2nd stage :**

        In the second stage we will use sockets for real-time predictions. But we will keep the image
        processing mode if the user switch to it. For text detection, we will not integrate it in this
        mode (real-time).

*In this stage we will build the following models :*

        - YOLOv4 that classify 11 classes (Laptop, Pen, Keyboard, Phone, Computer mouse, Person, Board, Bottle, Key, Book, Cars)
        - Facial recognition (multi face identification).



*NB : The two stages are independents. If we did not get what we expect in the second step, we will had already implemented our RestAPI. For each stage we will create a branch.* 


# How our product will work?

