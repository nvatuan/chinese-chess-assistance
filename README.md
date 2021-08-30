# Chinese Chess Assistance (CCA) System

This is a Smart System project that:
1. Applies Artificial Intelligence
2. Applies Embedded programming
3. Applies Internet of Things
With the purpose of assisting human making decisions.

## Summary
<p align="center">
<img src="https://user-images.githubusercontent.com/24392632/131322217-d9eed454-ffc8-4a78-94eb-96d9a9301624.png" width="60%" alt="The system's process">
</p>

The system consists of 3 steps:
1. Monitors the chessboard, taking picture every few millisecs.
2. Recognizes the pieces, understands the chess board position. Then, search and calculate for the next best moves.
3. Broadcast those information over LAN via wi-fi. The system has a dedicated web-server to display these information.

As you may know, the hard task is in Step 2, which will be described below.

## The Problem and Solution
The problem CCA has to solve can be summed up as follow: 
"Provided a picture frame that contains a game of Chinese chess, please suggest the next best moves for the two players."

Based on the above problem, the solution must solve these subtasks:
1. The computer understands the board. (Solved using Computer vision with a Tensorflow Classifier model)
2. The computer suggests chess moves. (Solved using a [chinese chess engine](https://github.com/bupticybee/elephantfish) as backend with some modifications)

Here we will describe only the first subtask.

The taken frame will first go through preprocess phase to better isolate the board from the rest of the images. This preprocess has 3 steps:
1. Find mask of the board
2. Find contour and four corners
3. Perspective transform

Below is an example of a frame going through preprocessing:
<p align="center">
  <img src="https://user-images.githubusercontent.com/24392632/131324022-b35e9e9d-e618-46e1-a424-a457753f2ad5.png" width="60%" alt="Preprocess example">
</p>

After obtaining the top-down view of the board, we attempt to retrieve each position on the board by cutting the image using vertical and horizontal lines. There are total 90 positions on the board. Next, we will use a classifier model (which was specifically made an trained for this taks) to recognize the symbols on the pieces. Below is an example.

<p align="center">
  <img src="https://user-images.githubusercontent.com/24392632/131324315-c58840aa-9ffd-41e4-bc19-021e866a1e26.png" width="60%" alt="Recognition example">
</p>

Lastly, we pass the board to the engine to retrieve the suggestions.

## Photos
<div align="center">
  <img src="https://user-images.githubusercontent.com/24392632/131325232-a331b97f-b704-4c6d-aa1a-e358877b3730.png" alt="Top-down view" width="60%">
  <p><em> Image of the system in action with the chess board </em></p>
  
  <img src="https://user-images.githubusercontent.com/24392632/131325650-397fa80f-a23e-4eb8-affa-a4de096440a1.png" alt="Web-server" width="60%">
  <p><em> Image of the prediction page of the site </em></p>
</div>

## Deployment
Our project were deployed on a Raspberry Pi 3B. This device also has a small webserver that is used to deliver/broadcast the current chess game to other devices that connect to the server. For more information, please check on our report [here](https://github.com/nvatuan/chinese-chess-assistance/tree/master/report) (Vietnamese and English).

## Demonstrations
We did a small video to demonstate our project/system [here](https://youtu.be/O_xAv5Q_S-0).
