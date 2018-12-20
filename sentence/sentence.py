import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import random
import sys


def flip_coin():
    """
        Generate head or tail. 1 is tail, 0 is heads.
    """
    return random.randint(0, 1)

def sentence(Y, penalty, limit):
    """
        Simulate a sentence, starting with 2 days sentence, adding "penalty"
        days for each tail, exiting after either you die (limit is reached)
        or you got free (days_remaining = 0).
        :param Y: years of initial sentence
        :param penalty: increment for tails
        :param limit: in how many days you die
        :return days_spent: number of days spent in jail
        :return days_remaining: days you need to spend in jail (it can happen that
                you die but still have tons of days to spend in jail)
        :return flag: -1 if you die, 1 if you get out faster than initial sentence,
                0 if you get out but not faster than Y
    """
    days_remaining = 2
    days_spent = 0
    while days_remaining != 0 and days_spent < limit:
        days_remaining += flip_coin() * penalty - 1
        days_spent += 1

    if days_spent == limit:
        flag = -1
    elif days_spent < 365 * Y:
        flag = 1
    else:
        flag = 0

    return days_spent, days_remaining, flag

def sentence_looper(niter, Y, penalty, limit, debug=False):
    """
        Main simulation. It runs function sentence niter times.
        :param niter: number of scenarios tested
        :param Y: years of initial sentence
        :param pentalty: increment for tails
        :param limit: in how many days you die
        :param debug: debug mode for printing
        :return days_spent: list of days spent in jail for each scenario
        :return days_remaining: list of days remaining in jail for each scenario
        :return better_than_Y: how many times you escaped faster than initial sentence
        :return reached_limit: how many times you died
    """
    days_spent = [0 for _ in range(niter)]
    days_remaining = [0 for _ in range(niter)]
    better_than_Y = 0
    reached_limit = 0
    for i in range(niter):
        if debug and i % 10000 == 0:
            print i

        ds, dr, flag = sentence(Y, penalty, limit)

        days_spent[i] = ds
        days_remaining[i] = dr

        if flag == 1:
            better_than_Y += 1
        elif flag == -1:
            reached_limit += 1

    return days_spent, days_remaining, better_than_Y, reached_limit

def E(x):
    """
        Calculates expected value given list x of values.
        :param x: list of observations
        :returns expected value of X
    """
    return float(sum(x)) / len(x)


if __name__ == "__main__":
    try:
        niter = int(sys.argv[1])
        Y = int(sys.argv[2])
        penalty = int(sys.argv[3])
    except:
        niter = 100000
        Y = 35
        penalty = 3

    limit = 365 * 60

    days_spent, days_remaining, better_than_Y, reached_limit = \
            sentence_looper(niter=niter, Y=Y, penalty=penalty, limit=limit, debug=True)

    E_days = E(days_spent)

    print "You got out in less than 35 years in {}%".format(100.0 * better_than_Y / niter)
    print "You reached limit in {}%".format(100.0 * reached_limit / niter)
    print "Expected value of days spent in jail is {0} which is {1} years".format(int(E_days), int(E_days/365))

    plt.figure()
    plt.hist(days_spent, bins=100)
    plt.title("Days spent in jail (E(X) = {0}), penalty = {1}, Y = {2}".format( \
            E_days, penalty, Y))
    plt.xlabel("Days")
    plt.ylabel("Occurences")
    plt.tight_layout()
    plt.savefig("days_spent_hist_{0}_{1}.pdf".format(penalty, Y))

    plt.figure()
    plt.hist(days_remaining, bins=100)
    plt.title("Days remaining in jail")
    plt.xlabel("Days")
    plt.ylabel("Occurences")
    plt.tight_layout()
    plt.savefig("days_remaining_hist_{0}_{1}.pdf".format(penalty, Y))
