# python3 readInput.py A-VRP/A-n33-k5.vrp 

import sys
import math
import copy
import time
from itertools import permutations
class graphDetails:
	totalVertices = -1
	capacity = -1
	depot = -1
	minimumVehicle = -1
	obtimalCost = -1

class vertex:
	def __init__(self,vertex_id,x,y):
		self.vertex_id = vertex_id
		self.x = x
		self.y = y
		self.capacity = -1
		self.angle=-1
		
def readInput(G,inputFile,vertexCoordinates):
	# reading minimum vehicle and optimal cost
	inputFileList = inputFile.readlines()

	dataFirstLine = []
	#rptint(inputFileList)
	currLine = inputFileList[1].split()
	for i in currLine:
		i = i.strip(',')
		i = i.strip(')')
		if(i.isdigit()):
			dataFirstLine.append(i)
	#print(int(dataFirstLine[0]+" "+dataFirstLine[1]))
	G.minimumVehicle = int(dataFirstLine[0])
	G.obtimalCost = int(dataFirstLine[1])
	
	# obtained minimum vehicle and optimal cost

	#reading capacity
	currLine = inputFileList[5].split()
	for i in currLine:
		if(i.isdigit()):
			dataFirstLine.append(i) 

	G.capacity = int(dataFirstLine[2])
	#obtained capacity

	#removing all the header text in the data file
	inputFileList = inputFileList[7:]
	
	#reading coordinates of stops
	for i in inputFileList:
		if(i.split()[0]=="DEMAND_SECTION"):
			break	
		curr = i.split()
		currId = int(curr[0])
		currX = int(curr[1])
		currY = int(curr[2])
		currVertex = vertex(currId,currX,currY)
		vertexCoordinates[currId] = currVertex #map with key as vertexId and value is the vertex

	inputFileList = inputFileList[len(vertexCoordinates)+1:]

	#obtained all the vertices and its coordinates
	
	#reading capacity for all vertices

	for i in inputFileList:
		if(i.split()[0]=="DEPOT_SECTION"):
			break
		curr = i.split()
		vertexCoordinates[int(curr[0])].capacity = int(curr[1])

	#capacity obtained
	inputFileList=inputFileList[-3:]
	G.depot=int(inputFileList[0])

def getAngle(angle,G,vertexCoordinates):
	#print("finding angle")
	print("angle")
	x1=vertexCoordinates[G.depot].x
	y1=vertexCoordinates[G.depot].y
	print(str(x1)+" "+str(y1))
	for i in vertexCoordinates:
		id=vertexCoordinates[i].vertex_id
		x2=vertexCoordinates[i].x
		y2=vertexCoordinates[i].y
		a=math.atan2(y2-y1,x2-x1)
		b=math.degrees(a)
		if(b<0):
			b=360+b
		angle[id]=b

def getDistance(distance,G,vertexCoordinates):
	print("distance")
	x1=vertexCoordinates[G.depot].x
	y1=vertexCoordinates[G.depot].y
	print(str(x1)+" "+str(y1))
	for i in vertexCoordinates:
		id=vertexCoordinates[i].vertex_id
		x2=vertexCoordinates[i].x
		y2=vertexCoordinates[i].y
		a=math.sqrt((x2-x1)**2+(y2-y1)**2)
		#print(a)
		distance[id]=a

def obtainapsp(allpairpathlength,vertexCoordinates):
	for i in vertexCoordinates:
		x1=vertexCoordinates[i].x
		y1=vertexCoordinates[i].y
		id1=vertexCoordinates[i].vertex_id
		for j in vertexCoordinates:
			x2=vertexCoordinates[j].x
			y2=vertexCoordinates[j].y
			if x1!=x2 or y1!=y2:
				id2=vertexCoordinates[j].vertex_id
				a=math.sqrt((x2-x1)**2+(y2-y1)**2)
				allpairpathlength[str(id1)+"_"+str(id2)]=a

def getInitialSolution(res,G,vertexCoordinates,path,allpairpathlength):
	print("initial Solution")
	path1={}
	Veh_Cap=G.capacity
	print("vehicle capacity =",type(Veh_Cap))
	prev=res[0][0]
	# for i in vertexCoordinates:
	# 	print(i)
	n=(len(res))
	# create string1
	s=[]
	spl=[]
	pathlength=0
	# s.append(prev)
	for i in range(1,n):
		# print(pathlength,allpairpathlength[(str(prev)+"_"+str(res[i][0]))])
		# print(type(vertexCoordinates[res[i][0]].capacity))
		if(vertexCoordinates[res[i][0]].capacity<=Veh_Cap):
			s.append(res[i][0])
			pathlength=pathlength+allpairpathlength[(str(prev)+"_"+str(res[i][0]))]
			prev=res[i][0]
			# print(pathlength)
			# print(res[i][1][1])
			# append node in string1
			Veh_Cap = Veh_Cap-vertexCoordinates[res[i][0]].capacity
		else:
			pathlength=pathlength+allpairpathlength[(str(prev)+"_"+str(res[0][0]))]
			# s.append(res[0][0])
			prev=res[0][0]
			# print(s)
			# print(pathlength)
			spl.append(s)
			# print(type(s))
			spl.append(pathlength)
			spl.append(G.capacity-Veh_Cap)
			# print(type(spl[0][0]))
			path.append(spl)
			spl=[]
			# print(path)
			s=[]
			# print(s)
			# print(pathlength)
			pathlength=0
			# s.append(res[0][0])
			s.append(res[i][0])
			# append last vertex to string1-> append string1 to list-> make String1 empty and append first vertex-> append starting index to string-> append next vertex to string-> make veh_cap to G.capacity->reduce size of Veh_cap by capacity of current vertex
			Veh_Cap=G.capacity
			Veh_Cap=Veh_Cap-vertexCoordinates[res[i][0]].capacity
	if(s!=str(prev)):
		pathlength=pathlength+allpairpathlength[(str(prev)+"_"+str(res[0][0]))]
		# s.append(res[0][0])
		# path.append(s)
		spl.append(s)
		spl.append(pathlength)
		spl.append(G.capacity-Veh_Cap)
		path.append(spl)

 		
def sss(G,path,sum,allpairpathlength,count):
	# print(count)
	if count == 0:
		return path,sum

	path1=list(path)
	pathcp1=list(path)
	sumcp1=sum
	for i in range(0,len(path1)-1):
		path1[i],path1[i+1]=path1[i+1],path1[i]
		sum1=interpathswapcost(G,path1,allpairpathlength)
		if(sumcp1>sum1):
			sumcp1=sum1
			pathcp1=path1
		if(sum1<sum):
			# print(i," ",end="")
			# print(sum,sum1)
			p1,s1=sss(G,path1,sum1,allpairpathlength,count)
		else:
			p1,s1=sss(G,path1,sum1,allpairpathlength,count-1)
		if(s1<sumcp1):
			pathcp1=p1
			sumcp1=s1
		path1[i],path1[i+1]=path1[i+1],path1[i]
	# print(pathcp1,sumcp1)
	return pathcp1,sumcp1
		# else:
		# 	sss(G,path)
	# permutations_path = permutations(path)
	# sumloc=0
	# prev=G.depot
	# # print(sum)
	# # print(permutations_path)
	# for i in permutations_path:
	# 	# print(type(i))
	# 	prev=G.depot
	# 	sumloc=0
	# 	for j in i:
	# 		sumloc=sumloc+allpairpathlength[str(prev)+"_"+str(j)]
	# 		prev=j
	# 	sumloc=sumloc+allpairpathlength[str(prev)+"_"+str(G.depot)]
	# 	# print(sumloc)
	# 	if(sumloc<sum):
	# 		# print(sumloc)
	# 		# print(sum,sumloc)
	# 		sum=sumloc
	# 		path=list(i)
	# 		# print(path)
	# # print(type(path))
	# return path,sum
def interpathswapcost(G,path,allpairpathlength):
	prev=G.depot
	sumloc=0
	for j in path:
		sumloc=sumloc+allpairpathlength[str(prev)+"_"+str(j)]
		prev=j
	sumloc=sumloc+allpairpathlength[str(prev)+"_"+str(G.depot)]
	return sumloc	
def InterPathSwap(G,path1,pathlength1,capacity1,path2,pathlength2,capacity2,vertexCoordinates,allpairpathlength):
	# print("HI")
	path1cp=list(path1)
	path2cp=list(path2)
	pathres1=list(path1)
	lenres1=pathlength1
	capres1=capacity1
	pathres2=list(path2)
	lenres2=pathlength2
	capres2=capacity2
	for i in range(0,len(path1cp)):
		for j in range(0,len(path2cp)):
			# print(capacity1-vertexCoordinates[path1cp[i]].capacity+vertexCoordinates[path2cp[j]].capacity,capacity2+vertexCoordinates[path1cp[i]].capacity-vertexCoordinates[path2cp[j]].capacity)
			if( capacity1-vertexCoordinates[path1cp[i]].capacity+vertexCoordinates[path2cp[j]].capacity<=G.capacity):
				if(capacity2+vertexCoordinates[path1cp[i]].capacity-vertexCoordinates[path2cp[j]].capacity<=G.capacity):
					path1cp[i],path2cp[j]=path2cp[j],path1cp[i]
					a1=list(path1cp)
					c1=capacity1-vertexCoordinates[path1cp[i]].capacity+vertexCoordinates[path2cp[j]].capacity
					b1=interpathswapcost(G,path1cp,allpairpathlength)
					a2=list(path2cp)
					c2=capacity2+vertexCoordinates[path1cp[i]].capacity-vertexCoordinates[path2cp[j]].capacity
					b2=interpathswapcost(G,path2cp,allpairpathlength)
					# print(path1,path2,pathlength1,pathlength2)
					# print(pathres1,pathres2,b1,b2)
					# print(c1,c2,G.capacity)
					if(b1+b2<lenres1+lenres2 and c1<G.capacity and c2<G.capacity):
						lenres1=b1
						lenres2=b2
						pathres1=a1
						pathres2=a2
						capres1=c1
						capres2=c2
						# print(pathres1,pathres2)

					path1cp[i],path2cp[j]=path2cp[j],path1cp[i]
				# print(path1cp,path2cp)
	if(pathres1 != path1 or pathres2!=path2 and lenres1<pathlength1 and lenres2<pathlength2):
		return pathres1,pathres2,lenres1,lenres2,capres1,capres2,1
		print(path1,path2,pathlength1,pathlength2)
		print(pathres1,pathres2,b1,b2)
	return path1,path2,pathlength1,pathlength2,capacity1,capacity2,0
		#  compare each swap
		# 	call sss
		# 	compare result is less than origial swap
		# inbuilt function for swap of one element in two list.
def InterPathMove(G,path1,pathlength1,capacity1,path2,pathlength2,capacity2,vertexCoordinates,allpairpathlength):
	# print("bye")
	path1cp=list(path1)
	path2cp=list(path2)
	pathres1=list(path1)
	lenres1=pathlength1
	capres1=capacity1
	pathres2=list(path2)
	lenres2=pathlength2
	capres2=capacity2
	for j in range(0,len(path2cp)):
		if capacity1+vertexCoordinates[path2cp[j]].capacity<G.capacity:
			a1=path1cp.append(path2cp[j])
			a2=list(path2cp)
			a2=a2.pop(j)
			c1=capacity1+vertexCoordinates[path2cp[j]].capacity
			c2=capacity2- vertexCoordinates[path2cp[j]].capacity
			a1,b1=sss(G,path1,pathlength1,allpairpathlength)
			a2,b2=sss(G,path2,pathlength2,allpairpathlength)
			if(b1+b2<lenres1+lenres2 and c1<G.capacity and c2<G.capacity):
				lenres1=b1
				lenres2=b2
				pathres1=a1
				pathres2=a2
				capres1=c1
				capres2=c2
	if(pathres1 != path1 or pathres2!=path2 and lenres1<pathlength1 and lenres2<pathlength2):
		return pathres1,pathres2,lenres1,lenres2,capres1,capres2,1
		print(path1,path2,pathlength1,pathlength2)
		print(pathres1,pathres2,b1,b2)
	return path1,path2,pathlength1,pathlength2,capacity1,capacity2,0
	
def InterPathMove1(G,path1,pathlength1,capacity1,path2,pathlength2,capacity2,vertexCoordinates,allpairpathlength):
	# print("bye")
	path1cp=list(path1)
	path2cp=list(path2)
	pathres1=list(path1)
	lenres1=pathlength1
	capres1=capacity1
	pathres2=list(path2)
	lenres2=pathlength2
	capres2=capacity2
	for j in range(0,len(path2cp)):
		if capacity1+vertexCoordinates[path2cp[j]].capacity<G.capacity:
			# print("hello")
			n=len(path1cp)
			val=path2cp[j]
			for i in range(0,n):
				# print("dkdk")
				a1=list(path1cp)
				a1=path1cp.insert(i,val)
				a2=list(path2cp)
				a2=a2.pop(j)
				c1=capacity1+vertexCoordinates[path2cp[j]].capacity
				c2=capacity2- vertexCoordinates[path2cp[j]].capacity
				b1=interpathswapcost(G,path1,allpairpathlength)
				b2=interpathswapcost(G,path2,allpairpathlength)
				if(b1+b2<lenres1+lenres2 and c1<G.capacity and c2<G.capacity):
					# print("dkdk")
					lenres1=b1
					lenres2=b2
					pathres1=a1
					pathres2=a2
					capres1=c1
					capres2=c2
	if(pathres1 != path1 or pathres2!=path2 and lenres1<pathlength1 and lenres2<pathlength2):
		return pathres1,pathres2,lenres1,lenres2,capres1,capres2,1
		print(path1,path2,pathlength1,pathlength2)
		print(pathres1,pathres2,b1,b2)
	return path1,path2,pathlength1,pathlength2,capacity1,capacity2,0
	
def optimize(G,path,allpairpathlength,vertexCoordinates):
	sum=0
	t0= time.time()
	for i in path:
		# print(i[0],i[1])
		p=1
		# while p==1:
			# p,i[0],i[1]=
		i[0],i[1]=sss(G,i[0],i[1],allpairpathlength,2)
		# print(i)
		sum=sum+i[1]
	
	# print(type(path[0][0]),type(path[1][0]))
	a=1
	while(a):
		a=0
		for i in range(0,len(path)):
			if(i==len(path)-1):
				# print("last ",end="")
				# print(type(path[i][0]),type(path[0][0]))
				path[i][0],path[0][0],path[i][1],path[0][1],path[i][2],path[0][2],b=InterPathSwap(G,path[i][0],path[i][1],path[i][2],path[0][0],path[0][1],path[0][2],vertexCoordinates,allpairpathlength)
			else:
				path[i][0],path[i+1][0],path[i][1],path[i+1][1],path[i][2],path[i+1][2],b=InterPathSwap(G,path[i][0],path[i][1],path[i][2],path[i+1][0],path[i+1][1],path[i+1][2],vertexCoordinates,allpairpathlength)
			a=a or b
		# interpath move without intra approach:
	# a=1
	# while(a):
	# 	a=0
	# 	for i in range(0,len(path)):
	# 		if(i==len(path)-1):
	# 			# print("last ",end="")
	# 			# print(type(path[i][0]),type(path[0][0]))
	# 			# path[i][0],path[0][0],path[i][1],path[0][1],b=
	# 			path[i][0],path[0][0],path[i][1],path[0][1],path[i][2],path[0][2],b=InterPathMove1(G,path[i][0],path[i][1],path[i][2],path[0][0],path[0][1],path[0][2],vertexCoordinates,allpairpathlength)
	# 			path[0][0],path[i][0],path[0][1],path[i][1],path[0][2],path[i][2],b=InterPathMove1(G,path[0][0],path[0][1],path[0][2],path[i][0],path[i][1],path[i][2],vertexCoordinates,allpairpathlength)
	# 		else:
	# 			# path[i][0],path[i+1][0],path[i][1],path[i+1][1],b=
	# 			path[i][0],path[i+1][0],path[i][1],path[i+1][1],path[i][2],path[i+1][2],b=InterPathMove1(G,path[i][0],path[i][1],path[i][2],path[i+1][0],path[i+1][1],path[i+1][2],vertexCoordinates,allpairpathlength)
	# 			path[i+1][0],path[i][0],path[i+1][1],path[i][1],path[i+1][2],path[i][2],b=InterPathMove1(G,path[i+1][0],path[i+1][1],path[i+1][2],path[i][0],path[i][1],path[i][2],vertexCoordinates,allpairpathlength)
	# 		a=a or b
	t1= time.time()
	print(t1-t0)
		# print(i[0],i[1])
			# print(i[0],i[1])
	# print(sum)
	# sum1=0
	# for i in path:
	# 	sum1=sum1+i[1]
	# print(sum1)

	# print(sum)
def obtainPath(res,G,vertexCoordinates,path,allpairpathlength):
	path1={}
	path2={}
	# print(G.capacity)
	getInitialSolution(res,G,vertexCoordinates,path,allpairpathlength)
	# for i in path:
	#  	print(i)
	sum=0
	for i in path:
		sum+=i[1]
		for j in range(0,len(i[0])):
			print(i[0][j]," ",end="")
			# sum=sum+allpairpathlength[(str(i[0][j])+"_"+str(i[0][j+1]))]
		# print(sum)
		print(i[1],sum,i[2])
	print()
	optimize(G,path,allpairpathlength,vertexCoordinates)
	sum=0
	for i in path:
		sum+=i[1]
		for j in range(0,len(i[0])):
			print(i[0][j]," ",end="")
		print(i[1],sum,i[2])
			# sum=sum+allpairpathlength[(str(i[0][j])+"_"+str(i[0][j+1]))]
		# print()
	# print(path)
def getDistanceAngle(distanceAngle,G,vertexCoordinates):
	print("distanceAngle")
	x1=vertexCoordinates[G.depot].x  #should write vertexCoordinates[G.depot] the depot need not always be 1
	y1=vertexCoordinates[G.depot].y
	print(str(x1)+" "+str(y1))
	for i in vertexCoordinates:
		id=vertexCoordinates[i].vertex_id
		x2=vertexCoordinates[i].x
		y2=vertexCoordinates[i].y
		a=math.atan2(y2-y1,x2-x1)
		b=math.degrees(a)
		if(b<0):
			b=360+b
		#angle[id]=b

		d=math.sqrt((x2-x1)**2+(y2-y1)**2)
		#print(a)
		#distance[id]=d
		distanceAngle[id]=[b,d]

def main():
	inputFile = open(sys.argv[1],"r")
	vertexCoordinates = {}
	G = graphDetails()
	readInput(G,inputFile,vertexCoordinates)
	print("Minimum Vehicle = "+str(G.minimumVehicle)+" Obtimal Cost = "+str(G.obtimalCost)+" Capacity = "+str(G.capacity))
	print(str(vertexCoordinates[2].x)+" "+str(vertexCoordinates[2].y))
	print(str(G.depot))
	angle={}
	getAngle(angle,G,vertexCoordinates)
	# for i in angle:
	#  	print(angle[i])
	# for i in vertexCoordinates:
	# 	print("Vertex Id = "+str(vertexCoordinates[i].vertex_id)+" x = "+str(vertexCoordinates[i].x)+" y = "+str(vertexCoordinates[i].y)+" capacity = "+str(vertexCoordinates[i].capacity))
	

	distance = {}
	# getDistance(distance,G,vertexCoordinates)
	# for i in distance:
	#  	print(distance[i])
	distanceAngle={} #distance angle is dictionary where key is vertex id and value is (angle,distance)
	getDistanceAngle(distanceAngle,G,vertexCoordinates)
	# for i in distanceAngle:
	# 	print(distanceAngle[i])
	
	res = sorted(distanceAngle.items(), key = lambda kv:(kv[1][0], kv[1][1])) #res is a list with res[0] is vertex id, res[1][0] and res[1][1] is angle and distance wrt to depot
	print("Sorted from here")
	# print(res)
	# for i in res:
	#    	print(i)
	allpairpathlength={}
	obtainapsp(allpairpathlength, vertexCoordinates)
	# for i in allpairpathlength:
		# print(allpairpathlength[i])
		# print(i)
	path=[]
	obtainPath(res,G,vertexCoordinates,path,allpairpathlength) #take parameter as required

main()

	# for i in path:
		# 	print(i)
	# interpath move with intra approach:
	# a=1
	# while(a):
	# 	a=0
	# 	for i in range(0,len(path)):
	# 		if(i==len(path)-1):
	# 			print("last ",end="")
	# 			# print(type(path[i][0]),type(path[0][0]))
	# 			# path[i][0],path[0][0],path[i][1],path[0][1],b=
	# 			path[i][0],path[0][0],path[i][1],path[0][1],path[i][2],path[0][2],b=InterPathMove(G,path[i][0],path[i][1],path[i][2],path[0][0],path[0][1],path[0][2],vertexCoordinates,allpairpathlength)
	# 			path[0][0],path[i][0],path[0][1],path[i][1],path[0][2],path[i][2],b=InterPathMove(G,path[0][0],path[0][1],path[0][2],path[i][0],path[i][1],path[i][2],vertexCoordinates,allpairpathlength)
	# 		else:
	# 			# path[i][0],path[i+1][0],path[i][1],path[i+1][1],b=
	# 			path[i][0],path[i+1][0],path[i][1],path[i+1][1],path[i][2],path[i+1][2],b=InterPathMove(G,path[i][0],path[i][1],path[i][2],path[i+1][0],path[i+1][1],path[i+1][2],vertexCoordinates,allpairpathlength)
	# 			path[i+1][0],path[i][0],path[i+1][1],path[i][1],path[i+1][2],path[i][2],b=InterPathMove(G,path[i+1][0],path[i+1][1],path[i+1][2],path[i][0],path[i][1],path[i][2],vertexCoordinates,allpairpathlength)
	# 		a=a or b
