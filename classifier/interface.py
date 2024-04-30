
class IClassifier:
    def train(self,datasetPath:str, testPercent:float)->None:
        ...
    def test(self)->list[list[float]]:
        ...
    def predict(self, x:list[float])->list[list[float]]:
        ...
    def report(self, outputPath:str or None)->None:
        ...