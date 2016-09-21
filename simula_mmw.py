#!/usr/bin/python
import sys
import math
import random

'''
simulation total time = 5e4 slots
delay threshold = 2e4 slots
traffic load = arrival_rate * 1000 B * nNodes / transmission_rate
'''
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

	def isInside(self, a, b, ret):#returns the beam sector which the node is
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
		if (ret == None):
	   		return sector
		else:
			return dist

def nodebuffer(schedule, node):#, demand, threshold):
	nodebuffer = []
	
	for i in range(len(schedule)):
		slots = 0
		for j in range(1,len(schedule[i])):
			if (schedule[i][j][0] == node):
				for k in range(i):
					slots = slots + schedule[k][0]
					#print slots
				nodebuffer.append([slots, schedule[i][j][1]])
	return nodebuffer


def beamIntersection(nodelist, link1, link2):
	sector10 = nodelist[link1[0]].inInside(nodelist[link1[1]].x,nodelist[link1[1]].y)
	#sectora =  nodelist[link1[0]].inInside(nodelist[link2[0]].x,nodelist[link2[0]].y)
	sectorb =  nodelist[link1[0]].inInside(nodelist[link2[1]].x,nodelist[link2[1]].y)

	#sector11 = nodelist[link1[1]].inInside(nodelist[link1[0]].x,nodelist[link1[0]].y)
	#sectorc =  nodelist[link1[1]].inInside(nodelist[link2[0]].x,nodelist[link2[0]].y)
	#sectord =  nodelist[link1[1]].inInside(nodelist[link2[1]].x,nodelist[link2[1]].y)

	sector20 = nodelist[link2[0]].inInside(nodelist[link2[1]].x,nodelist[link2[1]].y)
	#sectore =  nodelist[link2[0]].inInside(nodelist[link1[0]].x,nodelist[link1[0]].y)
	sectorf =  nodelist[link2[0]].inInside(nodelist[link1[1]].x,nodelist[link1[1]].y)
	'''
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
	'''
	if((sector10 == sectorb) or (sector20 == sectorf)):
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

	#print "edges ->",edges[:]
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
		#print "counter->",counter
		counter = counter+1
		if (colors==[]):
			break
		schedule.append(colors)
		#print colors[:]

		colors = []
	#print schedule
	maximo = 0
	for i in range(len(schedule)):
		maximo = demand[schedule[i][0][0]][schedule[i][0][1]]
		for j in range(1,len (schedule[i])):
			if (demand[schedule[i][j][0]][schedule[i][j][1]] > maximo):
				maximo = demand[schedule[i][j][0]][schedule[i][j][1]]
		schedule[i].insert(0, maximo)

	
	#print "FDMAC ->",schedule
	return schedule
#'''

#funcao de bloqueio ja funciona, so falta dar uma arrumada!
def blockage(nNodes, channel, rate):
	NumBlock = rate *math.pow(nNodes,2)
	visited = []
	#print "Blockage Number ->",NumBlock
	for i in range(nNodes*nNodes):
		visited.append(i)
	#print channel
	while(NumBlock > 0):
		blocked = random.choice(visited)
		#print blocked,
		NumBlock= NumBlock - 1
		visited.remove(blocked)
		i = int(blocked/nNodes)
		j = blocked % nNodes
		channel[i][j] = 0

	#print
	#print channel

#criar brdmacScheduler
def brdmacScheduler(nNodes, demand, channel, nodelist, relayedpkts):
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
	#print copy

	runs = nNodes*nNodes
	#print "channel 2",channel
	#elegendo os relays
	for i in range (0, nNodes):
		temp = []
		for j in range (0, nNodes):
			if ((demand[i][j]!=0)and(channel[i][j]==0)):
				candidates = []
				for k in range(nNodes):
					#print "(",i, j,")", k, 
					#print channel[i][k],channel[k][j]
					if ((channel[i][k] != 0)and(channel[k][j])!=0):
						candidates.append(k)
						#print i,"->",k,"->",j
				temp.append(candidates)
			else:
				temp.append(None)
		relays.append(temp)

	#print "relays ->",relays
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
				temp =[]
				for u in range(len(value)):#linha 9: para cada no candidato a relay...
					Scju = 0
					#para cada aresta que aponta para esse vertice
					for v in range(nNodes):#linha 11
						#print (l*nNodes)+value[k]
						#soma dos pesos das l arestas que incidem sobre o no k
						Scju = Scju + Wc[(v*nNodes)+value[u]]
					temp.append(Scju)
					#end for
					#print temp
				Sc = max(temp)#linha 15
				#print "Sc",Sc
				#end for
				#print
				#print temp.index(Sc), Sc
				#print
				Sjr = 0
				for k in range(nNodes):
					#Sjr = Sjr + Wc[(j*nNodes)+value[k]]
					Sjr=Sjr+Wc[(int(i/nNodes)*nNodes)+k]#linha 17
				#endfor
				#print "Sjr",Sjr
				Mj.append(max(Sjr, Sc))
				copy[i-l+value[j]]=-copy[i]+copy[i-l+value[j]]
			#end for
			#elected[i] = min(Mj)
			#print "temp", temp
			#print "Mj", Mj
			#print int(i/nNodes),l, temp.index(min(Mj))
			elected[i] = relays[int(i/nNodes)][l][Mj.index(min(Mj))]
			#copy[i]=0
			#print relays
			#print "elected",elected[i]
		#endif
		elif ((value != None)and(len(value)==1)):
			elected[i]=value[0]
			#copy[int(i/nNodes)+elected[i]]=copy[int(i/nNodes)+elected[i]]+copy[i]
		elif (value == None):#)or(value==[])):
			elected[i]=None
		i = i+1
	#fim do while

	#print elected
	'''
	print "channel->", channel
	print "demand ->", demand
	print "copy ->", copy
	#print "visited ->", visited
	'''
	
	for i in range(nNodes):
		copy[i]=copy[i*nNodes:i*nNodes+nNodes]
	
	while(len(copy)!=nNodes):
		copy.remove(copy[nNodes])
	#print copy
	
	for i in range(nNodes): temp.append(0)
	for i in range(nNodes):
		for j in range(nNodes): copy[i][j]=0
		for j in range(nNodes):
			if(elected[(i*nNodes) + j] != None):
				copy[i][elected[(i*nNodes) + j]] = copy[i][elected[(i*nNodes) + j]]+demand[i][j]#+demand[i][elected[(i*nNodes) + j]]
				relayedpkts[0] = relayedpkts[0] + demand[i][j]
				copy[i][j]=0
			else:
				copy[i][j]=copy[i][j]+demand[i][j]
	#print copy
		
	
	#FAZER O ESCALONAMENTO!!!
	return fdmacScheduler(nNodes, copy, nodelist)
	'''
	counter = 0
	visited = []
	while (len(visited)<nNodes*nNodes-1):
		counter = counter + 1
		for k in range(runs):
			if (channel[int(k/nNodes)][k%nNodes]!=0):
				#demanda dos enlaces normalizada pela velocidade do enlace
				Wc.append(math.ceil(copy[k]/channel[int(k/nNodes)][k%nNodes]))#linha 7
			else:#preciso disso para nao gerar problemas com divisao por 0
				Wc.append(0)
		Vt = []
		Et = []
		while(len(Et)<math.floor(nNodes/2)):
			eij = Wc.index(max(Wc))
			if(Vt.count(eij)==0):
				Vt.append(eij)
		#fim do while
	'''	

	#print "BRDMAC ->", final
	#return final


#criar funcao que calcula o delay
def delayCalc(nNodes, schedule, demand):
	delay = 0
	pkts = 0
	avg_delay = 0
	for i in range (len(schedule)-1):
		for j in range(i):
			delay= delay + schedule[i][0]#[j][0]

	#for i in range (nNodes):
	#	for j in range(nNodes):
	#		pkts = pkts + demand[i][j]

	avg_delay = delay/len(schedule)#pkts
	return avg_delay

#Gerador de trafego
def poissontraffic(nNodes, rate):
	packets = round(random.random()*10,1)*nNodes/rate*2
	return packets

#criar funcao que calcula a taxa de sucesso
#def deliveryrate (schedule, threshold):
	

#criar funcao que calcula o Jain's fairness Index com relacao ao delay
def fairnessindex(nNodes, resource):
	num = 0
	den = 0
	for i in range(nNodes):
		num = num + resource[i]
		den = den + math.pow(resource[i],2)
	fairness = math.pow(num, 2)/(nNodes*den)
	return fairness

def main():
	
	#Defining Variables
	nNodes = int(sys.argv[1])#10
	areaSize = 10
	nodelist = [];#list of nodes
	random.seed(int(sys.argv[5]))#26)
	load = 0
	charge = float(sys.argv[3])#4.5
	rate = float(sys.argv[4])
	#Randomic Position of the nodes
	for i in range (nNodes):
		nodelist.append(Node(random.randint(0,areaSize),random.randint(0,areaSize), 10))
		nodelist[i].setBeam(int(sys.argv[2]))

	drate_f = 0 #delivery rate fdmac
	drate_b = 0 #delivery rate brdmac
	delayf = 0
	delayb = 0
	threshold = 1.6e4 #limite de permanencia no buffer
	relayedpkts = [0] #Portion of the packets to be relayed

	fdmac = []
	brdmac = []
	buffer_f = []
	buffer_b = []
	avgdelayf = [0 for i in range(nNodes)]
	avgdelayb = [0 for i in range(nNodes)]
	demand = [[0 for i in range(nNodes)] for j in range(nNodes)]
	channel = [[0 for i in range(nNodes)] for j in range(nNodes)]
	copyf = [[0 for i in range(nNodes)] for j in range(nNodes)]
	copyb = [[0 for i in range(nNodes)] for j in range(nNodes)]
	#randomic generation of the traffic and channel
	z = 0
	while(load < 5e4):
		for i in range (0, nNodes):
			for j in range (0, nNodes):
				if (i != j):
					if (nodelist[i].isInside(nodelist[j].x, nodelist[j].y,None)):
						if (nodelist[i].isInside(nodelist[j].x, nodelist[j].y,True) >=7):
							channel[i][j] = 1 #random.randint(1,2)#random.uniform(0, 5)
						else:
							channel[i][j] = 2
						demand[i][j] = poissontraffic(nNodes, channel[i][j])*charge
						#COMO O FDMAC NAO FAZ RELAY, SE NAO ENVIOU UM PACOTE, ELE FICA PARA
						#O PROXIMO SCHEDULING
						copyf[i][j] = copyf[i][j] + demand[i][j]
						copyb[i][j] = demand[i][j]#+copyb[i][j]
						#math.floor(random.uniform(0, 4.5))#*random.uniform(0,channel[i][j]))
						load = load + demand[i][j]
						#print poissontraffic(nNodes, channel[i][j])
	
		blockage(nNodes, channel, rate)#ja funciona!

		fdmac = fdmacScheduler(nNodes, copyf, nodelist)
		brdmac = brdmacScheduler(nNodes, copyb, channel, nodelist, relayedpkts)
		print brdmac
		delayf = delayf + delayCalc(nNodes, fdmac, demand)
		delayb = delayb + delayCalc(nNodes, brdmac, demand)
		
		for n in range(nNodes):
			temp = []
			if(len(buffer_f) < nNodes):
				buffer_f.append(nodebuffer(fdmac,n))
			else:
				temp = nodebuffer(fdmac,n)
				#SE O PACOTER FICOU DA RODADA ANTERIOR INCREMENTAR O BUFFER
				#COM O PREVISTO PARA ESSA RODADA		
				counter = len(temp)
				m = 0
				#print len(buffer_f[n]), len(temp)
				for i in range(len(buffer_f[n])):
					counter = len(temp)
					m=0										
					while(counter > 0):
						#print n, m, i
						if(buffer_f[n][i][1] == temp[m][1]):
							#SE TIVER PACOTE PARA UM DESTINO AINDA NO BUFFER, SOMAR A CAPACIDADE
							buffer_f[n][i][0] = buffer_f[n][i][0] + temp[m][0]
							temp.remove(temp[m])
							counter = counter - 1
						else:
							m = m+1
							counter = counter - 1
				buffer_f[n] = buffer_f[n]+temp

			if(len(buffer_b) < nNodes):
				buffer_b.append(nodebuffer(brdmac,n))
			else:
				temp = nodebuffer(brdmac,n)
				buffer_b[n] = buffer_b[n] + temp
			den = 0
			for i in range(len(buffer_b[n])):
				avgdelayb[n] = avgdelayb[n] + buffer_b[n][i][0]
				den = den + copyb[n][buffer_b[n][i][1]]
			if(den!=0):
				avgdelayb[n] = avgdelayb[n]/den
			
			for i in range(len(buffer_f[n])):
				avgdelayf[n] = avgdelayf[n] + buffer_f[n][i][0]
				den = den + copyf[n][buffer_f[n][i][1]]
			if(den!=0):
				avgdelayf[n] = avgdelayf[n]/den
		print buffer_b
		for n in range(nNodes):
			for m in range(nNodes):
				if (channel[n][m]!=0):
					#SE O PACOTE PODE SER ENVIADO ELE NAO INFLUENCIA NO PROXIMO SCHEDULING
					copyf[n][m]=0	

		for n in range(nNodes):
			counter = len(buffer_f[n])
			m = 0
			while(counter>0):
				if(copyf[n][buffer_f[n][m][1]] == 0):
					#PACOTE ENVIADO, LIMPAR O BUFFER
					buffer_f[n].remove(buffer_f[n][m])
					counter = counter -1
				else:
					m = m + 1
					counter = counter -1

		for n in range(nNodes):
			counter = len(buffer_b[n])
			m = 0
			while(counter>0):
				if(copyf[n][buffer_b[n][m][1]] == 0):
					#PACOTE ENVIADO, LIMPAR O BUFFER
					buffer_b[n].remove(buffer_b[n][m])
					counter = counter -1
				else:
					m = m + 1
					counter = counter -1

		for n in range(nNodes):
			counter = len(buffer_f[n])
			m = 0
			while(counter>0):
				#SE O PACOTE FICOU NO BUFFER POR MUITO TEMPO ELE E DESCARTADO
				if (buffer_f[n][m][0]>threshold):
					#DIMINUI A TAXA DE ENTREGA
					drate_f = drate_f + copyf[n][buffer_f[n][m][1]]
					#DESCARTA
					copyf[n][buffer_f[n][m][1]]=0
					#REMOVE DO BUFFER
					buffer_f[n].remove(buffer_f[n][m])
					counter = counter -1
				else:
					m = m + 1
					counter = counter -1

		for n in range(nNodes):
			counter = len(buffer_b[n])
			m = 0
			while(counter>0):
				if (buffer_b[n][m][0]>threshold):
					drate_b = drate_b + copyb[n][buffer_b[n][m][1]]
					copyb[n][buffer_b[n][m][1]]=0
					buffer_b[n].remove(buffer_b[n][m])
					counter = counter -1
				else:
					m = m + 1
					counter = counter -1

		z = z+1

	for i in range(nNodes):
		avgdelayb[i] = avgdelayb[i]/z
		avgdelayf[i] = avgdelayf[i]/z

	print avgdelayb,"\n",avgdelayf

	drate_b = (load - drate_b)/load
	drate_f = (load - drate_f)/load
	relayedpkts[0] = relayedpkts[0]/load
	delayf = delayf/z
	delayb = delayb/z
	
	print drate_b
	print drate_f
	print relayedpkts[0]
	print delayf
	print delayb
	print fairnessindex(nNodes, avgdelayb)
	print fairnessindex(nNodes, avgdelayf)
		
if __name__ == "__main__":
    sys.exit(main())
