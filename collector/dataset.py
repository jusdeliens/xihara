from .interface import ICollector
import os
import traceback
from typing import Any

class CsvDataCollector(ICollector):
    """Class to add line of values of the same dimension in a CSV file"""
    def __init__(self, classLabels:list[str], filePath:str):
        """⚠️ classLabels len must be the same as data specified during collect"""
        super().__init__()
        self.__classLabels = classLabels
        self.__filePath = filePath

    def __addToFile(self, values:list[Any]):
        try:
            with open(self.__filePath, "a") as f:
                line = ""
                for i in range(len(values)):
                    if i>0: line += ','
                    line += str(values[i])
                f.write(f"{line}\n")
        except Exception as e:
            print(f"⚠️  Exception during file add at {self.__filePath} : {str(e)}")
            print(traceback.format_exc())

    def reset(self) -> None:
        if os.path.exists(self.__filePath):
            try:
                os.remove(self.__filePath)
                print(f"🗑️  Removed {self.__filePath} file")
            except Exception as e:
                print(f"⚠️  Exception during file deletion at {self.__filePath} : {str(e)}")
                print(traceback.format_exc())
        self.__addToFile(self.__classLabels)

    def collect(self, data:list[Any]) -> None:
        """⚠️ data len must be the same as classLabels set during init"""
        self.__addToFile(data)