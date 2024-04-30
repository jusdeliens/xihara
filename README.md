# Xihara
A playfull way to teach machine learning by giving the ability to Ova bots to recognize colors with its camereye 👁️

[![A playfull challenge where students compete with others by developping the best machine learning algorithms](xihara-challenge.png)](http://www.youtube.com/watch?v=3O7sKRbIdt4 "Video Title")

## 🎯 Claims

In this multirobot challenge, each robot is placed above a screen, its camera pointing toward a colored circle.
The server controls the colors and make them change more or less randomly. 
In order to win, each robot must recognize the border color of the circle and change the RGB color of its LED accordingly.
The server keeps in the inner Xihara circle the possibles color to guess, so the robot can rely on at any time.  

Here is an example of 4 images captured by one Ova at different time, where the server is set to display 3 colors to guess : red, green, blue.

![Red color to guess among 4 others](/train/4_0_240_240_0.jpeg "🔴Red to guess") ![Green color to guess among 4 others](/train/4_1_240_240_22.jpeg "🟢Green to guess") ![Blue color to guess among 4 others](/train/4_2_240_240_43.jpeg "🔵Blue to guess")

The next level of Xihara challenge, called `SymphonX`, consists of associating colors to musical tones thanks to a dictionary sent by the server, where each color to guess (the key) comes with a frequency (the value) to play using the robot buzzer. Mastering LED RGB and buzzer tone frequency will give you more points for each color to guess. Finally, when a student manage to guess the melody played by the robots, the game ends, and the winner will be the one with most points gained 🏆 


## 🎮 How to play ?

Xihara challenges are performed by our students during our IA classrooms and special robotics events.

It requires the following materials :
- 1 ova bot per student
- 1 computer per student
- 1 [15 inch tablet](https://support.microsoft.com/fr-fr/surface/surface-book-3-sp%C3%A9cifications-et-fonctionnalit%C3%A9s-261d4bb1-2851-d9d5-2020-283429f6cd8c) or any screen laid horizontally 
- A webrowser to display the Xihara arena and the colors to guess on the screen
- A MQTT broker as a hub. It can be the official online Jusdeliens's broker or your own local broker according to your wishes.
- 1 wifi access point available for every robots and computers 

Whether your are a student or a teacher, feel free to [contact us](https://jusdeliens.com/contact) to setup your own gear to perform your Xihara challenge in your organization, we will be glad to show you how.

## 🧠 Skills

Solving this problem will allow you to master
- the notorious numpy, matplotlib, scikit learn and pillow python libraries
- a practical approach of image processing metrics and basics statistics such as gradient, mean, standard deviation 
- SVM, KNN with a good understanding of how they work, and how to assess and improve their performances
- best programming practices such as Object Oriented Programming, SOLID concepts, Test and Comment Driven Development

## 👣 Steps

In this order, you will have to 
1. Brainstorm how to make all this work, think in term of responsabilities (S in SOLID) or in domain (Domain Driven Design) to foresee the classes and objects of your design, and the todo list corresponding 
2. Connect to your robot through the broker and enable its camera to collect some pictures 
3. Automate the collect and the labeling of your data to be able to work with any color number (from 2 to 6)
4. Characterize and feed your classifiers
5. Train and assess your classifier performances
6. Predict each new color and control the LED in loop
7. Play the buzzer tone for each color in loop
8. and finally ... recognize the melody !

## ⚙️ Setup

1. Clone this repo
2. Update all submodules recursively
```
git submodule update --init --recursive
```
3. pip install all deps in [the requirement list](requirements.txt)
```
pip install --no-cache-dir -r requirements.txt
```
4. Add a .env file in the root project directory, containing the following credentials. If you don't have any credentials, feel free [to contact us](https://jusdeliens.com/contact) to join the adventure 🚀
```.env
# Credentials to connect to Ova bot
# The name of your player or your robot ID as str
ROBOTID         = ...
# The name of the arena to join as str
ARENA           = ...
# The broker user name provided by a Jusdeliens administrator as str
USERNAME        = ...
# The broker user password as str
PASSWORD        = ...
# The broker ip address or dns as str
BROKERADDRESS   = ...
# The broker port as int 
BROKERPORT      = ...
# Verbosity level as int from 0:no log, to 4: full debug logs
VERBOSITY       = 3 

# Train dir where images and csv file will be searched
TRAINDIRPATH="train"
TRAINDATASET="data.csv"

# Xihara train parameters to adjust according to server rules
TRAINNCOLORS=5
TRAINNCOLORCYCLES=2
TRAINDTCOLOR=5000
```
5. Then run the main.py with python interpretor (⚠️ at least version 3.9)
```
python main.py
```

## 📂 Folders

The following folders contains the solution of the challenge.
Ideally, students will have to rewrite it from scratch, coached by their teachers to make them use the best practices. 
And if they are stucked, they can keep the interfaces and implement the classes behind, and theirs methods.

### 📂 collector 
The python scripts used to capture and store pictures automatically for training classifiers. 

### 📂 characterizer
The python sources implementing different algorithms to assessing the picture to classify.
Ideally, students should produce the `/train/report.png` figures using matplotib, in order to validate their characterizering metrics, before going any further implementing classification algorithms.

![Matplotib figures](/train/report.png "")

For instance, in the picture below, we easily see that using mean and standard deviation characterizing allow us to segregate by hand the colored dots representing each labeled data. So any classifier should performed well considering this.

### 📂 classifier
The python scripts implementing different classifiers with common methods

### 📂 train
The `.jpeg` pictures collected during the train, and the `data.csv` containing the metrics assessed by characterizer for each picture of this folder.

## 🧑‍💻 Author
Designed with 💖 by [Jusdeliens Inc.](https://jusdeliens.com)

## ⚖️ License
Under CC BY-NC 4.0 licence 
👉 https://creativecommons.org/licenses/by-nc/4.0/deed.en

