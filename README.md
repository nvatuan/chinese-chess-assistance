# dev-boardPreprocess
This is the branch that is responsible for normalizing and extracting 90 positions (9 columns, 10 rows) of the chess board.

## Warp into a rectangle
The board is a rectangle but because of the camera angle it might be warped. This step will re-warp the board into a straight rectangle.

## Crop into 90 positions
After acquiring a top-down view of the board, the board will be cropped into 90 small images, corresponding to 90 positions on the table.
