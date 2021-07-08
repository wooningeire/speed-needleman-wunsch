# from random import choice
# https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

str1 = "laughter medicine"
str2 = "slaughter medical"

gap_char = "▓"

# matrix[row][col]; row ~ str1 & col ~ str2
score_path_matrix = [[None] * len(str2) for char in str1]
best_candidate_sum_id_matrix = [[None] * len(str2) for char in str1] # encoded as 3-bit binary int; 0b001 for diagonal, 0b010 for vertical, 0b100 for horizontal

# construct the alignment score matrix and find the best alignment

def get_score_at(row: int, col: int):
	if row == -1:
		return -col - 1
	if col == -1:
		return -row - 1

	return score_path_matrix[row][col]

for row, char1 in enumerate(str1):
	for col, char2 in enumerate(str2):
		chars_match = char1 == char2

		# compute candidate sums

		# match/mismatch
		match_mismatch_sum = get_score_at(row - 1, col - 1) + (1 if chars_match else -1)

		# indel from row
		indel_row_sum = get_score_at(row - 1, col) - 1

		# indel from col
		indel_col_sum = get_score_at(row, col - 1) - 1

		best_candidate_sum = max(match_mismatch_sum, indel_row_sum, indel_col_sum)
		score_path_matrix[row][col] = best_candidate_sum

		# store which candidate sum(s) was the best so that the best alignment can be backtraced
		best_candidate_sum_id = 0
		for i, candidate_sum in enumerate([match_mismatch_sum, indel_row_sum, indel_col_sum]):
			if candidate_sum == best_candidate_sum:
				best_candidate_sum_id += 0b1 << i
		
		best_candidate_sum_id_matrix[row][col] = best_candidate_sum_id

print("alignment score matrix:")
for score_row in score_path_matrix:
	print(score_row)

print()
print("best candidate sum(s) matrix:")
for score_row in best_candidate_sum_id_matrix:
	print(score_row)

def backtrace_best_alignment():
	aligned_str1 = ""
	aligned_str2 = ""

	row = len(str1) - 1
	col = len(str2) - 1

	n_remaining_chars1 = len(str1)
	n_remaining_chars2 = len(str2)

	while row >= 0 and col >= 0:
		print(row, col)
		print(" : ", aligned_str1)
		print(" : ", aligned_str2)
		print()
		best_candidate_sum_id = best_candidate_sum_id_matrix[row][col]

		# use the stored best candidate sum ids to determine which direction to travel in the matrix
		# moving in a certain direction indicates that a char should be added to the corresponding string
		# (ie, moving 1 row is 1 char for str1, moving 1 col is 1 char for str2)

		# randomly select one of the best candidate sum methods
		# best_candidate_sum = choice([i for i in range(3) if best_candidate_sum_id & 0b1 << i != 0])

		best_candidate_sum = next(i for i in range(3) if best_candidate_sum_id & 0b1 << i != 0)

		# 0b001: row+col movement, prepend next char for both strings
		if best_candidate_sum == 0:
			aligned_str1 = str1[row] + aligned_str1
			aligned_str2 = str2[col] + aligned_str2
			row -= 1
			col -= 1
			n_remaining_chars1 -= 1
			n_remaining_chars2 -= 1
		# 0b010: row movement, prepend next char for str1 only
		elif best_candidate_sum == 1:
			aligned_str1 = str1[row] + aligned_str1
			aligned_str2 = gap_char + aligned_str2
			row -= 1
			n_remaining_chars1 -= 1
		# 0b100: col movement, prepend next char for str2 only
		elif best_candidate_sum == 2:
			aligned_str2 = str2[col] + aligned_str2
			aligned_str1 = gap_char + aligned_str1
			col -= 1
			n_remaining_chars2 -= 1

	aligned_str1 = str1[:n_remaining_chars1] + aligned_str1
	aligned_str2 = str2[:n_remaining_chars2] + aligned_str2

	max_aligned_str_length = max(len(aligned_str1), len(aligned_str2))
	aligned_str1 = aligned_str1.rjust(max_aligned_str_length, gap_char)
	aligned_str2 = aligned_str2.rjust(max_aligned_str_length, gap_char)

	return aligned_str1, aligned_str2

print()
print("backtracing:")
for aligned_str in backtrace_best_alignment():
	print(aligned_str)

print("(alignment score = {})".format(score_path_matrix[-1][-1]))