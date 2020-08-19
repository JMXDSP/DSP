import scipy.integrate as spi
import numpy as np
import pylab as pl

a = 0.5
b = 0.1
c=0.025
d = 0.01
e=0.03
ND=100.0
TS=1
S0 =0.88
I0 =0.15
R0=0.01
INPUT = (S0, I0, R0)

def diff_eqs(INP, t):
    '''The main set of equations'''
    Y = np.zeros((3))
    V = INP
    Y[0] = -a* V[0]*V[1]+e*V[1]*V[2]-d*V[0]
    Y[1] = a* V[0]*V[1]-b*V[1]+c*V[1]*V[2]
    Y[2] = b*V[1]+d*V[0]-c*V[1]*V[2]
    return Y  # For odeint


t_start = 0.0;t_end = ND;t_inc = TS
t_range = np.arange(t_start, t_end + t_inc, t_inc)
RES = spi.odeint(diff_eqs, INPUT, t_range)

print
RES

# Ploting
pl.subplot(111)
pl.plot(RES[:, 1], '-r', label='Infectious')
pl.plot(RES[:, 0], '-g', label='Susceptibles')
pl.plot(RES[:, 2], '-k', label='Recovereds')
pl.legend(loc=0)
pl.title('dy_SIR.py')
pl.xlabel('Time')
pl.ylabel('Infectious Susceptibles and Recovereds')
pl.xlabel('Time')
pl.show()
