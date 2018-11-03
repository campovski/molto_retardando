import math
import random
import matplotlib.pyplot as plt
import sys
import time


coin = [math.pi, math.e]  # coin has values pi and e
percentages = []  # stores percentages for given n_throws
l = int(sys.argv[1])  # lower limit on number of throws
u = int(sys.argv[2])  # upper limit on number of throws
N = int(sys.argv[3])  # number of repetitions for each n_throw

start_time = time.clock()  # start time
print 'Starting...'

try:
    # Loop through all possible number of throws. For each number of throws
    # repeat simulation N times. At the end save the histogram and sums generated.
    for n_throws in range(l, u+1):
        n_divisible_3 = 0  # count of sums that were divisible by 3
        sums = []  # stores all sums to plot histogram and save to csv

        print '\nSimulating {0} coin flips {1} times... '.format(n_throws, N)
        if N > 10000:
            sys.stdout.write('[{}] 0.0%'.format(' '*50))
        sys.stdout.flush()

        # Run simulation N times.
        for i in range(1, N+1):
            if N >= 10000 and i % (N/1000) == 0:
                sys.stdout.write('\r')
                sys.stdout.write('[%-50s] %.1f%%' % ('='*(i*100/N/2), i*100.0/N))
                sys.stdout.flush()

            suma = 0.0  # current sum

            # Simulate throws, round down and save the suma.
            for _ in range(n_throws):
                suma += coin[random.randint(0, 1)]
            suma = int(suma)
            sums.append(suma)

            if suma % 3 == 0:
                n_divisible_3 += 1

        if N >= 10000:
            print ''
        print 'Number of sums divisible with 3 is {}.'.format(n_divisible_3)
        print 'That is {}%.'.format(float(n_divisible_3)*100/N)
        percentages.append(float(n_divisible_3)*100/N)

        # Count all sums that we get and save it to csv file.
        sums_occurences = {}
        for suma in sums:
            try:
                sums_occurences[suma] += 1
            except KeyError:
                sums_occurences[suma] = 1

        f = open('out/csv/results_{0}_{1}.csv'.format(N, n_throws), 'w')
        for key in sorted(sums_occurences):
            f.write('{0},{1}\n'.format(key, sums_occurences[key]))
        f.close()

        # Plot histogram.
        x_limit = int(n_throws * math.e)
        x_Limit = int(n_throws * math.pi)
        y_Limit = math.ceil(max(sums_occurences.values()) * 1.01)
        bins = x_Limit - x_limit + 1

        plt.hist(sums, bins=bins)
        plt.xlabel('Sum')
        plt.ylabel('Number of occurences')
        plt.title(r'$\mathrm{Sums\ of\ coin\ flips\ with\ } \pi,e \mathrm{\ sides}$')
        plt.axis([x_limit, x_Limit, 0, y_Limit])
        plt.xticks(range(x_limit, x_Limit+1, max(1, (x_Limit - x_limit)/10)))
        plt.grid(True)
        plt.savefig('out/hist/hist_{0}_{1}.pdf'.format(N, n_throws))
        plt.clf()
        plt.close()

    # Plot graph of percentages in relation to number of throws.
    plt.plot(range(l, u+1), percentages, marker='o', markersize=2, linewidth=0.5)
    plt.xlabel('Number of throws ($n$)')
    plt.ylabel('Percentage')
    plt.title('Percentage of sums divisible with 3 when throwing coin $n$ times')
    plt.grid(True)
    plt.savefig('out/percentages/percentages_{0}_{1}-{2}.pdf'.format(N, l, u))

except KeyboardInterrupt:
    # Plot graph of percentages in relation to number of throws.
    plt.plot(range(l, l+len(percentages)), percentages, marker='o', markersize=2, linewidth=0.5)
    plt.xlabel('Number of throws ($n$)')
    plt.ylabel('Percentage')
    plt.title('Percentage of sums divisible with 3 when throwing coin $n$ times')
    plt.grid(True)
    plt.savefig('out/percentages/percentages_{0}_{1}-{2}.pdf'.format(N, l, l+len(percentages)))

finally:
    # Stop the clock and print execution time.
    end_time = time.clock()
    diff_time = round(end_time - start_time, 1)
    print ''
    if diff_time > 60:
        diff_time = int(diff_time)
        print 'Execution time: {0}m{1}s'.format(diff_time / 60, diff_time % 60)
    else:
        print 'Execution time: {}s'.format(diff_time)
