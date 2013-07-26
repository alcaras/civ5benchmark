import cPickle as pickle

jar = open('histograms.pickle', 'rb')
histograms = pickle.load(jar)
jar.close()
