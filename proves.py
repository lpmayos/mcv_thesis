from pylab import *
import pickle


# from http://matplotlib.org/examples/pylab_examples/boxplot_demo.html

# # fake up some data
# spread= rand(50) * 100
# center = ones(25) * 50
# flier_high = rand(10) * 100 + 100
# flier_low = rand(10) * -100
# data =concatenate((spread, center, flier_high, flier_low), 0)

# # fake up some more data
# spread= rand(50) * 100
# center = ones(25) * 40
# flier_high = rand(10) * 100 + 100
# flier_low = rand(10) * -100
# d2 = concatenate( (spread, center, flier_high, flier_low), 0 )
# data.shape = (-1, 1)
# d2.shape = (-1, 1)
# #data = concatenate( (data, d2), 1 )
# # Making a 2-D array only works if all the columns are the
# # same length.  If they are not, then use a list instead.
# # This is actually more efficient because boxplot converts
# # a 2-D array into a list of vectors internally anyway.
# data = [data, d2, d2[::2,0]]


data = pickle.load(open("pickle/all_videos_sentences_similarities_exp1.pickle", "rb"))

# multiple box plots on one figure
figure()

# get dictionary returned from boxplot
bp_dict = boxplot(data, vert=False)

for line in bp_dict['medians']:
    x, y = line.get_xydata()[1]  # position for median line: [1] top of median line, [0] bottom of median line
    text(x, y + 0.02, '%.3f' % x, horizontalalignment='center')  # overlay median value above, centered

for line in bp_dict['boxes']:
    x, y = line.get_xydata()[0]  # bottom of left line
    text(x, y - 0.02, '%.3f' % x, horizontalalignment='center', verticalalignment='top')
    x, y = line.get_xydata()[3]  # bottom of right line
    text(x, y - 0.02, '%.3f' % x, horizontalalignment='center', verticalalignment='top')

for line in bp_dict['whiskers']:
    x, y = line.get_xydata()[1]
    plt.text(x, y - 0.08, '%.3f' % x, horizontalalignment='center')

show()
