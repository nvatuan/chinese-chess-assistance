import cv2
import numpy as np

UNIT_SIZE = 57

def placePiece(px, py, piece, canvas, mx=2, my=3):
    w, h, _ = piece.shape
    ox, oy = px * UNIT_SIZE, py * UNIT_SIZE
    for x in range(w):
        for y in range(h):
            if piece[x][y][3] != 0: # if [x][y] pixel is not transparent
                canvas[ox+x+mx][oy+y+my] = piece[x][y]

def mapTextureToSignature(PATH = './texture'):
    from os.path import exists
    COLOR = ['b', 'r']
    PIECE = ['x', 'm', 't', 's', 'g', 'p', 'c']
    POSTFIX = ['', '_selected']
    EXTENSION = ['.png']

    # a mapping map letters to img object
    m = {}

    # generate blank img
    bl = np.zeros((UNIT_SIZE, UNIT_SIZE, 4), np.uint8)
    m['-'] = bl

    # loading icon for unknown images
    unk = PATH + '/' + 'unknown.png'
    if not exists(unk):
        print('Could not load: File [', unk, '] does not exists.')
        m['?'] = m['-']
    else:
        m['?'] = cv2.imread(unk, cv2.IMREAD_UNCHANGED)

    # loading pieces' img
    for c in COLOR:
        for p in PIECE:
            for post in POSTFIX:
                for e in EXTENSION:
                    file = PATH + '/' + c + p + post + e
                    if not exists(file):
                        print('Could not load: File [', file, '] does not exists.')
                        m[sign] = m['?']
                    else:
                        sign = p if c == 'b' else p.upper()
                        sign = sign if post == '' else sign + '*'

                        m[sign] = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    
    return m

def renderBoard(descriptor, outputName = 'board.png', PATH = './texture'):
    from os.path import exists, dirname, abspath
    if not exists(PATH):
        print('FATAL: Texture directory [', dirname(os.path.abspath(__file__)) + PATH[1:], '] could not be found. Aborting..')
        return False

    if not exists(PATH + "/canvas.png"):
        print('FATAL: Could not load canvas[', PATH + "/canvas.png", "]. Aborting..");
        return False
    
    if len(descriptor) < 90:
        print('FATAL: Descriptor string length is less than required. (< 90)')
        return False

    canv = cv2.imread(PATH + "/canvas.png", cv2.IMREAD_UNCHANGED)
    texture = mapTextureToSignature()

    for x in range(10):
        for y in range(9):
            index = x*9 + y
            placePiece(x, y, texture.get(descriptor[index], texture['?']), canv)
    
    #cv2.imshow('Board', canv); cv2.waitKey(0);
    cv2.imwrite(outputName, canv)
    return True

if __name__ == "__main__":
    import sys

    if len(sys.argv) <= 1:
        print('Syntax: render.py <board_description> [output_file_name]')
        print('Need at least 1 arguments: <board_desciption>\n')
        print('\t> <board_desciption> is a string describing the board.\n' +
            '\tThe string descriptor is a 90 letters string, each letter from left to right is describing\n ' +
            '\ta position on the board from the top-left going left to right and top to bottom.\n' +
            '\tA letter can be:\n' +
            '\t\t' + '- \'x\' for black rook\n' + 
            '\t\t' + '- \'m\' for black knight\n' +
            '\t\t' + '- \'t\' for black elephant\n' +
            '\t\t' + '- \'s\' for black advisor\n' +
            '\t\t' + '- \'g\' for black general\n' +
            '\t\t' + '- \'p\' for black cannon\n' +
            '\t\t' + '- \'c\' for black soldier\n' +
            '\t\t' + '- Each of the above but uppercase for corresponding piece but red\n' + 
            '\t\t' + '- \'-\' for blank\n' +
            '\tFor example, the descriptor string for the staring position is:\n' +
            '\t\'xmtsgstmx----------p-----p-c-c-c-c-c------------------C-C-C-C-C-P-----P----------XMTSGSTMX\'\n' +
            '\tEach letter above is corresponding with a image file name, they will be loaded all before actual\n' +
            '\tdrawing work is done.\n' +
            '\n' +
            '\t> The [output_file_name] is the output image name. Optional. Default value is \'board.png\'.'
        )
    elif len(sys.argv) == 2:
        renderBoard(sys.argv[1])
    else:
        renderBoard(sys.argv[1], sys.argv[2])