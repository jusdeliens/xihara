from collector.image import AutoImageCollector
from characterizer.interface import IPixelCharacterizer
from characterizer.image import IshiaharaRGBMeanStdImageCharacterizer
from classifier.interface import IClassifier
from pyrobotx.robot import IRobot
from pyrobotx.client import OvaClientMqtt
from PIL.Image import Image
from datetime import datetime
import debug as debug
		
class OvaRgbPixelCharacterizer(IPixelCharacterizer):
	"""Adapter class to return rgb of a pixel in a real time image from camera"""
	def __init__(self, robot:IRobot):
		self.__robot = robot
	def labels(self): 
		return ["Red","Green","Blue"]
	def characterize(self, x : int, y : int) -> list[float]:
		return self.__robot.getImagePixelRGB(x,y)

class OvaLuminosityPixelCharacterizer(IPixelCharacterizer):
	"""Adapter class to return rgb of a pixel in a real time image from camera"""
	def __init__(self, robot:IRobot):
		self.__robot = robot
	def labels(self): 
		return ["Lum"]
	def characterize(self, x : int, y : int) -> list[float]:
		return [self.__robot.getImagePixelLuminosity(x,y)]
	
class OvaMqttXiharaImageCollector(OvaClientMqtt):
	def __init__(self, robotId:str, playerId:str, arena:str, username:str, password:str, server:str, port:int, nColors:int, dtColor:int, outputPath:str):
		super().__init__(robotId,playerId, arena,username, password, server, port, useProxy=True, clientId=playerId)
		self.__imgCollector = AutoImageCollector(nColors, dtColor, outputPath)
	def _onImageReceived(self, img:Image) -> None:
		"""
		Overrides Ova's method to save image as soon as it is received
		using pillow image instance.
		"""
		self.__imgCollector.collect(img)
	def reset(self):
		self.__imgCollector.reset()

class OvaMqttXiharaColorRecognizer(OvaClientMqtt):
	"""
	To be implemented 21/02/2024
	Class to recognize color using trained classifier specified during instanciation
	update() method is to be called in the main loop to control
	LED color according to the colors found on the picture received
	"""
	def __init__(self, classifier:IClassifier, robotId:str, playerId:str, arena:str, username:str, password:str, server:str, port:int, nColors:int):
		super().__init__(robotId,arena,username, password, server, port, useProxy=True, clientId=playerId)
		self.__classifier = classifier
		self.__colors = []
		print("🤖 Creating ova bot for recognizing", nColors, "colors:", self.__colors)
		self.__characterize = IshiaharaRGBMeanStdImageCharacterizer(
							int(240),int(240),
							OvaRgbPixelCharacterizer(self))
		self.__score = 0
		self.__nGuess = 0
	def _onUpdated(self) -> None:
		playerState = self.getPlayerState()
		if ( "score" in playerState ):
			self.__score = playerState["score"]
		if ( "nGuess" in playerState ):
			self.__nGuess = playerState["nGuess"]
		arenaState = self.getArenaState()
		if ( "colors" in arenaState ):
			self.__colors = arenaState["colors"]
			self.__colors.append((0,0,0))
		if ( "tones" in arenaState ):
			self.__tones = arenaState["tones"]

	def _onImageReceived(self, img:Image) -> None:
		"""
		Overrides Ova's method to save image as soon as it is received
		using pillow image instance.
		"""
		tBegin = datetime.now()
		x = self.__characterize.characterize()
		dtCharacterize = (datetime.now()-tBegin).total_seconds()*1000
		tBegin = datetime.now()
		colorClass = int(self.__classifier.predict([x]))
		dtPredict = (datetime.now()-tBegin).total_seconds()*1000
		print("🌈 Recognized color class", colorClass)
		if ( 0 <= colorClass < len(self.__colors) ):
			r,g,b = self.__colors[colorClass]
			print("🤖 Setting LED to RGB ",r,",",g,",",b)
			self.setLedColor(r,g,b)
		if ( 0 <= colorClass < len(self.__tones) ):
			f = self.__tones[colorClass]
			print("📢 Playing tone ", f, "Hz")
			self.playMelody([[f,100]])



