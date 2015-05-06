# coding=utf-8
import numpy

# weight matrix generation
def update_weight(n1, n2, n3, score_matrix):
    score_matrix[n1 * 127 + n2][n3] += 1
    return score_matrix

def sum_all(pos, score_matrix):
    return sum([score_matrix[pos][i] for i in range(128)])

def normalize_matrix(score_matrix):
    for i in range(128*128):
        s = sum_all(i, score_matrix)
        if s != 0:
            for j in range(128):
                score_matrix[i][j] /= s
    return score_matrix

# learning process

