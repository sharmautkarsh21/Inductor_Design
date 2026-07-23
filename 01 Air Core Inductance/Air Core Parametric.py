import femm
import math

r_in = 120.0      # mm
g = 10 # airgap thickness
d    = 1.0      # winding thickness (radial)
h    = 100.0    # winding height
turns = 100
current = 1.0

femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0,"millimeters","axi",1e-8,1,30)

femm.mi_getmaterial("Air")
# mi_addmaterial('matname', mu_x, mu_y, H_c, J, Cduct, Lam_d, Phi hmax, lam fill, LamType, Phi_hx, Phi_hy, nstr, dwire)
femm.mi_addmaterial("Copper",1,1,0,0,58,0,0,1,3,0,0,1,1)
femm.mi_addcircprop("Coil",current,1)

x1 = g/2
x2 = g/2 + d
y1 = -h/2
y2 = h/2

femm.mi_drawrectangle(x1,y1,x2,y2)

xc = g/2 + d/2
yc = 0
femm.mi_addblocklabel(xc,yc)
femm.mi_selectlabel(xc,yc)
femm.mi_setblockprop("Copper",1,0,"Coil",0,0,turns)
femm.mi_clearselected()

r_outer=r_in
air_x = 0.25*(r_in+d+r_outer)
air_y = 0

femm.mi_addblocklabel(air_x,air_y)
femm.mi_selectlabel(air_x,air_y)
femm.mi_setblockprop("Air",1,0,"r_outer",0,0,0)
femm.mi_clearselected()


femm.mi_makeABC(7,r_in,0,0,0)

femm.smartmesh(1)
femm.mi_saveas("Parameterised_Air_Core.fem")

femm.mi_analyze()
femm.mi_loadsolution()



