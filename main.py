from PIL import ImageGrab
import os
import time
import win32api, win32con
import math

"""
ekranın sol tarafında kaldığı için ekranın sol tarafını tarıyor oyun için

x_pad = 222
y_pad = 351
x_max = 722
y_max = 851

"""

x_pad = 222
y_pad = 351

max_depth = 4

board = [[0 for x in range(4)] for x in range(4)]


#vk kodları için offsetleri
VK_CODE = {'left':0x25,
           'up':0x26,
           'right':0x27,
           'down':0x28}
#karekordinatları
SQUARE_COORDS = {0:(65,30),
                 1:(185,30),
                 2:(305,30),
                 3:(425,30),
                 4:(65,150),
                 5:(185,150),
                 6:(305,150),
                 7:(425,150),
                 8:(65,270),
                 9:(185,270),
                 10:(305,270),
                 11:(425,270),
                 12:(65,390),
                 13:(185,390),
                 14:(305,390),
                 15:(425,390)
                 }
#kare ici
SQUARE_INDICES = {0:(0,0),
                  1:(1,0),
                  2:(2,0),
                  3:(3,0),
                  4:(0,1),
                  5:(1,1),
                  6:(2,1),
                  7:(3,1),
                  8:(0,2),
                  9:(1,2),
                  10:(2,2),
                  11:(3,2),
                  12:(0,3),
                  13:(1,3),
                  14:(2,3),
                  15:(3,3)
                  }

#karelere puan esitlemesi
SQUARE_SCORES = {0:0,
                 2:0,
                 4:4,
                 8:11,
                 16:28,
                 32:65,
                 64:141,
                 128:300,
                 256:627,
                 512:1292,
                 1024:2643,
                 2048:5372,
                 4096:10874,
                 8192:21944
                 }


SQUARE_MULTS = {0:2,
                1:2,
                2:2,
                3:2,
                4:1.25,
                5:1.25,
                6:1.25,
                7:1.25,
                8:1,
                9:1,
                10:1,
                11:1,
                12:0.8,
                13:0.8,
                14:0.8,
                15:0.8
                }
                 
#offsetli yön tusları icin
def arrowKey(direction):
    win32api.keybd_event(VK_CODE[direction],0,0,0)
    time.sleep(.05)
    win32api.keybd_event(VK_CODE[direction],0,win32con.KEYEVENTF_KEYUP,0)

#opencv kullanmıyoruz biraz hızlı işlem yapmak icin screengrap kullanıyoruz.
def screenGrab():
    box = (x_pad, y_pad, 722, 851)
    im = ImageGrab.grab(box)
    return im

#Her karenin sayısını bulur
def getSquareNumbers():
    #get the screen
    im = screenGrab()

    # tüm kareleri baktırıyoruz. 16 kare oldugu icin 16 range veriyoruz
    # eğer nesneleri tespit etmemiz gereken yer 16 kareden fazla ise bu sayıyı artırın

    for sq in range(0,16):
       # şimdi gelelim buraya
       # her nesneye nesne öğrenmesi yapmıyoruz eğer profesyonel bir şey yapacak olsak
       # ve biz bunu nesne tanımalı yapacak olsak dataset kullanırdık
       # amaaa burada her sayı farklı renkte bu yüzden renklere göre işlem yaptıracağız
       # 2 - 4 -6  tüm karelerin renkleri sabit olduğu için renk tespiti yapacağız

        rgb = im.getpixel(SQUARE_COORDS[sq])
        val = getNumberFromRGB(rgb)
        if(val == -1):
            print ("Renk Tespit edilemedi",rgb)

        #store in board
        board[sq%4][sq//4] = val
        

#Verilen rgb değerlerine sahip bir karenin sayısını döndürür
def getNumberFromRGB(rgb):
    def distance(p1,p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)
    
    if(distance(rgb,(204, 192, 179)) <= 5):
        return 0
    elif(distance(rgb,(238, 228, 218)) <= 5):
        return 2
    elif(distance(rgb,(237, 224, 200)) <= 5):
        return 4
    elif(distance(rgb,(242, 177, 121)) <= 5):
        return 8
    elif(distance(rgb,(245, 149, 99)) <= 5):
        return 16
    elif(distance(rgb,(246, 124, 95)) <= 5):
        return 32
    elif(distance(rgb,(246, 94, 59)) <= 5):
        return 64
    elif(distance(rgb,(237, 207, 114)) <= 5):
        return 128
    elif(distance(rgb,(237, 204, 97)) <= 5):
        return 256
    elif(distance(rgb,(237, 200, 80)) <= 5):
        return 512
    elif(distance(rgb,(237, 197, 63)) <= 3):
        return 1024
    elif(distance(rgb,(237, 194, 46)) <= 5):
        return 2048
    else:
        return -1

# bir kez oynar puanı hesaplar
def makeMove(array, direction):
    score = 0
    legal_move = 0
    array_temp = [[0 for x in range(0,4)] for x in range(0,4)]
    for x in range(0,16):
        array_temp[x%4][x//4] = array[x%4][x//4]

    
    if(direction == 'left'):
       #4x4 oldugu için range 4
        for y_ind in range(0,4):


            for x_ind in range(0,4):

               #burada boş kareyi tespit ediyoruz
                if(array_temp[x_ind][y_ind] == 0):
                    #boş olmayan kareyi bul
                    for x_temp in range(x_ind+1,4):
                        if(array_temp[x_temp][y_ind]):
                            #boş olmayan kareye kaydır
                            array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                            array_temp[x_temp][y_ind] = 0
                            legal_move = 1
                            break                    


            for x_ind in range(0,3):

                if(array_temp[x_ind][y_ind] == array_temp[x_ind+1][y_ind] and array_temp[x_ind][y_ind] != 0): 
                   #blokları birleştir bir kez oyna
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1

                    for x_temp in range(x_ind+1,3):
                        array_temp[x_temp][y_ind] = array_temp[x_temp+1][y_ind]

                    array_temp[3][y_ind] = 0

    if(direction == 'right'):

        for y_ind in range(0,4):


            for x_ind in range(3,-1,-1):
                if(array_temp[x_ind][y_ind] == 0):
                    for x_temp in range(x_ind-1,-1,-1):
                        if(array_temp[x_temp][y_ind]):
                            array_temp[x_ind][y_ind] = array_temp[x_temp][y_ind]
                            array_temp[x_temp][y_ind] = 0
                            legal_move = 1
                            break                    


            for x_ind in range(3,0,-1):
                if(array_temp[x_ind][y_ind] == array_temp[x_ind-1][y_ind] and array_temp[x_ind][y_ind] != 0):
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1
                    for x_temp in range(x_ind-1,0,-1):
                        array_temp[x_temp][y_ind] = array_temp[x_temp-1][y_ind]

                    array_temp[0][y_ind] = 0

    if(direction == 'up'):
        for x_ind in range(0,4):
            for y_ind in range(0,4):
                if(array_temp[x_ind][y_ind] == 0):
                    for y_temp in range(y_ind+1,4):
                        if(array_temp[x_ind][y_temp]):
                            array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                            array_temp[x_ind][y_temp] = 0
                            legal_move = 1
                            break
            for y_ind in range(0,3):
                if(array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind+1] and array_temp[x_ind][y_ind] != 0):
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1
                    for y_temp in range(y_ind+1,3):
                        array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp+1]

                    array_temp[x_ind][3] = 0

    if(direction == 'down'):
        for x_ind in range(0,4):
            for y_ind in range(3,-1,-1):
                if(array_temp[x_ind][y_ind] == 0):
                    for y_temp in range(y_ind-1,-1,-1):
                        if(array_temp[x_ind][y_temp]):
                            array_temp[x_ind][y_ind] = array_temp[x_ind][y_temp]
                            array_temp[x_ind][y_temp] = 0
                            legal_move = 1
                            break
            for y_ind in range(3,0,-1):
                if(array_temp[x_ind][y_ind] == array_temp[x_ind][y_ind-1] and array_temp[x_ind][y_ind] != 0):
                    array_temp[x_ind][y_ind] *= 2
                    score += array_temp[x_ind][y_ind]
                    legal_move = 1
                    for y_temp in range(y_ind-1,0,-1):
                        array_temp[x_ind][y_temp] = array_temp[x_ind][y_temp-1]
                    array_temp[x_ind][0] = 0
    if(legal_move == 0):
        score = -1
    return (array_temp, score)     
#verilen boşluğa 2 ekler
def makeComputerMove(array, space):
    
    array_temp = [[0 for x in range(0,4)] for x in range(0,4)]
    for x in range(0,16):
        array_temp[x%4][x//4] = array[x%4][x//4]

   #verilen kareyi 2 yap
    array_temp[space%4][space//4] = 2

    return array_temp
    
#eski görüntü ile yeni görüntüyü kopyala
def copyBoard(board1, board2):
    for x in range(0,16):
        board2[x%4][x//4] = board2[x%4][x//4]

def printBoard(array,text):
    print (text)
    print (array[0][0], " ", array[1][0], " ",array[2][0]," ",array[3][0])
    print (array[0][1], " ", array[1][1], " ",array[2][1]," ",array[3][1])
    print (array[0][2], " ", array[1][2], " ",array[2][2]," ",array[3][2])
    print (array[0][3], " ", array[1][3], " ",array[2][3]," ",array[3][3])
    print (" ")

#olasılıkları hesaplayıp en iyi sonucu işlem yapar
def search(array, depth):
    best_score = -1;
    best_move = 'down' #başka bir hamle yapamadığı zaman oyun döngüsel takılırsa fix için bir kez aşağı çek
    moves = ['left','right','up']

    for move in moves:
        score = -1
        move_results = makeMove(array,move)
        if(depth <= 0 or move_results[1] == -1):
            score = move_results[1]
        else:
            search_results = search(move_results[0],depth-1)
            score = 0.8*(move_results[1] + search_results[1])
        if(score > best_score):
            best_score = score
            best_move = move
    return (best_move,best_score)

def playerSearch(array, depth, ply):
    
    best_score = -1
    best_move = 'down'
    pv = [0 for x in range(0,ply+1)]
    moves = ['left','right','up','down']
    if(depth <= 0):
        return (best_move, evaluateBoard(array),'end')
    #search each move
    for move in moves:
        score = -1
        (new_board, move_score) = makeMove(array,move)
        if(move_score == -1):
            continue
        else:
            (score, pv_temp) = computerSearch(new_board,best_score,depth - 1, ply + 1)
        if(score > best_score):
            best_score = score
            best_move = move
            pv[0] = move
            pv[1:] = pv_temp[::]
    return (best_move, best_score, pv)
def computerSearch(array, best_score, depth, ply):

    pv = [0 for x in range(0,ply+1)]
    if(depth <= 0):
        return (evaluateBoard(array),"X")
    worst_score = 100000000
    total = 0
    moves_made = 0
    
    #tüm kareleri tekrar kontrol et
    for sq in range(0,16):

       #kare boş degils devam ke
        if(array[sq%4][sq//4] != 0):
            continue
        #yürü
        new_board = makeComputerMove(array, sq)
        (temp, score, pv_temp) = playerSearch(new_board, depth - 1, ply + 1)
        total += score
        moves_made += 1
        if(score < worst_score):
            worst_score = score
            pv[0] = sq
            pv[1:] = pv_temp[::]

    if(array[0][0] == 0):
        worst_score *= (1 - 0.1*depth)

    if(array[1][0] == 0):
        worst_score *= (1 - 0.03*depth)



    return (worst_score, pv)


def evaluateBoard(array):

    score = 0
    maximum = 0
    for sq in range(0,16):
        score += SQUARE_SCORES[array[sq%4][sq//4]]*SQUARE_MULTS[sq]
        if(array[sq%4][sq//4] > maximum):
            maximum = array[sq%4][sq//4]
    if(array[0][0] == maximum):
        score *= 1.4
    return score
        
    
def main():
    print ("Starting in 3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print ("1")
    time.sleep(1)
    print ("Start")
    print (" ")
    
    board[0][0] = 256
    board[0][1] = 8
    board[0][2] = 2
    board[0][3] = 4
    board[1][0] = 128
    board[1][1] = 0
    board[1][2] = 0
    board[1][3] = 0
    board[2][0] = 0
    board[2][1] = 0
    board[2][2] = 0
    board[2][3] = 0
    board[3][0] = 2
    board[3][1] = 0
    board[3][2] = 0
    board[3][3] = 0
    
    while True:
        getSquareNumbers()
        printBoard(board,'x')
        (move, score, pv) = playerSearch(board,5,0)
        print ("Move: ", move, " Score: ", score)
        print ("info: ", pv[::],"\n\n")
        (left, score) = makeMove(board, 'left')
        arrowKey(move)
        time.sleep(0.25)

if __name__ == '__main__':
    main()
