# -*- coding: utf-8 -*-
"""
Visualization of stochastic gradient methods vs. gradient descent for
the simple Boyan chain. The difference between the MSE and MSPBE can be
understood nicely from this example.

Created on Mon Jan 30 21:06:12 2012

@author: Christoph Dann <cdann@cdann.de>
"""

import td
import task
import numpy as np
import matplotlib.pyplot as plt
import examples
import scipy.optimize


n = 7
n_feat = 2
n_iter = 100
mdp = examples.BoyanChain(n, n_feat)
phi=mdp.phi
task = task.LinearValuePredictionTask(mdp, 1, phi, np.array([50.,0.]))


methods = []

lstd = td.LSTDLambda(lam=0, eps=1000, phi=phi)
lstd.name = r"LSTD({}) $\epsilon$={}".format(0, 1000)    
lstd.color = "b"        
#methods.append(lstd)

for alpha in [1]:
    td0 = td.LinearTDLambda(lam=0, alpha=alpha, phi=phi)
    td0.name = r"TD(0) $\alpha$={}".format(alpha)    
    td0.color = "k"
    methods.append(td0)
    
for alpha, mu in[( 1, 0.1)]:        
    tdc = td.TDC(alpha=alpha, beta=alpha*mu, phi=phi)
    tdc.name = r"TDC $\alpha$={} $\mu$={}".format(alpha, mu)   
    tdc.color = "r"        
    methods.append(tdc)

err_f = task._init_error_fun("RMSE")
param_sgd = task.parameter_traces(methods, n_samples=500)

# Ordinary Gradient Descent
grad = lambda x: scipy.optimize.approx_fprime(x, err_f, scipy.optimize.optimize._epsilon*5)
param_gd = np.empty((param_sgd.shape[0],2))
p = task.theta0
for i in xrange(param_gd.shape[0]):
    param_gd[i,:] = p
    p -= 10*grad(p)

size = np.array(param_sgd.shape) + [0,1,0]
param = np.empty(size)
param[:,:-1,:] = param_sgd
param[:,-1,:] = param_gd


w1, w2 = np.meshgrid(np.linspace(np.min(-10 + param[:,:,0]), 10 + np.max(param[:,:,0]), 150), 
                     np.linspace(np.min(-10 + param[:,:,1]), 10 + np.max(param[:,:,1]), 150))
                     

extends = np.min(w1), np.max(w1), np.min(w2),np.max(w2)
s = w1.copy()

for i in xrange(w1.shape[0]):
    for j in xrange(w2.shape[1]):
        s[i,j] = err_f([w1[i,j], w2[i,j]])



plt.figure()
plt.imshow(s, extent=extends, origin="lower")
plt.xlabel(r"$\theta_1$")
plt.ylabel(r"$\theta_2$")
plt.autoscale(tight=True)
plt.colorbar().ax.set_ylabel(r"$\sqrt{MSE}$")

plt.plot(param[:,0,0],param[:,0,1],'w', linewidth=2, label="TD(0)")
plt.plot(param[:,1,0],param[:,1,1],'#aaffaa', linewidth=2, label="TDC")
plt.plot(param[:,2,0],param[:,2,1],'m', linewidth=2, label="Grad. Desc.")
lg = plt.legend(loc= "lower right")    
lg.get_frame().set_facecolor('#cccccc')

plt.show()