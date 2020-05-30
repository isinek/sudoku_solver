from sys import argv


__verbose__ = False


def is_sudoku_legal(table):
	if table is None or sum([len(r) for r in table]) != 81:
		return False
	for i in range(9):
		for j in range(9):
			if table[i][j] == 0:
				continue

			ii, jj = i//3*3, j//3*3
			for k in range(9):
				if (not (ii + k//3 == i and jj + k%3 == j) and table[ii + k//3][jj + k%3] == table[i][j]) or \
				    (k != i and table[k][j] == table[i][j]) or \
				    (k != j and table[i][k] == table[i][j]):
					return False
	return True


def is_sudoku_solved(table):
	if table is None:
		return False
	return all([all(n > 0 for n in row) for row in table]) and is_sudoku_legal(table)


def print_table(table_map):
	for i in range(9):
		if i > 0 and not i % 3:
			print('-'*21)
		print(' '.join([str(x) for x in table_map[i][:3]]), '| ', end='')
		print(' '.join([str(x) for x in table_map[i][3:6]]), '| ', end='')
		print(' '.join([str(x) for x in table_map[i][6:]]))
	print()


def print_table_map(table_map):
	max_len = max([max(len(x) for x in r) for r in table_map])
	for i in range(9):
		if i > 0 and not i % 3:
			print('-'*(9*max_len + 12))
		print(' '.join([''.join([str(n) for n in x] + [' ']*(max_len - len(x))) for x in table_map[i][:3]]), '| ', end='')
		print(' '.join([''.join([str(n) for n in x] + [' ']*(max_len - len(x))) for x in table_map[i][3:6]]), '| ', end='')
		print(' '.join([''.join([str(n) for n in x] + [' ']*(max_len - len(x))) for x in table_map[i][6:]]))
	print()


class MappingSolver():
	def __init__(self, table):
		self.clearing_map = [[False for _ in range(9)] for _ in range(9)]
		self.table_map = [[[x + 1 for x in range(9)] for _ in range(9)] for _ in range(9)]
		self.solution = None
		self.n_steps = 0
		self.table_map_queue = []
		for r in range(9):
			for c in range(9):
				if table[r][c]:
					self.__clear_options(table[r][c], r, c)
					self.clearing_map[r][c] = True
		if __verbose__: print_table_map(self.table_map)


	def __clear_options(self, n, r, c, clear_row=True, clear_col=True):
		for i in range(9):
			if i//3 != c//3 and clear_row and n in self.table_map[r][i]:
				self.table_map[r][i].remove(n)
			if i//3 != r//3 and clear_col and n in self.table_map[i][c]:
				self.table_map[i][c].remove(n)
			if clear_row and clear_col and ((r//3)*3 + i%3) == r and ((c//3)*3 + i//3) == c:
				self.table_map[(r//3)*3 + i%3][(c//3)*3 + i//3] = [n]
			elif clear_row and clear_col and n in self.table_map[(r//3)*3 + i%3][(c//3)*3 + i//3]:
				self.table_map[(r//3)*3 + i%3][(c//3)*3 + i//3].remove(n)


	def __check_loneliness(self, n, r, c):
		diff_row, diff_col = False, False
		lonely_row, lonely_col, lonely_block = True, True, True
		for i in range(9):
			if n in self.table_map[r][i] and i != c:
				lonely_col = False
			if n in self.table_map[i][c] and i != r:
				lonely_row = False
			if n in self.table_map[(r//3)*3 + i%3][(c//3)*3 + i//3] and not (((r//3)*3 + i%3) == r and ((c//3)*3 + i//3) == c):
				lonely_block = False
				if ((r//3)*3 + i%3) != r:
					diff_row = True
				if ((c//3)*3 + i//3) != c:
					diff_col = True

		if lonely_row or lonely_col or lonely_block:
			self.table_map[r][c] = [n]

		if not diff_row:
			self.__clear_options(n, r, c, clear_col=False)
		if not diff_col:
			self.__clear_options(n, r, c, clear_row=False)


	def solve(self):
		if self.solution:
			return self.solution

		self.n_steps = 0
		self.solution = [[[n[0], 0][len(n) > 1] for n in r] for r in self.table_map]
		while not is_sudoku_solved(self.solution):
			prev_table_map_state = ''.join([''.join([''.join([str(x) for x in c]) for c in r]) for r in self.table_map])
			for r in range(9):
				for c in range(9):
					if not self.clearing_map[r][c] and len(self.table_map[r][c]) == 1:
						self.__clear_options(self.table_map[r][c][0], r, c)
						self.clearing_map[r][c] = True
					if len(self.table_map[r][c]) > 1:
						for x in self.table_map[r][c]:
							self.__check_loneliness(x, r, c)
							if len(self.table_map[r][c]) == 1:
								break
			if __verbose__: print_table_map(self.table_map)

			self.n_steps += 1
			try:
				self.solution = [[[n[0], 0][len(n) > 1] for n in r] for r in self.table_map]
			except:
				self.solution = None
			if prev_table_map_state == ''.join([''.join([''.join([str(x) for x in c]) for c in r]) for r in self.table_map]):
				for r in range(9):
					if len(self.table_map_queue):
						self.table_map = self.table_map_queue.pop()
						if __verbose__: print_table_map(self.table_map)
						break
					for c in range(9):
						if len(self.table_map[r][c]) > 1:
							tmp_table_map = [[c[:] for c in r] for r in self.table_map]
							for x in self.table_map[r][c]:
								tmp_table_map[r][c] = [x]
								self.table_map_queue += [[[c[:] for c in r] for r in tmp_table_map]]
							break

		if __verbose__: print('Steps:', self.n_steps)

		if is_sudoku_solved(self.solution):
			return self.solution
		else:
			return None


if __name__ == '__main__':
	if '-v' in argv:
		__verbose__ = True

	sudoku_table = [[int(i) for i in str(input())] for _ in range(9)]
	print_table(sudoku_table)
	if not is_sudoku_legal(sudoku_table):
		print('Entered sudoku table is invalid!')
		exit(-1)

	mapping_solver = MappingSolver(sudoku_table)
	solution = mapping_solver.solve()

	if is_sudoku_solved(solution):
		print_table(solution)
	else:
		print('Failed to solve sudoku!')
		exit(-2)

