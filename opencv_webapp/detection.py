import cv2
import os
import numpy as np
import sys
def detect(img):
    face_cascade=cv2.CascadeClassifier('C:\\Anaconda\\envs\\TensorFlow\\Library\\etc\\haarcascades\\haarcascade_frontalface_alt2.xml')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)

    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),[0,255,0],1)

def readTrainingData(path,sz=None):
    c=0
    x,y=[],[]
    for dirname,dirnames,filenames in os.walk(path):
        print(dirname)
        for subdirname in dirnames:
            subject_path=os.path.join(dirname,subdirname)
            for filename in os.listdir(subject_path):
                try:
                    if(filename == '.directory'):
                        continue
                    filepath=os.path.join(subject_path,filename)
                    print(filepath)
                    print('index',c)
                    im = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
                    #resize to given size
                    if sz is not None:
                        im=cv2.resize(im,(200,200))
                    x.append(np.asarray(im,np.uint8))
                    y.append(c)

                except IOError:
                    print("I/O error({0}): {1}".format(IOError.errno(),IOError.strerror()))
                except:
                    print("unexpected error",sys.exc_info()[0])
            c=c+1
    return [x,y]
def mIcon(img,x,y,w,h):
    icon = cv2.imread('C:\\Users\\Milan\\Documents\\DeepLearning\\MachineIconalpha.png')
    icon = cv2.resize(icon,(w,h),interpolation=cv2.INTER_LINEAR)
    row,col,channel=icon.shape
    roi=img[x:x+w,y:y+h]
    icongray=cv2.cvtColor(icon,cv2.COLOR_BGR2GRAY)
    ret,mask = cv2.threshold(icongray,250,255,cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(icon,icon,mask = mask)
    dst = cv2.add(img1_bg,img2_fg)
    img[x:x+w,y:y+h]=dst


def eigenfacesRec(datapath=None):
    names=['janet','milan','rb']
    [X,y]=readTrainingData(datapath)
    y=np.asarray(y,np.int32)
    model= cv2.face.EigenFaceRecognizer_create()
    model.train(np.asarray(X),np.asarray(y))
    face_cascade = cv2.CascadeClassifier(
        'C:\\Anaconda\\envs\\TensorFlow\\Library\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
    camera = cv2.VideoCapture('E:\\aampressvideo\\testing\\130 Crore ka Idea.mp4')
    #camera=cv2.VideoCapture(0)
    while True:
        ret,image=camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        for x,y,w,h in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
            #mIcon(image,x,y,w,h)
            roi = gray[x:x+w,y:y+h]
            try:
                roi = cv2.resize(roi,(200,200),interpolation=cv2.INTER_LINEAR)
                params=model.predict(roi)
                print("Label: %s, Confidence: %.2f" % (params[0] ,params[1]))
                cv2.putText(image, names[params[0]], (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            except:
                continue
        cv2.imshow('cam',image)
        if cv2.waitKey(int(1000/15)) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


eigenfacesRec(datapath='C:/Users/Milan/PycharmProjects/opencv/scripts/Face detection/data/at/')





