# Chinese chess assistance

## About the Project
This is a Smart System project with the following requirements:
1. Apply Artificial Intelligence
2. Apply Embedded programming
3. Apply Internet of Things
With the purpose of assisting human making decisions.

## Summary
### The problem
"Provided a picture frame that contains a game of Chinese chess, please suggest the next best moves for the two players."

### General solution
Based on the above problem, the project's solution consists of 2 following models:
1. The computer understands the board (using Computer vision with a Tensorflow Classifier model)
2. The computer suggests chess moves (using a [chinese chess engine](https://github.com/bupticybee/elephantfish) as backend with some modifications)

## Deployment
Our project were deployed on a Raspberry Pi 3B. This device also has a small webserver that is used to deliver/broadcast the current chess game to other devices that connect to the server. For more information, please check on our report [here](https://github.com/nvatuan/chinese-chess-assistance/tree/master/report) (Vietnamese and English).

## Demonstrations
We did a small video to demonstate our project/system [here](https://youtu.be/O_xAv5Q_S-0).
