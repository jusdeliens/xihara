from .interface import IImageCharacterizer, IPixelCharacterizer
from .pixel import RgbDiffPixelCharacterizer, FilterPixelCharacterizer
from math import sqrt

class MeanStdFullImageCharacterizer(IImageCharacterizer):
    """
    Class to characterize an image using mean and standard deviation metrics
    of a scalar value returned on each pixel using the pixelCharacterizer 
    specified as arg when instanciated.
    """
    def __init__(self, imageHeight:int, imageWidth:int, pixelCharacterizer: IPixelCharacterizer) -> None:
        super().__init__()
        self.__imageHeight = imageHeight
        self.__imageWidth = imageWidth
        self.__pixelCharacterizer = pixelCharacterizer

    def labels(self):
        subLabel = self.__pixelCharacterizer.labels()
        return [subLabel[0]+"Mean", subLabel[0]+"Std"]

    def characterize(self) -> list[float] :
        # Calcul de la moyenne des gradients de l'image 
        moyenne = 0
        for x in range (self.__imageWidth):
            for y in range (self.__imageHeight):
                moyenne += self.__pixelCharacterizer.characterize(x, y)[0]
        moyenne /= self.__imageWidth*self.__imageHeight

        # Calcul de l'ecart-type des gradients de tous les points de l'image
        std=0
        for x in range (self.__imageWidth):
            for y in range (self.__imageHeight):
                std += (moyenne - self.__pixelCharacterizer.characterize(x, y)[0]) **2
        std /= self.__imageWidth*self.__imageHeight
        std = sqrt(std)

        # Renvoie de la liste des variables explicatives
        return [moyenne, std]
    
class MeanStdPartialImageCharacterizer(IImageCharacterizer):
    """
    Class to characterize an area on an image using mean and standard deviation 
    metric of a scalar value returned on each pixel using the pixelCharacterizer 
    specified as arg when instanciated.
    """
    def __init__(self, imageHeight:int, imageWidth:int, pixelCharacterizer:IPixelCharacterizer) -> None:
        super().__init__()
        self.__imageHeight = imageHeight
        self.__imageWidth = imageWidth
        self.__pixelCharacterizer = pixelCharacterizer

    def labels(self):
        subLabel = self.__pixelCharacterizer.labels()
        return [subLabel[0]+"Mean", subLabel[0]+"Std"]

    def characterize(self) -> list[float] :
        # Calcul de la moyenne des scalaires de l'image 
        moyenne, n = 0, 0
        for x in range (self.__imageWidth):
            for y in range (self.__imageHeight//3, self.__imageHeight):
                moyenne += self.__pixelCharacterizer.characterize(x, y)[0]
                n += 1
        moyenne /= n

        # Calcul de l'ecart-type des scalaires de tous les points de l'image
        std=0
        for x in range (self.__imageWidth):
            for y in range (self.__imageHeight//3, self.__imageHeight):
                std += (moyenne - self.__pixelCharacterizer.characterize(x, y)[0]) **2
        std /= n
        std = sqrt(std)

        # Renvoie de la liste des variables explicatives
        return [moyenne, std]

class Ishiahara3ColorsImageCharacterizer(IImageCharacterizer):
    """
    Class to characterize a color to recognize on an image during an Xihara challenge
    by comparing a pixel reference of the color to find (the outer circle), with one 
    pixel of each color that can be (displayed in the inner circle).
    """
    def __init__(self, imageHeight:int, imageWidth:int, pixelCharacterizer:IPixelCharacterizer) -> None:
        super().__init__()
        # 👇🏾 Set pixel position for each color to recognize
        self.__colorCharacterizers = [
            RgbDiffPixelCharacterizer((imageWidth//2,0), pixelCharacterizer),                   # black
            RgbDiffPixelCharacterizer((1*imageWidth//2,imageHeight//4), pixelCharacterizer),    # color 1
            RgbDiffPixelCharacterizer((3*imageWidth//2,imageHeight//4), pixelCharacterizer),    # color 2
        ]
        self.__refPixel = (imageWidth//2, imageHeight//6)

    def labels(self) -> list[str]:
        labelsByColor = []
        i=0
        for characterizer in self.__colorCharacterizers:
            subLabels = characterizer.labels()
            for subLabel in subLabels:
                labelsByColor.append(subLabel+"Color"+str(i))
            i+=1
        return labelsByColor
    
    def characterize(self) -> list[float] :
        rgbDiffByColor = []
        x,y = self.__refPixel
        for characterizer in self.__colorCharacterizers:
            rgbDiffs = characterizer.characterize(x,y)
            for rgbDiff in rgbDiffs:
                rgbDiffByColor.append(rgbDiff)
        return rgbDiffByColor

class IshiaharaRGBMeanStdImageCharacterizer(IImageCharacterizer):
    """
    Class to characterize a color to recognize on an image during an Xihara challenge
    by assessing mean and std on R,G,B pixel values of half the image.
    """
    def __init__(self, imageHeight:int, imageWidth:int, pixelCharacterizer:IPixelCharacterizer) -> None:
        super().__init__()
        self.__meanStd:list[IImageCharacterizer] = []
        for rgbFilter in ['r','g','b']:
            self.__meanStd.append(MeanStdPartialImageCharacterizer(
                                    imageWidth, imageHeight, 
                                    FilterPixelCharacterizer(pixelCharacterizer, rgbFilter)))

    def labels(self) -> list[str]:
        x = []
        for characterizer in self.__meanStd:
            mean, std = characterizer.labels()
            x.append(mean)
            x.append(std)
        return x    
    
    def characterize(self) -> list[float] :
        x = []
        for characterizer in self.__meanStd:
            mean, std = characterizer.characterize()
            x.append(mean)
            x.append(std)
        return x