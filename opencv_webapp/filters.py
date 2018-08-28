import cv2
import numpy as np


def StrokeEdges(src,dst,blurksize=7,edgeksize=5):
    if blurksize>=3:
        blurredSrc=cv2.medianBlur(src,blurksize)
        graysrc=cv2.cvtColor(blurredSrc,cv2.COLOR_BGR2GRAY)
    else:
        graysrc=cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(graysrc,cv2.CV_8U,graysrc,edgeksize)
    normalizedIverseAlpha=(1.0/255)*(255-graysrc)
    channels=cv2.split(src)
    for channel in channels:
        channel[:]=channel * normalizedIverseAlpha
    cv2.merge(channels,dst)

class VconvolutionFilter(object):
    def __init__(self,kernel):
        self._kernel=kernel

    def apply(self,src,dst):
        cv2.filter2D(src,-1,self._kernel,dst)

class SharpenFilter(VconvolutionFilter):
    def __init__(self):
        kernel=np.array([[-1,-1,-1],
                         [-1, 9,-1],
                         [-1,-1,-1]])
        VconvolutionFilter.__init__(self,kernel)

class FindEdgesFilter(VconvolutionFilter):
    def __init__(self):
        kernel=np.array([[-1,-1,-1],
                         [-1, 8,-1],
                         [-1,-1,-1]])
        VconvolutionFilter.__init__(self,kernel)

class BlurFilter(VconvolutionFilter):
    def __init__(self):
        kernel = np.array([[0.04, 0.04, 0.04, 0.04, 0.04],
                           [0.04, 0.04, 0.04, 0.04, 0.04],
                           [0.04, 0.04, 0.04, 0.04, 0.04],
                           [0.04, 0.04, 0.04, 0.04, 0.04],
                           [0.04, 0.04, 0.04, 0.04, 0.04]])
        VconvolutionFilter.__init__(self, kernel)

class EmbossFilter(VconvolutionFilter):
    def __init__(self):
        kernel=np.array([[-2, -1, 0],
                         [-1, 1, 1],
                         [0, -1, 2]])
        VconvolutionFilter.__init__(self,kernel)


