import cv2
from opencv_webapp.manager import CaptureManager,WindowManager
from opencv_webapp import filters
class Cameo(object):
    def __init__(self):
        self._windowManager = WindowManager('Cameo',self.onKeyPress)
        self._captureManager = CaptureManager(cv2.VideoCapture('/home/ubuntu/Webyug/images/How to Read Math Equations--mu3TYZ_udM.mkv'),self._windowManager,False)
        self._filter = filters.BlurFilter()
    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame=self._captureManager.frame
            self._captureManager.exitFrame()
            self._windowManager.processEvent()


    def onKeyPress(self,keycode):
        """Handle a keypress.
        space  -> Take a screenshot.
        tab    -> Start/stop recording a screencast.
        escape -> Quit.   """
        if keycode == 32:
            print('space pressed')
            self._captureManager.writeImage('screenshot.png')

        elif keycode == 9:
            if not self._captureManager.isWrittingVideo:
                self._captureManager.startWrittingVideo('screencat.avi')
            else:
                self._captureManager.stopWrittingVideo()
        elif keycode == 27:
            self._windowManager.destroyWindow()
#
# if __name__=="__main__":
#     Cameo().run()
