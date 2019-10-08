#==============================================================================#
# TITLE
#==============================================================================#
# University of Cincinnati
# Aerocats - Regular Class 2016
# propulsion.py: Aerothon propulsion definition
#
# update log:
#    11/07/2015 - shiggins: original version
#    11/13/2015 - updates to links in IMPORTS
#    01/18/2015 - transition to ATLAS
#
#==============================================================================#
# IMPORTS
#==============================================================================#
# import built-in modules
import os
import sys

# (USER) set up directories
trunkDir = r'C:\eclipse\workspace\AircraftDesign\trunk'
BAPDir = os.path.join(trunkDir,r'Aircraft_Models\Reg2016Aircraft_bAIRcats\ATLAS')

# link path to Aerothon
sys.path.append(trunkDir)

# import Aerothon modules
from scalar.units import GRAM, gacc, A, V, mAh, IN
from Aerothon.ACMotor import ACSpeedController

#==============================================================================#
# SPEED CONTROLLER MODELS
#==============================================================================#
Phoenix10 = ACSpeedController()
Phoenix10.Weight = 7*GRAM*gacc
Phoenix10.Imax = 10*A

Phoenix25 = ACSpeedController()
Phoenix25.Weight = 19*GRAM*gacc
Phoenix25.Imax = 25*A

Phoenix100 = ACSpeedController()
Phoenix100.Weight = 72.9*GRAM*gacc
Phoenix100.Imax = 100*A 
Phoenix100.LWH = (2.8*IN, 2*IN, 0.9*IN)

X5 = ACSpeedController()
X5.Weight = 5*GRAM*gacc
X5.Imax = 5*A
