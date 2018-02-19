import sys
IO = 0

class BPlusTREE:
    KeyType = None
    ValType = None
    Head = None
    Height = 0
    d = 60
    
    def __init__(self,_d = 60,kType = int, vType = tuple):
        self.KeyType = kType
        self.ValType = vType
        self.Head = None
        self.Height = 0
        self.d = _d
        
        
    def delete(self,key): #TODO
        pass
    
    def insert(self,key,value):
        if not (isinstance( key, self.KeyType ) and isinstance(value, self.ValType)):
            raise TypeError("BPlusTree.insert can only accept input (<keyType = int>,<valType = tuple>)")
        if (self.Head == None):
            self.Height = self.Height+1
            self.Head = Node(self.d)
        newHead = self.Head.insert(key,value)
        if newHead!=None:
            self.Height = self.Height+1
            self.Head = newHead
                
    def rangeSearch(self,keyStart,keyEnd):
        global IO
        IO+=1

        if not (isinstance( keyStart, self.KeyType) and isinstance( keyEnd, self.KeyType )):
            raise TypeError("BPlusTree.rangeSearch van only accept input (<keyType = int>,<keyType = int>)")
        if  (self.Head == None):
            return []
        else:
            result = []
            self.Head.rangeSearch(keyStart,keyEnd,result)
            return result
        
        
    
    def search(self,key):
        if not(isinstance( key, self.KeyType )):
            raise TypeError("BPlusTree.search can only accept input (<keyType = int>)")

        elif (self.Head == None):
            return None
        
        return self.Head.search(Key)
            
    
class Node:
    myPar = None
    myPointers = None
    myKeys = None
    myVals = None
    d = 60


    def __init__(self,_d = 60,Parent=None):
        self.myPar = Parent
        self.myPointers = [None]*(2*_d+2)
        self.myKeys = []
        self.myVals = []
        self.d = _d

    def search(self,key):
        i=0
        while i<len(self.myKeys):
            if key<=self.myKeys[i]:
                if self.myPointers[1]==None:
                    return self.myVals[i]
                else:
                    return self.myPointers[i].search(key)
            i+=1
        if self.myPointers[1]==None:
            return None
        else:
            return self.myPointers[len(self.myKeys)].search(key)
    def rangeSearch(self,keyStart,keyEnd,Solution):
        global IO
        IO+=1

        i=0
        while i<len(self.myKeys):
            if keyStart<=self.myKeys[i]:
                if self.myPointers[1]==None:
                    self.rangeSearchHelper(keyStart,keyEnd,Solution)
                    return 0
                else:
                    self.myPointers[i].rangeSearch(keyStart,keyEnd,Solution)
                    return 0
            i+=1
        if self.myPointers[1]==None:
            self.rangeSearchHelper(keyStart,keyEnd,Solution)
        else:
            self.myPointers[len(self.myKeys)].rangeSearch(keyStart,keyEnd,Solution)
    def rangeSearchHelper(self,keyStart,keyEnd,Solution):
        global IO
        IO+=1

        #Solution.extend(myVals) #Removed for testing
        if self.myPointers[-1]!=None:
            if self.myKeys[-1]<keyEnd:
                self.myPointers[-1].rangeSearchHelper(keyStart,keyEnd,Solution)


    def insert(self,key,value):
        i=0
        while i<len(self.myKeys) and key>self.myKeys[i]:
            i+=1
            
        if self.myPointers[1] == None:
            self.myKeys.insert(i,key)
            self.myVals.insert(i,value)
            if (len(self.myKeys)>2*self.d):
                ANode = Node(_d = self.d, Parent = self.myPar)
                ANode.myPointers[0] = self
                ANode.myPointers[-1] = self.myPointers[-1]
                self.myPointers[-1] = ANode
                for foo in range(self.d):
                    ANode.insert(self.myKeys.pop(),self.myVals.pop())
                if self.myPar == None:
                    self.myPar = Node(_d = self.d)
                    ANode.myPar = self.myPar
                    self.myPar.parentInsert(self.myKeys[-1],ANode,self)
                    return self.myPar
                else:
                    ANode.myPar = self.myPar
                    return self.myPar.parentInsert(self.myKeys[self.d],ANode)
        else:
            return self.myPointers[i].insert(key,value)
        return None

    def parentInsert(self,key,rightNode,leftNode = None):
        i=0
        if leftNode != None:
            self.myPointers[0] = leftNode
            self.myPointers[1] = rightNode
            self.myKeys.append(key)
        else:
            while i<len(self.myKeys) and key>self.myKeys[i]:
                i+=1
            self.myKeys.insert(i,key)
            while (i<len(self.myKeys)):
                self.myPointers[i+1],rightNode = (rightNode,self.myPointers[i+1])
                i+=1
        if (len(self.myKeys)>2*self.d):
            ANode = Node(_d = self.d, Parent = self.myPar)
            tempNode1 = self.myPointers.pop(self.d+1)
            tempNode1.myPar = ANode
            for foo in range(self.d):
                tempNode2 = self.myPointers.pop()
                tempNode2.myPar = ANode
                ANode.parentInsert(self.myKeys.pop(),tempNode2,tempNode1)
                tempNode1 = None
            self.myPointers.extend([None]*(self.d+1))
            if self.myPar==None:
                self.myPar = Node(self.d)
                ANode.myPar = self.myPar
                self.myPar.parentInsert(self.myKeys.pop(),ANode,self)
                return self.myPar
            else:
                ANode.myPar = self.myPar
                return self.myPar.parentInsert(self.myKeys.pop(),ANode)
        return None
def mapToInt(xCoord,yCoord,precision):
    P = 1<<precision
    X = int(xCoord*P)
    Y = int(yCoord*P)
    return (X,Y)

def GetH_Value(xCoord,yCoord,precision):
    rotation_table = [3,0,0,1]
    sense_table= [-1,1,1,-1]
    quad_table = [[[0,1],[3,2]],[[1,2],[0,3]],[[2,3],[1,0]],[[3,0],[2,1]]]
    rotation = 0
    sense = 1
    num = 0
    k = 1<<precision
    p = precision
    while p>=0:
        xbit = xCoord>>p
        ybit = yCoord>>p
        xCoord = xCoord%k
        yCoord = yCoord%k
        quad = quad_table[rotation][xbit][ybit]
        if sense==-1:
            num+= k*k*(3-quad)
        else:
            num+= k*k*quad
        num += (sense == -1)
        rotation += rotation_table[quad]
        rotation = rotation%4
        sense = sense*sense_table[quad]
        k = k>>1
        p -= 1
    return num

def GetZ_Value(xCoord,yCoord,precision):
    X,Y = (xCoord,yCoord)
    i = 0
    Q = 1
    Ret = 0
    while i<precision:
        Ret += (X&Q) << i
        Ret += (Y&Q) << (i+1)
        Q = Q<<1
        i+=1
    return Ret

def split_list(n):
    return [(x+1) for x,y in zip(n, n[1:]) if y-x != 1]

def get_sub_list(my_list):
    my_index = split_list(my_list)
    output = list()
    prev = 0
    for index in my_index:
        new_list = [ x for x in my_list[prev:] if x < index]
        output.append(new_list)
        prev += len(new_list)
    output.append([ x for x in my_list[prev:]])
    return output	

def Map2dto1d(x1,y1,x2,y2,precision,func):
    X1,Y1 = mapToInt(x1,y1,precision)
    X2,Y2 = mapToInt(x2,y2,precision)
    
    if Y1>Y2:
        Y1,Y2 = (Y2,Y1)
    if X1>X2:
        X1,X2 = (X2,X1)
    
    Ranges = []
    
    for V in range(X1,X2+1):
        for U in range(Y1,Y2+1):
            Ranges.append(func(V,U,precision))
    Ranges = sorted(Ranges)
    Final = get_sub_list(Ranges)
    
    return Final



Di =["dataset1.txt","dataset2.txt"]
Dj =["Squeries.txt","Uqueries.txt"]
Dk =[GetH_Value,GetZ_Value]
Dk2 = ["H","Z"]

d = 60
P = 5


for i in range(2):
    for k in range(2):
        File = open(Di[i])
        MyTree = BPlusTREE(d)
        Func = Dk[k]
        for line in File:
            X,Y = map(float,line.strip().split(','))
            nX,nY = mapToInt(X,Y,P)
            MyTree.insert(Func(nX,nY,P),(X,Y))

        for j in range(2):
            File2 = open(Dj[j])
            count = 0
            for line in File2:
                x1,y1,x2,y2 = map(float,line.strip().split(','))
                count +=1
                Ranges = Map2dto1d(x1,y1,x2,y2,P,Func)
                for R in Ranges:
                    if R!=[]:
                        MyTree.rangeSearch(R[0],R[-1])
            print("FINISHED")
            print((Di[i],Dj[j],Dk2[k]))
            print(MyTree.Height)
            print(IO)
            print(IO/count)
            IO = 0
