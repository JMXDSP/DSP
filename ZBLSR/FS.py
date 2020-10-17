import scipy.integrate as spi
import numpy as np
import pylab as pl

a = 0.50
b = 0.25
c = 0.05
d = 0.50
ND=30
TS=1.0
B0 =0.80
L0=0.19
S0 =0.08
R0=0.00
INPUT = (B0, L0,S0, R0)


def diff_eqs(INP, t):
    '''The main set of equations'''
    Y = np.zeros((4))
    V = INP
    Y[0] = -a* V[0]*V[1]-c*V[0]*V[2]-d*V[0]
    Y[1] = a* V[0]*V[1]-b*V[1]
    Y[2] = c* V[0]*V[2]+b*V[1]
    Y[3] = d*V[0]
    return Y  # For odeint


t_start = 0.0;t_end = ND;t_inc = TS
t_range = np.arange(t_start, t_end + t_inc, t_inc)
a = 0.5
RES = spi.odeint(diff_eqs, INPUT, t_range)
a = 0.6
RES1 = spi.odeint(diff_eqs, INPUT, t_range)
a = 0.7
RES2 = spi.odeint(diff_eqs, INPUT, t_range)


# Ploting
pl.subplot(111)
pl.figure(figsize=[11,8])
# pl.plot(RES[:, 0], '-+g', label='Brower')
# pl.plot(RES[:, 1], '-p', label='Like')
pl.plot(RES[:, 2], '-^r', label='Share')
pl.plot(RES1[:, 2], '-og', label='Share')
pl.plot(RES2[:, 2], '-db', label='Share')
# pl.plot(RES[:, 3], '-db', label='Recover')
pl.legend(loc=1)
pl.title('BLSR.py')
pl.xlabel('Time')
pl.ylabel('%')
pl.xlabel('Time')
pl.show()
