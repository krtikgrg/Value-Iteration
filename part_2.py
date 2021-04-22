from copy import deepcopy
from math import inf
import random
import os

filename = "./outputs/part_2_trace.txt"
filenamt = "./part_test.txt"
filenam1 = "./outputs/part_2_task_2.1_trace.txt"
filenam2 = "./outputs/part_2_task_2.2_trace.txt"
filenam3 = "./outputs/part_2_task_2.3_trace.txt"
filenafa = "./faltu.txt"

os.makedirs(os.path.dirname(filename), exist_ok=True)
FS = open(filename,"w+")


#HIT is for blade and SHOOT is for arrow

REWARD_MM = 50
DAMAGE_ARROW = 1    #scaled down
DAMAGE_BLADE = 2    #scaled down
FACTOR_HEALTH_MM = 25

W={}
C={}
E={}
N={}
S={}
MAP_STATE_TO_ACTIONS = {}
MAP_ACTIONS_TO_STATE = {}
MAP_PROBAB_TO_STATE = {}
MAP_ACTIONS_TO_NAME = {}
PROBAB_EAST = {}
PROBAB_WEST = {}
PROBAB_NORTH = {}
PROBAB_SOUTH = {}
PROBAB_CENTER = {}
reward = []
reward.append(REWARD_MM)
reward.append(0)
reward.append(0)
reward.append(0)
reward.append(0)
MAP_ACTIONS_TO_NAME["U"] = "UP"
MAP_ACTIONS_TO_NAME["D"] = "DOWN"
MAP_ACTIONS_TO_NAME["L"] = "LEFT"
MAP_ACTIONS_TO_NAME["R"] = "RIGHT"

state_MM = []
state_MM.append("D")
state_MM.append("R")

pos_IJ = []
pos_IJ.append("W")
pos_IJ.append("N")
pos_IJ.append("E")
pos_IJ.append("S")
pos_IJ.append("C")
POS_TO_INDEX = {}
POS_TO_INDEX["W"] = 0
POS_TO_INDEX["N"] = 1
POS_TO_INDEX["E"] = 2
POS_TO_INDEX["S"] = 3
POS_TO_INDEX["C"] = 4
MAP_MM_INDEX = {}
MAP_MM_INDEX["D"] = 0
MAP_MM_INDEX["R"] = 1


MAX_ARROWS = 3
MAX_MM_HEALTH = 100
MAX_MATERIALS = 2


PROB_MOVE_SUCCESSFUL = 0.85 #rest goes to EAST with prob = 0.15


PROB_ARROW_HIT_CENTER = 0.5
PROB_BLADE_HIT_CENTER = 0.1


CRAFT_ONE = 0.5
CRAFT_TWO = 0.35
CRAFT_THREE = 0.15


GATHER_MATERIAL = 0.75


PROB_ARROW_HIT_EAST = 0.9
PROB_BLADE_HIT_EAST = 0.2


#actions from west and east have 100% chance of occuring
PROB_ARROW_HIT_WEST = 0.25
PROB_BLADE_HIT_WEST = 0.0


MM_READY_STATE = 0.2
MM_DORMANT_STATE = 0.8
MM_ATTACK = 0.5     #affect only if IJ on center and east square => IJ drops arrows + MM health regain + CANCEL INDIANA action + REWARD -40
MM_REGAIN_HEALTH = 1 #scaled down
NEGATIVE_REWARD_MM = 40


STAY_STEP_COST = -10 #TEAM NUMBER = 61 => 61%3 => 1 => Y = arr[1] => Y = 1 ; 0 for task2.2, -10 for task 1
GENERAL_STEP_COST = -10
GAMMA = 0.999 #0.999 for task 1 and 0.25 for task 2.3
DELTA = 0.001


START_STATE_ONE = ['W',0,0,'D',100]
START_STATE_TWO = ['C',2,0,'R',100]

WEST_ACTIONS = ["R","S","F"]
W["R"] = "C"
W["S"] = "W"
W["F"] = "W"
PROBAB_WEST["R"] = 1.0
PROBAB_WEST["S"] = 1.0
PROBAB_WEST["F"] = 0.25


EAST_ACTIONS = ["L","S","F","H"]
E["L"] = "C"   #task 2.1 for W + C for task 1
E["S"] = "E"
E["F"] = "E"
E["H"] = "E"
PROBAB_EAST["L"] = 1.0 
PROBAB_EAST["S"] = 1.0
PROBAB_EAST["F"] = 0.9
PROBAB_EAST["H"] = 0.2


SOUTH_ACTIONS = ["U","S","G"]
S["U"] = "C"
S["S"] = "S"
S["G"] = "S"
PROBAB_SOUTH["U"] = 0.85
PROBAB_SOUTH["S"] = 0.85
PROBAB_SOUTH["G"] = 0.75


NORTH_ACTIONS = ["D","S","C"]
N["D"] = "C"
N["S"] = "N"
N["C"] = "N"
PROBAB_NORTH["D"] = 0.85 
PROBAB_NORTH["S"] = 0.85
PROBAB_NORTH["C"] = 1.0 

CENTER_ACTIONS = ["U","S","L","R","D","F","H"]
C["U"] = "N"
C["D"] = "S"
C["L"] = "W"
C["R"] = "E"
C["S"] = "C"
C["F"] = "C"
C["H"] = "C"
PROBAB_CENTER["U"] = 0.85
PROBAB_CENTER["D"] = 0.85
PROBAB_CENTER["L"] = 0.85
PROBAB_CENTER["R"] = 0.85
PROBAB_CENTER["S"] = 0.85
PROBAB_CENTER["F"] = 0.5
PROBAB_CENTER["H"] = 0.1

MAP_STATE_TO_ACTIONS['W'] = WEST_ACTIONS
MAP_STATE_TO_ACTIONS['N'] = NORTH_ACTIONS
MAP_STATE_TO_ACTIONS['E'] = EAST_ACTIONS
MAP_STATE_TO_ACTIONS['S'] = SOUTH_ACTIONS
MAP_STATE_TO_ACTIONS['C'] = CENTER_ACTIONS

MAP_ACTIONS_TO_STATE['W'] = W
MAP_ACTIONS_TO_STATE['N'] = N
MAP_ACTIONS_TO_STATE['E'] = E
MAP_ACTIONS_TO_STATE['S'] = S
MAP_ACTIONS_TO_STATE['C'] = C 

MAP_PROBAB_TO_STATE["W"] = PROBAB_WEST
MAP_PROBAB_TO_STATE["N"] = PROBAB_NORTH
MAP_PROBAB_TO_STATE["E"] = PROBAB_EAST
MAP_PROBAB_TO_STATE["S"] = PROBAB_SOUTH
MAP_PROBAB_TO_STATE["C"] = PROBAB_CENTER

MAP_ACTION_TO_VARIABLE = {}
MAP_ACTION_TO_VARIABLE["UP"] = "U"
MAP_ACTION_TO_VARIABLE["DOWN"] = "D"
MAP_ACTION_TO_VARIABLE["LEFT"] = "L"
MAP_ACTION_TO_VARIABLE["RIGHT"] = "R"
MAP_ACTION_TO_VARIABLE["SHOOT"] = "F"
MAP_ACTION_TO_VARIABLE["STAY"] = "S"
MAP_ACTION_TO_VARIABLE["HIT"] = "H"
MAP_ACTION_TO_VARIABLE["GATHER"] = "G"
MAP_ACTION_TO_VARIABLE["CRAFT"] = "C"

state_utility = []
policy_sel = []
for i in range(5): # pos{{W = 0} {N = 1} {E = 2} {S = 3} {c = 4}}
    temp_mat = []
    temp_mat1 = []
    for j in range(3): # materials
        temp_arrow = []
        temp_arrow1 = []
        for k in range(4): # arrows
            temp_state = []
            temp_state1 = []
            for l in range(2): # state of MM {{D = 0} {R = 1}}
                temp_Health = []
                temp_Health1 = []
                for m in range(5): # heath {{%{health}/25}}
                    temp_Health.append(0)
                    if(m>=1):
                        temp_Health1.append("")
                    else:
                        temp_Health1.append("NONE")
                temp_state.append(temp_Health)
                temp_state1.append(temp_Health1)
            temp_arrow.append(temp_state)
            temp_arrow1.append(temp_state1)
        temp_mat.append(temp_arrow)
        temp_mat1.append(temp_arrow1)
    state_utility.append(temp_mat)
    policy_sel.append(temp_mat1)

    # stepIJ(healthMM,state_MM[1],arrowWithIJ,matWithIJ,localPos,state_utility,0.2)
def stepIJ(healthMM,stateMM,arrowWithIJ,matWithIJ,localPos,state_utility,scale,stay = 1):
    # print("Kartik")
    #stay => 0,1,2,3 => stay =0
    # if healthMM == 25 and stateMM == "R" and arrowWithIJ == 1 and matWithIJ == 0 and localPos == "W":
        # print("scale",scale,stay)
    actions = MAP_STATE_TO_ACTIONS[localPos] #kya kya actions possible hai
    move = MAP_ACTIONS_TO_STATE[localPos] #kahan gya kis action ko lekar
    probab = MAP_PROBAB_TO_STATE[localPos] #probab of each action
    actionS = ""
    maxUti = -inf
    addfactor = 0
    #dormant, scale =attacking probab, stay =3
    # if stay == 3:
    #     addfactor = 1
    for action in actions:
        finPos = move[action]
        finMat = matWithIJ
        finArr = arrowWithIJ
        finHea = healthMM//FACTOR_HEALTH_MM #scaled down
        finSta = MAP_MM_INDEX[stateMM] #R=>1;D=>0
        sucPro = probab[action]
        fin2Hea = min(4,finHea+addfactor)
        newval = 0
        if stay!=2 and action == "C":
            if matWithIJ > 0:
                finMat = matWithIJ - 1
                #one arrow
                finArr = min(MAX_ARROWS,arrowWithIJ+1)
                a = scale * CRAFT_ONE * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
                a = a + ((1.0-scale) * CRAFT_ONE * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
                #two arrow
                finArr = min(MAX_ARROWS,arrowWithIJ+2)
                b = scale * CRAFT_TWO * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
                b = b + ((1.0-scale) * CRAFT_TWO * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
                #three arrow
                finArr = min(MAX_ARROWS,arrowWithIJ+3)
                c = scale * CRAFT_THREE * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
                c = c + ((1.0-scale) * CRAFT_THREE * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
                maxUti = max(maxUti,a+b+c)
                priThing = a+b+c
                newval = a+b+c
                # if(maxUti == (a+b+c)):
                #     actionS = "CRAFT"
                if abs(maxUti - priThing) <= 1e-6:
                    actionS = "CRAFT"
            # else:
            #     a = scale * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            #     maxUti = max(maxUti,a)
            #     if(maxUti == a):
            #         actionS = "CRAFT"
        elif stay!=2 and action == "G":
            b = scale * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            b = b + ((1.0-scale) * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
            matNum = 1
            temp_mat_num = finMat + matNum
            if temp_mat_num <= MAX_MATERIALS:
                finMat = temp_mat_num
            else:
                finMat = MAX_MATERIALS
            a = scale * sucPro * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            a = a + ((1.0-scale) * sucPro * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
            maxUti = max(maxUti,a+b)
            priThing = a+b
            newval = a+b
            if abs(maxUti - priThing) <= 1e-6:
                actionS = "GATHER"
        elif stay!=2 and action == "H":
            b = scale * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            b = b + ((1.0-scale) * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
            finHea = max(0,finHea - DAMAGE_BLADE)
            fin2Hea = max(0,fin2Hea - DAMAGE_BLADE)
            a = scale * (sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            a = a + ((1.0-scale) * (sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
            maxUti = max(maxUti,a+b)
            priThing = a+b
            newval = a+b
            if abs(maxUti - priThing) <= 1e-6:
                actionS = "HIT"
        elif stay!=2 and action == "F":
            if finArr >=1 :
                finArr -= 1
                b = scale * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
                b = b + ((1.0-scale) * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
                finHea = max(0,finHea - DAMAGE_ARROW)
                fin2Hea = max(0,fin2Hea - DAMAGE_ARROW)
                a = scale * (sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
                a = a + ((1.0-scale) * (sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea])) 
                maxUti = max(maxUti,a+b)
                priThing = a+b
                newval = a+b
                if abs(maxUti - priThing) <= 1e-6:
                    actionS = "SHOOT"
            # else:
            #     a = scale * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            #     a = a + ((1.0-scale) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
            #     maxUti = max(maxUti,a)
            #     if(maxUti == a):
            #         actionS = "SHOOT"
        elif stay!=0 and action == "S":
            b = scale * (1.0-sucPro) * (STAY_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX["E"]][finMat][finArr][finSta][fin2Hea])
            a = scale * (sucPro) * (STAY_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            b = b + ((1.0-scale) * (1.0-sucPro) * (STAY_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX["E"]][finMat][finArr][1-finSta][finHea]))
            a = a + ((1.0-scale) * (sucPro) * (STAY_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
            maxUti = max(maxUti,a+b)
            priThing = a+b
            newval = a+b
            if abs(maxUti - priThing) <= 1e-6:
                actionS = "STAY"
        elif stay!=2 and (action == "L" or action == "R" or action == "U" or action == "D"):
            b = scale * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX["E"]][finMat][finArr][finSta][fin2Hea])
            a = scale * (sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][finSta][fin2Hea])
            b = b + ((1.0-scale) * (1.0-sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX["E"]][finMat][finArr][1-finSta][finHea]))
            a = a + ((1.0-scale) * (sucPro) * (GENERAL_STEP_COST + reward[finHea] + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][finArr][1-finSta][finHea]))
            maxUti = max(maxUti,a+b)
            priThing = a+b
            newval = a+b
            if abs(maxUti - priThing) <= 1e-6:
                actionS = MAP_ACTIONS_TO_NAME[action]
        # if localPos == "W" and matWithIJ == 0 and arrowWithIJ == 1 and stateMM == "R" and healthMM == 25:
        #     print("testing")
        #     print(action)
        #     print(newval)
        #     print(sucPro)
        #     print(finArr)
        #     print(finSta)
        #     print(finMat)
        #     print(finHea)
        #     print(fin2Hea)
        #     print(scale)
    return maxUti,actionS

def step_IJ(healthMM,stateMM,arrowWithIJ,matWithIJ,localPos,state_utility,scale1):
    #do some thing
    # print("Ayush")
    #ready,attack
    #center, east => common move =>left
    finHea = healthMM//FACTOR_HEALTH_MM # 25 => 1
    finSta = MAP_MM_INDEX[stateMM] #1
    finArr = arrowWithIJ
    finMat = matWithIJ
    finPos = localPos
    # ATTACK * 
    # GENERAL
    # STAY
    # Stay step is different from other steps
    testing1,testing2 = stepIJ(healthMM,stateMM,arrowWithIJ,matWithIJ,localPos,state_utility,1.0,0) #moves => not stay => move best result not considering stay move for any state
    a = (1.0 - scale1) * testing1 #not attack + other than saty action
    testing3,testing4 = stepIJ(healthMM,stateMM,arrowWithIJ,matWithIJ,localPos,state_utility,1.0,2) #stay only => STAY 
    b = (1.0 - scale1) * testing3 #not attach + saty action
    finHea = min(4,1+(healthMM//FACTOR_HEALTH_MM)) # 25 => 1
    maxUti = -inf
    a = a + (scale1 * (GENERAL_STEP_COST + reward[finHea]- 40 + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][0][1-finSta][finHea])) #attack + other than stay
    b = b + (scale1 * (STAY_STEP_COST + reward[finHea]- 40 + GAMMA * state_utility[POS_TO_INDEX[finPos]][finMat][0][1-finSta][finHea])) #attack + stay
    maxUti = max(maxUti,a,b)
    actionS = ""
    priThing = a
    priThing1 = b
    if abs(maxUti - priThing) <= 1e-6:
        actionS = testing2
    elif abs(maxUti - priThing1) <= 1e-6:
        # print("AYUSH BOND KI TEAM MEIN 3 LDKIYAN")
        actionS = testing4 #STAY
    return maxUti,actionS

sigmaDelta = 0
next_state_utility = deepcopy(state_utility)
curDiff = inf
iter_ctr = 0
while(curDiff>DELTA):
    # if iter_ctr == 2:
    #     exit()
    state_utility = deepcopy(next_state_utility)
    curDiff = -inf
    # print("iteration="+str(iter_ctr))
    FS.write("iteration="+str(iter_ctr)+"\n")
    for i in range(5): #pos
        for j in range(3): #mat
            for k in range(4): #arrow
                for l in range(2): #stateMM
                    for m in range(5): #healthMM
                        localPos = pos_IJ[i] #character
                        matWithIJ = j #int
                        arrowWithIJ = k #int
                        stateMM = state_MM[l] #character
                        healthMM = m * FACTOR_HEALTH_MM #actual health without scale
                        if healthMM == 0:
                            next_state_utility[i][j][k][l][m] = 0.000
                            # print("("+localPos+","+str(matWithIJ)+","+str(arrowWithIJ)+","+stateMM+","+str(healthMM)+") :NONE=[0.000]")
                            FS.write("("+localPos+","+str(matWithIJ)+","+str(arrowWithIJ)+","+stateMM+","+str(healthMM)+"):NONE=[0.000]\n")
                            # FS.write("("+localPos+","+str(matWithIJ)+","+str(arrowWithIJ)+","+stateMM+","+str(healthMM)+")=[0.000]\n")
                            # print("Aaradhya")
                            continue
                        # two independent events => {MM ka choice || IJ kya kaam krta} => p(1) * P(2) => state A -> state B => 1,2 => 1 inter 2 => P(1) * P(2)
                        a = -inf
                        actionA = ""
                        actionS = ""
                        if stateMM == "D":
                            # if i==0 and j==0 and k ==1 and l==0 and m==1:
                                # print("fuckAll",MM_READY_STATE)
                            a,actionA = stepIJ(healthMM,state_MM[1],arrowWithIJ,matWithIJ,localPos,state_utility,0.2)
                        else:
                            # if i==0 and j==0 and k ==1 and l==0 and m==1:
                                # print("fuckAll2")
                            if localPos == 'C' or localPos == 'E':
                                a,actionA = step_IJ(healthMM,state_MM[1],arrowWithIJ,matWithIJ,localPos,state_utility,0.5)
                            else:  #gadbad health regain
                                a,actionA = stepIJ(healthMM,state_MM[0],arrowWithIJ,matWithIJ,localPos,state_utility,0.5,3)
                        maxUti = a
                        actionS = actionA
                        curDiff = max(curDiff,abs(maxUti-state_utility[i][j][k][l][m]))
                        next_state_utility[i][j][k][l][m] = maxUti
                        policy_sel[i][j][k][l][m] = actionS
                        # print("("+localPos+","+str(matWithIJ)+","+str(arrowWithIJ)+","+stateMM+","+str(healthMM)+") :"+actionS+"=["+str((int(maxUti*1000))/1000.0)+"]")
                        # FS.write("("+localPos+","+str(matWithIJ)+","+str(arrowWithIJ)+","+stateMM+","+str(healthMM)+") :"+actionS+"=["+str((int(maxUti*1000))/1000.0)+"]\n")
                        FS.write("("+localPos+","+str(matWithIJ)+","+str(arrowWithIJ)+","+stateMM+","+str(healthMM)+"):"+actionS+"=["+ "{:0.3f}".format(round(maxUti, 3))+"]\n")
                        # FS.write("("+localPos+","+str(matWithIJ)+","+str(arrowWithIJ)+","+stateMM+","+str(healthMM)+")"+"=["+ "{:0.3f}".format(round(maxUti, 3))+"]\n")
                        # + "{:0.3f}]".format(round(utility, 3))
    iter_ctr += 1
    sigmaDelta += curDiff
print(sigmaDelta/iter_ctr)
# exit()
# print("")
# print("")

# FS.write("")
# FS.write("")


START_STATE_ONE[4] = START_STATE_ONE[4] // FACTOR_HEALTH_MM
strt_ctr = 0
while(START_STATE_ONE[4] != 0) and strt_ctr != 25:
    strt_ctr +=1
    localPos = START_STATE_ONE[0] #character
    matWithIJ = START_STATE_ONE[1] #int
    arrowWithIJ = START_STATE_ONE[2] #int
    stateMM = START_STATE_ONE[3] #character
    healthMM = START_STATE_ONE[4] #with scale
    # print(POS_TO_INDEX[localPos])
    # print(matWithIJ)
    # print(arrowWithIJ)
    # print(MAP_MM_INDEX[stateMM])
    # print(healthMM//FACTOR_HEALTH_MM)
    action = policy_sel[POS_TO_INDEX[localPos]][matWithIJ][arrowWithIJ][MAP_MM_INDEX[stateMM]][healthMM]
    print(START_STATE_ONE)
    print("Take Action: "+action)
    if action == "NONE":
        break
    action = MAP_ACTION_TO_VARIABLE[action]
    actions = MAP_STATE_TO_ACTIONS[localPos]
    move = MAP_ACTIONS_TO_STATE[localPos]    
    probabArr = MAP_PROBAB_TO_STATE[localPos]
    if stateMM == "D":
        probab = random.uniform(0.0,1.0)
        if probab<=0.2:
            START_STATE_ONE[3] = "R"
        else:
            START_STATE_ONE[3] = "D"
        if action == "U" or action == "D" or action =="L" or action == "R" or action == "S":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                START_STATE_ONE[0] = move[action]
            else:
                START_STATE_ONE[0] = "E"
        elif action == "C":
            if matWithIJ>0:
                START_STATE_ONE[1] -= 1
                probab = random.uniform(0.0,1.0)
                newArr = arrowWithIJ
                if probab <= CRAFT_ONE:
                    newArr = min(MAX_ARROWS,1+newArr)
                elif probab <= CRAFT_ONE+CRAFT_TWO:
                    newArr = min(MAX_ARROWS,2+newArr)
                else:
                    newArr = min(MAX_ARROWS,3+newArr)
                START_STATE_ONE[2] = newArr
        elif action == "G":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                START_STATE_ONE[1] = min(MAX_MATERIALS,1+START_STATE_ONE[1])
        elif action == "F":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                if arrowWithIJ > 0:
                    START_STATE_ONE[2] -= 1
                    START_STATE_ONE[4] -= 1
            else:
                if arrowWithIJ > 0:
                    START_STATE_ONE[2] -= 1
        elif action == "H":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                    START_STATE_ONE[4] = max(0,START_STATE_ONE[4] - 2)
    else:
        probab = random.uniform(0.0,1.0)
        if probab <= MM_ATTACK and (START_STATE_ONE[0] == "C" or START_STATE_ONE[0] == "E"):
            START_STATE_ONE[2] = 0
            START_STATE_ONE[3] = "D"
            START_STATE_ONE[4] = min(4,START_STATE_ONE[4]+1)
        else: 
            factor = 1.0
            if probab <= MM_ATTACK:
                START_STATE_ONE[3] = "D"
                START_STATE_ONE[4] = min(4,START_STATE_ONE[4]+1)
                factor = 1.0
            else:
                factor = 1.0
            
            if action == "U" or action == "D" or action =="L" or action == "R" or action == "S":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                    START_STATE_ONE[0] = move[action]
                else:
                    START_STATE_ONE[0] = "E"
            elif action == "C":
                if matWithIJ>0:
                    START_STATE_ONE[1] -= 1
                    probab = random.uniform(0.0,1.0)
                    newArr = arrowWithIJ
                    if probab <= CRAFT_ONE*factor:
                        newArr = min(MAX_ARROWS,1+newArr)
                    elif probab <= (CRAFT_ONE+CRAFT_TWO)*factor:
                        newArr = min(MAX_ARROWS,2+newArr)
                    elif probab <= (CRAFT_TWO+CRAFT_THREE+CRAFT_ONE)*factor:
                        newArr = min(MAX_ARROWS,3+newArr)
                    START_STATE_ONE[2] = newArr
            elif action == "G":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                    START_STATE_ONE[1] = min(MAX_MATERIALS,1+START_STATE_ONE[1])
            elif action == "F":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                    if arrowWithIJ > 0:
                        START_STATE_ONE[2] -= 1
                        START_STATE_ONE[4] -= 1
                else:
                    if arrowWithIJ > 0:
                        START_STATE_ONE[2] -= 1
            elif action == "H":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                        START_STATE_ONE[4] = max(0,START_STATE_ONE[4] - 2)

print(START_STATE_ONE)
if(strt_ctr == 25):
    print("ended due to limitation")


print("")
print("")

START_STATE_TWO[4] = START_STATE_TWO[4] // FACTOR_HEALTH_MM
strt_ctr = 0
while(START_STATE_TWO[4] != 0) and strt_ctr!=25:
    strt_ctr += 1
    localPos = START_STATE_TWO[0] #character
    matWithIJ = START_STATE_TWO[1] #int
    arrowWithIJ = START_STATE_TWO[2] #int
    stateMM = START_STATE_TWO[3] #character
    healthMM = START_STATE_TWO[4] #with scale
    # print(POS_TO_INDEX[localPos])
    # print(matWithIJ)
    # print(arrowWithIJ)
    # print(MAP_MM_INDEX[stateMM])
    # print(healthMM//FACTOR_HEALTH_MM)
    action = policy_sel[POS_TO_INDEX[localPos]][matWithIJ][arrowWithIJ][MAP_MM_INDEX[stateMM]][healthMM]
    print(START_STATE_TWO)
    print("Take Action: "+action)
    if action == "NONE":
        break
    action = MAP_ACTION_TO_VARIABLE[action]
    actions = MAP_STATE_TO_ACTIONS[localPos]
    move = MAP_ACTIONS_TO_STATE[localPos]    
    probabArr = MAP_PROBAB_TO_STATE[localPos]
    if stateMM == "D":
        probab = random.uniform(0.0,1.0)
        if probab<=0.2:
            START_STATE_TWO[3] = "R"
        else:
            START_STATE_TWO[3] = "D"
        if action == "U" or action == "D" or action =="L" or action == "R" or action == "S":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                START_STATE_TWO[0] = move[action]
            else:
                START_STATE_TWO[0] = "E"
        elif action == "C":
            if matWithIJ>0:
                START_STATE_TWO[1] -= 1
                probab = random.uniform(0.0,1.0)
                newArr = arrowWithIJ
                if probab <= CRAFT_ONE:
                    newArr = min(MAX_ARROWS,1+newArr)
                elif probab <= CRAFT_ONE+CRAFT_TWO:
                    newArr = min(MAX_ARROWS,2+newArr)
                else:
                    newArr = min(MAX_ARROWS,3+newArr)
                START_STATE_TWO[2] = newArr
        elif action == "G":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                START_STATE_TWO[1] = min(MAX_MATERIALS,1+START_STATE_TWO[1])
        elif action == "F":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                if arrowWithIJ > 0:
                    START_STATE_TWO[2] -= 1
                    START_STATE_TWO[4] -= 1
            else:
                if arrowWithIJ > 0:
                    START_STATE_TWO[2] -= 1
        elif action == "H":
            probab = random.uniform(0.0,1.0)
            if probab <= probabArr[action]:
                    START_STATE_TWO[4] = max(0,START_STATE_TWO[4] - 2)
    else:
        probab = random.uniform(0.0,1.0)
        if probab <= MM_ATTACK and (START_STATE_TWO[0] == "C" or START_STATE_TWO[0] == "E"):
            START_STATE_TWO[2] = 0
            START_STATE_TWO[3] = "D"
            START_STATE_TWO[4] = min(4,START_STATE_TWO[4]+1)
        else: 
            factor = 1.0
            if probab <= MM_ATTACK:
                START_STATE_TWO[3] = "D"
                START_STATE_TWO[4] = min(4,START_STATE_TWO[4]+1)
                factor = MM_ATTACK
            else:
                factor = 1.0 - MM_ATTACK
            
            if action == "U" or action == "D" or action =="L" or action == "R" or action == "S":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                    START_STATE_TWO[0] = move[action]
                else:
                    START_STATE_TWO[0] = "E"
            elif action == "C":
                if matWithIJ>0:
                    START_STATE_TWO[1] -= 1
                    probab = random.uniform(0.0,1.0)
                    newArr = arrowWithIJ
                    if probab <= CRAFT_ONE*factor:
                        newArr = min(MAX_ARROWS,1+newArr)
                    elif probab <= (CRAFT_ONE+CRAFT_TWO)*factor:
                        newArr = min(MAX_ARROWS,2+newArr)
                    elif probab <= (CRAFT_TWO+CRAFT_THREE+CRAFT_ONE)*factor:
                        newArr = min(MAX_ARROWS,3+newArr)
                    START_STATE_TWO[2] = newArr
            elif action == "G":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                    START_STATE_TWO[1] = min(MAX_MATERIALS,1+START_STATE_TWO[1])
            elif action == "F":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                    if arrowWithIJ > 0:
                        START_STATE_TWO[2] -= 1
                        START_STATE_TWO[4] -= 1
                else:
                    if arrowWithIJ > 0:
                        START_STATE_TWO[2] -= 1
            elif action == "H":
                probab = random.uniform(0.0,1.0)
                if probab <= probabArr[action]*factor:
                        START_STATE_TWO[4] = max(0,START_STATE_TWO[4] - 2)

print(START_STATE_TWO)
if(strt_ctr == 25):
    print("ended due to limitation")

            
        

# regain+arrow => 0 even in the case of 100 health
# 100 + 25 => 100 -25 => 75
# C,1,3,D,100 => shoot => shoot => shoot => north => craft => south => shoot
#                 -10 -10 -10 -10 -10 -10 +50       => -10
# greator than equal to -10 => all positive numbers and negative numebrs from [0 ,-10]
# A => B => D
# Bellman Equation
# max for all actions [ sigma     P(s`|s,a) * ( stepcost + reward + gamma * util )] => up,left,right,down ======> WRONG PERFECTLY WRONG 
# max for all actions cartesianProduct stateMM [  sigma  P(s`|s,a,a_F_MM) ] * (stepcost + reward + gamma * util)]
#s`` (original state) => s => s`
# P(s`|s,a) assume krke ki mai state s
# P(s`` => s) MM
# p(s => s`) PLAYER
# p(s`` => s`) 
# s``=> s MON
# s => a` IJ
# P(s`` => s`) = P(s`` => s) * P(s => s`)
# bifurcation step` step => step`` => action step+step`
# W,0,0,R/D,100