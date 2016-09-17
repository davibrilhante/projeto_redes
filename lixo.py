    node1 = Node(1, 1, 10)
    node1.setBeam(4)
    print node1.beamAperture()
    print node1.x, ",", node1.y,"=>", node1.radius

    node2 = Node(2, 2, 10)
    node2.setBeam(8)
    print node2.beamAperture()
    print node2.x, ",", node2.y,"=>", node2.radius

    print "2 esta no setor",node1.isInside(node2.x,node2.y),"de 1"#*(180/pi)
    print "1 esta no setor",node2.isInside(node1.x,node1.y),"de 2"#*(180/pi)




	print copy[:]
	i = 0
	runs = math.pow(nNodes,2)
	repeat = 0
	row = 0
	column = 0

	while(i<runs):
		if (copy[i]!= 0):
			if (copy[i]!=copy[i-1]):
				repeat = 0
				column = nNodes
				row = nNodes

			for j in range(row):
				for k in range(column):
					if (demand[j][k] == copy[i]):
						row = j
						column = k
						repeat=repeat+1
						print repeat
					else:
						1
			visited.append([row,column])
			#print i
			print visited[i]
		i = i + 1


			if((schedule[i][0]!=visited[i][0])and(schedule[i][1]!=visited[i][1])):



 #if(edges[i][0])and(edges[i][1])
			try:
				((schedule.index(edges[i][0]))and(schedule.index(edges[i][0])))
			except:
				visited[i]=1

				print 'ok'
			else:
				pass


#Acho que Nao preciso disso
'''
def linkCreator (nNodes, links):
    for i in range(nNodes):
		links.append(i)
    random.shuffle(links)
    return links
'''




def brdmacScheduler(nNodes, demand, channel, nodelist):
	copy = []
	edges = []
	visited = []
	relays = []

	for i in range (0, nNodes):
		for j in range (0, nNodes):
			copy.append(demand[i][j])
			visited.append(0)

	#elegendo os relays
	for i in range (0, nNodes):
		temp = []
		for j in range (0, nNodes):
			if ((demand[i][j]!=0)and(channel[i][j]==0)):
				for k in range(nNodes):
					if ((channel[i][k] != 0)and(channel[k][j])!=0):
						temp.append(k)
						print i,"->",k,"->",j
					#else:
						#temp.append(0)
			else:
				temp.append(None)
		relays.append(temp)#ver direito a questao de ter mais de um possivel relay para cada bloqueio

	print "relays ->",relays
	copy.sort(reverse=True)
	i = 0
	while(visited.count(0)>0):
		visited.remove(0)
		visited.insert(i, 1)
		if (relays[int (i/nNodes)].count(None)<4):
			print "aqui",int(i/nNodes),",",i%nNodes
		i=i+1

	print "visited ->", visited



for j in range(nNodes):
    if (relays[int(i/nNodes)][j] != None):
        copy[int(i/nNodes) + relays[int(i/nNodes)][j]] = copy[i]+copy[int(i/nNodes) + relays[int(i/nNodes)][j]]
        for k in range(nNodes*nNodes):
            Wc.append(math.ceil(demand[int(k/nNodes)][k%nNodes]/channel[int(k/nNodes)][k%nNodes]))
        for k in range(nNodes):
            if (relays[int(i/nNodes)][k] != None):

                
