from cspbase import *
import time


def enforce_gac(constraint_list):
    '''Input a list of constraint objects, each representing a constraint, then 
       enforce GAC on them pruning values from the variables in the scope of
       these constraints. Return False if a DWO is detected. Otherwise, return True. 
       The pruned values will be removed from the variable object cur_domain. 
       enforce_gac modifies the variable objects that are in the scope of
       the constraints passed to it.'''

#<<<your implemenation of enforce_gac below
    
    
    listOfCons = list(constraint_list)
    conQueue = list(constraint_list)
    while (len(conQueue) != 0):
        eachCon = conQueue.pop(0)
        for eachVar in eachCon.scope:
            gacIndex = 0
            limit = len(eachVar.curdom)
            while (gacIndex != limit):
                eachValue = eachVar.curdom[gacIndex]
                assign = eachCon.has_support(eachVar, eachValue)
                gacIndex = gacIndex + 1
                if (assign == False):
                    eachVar.prune_value(eachValue)
                    gacIndex = gacIndex - 1
                    if (len(eachVar.curdom) == 0):
                        conQueue = []
                        return 'DWO'
                    else:
                        for otherCons in listOfCons :
                            existOrNot_Var = False
                            existOrNot_Con = True
                            
                            for m in otherCons.scope:
                                if eachVar.name == m.name:
                                    existOrNot_Var = True
                                    break
                            for g in conQueue:
                                if g.name == otherCons.name:
                                    existOrNot_Con = False
                                    break
                            if (existOrNot_Var and existOrNot_Con):
                                tempCur = otherCons.sat_tuples[:]
                                new_Con = Constraint(otherCons.name, otherCons.scope)
                                addTuples(new_Con)  # add new tuples for the new constraint
                                
                                conQueue.append(new_Con)
                
                limit = len(eachVar.curdom)  # update the len of curdom since it might be changed
    return True
                                        
            

#>>>your implemenation of enforce_gac above

                            
def sudoku_enforce_gac_model_1(initial_sudoku_board):
    '''The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [
       [0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       In model_1 you should create a variable for each cell of the
       board, with domain equal to {1-9} if the board has a 0 at that
       position, and domain equal {i} if the board has a fixed number i
       at that cell. 
       
       Model_1 should create BINARY CONSTRAINTS OF NOT-EQUAL between all
       relevant variables (e.g., all pairs of variables in the same
       row), then invoke enforce_gac on those constraints. All of the
       constraints of Model_1 MUST BE binary constraints (i.e.,
       constraints whose scope includes two and only two variables).
       
       This function outputs the GAC consistent domains after
       enforce_gac has been run. The output is a list with the same
       layout as the input list: a list of nine lists each
       representing a row of the board. However, now the numbers in
       the positions of the input list are to be replaced by LISTS
       which are the corresponding cell's pruned domain (current
       domain) AFTER gac has been performed.
       
       For example, if GAC failed to prune any values the output from
       the above input would result in an output would be: NOTE I HAVE
       PADDED OUT ALL OF THE LISTS WITH BLANKS SO THAT THEY LINE UP IN
       TO COLUMNS. Python would not output this list of list in this
       format.
       
       
       [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8]],
       [[1,2,3,4,5,6,7,8,9],[                7],[1,2,3,4,5,6,7,8,9],[                4],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3]],
       [[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9],[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6]],
       [[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                5],[                7],[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9]],
       [[                6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]]
       
       Of course, GAC would prune some variable domains so this would
       not be the outputted list.

    '''

#<<<your implemenation of model_1  below
    
    allVariables = buildVariables(initial_sudoku_board)
    allConstraints = buildConstraints(allVariables)
    result = enforce_gac(allConstraints)
    if (result == 'DWO'):
        print('DWO!')
        return
    displayResult(allVariables)
    

#>>>your implemenation of model_1 above



def buildVariables(initial_sudoku_board):
    # takes in a sudoku board, build all the variables
    # the naming of variables are corresponded to their order in board
    # returns the list of variables
    allVar = list()
    varName = 1
    
    for eachRow in initial_sudoku_board:
        variableRow = list()
        for eachNum in eachRow:
            if (eachNum != 0):
                newVar = Variable(varName, [eachNum])
                varName = varName + 1
            else:
                newVar = Variable(varName, [1, 2, 3, 4, 5, 6, 7, 8, 9])
                varName = varName + 1
            variableRow.append(newVar)
        allVar.append(variableRow)
    
    return allVar
            

    
def buildConstraints(allVariables):
    # function that build all constraints completely,
    # including adding the satisfied tuples
    # return the list of constraints
    allConstraints = list()
    
    add3x3Constraints(allVariables, allConstraints)
    addRowConstraints(allVariables, allConstraints)
    addColConstraints(allVariables, allConstraints)
    
    return allConstraints

def add3x3Constraints(allVariables, allConstraints):
    # build all the constraints in the 3x3 areas on the board
    startX = 0          # pointer to the x coordinate of the 3x3 area currently working on
    startY = 0          # pointer to the y coordinate
    relMask1 = 0        # use to translate variable's absolute position into relative position
    relMask2 = 0        # use to translate variable's absolute position into relative position
    
    while (startX <= 6 and startY <= 6):
        relMask1 = startX
        relMask2 = startY * 9
        i = 0
        test = 1
        while (i != 8):
            var1 = allVariables[startY + i/3][startX + i%3]
            m = 1
            # this if else is to deal with special cases where %9 returns 0 and 
            # can potentially mess up the building up
            if ((var1.name-relMask2)%9 == 0):
                var1_relPos = (var1.name-relMask2) - (var1.name-relMask2)/9*relMask1
            else:
                var1_relPos = ((var1.name-relMask2)/9)*3 + ((var1.name-relMask2)%9) - relMask1
            while( (var1_relPos + m) < 10 ):
                var2 = allVariables[startY + (i+m)/3][startX + (i+m)%3]
                conName = str(var1.name) + '&' + str(var2.name)
                newConstraint = Constraint(conName, [var1, var2])
                addTuples(newConstraint)
                allConstraints.append(newConstraint)
                test = test + 1
                m = m + 1
            i = i + 1
        startX = startX + 3
        if (startX == 9):
            startX = 0
            startY = startY + 3
        
def addRowConstraints(allVariables, allConstraints):
    # add all the constraints of each row of the board to the list of constraints
    startY = 0  
    
    while(startY != 9):
        eachRow = allVariables[startY]
        for eachVar1 in eachRow:
            for eachVar2 in eachRow:
                if(eachVar1 != eachVar2 and eachVar2.name > eachVar1.name):
                    conName = str(eachVar1.name) + '&' + str(eachVar2.name)
                    newConstraint = Constraint(conName, [eachVar1, eachVar2])
                    addTuples(newConstraint)
                    allConstraints.append(newConstraint)
        startY = startY + 1
        
def addColConstraints(allVariables, allConstraints):
    # add all the constraints of each column of the board to the list of constraints
    startX = 0
    
    while(startX != 9):
        startY = 0
        while(startY != 9):
            var1 = allVariables[startY][startX]
            var2_pos = startY + 1
            while(var2_pos != 9):
                var2 = allVariables[var2_pos][startX]
                conName = str(var1.name) + '&' + str(var2.name)
                newConstraint = Constraint(conName, [var1, var2])
                addTuples(newConstraint)
                allConstraints.append(newConstraint)
                var2_pos = var2_pos + 1
            startY = startY + 1
        startX = startX + 1


def displayResult(allVariables):
    # takes in a list of all variables of a board,
    # display the status of the board by showing the curdom of the variables
    displayList = list()
    for eachRow in allVariables:
        subList = list()
        for eachVar in eachRow:
            if(len(eachVar.curdom) != 1):
                subList.append(eachVar.curdom)
            else:
                subList.append(eachVar.curdom)
        displayList.append(subList)
        
    for eachsub in displayList:
        print(eachsub)

def addTuples2(newConstraint):
    # helper function for adding satisfied tuples
    var1 = newConstraint.scope[0]
    var2 = newConstraint.scope[1]
    satisfy_tups = list()
    
    for eachVal1 in var1.curdom:
        for eachVal2 in var2.curdom:
            if (eachVal1 != eachVal2):
                satisfy_tups.append((eachVal1, eachVal2))
    
    newConstraint.add_satisfying_tuples(satisfy_tups)

##############################

def sudoku_enforce_gac_model_2(initial_sudoku_board):
    '''This function takes the same input format (a list of 9 lists
    specifying the board, and generates the same format output as
    sudoku_enforce_gac_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables,
    invoke enforce_gac on those constraints, and then output the list of gac 
    consistent variable domains in the same format as for model_1.
    '''
     
    
#<<<your implemenation of model_2  below
    allVariables = buildVariables(initial_sudoku_board)
    allConstraints = buildConstraints_2(allVariables)
    result = enforce_gac(allConstraints)
    if (result == 'DWO'):
        print('DWO!')
        return
    displayResult(allVariables)
#>>>your implemenation of model_2 above

def buildConstraints_2(allVariables):
    # build all the constraints, first build 3x3 constraints,
    # then build row and column constraints
    # return the list of constraints
    allConstraints = list()
    loopIndex = 0
    varCur = 0
        
    while(loopIndex != 3):
        build3x3(allVariables, varCur, allConstraints)
        build3x3(allVariables, varCur + 3, allConstraints)
        build3x3(allVariables, varCur + 6, allConstraints)
        varCur = varCur + 27
        loopIndex= loopIndex + 1
        
    loopIndex = 0
    while(loopIndex != 9):
        buildrow(allVariables, loopIndex, allConstraints)
        buildcol(allVariables, loopIndex, allConstraints)
        loopIndex = loopIndex + 1
    
    return allConstraints
    
def build3x3(allVariables, varCur, allConstraints):
    # build one 3x3 constraint
    # takes in an index that identifies which 3x3 area this is
    conName = '3x3' + str(varCur)
    scopeList = list()
    
    curX = varCur%9
    curY = varCur/9
    loopIndex = 0
    while(loopIndex != 3):
        scopeList.append(allVariables[curY][curX])
        scopeList.append(allVariables[curY][curX + 1])
        scopeList.append(allVariables[curY][curX + 2])
        curY = curY + 1
        loopIndex = loopIndex + 1
            
    new_con = Constraint(conName, scopeList)
    addTuples9(new_con)
    allConstraints.append(new_con)

def buildrow(allVariables, index, allConstraints):
    # build one row constraint
    # takes in an index that identifies which row this is
    conName = 'row' + str(index)
    scopeList = allVariables[index]
    new_con = Constraint(conName, scopeList)
    addTuples9(new_con)
    allConstraints.append(new_con)
    
def buildcol(allVariables, index, allConstraints):
    # build one column constraint,
    # takes in an index that identifies which column this is
    conName = 'col' + str(index)
    scopeList = list()
    
    for eachRow in allVariables:
        scopeList.append(eachRow[index])
        
    new_con = Constraint(conName, scopeList)
    addTuples9(new_con)
    allConstraints.append(new_con)


def addTuples(con):
    # this function is to implement the add tuples of new constraints in the gac_enforce()
    # which will switch the add_tuple function according to which model the program is applying.
    # The reason for apply updateTuple9() directly instead of addTuples9() is to avoid the probability
    # of creating inconsistency by doing the unnecessary checking before adding tuples
    if(len(con.scope) == 2):
        addTuples2(con)
    elif (len(con.scope) == 9):
        updateTuples9(con)

def addTuples9(con):
    # Add the satisfied tuples to the constraint takes in
    # Apply a checking algorithm before adding satisfied tuples to avoid running on tuples
    # that are for sure does not satisfies the constraint
    # The algorithm is to find all the variables that only have one value in their curdom,
    # then by definition this value must be their value on this soduku board
    # therefore, the curdom of all other variables in the scope should remove this value from their curdom 
    
    possibleTuples = [[],[],[],[],[],[],[],[],[]]
    
    mustBe = list()
    for eachVar in con.scope:
        if(len(eachVar.curdom) == 1):
            mustBe.append(eachVar.curdom[0])
    
    
    for eachVar2 in con.scope:
        valueList = eachVar2.curdom
        if(len(valueList) != 1):
            index = 0
            limit = len(valueList)
            while(index != limit):
                eachValue = valueList[index]
                try:
                    result = mustBe.index(eachValue)
                except ValueError:
                    result = -1
                if (result != -1):
                    eachVar2.prune_value(eachValue)
                    index = index -1
                    limit = len(eachVar2.curdom)
                index = index + 1
    updateTuples9(con)
                                        

def updateTuples9(con):
    # function that does the actual adding satisfied tuples
    
    for ev1 in con.scope[0].curdom:
        for ev2 in con.scope[1].curdom:
            if (ev2 != ev1):
                for ev3 in con.scope[2].curdom:
                    if (ev3 != ev2 and ev3 != ev1):
                        for ev4 in con.scope[3].curdom:
                            if (ev4 != ev3 and ev4 != ev2 and ev4 != ev1):
                                for ev5 in con.scope[4].curdom:
                                    if (ev5 != ev4 and ev5 != ev3 and ev5 != ev2 and ev5 != ev1):
                                        for ev6 in con.scope[5].curdom:
                                            if (ev6 != ev5 and ev6 != ev4 and ev6 != ev3 and ev6 != ev2 and ev6 != ev1):
                                                for ev7 in con.scope[6].curdom:
                                                    if (ev7 != ev6 and ev7 != ev5 and ev7 != ev4 and ev7 != ev3 and ev7 != ev2 and ev7 != ev1):
                                                        for ev8 in con.scope[7].curdom:
                                                            if (ev8 != ev7 and ev8 != ev6 and ev8 != ev5 and ev8 != ev4 and ev8 != ev3 and ev8 != ev2 and ev8 != ev1):
                                                                for ev9 in con.scope[8].curdom:
                                                                    if (ev9 != ev8 and ev9 != ev7 and ev9 != ev6 and ev9 != ev5 and ev9 != ev4 and ev9 != ev3 and ev9 != ev2 and ev9 != ev1):
                                                                        con.add_satisfying_tuples([(ev1, ev2, ev3, ev4, ev5, ev6, ev7, ev8, ev9)])
                                        
                                        