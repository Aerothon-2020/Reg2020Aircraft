from __future__ import division # let 5/2 = 2.5 rather than 2
#from os import environ as _environ; _environ["scalar_off"] = "off"
#==============================================================================#
# TITLE
#==============================================================================#
# University of Cincinnati
# Aerocats - Regular Class 2016
# propulsion.py: Aerothon propulsion definition
#
# update log:
#    11/07/2015 - shiggins: original version
#    11/13/2015 - shiggins: updates to links in IMPORTS
#    01/18/2015 - shiggins: transition to ATLAS
#    01/20/2017 - dechellis: addition of Scorpion & 22x8 powerplant
#
#==============================================================================#
# IMPORTS
#==============================================================================#
# import built-in modules
import os
import sys
import numpy as npy

# (USER) set-up directories
trunkDir = r'C:\eclipse\workspace\AircraftDesign\trunk'
BAPDir = os.path.join(trunkDir,r'Aircraft_Models\Reg2018Aircraft_UCBearForce\BAP')

# link path to Aerothon
sys.path.append(trunkDir)

# import Aerothon modules
from scalar.units import IN, LBF, PSFC, SEC, ARCDEG, FT, OZF, RPM, HP, inHg
from scalar.units import AsUnit
from Aerothon.ACPropulsion import ACPropulsion

# Hacker Powerplant
#sys.path.append(os.path.join(BAPDir,r'Propulsion\Propellers'))
from Propellars.APC_20x8E import Prop
#sys.path.append(os.path.join(BAPDir,r'Propulsion\Motors'))
#from Motors.Hacker_A50_14L import Motor
from Motors.Hacker_A50_14L import Motor

## # Scorpion Powerplant
##sys.path.append(os.path.join(BAPDir,r'Propulsion\Propellers'))
##from APC_22x10E import Prop
##sys.path.append(os.path.join(BAPDir,r'Propulsion\Motors'))
##from Scorpion250KV import Motor

#==============================================================================#
# PROPULSION MODEL
#==============================================================================#
# Set Propulsion properties
Propulsion = ACPropulsion(Prop,Motor)
Propulsion.Alt  = 0*FT
Propulsion.Vmax = 60*FT/SEC
Propulsion.nV   = 20

#==============================================================================#
# VISUALIZATION & RESULTS
#==============================================================================#
if __name__ == '__main__':
    import pylab as pyl
   
    print "Static Thrust :", AsUnit( Propulsion.T(0*FT/SEC), "lbf")
    
    Vmax = 60
    V = npy.linspace(0,Vmax,30)*FT/SEC
    Vprop = npy.linspace(0,Vmax,5)*FT/SEC
    N = npy.linspace(1000,20000,30)*RPM
    Propulsion.PlotMatched(V, N, Vprop, fig = 2 )
    Propulsion.PlotTPvsN(N, Vprop, fig=1)
    Propulsion.PlotTestData(fig=3)
    
    Propulsion.Draw(fig=4)
    
    pyl.show()
