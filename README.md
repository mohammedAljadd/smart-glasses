# Overview

Hello everyone, this is a project we are working as a team of 6 members in our engineering school [INSA Rennes](https://www.insa-rennes.fr/). The idea is to design and build a smart glasses for blind people.

The three main services of our product are:
    
    - Facial recognition.
    - Object detection.
    - Text recognition.

There will be two modes for using the product:

    - Image mode : Process images. 
    - Video mode : process a real-time video.

So, the user has the choice to choose between image processing or real-time processing for better experience.  

# Team members

[AL JADD Mohammed](https://www.linkedin.com/in/aljadd/) (the project coordinator)

[AIT JILALI Nouhaila](https://www.linkedin.com/in/nouhaila-ait-jilali-a751951b7/)

[EL NABAOUI Nouhaila](https://www.linkedin.com/in/nouhaila-el-nabaoui-b43b8b19b/)

[EL-ASRI Nossaiba](https://www.linkedin.com/in/nossaiba-el-asri-725b331b2/)

YE Langze

OUASSOU Ahmed

# Project stages

**1st stage :**

        The first stage of our project is to expose the three deep learning models as a Restful API 
        so that the user (Raspberry PI model 3) gets the prediction after sending an HTTP request
        containing an image.

*In this stage we will build the following models :*

        - Use Tesseract OCR.
        - YOLOv4 for three classes : (Person, Laptop, Phone).
        - Facial recognition for our group members with CNN, LBPH.


**2nd stage :**

        In the second stage we will use sockets for real-time predictions. But we will keep the image
        processing mode if the user switch to it. For text detection, we will not integrate it in this
        mode (real-time).
- Link of the second version : <a href="https://github.com/mohammedAljadd/iEars/tree/main/2nd%20version" target="_blank">2nd version</a>.

*In this stage we will build the following models :*

        - YOLOv4 that classify 11 classes (Laptop, Pen, Keyboard, Phone, Computer mouse, Person, 
        Board, Bottle, Key, Book, Cars)
        - Facial recognition with FaceNet.



*NB : The two stages are independents. If we did not get what we expect in the second step, we will had already implemented our RestAPI. For each stage we will create a branch.* 


# Product demonstration



# How to explore this github repository?


# Deep learning models
### 1-Facial recognition:
        1- CNN:

        2- LBH:

        3- FaceNet

### 2-Text recognition:
        1- Tesseract:

        2- Handwritting recognition:


### 3-Object detection:



# Project report in french

- The project report is written in Latex. Here is the link to overleaf : <a href="https://www.overleaf.com/project/61e4b995b878196c857a475c" target="_blank">Link</a>

<a href="https://github.com/mohammedAljadd/iEars/tree/main/Project%20report%20in%20Latex" target="_blank">Source files Latex.</a>



