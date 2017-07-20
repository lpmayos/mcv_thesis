import matplotlib.pyplot as plt
import numpy as np


def boxplot_demo2():
    becher = [9.1495, 9.9479, 9.7933, 9.8002, 8.47, 9.14, 9.06, 9.6933, 9.7871, 10.5676, 9.7441, 10.4874, 7.9584, 7.9598, 8.3483, 7.2536, 9.0823, 10.8343, 10.4104, 7.2004, 9.6297, 9.96, 9.761, 9.684, 8.6062, 10.2098, 8.9002, 8.4511, 9.3335, 9.34946, 8.0319, 7.6379, 7.8435, 8.7572, 8.0516, 8.4134, 10.0623, 9.6406, 9.0502, 10.6821, 11.1951, 11.1876, 10.0111, 8.8456, 10.2769, 9.3939, 11.3178, 9.397, 9.9851, 9.9921, 10.1132, 8.9775, 10.499, 11.209, 10.66, 10.2704, 10.9543, 10.6529, 10.9925, 9.6625, 7.8673, 9.0023, 8.9538, 9.3961, 8.8799, 9.3722, 10.697, 9.808, 9.894, 9.5648, 10.2994, 9.0708, 9.2368, 8.8131, 8.3218, 10.1733, 9.5885, 10.7685, 9.2015, 9.881, 9.4362, 9.9686, 9.3, 9.979, 9.896, 10.05, 9.9113, 8.533, 9.68297]
    Q1, median, Q3 = np.percentile(np.asarray(becher), [25, 50, 75])
    IQR = Q3 - Q1

    loval = Q1 - 1.5 * IQR
    hival = Q3 + 1.5 * IQR

    wiskhi = np.compress(becher <= hival, becher)
    wisklo = np.compress(becher >= loval, becher)
    actual_hival = np.max(wiskhi)
    actual_loval = np.min(wisklo)

    Qs = [Q1, median, Q3, loval, hival, actual_loval, actual_hival]
    Qname = ["Q1 = " + str(Q1), "median = " + str(median), "Q3 = " + str(Q3), "Q1-1.5xIQR = " + str(loval), "Q3+1.5xIQR = " + str(hival), "Actual LO = " + str(actual_loval), "Actual HI = " + str(actual_hival)]

    for Q, name in zip(Qs, Qname):
        plt.axhline(Q, color="k")
        plt.text(1.52, Q, name)
    plt.boxplot(becher)
    plt.show()
    plt.close()


def boxplot_demo():

    # np.random.seed(10)
    # data = np.random.normal(100, 10, 200)

    data = [9.1495, 9.9479, 9.7933, 9.8002, 8.47, 9.14, 9.06, 9.6933, 9.7871, 10.5676, 9.7441, 10.4874, 7.9584, 7.9598, 8.3483, 7.2536, 9.0823, 10.8343, 10.4104, 7.2004, 9.6297, 9.96, 9.761, 9.684, 8.6062, 10.2098, 8.9002, 8.4511, 9.3335, 9.34946, 8.0319, 7.6379, 7.8435, 8.7572, 8.0516, 8.4134, 10.0623, 9.6406, 9.0502, 10.6821, 11.1951, 11.1876, 10.0111, 8.8456, 10.2769, 9.3939, 11.3178, 9.397, 9.9851, 9.9921, 10.1132, 8.9775, 10.499, 11.209, 10.66, 10.2704, 10.9543, 10.6529, 10.9925, 9.6625, 7.8673, 9.0023, 8.9538, 9.3961, 8.8799, 9.3722, 10.697, 9.808, 9.894, 9.5648, 10.2994, 9.0708, 9.2368, 8.8131, 8.3218, 10.1733, 9.5885, 10.7685, 9.2015, 9.881, 9.4362, 9.9686, 9.3, 9.979, 9.896, 10.05, 9.9113, 8.533, 9.68297]

    # boxplot with outliers
    plt.figure()

    # get dictionary returned from boxplot
    bp_dict = plt.boxplot(data, vert=False)

    for i, line in enumerate(bp_dict['medians']):
        x, y = line.get_xydata()[1]  # position for median line: [1] top of median line, [0] bottom of median line
        median = x
        plt.text(x, y + 0.02, '%.3f' % median, horizontalalignment='center')  # overlay median value above, centered

    for i, line in enumerate(bp_dict['boxes']):
        x, y = line.get_xydata()[0]  # bottom of left line
        q1 = x
        plt.text(x, y - 0.02, '%.3f' % q1, horizontalalignment='center', verticalalignment='top')
        x, y = line.get_xydata()[3]  # bottom of right line
        q3 = x
        plt.text(x, y - 0.02, '%.3f' % q3, horizontalalignment='center', verticalalignment='top')

    min_max = []
    for i, line in enumerate(bp_dict['whiskers']):
        x, y = line.get_xydata()[1]
        min_max.append(x)
        plt.text(x, y - 0.08, '%.3f' % x, horizontalalignment='center')

    plt.show()
    plt.close()


def main():
    boxplot_demo()
    boxplot_demo2()


if __name__ == "__main__":
    main()
