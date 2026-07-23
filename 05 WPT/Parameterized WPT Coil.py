# Created by Utkarsh Sharma
# 17.07.2026 

import femm
import math
import csv
import matplotlib.pyplot as plt

femm.openfemm()
femm.newdocument(0)

d = 1.15 # wire diameter in mm
W = 25 # Length of the plate
H = 3 # Height of the plate
n_c = 8 # number of conductors
coil_g = 0.075 # gap between plate and 
coil_space = 0.1
Current_Val = 1 # A rms
turns = 1
last_layer_offset = 3.55

group_plate = 100
group_coil = 1
group_airregion = 500

femm.mi_probdef(0,"millimeters","axi",1e-8,1,30)
# Create the outer bounding space with Dirichilet Boundayr Conditions
femm.mi_makeABC(7,W*1.5,0,0,0)

femm.mi_getmaterial("Air")
femm.mi_addmaterial("Copper",1,1,0,0,58,0,0,1,0,0,0,1,1)
femm.mi_addcircprop("Coil",Current_Val,1)
femm.mi_addmaterial("Ferrite",2000,2000,0,0,0,0,0,1,0,0,0,1,0)

x1_rect = 0
x2_rect = W
y1_rect = -d/2-coil_g
y2_rect = -d/2-coil_g-H
# Create rectangle
femm.mi_drawrectangle(x1_rect,y1_rect,x2_rect,y2_rect)
femm.mi_addblocklabel((x1_rect+x2_rect)/2,(y1_rect+y2_rect)/2)
femm.mi_selectlabel((x1_rect+x2_rect)/2,(y1_rect+y2_rect)/2)
femm.mi_setblockprop("Ferrite",1,0,0,0,group_plate,0)

for i in range(0,n_c):
    x1 = W-last_layer_offset - i*(d+coil_space)
    x2 = x1-d
    y1 = 0
    y2 = 0
    femm.mi_addnode(x1,y1)
    femm.mi_addnode(x2,y2)
    femm.mi_addarc(x1,y1,x2,y2,180,10)
    femm.mi_addarc(x2,y2,x1,y1,180,10)
    femm.mi_addblocklabel((x1+x2)/2,(y1+y2)/2)
    femm.mi_selectlabel((x1+x2)/2,(y1+y2)/2)
    femm.mi_setblockprop("Copper",1,0,"Coil",0,group_coil,turns)

femm.mi_clearselected()

# Assign the airgap as air 
air_x = x2_rect*1.25
air_y = 0
femm.mi_addblocklabel(air_x,air_y)
femm.mi_selectlabel(air_x,air_y)
femm.mi_setblockprop("Air",1,0,0,0,group_airregion,0)
femm.mi_clearselected()

femm.mi_zoomnatural()
femm.smartmesh(1)
femm.mi_saveas("Parameterised_WPT.fem")
femm.mi_analyze()
femm.mi_loadsolution()
###########################################################################################################

# #Adding the Materials
# femm.mi_getmaterial("Air")
# # mi_addmaterial('matname', mu_x, mu_y, H_c, J, Cduct, Lam_d, Phi_hmax, lam fill, LamType, Phi_hx, Phi_hy, nstr, dwire)
# # 0 - Not laminated or laminated in plane
# # 1 - laminated in x or z
# # 2 - laminated in y or z
# # 3 - magnet wire
# # 4 - plain stranded wire
# # 5 - Litz wire
# # 6 - square wire

# femm.mi_addmaterial("Copper",1,1,0,0,58,0,0,1,3,0,0,1,0.5)
# femm.mi_addcircprop("Coil",Current_Val,1)
# femm.mi_addmaterial("Ferrite",2200,2200,0,0,0,0,0,1,0,0,0,1,0)
# femm.mi_addmaterial("MySteel",1,1,0,0,0)

# # Import the BH curve of the steel from csv file
# with open("my_steel.csv") as f:
#     reader = csv.reader(f, delimiter="\t")    
#     for row in reader:
#             B_steel = float(row[0])
#             H_steel = float(row[1])
#             femm.mi_addbhpoint("MySteel", B_steel, H_steel)

# L_array = []
# for i in range(2,40,2):
#     i = i*0.1
#     femm.mi_modifycircprop("Coil",1,i)
#     femm.mi_analyze()
#     femm.mi_loadsolution()
#     L = femm.mo_getcircuitproperties("Coil")[2]/i
#     L_array.append(L*1e6)
#     print(f"The inductance for current = {i:3f} = {L*1e6:3f}")

# i_array = [i*0.1 for i in range(2,40,2)]
# plt.plot(i_array,L_array)
# plt.title("Inductance vs Current")
# plt.xlabel("Current (Apeak)")
# plt.ylabel("Inductance (uH)")
# plt.xticks()
# plt.yticks
# plt.show()
