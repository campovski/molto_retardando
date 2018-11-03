import itertools
import sys
import matplotlib
import matplotlib.pyplot as plt
import copy


def getOverlap(perms):
    """
        Calculates the length overlap of perms[i] and perms[j].
        perms[i] is checked from the end and perms[j] from the beginning.
        :param perms = list of all permutations in range(N)
    """
    n = len(perms)
    if n == 0:
        return -1
    N = len(perms[0])
    M = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            startOfSuffix = perms[i].index(perms[j][0])
            k = 0
            failed = False
            while k + startOfSuffix < N:
                if perms[i][k+startOfSuffix] != perms[j][k]:
                    failed = True
                    break
                k += 1
            if not failed:
                M[i][j] = N - startOfSuffix

    return M


def generateIndexList(om):
    """
    Generates list of permutation indices that result in shortest path.
    :param om: overlap matrix
    """

    n = len(om)
    queue = [0]

    while len(queue) < n:
        annihilateColumn(om, queue[-1])
        queue.append(om[queue[-1]].index(max(om[queue[-1]])))

    return queue


def annihilateColumn(m, k):
    """
    Sets column k of matrix m to 0. We also don't need to return the matrix,
    because matrices get passed in by reference.
    :param m: matrix
    :param k: index of column to nullify
    """
    for i in range(len(m)):
        m[i][k] = 0


def prettyPrint(perms, path, om):
    """
    Generates a sequence of numbers that includes all permutations and
    is the shortest one. Basically, forms a solution from list of indexes.
    :param perms: list of all permutations
    :param path: list of indices that tells the sequence of perms
    :param om: overlap matrix, used to efficiently concat perms
    """

    string = "".join(str(x+1) for x in perms[path[0]])  # natural numbers instead of 0+
    for i in range(1, len(path)):
        startString = om[path[i-1]][path[i]]
        string += "".join(str(x+1) for x in perms[path[i]][startString:])

    return string, len(string)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        N = 5
    else:
        N = int(sys.argv[1])

    perms = list(itertools.permutations(range(N)))

    overlapMatrix = getOverlap(perms)
    idxList = generateIndexList(copy.deepcopy(overlapMatrix))

    print prettyPrint(perms, idxList, overlapMatrix)[1]
