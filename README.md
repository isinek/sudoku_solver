# Sudoku solver

This simple sudoku solver is able to solve all sudokus that don't need _improvisation_.

## How does it work?

1. Input sudoku:
	> `python3 sudoku_solver.py` \
	\
	`876900000` \
	`010006000` \
	`040305800` \
	`400000210` \
	`090500000` \
	`050040306` \
	`029000008` \
	`004690173` \
	`000001004`

	Or:
	> `python3 sudoku_solver.py < theguardian_com_sudoku_easy_4035.txt`

2. Sudoku is checked for errors

3. Initialize `MappingSolver`.
	* uses `self.table_map` to see all possible options for each field
	* uses `self.clearing_map` to see which fields are already checked and locked
	* goes trought each field in original table, check static fields and clear options for each row, column and block of numbers
	* clearing is looped until all options are minimized and sudoku is solved

4. Solution printout:
	> `8 7 6 | 9 1 4 | 5 3 2` \
	`3 1 5 | 2 8 6 | 7 4 9` \
	`9 4 2 | 3 7 5 | 8 6 1` \
	`---------------------` \
	`4 3 8 | 7 6 9 | 2 1 5` \
	`6 9 1 | 5 2 3 | 4 8 7` \
	`2 5 7 | 1 4 8 | 3 9 6` \
	`---------------------` \
	`1 2 9 | 4 3 7 | 6 5 8` \
	`5 8 4 | 6 9 2 | 1 7 3` \
	`7 6 3 | 8 5 1 | 9 2 4`
