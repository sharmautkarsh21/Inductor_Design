# Created by Utkarsh Sharma
# 17.07.2026 

import femm
import math
import csv
import matplotlib.pyplot as plt

femm.openfemm()
femm.newdocument(0)

W = 25 # width of the inductor
H = 25.6 # height of the inductor
D = 7.5 # depth of the core
W_w = 5 # width of the window
g  = 0.5 # airgap of the cetral limb
W_l = 4.1 # width of the side/top limb
Current_Val = 1 # A rms
turns = 80
# Various groups for easy calling of the groups
group_core = 100
group_window = 10
group_coil = 1
group_airgap = 0
group_airregion = 500

femm.mi_probdef(0,"millimeters","planar",1e-8,D,30)

# Create the outer bounding space with Dirichilet Boundayr Conditions
femm.mi_makeABC(7,2*max(W,H),0,0,0)
# Create rectanle
femm.mi_drawrectangle(-W/2,-H/2,W/2,H/2)
#create side limb inner wall
femm.mi_drawline(-W/2+W_l,-H/2+W_l,-W/2+W_l,H/2-W_l)
femm.mi_drawline(W/2-W_l,-H/2+W_l,W/2-W_l,H/2-W_l)

# Create center limb inner wall
femm.mi_drawline(-W/2+W_l+W_w,-H/2+W_l,-W/2+W_l+W_w,H/2-W_l)
femm.mi_drawline(W/2-W_l-W_w,-H/2+W_l,W/2-W_l-W_w,H/2-W_l)

# Create partitial in window for coil
femm.mi_drawline(-W/2+W_l+W_w/2,-H/2+W_l,-W/2+W_l+W_w/2,H/2-W_l)
femm.mi_drawline(W/2-W_l-W_w/2,-H/2+W_l,W/2-W_l-W_w/2,H/2-W_l)

# Create the bottom and top wall for left window
femm.mi_drawline(-W/2+W_l,-H/2+W_l,-W/2+W_l+W_w,-H/2+W_l)
femm.mi_drawline(-W/2+W_l,H/2-W_l,-W/2+W_l+W_w,H/2-W_l)

# Create the bottom and top wall for left window
femm.mi_drawline(W/2-W_l,-H/2+W_l,W/2-W_l-W_w,-H/2+W_l)
femm.mi_drawline(W/2-W_l,H/2-W_l,W/2-W_l-W_w,H/2-W_l)

# Create the airgap
W_c = W-2*(W_l+W_w) # Width of the central limb
femm.mi_drawline(-W_c/2,-g/2,W_c/2,-g/2)
femm.mi_drawline(-W_c/2,g/2,W_c/2,g/2)

#Adding the Materials
femm.mi_getmaterial("Air")
# mi_addmaterial('matname', mu_x, mu_y, H_c, J, Cduct, Lam_d, Phi_hmax, lam fill, LamType, Phi_hx, Phi_hy, nstr, dwire)
# 0 - Not laminated or laminated in plane
# 1 - laminated in x or z
# 2 - laminated in y or z
# 3 - magnet wire
# 4 - plain stranded wire
# 5 - Litz wire
# 6 - square wire

femm.mi_addmaterial("Copper",1,1,0,0,58,0,0,1,3,0,0,1,0.5)
femm.mi_addcircprop("Coil",Current_Val,1)
femm.mi_addmaterial("Ferrite",2200,2200,0,0,0,0,0,1,0,0,0,1,0)
femm.mi_addmaterial("MySteel",1,1,0,0,0)

# Import the BH curve of the steel from csv file
with open("my_steel.csv") as f:
    reader = csv.reader(f, delimiter="\t")    
    for row in reader:
            B_steel = float(row[0])
            H_steel = float(row[1])
            femm.mi_addbhpoint("MySteel", B_steel, H_steel)

# Assign the left coil 
xc = -W/2+W_l+0.75*W_w
yc = 0
femm.mi_addblocklabel(xc,yc)
femm.mi_selectlabel(xc,yc)
femm.mi_setblockprop("Copper",1,0,"Coil",0,0,turns)
femm.mi_clearselected()

# Assign the right coil 
xc = W/2-W_l-0.75*W_w
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
femm.mi_setblockprop("Air",1,0,0,0,group_airgap,0)
femm.mi_clearselected()

# Assign the left air region in window
air_x = -W/2+W_l+0.25*W_w
air_y = 0
femm.mi_addblocklabel(air_x,air_y)
femm.mi_selectlabel(air_x,air_y)
femm.mi_setblockprop("Air",1,0,0,0,group_window,0)
femm.mi_clearselected()

# Assign the right air region in window
air_x = W/2-W_l-0.25*W_w
air_y = 0
femm.mi_addblocklabel(air_x,air_y)
femm.mi_selectlabel(air_x,air_y)
femm.mi_setblockprop("Air",1,0,0,0,group_window,0)
femm.mi_attachdefault()
femm.mi_clearselected()

# Create the air region around the inductor
air_x = W*1.25
air_y = 0
femm.mi_addblocklabel(air_x,air_y)
femm.mi_selectlabel(air_x,air_y)
femm.mi_setblockprop("Air",1,0,0,0,group_airregion,0)
femm.mi_attachdefault()
femm.mi_clearselected()

# Assign the core region
core_x = 0
core_y = H/4
femm.mi_addblocklabel(core_x,core_y)
femm.mi_selectlabel(core_x,core_y)
femm.mi_setblockprop("MySteel",1,0,0,0,group_core,0)
femm.mi_clearselected()

femm.mi_zoomnatural()
femm.smartmesh(1)
femm.mi_saveas("Parameterised_EE_Core_Nonlienar.fem")

L_array = []
for i in range(2,40,2):
    i = i*0.1
    femm.mi_modifycircprop("Coil",1,i)
    femm.mi_analyze()
    femm.mi_loadsolution()
    L = femm.mo_getcircuitproperties("Coil")[2]/i
    L_array.append(L*1e6)
    print(f"The inductance for current = {i:3f} = {L*1e6:3f}")

i_array = [i*0.1 for i in range(2,40,2)]
plt.plot(i_array,L_array)
plt.title("Inductance vs Current")
plt.xlabel("Current (Apeak)")
plt.ylabel("Inductance (uH)")
plt.xticks()
plt.yticks
plt.savefig('L_vs_I.png', dpi=300, bbox_inches='tight')
plt.show()
