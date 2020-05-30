# Sudoku solver

This simple sudoku solver is able to solve any given sudoku. \
If you want to see steps in solveing sudoku, use -v attribute.

## How does it work?

1. Input sudoku:
	> `python3 sudoku_solver.py` \
	\
	`850000000` \
	`060703000` \
	`001089000` \
	`700000031` \
	`500090600` \
	`900000024` \
	`004061000` \
	`020504000` \
	`690000000`

	Or:
	> `python3 sudoku_solver.py < theguardian_com_sudoku_expert_4818.txt`

2. Sudoku is checked for errors

3. Initialize `MappingSolver`.
	* uses `self.table_map` to see all possible options for each field
	* uses `self.clearing_map` to see which fields are already checked and locked
	* goes trought each field in original table, check static fields and clear options for each row, column and block of numbers
	* clearing is looped until all options are minimized
	* if sudoku is not solved when all options are minimized
		* first field with multiple options is found
		* copies of tables are queued with one option on selected field into `self.table_map_queue`
		* if option is correct, sudoku is cleared and solved
		* if option is not correct, new table is taken from queue and minimized

4. Solution printout:
	> `8 5 7 | 2 1 6 | 4 9 3` \
	`4 6 9 | 7 5 3 | 8 1 2` \
	`2 3 1 | 4 8 9 | 7 5 6` \
	`---------------------` \
	`7 8 2 | 6 4 5 | 9 3 1` \
	`5 4 3 | 1 9 2 | 6 7 8` \
	`9 1 6 | 8 3 7 | 5 2 4` \
	`---------------------` \
	`3 7 4 | 9 6 1 | 2 8 5` \
	`1 2 8 | 5 7 4 | 3 6 9` \
	`6 9 5 | 3 2 8 | 1 4 7`
