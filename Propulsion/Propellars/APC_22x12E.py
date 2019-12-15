from __future__ import division # let 5/2 = 2.5 rather than 2
#==============================================================================#
# TITLE
#==============================================================================#
# University of Cincinnati
# Aerocats - Regular Class 2016
# APC_20x8E.py: Aerothon propeller definition
#
# update log:
#    11/07/2015 - shiggins: original version
#    11/13/2015 - shiggins: updates to format and to links in IMPORTS
#    12/15/2015 - shiggins: updates from tests by M.Rorapaugh
#    01/18/2016 - shiggins: transition to ATLAS
#
#==============================================================================#
# IMPORTS
#==============================================================================#
# import built-in modules
import os
import sys
import numpy as npy
import pylab as pyl

# (USER) set-up directories
#trunkDir = r'C:\eclipse\workspace\AircraftDesign\trunk'
#BAPDir = os.path.join(trunkDir,r'Aircraft_Models\Reg2018Aircraft_UCBearForce\BAP')

# link path to Aerothon
#sys.path.append(trunkDir)

# import Aerothon modules
from scalar.units import IN, LBF, SEC, ARCDEG, FT, RPM, OZF, GRAM, gacc, W, K,\
     degR, inHg, MM
from scalar.units import AsUnit
from Aerothon.ACPropeller import ACPropeller
from Aerothon.AeroUtil import STDCorrection

#==============================================================================#
# PROPELLER MODEL
#==============================================================================#
# Set Propeller properties
Prop = ACPropeller()
Prop.name       = 'APC 22x12E'
Prop.D          = 22*IN
Prop.Thickness  = 0.5*IN

Prop.Pitch      = 12*IN
Prop.dAlpha     = 11*ARCDEG # 3.3
Prop.Solidity   = 0.0126  

Prop.AlphaStall = 20*ARCDEG
Prop.AlphaZeroCL = 0*ARCDEG
Prop.CLSlope    = .065/ARCDEG  #- 2D airfoil lift slope
Prop.CDCurve    = 2.2          #- 2D curvature of the airfoil drag bucket
Prop.CDp        = .04          #- Parasitic drag

Prop.Weight     = 159.89*GRAM*gacc

Prop.ThrustUnit = LBF
Prop.ThrustUnitName = 'lbf'
Prop.PowerUnit = W 
Prop.PowerUnitName = 'watt' 
Prop.MaxTipSpeed = None

# These are corrected for standard day
# (Second set of data taken - concern about first set since taken at night)
STD = STDCorrection(30.13*inHg, (-5 + 273.15)*K)
STD2 = STDCorrection( 30.10*inHg, (12.7+273.15)*K )

Prop.ThrustData = [(4250 *RPM, 209.2*OZF*STD),
                   (4250 *RPM, 195.2*OZF*STD)] # this point taken after initial points on Hacker A50. Used to verify good data.

Arm = 19.5*IN*STD
Arm2=19.5*IN*STD2 # Took torque data in closet with known prop to observe difference between temp
Prop.TorqueData = None

#==============================================================================#
# VISUALIZATION & RESULTS
#==============================================================================#
if __name__ == '__main__':
   
    print " D     : ", AsUnit( Prop.D, 'in')
    print " Pitch : ", AsUnit( Prop.Pitch, 'in')
    
    Vmax = 50
    h=0*FT
    N=npy.linspace(1000, 6800, 5)*RPM
    
    Alpha = npy.linspace(-25,25,41)*ARCDEG
    V     = npy.linspace(0,Vmax,30)*FT/SEC
    
    Prop.CoefPlot(Alpha,fig = 1)
    Prop.PTPlot(N,V,h,'V', fig = 2)

#    N = npy.linspace(0, 13000,31)*RPM
#    V = npy.linspace(0,Vmax,5)*FT/SEC

#    Prop.PTPlot(N,V,h,'N', fig = 3)
    Prop.PlotTestData(fig=4)

    N = 4250*RPM
    print 'Static Thrust   : ', AsUnit(Prop.T(N,0*FT/SEC, h),'lbf')
    print 'Measured Thrust : ', AsUnit(max(npy.array(Prop.ThrustData)[:,1]),'lbf')
    N = 6410*RPM
    print

    pyl.show()
