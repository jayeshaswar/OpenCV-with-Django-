import cv2
import numpy as np
import time

class CaptureManager(object):
    def __init__(self,capture,previewWindowManager=None,shouldMirrorPreview=False):
        self.previewWindowManager=previewWindowManager
        self.shouldMirrorPreview=shouldMirrorPreview
        self._capture=capture
        self._channel=0
        self._entered_frame=False
        self._frame=None
        self._imageFileName=None
        self._videoFileName=None
        self._videoEncoding=None
        self._videoWriter=None

        self._startTime=None
        self._frameElapsed=0
        self._fpsEstimate=None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self,value):
        if self._channel != value:
            self._channel=value
            self._frame=None

    @property
    def frame(self):
        if self._entered_frame and self._frame is None:
            _,self._frame=self._capture.retrieve()
            return self._frame

    @property
    def isWrittingImage(self):
        return self._imageFileName is not None

    @property
    def isWrittingVideo(self):
        return self._videoFileName is not None

    def enterFrame(self):
        assert not self._entered_frame,'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def exitFrame(self):
        # if self.frame is None:
        #     print('exit called')
        #     self._entered_frame=False
        #     return

        if self._frameElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed=time.time() - self._startTime
            self._fpsEstimate = self._frameElapsed/timeElapsed
        self._frameElapsed +=1

        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirrorFrame=np.flip(self._frame).copy()
                print('flip frame')
                self.previewWindowManager.show(mirrorFrame)
            else:
                self.previewWindowManager.show(self._frame)

        if self.isWrittingImage:
            cv2.imwrite(self._imageFileName,self._frame)
            self._imageFileName=None
        #write video
        self._writeVideoFrame()

        #release frames
        self._frame = None
        self._entered_frame=False


    def writeImage(self,filename):
        self._imageFileName = filename

    def startWrittingVideo(self,filename,encoding=cv2.VideoWriter_fourcc('I','4','2','0')):
        self._videoFileName = filename
        self._videoEncoding = encoding

    def stopWrittingVideo(self):
        self._videoFileName=None
        self._videoEncoding=None
        self._videoWriter=None

    def _writeVideoFrame(self):
        if not self.isWrittingVideo:
            return

        if self._videoWriter is None:
            fps= self._capture.get(cv2.CAP_PROP_FPS)
            print(fps)
            if fps == 0.0:
                if self._frameElapsed < 20:
                    return
                else:
                    fps=self._fpsEstimate
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter=cv2.VideoWriter(self._videoFileName,self._videoEncoding,fps,size)
        self._videoWriter.write(self._frame)



#window manager class

class WindowManager(object):
    def __init__(self,windowname,keyPressedCallback):
        self.keypressedCalledback = keyPressedCallback
        self._windowname=windowname
        self._isWindowCreated=False
    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowname)
        self._isWindowCreated=True

    def destroyWindow(self):
        cv2.destroyWindow(self._windowname)
        self._isWindowCreated=False

    def show(self,frame):
        cv2.imshow(self._windowname,frame)

    def processEvent(self):
        keycode=cv2.waitKey(0)
        if self.keypressedCalledback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypressedCalledback(keycode)