#!/usr/bin/env python
import numpy as np
import random
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def read_data(file_path):
	l = []
	first = True
	f = open(file_path, 'rt')
	reader = csv.reader(f)
	for row in reader:
		if first:
			first = False
			continue
		arr = map(float, row[0].split(' '))
		l.append(arr)
	return l

class KMeans():
	def __init__(self, K, X=None, N=0):
		self.K = K
		if X == None:
			if N == 0:
				raise Exception("If no data is provided, \
								 a parameter N (number of points) is needed")
			else:
				self.N = N
				self.X = self._init_board_gauss(N, K)
		else:
			self.X = X
			self.N = len(X)
		self.mu = None
		self.clusters = None
		self.method = None
 
	def _init_board_gauss(self, N, k):
		n = float(N)/k
		X = []
		for i in range(k):
			c = (random.uniform(-1,1), random.uniform(-1,1))
			s = random.uniform(0.05,0.15)
			x = []
			while len(x) < n:
				a,b = np.array([np.random.normal(c[0],s),np.random.normal(c[1],s)])
				# Continue drawing points from the distribution in the range [-1,1]
				if abs(a) and abs(b)<1:
					x.append([a,b])
			X.extend(x)
		X = np.array(X)[:N]
		return X
 
	def plot_board(self, custom_text=''):
		X = self.X
		fig = plt.figure(figsize=(5,5))
		plt.xlim(-1,1)
		plt.ylim(-1,1)
		if self.mu and self.clusters:
			mu = self.mu
			clus = self.clusters
			K = self.K
			for m, clu in clus.items():
				cs = cm.spectral(1.*m/self.K)
				plt.plot(mu[m][0], mu[m][1], 'o', marker='*', \
						 markersize=12, color=cs)
				plt.plot(zip(*clus[m])[0], zip(*clus[m])[1], '.', \
						 markersize=8, color=cs, alpha=0.5)
		else:
			plt.plot(zip(*X)[0], zip(*X)[1], '.', alpha=0.5)
		if self.method == '++':
			tit = 'K-means++'
		else:
			tit = 'K-means with random initialization'
		# Scale the plot image
		# X lim
		plt.xlim([min(zip(*X)[0]),max(zip(*X)[0])])
		# Y lim
		plt.ylim([min(zip(*X)[1]),max(zip(*X)[1])])

		pars = 'N=%s, K=%s' % (str(self.N), str(self.K))
		plt.title('\n'.join([pars, tit]), fontsize=16)
		plt.savefig('kpp%s_N%s_K%s.png' % (custom_text, str(self.N), str(self.K)), \
					bbox_inches='tight', dpi=200)
 
	def _cluster_points(self):
		mu = self.mu
		clusters  = {}
		for x in self.X:
			bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) \
							 for i in enumerate(mu)], key=lambda t:t[1])[0]
			try:
				clusters[bestmukey].append(x)
			except KeyError:
				clusters[bestmukey] = [x]
		self.clusters = clusters
 
	def _reevaluate_centers(self):
		clusters = self.clusters
		newmu = []
		keys = sorted(self.clusters.keys())
		for k in keys:
			newmu.append(np.mean(clusters[k], axis = 0))
		self.mu = newmu
 
	def _has_converged(self):
		K = len(self.oldmu)
		return(set([tuple(a) for a in self.mu]) == \
			   set([tuple(a) for a in self.oldmu])\
			   and len(set([tuple(a) for a in self.mu])) == K)
 
	def find_centers(self, method='random'):
		self.method = method
		X = self.X
		K = self.K
		self.oldmu = random.sample(X, K)
		if method != '++':
			# Initialize to K random centers
			self.mu = random.sample(X, K)
		while not self._has_converged():
			self.oldmu = self.mu
			# Assign all points in X to clusters
			self._cluster_points()
			# Reevaluate centers
			self._reevaluate_centers()

class KPlusPlus(KMeans):
	def _dist_from_centers(self):
		cent = self.mu
		X = self.X
		D2 = np.array([min([np.linalg.norm(x-c)**2 for c in cent]) for x in X])
		self.D2 = D2
 
	def _choose_next_center(self):
		self.probs = self.D2/self.D2.sum()
		self.cumprobs = self.probs.cumsum()
		r = random.random()
		ind = np.where(self.cumprobs >= r)[0][0]
		return(self.X[ind])
 
	def init_centers(self):
		self.mu = random.sample(self.X, 1)
		while len(self.mu) < self.K:
			self._dist_from_centers()
			self.mu.append(self._choose_next_center())
 
	def plot_init_centers(self):
		X = self.X
		fig = plt.figure(figsize=(5,5))
		plt.xlim(-1,1)
		plt.ylim(-1,1)
		plt.plot(zip(*X)[0], zip(*X)[1], '.', alpha=0.5)
		plt.plot(zip(*self.mu)[0], zip(*self.mu)[1], 'ro')
		plt.savefig('kpp_init_N%s_K%s.png' % (str(self.N),str(self.K)), bbox_inches='tight', dpi=200)

# Used to find the best k-means. Implementation of Pham et al. f(K)
# This implementation INCLUDES the Gap Statistic method for comparison.
class DetK(KPlusPlus):
	def fK(self, thisk, Skm1=0):
		X = self.X
		Nd = len(X[0])
		a = lambda k, Nd: 1 - 3/(4*Nd) if k == 2 else a(k-1, Nd) + (1-a(k-1, Nd))/6
		self.find_centers(thisk, method='++')
		mu, clusters = self.mu, self.clusters
		Sk = sum([np.linalg.norm(mu[i]-c)**2 \
				 for i in range(thisk) for c in clusters[i]])
		if thisk == 1:
			fs = 1
		elif Skm1 == 0:
			fs = 1
		else:
			fs = Sk/(a(thisk,Nd)*Skm1)
		return fs, Sk

def clustering(dt):
	best_k = 0
	for k in range(2,9):
		kplusplus = KPlusPlus(k, X=dt)
		kplusplus.init_centers()
		
		#kplusplus.plot_init_centers()
		
		# Random initialization
		#kplusplus.find_centers()
		#kplusplus.plot_board('_rnd')
		
		# k-means++ initialization (Better)
		kplusplus.find_centers(method='++')
		kplusplus.plot_board('_plus')
		
		print 'Creating plot with k: %s' % k

def clustering_pham(dt):
	kpp = DetK(2, N=300)
	kpp.fK(10)
	kpp.plot_all()

def main():
	data = read_data('clust.csv')
	npdata = np.array(data)

	# Data preview
	#plt.plot(npdata[:,0], npdata[:,1], '.')
	#plt.show()
	
	clustering_pham(npdata)

if __name__ == "__main__":
	main()



