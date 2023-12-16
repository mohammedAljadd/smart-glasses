# 1-Overview
<img src="https://github.com/mohammedAljadd/smart-glasses/blob/main/smart-glasses-design.jpg" width="900">
This is a project in our engineering school INSA Rennes. The idea is to design and build a smart glasses for blind people.

[INSA Rennes website](https://www.insa-rennes.fr/)

#### Team members :

[AL JADD Mohammed](https://www.linkedin.com/in/aljadd/) (the project coordinator)

[AIT JILALI Nouhaila](https://www.linkedin.com/in/nouhaila-ait-jilali-a751951b7/)

[EL NABAOUI Nouhaila](https://www.linkedin.com/in/nouhaila-el-nabaoui-b43b8b19b/)

[EL-ASRI Nossaiba](https://www.linkedin.com/in/nossaiba-el-asri-725b331b2/)

YE Langze

OUASSOU Ahmed

#### Product services :

The three main services of our product are:
    
    - Facial recognition.
    - Object detection.
    - Text recognition.

There will be two modes to use the product:

    - Image mode : Process images. 
    - Video mode : process a real-time video.

So, the user has the choice to choose between image processing or real-time processing for better experience.  


# 2 Product hardware and software :

## 2-1 Overview

Our smart glasses are built on a Raspberry Pi 4 platform, offering a portable and accessible solution for the visually impaired. The glasses are designed with a user-friendly interface featuring buttons to facilitate mode selection (image or video) and task assignment (OCR, object detection, or facial recognition).

### Connectivity and Computation:

In scenarios without an active internet connection, the Raspberry Pi 4 handles data processing locally. However, to expedite computations and enhance performance, when an internet connection is available, the glasses seamlessly transmit data to a remote server for expedited processing.

### Models and Training:

Our models, powered by TensorFlow, underwent rigorous training to ensure optimal performance across tasks. We specifically curated and utilized extensive datasets to bolster the accuracy and reliability of facial recognition capabilities.

## 2-2 Detailed Specifications

### Hardware Components:
- Raspberry Pi 4: Central computing platform for the smart glasses.
- Buttons: Integrated for intuitive mode and task selection.
- Camera Module: Enables image and video capture for processing.

### Software Frameworks and Libraries:
- TensorFlow: Used for model development and training.
- Custom Software: Developed for user interface and interaction.

### Connectivity and Data Transmission:
- Internet Connectivity: Facilitates data transfer to a remote server.
- Data Transmission Protocol: Ensures seamless and secure data exchange.

### Model Training and Data Collection:
- TensorFlow Framework: Employed for model training and optimization.
- Dataset Gathering: Specifically collected data for facial recognition tasks.

### System Architecture:




