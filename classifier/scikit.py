from .interface import IClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import matplotlib as mp
import numpy as np

class SvmClassifier(IClassifier):
    def __init__(self,kernel="linear"):
        self.__classifier = SVC(kernel=kernel, random_state=0)
        self.__x_test = None
        self.__y_test = None
        self.__nClasses = 0
        self.__lblClasses = []
        self.__trainData = None
        self.__classColors = [
            [""],
            ["", ""],
            ["", "", ""],
            ["red", "green", "blue", "black"],
            ["red", "green", "cyan", "purple", "black"],
            ["red", "yellow", "green", "blue", "purple", "black"],
            ["red", "yellow", "green", "cyan", "blue", "magenta", "black"],
            ["red", "yellow", "green", "cyan", "cornflowerblue", "blue", "magenta", "black"],
        ]

    def train(self,datasetPath:str, testPercent:float=0.2)->None:
        self.__trainData    = pd.read_csv(datasetPath)
        x					= self.__trainData.iloc[:,:-1].values
        y					= self.__trainData.iloc[:,-1].values
        self.__nClasses     = 1+int(y.max())
        self.__lblClasses   = [f"class {iClass}" for iClass in range(self.__nClasses)]
        x_train, self.__x_test, y_train, self.__y_test = train_test_split(x,y,test_size=testPercent) #20% pour test, 80% pour entrainement
        self.__classifier.fit(x_train,y_train)

    def test(self)->list[list[float]]:
        y_pred = self.__classifier.predict(self.__x_test)
        confMatrix = confusion_matrix(self.__y_test,y_pred)
        print(f"Confusion matrix: \n{confMatrix}")
        print(classification_report(self.__y_test,y_pred))
        return confMatrix
    
    def report(self, outputPath:str or None="report.png") -> None:
        """
        Display matplotlib report with scatters
        """
        # Faire un nuage de point pour chaque combinaison de 2 variables explicatives différentes
        nVarsExplicatives = self.__trainData.shape[1]-1
        fig, axs = plt.subplots(nrows=nVarsExplicatives, ncols=nVarsExplicatives) # Diviser fenetre en grille de 2 colonnes 1 ligne
        fig.suptitle(f"Train characterization with {self.__nClasses} classes", fontsize=16)
        for axCol in range(nVarsExplicatives):
            for axRow in range(nVarsExplicatives):
                ax = axs[axRow][axCol]
                if axCol != axRow:
                    # Scatter les points de chaque classe
                    for iClass in range(self.__nClasses):
                        ax.scatter(self.__trainData[self.__trainData.Class==iClass].iloc[:, axCol].values, 
                                self.__trainData[self.__trainData.Class==iClass].iloc[:, axRow].values, 
                                color=self.__classColors[self.__nClasses-1][iClass], label=self.__lblClasses[iClass])
                elif axCol == axRow == 0:
                    # Faire disparaitre l'axe en haut à gauche sauf la légende 
                    invisible = "#ffffff"
                    spines = ['bottom','top','right','left']
                    for spine in spines:
                        ax.spines[spine].set_color(invisible)
                    ax.tick_params(axis='x', colors=invisible)
                    ax.tick_params(axis='y', colors=invisible)
                else:
                    # Faire tout disparaître pour les autres scatter de la diagonale
                    ax.axis('off')
                ax.tick_params(axis='x', labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                if axCol == 0:
                    # Afficher en légende y à gauche de chaque graphe les lignes correspondantes aux variables explicatives j
                    ax.set_ylabel(self.__trainData.columns[axRow])
                if axRow == 0:
                    # Afficher en titre au dessus de chaque graphe les colonnes correspondantes aux variables explicatives i
                    ax.set_title(self.__trainData.columns[axCol])
                if axCol == nVarsExplicatives-2 and axRow == nVarsExplicatives-1:
                    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if outputPath != None:
            print("📊 Writing train report at", outputPath)
            plt.savefig(outputPath, format='png', dpi=1200)
        else:
            print("📊 Showing train report in plot window ")
            plt.show(block=True)

    def predict(self, x:list[float])->list[list[float]]:
        return self.__classifier.predict(x)[0]

