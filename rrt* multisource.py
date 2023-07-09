import numpy as np
import cv2
import random
import math

dist = 25

class node:
    def __init__(self, x, y, parent,cost):
        self.x = x
        self.y = y
        self.parent = parent
        self.cost=cost

class RRTmap:
    
    def __init__(self, img):
        self.img = img
        self.nodelist = [[], []]

    def addnode(self, x, y, parent, tree, cost=float(dist)):
        if parent!=None:
            self.nodelist[tree].append(node(x, y, parent,parent.cost+cost))
        else:
            self.nodelist[tree].append(node(x, y, parent,cost))

 
    def dfsgreen(self,img,i,j):
        n,l,t=np.shape(img)
        img[i,j]=[255,255,255]
        if (i-1>=0):
            if (img[i-1,j,1] > 0 and img[i-1,j,0] ==0 and img[i-1,j,2] ==0 ):
                self.dfsgreen(img,i-1,j)

        if (j-1>=0):
            if (img[i,j-1,1] > 0 and img[i,j-1,0] ==0 and img[i,j-1,2] ==0 ):
  
                self.dfsgreen(img,i,j-1)        
        if (j+1<l):
            if (img[i,j+1,1] > 0 and img[i,j+1,0] ==0 and img[i,j+1,2] ==0 ):

                self.dfsgreen(img,i,j+1)
        if (i+1<n):
            if (img[i+1,j,1] > 0 and img[i+1,j,0] ==0 and img[i+1,j,2] ==0 ):

                self.dfsgreen(img,i+1,j)
        if ((i-1>=0) and (j-1>=0)):
            if (img[i-1,j-1,1] > 0 and img[i-1,j-1,0] ==0 and img[i-1,j-1,2] ==0 ):

                self.dfsgreen(img,i-1,j-1)
        if ((i-1>=0) and (j+1<l)):
            if (img[i-1,j+1,1] > 0 and img[i-1,j+1,0] ==0 and img[i-1,j+1,2] ==0 ):

                self.dfsgreen(img,i-1,j+1)
        if ((i+1<n) and (j-1>=0)):
            if (img[i+1,j-1,1] > 0 and img[i+1,j-1,0] ==0 and img[i+1,j-1,2] ==0 ):

                self.dfsgreen(img,i+1,j-1)
        if ((i+1<n) and (j+1<l)):
            if (img[i+1,j+1,1] > 0 and img[i+1,j+1,0] ==0 and img[i+1,j+1,2] ==0 ):

                self.dfsgreen(img,i+1,j+1)

    
    def dfsred(self,img,i,j):
        n,l,t=np.shape(img)
        img[i,j]=[255,255,255]
        if (i-1>=0):
            if (img[i-1,j,2] > 0 and img[i-1,j,0] ==0 and img[i-1,j,1] ==0 ):
                self.dfsred(img,i-1,j)

        if (j-1>=0):
            if (img[i,j-1,2] > 0 and img[i,j-1,0] ==0 and img[i,j-1,1] ==0 ):
  
                self.dfsred(img,i,j-1)        
        if (j+1<l):
            if (img[i,j+1,2] > 0 and img[i,j+1,0] ==0 and img[i,j+1,1] ==0 ):

                self.dfsred(img,i,j+1)
        if (i+1<n):
            if (img[i+1,j,2] > 0 and img[i+1,j,0] ==0 and img[i+1,j,1] ==0 ):

                self.dfsred(img,i+1,j)
        if ((i-1>=0) and (j-1>=0)):
            if (img[i-1,j-1,2] > 0 and img[i-1,j-1,0] ==0 and img[i-1,j-1,1] ==0 ):

                self.dfsred(img,i-1,j-1)
        if ((i-1>=0) and (j+1<l)):
            if (img[i-1,j+1,2] > 0 and img[i-1,j+1,0] ==0 and img[i-1,j+1,1] ==0 ):

                self.dfsred(img,i-1,j+1)
        if ((i+1<n) and (j-1>=0)):
            if (img[i+1,j-1,2] > 0 and img[i+1,j-1,0] ==0 and img[i+1,j-1,1] ==0 ):

                self.dfsred(img,i+1,j-1)
        if ((i+1<n) and (j+1<l)):
            if (img[i+1,j+1,2] > 0 and img[i+1,j+1,0] ==0 and img[i+1,j+1,1] ==0 ):

                self.dfsred(img,i+1,j+1)

    def findstart(self):
        r, c, t = np.shape(self.img)
        temp=np.copy(self.img)
        count=0
        for i in range(r):
            for j in range(c):
                if (temp[i][j][2] > 0 and temp[i][j][0] ==0 and temp[i][j][1] ==0):
                    self.addnode(i, j, None, 0,0.0)
                    self.dfsred(temp,i,j)
                    count+=1
        print("start count=",count)

    def findend(self):
        r, c, t = np.shape(self.img)
        temp=np.copy(self.img)
        count=0
        for i in range(r):
            for j in range(c):
                if (temp[i][j][1] > 0 and temp[i][j][2] ==0 and temp[i][j][0] ==0):
                    self.addnode(i, j, None, 1,0.0)
                    self.dfsgreen(temp,i,j)
                    count+=1
        print("end count=",count)

    def randpt(self):
        r, c, t = np.shape(self.img)
        x = random.randint(0, r-1)
        y = random.randint(0, c-1)
        return (x, y)


    def calcdist(self, node, pt):
        return ((node.x-pt[0])**(2)+(node.y-pt[1])**(2))**(1/2)

    def findclosest(self, pt, tree):
        dist = []

        for node in self.nodelist[tree]:
            dist.append(self.calcdist(node, pt))
        distind = np.argsort(dist)
        return self.nodelist[tree][distind[0]]

    def showedge(self, pt1, pt2, tree):
        if tree==2:
            cv2.line(self.img, pt1, pt2, (200, 0, 200), 6)
        
        elif tree==3:
            cv2.line(self.img, pt1, pt2, (200, 200, 200), 2)            

        elif tree:
            cv2.line(self.img, pt1, pt2, (0, 200, 200), 2)
        
        else:
            cv2.line(self.img, pt1, pt2, (200, 200, 0), 2)

    def showpt(self, pt):
        cv2.circle(self.img, pt, color=[0, 0, 255], radius=3, thickness=3)

    def connectnew(self, pt,closest,tree,planning=50):
        nodesinneigh=[]
        costneigh=[]
        for node1 in self.nodelist[tree]:
            if self.calcdist(node1,pt)<=planning:
                
                nodesinneigh.append(node1)
                costneigh.append(node1.cost+self.calcdist(node1,pt))
        
        if len(nodesinneigh)>0:
            costneighind=np.argsort(costneigh)
            ind=costneighind[0]
            connode=nodesinneigh[ind];

            if (pt[1]-connode.y) == 0:
                m = 10000000000000000
            else:
                m = (pt[0]-connode.x)/(pt[1]-connode.y)

            theta = math.atan(m)
            
            check1=1
            
            for distn in range (int(self.calcdist(connode,pt))):
            
                if (pt[1]-connode.y > 0):
                    xnew = int(connode.x+distn*math.sin(theta))
                    ynew = int(connode.y+distn*math.cos(theta))
                else:
                    xnew = int(connode.x-distn*math.sin(theta))
                    ynew = int(connode.y-distn*math.cos(theta))

                if (self.img[xnew, ynew, 0] >200 and self.img[xnew, ynew, 1] >200 and self.img[xnew, ynew, 2] > 200):
                    check1=0
            
            if check1:
                self.addnode(pt[0], pt[1], connode, tree,self.calcdist(connode,pt))
                self.showedge((pt[1], pt[0]), (connode.y, connode.x), tree)
                self.showpt((pt[1], pt[0]))
                return node(pt[0], pt[1], connode, connode.cost+self.calcdist(connode,pt))    

        else:
            self.addnode(pt[0], pt[1], closest, tree,self.calcdist(closest,pt))
            self.showedge((pt[1], pt[0]), (closest.y, closest.x), tree)
            self.showpt((pt[1], pt[0]))
            return node(pt[0], pt[1], closest, closest.cost+self.calcdist(closest,pt)) 

    def addnodenew(self, closestnode, pt, dist, tree):
        r, c, t = np.shape(self.img)
        if (self.calcdist(closestnode, pt) <= dist):
            return self.connectnew(pt,closestnode,tree)

        else:
            if (pt[1]-closestnode.y) == 0:
                m = 10000000000000000
            else:
                m = (pt[0]-closestnode.x)/(pt[1]-closestnode.y)

            theta = math.atan(m)
            check1=1
            if (pt[1]-closestnode.y > 0):
                xnew = int(closestnode.x+dist*math.sin(theta))
                ynew = int(closestnode.y+dist*math.cos(theta))
            else:
                xnew = int(closestnode.x-dist*math.sin(theta))
                ynew = int(closestnode.y-dist*math.cos(theta))

            if (self.img[xnew, ynew, 0] >=200 and self.img[xnew, ynew, 1] >200 and self.img[xnew, ynew, 2] > 200):
                check1=0
            if (check1 and xnew < r and ynew < c):
                return self.connectnew((xnew,ynew),closestnode,tree)
                
    def showpath(self, node):
        while node.parent != None:
            self.showedge((node.y, node.x), (node.parent.y, node.parent.x), 2)
            node=node.parent

    def rewire(self,currnode,planning,tree):
        for node1 in self.nodelist[tree]:
            if self.calcdist(node1,(currnode.x,currnode.y))<=planning and node1.cost>currnode.cost+self.calcdist(node1,(currnode.x,currnode.y)):
                cv2.line(self.img, (node1.y,node1.x), (node1.parent.y,node1.parent.x), (0, 0, 0), 2)
                self.showedge((node1.y,node1.x),((currnode.y,currnode.x)),tree)
                node1.parent=currnode
                node1.cost=currnode.cost+self.calcdist(node1,(currnode.x,currnode.y))
        
    def terminate(self, node1, dist, tree):
        if tree:
            for node2 in self.nodelist[0]:
                if self.calcdist(node2, (node1.x, node1.y)) <= dist :
                    self.showedge((node1.y, node1.x), (node2.y, node2.x), 2)
                    self.showpath(node2)
                    self.showpath(node1)
                    print("Made path 2 with dist= ",node1.cost+node2.cost)
                    return 0

        else:
            for node2 in self.nodelist[1]:
                if self.calcdist(node2, (node1.x, node1.y)) <= dist :
                    self.showedge((node1.y, node1.x), (node2.y, node2.x), 2)
                    self.showpath(node2)
                    self.showpath(node1)
                    print("Made path 1 with dist= ",node1.cost+node2.cost)
                    return 0

        return 1

    def grow(self, dist, pt, tree):
        planning=50
        closest = self.findclosest(pt, tree)
        addedpt=self.addnodenew(closest, pt, dist, tree)
        if addedpt!=None:
            self.rewire(addedpt,planning,tree)
            check = self.terminate(addedpt, dist, tree)
            
            return check
        return 1

img = cv2.imread("multisourceimg.png", 1)
map = RRTmap(img)
map.findstart()
map.findend()s
cv2.namedWindow('RRT', cv2.WINDOW_NORMAL)
end1 = end2 = 1

while end1 and end2:
    prob=random.random()
    if prob<0.9 or len(map.nodelist[1])==0:
        rand = map.randpt()
        end1 = map.grow(dist, rand, 0)
    else:
        neednode=map.findclosest((map.nodelist[0][0].x,map.nodelist[0][0].y),1)
        end1 = map.grow(dist, (neednode.x,neednode.y), 0)

    if end1==0:
        cv2.imshow("RRT", (map.img).astype(np.uint8))
        cv2.waitKey(0)
        break

    if prob<0.9 or len(map.nodelist[0])==0:
        rand = map.randpt()
        end2 = map.grow(dist, rand, 1)
    else:
        neednode=map.findclosest((map.nodelist[1][0].x,map.nodelist[1][0].y),0)
        end2 = map.grow(dist, (neednode.x,neednode.y), 1)

    cv2.imshow("RRT", (map.img).astype(np.uint8))
    cv2.waitKey(50)

cv2.waitKey(0)
