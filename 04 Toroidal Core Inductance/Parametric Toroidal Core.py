# Created by Utkarsh Sharma
# 17.07.2026 

import femm
import math
import csv
import matplotlib.pyplot as plt
femm.openfemm()
femm.newdocument(0)

od = 140 # Core outer diameter
id = 100 # Core inner diameter
wire_dia = 0.5 # Wire diameter
wire_layer = 1 # Number of layers
turns = 100 # Number of turns
wire_id = id-wire_layer*wire_dia # Wire inner diameter
wire_od = od+wire_layer*wire_dia # Wire outer diameter
D = 20 # Depth of the core

# Analytical calculation of the inductance of the toroidal core
mu_0 = 4*math.pi*1e-7 # Permeability of free space
mu_r = 1000 # Relative permeability of the core material
L_analytical = mu_0*mu_r*D*0.001*turns**2*math.log(od/id)/(2*math.pi) # Inductance in Henrys

group_coil = 1
group_airregion = 300
group_core = 100
Current_Val = 1 # A rms

femm.mi_probdef(0,"millimeters","planar",1e-8,D,30)
femm.mi_makeABC(2,wire_od*3,0,0,0)

femm.mi_addnode(od/2,0)
femm.mi_addnode(-od/2,0)
femm.mi_addnode(id/2,0)
femm.mi_addnode(-id/2,0)
femm.mi_addarc(od/2,0,-od/2,0,180,1)
femm.mi_addarc(-od/2,0,od/2,0,180,1) 
femm.mi_addarc(id/2,0,-id/2,0,180,1)
femm.mi_addarc(-id/2,0,id/2,0,180,1) 


femm.mi_addnode(wire_id/2,0)
femm.mi_addnode(-wire_id/2,0)
femm.mi_addnode(wire_od/2,0)
femm.mi_addnode(-wire_od/2,0)
femm.mi_addarc(wire_id/2,0,-wire_id/2,0,180,1)
femm.mi_addarc(-wire_id/2,0,wire_id/2,0,180,1)
femm.mi_addarc(wire_od/2,0,-wire_od/2,0,180,1)
femm.mi_addarc(-wire_od/2,0,wire_od/2,0,180,1)  


#Adding the Materials
femm.mi_getmaterial("Air")
femm.mi_addmaterial("Copper",1,1,0,0,58,0,0,1,3,0,0,1,0.5)
femm.mi_addcircprop("Coil",Current_Val,1)
femm.mi_addmaterial("Ferrite",mu_r,mu_r,0,0,0,0,0,1,0,0,0,1,0)

# Assign the inner coil 
xc = wire_id/2+0.25*wire_dia*wire_layer
yc = 0
femm.mi_addblocklabel(xc,yc)
femm.mi_selectlabel(xc,yc)
femm.mi_setblockprop("Copper",1,0,"Coil",0,0,turns)
femm.mi_clearselected()

# Assign the inner coil 
xc = wire_od/2-0.25*wire_dia*wire_layer
yc = 0
femm.mi_addblocklabel(xc,yc)
femm.mi_selectlabel(xc,yc)
femm.mi_setblockprop("Copper",1,0,"Coil",0,0,-turns)
femm.mi_clearselected()

# Assign the airgap as air 
air_x = 0
air_y = 0
femm.mi_addblocklabel(air_x,air_y)
femm.mi_selectlabel(air_x,air_y)
femm.mi_setblockprop("Air",1,0,0,0,group_airregion,0)
femm.mi_clearselected()

# Assign the core region
core_x = (id/2+od/2)/2
core_y = 0
femm.mi_addblocklabel(core_x,core_y)
femm.mi_selectlabel(core_x,core_y)
femm.mi_setblockprop("Ferrite",1,0,0,0,group_core,0)
femm.mi_clearselected()

# Assign the airgap as air 
air_x = 1.5*od/2
air_y = 0
femm.mi_addblocklabel(air_x,air_y)
femm.mi_selectlabel(air_x,air_y)
femm.mi_setblockprop("Air",1,0,0,0,group_airregion,0)
femm.mi_clearselected()

femm.mi_zoomnatural()
femm.smartmesh(1)
femm.mi_saveas("Parameterised_Toroid_Core.fem")
femm.mi_analyze()
femm.mi_loadsolution()  

coil_prop = femm.mo_getcircuitproperties('Coil')
L_fea =    coil_prop[2]/coil_prop[0] # Inductance in Henrys

print(f"Analytical Inductance: {L_analytical:.4f} H")
print(f"FEA Inductance: {L_fea:.4f} H")

