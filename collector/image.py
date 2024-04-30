from .interface import ICollector
from PIL.Image import Image
from datetime import datetime
import os
import traceback

class AutoImageCollector(ICollector):
	"""
	Class to collect several images of each class to recognize.
	The classes to recognize on the images should be displayed peridically:
	every dtClass msecs, the next class should be displayed, and once all 
	classes are displayed, it should go back to the first class then repeat
	the same sequence in the same order, thus, as many cycles as needed to be.
	
	Before starting a collect, make sure to wait until the first class 
	(index 0) appears.
	Then call collect() in a loop every time an image is received. 
	Then stop collecting when all classes are displayed, after a 
	cycle is completed (the first, or any cycle).
	Finally, as supervised learning, you should check image collected in the
	spcified outputPath folder, and remove corrupted or misclassified images. 
	"""
	def __init__(self, nClasses:int, dtClass:int, outputPath:str):
		self.__imgDirPath 	= outputPath		# The output path where to save the image
		self.__nClasses 	= nClasses			# The number of possible class to recognize
		self.__dtClass 		= dtClass 			# The delta time in msecs to wait before going to the next class to collect
		self.__classIndex 	= 0 				# Will be incremented automatically after __dtClass msecs
		self.__classCycle 	= 0 				# Will be incremented automatically after __nClasses*__dtClass msecs
		self.__imageId 		= 0					# Will be incremented once all class classes are collected
		self.__tPrevClass	= datetime.now()	# Timestamp of the previous class change
		
	def reset(self):
		"""
		Remove all jpeg files in self.__imgDirPath and restart counters.
		To be called just before starting a image collect. 
		"""
		for f in os.listdir(self.__imgDirPath):
			if not f.endswith(".jpeg"):
				continue
			os.remove(os.path.join(self.__imgDirPath, f))
		self.__classIndex 	= 0 	
		self.__classCycle	= 0			
		self.__imageId 		= 0					
		self.__tPrevClass	= datetime.now()
		print(f"🌈 Reset collect and restart from class {self.__classIndex}")
	
	def collect(self, img:Image):
		"""
		To be called to save image as soon as it is received
		using pillow image instance.
		The output name will be {nClasses}_{classClass}_{imageId}.jpg with
		`nClasses`	: an int number of classs in the center of the calibration circle 
		`classClass`: an int number for the class class to learn to recognize
		`imageId`	: an auto incremented int id 
		"""
		# Save the image
		imgName = f"{self.__nClasses}_{self.__classIndex}_{img.width}_{img.height}_{self.__imageId}.jpeg"
		imgPath = os.path.join(self.__imgDirPath,imgName)
		try:
			tBegin = datetime.now()
			img.save(imgPath)
			dt = int((datetime.now()-tBegin).total_seconds() * 1000)
			print(f"🖼️  Saved image to {imgPath} in {dt} ms")
		except Exception as e:
			print(f"⚠️ Exception during image saving to {imgPath} : {str(e)}")
			print(traceback.format_exc())

		# Change collector's attributes for the next image
		self.__imageId += 1
		now = datetime.now()
		dt = int((now-self.__tPrevClass).total_seconds() * 1000)
		if dt >= self.__dtClass:
			self.__tPrevClass = now
			self.__classCycle += (self.__classIndex+1)//self.__nClasses
			self.__classIndex = (self.__classIndex+1)%self.__nClasses
			print(f"🌈 Collect next class {self.__classIndex} on cycle {self.__classCycle}")