from sys import argv


__verbose__ = False


def sudoku_solved(table):
	return all([all(len(n) == 1 for n in row) for row in table])


def print_table_map(table_map):
	max_len = max([max(len(x) for x in r) for r in table_map])
	for i in range(9):
		if i > 0 and not i % 3:
			print('-'*(9*max_len + 12))
		print(' '.join([''.join([str(n) for n in x] + [' ']*(max_len - len(x))) for x in table_map[i][:3]]), '| ', end='')
		print(' '.join([''.join([str(n) for n in x] + [' ']*(max_len - len(x))) for x in table_map[i][3:6]]), '| ', end='')
		print(' '.join([''.join([str(n) for n in x] + [' ']*(max_len - len(x))) for x in table_map[i][6:]]))


def clear_options(table_map, n, r, c, clear_row=True, clear_col=True):
	if __verbose__:
		print('clear_options', n, r, c, clear_row, clear_col)

	for i in range(9):
		if i//3 != c//3 and clear_row and n in table_map[r][i]:
			table_map[r][i].remove(n)
		if i//3 != r//3 and clear_col and n in table_map[i][c]:
			table_map[i][c].remove(n)
		if clear_row and clear_col and ((r//3)*3 + i%3) == r and ((c//3)*3 + i//3) == c:
			table_map[(r//3)*3 + i%3][(c//3)*3 + i//3] = [n]
		elif clear_row and clear_col and n in table_map[(r//3)*3 + i%3][(c//3)*3 + i//3]:
			table_map[(r//3)*3 + i%3][(c//3)*3 + i//3].remove(n)

	return table_map


def check_loneliness(table_map, n, r, c):
	diff_row, diff_col = False, False
	lonely_row, lonely_col, lonely_block = True, True, True
	for i in range(9):
		if n in table_map[r][i] and i != c:
			lonely_col = False
		if n in table_map[i][c] and i != r:
			lonely_row = False
		if n in table_map[(r//3)*3 + i%3][(c//3)*3 + i//3] and not (((r//3)*3 + i%3) == r and ((c//3)*3 + i//3) == c):
			lonely_block = False
			if ((r//3)*3 + i%3) != r:
				diff_row = True
			if ((c//3)*3 + i//3) != c:
				diff_col = True

	if lonely_row or lonely_col or lonely_block:
		table_map[r][c] = [n]
		if __verbose__:
			print('check_loneliness', n, r, c)

	if not diff_row:
		clear_options(table_map, n, r, c, clear_col=False)
	if not diff_col:
		clear_options(table_map, n, r, c, clear_row=False)

	return table_map


def solve_with_mapping(table):
	clearing_map = [[False for _ in range(9)] for _ in range(9)]
	table_map = [[[x + 1 for x in range(9)] for _ in range(9)] for _ in range(9)]
	for r in range(9):
		for c in range(9):
			if table[r][c]:
				table_map = clear_options(table_map, table[r][c], r, c)
				clearing_map[r][c] = True

	if __verbose__:
		print_table_map(table_map)
		print()

	counter = 0
	while not sudoku_solved(table_map):
		prev_table_map_hash = ''.join([''.join([''.join([str(x) for x in c]) for c in r]) for r in table_map])
		for r in range(9):
			for c in range(9):
				if not clearing_map[r][c] and len(table_map[r][c]) == 1:
					table_map = clear_options(table_map, table_map[r][c][0], r, c)
					clearing_map[r][c] = True
				if len(table_map[r][c]) > 1:
					for x in table_map[r][c]:
						table_map = check_loneliness(table_map, x, r, c)
						if len(table_map[r][c]) == 1:
							break
		if __verbose__:
			print_table_map(table_map)
			print()

		counter += 1
		if prev_table_map_hash == ''.join([''.join([''.join([str(x) for x in c]) for c in r]) for r in table_map]):
			break

	print('Steps:', counter)
	if sudoku_solved(table_map):
		print_table_map(table_map)
	else:
		print('Failed to solve sudoku!')


if __name__ == '__main__':
	if '-v' in argv:
		__verbose__ = True
	sudoku_table = [[int(i) for i in str(input())] for _ in range(9)]
	solve_with_mapping(sudoku_table)
