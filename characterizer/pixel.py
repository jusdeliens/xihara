from .interface import IPixelCharacterizer
from math import sqrt
from PIL import Image

class GradPixelCharacterizer(IPixelCharacterizer):
    """
    Class to characterize any pixel using its gradien with its close pixels using a scalar
    returned by the specified srcScalarPixelCharacterizer
    """
    def __init__(self, srcScalarPixelCharacterizer: IPixelCharacterizer):
        super().__init__()
        self.__pixelCharacterizer = srcScalarPixelCharacterizer

    def labels(self):
        subLabel = self.__pixelCharacterizer.labels()
        return [subLabel[0]+"Grad"]

    def characterize(self, x :int, y : int) -> list[float]:
        return [sqrt(
            (self.__pixelCharacterizer.characterize(x + 1,y)[0] - self.__pixelCharacterizer.characterize(x - 1, y)[0]) **2
            +
            (self.__pixelCharacterizer.characterize(x, y + 1)[0] - self.__pixelCharacterizer.characterize(x, y - 1)[0]) **2
        )]

class FilterPixelCharacterizer(IPixelCharacterizer):
    """
    Class to characterize any pixel by only one color value filtered, 
    either its R value, or G or B, returned by the specified srcScalarPixelCharacterizer
    """
    filterToIndexMap = {'r':0, 'g':1, 'b':2}
    def __init__(self, srcScalarPixelCharacterizer: IPixelCharacterizer, filter:str='r'):
        super().__init__()
        self.__iRgb:int = FilterPixelCharacterizer.filterToIndexMap[filter]
        self.__pixelCharacterizer = srcScalarPixelCharacterizer

    def labels(self):
        subLabel = self.__pixelCharacterizer.labels()
        return [subLabel[self.__iRgb]]

    def characterize(self, x :int, y : int) -> list[float]:
        return [self.__pixelCharacterizer.characterize(x,y)[self.__iRgb]]

class RgbDiffPixelCharacterizer(IPixelCharacterizer):
    """
    Class to characterize any pixel compare to a reference pixel using absolute diff on r,g,b value,
    according to the values returned by the specified srcRgbPixelCharacterizer
    """
    def __init__(self, pixelRef:tuple[int,int], srcRgbPixelCharacterizer: IPixelCharacterizer):
        self.__pixelRef = pixelRef
        self.__pixelCharacterizer = srcRgbPixelCharacterizer

    def labels(self):
        subLabel = self.__pixelCharacterizer.labels()
        return [subLabel[0]+"Diff",subLabel[1]+"Diff",subLabel[2]+"Diff"]

    def characterize(self, x : int, y : int) -> list[float]:
        xRef,yRef = self.__pixelRef
        rgbRef = self.__pixelCharacterizer.characterize(xRef,yRef)
        rgb = self.__pixelCharacterizer.characterize(x,y)
        return [abs(rgb[0]-rgbRef[0]),abs(rgb[1]-rgbRef[1]), abs(rgb[2]-rgbRef[2])]

class FileImageRgbPixelCharacterizer(IPixelCharacterizer):
    """Adapter to return r,g,b value of any image from a file, using Pillow module"""
    def __init__(self, imagePath:str):
        self.__img = None
        with Image.open(imagePath) as img:
            self.__img = img.convert("RGB").copy() #TODO here: del the copy to gain speed
    
    def labels(self):
        return ["Red","Blue","Green"]

    def characterize(self, x: int, y: int) -> list[float]:
        if x < 0 or x > self.__img.width or y < 0 or y > self.__img.height:
            return [0,0,0]
        r,g,b = self.__img.getpixel((x,y))
        return [r,g,b]