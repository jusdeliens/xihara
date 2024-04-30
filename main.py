from ova import OvaMqttXiharaImageCollector,OvaMqttXiharaColorRecognizer
from characterizer.image import IshiaharaRGBMeanStdImageCharacterizer
from characterizer.pixel import FileImageRgbPixelCharacterizer
from collector.dataset import CsvDataCollector
from classifier.scikit import SvmClassifier
from datetime import datetime
import os
from dotenv import dotenv_values

config = dotenv_values(".env") 
ROBOTID = config['ROBOTID']
PLAYERID = config['PLAYERID']
BROKERPORT = int(config['BROKERPORT'])
BROKERADDRESS = config['BROKERADDRESS']
BROKERUSERNAME = config['BROKERUSERNAME']
BROKERPASSWORD = config['BROKERPASSWORD']
ARENANAME = config['ARENANAME']
TRAINDIRPATH = config['TRAINDIRPATH']
TRAINDATASET = config['TRAINDATASET']
TRAINNCOLORS = int(config['TRAINNCOLORS'])
TRAINNCOLORCYCLES = int(config['TRAINNCOLORCYCLES'])
TRAINDTCOLOR = int(config['TRAINDTCOLOR'])
print("💾 Loaded env:\n", config)

# Collecting image from ova on a predictible periodical sequence
collectImage = input("🎥 Collect images for training (⚠️  all previous images WILL BE DESTROYED) ?\n(y)es or (n)o (default=n): ")
if collectImage == "y":
	res = input(f"📂 Images output dir (default=`{TRAINDIRPATH}`): ")
	if ( res != "" ): TRAINDIRPATH = res
	res = input(f"🌈 How many colors to recognize (default={TRAINNCOLORS}): ")
	if ( res != "" ): TRAINNCOLORS = int(res)
	res = input(f"➿ How many color cycles to repeat (default={TRAINNCOLORCYCLES}): ")
	if ( res != "" ): TRAINNCOLORCYCLES = int(res)
	res = input(f"⏱️  How many msecs to wait before each color change (default={TRAINDTCOLOR}): ")
	if ( res != "" ): TRAINDTCOLOR = int(res)

	imgCollector = OvaMqttXiharaImageCollector(	server=BROKERADDRESS,
												robotId=ROBOTID, playerId=PLAYERID,
												port=BROKERPORT, arena=ARENANAME,
												username=BROKERUSERNAME, password=BROKERPASSWORD,
												nColors=TRAINNCOLORS, dtColor=TRAINDTCOLOR, outputPath=TRAINDIRPATH
											)

	# Erase previous images
	imgCollector.reset()

	# Start the collector
	input("⌨️  Hit enter key to start collecting, as soon as red color appears 🔴 ...\n> ")
	imgCollector.reset()

	# Loop until all colors have been displayed TRAINNCOLORCYCLES times
	collectDuration = TRAINDTCOLOR*TRAINNCOLORS*TRAINNCOLORCYCLES
	tBegin = datetime.now()
	while (datetime.now()-tBegin).total_seconds()*1000 <= collectDuration:
		imgCollector.update()
	print("👁️  Check the pictures saved in 👉", TRAINDIRPATH)
	input("⌨️  Then Hit enter key to start characterizing ...\n> ")

# Collecting features from train images to data.csv 
datasetPath = os.path.join(TRAINDIRPATH,TRAINDATASET)
classLabels = [f"color{str(i)}" for i in range(TRAINNCOLORS)]
if collectImage == "y" or os.path.exists(datasetPath) == False:
	print(f"📈 Assessing and exporting training metrics to {datasetPath}...")
	trainDataCollector = None
	trainFiles = os.listdir(TRAINDIRPATH)
	for iFile in range(len(trainFiles)):
		f = trainFiles[iFile]
		if not f.endswith(".jpeg"):
			continue
		imgPath = os.path.join(TRAINDIRPATH, f)
		try: nColors,colorClassId,imgW,imgH,imgId = f.split("_")
		except: continue
		# Add only TRAINNCOLORS images in csv
		if int(nColors) != TRAINNCOLORS:
			continue
		imgCharacterizer = IshiaharaRGBMeanStdImageCharacterizer(
							int(imgW),int(imgH),
							FileImageRgbPixelCharacterizer(imgPath))
		if trainDataCollector == None:
			trainLabels = imgCharacterizer.labels()
			trainLabels.append("Class")
			trainDataCollector = CsvDataCollector(trainLabels, datasetPath)
			trainDataCollector.reset()
			print(f"\t{trainLabels}")
		trainValues = imgCharacterizer.characterize()
		trainValues.append(colorClassId)
		print(f"{iFile}/{len(trainFiles)}\t{str(trainValues)}")
		trainDataCollector.collect(trainValues)
		
# TO BE IMPLEMENTED 21/02/2024

# Train classifier from dataset
print(f"🧠 Training classifier from dataset found at {datasetPath}...")
classifier = SvmClassifier()
classifier.train(datasetPath, 0.2)
# Test classifier perfs
showTestResult = input("📈  Show train results ?\n(y)es or (n)o (default=n): ")
if showTestResult == "y":
	classifier.test()
	classifier.report()

# Start Xihara challenge
ovaEye = OvaMqttXiharaColorRecognizer(
	classifier=classifier, 
	server=BROKERADDRESS,
	robotId=ROBOTID,
	playerId=PLAYERID,
	port=BROKERPORT, arena=ARENANAME,
	username=BROKERUSERNAME, password=BROKERPASSWORD,
	nColors=TRAINNCOLORS
)
ovaEye.enableCamera(True)
while True:
	ovaEye.update()
