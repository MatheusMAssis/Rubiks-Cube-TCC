import numpy as np
import random as rd


########################
#--- CUBE MOVEMENTS ---#
########################

#--- FRONT ---#

def F(arr):
    arr[6:9, 0:3] = np.fliplr(arr[6:9, 0:3].transpose())
    t1 = np.array(arr[2, 0:3])
    t2 = np.array(arr[9:12, 0])
    t3 = np.array(arr[15, 0:3])
    t4 = np.array(arr[3:6, 2])
    arr[2, 0:3] = np.fliplr([t4])[0]
    arr[9:12, 0] = t1
    arr[15, 0:3] = np.fliplr([t2])[0]
    arr[3:6, 2] = t3

def Fi(arr):
    F(arr)
    F(arr)
    F(arr)

#--- UP ---#

def U(arr):
    arr[0:3, 0:3] = np.fliplr(arr[0:3, 0:3].transpose())
    t1 = np.array(arr[12, 0:3])
    t2 = np.array(arr[9, 0:3])
    t3 = np.array(arr[6, 0:3])
    t4 = np.array(arr[3, 0:3])
    arr[12, 0:3] = t4
    arr[9, 0:3] = t1
    arr[6, 0:3] = t2
    arr[3, 0:3] = t3

def Ui(arr):
    U(arr)
    U(arr)
    U(arr)

#--- DOWN ---#

def D(arr): 
    arr[15:18, 0:3] = np.fliplr(arr[15:18, 0:3].transpose())
    t1 = np.array(arr[8, 0:3])
    t2 = np.array(arr[11, 0:3])
    t3 = np.array(arr[14, 0:3])
    t4 = np.array(arr[5, 0:3])
    arr[8, 0:3] = t4
    arr[11, 0:3] = t1
    arr[14, 0:3] = t2
    arr[5, 0:3] = t3

def Di(arr):
    D(arr)
    D(arr)
    D(arr)

#--- LEFT ---#

def L(arr):
    arr[3:6, 0:3] = np.fliplr(arr[3:6, 0:3].transpose())
    t1 = np.array(arr[0:3, 0])
    t2 = np.array(arr[6:9, 0])
    t3 = np.array(arr[15:18, 0])
    t4 = np.array(arr[12:15, 2])
    arr[0:3, 0] = np.fliplr([t4])[0]
    arr[6:9, 0] = t1
    arr[15:18, 0] = t2
    arr[12:15, 2] = np.fliplr([t3])[0]

def Li(arr):
    L(arr)
    L(arr)
    L(arr)

#--- RIGHT ---#

def R(arr):
    arr[9:12, 0:3] = np.fliplr(arr[9:12, 0:3].transpose())
    t1 = np.array(arr[0:3, 2])
    t2 = np.array(arr[12:15, 0])
    t3 = np.array(arr[15:18, 2])
    t4 = np.array(arr[6:9, 2])
    arr[0:3, 2] = t4
    arr[12:15, 0] = np.fliplr([t1])[0]
    arr[15:18, 2] = np.fliplr([t2])[0]
    arr[6:9, 2] = t3

def Ri(arr):
    R(arr)
    R(arr)
    R(arr)

#--- BACK ---#

def B(arr):
    arr[12:15, :] = np.fliplr(arr[12:15, :].transpose())
    t1 = np.array(arr[0, 0:3])
    t2 = np.array(arr[3:6, 0])
    t3 = np.array(arr[17, 0:3])
    t4 = np.array(arr[9:12, 2])
    arr[0, 0:3] = t4
    arr[3:6, 0] = np.fliplr([t1])[0]
    arr[17, 0:3] = t2
    arr[9:12, 2] = np.fliplr([t3])[0]

def Bi(arr):
    B(arr)
    B(arr)
    B(arr)


#--- MOVEMENT ---#

def make_move(arr, move):
    if move == 1 or move == "F":
        F(arr)
        return "F"
    elif move == 2 or move == "Fi":
        Fi(arr)
        return "Fi"
    elif move == 3 or move == "U":
        U(arr)
        return "U"
    elif move == 4 or move == "Ui":
        Ui(arr)
        return "Ui"
    elif move == 5 or move == "D":
        D(arr)
        return "D"
    elif move == 6 or move == "Di":
        Di(arr)
        return "Di"
    elif move == 7 or move == "L":
        L(arr)
        return "L"
    elif move == 8 or move == "Li":
        Li(arr)
        return "Li"
    elif move == 9 or move == "R":
        R(arr)
        return "R"
    elif move == 10 or move == "Ri":
        Ri(arr)
        return "Ri"
    elif move == 11 or move == "B":
        B(arr)
        return "B"
    elif move == 12 or move == "Bi":
        Bi(arr)
        return "Bi"


###########################
#--- AUXILIAR FUNCTION ---#
###########################

def scramble(arr, n):
    list_of_movements = []
    scramble_list = [rd.randint(1, 12) for i in range(n)]
    for movement in scramble_list:
        move = make_move(arr, movement)
        list_of_movements.append(move)
    return list_of_movements