import cv2

import numpy as np

 

'''projection horizotale'''

def getHProjection(image):

    hProjection = np.zeros(image.shape,np.uint8)

    #height and width of image

    (h,w)=image.shape

    #length of array same as height of image
 
    h_ = [0]*h

    #count up the number of white pixels in every line

    for y in range(h):

        for x in range(w):

            if image[y,x] == 255:

                h_[y]+=1

    #draw the horizontal projection 

    for y in range(h):

        for x in range(h_[y]):

            hProjection[y,x] = 255

    ##################################################cv2.imshow('hProjection2',hProjection)

 

    return h_

 

def getVProjection(image):

    vProjection = np.zeros(image.shape,np.uint8);

    #heigth and width of image

    (h,w) = image.shape

    #length of array same as width of image

    w_ = [0]*w

    #count up the number of white pixels in every column

    for x in range(w):

        for y in range(h):

            if image[y,x] == 255:

                w_[x]+=1

    #draw the projection vertical

    for x in range(w):

        for y in range(h-w_[x],h):

            vProjection[y,x] = 255

    #cv2.imshow('vProjection',vProjection)

    return w_

 

if __name__ == "__main__":

    #give the origin image

    origineImage = cv2.imread('mail3.png')

    # gray image   

    #image = cv2.imread('test.jpg',0)

    image = cv2.cvtColor(origineImage,cv2.COLOR_BGR2GRAY)

    ##################################################cv2.imshow('gray',image)

    # image binarization

    retval, img = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)

    ##################################################cv2.imshow('binary',img)

    #length and width of image

    (h,w)=img.shape

    Position = []

    #horizontal projection

    H = getHProjection(img)

 

    start = 0

    H_Start = []

    H_End = []

    #find the location where we can cut by horizontal projection

    for i in range(len(H)):

        if H[i] > 0 and start ==0:

            H_Start.append(i)

            start = 1

        if H[i] <= 0 and start == 1:

            H_End.append(i)

            start = 0

    #cut the lines and store the location to cut

    for i in range(len(H_Start)):

        #the image of every line

        cropImg = img[H_Start[i]:H_End[i], 0:w]

        #cv2.imshow('cropImg',cropImg)

        #cut vertically by image of line

        W = getVProjection(cropImg)

        Wstart = 0

        Wend = 0

        W_Start = 0

        W_End = 0

        for j in range(len(W)):

            if W[j] > 0 and Wstart ==0:

                W_Start =j

                Wstart = 1

                Wend=0

            if W[j] <= 0 and Wstart == 1:

                W_End =j

                Wstart = 0

                Wend=1

            if Wend == 1:

                Position.append([W_Start,H_Start[i],W_End,H_End[i]])

                Wend =0

    #enclose every letter

    for m in range(len(Position)):

        cv2.rectangle(origineImage, (Position[m][0],Position[m][1]), (Position[m][2],Position[m][3]), (0 ,229 ,238), 1)

    cv2.imshow('image',origineImage)

    cv2.waitKey(0)