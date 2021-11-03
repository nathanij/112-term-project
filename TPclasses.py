import tkinter as tk
import copy, math

class Matrix(object):
    def __init__(self, rows, columns, elements):
        self.rows = rows
        self.columns = columns
        self.elements = elements
        if rectangular(self.elements):
            self.legalMatrix = True
        else:
            self.legalMatrix = False
        if self.rows == self.columns:
            self.isSquare = True
        else:
            self.isSquare = False
        if checkDiagonal(self):
            self.isDiag = True
        else:
            self.isDiag = False
        if isIdentity(self):
            self.isI = True
        else:
            self.isI = False

    def scalarMult(self, n): #multiplies matrix by scalar
        if not self.legalMatrix:
            return 'Not a legal matrix!'
        else:
            productMat = copy.deepcopy(self.elements)
            for row in range (len(self.elements)):
                for col in range (len(self.elements[0])):
                    a = (productMat[row][col])
                    productMat[row][col] = n * a
            tSteps = [f'Original matrix, scalar = {n}', 'Scaled Matrix']
            mSteps = [self]
            aSteps = [self]
            if isinstance(self,Vector):
                q = Vector(productMat)
                mSteps.append(q)
                aSteps.append(q)
                return Vector(productMat), mSteps, aSteps, tSteps
            else:
                q = Matrix(len(productMat),len(productMat[0]),productMat)
                mSteps.append(q)
                aSteps.append(q)
                return Matrix(len(productMat),len(productMat[0]),productMat), mSteps, aSteps, tSteps

    def addMatrix(self,m2): #adds the two matrices
        if self.rows != m2.rows or self.columns != m2.columns:
            return 'Matrix sizes must match!'
        else:
            result = copy.deepcopy(self.elements)
            for row in range (len(result)):
                for col in range (len(result[0])):
                    result[row][col] += m2.elements[row][col]
            mSteps = [self]
            aSteps = [m2]
            tSteps = ['Original matrices', 'Added matrices element by element']
            if isinstance(self,Vector) and isinstance(m2,Vector):
                a = Vector(result)
                mSteps.append(a)
                aSteps.append(a)
                return a, mSteps, aSteps, tSteps
            else:
                a = Matrix(len(result),len(result[0]),result)
                mSteps.append(a)
                aSteps.append(a)
                return a, mSteps, aSteps, tSteps

    def subMatrix(self,m2):
        if not isinstance(m2, Matrix):
            return 'Input not a matrix!'
        elif self.rows != m2.rows or self.columns != m2.columns:
            return 'Matrix sizes must match!'
        else:
            result = copy.deepcopy(self.elements)
            for row in range (len(result)):
                for col in range (len(result[0])):
                    result[row][col] -= m2.elements[row][col]
            if isinstance(self,Vector) and isinstance(m2,Vector):
                sumMatrix = Vector(result)
            else:
                sumMatrix = Matrix(len(result),len(result[0]),result)
            return sumMatrix

    def multiplyMatrix(self,matrix2): #multiplies in order self*matrix2
        if not isinstance(matrix2, Matrix):
            return 'Input not a matrix!'
        elif self.columns != matrix2.rows:
            return 'Number of columns in m1 must match number of rows in m2'
        else:
            m1=copy.deepcopy(self.elements)
            m2=copy.deepcopy(matrix2.elements)
            product = [[0 for i in range(matrix2.columns)]\
                for j in range(self.rows)]
            for row in range(self.rows):
                for col in range(matrix2.columns):
                    v1 = Vector([m1[row]])
                    a = []
                    for r in range(len(m2)):
                        a.append(m2[r][col])
                    v2 = Vector([a])
                    a, b, c, d = v1.dotProduct(v2)
                    product[row][col] = a
            return Matrix(self.rows,matrix2.columns,product)

    def transpose(self): #finds transpose
        t = []
        for col in range(self.columns):
            a = []
            for row in range(self.rows):
                a.append(self.elements[row][col])
            t.append(a)
        tSteps = ['Original matrix and transpose (reflected across main diagonal)']
        mSteps = [self]
        aSteps = [Matrix(self.columns,self.rows,t)]
        return Matrix(self.columns,self.rows,t), mSteps, aSteps, tSteps

    def removeCol(self, xColumn): #removes a column
        if xColumn < 0 or xColumn >= self.columns:
            return 'Input a valid column to remove'
        newM = []
        for row in range(self.rows):
            newR = []
            for col in range(self.columns):
                if col != xColumn:
                    newR.append(self.elements[row][col])
            newM.append(newR)
        return Matrix(self.rows,self.columns-1,newM)
    
    def removeRow(self, xRow): #removes a row
        if xRow < 0 or xRow >= self.rows:
            return 'Input a valid row to remove'
        newM = self.elements[:xRow] + self.elements[xRow+1:]
        return Matrix(self.rows-1,self.columns,newM)

    '''def determinant(self): #first of the recursives (finds the determinant)
        if self.isSquare == False:
            return 'Matrix must be square'
        elif self.rows == 1:
            return self.elements[0][0]
        elif self.rows == 2:
            return self.elements[0][0]*self.elements[1][1]-\
                self.elements[0][1]*self.elements[1][0]
        else:
            flip = 1
            total = 0
            for element in range(self.columns):
                mult = self.elements[0][element]
                a = self.removeRow(0)
                newM = a.removeCol(element)
                total += flip * mult * newM.determinant()
                flip = alternate(flip)
            return total'''
    def determinant(self):
        if self.rows == 1:
            mSteps = [self]
            aSteps = [self]
            a = self.elements[0][0]
            tSteps = [f'Determinant of matrix is {a}']
            return a, mSteps, aSteps, tSteps
        elif self.rows == 2:
            mSteps = [self]
            aSteps = [self]
            a = self.elements[0][0]*self.elements[1][1] - self.elements[0][1]*self.elements[1][0]
            tSteps = [f'Determinant of matrix is {a}']
            return a, mSteps, aSteps, tSteps
        else:
            flip = 1
            total = 0
            mSteps = [self]
            aSteps = [self]
            tSteps = ['Determinant is alternating sum of submatrices * corresponding entry']
            for element in range(self.columns):
                mult = self.elements[0][element]
                a = self.removeRow(0)
                newM = a.removeCol(element)
                w, x, y, z = newM.determinant()
                total += flip * mult * w
                mSteps.append(newM)
                aSteps.append(newM)
                tSteps.append(f'Added {flip} * {mult} * {w} to total. \n Total = {total}')
                for entry in x:
                    mSteps.append(entry)
                    aSteps.append(entry)
                for entry in z:
                    tSteps.append(entry)
                flip = alternate(flip)
            mSteps.append(self)
            aSteps.append(self)
            tSteps.append(f'Total determinant is {total}')
            return total, mSteps, aSteps, tSteps



    def rowOp(self, row1, row2, factor): #adds row1*factor to row 2
        r1, r2 = copy.copy(self.elements[row1]), copy.copy(self.elements[row2])
        newM = []
        for row in range(self.rows):
            if row != row2:
                newM.append(self.elements[row])
            else:
                newR = []
                for element in range(self.columns):
                    newR.append(r2[element]+factor*r1[element])
                newM.append(newR)
        return Matrix(self.rows,self.columns,newM)

    def rowSwap(self, row1, row2):
        r1, r2 = copy.deepcopy(self.elements[row1]), copy.deepcopy(self.elements[row2])
        newM = []
        for row in range(self.rows):
            if row == row1:
                newM.append(r2)
            elif row == row2:
                newM.append(r1)
            else:
                newM.append(self.elements[row])
        return Matrix(self.rows,self.columns,newM)

    def rowScale(self, row1, scalar): #multiplies row by scalar
        r1 = copy.copy(self.elements[row1])
        newM = []
        for row in range(self.rows):
            if row != row1:
                newM.append(self.elements[row])
            else:
                newR = []
                for element in range(self.columns):
                    newR.append(r1[element]*scalar)
                newM.append(newR)
        return Matrix(self.rows,self.columns,newM)
    
    def diagonalOneScale(self, row): #generates the scalar for turning the diagonal entry to a 1
        scale = 1/self.elements[row][row]
        return scale 

    def isUTriangular(self): #used in inverse so each row independent already
        a =  self.elements
        for row in range(self.rows):
            for col in range(row+1):
                if row == col:
                    if a[row][col] != 1:
                        return False
                else:
                    if a[row][col] != 0:
                        return False
        return True

    def uTriStep(self, augment, tSteps): #Takes a step for upper triangularizing
        for col in range(self.columns):
            for row in range(col,self.rows):
                num = self.elements[row][col]
                if row == col:
                    if num != 1:
                        scale = self.diagonalOneScale(row)
                        s = self.rowScale(row,scale)
                        a = augment.rowScale(row,scale)
                        text = f'Multiplied row {row} by {scale}.'
                        tSteps.append(text)
                        return s, a, tSteps
                else:
                    if num != 0:
                        s = self.rowOp(col,row,0-num)
                        a = augment.rowOp(col,row,0-num)
                        text = f'Subtracted {num} times row {col} from row {row}'
                        tSteps.append(text)
                        return s,a, tSteps
        return self, augment, tSteps

    def uTriangulate(self, augment, aSteps, mSteps, tSteps): #turns self into upper triangular while applying the same operations to augment
        if self.isUTriangular():
            return self, augment, aSteps, mSteps, tSteps
        else:
            a, augment, tSteps= self.uTriStep(augment, tSteps)
            a.truncated()
            augment.truncated()
            aSteps.append(augment)
            mSteps.append(a)
            return a.uTriangulate(augment, aSteps, mSteps, tSteps)

    def stripDec(self): #strips long decimals for 0 and 1 (prefraction)
        for row in range(self.rows):
            for col in range(self.columns):
                for x in range(-3,4):
                    if abs(self.elements[row][col]-x)<.001:
                        self.elements[row][col] = x
        return self

    def truncated(self):
        for row in range(self.rows):
            for col in range(self.columns):
                num = self.elements[row][col]
                self.elements[row][col] = truncate(num, 3)
        return self

    
    def triToIn(self, augment, aSteps, mSteps, tSteps): #goes from triangular to inverse
        if self.isI:
            return augment, aSteps, mSteps, tSteps
        else:
            a, b, tSteps = self.triToInStep(augment, tSteps)
            a.truncated()
            b.truncated()
            aSteps.append(b)
            mSteps.append(a)
            return a.triToIn(b, aSteps, mSteps, tSteps)

    def triToInStep(self, augment, tSteps): #steps for above wrapper
        for row in range(self.rows):
            for col in range(1+row,self.columns):
                num = self.elements[row][col]
                if num != 0:
                    s = self.rowOp(col,row,0-num)
                    a = augment.rowOp(col,row,0-num)
                    text = f'Subtracted {num} times row {col} from row {row}'
                    tSteps.append(text)
                    return s, a, tSteps
        return self, augment, tSteps

    def inverse(self): #wrapper for finding inverse
        if self.isSquare == False:
            return 'Matrix must be square'
        elif self.determinant == 0:
            return 'Matrix not invertible'
        augment = createIdentity(self.rows)
        aSteps = [augment]
        mSteps = [self]
        tSteps = ['Original matrix and augmented identity']
        return self.findInverse(augment, aSteps, mSteps, tSteps)

    def findInverse(self, augment, aSteps, mSteps, tSteps): #calls triangulate then invert
        s, augment, aSteps, mSteps, tSteps = self.uTriangulate(augment, aSteps, mSteps, tSteps)
        return s.triToIn(augment, aSteps, mSteps, tSteps)
    
    def isFull(self): #checks if a matrix is full of integers and/or fractions
        for row in range(self.rows):
            for col in range(self.columns):
                if isinstance(self.elements[row][col],int) or isinstance(self.elements[row][col],Fraction):
                    pass
                else:
                    return False
        return True

    def rref(self):
        s, mSteps, tSteps = self.REF()
        return s.getRREF(mSteps, tSteps)

    def getRREF(self, mSteps, tSteps):
        if self.isRREF():
            pass

    def REF(self):
        mSteps = [self]
        tSteps = ['Original Matrix']
        return self.rowREF(mSteps, tSteps, 0)

    def refA(self, augment):
        mSteps = [self]
        tSteps = ['Original Matrix and Augment']
        aSteps = [augment]
        return self.rowRefA(augment, mSteps, aSteps, tSteps, 0)

    def rowREF(self,mSteps,tSteps,count):
        if self.rowShuffle(mSteps,tSteps, count) != None:
            return self.rowShuffle(mSteps, tSteps, count)  
        else:
            count += 1
            return self.rowREF(mSteps, tSteps, count)

    def rowRefA(self, augment, mSteps, aSteps, tSteps, count):
        if self.rowShuffleA(augment, mSteps, aSteps, tSteps, count) != None:
            return self.rowShuffleA(augment, mSteps, aSteps, tSteps, count)
        else:
            count += 1
            return self.rowRefA(augment, mSteps, aSteps, tSteps, count)

    def rowShuffle(self, mSteps, tSteps, count):
        if self.rows == 2:
            if count == 0:
                return self.toREF(mSteps,tSteps,0)
            else:
                s = self.rowSwap(0, 1)
                text = f'Swapped Row 0 with Row 1'
                tSteps.append(text)
                mSteps.append(s)
                return s.toREF(mSteps,tSteps,0)
        elif self.rows == 3:
            if count == 0:
               return self.toREF(mSteps,tSteps,0)
            elif count % 2 == 1:
                s = self.rowSwap(0, 1)
                text = f'Swapped Row 1 with Row 2'
                tSteps.append(text)
                mSteps.append(s)
                return s.toREF(mSteps, tSteps,0)
            else:
                s = self.rowSwap(0, 2)
                text = f'Swapped Row 1 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                return s.toREF(mSteps, tSteps,0) 
        elif self.rows == 4:
            if count == 0:
               return self.toREF(mSteps,tSteps,0)
            elif count % 2 == 1:
                s = self.rowSwap(2, 3)
                text = f'Swapped Row 2 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                return s.toREF(mSteps, tSteps,0)
            elif count % 5 == 1:
                s = self.rowSwap(0, 3)
                text = f'Swapped Row 0 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                return s.toREF(mSteps, tSteps,0) 
            else:
                s = self.rowSwap(1, 3)
                text = f'Swapped Row 1 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                return s.toREF(mSteps, tSteps,0) 

    def rowShuffleA(self, augment, mSteps, aSteps, tSteps, count):
        if self.rows == 2:
            if count == 0:
                return self.toRefA(augment, mSteps, aSteps, tSteps,0)
            else:
                s = self.rowSwap(0, 1)
                text = f'Swapped Row 0 with Row 1'
                tSteps.append(text)
                mSteps.append(s)
                a = augment.rowSwap(0,1)
                aSteps.append(a)
                return s.toRefA(a, mSteps,aSteps, tSteps,0)
        elif self.rows == 3:
            if count == 0:
               return self.toRefA(augment, mSteps, aSteps, tSteps,0)
            elif count % 2 == 1:
                s = self.rowSwap(0, 1)
                text = f'Swapped Row 1 with Row 2'
                tSteps.append(text)
                mSteps.append(s)
                a = augment.rowSwap(0,1)
                aSteps.append(a)
                return s.toRefA(a, mSteps,aSteps, tSteps,0)
            else:
                s = self.rowSwap(0, 2)
                text = f'Swapped Row 1 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                a = augment.rowSwap(0,2)
                aSteps.append(a)
                return s.toRefA(a, mSteps,aSteps, tSteps,0)
        elif self.rows == 4:
            if count == 0:
               return self.toRefA(augment, mSteps, aSteps, tSteps,0)
            elif count % 2 == 1:
                s = self.rowSwap(2, 3)
                text = f'Swapped Row 2 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                a = augment.rowSwap(2,3)
                aSteps.append(a)
                return s.toRefA(a, mSteps,aSteps, tSteps,0)
            elif count % 5 == 1:
                s = self.rowSwap(0, 3)
                text = f'Swapped Row 0 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                a = augment.rowSwap(0,3)
                aSteps.append(a)
                return s.toRefA(a, mSteps,aSteps, tSteps,0)
            else:
                s = self.rowSwap(1, 3)
                text = f'Swapped Row 1 with Row 3'
                tSteps.append(text)
                mSteps.append(s)
                a = augment.rowSwap(1,3)
                aSteps.append(a)
                return s.toRefA(a, mSteps,aSteps, tSteps,0)

    def toREF(self, mSteps, tSteps, count):
        if self.isREF():
            return self, mSteps, tSteps
        elif count > 200:
            return None
        else:
            m, mSteps, tSteps = self.refStep(mSteps, tSteps)
            count += 1
            return m.toREF(mSteps, tSteps, count)

    def toRefA(self, augment, mSteps, aSteps, tSteps, count):
        if self.isREF():
            return self, augment, mSteps, aSteps, tSteps
        elif count > 200:
            return None
        else:
            m, a, mSteps, aSteps, tSteps = self.refStepA(augment, mSteps, aSteps, tSteps)
            count += 1
            return m.toRefA(a, mSteps, aSteps, tSteps, count)

    def refStep(self, mSteps, tSteps):
        count = -1
        pRow = 0
        for col in range(self.columns):
            for row in range(col,self.rows):
                num = self.elements[row][col]
                if num != 0:
                    if col <= count:
                        scale = findMultiplier(num,self.elements[pRow][col],0)
                        m = self.rowOp(pRow,row,scale)
                        text = f'Added {scale} times row {pRow} to row {row}'
                        tSteps.append(text)
                        m.truncated()
                        mSteps.append(m)
                        return m, mSteps, tSteps
                    else:
                        count = col
                        pRow = row
        return self, mSteps, tSteps

    def refStepA(self, augment, mSteps, aSteps, tSteps):
        count = -1
        pRow = 0
        for col in range(self.columns):
            for row in range(col,self.rows):
                num = self.elements[row][col]
                if num != 0:
                    if col <= count:
                        scale = findMultiplier(num,self.elements[pRow][col],0)
                        m = self.rowOp(pRow,row,scale)
                        a = augment.rowOp(pRow,row,scale)
                        text = f'Added {scale} times row {pRow} from row {row}'
                        tSteps.append(text)
                        m.truncated()
                        a.truncated()
                        mSteps.append(m)
                        aSteps.append(a)
                        return m, a, mSteps, aSteps, tSteps
                    else:
                        count = col
                        pRow = row
        return self, augment, mSteps, aSteps, tSteps


    def refSwapLegal(self,row1,row2):
        if row1 == row2:
            return False
        else:
            return (self.rowSwap(row1,row2)).isREF()
    
    def charPoly(self): #return coeffs of characteristic polynomial
        if self.rows == 2:
            a = 1
            b = -self.elements[0][0]-self.elements[1][1]
            c = self.determinant()
            return [a, b, c]
        elif self.rows == 3:
            a = self.elements[0][0]
            b = self.elements[0][1]
            c = self.elements[0][2]
            d = self.elements[1][0]
            e = self.elements[1][1]
            f = self.elements[1][2]
            g = self.elements[2][0]
            h = self.elements[2][1]
            i = self.elements[2][2]
            A = 1
            B = -i-e-a
            C = i*e-f*h+a*e+a*i-b*d-c*g
            D = -a*i*e-a*f*h+b*d*i+b*f*g+c*d*h+c*e*g
            return [A, B, C, D]

    def eigen(self): #CITATION uses cubic formula from HW1, https://www.cs.cmu.edu/~112/notes/hw1.html
        values = set()
        if self.rows > 3 or self.rows < 1:
            return 'Only 2 and 3 dimensions supported'
        elif self.rows == 2:
            a, b, c = self.charPoly()[0], self.charPoly()[1], self.charPoly()[2]
            var = [-1,1]
            for num in var:
                value = (-b + num * (b**2-4*a*c)**(1/2))/2*a
                values.add(truncate(value,3))
                return values
        else:
            a, b, c, d = self.charPoly()[0], self.charPoly()[1], self.charPoly()[2], self.charPoly()[3]
            p = -b/(3*a)
            q = p**3 + (b*c-3*a*d)/(6*a**2)
            r = c/(3*a)
            r1 = (q+(q**2+(r-p**2)**3)**(1/2))**(1/3)
            r1 += (q-(q**2+(r-p**2)**3)**(1/2))**(1/3) + p 
            values.add(truncate(r1.real,3))
            r2 = (-b-(r1*a)+(b**2-4*a*c-2*a*b*r1-3*(a**2)*(r1**2))**(1/2))/(2*a)
            values.add(truncate(r2.real,3))
            r3 = (-b-r1*a-(b**2-4*a*c-2*a*b*r1-3*(a**2)*(r1**2))**(1/2))/(2*a)
            values.add(truncate(r3.real,3))
            return values

            

    def isREF(self):
            count = -1
            for row in range(self.rows):
                for col in range(self.columns):
                    if self.elements[row][col] != 0:
                        if col <= count:
                            return False
                        else:
                            count = col
                            break
            return True

    def isRREF(self):
        count = -1
        for col in range(self.columns):
            for row in range(self.rows):
                value = self.elements[row][col]        
        return True

class Vector(Matrix):
    def __init__(self, elements):
        self.rows = 1
        self.columns = len(elements[0])
        self.elements = elements
        self.legalMatrix = True

    def dotProduct(self,v2): #dots the two vectors
        if not isinstance(v2, Vector):
            return 'Input must be a Vector'
        elif self.columns != v2.columns:
            return 'Vectors must be the same length'
        else:
            text = ''
            dProd = 0
            for element in range(self.columns):
                dProd = dProd+self.elements[0][element]*v2.elements[0][element]
                text += f'{self.elements[0][element]}*{v2.elements[0][element]}+'
            text = text[:len(text)-1]
            mSteps = [self]
            aSteps = [v2]
            tSteps = [text]
            return dProd, mSteps, aSteps, tSteps
    
    def cross(self,vector2): #represents self X vector 2
        if not isinstance(vector2, Vector):
            return 'Input must be a Vector'
        elif self.columns != 3 or vector2.columns !=3:
            return 'Vectors must be of length 3'
        else:
            v1=copy.deepcopy(self.elements)
            v2=copy.deepcopy(vector2.elements)
            text = f'({v1[0][1]}*{v2[0][2]} - {v1[0][2]}*{v2[0][1]}), ({v1[0][2]}*{v2[0][0]} - {v1[0][0]}*{v2[0][2]}), ({v1[0][0]}*{v2[0][1]} - {v1[0][1]}*{v2[0][0]})'
            emptyCross = [[0,0,0]]
            emptyCross[0][0]=v1[0][1]*v2[0][2] - v1[0][2]*v2[0][1]
            emptyCross[0][1]=v1[0][2]*v2[0][0] - v1[0][0]*v2[0][2]
            emptyCross[0][2]=v1[0][0]*v2[0][1] - v1[0][1]*v2[0][0]
            tSteps = ['original two vectors',text]
            crossProduct = Vector(emptyCross)
            aSteps = [vector2, crossProduct]
            mSteps = [self,crossProduct]
            return crossProduct, mSteps, aSteps, tSteps

    def projection(self,direction): #projection of self onto direction
        if not isinstance(direction,Vector):
            return 'Direction must be a vector'
        elif self.columns != direction.columns:
            return 'Vectors must be the same dimension'
        else:
            A, a, b, c = self.dotProduct(direction)
            B, a, b, c = direction.dotProduct(direction)
            scalar = A/B
            proj, a, b, c = direction.scalarMult(scalar)
            proj.truncated()
            mSteps = [self, proj]
            aSteps = [direction, proj]
            text = f'({self.elements[0]}*{direction.elements[0]}/{direction.elements[0]}*{direction.elements[0]})*{direction.elements[0]} = {truncate(scalar,3)} * {direction.elements[0]}'
            tSteps = ['Original two vectors',text]
            return proj, mSteps, aSteps, tSteps

    def projectionMatrix(self): #generates the projection matrix for self
        a, text, b, c = self.dotProduct(self)
        scalar = 1/a
        q , A, B, C = self.transpose()
        matrix = q.multiplyMatrix(self)
        tSteps = ['Direction and its transpose',f'Scalar is {truncate(1/a,3)}, unscaled on left, scaled on right']
        result, a, b, c = matrix.scalarMult(scalar)
        result.truncated()
        mSteps = [self,result]
        aSteps = [q,matrix]
        return result, mSteps, aSteps, tSteps

def rectangular(a): #checks if matrix is rectangular
    if len(a) ==1 or len(a) == 0:
        return True
    else:
        length = len(a[0])
        for row in range(1,len(a)):
            if len(a[row]) != length:
                return False
        return True

def sameSize(a,b): #checks if two matrices are the same size
    if len(a) != len(b):
        return False
    else:
        for row in range (len(a)):
            if len(a[row]) != len(b[row]):
                return False
        return True

def createIdentity(n): #creates n by n identity
    if n<1:
        return None
    I = [[0 for i in range(n)]for j in range(n)]
    for coord in range(n):
        I[coord][coord] = 1
    return Matrix(n,n,I)

def createEmpty(rows,cols):#creates an empty matrix
    e = [['___' for i in range(cols)]for j in range(rows)]
    if rows == 1:
        return Vector(e)
    else:
        return Matrix(rows,cols,e)

def checkDiagonal(a): #checks if a matrix is diagonal
    if not a.isSquare:
        return False
    else:
        for row in range(a.rows):
            for col in range(a.columns):
                if a.elements[row][col] != 0 and row != col:
                    return False
        return True

def isIdentity(a): #check if a matrix is the identity
    if not a.isDiag:
        return False
    else:
        for row in range(a.rows):
            for col in range(a.columns):
                if a.elements[row][col] != 0 and row != col:
                    return False
        return True

def alternate(a): #flips between 1 and -1
    if a == 1:
        return -1
    else:
        return 1

def findMultiplier(a, b, target): #finds the correct multiplier for a target value
    return (target-a)/b

class Fraction(object):
    def __init__(self, num, denom):
        self.num = num
        self.denom = denom
        if num % denom == 0:
            self.isInt = True
        else:
            self.isInt = False
        self.display = f'{num}/{denom}'

    def multiply(self, factor):#multiplies fractions by a fraction or integer
        if isinstance(factor, int):
            a = self.num * factor
            return Fraction(a, self.denom)
        else:
            a = self.num * factor.num
            b = self.denom * factor.denom
            return Fraction(a,b)

    def value(self): #decimal value for fraction
        return self.num/self.denom

    def reduce(self): #simplifies the fraction
        factor = gcf(self.num, self.denom)
        a = self.num//factor
        b = self.denom//factor
        return Fraction(a,b)

def gcf(a, b): #generates gcf of two numbers
    l1, l2 = primeFac(a), primeFac(b)
    factor = 1
    for element in l1:
        if element in l2:
            factor *= element
            l2.remove(element)
    return factor

def primeFac(n): #wrapper for prime factorization of n
    l = []
    return primeFac2(n, l)

def primeFac2(n, l): #builds the list
    if n == 1:
        return l
    else:
        if n % 2 == 0:
            n //= 2
            l.append(2)
            return primeFac2(n, l)
        else:
            for factor in range(3, n+1, 2):
                if isPrime(factor) and n % factor == 0:
                    n //= factor
                    l.append(factor)
                    return primeFac2(n, l)

def isPrime(n): #CITATION: used class version of fasterIsPrime from https://www.cs.cmu.edu/~112/notes/notes-loops.html
    if (n < 2):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False
    maxFactor = round(n**0.5)
    for factor in range(3,maxFactor+1,2):
        if (n % factor == 0):
            return False
    return True

def gramSchmidt(L):#L is list of vectors with same dimension, n=0
    #if not indep(L):
        #return 'Vectors not a basis'
    basis = set()
    b1 = L[0]
    s, A, B, C = b1.dotProduct(b1)
    b1, A, B, C = b1.scalarMult((1/s)**(1/2))
    b1 = b1.truncated()
    basis.add(b1)
    mSteps = [b1]
    aSteps = [b1]
    tSteps = ['Normalized the first basis vector']
    return gS(L[1:], basis, mSteps, aSteps, tSteps)

def gS(L, basis, mSteps, aSteps, tSteps):
    if len(L) == 0:
        return basis, mSteps, aSteps, tSteps
    else:
        v2 = L[0]
        mSteps.append(v2)
        aSteps.append(v2)
        tSteps.append('Take projection of next vector onto each new basis vector.')
        c = Vector([[0 for i in range(len(v2.elements[0]))]])
        for v in basis:
            a, B, C, D = v2.projection(v)
            c, d, e, f = c.addMatrix(a)
        c = c.truncated()
        tSteps.append('The sum of the projections')
        mSteps.append(c)
        aSteps.append(c)
        b2 = v2.subMatrix(c)
        b2 = b2.truncated()
        tSteps.append('Subtract the sum from the vector')
        mSteps.append(b2)
        aSteps.append(b2)
        s, A, B, C = b2.dotProduct(b2)
        b2, A, B, C = b2.scalarMult((1/s)**(1/2))
        b2 = b2.truncated()
        tSteps.append('Normalize the vector and add to basis.')
        mSteps.append(b2)
        aSteps.append(b2)
        basis.add(b2)
        return gS(L[1:], basis, mSteps, aSteps, tSteps)

def indep(L):
    pass

def closeEnough(num, target):
    if abs(num-target) <= 10**(-3):
        return True
    else:
        return False

def truncate(number, digits) -> float: #CITATION, taken from https://stackoverflow.com/questions/8595973/truncate-to-three-decimals-in-python
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

def solveEq(M, A): #solves equation represented in matrix form with augment
    mat, aug, mSteps, aSteps, tSteps = M.refA(A)
    if aug.rows == 2:
        b = aug.elements[1][0] / mat.elements[1][1]
        a = (aug.elements[0][0] - b*mat.elements[0][1]) / mat.elements [0][0]
        mSteps.append(mat)
        aSteps.append(aug)
        tSteps.append(f'a = {a}, b = {b}')
        return a, b, mSteps, aSteps, tSteps
    if aug.rows == 3:
        c = aug.elements[2][0] / mat.elements[2][2]
        b = (aug.elements[1][0] - c * mat.elements[1][2])/mat.elements[1][1]
        a = (aug.elements[0][0]-b*mat.elements[0][1]-c*mat.elements[0][2])/mat.elements[0][0]
        mSteps.append(mat)
        aSteps.append(aug)
        tSteps.append(f'a = {a}, b = {b}, c = {c}')
        return a, b, c, mSteps, aSteps, tSteps

def changeBasis(B1, B2):
    mSteps = []
    aSteps = []
    tSteps = []
    bMat = [[0 for i in range(len(B1))] for j in range(B1[0].columns)]
    for v in range(len(B1)):
        for e in range(B1[v].columns):
            bMat[e][v] = B1[v].elements[0][e]
    bMat = Matrix(B1[0].columns,len(B1), bMat)
    mSteps.append(bMat)
    aSteps.append(bMat)
    tSteps.append('Matrix for solving for coefficients')
    sMat = [[0 for i in range(len(B1))] for j in range(B1[0].columns)]
    if B2[0].columns == 2:
        for v in range(len(B2)):
            vf, A, B, C = B2[v].transpose()
            a, b, mS, aS, tS = solveEq(bMat, vf)
            for element in mS:
                mSteps.append(element)
            for element in aS:
                aSteps.append(element)
            for element in tS:
                tSteps.append(element)
            sMat[0][v] = a
            sMat[1][v] = b
            q = Matrix(B1[0].columns,len(B1), copy.deepcopy(sMat))
            q = q.truncated()
            mSteps.append(q)
            aSteps.append(q)
            tSteps.append('Put solved coefficients in as a column of the solution matrix')
        sol = Matrix(B1[0].columns,len(B1), sMat)
        sol = sol.truncated()
        return sol, mSteps, aSteps, tSteps
    elif B2[0].columns == 3:
        for v in range(len(B2)):
            vf, A, B, C = B2[v].transpose()
            a, b, c, mS, aS, tS = solveEq(bMat, vf)
            for element in mS:
                mSteps.append(element)
            for element in aS:
                aSteps.append(element)
            for element in tS:
                tSteps.append(element)
            sMat[0][v] = a
            sMat[1][v] = b
            sMat[2][v] = c
            q = Matrix(B1[0].columns,len(B1), copy.deepcopy(sMat))
            mSteps.append(q.truncated())
            aSteps.append(q.truncated())
            tSteps.append('Put solved coefficients in as a column of solution matrix')
        sol = Matrix(B1[0].columns,len(B1), sMat)
        sol = sol.truncated()
        return sol, mSteps, aSteps, tSteps
