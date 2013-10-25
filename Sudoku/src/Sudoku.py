from SearchProblem import SearchProblem
from math import sqrt


class Sudoku(SearchProblem):
	
	emptySymbol = 0 # empty cells contain 0
	fv = {} #dict containing the sets of forbidden values for each cell.Example {'00' : [1,2,3], ... }
	ifv = {} #dict containing the sets of forbidden values for each cell given by the istance
	updated = {} #dict containing the cells on which updateFV has been called
	lastPos = [] # last [row,col] edit
	lastUpdate = [] #last [row,col] passed to updateFV()
	
	def __init__(self,line,verbose=False):
		self.verbose=verbose
		self.count=0
		self.n=int(sqrt(len(line))) #side of the grid
		self.sn=int(sqrt(self.n)) #side of the subgrid
		self.istance = []	#istance and partial are equals at the beginning
		self.partial = []
		
		line = line.replace("\n","")
		row = 0
		col = 0
		ROW = []
		
		for symbol in line:
			ROW.append(int(symbol))
			col = (col+1)%self.n
			if col==0:
				self.istance.append(ROW)
				self.partial.append(list(ROW))
				ROW = []
				
		if self.verbose:
			print("INIT Creating the sets for each cell")
		
		for row in range(self.n):
			for col in range(self.n):
				self.fv[self.getRC(row,col)] = set()
				self.ifv[self.getRC(row,col)] = set()
				self.updated[self.getRC(row,col)] = False
				
		for row in range(self.n):
			for col in range(self.n):
				if self.verbose:
					print("INIT Updating the forbidden values in ifv for "+self.getRC(row,col))
				if self.istance[row][col]!=self.emptySymbol:
					if self.verbose:
						print("Calling updateFV on: "+str(row)+"-"+str(col)+" istance "+str(self.istance[row][col]))
					self.updateFV(self.ifv,[row,col])
		
		if self.verbose:
			print("Istance forbidden values")
			self.printDict(self.ifv)
			print("Forbidden values")
			self.printDict(self.fv)
			
	def enumerateSI(self,row=0,col=0):
		if row == self.n: #we have a complete grid!
			yield self.partial
		else:
			nextrow = row
			nextcol = col+1
			if nextcol == self.n:
				nextcol = 0
				nextrow += 1
			for i in range(1,self.n+1):
				self.partial[row][col] = i  #try with this symbol
				for r in self.enumerateSI(nextrow,nextcol):
					yield r

	
	def isAdmissible(self,solution=None):
		if solution==None:
			solution = self.partial

		if self.verbose:
			print("Calling isAdmissible on: ")
			print(self)
			print("Checking solution is compatible with istance")
		#look 4 compatibility between solution and istance
		for row in range(self.n):
			for col in range(self.n):
				if self.istance[row][col]!=0 and solution[row][col]!=self.istance[row][col]:
					if self.verbose:
						print("Fixed cell changed "+str(row)+" "+str(col)) 	
					return False
		if self.verbose:
			print("Solution compatible with istance")
		
		#look 4 repeated values in rows
		if self.verbose:
			print("Looking for repeated values in rows")

		for row in range(self.n):
			seenValues = set()
			for col in range(self.n):
				if solution[row][col]!=0 and solution[row][col] in seenValues:
					if self.verbose:
						print("Repeated value in row: "+str(row)+"-"+str(col))
					return False
				seenValues.add(solution[row][col])
		if self.verbose:
			print("No repetition found in rows")

		#look 4 repeated values in cols
		if self.verbose:
			print("Looking for repeated values in cols")
		for col in range(self.n):
			seenValues = set()
			for row in range(self.n):
				if solution[row][col]!=0 and solution[row][col] in seenValues:
					if self.verbose:
						print("Repeated value in col: "+str(row)+"-"+str(col))
					return False
				seenValues.add(solution[row][col])
		if self.verbose:
			print("No repetitions found in cols")

		#look 4 repetitions in subgrids
		if self.verbose:
			print("Looking for repeated values in sub-grids")
		sn = int(sqrt(self.n))
		for cornerRow in range(0,self.n,sn):
			for cornerCol in range(0,self.n,sn):
				seenVals = set()
				for row in range(sn):
					for col in range(sn):
						val = solution[cornerRow+row][cornerCol+col]
						if val!=0 and val in seenVals:
							if self.verbose:
								print("Repetition in sub-grid "+str(cornerRow+row)+str(cornerCol+col))
							return False
						seenVals.add(val)
		if self.verbose:
			print("No repetitions found in subgrids")
			print("It's admissible")
			
		return True
		
	def hasBeenUpdated(self,k):
		return self.updated[k]
			
	
	def setNextEmpty(self,current,digit):
		if self.verbose:
			print("setNextEmpty")
			print("self.partial["+str(current[0])+"-"+str(current[1])+"]: "+str(self.partial[current[0]][current[1]]))
		isRemovable = self.hasBeenUpdated(self.getRC(current[0],current[1]))
		if self.verbose:
			print("isRemovable: "+str(isRemovable))
		if isRemovable:
			if self.verbose:
				print("Calling remove on "+str(current[0])+"-"+str(current[1]))
			self.removeFV([current[0],current[1]])
		self.partial[current[0]][current[1]] = digit
		self.lastPos = [current[0],current[1]]
		if self.verbose:
			print("setNextEmpty has set "+str(digit)+" in "+str(current[0])+"-"+str(current[1]))

	def computeNextEmpty(self,current):
		if current==None:
			currentRow=0
			currentCol=0
		else:
			currentRow=current[0]
			currentCol=current[1]
		
		if self.partial[currentRow][currentCol]!=0:
			for col in range(currentCol+1,self.n):
				if self.partial[currentRow][col] == 0:
					return [currentRow,col]
			for row in range(currentRow+1,self.n):
				for col in range(self.n):
					if self.partial[row][col] == 0:
						return [row,col]
			return None
		else:
			return [currentRow,currentCol]

	def isNotExtendible(self):
		self.count += 1
		k = self.getRC(self.lastPos[0],self.lastPos[1])
		if self.verbose:
			print("isNotExtendible")
			print(self.lastPos)
			print("The k is: "+k)
		if self.partial[self.lastPos[0]][self.lastPos[1]] in self.fv[k] or self.partial[self.lastPos[0]][self.lastPos[1]] in self.ifv[k]:
			return True
		self.updateFV(self.fv,[self.lastPos[0],self.lastPos[1]])
		if self.verbose:
			print("Forbidden values set updated")
		return False
		
	def Gamma(self,current):
		for gamma in range(self.n):
			yield gamma+1

	def __str__(self):
		s = ""
		for row in range(self.n):
			for col in range(self.n):
				if self.istance[row][col] == 0:
					s += " : "
				else:
					s += " "+str(self.istance[row][col])+" "
			s += "\t"
			for col in range(self.n):
				if self.partial[row][col] == 0:
					s += " : "
				else:
					s += " "+str(self.partial[row][col])+" "
			s += "\n"
		return s
	
	#returns the row and col indexes as a string. e.g. '00' 
	def getRC(self,row,col):
		return str(row)+str(col)
		
	def getMySubGridCorner(self,row,col):
		if row<=2:
			cornR = 0
		elif row<=5:
			cornR = 3
		else:
			cornR = 6
		if col<=2:
			cornC = 0
		elif col<=5:
			cornC = 3
		else:
			cornC = 6
		return [cornR,cornC]
	
	def printDict(self,d):
		for k in sorted(d.keys()):
			print(k+"\t"+str(sorted(d[k])))
	
	
	def updateFV(self,fv,pos):
		if self.verbose:
			print("updateFV")
		r = int(pos[0])
		c = int(pos[1])
		self.lastUpdate = [pos[0],pos[1]]
		if self.verbose:
			print("Last set in "+str(r)+"-"+str(c))
		if self.verbose:
			print("Updating the sets")
		#print("POS: "+str(pos))

		if self.verbose:
			print("Updating the sets of the values in row "+str(r))
		for col in range(self.n):
			k = self.getRC(r,col)
			if self.verbose:
				print("The key is: "+k)
				#print("Adding to self.fv: "+str(self.partial[r][c]))
			if col!=c:
				forbVK = fv[k] #the set of forbidden values having key K
				forbVK.add(self.partial[r][c])
		if self.verbose:
			print("Updating the sets of the values in col "+str(c))
		for row in range(self.n):
			k = self.getRC(row,c)
			if self.verbose:
				print("The key is: "+k)
				#print("Adding to self.fv: "+str(self.partial[r][c]))
			if row!=r:
				forbVK = fv[k] #the set of forbidden values having key K
				forbVK.add(self.partial[r][c])
				
		gridCorn = self.getMySubGridCorner(r,c)
		cornerRow = gridCorn[0]
		cornerCol = gridCorn[1]
		if self.verbose:
			print("Updating the sets of the values in the subgrid "+str(cornerRow)+"-"+str(cornerCol))
		for row in range(self.sn):
			for col in range(self.sn):
				k = self.getRC(cornerRow+row,cornerCol+col)
				if self.verbose:
					print("The key is: "+k)
					#print("Adding to self.fv: "+str(self.partial[r][c]))
				if row!=r and col!=c:
					forbVK = fv[k] #the set of forbidden values having key K
					if not self.partial[r][c] in forbVK:
						forbVK.add(self.partial[r][c])
		if self.verbose:
			print("Setting self.updated["+str(r)+str(c)+"] = True")
		self.updated[self.getRC(r,c)] = True
		
		if self.verbose:
			print("UPDATE: The forbidden values are")
			self.printDict(fv)
		
	def removeFV(self,pos):
		if self.verbose:
			print("removeFV")
		r = int(pos[0])
		c = int(pos[1])
		#if r!=self.lastUpdate[0] or c!=self.lastUpdate[1]:
		#	if self.verbose:
		#		print("Remove invoked on different row-col")
		#	return
		if self.verbose:
			print("Last set in "+str(r)+"-"+str(c))
		if self.verbose:
			print("Updating the sets")
		#print("POS: "+str(pos))

		for col in range(self.n):
			k = self.getRC(r,col)
			if self.verbose:
				print("The key is: "+k)
			if col!=c:
				forbVK = self.fv[k] #the set of forbidden values having key K
				if self.partial[r][c] in forbVK:
					if self.verbose:
						print("Removing "+str(self.partial[r][c])+" from the fv["+k+"]")
					forbVK.remove(self.partial[r][c])
		if self.verbose:
			print("Updating the sets of the values in col "+str(c))
		for row in range(self.n):
			k = self.getRC(row,c)
			if self.verbose:
				print("The key is: "+k)
			if row!=r:
				forbVK = self.fv[k] #the set of forbidden values having key K
				if self.partial[r][c] in forbVK:
					if self.verbose:
						print("Removing "+str(self.partial[r][c])+" from the fv["+k+"]")
					forbVK.remove(self.partial[r][c])
		
		gridCorn = self.getMySubGridCorner(r,c)
		cornerRow = gridCorn[0]
		cornerCol = gridCorn[1]
		if self.verbose:
			print("Updating the sets of the values in the subgrid "+str(cornerRow)+"-"+str(cornerCol))
		for row in range(self.sn):
			for col in range(self.sn):
				k = self.getRC(cornerRow+row,cornerCol+col)
				if self.verbose:
					print("The key is: "+k)
				if row!=r and col!=c:
					forbVK = self.fv[k] #the set of forbidden values having key K
					if self.partial[r][c] in forbVK:
						if self.verbose:
							print("Removing "+str(self.partial[r][c])+" from the fv["+k+"]")
						forbVK.remove(self.partial[r][c])
		self.updated[self.getRC(r,c)] = False
		if self.verbose:
			print("REMOVE: The forbidden values are")
			self.printDict(self.fv)