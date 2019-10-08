#==============================================================================#
# TITLE
#==============================================================================#
# University of Cincinnati
# Aerocats - Regular Class 2016
# Turnigy_6Cell_3000.py: Aerothon battery definition
#
# update log:
#    11/07/2015 - shiggins: original version
#    11/13/2015 - shiggins: updates to formatting and links in IMPORTS
#    01/18/2016 - shiggins: transition to ATLAS
#
#==============================================================================#
# IMPORTS
#==============================================================================#
# import built-in modules
import os
import sys

# (USER) set-up directories
trunkDir = r'C:\eclipse\workspace\AircraftDesign\trunk'

# import Aerothon modules
sys.path.append(trunkDir)
from scalar.units import GRAM, gacc, A, V, mAh, IN, LBF
from scalar.units import AsUnit
from Aerothon.ACMotor import ACBattery

#==============================================================================#
# BATTERY MODEL
#==============================================================================#
Weight = []
Power = []

### SPH: NEED TO CONFIRM THESE SPECS 151113 ###
Turnigy_6Cell_3000 = ACBattery()
Turnigy_6Cell_3000.Voltage = 22.2*V
Turnigy_6Cell_3000.Cells = 6 
Turnigy_6Cell_3000.Capacity = 3000*mAh
Turnigy_6Cell_3000.C_Rating = 25
Turnigy_6Cell_3000.Weight = .915*LBF
Turnigy_6Cell_3000.LWH = (1.5*IN,1.5*IN,5.5*IN)

Power.append(Turnigy_6Cell_3000.Power())
Weight.append(Turnigy_6Cell_3000.Weight)

#=============================================================================#
# VISUALIZATION & RESULTS
#=============================================================================#
if __name__ == '__main__':
    print AsUnit(Turnigy_6Cell_3000.Imax,'A')
