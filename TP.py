####################
#Matrix Calculator Term Project
#Author: Nathan James
#Andrewid: nathanij
####################
from cmu_112_graphics import *
#CITATION downloaded from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
from TPclasses import *
import tkinter as tk
import copy, math

def appStarted(app):
    app.modes = ['selectorMode','vectorMode', 'matrixMode', 'basisMode']
    app.modeString = ['Start Menu','Vector Mode','Matrix Mode', 'Basis Mode']
    app.matrixOps = ['Multiply by Scalar','Matrix Addition',
        'Matrix Multiplication','Get Transpose','Get Inverse', 'Get Determinant']
    app.vectorOps = ['Dot Product','Cross Product','Calculate Projection','Get Projection Matrix']
    app.basisOps = ['Gram-Schmidt','Change of Basis','Eigenvalue']
    app.matrixOp = None
    app.vectorOp = None
    app.basisOp = None
    app.r1High = False
    app.c1High = False
    app.s1High = False
    app.r2High = False
    app.c2High = False
    app.r1Selected = False
    app.c1Selected = False
    app.c1 = 0
    app.r1 = 0
    app.c2 = 0
    app.r2 = 0
    app.m1selX = 0
    app.m1selY = 0
    app.v1 = 0
    app.v2 = 0
    app.v3 = 0
    app.v4 = 0
    app.v5 = 0
    app.basis = []
    app.solBasis = []
    app.basisM = ''
    app.basis1 = []
    app.basis2 = []
    resetSelector(app)

def selectorMode_mousePressed(app, event): #checks box clicks for selecting modes
    if event.x > app.width/2-100 and event.x < app.width/2+100:
        if event.y > app.height/4-50 and event.y < app.height/4+50:
           resetVectorMode(app) 
        elif event.y > app.height/2-50 and event.y < app.height/2+50:
            resetMatrixMode(app)
        elif event.y > 3*app.height/4-50 and event.y < 3*app.height/4+50:
            resetBasisMode(app)

def selectorMode_redrawAll(app,canvas):
    drawHeader(app, canvas)
    canvas.create_text(app.width/2,app.height/4, text = 'Vector Mode',
    font = 'Arial 18 bold')
    canvas.create_rectangle(app.width/2-100,(app.height/4)-50,app.width/2+100,
    (app.height/4)+50, width = 5)
    canvas.create_text(app.width/2,app.height/2, text = 'Matrix Mode',
    font = 'Arial 18 bold')
    canvas.create_rectangle(app.width/2-100,(app.height/2)-50,app.width/2+100,
    (app.height/2)+50, width = 5)
    canvas.create_text(app.width/2,3*app.height/4, text = 'Basis Mode',
    font = 'Arial 18 bold')
    canvas.create_rectangle(app.width/2-100,(3*app.height/4)-50,app.width/2+100,
    (3*app.height/4)+50, width = 5)

def vectorMode_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    if app.vectorOp == None:
        checkVectorMenu(app,event.x,event.y)

def vectorMode_keyPressed(app, event):
    pass

def vectorMode_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.vectorOp == None:
        for x in range(len(app.vectorOps)):
            if x % 3 == 0:
                canvas.create_rectangle(app.width/13,app.height/3+150*(x//3),4*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(5*app.width/26,app.height/3+150*(x//3)+50, text=app.vectorOps[x],
                font = 'Arial 20 bold')
            elif x % 3 == 1:
                canvas.create_rectangle(5*app.width/13,app.height/3+150*(x//3),8*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(app.width/2,app.height/3+150*(x//3)+50, text=app.vectorOps[x],
                font = 'Arial 20 bold')
            else:
                canvas.create_rectangle(9*app.width/13,app.height/3+150*(x//3),12*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(21*app.width/26,app.height/3+150*(x//3)+50, text=app.vectorOps[x],
                font = 'Arial 20 bold')

def resetVectorMode(app):
    app.title = "You're in Vector Mode!"
    app.message = "Select your operation."
    app.mode = 'vectorMode'
    app.vectorOp = None
    app.r1High = False
    app.c1High = False
    app.s1High = False
    app.r2High = False
    app.c2High = False
    app.c1 = 0
    app.r1 = 0
    app.c2 = 0
    app.r2 = 0
    app.prod = 0
    app.mX2 = 0
    app.mY2 = 0
    app.matrixOp = None
    app.basisOp = None
    app.m1selX = 0
    app.m1selY = 0

def checkVectorMenu(app, x, y):
    for num in range(len(app.vectorOps)):
            if num % 3 == 0:
                if x>app.width/13 and x<4*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.vectorOp = app.vectorOps[num]
            elif num % 3 == 1:
                if x>5*app.width/13 and x<8*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.vectorOp = app.vectorOps[num]
            else:
                if x>9*app.width/13 and x<12*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.vectorOp = app.vectorOps[num]
    if app.vectorOp == 'Dot Product':
        app.message = 'Enter your vector dimensions! (Must be equal)'
        app.mode = 'vector2'
    elif app.vectorOp == 'Cross Product':
        app.message = 'Vector dimension must be 3'
        app.mode = 'vector2'
    elif app.vectorOp == 'Calculate Projection':
        app.message = 'Calculates projection of Vector 1 onto Vector 2'
        app.mode = 'vector2'
    elif app.vectorOp == 'Get Projection Matrix':
        app.message = 'Enter your vector dimensions please!'
        app.mode = 'vector1'

def vector2_keyPressed(app, event):
    if app.c1High:
        if event.key.isnumeric():
            a = app.c1*10+int(event.key)
            if a < 11:
                app.c1 = a
        elif event.key == 'Delete':
            app.c1 //= 10
    elif app.r1High:
        if event.key.isnumeric():
            a = app.r1*10+int(event.key)
            if a < 11:
                app.r1 = a
        elif event.key == 'Delete':
            app.r1 //= 10

def vector2_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    checkdim1AnySelection(app,event.x,event.y)
    if checkDone(app,event.x,event.y) and app.r1 !=0 and app.c1 != 0:
        if app.vectorOp == 'Dot Product' and app.r1 == app.c1:
            app.mode = 'display2Vector'
            app.message = 'Enter the elements for your vectors!'
            app.m1 = createEmpty(1,app.r1)
            app.m2 = createEmpty(1,app.c1)
        elif app.vectorOp == 'Cross Product' and app.r1 ==3 and app.c1 == 3:
            app.mode = 'display2Vector'
            app.message = 'Enter the elements for your vectors!'
            app.m1 = createEmpty(1,app.r1)
            app.m2 = createEmpty(1,app.c1)
        elif app.vectorOp == 'Calculate Projection' and app.r1 == app.c1:
            app.mode = 'display2Vector'
            app.message = 'Enter the elements for your vectors!'
            app.m1 = createEmpty(1,app.r1)
            app.m2 = createEmpty(1,app.c1)

def vector2_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.c1High:
        cWidth = 10
        rWidth = 1
    elif app.r1High:
        rWidth = 10
        cWidth = 1
        sWidth = 1
    else:
        rWidth = 1
        cWidth = 1
    canvas.create_text(2*app.width/5+140,app.height/3, text='Columns (v1):', anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,app.height/3-18,2*app.width/5+200,app.height/3+22, width = rWidth)
    if app.r1 != 0:
        canvas.create_text(2*app.width/5+180,app.height/3+2, text = str(app.r1), font='Arial 24 bold')
    canvas.create_text(2*app.width/5+140,11*app.height/24, text = 'Columns (v2):',anchor = 'e', font = 'Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,11*app.height/24-18,2*app.width/5+200,11*app.height/24+22, width = cWidth)
    if app.c1 != 0:
        canvas.create_text(2*app.width/5+180,11*app.height/24+2, text = str(app.c1), font='Arial 24 bold')
    drawDone(app,canvas, 'Done') 

def vector1_keyPressed(app, event):
    if app.r1High:
        if event.key.isnumeric():
            a = app.r1*10+int(event.key)
            if a < 11:
                app.r1 = a
        elif event.key == 'Delete':
            app.r1 //= 10

def vector1_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    checkdim1AnySelection(app,event.x,event.y)
    if checkDone(app,event.x,event.y) and app.r1 !=0:
            app.mode = 'display1Matrix'
            app.message = 'Enter the elements for your vector!'
            app.m1 = createEmpty(1,app.r1)
            app.m2 = createEmpty(0,0)

def vector1_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.r1High:
        cWidth = 10
    else:
        cWidth = 1
    canvas.create_text(2*app.width/5+140,app.height/3, text='Columns:', anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,app.height/3-18,2*app.width/5+200,app.height/3+22, width = cWidth)
    if app.r1 != 0:
        canvas.create_text(2*app.width/5+180,app.height/3+2, text = str(app.r1), font='Arial 24 bold')
    drawDone(app,canvas, 'Done')

def display2Vector_keyPressed(app, event):
    if event.key == 'Left':
            selShift2(app,-1)
    elif event.key == 'Right' or event.key == 'Enter' or event.key == 'Tab':
            selShift2(app,1)
    else:
        if app.mX2 < app.m1.columns:
            if app.m1.elements[app.mY2][app.mX2] == '___':
                    entry = 0
            else:
                entry = app.m1.elements[app.mY2][app.mX2]
            if event.key == '-' and entry != 0:
                entry = 0-entry
                app.m1 = edit1Matrix(app.mY2,app.mX2,entry,app.m1)
            if event.key.isnumeric():
                if entry >= 0:
                        a = entry*10+int(event.key)
                else:
                        a = entry*10-int(event.key)
                if abs(a) < 100:
                        app.m1 = edit1Matrix(app.mY2,app.mX2,a,app.m1)
            elif event.key == 'Delete':
                a = entry//10
                if a == 0:
                    app.m1 = edit1Matrix(app.mY2,app.mX2,'___',app.m1)
                else:
                    app.m1 = edit1Matrix(app.mY2,app.mX2,a,app.m1)
        else:
                if app.m2.elements[app.mY2][app.mX2-app.m1.columns] == '___':
                    entry = 0
                else:
                    entry = app.m2.elements[app.mY2][app.mX2-app.m1.columns]
                if event.key == '-' and entry != 0:
                    entry = 0-entry
                    app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,entry,app.m2)
                if event.key.isnumeric():
                    if entry >= 0:
                        a = entry*10+int(event.key)
                    else:
                        a = entry*10-int(event.key)
                    if abs(a) < 100:
                        app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,a,app.m2)
                elif event.key == 'Delete':
                    a = entry//10
                    if a == 0:
                        app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,'___',app.m2)
                    else:
                        app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,a,app.m2)

def display2Vector_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    if app.vectorOp == 'Dot Product':
        check2MatrixSel(app,event.x,event.y,0.5,app.width/4,app.height/8)
        if checkDone(app,event.x,event.y):
            if app.m1.isFull() and app.m2.isFull():
                app.prod, app.mSteps, app.aSteps, app.tSteps = app.m1.dotProduct(app.m2)
                resetSolutionMode(app)
                app.mode = 'displaySolutionM' 
    elif app.vectorOp == 'Cross Product':
        check2MatrixSel(app,event.x,event.y,0.5,app.width/4,app.height/8)
        if checkDone(app,event.x,event.y):
            if app.m1.isFull() and app.m2.isFull():
                app.m1, app.mSteps, app.aSteps, app.tSteps = app.m1.cross(app.m2)
                resetSolutionMode(app)
                app.mode = 'displaySolutionM' 
    else:
        check2MatrixSel(app,event.x,event.y,0.5,app.width/4,app.height/8)
        if checkDone(app,event.x,event.y):
            if app.m1.isFull() and app.m2.isFull():
                app.m1, app.mSteps, app.aSteps, app.tSteps = app.m1.projection(app.m2)
                resetSolutionMode(app)
                app.mode = 'displaySolutionM'

def display2Vector_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    drawDone(app, canvas, app.vectorOp)
    draw2Matrix(app, canvas, app.m1,app.m2, 0.5, app.width/4, app.height/8)

def matrixMode_mousePressed(app,event):
    checkSidebar(app,event.x,event.y)
    if app.matrixOp == None:
        checkMatrixMenu(app,event.x,event.y)

def matrixMode_keyPressed(app, event):
    pass

def matrixMode_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.matrixOp == None:
        for x in range(len(app.matrixOps)):
            if x % 3 == 0:
                canvas.create_rectangle(app.width/13,app.height/3+150*(x//3),4*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(5*app.width/26,app.height/3+150*(x//3)+50, text=app.matrixOps[x],
                font = 'Arial 20 bold')
            elif x % 3 == 1:
                canvas.create_rectangle(5*app.width/13,app.height/3+150*(x//3),8*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(app.width/2,app.height/3+150*(x//3)+50, text=app.matrixOps[x],
                font = 'Arial 20 bold')
            else:
                canvas.create_rectangle(9*app.width/13,app.height/3+150*(x//3),12*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(21*app.width/26,app.height/3+150*(x//3)+50, text=app.matrixOps[x],
                font = 'Arial 20 bold')

def checkMatrixMenu(app,x,y):#checks if an operation is selected
    for num in range(len(app.matrixOps)):
            if num % 3 == 0:
                if x>app.width/13 and x<4*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.matrixOp = app.matrixOps[num]
            elif num % 3 == 1:
                if x>5*app.width/13 and x<8*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.matrixOp = app.matrixOps[num]
            else:
                if x>9*app.width/13 and x<12*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.matrixOp = app.matrixOps[num]
    if dim1Any(app.matrixOp):
        app.message = 'Enter your matrix dimensions please!'
        app.mode = 'selDim1Any'
    if dim1Square(app.matrixOp):
        app.message = 'Enter your matrix dimensions please! (Must be square!)'
        app.mode = 'selDim1Square'
    if app.matrixOp == 'Matrix Multiplication':
        app.message = 'Enter your matrix dimensions please! (Columns of first must equal rows of second!)'
        app.mode = 'matrixMult'

def resetMatrixMode(app):
    app.title = "You're in Matrix Mode!"
    app.message = "Select your operation."
    app.mode = 'matrixMode'
    app.matrixOp = None
    app.r1High = False
    app.c1High = False
    app.s1High = False
    app.r2High = False
    app.c2High = False
    app.r1Selected = False
    app.c1Selected = False
    app.c1 = 0
    app.r1 = 0
    app.c2 = 0
    app.r2 = 0
    app.m1selX = 0
    app.m1selY = 0
    app.scalar = 0
    app.mX2 = 0
    app.mY2 = 0
    app.det = 0
    app.vectorOp = None
    app.basisOp = None
 
def selDim1Any_keyPressed(app, event):
    if app.c1High:
        if event.key.isnumeric():
            a = app.c1*10+int(event.key)
            if a < 11:
                app.c1 = a
        elif event.key == 'Delete':
            app.c1 //= 10
    elif app.r1High:
        if event.key.isnumeric():
            a = app.r1*10+int(event.key)
            if a < 11:
                app.r1 = a
        elif event.key == 'Delete':
            app.r1 //= 10
    elif app.s1High:
        if event.key == '-':
            app.scalar = -app.scalar
        if event.key.isnumeric():
            if app.scalar >= 0:
                a = app.scalar*10+int(event.key)
            else:
                a = app.scalar*10-int(event.key)
            if abs(a) < 100:
                app.scalar = a
        elif event.key == 'Delete':
            app.scalar //= 10

def selDim1Any_mousePressed(app,event):
    checkSidebar(app,event.x,event.y)
    checkdim1AnySelection(app,event.x,event.y)
    if checkDone(app,event.x,event.y) and app.r1 !=0 and app.c1 != 0:
        if app.matrixOp == 'Multiply by Scalar' and app.scalar == 0:
            pass
        else:
            app.mode = 'display1Matrix'
            app.message = 'Enter the elements for your matrix(matrices)!'
            app.m1 = createEmpty(app.r1,app.c1)
            app.m2 = createEmpty(app.r1,app.c1)

def selDim1Any_redrawAll(app,canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.c1High:
        cWidth = 10
        rWidth = 1
        sWidth = 1
    elif app.r1High:
        rWidth = 10
        cWidth = 1
        sWidth = 1
    elif app.s1High:
        sWidth = 10
        cWidth = 1
        rWidth = 1
    else:
        rWidth = 1
        cWidth = 1
        sWidth = 1
    canvas.create_text(2*app.width/5+140,app.height/3, text='Rows:', anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,app.height/3-18,2*app.width/5+200,app.height/3+22, width = rWidth)
    if app.r1 != 0:
        canvas.create_text(2*app.width/5+180,app.height/3+2, text = str(app.r1), font='Arial 24 bold')
    canvas.create_text(2*app.width/5+140,11*app.height/24, text = 'Columns:',anchor = 'e', font = 'Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,11*app.height/24-18,2*app.width/5+200,11*app.height/24+22, width = cWidth)
    if app.c1 != 0:
        canvas.create_text(2*app.width/5+180,11*app.height/24+2, text = str(app.c1), font='Arial 24 bold')
    if app.matrixOp == 'Multiply by Scalar':
        canvas.create_text(2*app.width/5+140,7*app.height/12, text = 'Scalar:',anchor = 'e', font = 'Arial 24 bold')
        canvas.create_rectangle(2*app.width/5+160,7*app.height/12-18,2*app.width/5+200,7*app.height/12+22, width = sWidth)
        if app.scalar != 0:
            canvas.create_text(2*app.width/5+180,7*app.height/12+2, text = str(app.scalar), font='Arial 24 bold')
    drawDone(app,canvas, 'Done')

def checkdim1AnySelection(app,x,y): #checks for dimension selection
    if x > (2*app.width/5)+160 and x < (2*app.width/5)+200:
        if y > app.height/3-18 and y < app.height/3+22:
            if not app.r1High:
                app.c1High = False
                app.r1High = True
                app.s1High = False
            else:
                app.r1High = False
        elif y > 11*app.height/24-18 and y < 11*app.height/24+22:
            if not app.c1High:
                app.c1High = True
                app.r1High = False
                app.s1High = False
            else:
                app.c1High = False
        elif y > 7*app.height/12-18 and y < 7*app.height/12+22:
            if not app.s1High:
                app.c1High = False
                app.r1High = False
                app.s1High = True
            else:
                app.s1High = False

def selDim1Square_keyPressed(app, event):
    if app.c1High:
        if event.key.isnumeric():
            if app.c1 >= 0:
                a = app.c1*10+int(event.key)
            else:
                a = app.c1*10-int(event.key)
            if abs(a) < 10:
                app.c1 = a
        elif event.key == 'Delete':
            app.c1 //= 10
    elif app.r1High:
        if event.key.isnumeric():
            if app.r1 >= 0:
                a = app.r1*10+int(event.key)
            else:
                a = app.r1*10-int(event.key)
            if abs(a) < 10:
                app.r1 = a
        elif event.key == 'Delete':
            app.r1 //= 10

def selDim1Square_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    checkDim1SquareSelection(app, event.x, event.y)
    if checkDone(app, event.x, event.y) and app.r1 == app.c1 and app.r1:
        if app.basisOp == 'Eigenvalue':
            if app.r1 == 2 or app.r1 == 3:
                app.mode = 'display1Matrix'
                app.message = 'Enter the elements for your matrix!'
                app.m1 = createEmpty(app.r1,app.c1)
        else:
            app.mode = 'display1Matrix'
            app.message = 'Enter the elements for your matrix!'
            app.m1 = createEmpty(app.r1,app.c1)

def selDim1Square_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.r1High:
        r1Width = 10
        c1Width = 1
        r2Width = 1
        c2Width = 1
    elif app.c1High:
        r1Width = 1
        c1Width = 10
        r2Width = 1
        c2Width = 1
    else:
        r1Width = 1
        c1Width = 1
        r2Width = 1
        c2Width = 1
    canvas.create_text(2*app.width/5+140,app.height/3, text='Rows:', anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,app.height/3-18,2*app.width/5+200,app.height/3+22, width = r1Width)
    if app.r1 != 0:
        canvas.create_text(2*app.width/5+180,app.height/3+2, text = str(app.r1), font='Arial 24 bold')
    canvas.create_text(2*app.width/5+140,11*app.height/24, text = 'Columns:',anchor = 'e', font = 'Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,11*app.height/24-18,2*app.width/5+200,11*app.height/24+22, width = c1Width)
    if app.c1 != 0:
        canvas.create_text(2*app.width/5+180,11*app.height/24+2, text = str(app.c1), font='Arial 24 bold')
    drawDone(app,canvas, 'Done')

def checkDim1SquareSelection(app,x,y):
    if x > (2*app.width/5)+160 and x < (2*app.width/5)+200:
        if y > app.height/3-18 and y < app.height/3+22:
            if not app.r1High:
                app.r1High = True
                app.c1High = False
                app.r2High = False
                app.c2High = False
            else:
                app.r1High = False
        elif y > 11*app.height/24-18 and y < 11*app.height/24+22:
            if not app.c1High:
                app.r1High = False
                app.c1High = True
                app.r2High = False
                app.c2High = False
            else:
                app.c1High = False

def matrixMult_keyPressed(app, event):
    if app.c1High:
        if event.key.isnumeric():
            if app.c1 >= 0:
                a = app.c1*10+int(event.key)
            else:
                a = app.c1*10-int(event.key)
            if abs(a) < 10:
                app.c1 = a
        elif event.key == 'Delete':
            app.c1 //= 10
    elif app.c2High:
        if event.key.isnumeric():
            if app.c2 >= 0:
                a = app.c2*10+int(event.key)
            else:
                a = app.c2*10-int(event.key)
            if abs(a) < 10:
                app.c2 = a
        elif event.key == 'Delete':
            app.c2 //= 10
    elif app.r1High:
        if event.key.isnumeric():
            if app.r1 >= 0:
                a = app.r1*10+int(event.key)
            else:
                a = app.r1*10-int(event.key)
            if abs(a) < 10:
                app.r1 = a
        elif event.key == 'Delete':
            app.r1 //= 10
    elif app.r2High:
        if event.key.isnumeric():
            if app.r2 >= 0:
                a = app.r2*10+int(event.key)
            else:
                a = app.r2*10-int(event.key)
            if abs(a) < 10:
                app.r2 = a
        elif event.key == 'Delete':
            app.r2 //= 10

def matrixMult_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    checkMatrixMultSel(app, event.x, event.y)
    if checkDone(app, event.x, event.y) and app.c1 == app.r2 and app.c1 != 0:
        app.mode = 'display1Matrix'
        app.message = 'Enter the elements for your matrices!'
        app.m1 = createEmpty(app.r1,app.c1)
        app.m2 = createEmpty(app.r2,app.c2)
    
def matrixMult_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.r1High:
        r1Width = 10
        c1Width = 1
        r2Width = 1
        c2Width = 1
    elif app.c1High:
        r1Width = 1
        c1Width = 10
        r2Width = 1
        c2Width = 1
    elif app.r2High:
        r1Width = 1
        c1Width = 1
        r2Width = 10
        c2Width = 1
    elif app.c2High:
        r1Width = 1
        c1Width = 1
        r2Width = 1
        c2Width = 10
    else:
        r1Width = 1
        c1Width = 1
        r2Width = 1
        c2Width = 1
    canvas.create_text(2*app.width/5+140,app.height/3, text='Rows:', anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,app.height/3-18,2*app.width/5+200,app.height/3+22, width = r1Width)
    if app.r1 != 0:
        canvas.create_text(2*app.width/5+180,app.height/3+2, text = str(app.r1), font='Arial 24 bold')
    canvas.create_text(2*app.width/5+140,11*app.height/24, text = 'Columns:',anchor = 'e', font = 'Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,11*app.height/24-18,2*app.width/5+200,11*app.height/24+22, width = c1Width)
    if app.c1 != 0:
        canvas.create_text(2*app.width/5+180,11*app.height/24+2, text = str(app.c1), font='Arial 24 bold')
    canvas.create_text(2*app.width/5+140,7*app.height/12, text='Rows (M2):', anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,7*app.height/12-18,2*app.width/5+200,7*app.height/12+22, width = r2Width)
    if app.r2 != 0:
        canvas.create_text(2*app.width/5+180,7*app.height/12+2, text = str(app.r2), font='Arial 24 bold')
    canvas.create_text(2*app.width/5+140,17*app.height/24, text='Columns (M2):', anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,17*app.height/24-18,2*app.width/5+200,17*app.height/24+22, width = c2Width)
    if app.c2 != 0:
        canvas.create_text(2*app.width/5+180,17*app.height/24+2, text = str(app.c2), font='Arial 24 bold')
    drawDone(app,canvas, 'Done')

def checkMatrixMultSel(app, x, y):
    if x > (2*app.width/5)+160 and x < (2*app.width/5)+200:
        if y > app.height/3-18 and y < app.height/3+22:
            if not app.r1High:
                app.r1High = True
                app.c1High = False
                app.r2High = False
                app.c2High = False
            else:
                app.r1High = False
        elif y > 11*app.height/24-18 and y < 11*app.height/24+22:
            if not app.c1High:
                app.r1High = False
                app.c1High = True
                app.r2High = False
                app.c2High = False
            else:
                app.c1High = False
        elif y > 7*app.height/12-18 and y < 7*app.height/12+22:
            if not app.r2High:
                app.r1High = False
                app.c1High = False
                app.r2High = True
                app.c2High = False
            else:
                app.r2High = False
        elif y > 17*app.height/24-18 and y < 17*app.height/24+22:
            if not app.c2High:
                app.r1High = False
                app.c1High = False
                app.r2High = False
                app.c2High = True
            else:
                app.c2High = False

def display1Matrix_keyPressed(app, event):
    if app.matrixOp == 'Matrix Addition' or app.matrixOp == 'Matrix Multiplication':
        if event.key == 'Left':
            selShift2(app,-1)
        elif event.key == 'Right' or event.key == 'Enter' or event.key == 'Tab':
            selShift2(app,1)
        else:
            if app.mX2 < app.m1.columns:
                if app.m1.elements[app.mY2][app.mX2] == '___':
                    entry = 0
                else:
                    entry = app.m1.elements[app.mY2][app.mX2]
                if event.key == '-' and entry != 0:
                    entry = 0-entry
                    app.m1 = edit1Matrix(app.mY2,app.mX2,entry,app.m1)
                if event.key.isnumeric():
                    if entry >= 0:
                        a = entry*10+int(event.key)
                    else:
                        a = entry*10-int(event.key)
                    if abs(a) < 100:
                        app.m1 = edit1Matrix(app.mY2,app.mX2,a,app.m1)
                elif event.key == 'Delete':
                    a = entry//10
                    if a == 0:
                        app.m1 = edit1Matrix(app.mY2,app.mX2,'___',app.m1)
                    else:
                        app.m1 = edit1Matrix(app.mY2,app.mX2,a,app.m1)
            else:
                if app.m2.elements[app.mY2][app.mX2-app.m1.columns] == '___':
                    entry = 0
                else:
                    entry = app.m2.elements[app.mY2][app.mX2-app.m1.columns]
                if event.key == '-' and entry != 0:
                    entry = 0-entry
                    app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,entry,app.m2)
                if event.key.isnumeric():
                    if entry >= 0:
                        a = entry*10+int(event.key)
                    else:
                        a = entry*10-int(event.key)
                    if abs(a) < 100:
                        app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,a,app.m2)
                elif event.key == 'Delete':
                    a = entry//10
                    if a == 0:
                        app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,'___',app.m2)
                    else:
                        app.m2 = edit1Matrix(app.mY2,app.mX2-app.m1.columns,a,app.m2)
    else:
        if event.key == 'Left':
            selShift(app,-1)
        elif event.key == 'Right' or event.key == 'Enter' or event.key == 'Tab':
            selShift(app,1)
        else:
            if app.m1.elements[app.m1selY][app.m1selX] == '___':
                entry = 0
            else:
                entry = app.m1.elements[app.m1selY][app.m1selX]
            if event.key == '-' and entry != 0:
                entry = 0-entry
                app.m1 = edit1Matrix(app.m1selY,app.m1selX,entry,app.m1)
            if event.key.isnumeric():
                if entry >= 0:
                    a = entry*10+int(event.key)
                else:
                    a = entry*10-int(event.key)
                if abs(a) < 100:
                    app.m1 = edit1Matrix(app.m1selY,app.m1selX,a,app.m1)
            elif event.key == 'Delete':
                a = entry//10
                if a == 0:
                    app.m1 = edit1Matrix(app.m1selY,app.m1selX,'___',app.m1)
                else:
                    app.m1 = edit1Matrix(app.m1selY,app.m1selX,a,app.m1)

def display1Matrix_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    if app.matrixOp == 'Matrix Addition':
        check2MatrixSel(app,event.x,event.y,0.5,app.width/4,app.height/8)
        if checkDone(app,event.x,event.y):
            if app.m1.isFull() and app.m2.isFull():
                app.m1, app.mSteps, app.aSteps, app.tSteps = app.m1.addMatrix(app.m2)
                resetSolutionMode(app)
                app.mode = 'displaySolutionM' 
    elif app.matrixOp == 'Matrix Multiplication':
        check2MatrixSel(app,event.x,event.y,0.5,app.width/4,app.height/8)
        if checkDone(app,event.x,event.y):
            if app.m1.isFull() and app.m2.isFull():
                app.m1 = app.m1.multiplyMatrix(app.m2)
                resetSolutionMode(app)
                app.mode = 'displaySolutionM'
    else:
        checkElSelector(app,event.x,event.y)
        if checkDone(app,event.x,event.y):
            if app.m1.isFull() == True:
                if app.matrixOp == 'Get Transpose':
                    app.m1, app.mSteps, app.aSteps, app.tSteps = app.m1.transpose()
                elif app.matrixOp == 'Multiply by Scalar':
                    app.m1, app.mSteps, app.aSteps, app.tSteps= app.m1.scalarMult(app.scalar)
                elif app.matrixOp == 'Get Inverse':
                    app.det, b, c, d = app.m1.determinant()
                    if app.det != 0:
                        app.m1, app.aSteps, app.mSteps, app.tSteps = app.m1.inverse()
                elif app.matrixOp == 'Get Determinant':
                    app.det, app.mSteps, app.aSteps, app.tSteps = app.m1.determinant()
                elif app.vectorOp == 'Get Projection Matrix':
                    app.m1, app.aSteps, app.mSteps, app.tSteps = app.m1.projectionMatrix()
                elif app.basisOp == 'Eigenvalue':
                    app.poly = app.m1.charPoly()
                    app.values = app.m1.eigen()
                resetSolutionMode(app)
                app.mode = 'displaySolutionM'              
          
def display1Matrix_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.matrixOp != None:
        drawDone(app, canvas, app.matrixOp)
    elif app.vectorOp != None:
        drawDone(app, canvas, app.vectorOp)
    else:
        drawDone(app, canvas, app.basisOp)
    if app.matrixOp == 'Matrix Addition' or app.matrixOp == 'Matrix Multiplication':
        draw2Matrix(app, canvas, app.m1,app.m2, 0.5, app.width/4, app.height/8)
    else:
        draw1Matrix(app, canvas, app.m1, 1, 0, 0)
        
def displaySolutionM_mousePressed(app,event):
    checkSidebar(app,event.x,event.y)
    if checkDone(app, event.x,event.y) and (app.matrixOp != None or app.vectorOp != None or app.basisOp == 'Gram-Schmidt' or app.basisOp == 'Change of Basis'):
        app.cAStep = app.aSteps[0]
        app.aSteps = app.aSteps[1:]
        app.cMStep = app.mSteps[0]
        app.mSteps = app.mSteps[1:]
        app.message = app.tSteps[0]
        app.tSteps = app.tSteps[1:]
        app.mode = 'step'


def displaySolutionM_redrawAll(app,canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    drawDone(app, canvas, 'Show Steps')
    if app.matrixOp == 'Get Inverse' and app.det == 0:
        canvas.create_text(app.width/2,app.height/2, text = 'Matrix is not invertible! (Determinant = 0)', font = 'Arial 24 bold')
    elif app.matrixOp == 'Get Determinant':
        canvas.create_text(app.width/2,app.height/2, text = f'The determinant is {app.det}!', font = 'Arial 24 bold')
    elif app.vectorOp == 'Dot Product':
        canvas.create_text(app.width/2,app.height/2, text = f'The dot product is {app.prod}!', font = 'Arial 24 bold')
    elif app.basisOp == 'Eigenvalue':
        if app.m1.rows == 2:
            canvas.create_text(app.width/2, 2*app.height/5, text = f'The characteristic polynomial is 0 = ({app.poly[0]})*x^2+({app.poly[1]})*x+({app.poly[2]})',font = 'Arial 24 bold' )
        elif app.m1.rows == 3:
            canvas.create_text(app.width/2, 2*app.height/5, text = f'The characteristic polynomial is 0 = ({app.poly[0]})*x^3+({app.poly[1]})*x^2+({app.poly[2]})*x+({app.poly[3]})',font = 'Arial 24 bold' )
        canvas.create_text(app.width/2, 3*app.height/5, text = f'The eigenvalue(s) are {app.values}',font = 'Arial 24 bold' )
    elif app.basisOp == 'Gram-Schmidt':
        shift = 0
        for vector in app.solBasis:
            draw1Matrix(app, canvas, vector, 0.5, 0, shift)
            shift += app.height/7
    else:
        draw1Matrix(app, canvas, app.m1, 1, 0, 0)

def step_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.cMStep is app.cAStep:
        draw1Matrix(app, canvas, app.cMStep, 1,0,0)
    else:
        draw2Matrix(app, canvas, app.cMStep,app.cAStep, 0.5, app.width/4, app.height/8)
    if len(app.aSteps) != 0:
        drawDone(app, canvas, 'Take Step')

def step_mousePressed(app, event):
    checkSidebar(app, event.x, event.y)
    if len(app.aSteps) != 0:
        if checkDone(app, event.x,event.y):
            app.cAStep = app.aSteps[0]
            app.aSteps = app.aSteps[1:]
            app.cMStep = app.mSteps[0]
            app.mSteps = app.mSteps[1:]
            app.message = app.tSteps[0]
            app.tSteps = app.tSteps[1:]

#basis mode goes here
def resetBasisMode(app):
    app.mode = 'basisMode'
    app.title = "You're in Basis Mode"
    app.message = 'Select your function'
    app.v1 = 0
    app.v2 = 0
    app.v3 = 0
    app.v4 = 0
    app.v5 = 0
    app.basisOp = None
    app.matrixOp = None
    app.vectorOp = None
    app.c1High = False
    app.r1High = False
    app.r1 = 0
    app.c1 = 0
    app.basisM = ''
    app.basis = []
    app.solBasis = []
    app.basis1 = []
    app.basis2 = []

def basisMode_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.basisOp == None:
        for x in range(len(app.basisOps)):
            if x % 3 == 0:
                canvas.create_rectangle(app.width/13,app.height/3+150*(x//3),4*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(5*app.width/26,app.height/3+150*(x//3)+50, text=app.basisOps[x],
                font = 'Arial 20 bold')
            elif x % 3 == 1:
                canvas.create_rectangle(5*app.width/13,app.height/3+150*(x//3),8*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(app.width/2,app.height/3+150*(x//3)+50, text=app.basisOps[x],
                font = 'Arial 20 bold')
            else:
                canvas.create_rectangle(9*app.width/13,app.height/3+150*(x//3),12*app.width/13,
                app.height/3+150*(x//3)+100, width = 5)
                canvas.create_text(21*app.width/26,app.height/3+150*(x//3)+50, text=app.basisOps[x],
                font = 'Arial 20 bold')

def basisMode_mousePressed(app, event):
    checkSidebar(app, event.x, event.y)
    checkBasisMenu(app, event.x, event.y)

def checkBasisMenu(app, x, y):
    for num in range(len(app.basisOps)):
            if num % 3 == 0:
                if x>app.width/13 and x<4*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.basisOp = app.basisOps[num]
            elif num % 3 == 1:
                if x>5*app.width/13 and x<8*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.basisOp = app.basisOps[num]
            else:
                if x>9*app.width/13 and x<12*app.width/13:
                    if y>150*(num//3)+app.height/3 and y<100+150*(num//3)+app.height/3:
                        app.basisOp = app.basisOps[num]
    if app.basisOp == 'Gram-Schmidt':
        app.message = 'Enter the number of vectors in your basis (2-5)'
        app.mode = 'selectDimBasis'
        app.basisM = 'Vectors:'
    elif app.basisOp == 'Change of Basis':
        app.message = 'Enter the number of vectors in your basis (2-3)'
        app.mode = 'selectDimBasis'
        app.basisM = 'Vectors:'
    elif app.basisOp == 'Eigenvalue':
        app.message = 'Enter your matrix dimensions please! (Must be square!(2-3))'
        app.mode = 'selDim1Square'

def selectDimBasis_mousePressed(app, event):
    checkSidebar(app,event.x,event.y)
    checkdim1AnySelection(app,event.x,event.y)
    if checkDone(app,event.x,event.y) and app.r1 > 0 and app.r1 < 6:
            if app.message != 'Enter the dimension for your basis vectors!':
                app.message = 'Enter the dimension for your basis vectors!'
                app.basisM = 'Columns:'
                app.numVectors = app.r1
                app.r1 = 0
            else:
                if app.r1 > 0 and app.r1 < 6:
                    app.vectorL = app.r1
                    app.count = 0
                    app.v1 = createEmpty(1,app.vectorL)
                    app.v2 = createEmpty(1,app.vectorL)
                    app.v3 = createEmpty(1,app.vectorL)
                    app.v4 = createEmpty(1,app.vectorL)
                    app.v5 = createEmpty(1,app.vectorL)
                    app.m1 = app.v1
                    app.mode = 'enterBasis'

def selectDimBasis_keyPressed(app, event):
    if app.r1High:
        if event.key.isnumeric():
            a = app.r1*10+int(event.key)
            if a < 11:
                app.r1 = a
        elif event.key == 'Delete':
            app.r1 //= 10

def selectDimBasis_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    if app.r1High:
        cWidth = 10
    else:
        cWidth = 1
    canvas.create_text(2*app.width/5+140,app.height/3, text=app.basisM, anchor = 'e', font='Arial 24 bold')
    canvas.create_rectangle(2*app.width/5+160,app.height/3-18,2*app.width/5+200,app.height/3+22, width = cWidth)
    if app.r1 != 0:
        canvas.create_text(2*app.width/5+180,app.height/3+2, text = str(app.r1), font='Arial 24 bold')
    drawDone(app,canvas, 'Done')

def enterBasis_mousePressed(app, event):
    checkSidebar(app, event.x, event.y)
    checkElSelector(app,event.x,event.y)
    if checkDone(app,event.x,event.y):
        if app.m1.isFull() == True:
            if app.basisOp == 'Gram-Schmidt':
                if app.count == 0:
                    app.v1 = app.m1
                    if app.numVectors == 1:
                        app.basis = [app.v1]
                        app.solBasis, app.mSteps, app.aSteps, app.tSteps = gramSchmidt(app.basis)
                        resetSolutionMode(app)
                        app.mode = 'displaySolutionM'
                    else:
                        app.m1 = app.v2
                        app.count += 1
                elif app.count == 1:
                    app.v2 = app.m1
                    if app.numVectors == 2:
                        app.basis = [app.v1,app.v2]
                        app.solBasis, app.mSteps, app.aSteps, app.tSteps = gramSchmidt(app.basis)
                        resetSolutionMode(app)
                        app.mode = 'displaySolutionM'
                    else:
                        app.m1 = app.v3
                        app.count += 1
                elif app.count == 2:
                    app.v3 = app.m1
                    if app.numVectors == 3:
                        app.basis = [app.v1,app.v2,app.v3]
                        app.solBasis, app.mSteps, app.aSteps, app.tSteps = gramSchmidt(app.basis)
                        resetSolutionMode(app)
                        app.mode = 'displaySolutionM'
                    else:
                        app.m1 = app.v4
                        app.count += 1
                elif app.count == 3:
                    app.v4 = app.m1
                    if app.numVectors == 4:
                        app.basis = [app.v1,app.v2,app.v3,app.v4]
                        app.solBasis, app.mSteps, app.aSteps, app.tSteps = gramSchmidt(app.basis)
                        resetSolutionMode(app)
                        app.mode = 'displaySolutionM'
                    else:
                        app.m1 = app.v5
                        app.count += 1
                else:
                    app.v5 = app.m1
                    app.basis = [app.v1,app.v2,app.v3,app.v4,app.v5]
                    app.solBasis, app.mSteps, app.aSteps, app.tSteps = gramSchmidt(app.basis)
                    resetSolutionMode(app)
                    app.mode = 'displaySolutionM'
            elif app.basisOp == 'Change of Basis':
                if len(app.basis1) != app.numVectors:
                    app.basis1.append(app.m1)
                    app.m1 = createEmpty(1,app.vectorL)
                    app.count += 1
                elif len(app.basis2) != app.numVectors:
                    app.basis2.append(app.m1)
                    app.m1 = createEmpty(1,app.vectorL)
                    app.count += 1
                    if len(app.basis2) == app.numVectors:
                        app.m1, app.mSteps, app.aSteps, app.tSteps = changeBasis(app.basis1,app.basis2)
                        resetSolutionMode(app)
                        app.message = 'Change of basis matrix!'
                        app.mode = 'displaySolutionM' 

                
def enterBasis_keyPressed(app, event):
    if event.key == 'Left':
            selShift(app,-1)
    elif event.key == 'Right' or event.key == 'Enter' or event.key == 'Tab':
            selShift(app,1)
    else:
            if app.m1.elements[app.m1selY][app.m1selX] == '___':
                entry = 0
            else:
                entry = app.m1.elements[app.m1selY][app.m1selX]
            if event.key == '-' and entry != 0:
                entry = 0-entry
                app.m1 = edit1Matrix(app.m1selY,app.m1selX,entry,app.m1)
            if event.key.isnumeric():
                if entry >= 0:
                    a = entry*10+int(event.key)
                else:
                    a = entry*10-int(event.key)
                if abs(a) < 100:
                    app.m1 = edit1Matrix(app.m1selY,app.m1selX,a,app.m1)
            elif event.key == 'Delete':
                a = entry//10
                if a == 0:
                    app.m1 = edit1Matrix(app.m1selY,app.m1selX,'___',app.m1)
                else:
                    app.m1 = edit1Matrix(app.m1selY,app.m1selX,a,app.m1)

def enterBasis_redrawAll(app, canvas):
    drawHeader(app, canvas)
    drawSidebar(app, canvas)
    drawDone(app, canvas,f'Vector {app.count+1}')
    draw1Matrix(app, canvas, app.m1, 1, 0, 0)

def resetSolutionMode(app):
    app.message = 'Solution!'
    app.m1selX = -1
    app.m1selY = -1
    app.mX2 = -1
    app.mY2 = -1
       
def check2MatrixSel(app,x,y,scale, rShift,dShift):
    #if app.m1.rows == app.m2.rows:
        size1 = (app.height/2)/(max(app.m1.rows,app.m1.columns)-1) * scale
        for row in range(app.m1.rows):
                for col in range(app.m1.columns):
                    if app.m1.columns % 2 == 1:
                        sideShift1 = size1*(col-(app.m1.columns//2))
                    else:
                        sideShift1 = size1*(col-(app.m1.columns//2)+0.5)
                    if x > (app.width/2)+(sideShift1)-20-rShift and x < (app.width/2)+(sideShift1)+20-rShift:
                        if y > (app.height/4)+(row*size1)-20+dShift and y < (app.height/4)+(row*size1)+20+dShift:
                            app.mX2 = col
                            app.mY2 = row
        size2 = (app.height/2)/(max(app.m2.rows,app.m2.columns)-1) * scale
        for row in range(app.m2.rows):
            for col in range(app.m2.columns):
                if app.m2.columns % 2 == 1:
                    sideShift2 = size2*(col-(app.m2.columns//2))
                else:
                    sideShift2 = size2*(col-(app.m2.columns//2)+0.5)
                if x > (app.width/2)+(sideShift2)-20+rShift and x < (app.width/2)+(sideShift2)+20+rShift:
                    if y > (app.height/4)+(row*size2)-20+dShift and y < (app.height/4)+(row*size2)+20+dShift:
                        app.mX2 = col+app.m1.columns
                        app.mY2 = row

def resetSelector(app):
    app.title = "You're in Selector Mode!"
    app.message = "Which mode would you like?"
    app.mode = 'selectorMode'

def drawSidebar(app, canvas):
    for x in range(len(app.modes)):
        canvas.create_rectangle(app.width-204,4+50*x,app.width-4,50*x+54)
        canvas.create_text(app.width-102,50*x+29, text=app.modeString[x], font = 'Arial 16')

def drawHeader(app, canvas):
    canvas.create_text(app.width/2,app.height/20, text = app.title, 
    font = 'Arial 26 bold')
    canvas.create_text(app.width/2,app.height/10, text = app.message,
    font = 'Arial 18')

def dim1Any(n): #one matrix operation with any input
    l = {'Multiply by Scalar','Matrix Addition','Get Transpose'}
    if n in l:
        return True
    else:
        return False

def dim1Square(n): #one matrix operations that require a square input
    l = {'Get Inverse','Get Determinant'}
    if n in l:
        return True
    else:
        return False

def drawDone(app, canvas, input): #draws done button
    canvas.create_text(app.width/2,29.5*app.height/32, text = input, font = 'Arial 24 bold')
    canvas.create_rectangle(2*app.width/5,7*app.height/8,3*app.width/5,31*app.height/32, width = 5)

def checkDone(app,x,y): #checks if done button is pressed
    if x > 2*app.width/5 and x < 3*app.width/5:
        if y > 27*app.height/32 and y < 31*app.height/32:
            return True
    return False

def draw1Matrix(app, canvas, m, scale, rShift, dShift): #draws a matrix (can scale)
        size = (app.height/2)/(max(max(m.rows,m.columns)-1,1)) * scale
        for row in range(m.rows):
            for col in range(m.columns):
                if m.columns % 2 == 1:
                    sideShift = size*(col-(m.columns//2))
                else:
                    sideShift = size*(col-(m.columns//2)+0.5)
                canvas.create_text((app.width/2)+(sideShift)+rShift,(app.height/4)+(row*size)+dShift,text=m.elements[row][col],
                font = 'Arial 18 bold')
                if col == app.m1selX and row == app.m1selY:
                    canvas.create_rectangle((app.width/2)+(sideShift)-20+rShift,(app.height/4)+(row*size)-20+dShift,
                    (app.width/2)+(sideShift)+20+rShift,(app.height/4)+(row*size)+20+dShift,width = 3)
        if m.columns % 2 == 1:
            maxShift = size*(m.columns//2)
        else:
            maxShift = size*((m.columns//2)-0.5)
        canvas.create_arc((app.width/2)-maxShift-80+rShift,app.height/4-40+dShift,(app.width/2)-maxShift-40+rShift,app.height/4+40+(size*(m.rows-1))+dShift,
        fill = 'black', style = 'arc', start = 90, extent = 180, width = 5)
        canvas.create_arc((app.width/2)+maxShift+40+rShift,app.height/4-40+dShift,(app.width/2)+maxShift+80+rShift,app.height/4+40+(size*(m.rows-1))+dShift,
        fill = 'black', style = 'arc', start = 90, extent = -180, width = 5)

def draw2Matrix(app, canvas, m1, m2, scale, rShift, dShift):
            size1 = (app.height/2)/(max(max(m1.rows,m1.columns)-1,1)) * scale
            for row in range(m1.rows):
                for col in range(m1.columns):
                    if m1.columns % 2 == 1:
                        sideShift1 = size1*(col-(m1.columns//2))
                    else:
                        sideShift1 = size1*(col-(m1.columns//2)+0.5)
                    canvas.create_text((app.width/2)+(sideShift1)-rShift,(app.height/4)+(row*size1)+dShift,text=m1.elements[row][col],
                    font = 'Arial 18 bold')
                    if col == app.mX2 and row == app.mY2:
                        canvas.create_rectangle((app.width/2)+(sideShift1)-20-rShift,(app.height/4)+(row*size1)-20+dShift,
                        (app.width/2)+(sideShift1)+20-rShift,(app.height/4)+(row*size1)+20+dShift,width = 3)
            if m1.columns % 2 == 1:
                maxShift1 = size1*(m1.columns//2)
            else:
                maxShift1 = size1*((m1.columns//2)-0.5)
            canvas.create_arc((app.width/2)-maxShift1-80-rShift,app.height/4-40+dShift,(app.width/2)-maxShift1-40-rShift,app.height/4+40+(size1*(m1.rows-1))+dShift,
            fill = 'black', style = 'arc', start = 90, extent = 180, width = 5)
            canvas.create_arc((app.width/2)+maxShift1+40-rShift,app.height/4-40+dShift,(app.width/2)+maxShift1+80-rShift,app.height/4+40+(size1*(m1.rows-1))+dShift,
            fill = 'black', style = 'arc', start = 90, extent = -180, width = 5)
            #second matrix
            size2 = (app.height/2)/(max(max(m2.rows,m2.columns)-1,1)) * scale
            for row in range(m2.rows):
                for col in range(m2.columns):
                    if m2.columns % 2 == 1:
                        sideShift2 = size2*(col-(m2.columns//2))
                    else:
                        sideShift2 = size2*(col-(m2.columns//2)+0.5)
                    canvas.create_text((app.width/2)+(sideShift2)+rShift,(app.height/4)+(row*size2)+dShift,text=m2.elements[row][col],
                    font = 'Arial 18 bold')
                    if col+m1.columns == app.mX2 and row == app.mY2:
                        canvas.create_rectangle((app.width/2)+(sideShift2)-20+rShift,(app.height/4)+(row*size2)-20+dShift,
                        (app.width/2)+(sideShift2)+20+rShift,(app.height/4)+(row*size2)+20+dShift,width = 3)
            if m2.columns % 2 == 1:
                maxShift2 = size2*(m2.columns//2)
            else:
                maxShift2 = size2*((m2.columns//2)-0.5)
            canvas.create_arc((app.width/2)-maxShift2-80+rShift,app.height/4-40+dShift,(app.width/2)-maxShift2-40+rShift,app.height/4+40+(size2*(m2.rows-1))+dShift,
            fill = 'black', style = 'arc', start = 90, extent = 180, width = 5)
            canvas.create_arc((app.width/2)+maxShift2+40+rShift,app.height/4-40+dShift,(app.width/2)+maxShift2+80+rShift,app.height/4+40+(size2*(m2.rows-1))+dShift,
            fill = 'black', style = 'arc', start = 90, extent = -180, width = 5)

def edit1Matrix(row,col,input,m): #edits m[row][col] to be the input
    a = copy.deepcopy(m.elements)
    a[row][col] = input
    if isinstance(m, Vector):
        return Vector(a)
    else:
        return Matrix(m.rows,m.columns,a)

def checkElSelector(app,x,y): #moves input selector by clicking
    size = (app.height/2)/(max(max(app.m1.rows,app.m1.columns)-1,1))
    for row in range(app.m1.rows):
        for col in range(app.m1.columns):
            if app.m1.columns % 2 == 1:
                sideShift = size*(col-(app.m1.columns//2))
            else:
                sideShift = size*(col-(app.m1.columns//2)+0.5)
            if x > (app.width/2)+(sideShift)-20 and x < (app.width/2)+(sideShift)+20:
                if y > (app.height/4)+(row*size)-20 and y < (app.height/4)+(row*size)+20:
                    app.m1selX = col
                    app.m1selY = row

def selShift(app,dir): #moves the input selector around from keys
    if dir == 1:
        if app.m1selX != app.m1.columns-1:
            app.m1selX += 1
        else:
            app.m1selX = 0
            if app.m1selY != app.m1.rows-1:
                app.m1selY += 1
            else:
                app.m1selY = 0
    else:
        if app.m1selX != 0:
            app.m1selX -= 1
        else:
            app.m1selX = app.m1.columns-1
            if app.m1selY != 0:
                app.m1selY -= 1
            else:
                app.m1selY = app.m1.rows-1

def selShift2(app,dir):
        if app.mX2 < app.m1.columns:
            if dir == 1:
                if app.mX2 != app.m1.columns-1:
                    app.mX2 += 1
                else:
                    app.mX2 = 0
                    if app.mY2 != app.m1.rows-1:
                        app.mY2 += 1
                    else:
                        app.mY2 = 0
            else:
                if app.mX2 != 0:
                    app.mX2 -= 1
                else:
                    app.mX2 = app.m1.columns-1
                    if app.mY2 != 0:
                        app.mY2 -= 1
                    else:
                        app.mY2 = app.m1.rows-1
        else:
            if dir == 1:
                if app.mX2 != app.m1.columns+app.m2.columns-1:
                    app.mX2 += 1
                else:
                    app.mX2 = app.m1.columns
                    if app.mY2 != app.m2.rows-1:
                        app.mY2 += 1
                    else:
                        app.mY2 = 0
            else:
                if app.mX2 != app.m1.columns:
                    app.mX2 -= 1
                else:
                    app.mX2 = app.m1.columns+app.m2.columns-1
                    if app.mY2 != 0:
                        app.mY2 -= 1
                    else:
                        app.mY2 = app.m2.rows-1

def checkSidebar(app,x,y):#checks if sidebar is clicked
    for num in range(len(app.modes)):
        if x >= app.width-204 and x <= app.width-4:
            if y >= 4+50*num and y <= 54+50*num:
                if num == 0:
                    resetSelector(app)
                elif num == 1:
                    resetVectorMode(app)
                elif num == 2:
                    resetMatrixMode(app)
                else:
                    resetBasisMode(app)
                
runApp(width=1200, height=700)