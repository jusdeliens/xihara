from .interface import IPixelCharacterizer
from .pixel import GradPixelCharacterizer, RgbDiffPixelCharacterizer
from .image import MeanStdFullImageCharacterizer

def test_GradPixelCharacterizer():
    print("🧪 Testing GradPixelCharacterizer", end="")
    class PixelLumTestCharacterizer(IPixelCharacterizer):
        def labels(self): 
            return ["Lum"]
        def characterize(self, x, y):
            return [0]
    characterizer = GradPixelCharacterizer(
                        PixelLumTestCharacterizer()
                    )
    assert characterizer.characterize(0,0) == [0]
    print(" -> ✅")
test_GradPixelCharacterizer()

def test_RgbDiffPixelCharacterizer():
    print("🧪 Testing RgbDiffPixelCharacterizer", end="")
    class PixelRgbTestCharacterizer(IPixelCharacterizer):
        def labels(self): 
            return ["Red","Green","Blue"]
        def characterize(self, x, y):
            return [10,10,10]
    characterizer = RgbDiffPixelCharacterizer(
                        [0,0],
                        PixelRgbTestCharacterizer()
                    )
    assert characterizer.characterize(0,0) == [0,0,0]
    print(" -> ✅")
test_RgbDiffPixelCharacterizer()

def test_MeanStdFullImageCharacterizer():
    print("🧪 Testing MeanStdFullImageCharacterizer", end="")
    class PixelLumTestCharacterizer(IPixelCharacterizer):
        def labels(self): 
            return ["Lum"]
        def characterize(self, x, y):
            return [0]
    characterizer = MeanStdFullImageCharacterizer(
                        10,10,
                        GradPixelCharacterizer(
                            PixelLumTestCharacterizer())
                    )
    assert characterizer.characterize() == [0, 0]
    print(" -> ✅")
test_MeanStdFullImageCharacterizer()
