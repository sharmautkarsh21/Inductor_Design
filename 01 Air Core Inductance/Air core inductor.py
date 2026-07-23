from math import pi, sqrt

d=10e-3; h=100e-3; N=100; D=1e-3
I=1
u0= 4*pi*1e-7; 
ro= 1.72e-8   # Cu resistivity

B= u0*N*I/sqrt(h**2 + d**2)
L= (pi/4)*u0*N**2*d**2/sqrt(h**2 + d**2)

# wire length
long= N*pi*d
# resistance
R= ro*long/(pi*D**2/4)

print("Induction (T)= ", B)
print("Inductance (H), ", L)
print("Resistance (R), ", R)

