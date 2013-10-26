from SearchProblem import SearchProblem
from math import sqrt


class Sudoku(SearchProblem):
	
	emptySymbol = 0 # empty cells contain 0

	def __init__(self,line,verbose=False):
		self.verbose=verbose
		self.count=0
		self.n=int(sqrt(len(line))) #side of the grid
		self.sn=int(sqrt(self.n)) #side of the subgrid
		self.istance = []	#istance and partial are equals at the beginning
		self.partial = []
		line = line.replace("\n","")
		col = 0
		ROW = []
		for symbol in line:
			ROW.append(int(symbol))
			col = (col+1)%self.n
			if col==0:
				self.istance.append(ROW)
				self.partial.append(list(ROW))
				ROW = []
			
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
		

	def setNextEmpty(self,current,digit):
		self.partial[current[0]][current[1]] = digit

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
		return not self.isAdmissible()
		
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
