# Cycle Quest
Cycle Quest is a game that promotes menstrual education for young teens.

For more information, visit: https://devpost.com/software/cycle-quest

<p align="center">
 <img width="570" alt="image" src="https://github.com/miaisakovic/cycle-quest/blob/main/graphics/cycle_quest.png">
</p>

## Table of Contents
* [Setup](#setup)
  * [For Linux](#for-linux)
  * [For MacOS](#for-macos)
  * [After Installing Initial Requirements](#after-installing-initial-requirements)
* [How to Play](#how-to-play)

## Setup 
### For Linux
If Python has not been previously installed, run the following:
```
$ sudo apt install python3.9
$ python3.9 --version
```
If pip has not been previously installed, run the following:
```
$ sudo apt-get install python3-pip 
$ pip3 --version
```

### For MacOS
If Homebrew has not been previously installed, follow the instructions listed [here](https://brew.sh/).

If Python has not been previously installed, run the following:
```
$ brew install python@3.9
$ python3.9 --version
```
If pip has not been previously installed, run the following:
```
$ python3.9 -m ensurepip --upgrade
$ pip3 --version
```

### After Installing Initial Requirements
Clone this repository:
```
$ git clone https://github.com/miaisakovic/cycle-quest.git
``` 
When asked to enter credentials, input your username and personal access token.

If the Pygame library has not been installed, run the following:
```
pip3 install pygame==2.4.0
```

## How to Play
Each time you would like to play this game, run the following command:
```
$ python3.9 <relative path to main.py>
```
