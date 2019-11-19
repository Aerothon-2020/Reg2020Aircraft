from __future__ import division # let 5/2 = 2.5 rather than 2
#==============================================================================#
# TITLE
#==============================================================================#
# University of Cincinnati
# Aerocats - Regular Class 2016
# wing_elliptical.py: Aerothon wing definition
#
# update log:
#    11/07/2015 - shiggins: original version
#    11/13/2015 - shiggins: updates to links in IMPORTS
#    11/17/2015 - shiggins: changing number of sections to match ellip
#    12/09/2015 - shiggins: attempt to approx mass (pre-CAD)
#    12/11/2015 - shiggins: wing span bump to 106" following S&C studies
#    12/13/2015 - shiggins: wing span bump to 107" after getting even more greedy
#    01/14/2016 - shiggins: updating masses to match proto build
#    01/18/2016 - shiggins: transition to ATLAS
#    01/19/2016 - shiggins: aileron resizing (one rib less)
#
#    10/10/2016 - dechellis: modification to box wing for 2017 team
#    12/13/2016 - dechellis: modifications after first prototype, taper & increase aileron size
#    01/12/2017 - dechellis: tune model to P2 CAD mass, inertias, and CG
#==============================================================================#
# IMPORTS
#==============================================================================#
# import built-in modules
import os
import sys
sys.path.append(r"C:\eclipse\AircraftDesign\trunk")
from math import atan

# (USER) set-up directories
#trunkDir = r'C:\eclipse\workspace\AircraftDesign\trunk'
#BAPDir = os.path.join(trunkDir,r'Aircraft_Models\Reg2017Aircraft_BearcatAirlines\_backup\BAP-P2')

# link path to Aerothon
#sys.path.append(trunkDir)

# import Aerothon modules
from scalar.units import LBF, SEC, ARCDEG, FT, IN, SLUG, OZF, OZM
from scalar.units import AsUnit
from Aerothon.DefaultMaterialsLibrary import PinkFoam, Monokote, Basswood,\
     Balsa, Ultracote, Poplar, AluminumBalsa
from Aerothon.ACWing import ACMainWing
from Aerothon.ACWingWeight import ACSolidWing, ACRibWing 

#==============================================================================#
# WING MODEL
#==============================================================================#
# Create the wing
Wing = ACMainWing(1)
Wing.Airfoil = 'S1223'

# lift-off conditions
Wing.Lift_LO = 45*LBF  # 151107: shiggins guess
#Wing.V_Stall = 38 * FT/SEC #SPH: where does this come from?
Wing.Alt_LO = 197*FT # approximation for elevation in Ft. Worth, TX

# wing geometry (to launch 54.5 pounds under 200 feet)
Wing.b = 68.66*IN      # wing span
Wing.S = (29*68.66)*IN**2  # wing surface area (was 3695.04)
# More realistic 12 ft wing
#Wing.b = 144*IN      # wing span 
#Wing.S = 20*FT**2  # wing surface area

Wing.FullWing = True

# Wing Chord vs Position
### Box Wing
##Wing.Fb = [1.0 ] # Wingspan Position (0 to 1)
##chord = [1.0 ] # Chord at Position with relation to nominal chord
### Straight Tapered Wing
##Wing.Fb = [0.2, 1.0] # Wingspan Position (0 to 1)
##chord = [1.10, 0.6] # Chord at Position with relation to nominal chord
### Mid Tapered Wing
endChord = 0.681
Wing.Fb = [(84-30)/84.0, 1.0] # Wingspan Position (0 to 1)
chord = [1.0, endChord] # Chord at Position with relation to nominal chord

Wing.TR = []
Wing.Gam = []
Wing.Lam = []
for i in range(len(Wing.Fb)):
    if i==0:
        Wing.TR.append(1.0)
        Wing.Lam.append(0.0)
        Wing.Gam.append(0.0)
    elif i==len(Wing.Fb)-1:
        Wing.TR.append(chord[i]/chord[i-1])
        Wing.Lam.append(10*ARCDEG)
        Wing.Gam.append(0.0)
    else:    
        Wing.TR.append(chord[i]/chord[i-1])
        Wing.Lam.append(-3*ARCDEG)
        Wing.Gam.append(0.0)

# shiggins: this is dihedral for each section defined by Wing.Fb (invalid if ConstUpper == True)
Wing.ConstUpper = True #top surfaces of the airfoils lie against upper wing surf

#Wing.SweepFc = 0.75 # shiggins 151107: not sure how this is calculated
Wing.CEdge  = 'LE' #LE of wing to be tapered or constant LE, shiggins 151107: will override LAM

#==============================================================================#
# Aerodynamic properties
#==============================================================================#
# Finite wing correction factor: make 2D airfoil data match the 3D wing profile
Wing.FWCF = 0.98

# Oswald efficiency
Wing.o_eff = 0.97

# Polar slope evaluations
Wing.ClSlopeAt = (0*ARCDEG, 7*ARCDEG)
Wing.CmSlopeAt = (0*ARCDEG, 7*ARCDEG)

#==============================================================================#
# Control Surfaces
#==============================================================================#
# Define the control surfaces
Wing.AddControl('Aileron')
Wing.Aileron.Fc = 0.3 # chord length of the aileron, % of total chord
Wing.Aileron.Fb = (30.0/84.0) #Span of the aileron, (in long/in wingspan)
Wing.Aileron.Ft = 0. #Adjusted to make Aileron begin at a Wing rib
Wing.Aileron.SgnDup = -1.0

Wing.Aileron.Weight = 0.01*LBF
Wing.Aileron.WeightGroup = "MainWing"

Wing.Aileron.Servo.Fc     = 0.47
Wing.Aileron.Servo.Weight = 1.73*OZF 
Wing.Aileron.Servo.Torque = 145.80*IN*OZM
Wing.Aileron.Servo.WeightGroup = 'Controls'

#==============================================================================#
# Structural properties
#==============================================================================#
# -> set-up class to define weights for the wing (assuming structure is made of ribs)
Wing.SetWeightCalc(ACRibWing)

#--------------------------------- MAIN SPAR ----------------------------------#
SparW = 1*IN
SparH = 2*IN
CapThk = 1/8*IN
WebThk = 1/8*IN

CapArea = 2*SparW*CapThk
WebArea = 2*(SparH-(2*CapThk))*WebThk

AluminumBalsa.ForceDensity *= 1.317

# -> scaling the density down to get an accurate representation of weight based
#    on the builds
#    **main spar assumed to weigh from 14.5-16 ozf**
SparLinearDensity = WebArea*AluminumBalsa.ForceDensity*2.021 + \
                    CapArea*AluminumBalsa.ForceDensity*2.021

# TESTS SHOULD BE RUN TO VALIDATE DENSITY VALUES IN AEROTHON!!, shiggins 151107

# ** Try splitting the main spar definition into three spars to accurately **
#                      represent the taper at the ends

# -> generate WingWeight obj for the main spar using AddSpar in ACWingWeight
Wing.WingWeight.AddSpar("MainSpar", SparH, SparW, (.27, 0),1.0,\
                        DSpar=False,Mirror=False,Structural=True)

# -> assign material to WingWeight object (use Basswood as a base then adjust)
Wing.WingWeight.MainSpar.SparMat = AluminumBalsa.copy()
Wing.WingWeight.MainSpar.SparMat.LinearForceDensity = SparLinearDensity

# -> scale the cross sectional dimensions of the spar relative to wing thk
#    along the span of the spar; first entry is x (d1), second entry is z (d2)
Wing.WingWeight.MainSpar.ScaleToWing = [False, False]

# -> add main spar WingWeight object to the weight group for the main wing
Wing.WingWeight.MainSpar.WeightGroup = "MainWing"

#------------------------------- SECONDARY SPAR -------------------------------#
secondSparW = 0.5*IN
secondSparH = 0.5*IN
secondCapThk = 1/8*IN
secondWebThk = 1/8*IN

secondCapArea = 2.0*secondSparW*secondCapThk
secondWebArea = 2.0*(secondSparH-(2*secondCapThk))*secondWebThk

# -> scaling the density down to get an accurate representation of weight based
#    on the builds
#    **main spar assumed to weigh from 14.5-16 ozf**
secondSparLinearDensity = .5*secondWebArea*Balsa.ForceDensity + \
                          .5*secondCapArea*Balsa.ForceDensity

Wing.WingWeight.AddSpar("SecondSpar", 1/2*IN, 1/2*IN, (0.613,0), 1.0, \
                        DSpar=False, Mirror=False,Structural=True)
Wing.WingWeight.SecondSpar.SparMat = Balsa.copy()
Wing.WingWeight.SecondSpar.SparMat.LinearForceDensity = secondSparLinearDensity
Wing.WingWeight.SecondSpar.ScaleToWing = [False, False]
Wing.WingWeight.SecondSpar.WeightGroup = "MainWing"

#-------------------------------- LEADING EDGE --------------------------------#
Wing.WingWeight.AddSpar("LeadingEdge",1/16*IN, 1/4*IN, (0,1), 1.0, False)
Wing.WingWeight.LeadingEdge.SparMat= Balsa.copy()
Wing.WingWeight.LeadingEdge.Position = (0.006,0)
Wing.WingWeight.LeadingEdge.ScaleToWing = [False, False]
Wing.WingWeight.LeadingEdge.WeightGroup = "MainWing"

Wing.WingWeight.AddSpar("LeadingEdgeBent1", 1/16*IN, 5.5*IN, (0,1), 1.0, False)
Wing.WingWeight.LeadingEdgeBent1.SparMat = Balsa.copy()
Wing.WingWeight.LeadingEdgeBent1.Position = (0.066,-0.8)
Wing.WingWeight.LeadingEdgeBent1.ScaleToWing = [False,False]
Wing.WingWeight.LeadingEdgeBent1.WeightGroup = "MainWing"

Wing.WingWeight.AddSpar("LeadingEdgeBent2", 1/16*IN, 5.5*IN, (0,1), 1.0, False)
Wing.WingWeight.LeadingEdgeBent2.SparMat = Balsa.copy()
Wing.WingWeight.LeadingEdgeBent2.Position = (0.068,-0.5)
Wing.WingWeight.LeadingEdgeBent2.ScaleToWing = [False,False]
Wing.WingWeight.LeadingEdgeBent2.WeightGroup = "MainWing"

#------------------------------- TRAILING EDGE --------------------------------#
Wing.WingWeight.AddSpar("TrailingEdge1", 1/32*IN, 2*IN, (0,1), 1.0, False)
Wing.WingWeight.TrailingEdge1.SparMat = Balsa.copy()
Wing.WingWeight.TrailingEdge1.Position = (0.94,-0.1)
Wing.WingWeight.TrailingEdge1.ScaleToWing = [False,False]
Wing.WingWeight.TrailingEdge1.WeightGroup = "MainWing"

Wing.WingWeight.AddSpar("TrailingEdge2", 1/32*IN, 2*IN, (0,1), 1.0, False)
Wing.WingWeight.TrailingEdge2.SparMat = Basswood.copy()
Wing.WingWeight.TrailingEdge2.Position = (0.94,0.1)
Wing.WingWeight.TrailingEdge2.ScaleToWing = [False,False]
Wing.WingWeight.TrailingEdge2.WeightGroup = "MainWing"

#----------------------------------- RIBS -------------------------------------#
# Rib material (1/8in balsa)
BWRibMat = Balsa.copy()
BWRibMat.Thickness = .125*IN
##BWRibMat.ForceDensity *= 0.315 ##MASS## density based on rib weights prototype 01/14/2016 SPH

Wing.WingWeight.RibMat   = BWRibMat
#Wing.WingWeight.RibSpace = 28.0*IN
Wing.WingWeight.RibSpace = 6.0*IN

#------------------------------------ SKIN ------------------------------------#
# -> add skin material to the weight
Wing.WingWeight.SkinMat = Ultracote.copy()
Wing.WingWeight.SkinMat.AreaForceDensity *= 0.9 
Wing.WingWeight.SkinMat.Thickness = 0.002125*IN # measured 12/10/2015 shiggins

#-----------------------------------------------------------------------------#
Wing.WingWeight.WeightGroup = 'MainWing'

#==============================================================================#
# Visualization & Results
#==============================================================================#
if __name__ == '__main__':
    import pylab as pyl
        
    print "V lift off   : ", AsUnit(Wing.GetV_LO(),'ft/s')
    print "V stall      : ", AsUnit(Wing.V_Stall,'ft/s')
    print "Wing Area    : ", AsUnit(Wing.S,'in**2')
    print "Wing Span    : ", AsUnit(Wing.b,'in')
    print "Wing AR      : ", Wing.AR
    print "Wing MAC     : ", AsUnit(Wing.MAC(),'in')
    print "Wing Xac     : ", AsUnit(Wing.Xac(),'in')
    print "Wing dCM_da  : ", Wing.dCM_da()
    print "Wing dCL_da  : ", Wing.dCL_da()
    print "Lift off Load: ", AsUnit(Wing.Lift_LO,'lbf')
    print "Wing Thk     : ", AsUnit(Wing.Thickness(0*FT),'in')
    print "Root Chord   : ", AsUnit(Wing.Chord(0*FT),'in')
    print "Tip Chord    : ", AsUnit(Wing.Chord(0*FT)*endChord,'in')
    print "Wing Lift    : ", AsUnit(Wing.Lift_LO,'lbf')
    print "Wing MOI     : ", AsUnit(Wing.MOI(),'slug*ft**2')
    print
    print "WEIGHT CALCULATIONS"
    print "Main Spar Wt : ", AsUnit(Wing.WingWeight.MainSpar.Weight,'ozf')
    print "2nd  Spar Wt : ", AsUnit(Wing.WingWeight.SecondSpar.Weight,'ozf')
    print "L.E. Weight  : ", AsUnit(Wing.WingWeight.LeadingEdge.Weight+\
                                    Wing.WingWeight.LeadingEdgeBent1.Weight+\
                                    Wing.WingWeight.LeadingEdgeBent2.Weight,'ozf')
    print "T.E. Weight  : ", AsUnit(Wing.WingWeight.TrailingEdge1.Weight+\
                                    Wing.WingWeight.TrailingEdge2.Weight,'ozf')
    print "Rib Weight   : ", AsUnit(Wing.WingWeight.RibWeight(),'ozf')
    print "Skin Weight  : ", AsUnit(Wing.WingWeight.SkinWeight(),'ozf')
    print "Servos Weight: ", AsUnit(2*Wing.Aileron.Servo.Weight,'ozf')
    print "WING WEIGHT  : ", AsUnit(Wing.Weight,'ozf')
    print
   
    Wing.WriteAVLWing('BAPWing.avl')
        
    Wing.Draw(fig=1)
##    Wing.Draw3DWingPolars(fig=2)
##    Wing.Draw2DAirfoilPolars(fig=3)
##    
##    Wing.WingWeight.DrawRibs = True
##    Wing.WingWeight.DrawDetail = True
##    Wing.WingWeight.Draw(fig=4)
##    
    pyl.show()
