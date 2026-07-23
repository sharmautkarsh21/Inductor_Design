# Created by Utkarsh Sharma
# 17.07.2026 

import femm
import math
import csv
import matplotlib.pyplot as plt

femm.openfemm()
femm.newdocument(0)

## Transformer's geometry
# Core dimensions 
Core_width = 0.8;
Core_hight = 0.6;
Core_depth = 0.6;
Central_limb_thickness = 0.2;
Side_limb_thickness = 0.1;
Upper_limb_thickness = 0.1; 
# Windings
Winding_hight = 0.4; 
Winding_width = 0.1;
Winding_depth = Core_depth;

mr = 1000;
## FEMM model
                    

femm.main_maximize;
femm.mi_probdef(60, 'meters', 'planar', 1.e-8, Core_depth, 30);


# Define the geometry
femm.mi_drawrectangle(Core_width/2,-Core_hight/2, -Core_width/2,Core_hight/2)
            
femm.mi_drawrectangle(Central_limb_thickness/2,-Winding_hight/2,
                Central_limb_thickness/2+Winding_width,Winding_hight/2)

            
femm.mi_drawrectangle(Central_limb_thickness/2+Winding_width,-Winding_hight/2
                ,Central_limb_thickness/2+2*Winding_width,Winding_hight/2)
            
femm.mi_drawrectangle(-Central_limb_thickness/2,-Winding_hight/2,
                -Central_limb_thickness/2-Winding_width,Winding_hight/2)
            
femm.mi_drawrectangle(-Central_limb_thickness/2-Winding_width,-Winding_hight/2,
                -Central_limb_thickness/2-2*Winding_width,Winding_hight/2)


# Add the boundary conditions
femm.mi_makeABC(7,Core_width*2.5,0,0,0)

# femm.mi_selectarcsegment(3*Core_hight,0)
# femm.mi_setarcsegmentprop(2.5, 'Asymptotic', 0, 0)
# femm.mi_selectarcsegment(-3*Core_hight,0)
# femm.mi_setarcsegmentprop(2.5, 'Asymptotic', 0, 0)

# Add material labels
femm.mi_addblocklabel(0,0);
femm.mi_addblocklabel(Core_width,0);
femm.mi_addblocklabel(Central_limb_thickness/2+0.5*Winding_width,0);
femm.mi_addblocklabel(Central_limb_thickness/2+1.5*Winding_width,-0.1*Winding_hight);
femm.mi_addblocklabel(-Central_limb_thickness/2-0.5*Winding_width,0);
femm.mi_addblocklabel(-Central_limb_thickness/2-1.5*Winding_width,-0.1*Winding_hight);

# Add materials properties
femm.mi_addmaterial('Air', 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0);
femm.mi_addmaterial('Coil', 1, 1, 0, 2*1000/Winding_hight/Winding_width/10e+6, 58, 0, 0, 1, 0, 0, 0);
femm.mi_addmaterial('Core', mr, mr, 0, 0, 0, 0, 0, 1, 0, 0, 0);

# Add winding properties
femm.mi_addcircprop('Primary', 200, 1);
femm.mi_addcircprop('Secondary', -200, 1);

# Define area properties
femm.mi_selectlabel(Core_width,0);
femm.mi_setblockprop('Air', 1, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()

femm.mi_selectlabel(0,0);
femm.mi_setblockprop('Core', 1, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()


femm.mi_selectlabel(Central_limb_thickness/2+0.5*Winding_width,0);
femm.mi_setblockprop('Coil', 1, 1, 'Primary', 0, 0, 1000);
femm.mi_clearselected()


femm.mi_selectlabel(-Central_limb_thickness/2-0.5*Winding_width,0);
femm.mi_setblockprop('Coil', 1, 1, 'Primary', 0, 0, -1000);
femm.mi_clearselected()


femm.mi_selectlabel(Central_limb_thickness/2+1.5*Winding_width,0);
femm.mi_setblockprop('Coil', 1, 1, 'Secondary', 0, 0, 1000);
femm.mi_clearselected()


femm.mi_selectlabel(-Central_limb_thickness/2-1.5*Winding_width,0);
femm.mi_setblockprop('Coil', 1, 1, 'Secondary', 0, 0, -1000);
femm.mi_clearselected()


femm.mi_zoomnatural();  
femm.mi_saveas('leakage_inductance.fem');

femm.mi_analyze();
femm.mi_loadsolution();
            
# filename=[simmode(sm).filename '.ans'];
# save_femm(prb,filename);


