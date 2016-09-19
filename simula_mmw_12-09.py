#!/usr/bin/python
import sys
import math
import random

pi = 3.14159265

class Node:
	#def __init__(self):
	def __init__(self, a, b, r):
		self.x = a
		self.y = b
		self.radius = r

	def setBeam (self, n):
		self.nBeams = n
	#fica ou nao?
	def setRf(self, gain, thr, ptx):
		self.antennaGain = gain
		self.rxThreshold = thr
		self.txPower = ptx

	def beamAperture(self):#returns the angle of each beam
		return 2*pi/self.nBeams

	def isInside(self, a, b):#returns the beam sector which the node is
		#Euclidian distance between the nodes
		dist = math.hypot(abs(self.x-a), abs(self.y-b))
		if (dist > self.radius):
			return None
		else:
			#angle in the correct quadrant
			angle = math.atan2(b - self.y, a - self.x)
			if (angle < 0):
			    angle = (2*pi) + angle
			sector = int(angle/self.beamAperture())
	   	return sector


def beamIntersection(nodelist, link1, link2):
	sector10 = nodelist[link1[0]].inInside(nodelist[link1[1]].x,nodelist[link1[1]].y)
	sectora =  nodelist[link1[0]].inInside(nodelist[link2[0]].x,nodelist[link2[0]].y)
	sectorb =  nodelist[link1[0]].inInside(nodelist[link2[1]].x,nodelist[link2[1]].y)

	sector11 = nodelist[link1[1]].inInside(nodelist[link1[0]].x,nodelist[link1[0]].y)
	sectorc =  nodelist[link1[1]].inInside(nodelist[link2[0]].x,nodelist[link2[0]].y)
	sectord =  nodelist[link1[1]].inInside(nodelist[link2[1]].x,nodelist[link2[1]].y)

	sector20 = nodelist[link2[0]].inInside(nodelist[link2[1]].x,nodelist[link2[1]].y)
	sectore =  nodelist[link2[0]].inInside(nodelist[link1[0]].x,nodelist[link1[0]].y)
	sectorf =  nodelist[link2[0]].inInside(nodelist[link1[1]].x,nodelist[link1[1]].y)

	sector21 = nodelist[link2[1]].inInside(nodelist[link2[0]].x,nodelist[link2[0]].y)
	sectorg =  nodelist[link2[1]].inInside(nodelist[link1[0]].x,nodelist[link1[0]].y)
	sectorh =  nodelist[link2[1]].inInside(nodelist[link1[1]].x,nodelist[link1[1]].y)

	if((sector10 == sectora) or (sector10 == sectorb)):
		return True
	elif((sector11 == sectorc) or (sector11 == sectord)):
		return True
	elif((sector20 == sectore) or (sector20 == sectorf)):
		return True
	elif((sector21 == sectorg) or (sector21 == sectorh)):
		return True

	return False
#'''
def fdmacScheduler(nNodes, demand, nodelist):
	copy = []#demand sorted in a non-increrasing way
	edges = []#links already scheduled
	for i in range (0, nNodes):
		for j in range (0, nNodes):
			copy.append(demand[i][j])
			#visited.append()

	copy.sort(reverse=True)
	runs = int(math.pow(nNodes,2))
	#print copy[:]
	counter = 0
	for k in range(counter, runs):
		if (copy[k]>0):
			for i in range(nNodes):
				for j in range(nNodes):
					if(demand[i][j] == copy[k]):
						counter = counter +1
						try:
							edges.index([i,j])
						except:
							edges.append([i, j])
						else:
							pass

	print "edges ->",edges[:]
	schedule = []
	colors = []
	visited = []
	for i in range (nNodes):
		visited.append(0)
	#print len(edges)
	half = int(nNodes/2)
	counter = 0;
	while(counter < runs):#len(edges)>0):
		for i in range (nNodes):
			#print 'entrou'
			visited[i]=0
		for i in range(counter,len(edges)):
			#print "i",i
			#print visited
			if((visited[edges[i][0]]==0)and(visited[edges[i][1]]==0)and(edges[i]!=[0,0])):
				#print "entrei no maldito if"
				visited[edges[i][0]]=1
				visited[edges[i][1]]=1
				colors.append([edges[i][0],edges[i][1]])
				edges.remove([edges[i][0],edges[i][1]])
				edges.insert(i,[0,0])
		print "counter->",counter
		counter = counter+1
		if (colors==[]):
			break
		schedule.append(colors)
		print colors[:]

		colors = []
	#print schedule
	maximo = 0
	for i in range(len(schedule)):
		maximo = demand[schedule[i][0][0]][schedule[i][0][1]]
		for j in range(1,len (schedule[i])):
			if (demand[schedule[i][j][0]][schedule[i][j][1]] > maximo):
				maximo = demand[schedule[i][j][0]][schedule[i][j][1]]
		schedule[i].insert(0, maximo)
	print "schedule ->",schedule
#'''

#funcao de bloqueio ja funciona, so falta dar uma arrumada!
def blockage(nNodes, channel, rate):
	NumBlock = rate *math.pow(nNodes,2)
	visited = []
	#print "Blockage Number ->",NumBlock
	for i in range(nNodes*nNodes):
		visited.append(i)
	print channel
	while(NumBlock > 0):
		blocked = random.choice(visited)
		print blocked,
		NumBlock= NumBlock - 1
		visited.remove(blocked)
		i = int(blocked/nNodes)
		j = blocked % nNodes
		channel[i][j] = 0

	print
	print channel

#criar brdmacScheduler
def brdmacScheduler(nNodes, demand, channel, nodelist):
	copy = []
	edges = []
	visited = []
	relays = []
	candidates = []
	elected = []
	for i in range (0, nNodes):
		for j in range (0, nNodes):
			copy.append(demand[i][j])
			visited.append(0)
			elected.append(0)
	print copy

	runs = nNodes*nNodes
	#elegendo os relays
	for i in range (0, nNodes):
		temp = []
		for j in range (0, nNodes):
			if ((demand[i][j]!=0)and(channel[i][j]==0)):
				candidates = []
				for k in range(nNodes):
					if ((channel[i][k] != 0)and(channel[k][j])!=0):
						candidates.append(k)
						print i,"->",k,"->",j
				temp.append(candidates)
			else:
				temp.append(None)
		relays.append(temp)

	print "relays ->",relays
	#copy.sort(reverse=True)#ainda nao preciso ordenar de forma nao crescente
	Scju = []
	i = 0
	Wc = []
	temp = []
	#Alterar o peso das arestas
	while(visited.count(0)>0):
		visited.remove(0)
		visited.insert(i, 1)
		Mj = []
		l = i%nNodes
		value = relays[int (i/nNodes)][l]
		if ((value != None)and(len(value)>1)): #se numero de relays > 1...
			for j in range(len(value)):#linha 4
				#print i+value[j],
				#se j eh candidato a relay do enlace i-l, entao a demanda de
				#j passa a ser, w_ij+w_il
				copy[i-l+value[j]]=copy[i]+copy[i-l+value[j]]

				#botei esse bloco pra dentro v
				#copy[i] = 0
				#print
				Wc = []
				for k in range(runs):
					if (channel[int(k/nNodes)][k%nNodes]!=0):
						#demanda dos enlaces normalizada pela velocidade do enlace
						Wc.append(math.ceil(copy[k]/channel[int(k/nNodes)][k%nNodes]))#linha 7
					else:#preciso disso para nao gerar problemas com divisao por 0
						Wc.append(0)
				#endfor

				#print "Wc ->", Wc
				for u in range(len(value)):#linha 9: para cada no candidato a relay...
					Scju = 0
					#para cada aresta que aponta para esse vertice
					for v in range(nNodes):#linha 11
						#print (l*nNodes)+value[k]
						#soma dos pesos das l arestas que incidem sobre o no k
						Scju = Scju + Wc[(v*nNodes)+value[u]]
					temp.append(Scju)
					#end for
				Sc = max(temp)#linha 15
				#end for
				#print
				#print temp.index(Sc), Sc
				#print
				Sjr = 0
				for k in range(nNodes):
					#Sjr = Sjr + Wc[(j*nNodes)+value[k]]
					Sjr=Sjr+Wc[(int(i/nNodes)*nNodes)+k]#linha 17
				#endfor
				Mj.append(max(Sjr, Sc))
				#end for
			elected[i] = Mj.index(min(Mj))
		#endif
		elif ((value != None)and(len(value)==1)):
			elected[i]=value
		elif (value == None):
			elected[i]=None
		i = i+1
	#fim do while

	print elected
	print "copy ->", copy
	print "visited ->", visited

#criar minha funcao: daviSinistroSchedule()

#criar funcao que calcula o delay

#criar funcao que calcula a taxa de sucesso

#criar funcao que calcula o Jain's fairness Index

def main():
	#Defining Variables
	nNodes = 11
	areaSize = 10
	nodelist = [];#list of nodes
	random.seed(26)
	#Randomic Position of the nodes
	for i in range (nNodes):
		nodelist.append(Node(random.randint(0,areaSize),random.randint(0,areaSize), 10))
		nodelist[i].setBeam(4)


	demand = [[0 for i in range(nNodes)] for j in range(nNodes)]
	channel = [[0 for i in range(nNodes)] for j in range(nNodes)]
	#randomic generation of the traffic and channel
	for i in range (0, nNodes):
		for j in range (0, nNodes):
			if (i != j):
				if (nodelist[i].isInside(nodelist[j].x, nodelist[j].y)):
					channel[i][j] = random.randint(0,5)#random.uniform(0, 5)
					demand[i][j] = math.floor(random.uniform(0, 4.5))#*random.uniform(0,channel[i][j]))

	print "demand",demand[:][:]
	print "channel", channel

	#blockage(nNodes, channel, 0.5)#ja funciona!

	fdmacScheduler(nNodes, demand, nodelist)
	brdmacScheduler(nNodes, demand, channel, nodelist)


if __name__ == "__main__":
    sys.exit(main())
