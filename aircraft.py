from __future__ import division # let 5/2 = 2.5 rather than 2
#==============================================================================#
# TITLE
#==============================================================================#
# University of Cincinnati
# Aerocats - Regular Class 2016
# _aircraft_BAP.py: Aerothon aircraft definition
#
# update log:
#    11/07/2015 - shiggins: original version
#    11/11/2015 - shiggins: updates with comments to make more user friendly
#    11/13/2015 - shiggins: updates to links in IMPORTS
#    11/22/2015 - shiggins: added MJZ approximations for tails
#                           updated mass properties to more accurately match CAD
#    12/02/2015 - shiggins: updating mass distribution
#    12/10/2015 - shiggins: continuing mass updates
#    12/11/2015 - shiggins: dimensions for control surfaces adjusted
#                           positions of control surfaces adjusted
#                           stable in S&C ControlsTable.py (MJZ)
#    01/14/2016 - shiggins: resized control surfs on tail to 50% chord to match
#                           prototype build
#                           mass not updated to match build just yet (DO NOT USE FOR FLIGHT PREDICTION)
#                           design & results presented @ CDR 01/14/2016
#    01/15/2016 - shiggins: further updates based on build measurements/masses
#                           to allow for accurate stab characteristics moving
#                           into test flight occurring 01/16/2016
#    01/18/2016 - shiggins: transition to ATLAS configuration following the
#                           prototype test flight on 01/16/2016
#    01/19/2016 - shiggins: tail redesign (for ATLAS)
#                           -> reduction in horiz stab span
#                           -> reduction in vert  stab span
#                           -> reduction in control surf sizing
#
#    10/06/2016 - dechellis: begin modifications for 2017 team
#                           -> increase payload to 40 lbs for preliminary TO distance estimation
#    10/26/2016 - dechellis: Increase GTOW to 54.5 lbs, modify tail to conventional tail configuration
#    11/14/2016 - dechellis: modify tail size and placement to match prototype 1 CAD
#    12/13/2016 - dechellis: increase rudder chord based on P1 flight test comments
#==============================================================================#
# IMPORTS
#==============================================================================#
# import built-in modules
import os
import sys
import time
import pylab as pyl
import cmath as math

# (USER) set-up directories
#trunkDir = r'C:\eclipse\AircraftDesign\trunk'
#BAPDir = os.path.join(trunkDir,r'Aircraft_Models\Reg2018Aircraft_UCBearForce')

# link path to Aerothon
##sys.path.append(trunkDir)

# import Aerothon modules
from scalar.units import M, FT, IN, ARCDEG, RAD, LBF, SEC, KG, SLUG, OZF, gacc,\
     GRAM, OZM
from scalar.units import AsUnit
from Aerothon.DefaultMaterialsLibrary import Monokote, Basswood,\
     Steel, Balsa, Aluminum, Ultracote
from Aerothon.ACAircraft import ACTailAircraft
#from Aerothon.ACTLenAircraft import ACTLenAircraft
from Aerothon.ACWingWeight import ACRibWing

# (USER) import Aerothon components
#sys.path.append(os.path.join(BAPDir,r'Aerodynamics\Wing'))
from Aerodynamics.Wing.BiWing import BoxWing # wing model

#sys.path.append(os.path.join(BAPDir,'Propulsion'))
from Propulsion.propulsion import Propulsion # propulsion model

#sys.path.append(os.path.join(BAPDir,r'Structures\Fuselage'))
from Structures.Fuselage.fuselage import Fuselage # fuselage model

timeStart = time.time() # start clock (to time simulation)

#==============================================================================#
# AIRCRAFT MODEL
#==============================================================================#
# Create the Aircraft from the ACTailAircraft class imported above from Aerothon
Aircraft = ACTailAircraft()
#Aircraft = ACTLenAircraft()
Aircraft.name = 'Turbo Time'

# Assign parts we imported above (generated outside of this script) to aircraft
Aircraft.SetWing(BoxWing)
Aircraft.SetFuselage(Fuselage)
Aircraft.SetPropulsion(Propulsion)

# Wing alignment
Aircraft.WingFuseFrac = 0.44 # 0.0 @ bottom of fuselage; 1.0 @ top of fuselage
#Aircraft.Wing.i = 0*ARCDEG   # induced angle of attack, wing incidence

# Engine alignment (height)
Aircraft.EngineAlign = 0.72

# Aircraft Properties
EmptyWeight = 20*LBF # dechellis: estimated airframe weight
SoccerBalls = 1.0
BallWeight = 1.0*LBF
StaticWeight = 30.0*LBF
PayloadWeight = (SoccerBalls*BallWeight)+StaticWeight
Fuselage.PayBay.SoccerBalls.Weight = BallWeight*SoccerBalls
Fuselage.PayBay.StaticPayload.Weight = StaticWeight
#TennisBalls = 60.0 # dechellis: number of tennis balls flying
#BallWeight = 0.131333*LBF # dechellis: weight of 1 tennis ball
#PayloadWeight = (0.50*LBF+BallWeight)*TennisBalls # dechellis: "passenger luggage"
#Fuselage.PayBay.TennisBalls.Weight = BallWeight*TennisBalls # Reassign tennis ball weight distribution based off desired loading
Aircraft.TotalWeight = PayloadWeight + EmptyWeight # needed for calculations
Aircraft.TippingAngle = 10*ARCDEG # Black line on AC plot, set to Lift Off AoA
Aircraft.RotationAngle = 15*ARCDEG # Red line on AC plot, recommend 15 deg
Aircraft.Alpha_Groundroll = 0*ARCDEG # AOA during ground roll

Aircraft.CMSlopeAt = (2 * ARCDEG, 10 * ARCDEG)    # shiggins: what does this do? 
Aircraft.CLSlopeAt = (3 * ARCDEG, 14 * ARCDEG)    # shiggins: what does this do?
Aircraft.CLHTSlopeAt = (-5 * ARCDEG, 10 * ARCDEG) # shiggins: what does this do?
Aircraft.DWSlopeAt = (3 * ARCDEG, 15 * ARCDEG)    # shiggins: what does this do?

Aircraft.Alpha_Zero_CM = 5.0 * ARCDEG # for steady level flight
Aircraft.StaticMargin = 0.1 # shiggins: this is driving wing position (higher values move the wing farther aft)
Aircraft.WingXMaxIt = 60 # shiggins: this is the no. of iterations to solve

Aircraft.VmaxPlt = 60*FT/SEC # Maximum velocity for plotting purposes

Aircraft.RotationTime = 0.5*SEC # Est time aircraft rotates on ground during takeoff

#==============================================================================#
# HORIZONTAL TAIL
#==============================================================================#
HTail = Aircraft.HTail # set up the horizontal tail class
HTail.Airfoil = 'NACA0012'

Aircraft.HTailPos = 0.0 # T-Tail = 1 (horiz tail at top of vert tail);
                        # reg    = 0 (horiz tail at same lvl as middle of tail bulk)

HTail.FullWing = True # Full wing surface (i.e. top and bottom tail)
HTail.Inverted = True # Invert the airfoil section

HTail.b = 49.2 * IN # horizontal tail span #MJZ was 50 in sholsinger
#HTail.S = 590.4 * IN**2 # horizontal tail planform area was 600 in**2 sholsinger
HTail.S =  650 * IN**2 # horizontal tail planform area was 600 in**2 sholsinger
HTail.L = 56*IN   # horizontal tail "length", dist back from wing AC
HTail.TR = 1.0 # horizontal tail taper ratio
HTail.o_eff = 0.97 # horizontal tail oswald #MJZ

HTail.SweepFc  = 1.0 - HTail.Elevator.Fc # sweep bout hinge, (Elevator LE straight)
HTail.DWF = 1.4 # Main wing Down wash factor (b/w 1 (close to wing), 2 (far away))

HTail.ClSlopeAt = (-10*ARCDEG, 10*ARCDEG) #SPH: what is this actually doing?
HTail.CmSlopeAt = (-4*ARCDEG, 5*ARCDEG) #SPH: what is this actually doing?

# Elevator properties
HTail.Elevator.Fc = 0.50 # Elevator chord (% chord)
HTail.Elevator.Fb = 1.0 # Elevator span (% span)
HTail.Elevator.Ft = 0.0 # Start of the aileron (% span)
HTail.Elevator.Weight = 2.8*OZF # ##MASS##: matches prototype build 01/14/2016 SPH
HTail.Elevator.WeightGroup = 'HTail'

HTail.Elevator.Servo.Fc  = 0.363 # c.g. of servo matches proto build 01/14/2016 SPH
HTail.Elevator.Servo.Fbc = 0.0
HTail.Elevator.Servo.Weight = 1.58*OZF ##MASS## measured for proto build 01/15/2016 SPHHTail.Elevator.Servo.WeightGroup = 'Controls'
HTail.Elevator.Servo.Torque = 152*IN*OZM # 2 servos on elevator @76 IN*OZM each

# Structural properties
# Spar taken as 1/8 inch width and thickness of the max thickness at the root
Basswood = Basswood.copy()
RibMat = Balsa.copy()
RibMat.Thickness = 1/8 * IN
RibMat.ForceDensity *= 0.425*0.85 # assuming 50% rib area cut-out

HTail.SetWeightCalc(ACRibWing)
HTail.WingWeight.RibMat = RibMat
HTail.WingWeight.RibSpace = 4.0 * IN

HTail.WingWeight.SkinMat = Ultracote.copy()
HTail.WingWeight.SkinMat.AreaForceDensity *= 0.5 # shiggins: based on measurements
HTail.WingWeight.SkinMat.Thickness = 0.002125 * IN # shiggins: based on measurements
HTail.WingWeight.WeightGroup = 'HTail'

HTail.WingWeight.AddSpar('MainSpar', 0.5*IN, 0.75*IN, (0.25,1),1.0, False)
HTail.WingWeight.MainSpar.SparMat = Basswood.copy()
HTail.WingWeight.MainSpar.SparMat.LinearForceDensity = 0.83*0.078125*OZF/IN # = Balsa.copy()
HTail.WingWeight.MainSpar.Position = (0.45,0.55)
HTail.WingWeight.MainSpar.ScaleToWing = [False, False]
HTail.WingWeight.MainSpar.WeightGroup = "HTail"

HTail.WingWeight.AddSpar('LeadingEdge', 1/32*IN, 1.25*IN, (0.25,1),1.0, False)
HTail.WingWeight.LeadingEdge.SparMat = Balsa.copy() #.LinearForceDensity = .008*LBF/(1*IN)
HTail.WingWeight.LeadingEdge.Position = (0.45,0.55)
HTail.WingWeight.LeadingEdge.ScaleToWing = [False, False]
HTail.WingWeight.LeadingEdge.WeightGroup = "HTail"

HTail.WingWeight.AddSpar('TrailingEdge1', 1/32*IN, 2*IN, (0.25,1),1.0, False)
HTail.WingWeight.TrailingEdge1.SparMat = Balsa.copy() #.LinearForceDensity = .008*LBF/(1*IN)
HTail.WingWeight.TrailingEdge1.Position = (0.45,0.55)
HTail.WingWeight.TrailingEdge1.ScaleToWing = [False, False]
HTail.WingWeight.TrailingEdge1.WeightGroup = "HTail"

HTail.WingWeight.AddSpar('TrailingEdge2', 1/32*IN, 2*IN, (0.25,1),1.0, False)
HTail.WingWeight.TrailingEdge2.SparMat = Balsa.copy() #.LinearForceDensity = .008*LBF/(1*IN)
HTail.WingWeight.TrailingEdge2.Position = (0.45,0.55)
HTail.WingWeight.TrailingEdge2.ScaleToWing = [False, False]
HTail.WingWeight.TrailingEdge2.WeightGroup = "HTail"

#==============================================================================#
# VERTICAL TAIL
#==============================================================================#
# VERTICAL TAIL
VTail = Aircraft.VTail
VTail.Airfoil = 'NACA0012'

Aircraft.VTailPos = 0.0 # spanwise along the horiz tail semi-span
VTail.Axis    = (0.0, 1.0) # (0,1) full wing (or vert above centerline); (0,-1) for vert below centerline

VTail.L       = HTail.L # match the LE of the horiz and vert tails
VTail.S       = 222.5 * IN**2 
VTail.b       = 20 * IN
VTail.TR      = 0.85417

VTail.o_eff   = 0.96

VTail.FullWing = False # top and bottom of centerline
VTail.Symmetric = False # duplicates the vtail on the opposite side of tail

# Rudder properties
VTail.Rudder.Fc = 0.50 # percent of vertical tail used by rudder
VTail.Rudder.Fb = 1.0 # span of the rudder (percent span of vtail)
VTail.Rudder.Ft = 0.0 # start of the rudder (percent span of vtail)
VTail.Rudder.Weight = 0.5*OZF # ##MASS##: matches prototype build 01/14/2016 SPH
VTail.Rudder.WeightGroup = "VTail"
VTail.Rudder.SgnDup    = -1.0 # ??? #SPH 11/17/2015
VTail.Rudder.Servo.Fc  = 0.32 # fraction of vtail chord, matches prototype build 01/14/2016 SPH
VTail.Rudder.Servo.Fbc = 0.17 # matches prototype build 01/14/2016 SPH
VTail.Rudder.Servo.Weight = 0.85 * OZF ##MASS##: matches prototype build 01/14/2016 SPH
VTail.Rudder.Servo.WeightGroup = "Controls"
VTail.Rudder.Servo.Torque = 76*IN*OZM # matches prototype build 01/14/2016 SPH
VTail.SweepFc = VTail.TR #sweep bout rudder hinge 

# Structural properties
VTail.SetWeightCalc(ACRibWing)
VTail.WingWeight.RibMat = RibMat # properties assigned above in htail
VTail.WingWeight.RibSpace = 5.0 * IN

VTail.WingWeight.SkinMat = Ultracote.copy()
VTail.WingWeight.SkinMat.AreaForceDensity *= 0.5 # shiggins: based on measurements
VTail.WingWeight.SkinMat.Thickness = 0.002125*IN  # shiggins: based on measurements

VTail.WingWeight.WeightGroup = 'VTail'

VTail.WingWeight.AddSpar("MainSpar", 0.5*IN, 0.75*IN, (0.25,1),1.0, False)
VTail.WingWeight.MainSpar.SparMat = Basswood.copy()
VTail.WingWeight.MainSpar.SparMat.LinearForceDensity = 0.83*0.078125*OZF/IN #= Balsa.copy()
VTail.WingWeight.MainSpar.Position = (0.45,0)
VTail.WingWeight.MainSpar.ScaleToWing = [False, False]
VTail.WingWeight.MainSpar.WeightGroup = "VTail"

VTail.WingWeight.AddSpar("LeadingEdge", 1/8*IN, 1/4*IN, (0.25,1),1.0, False)
VTail.WingWeight.LeadingEdge.SparMat = Balsa.copy() #.LinearForceDensity = .008*LBF/(1*IN)
VTail.WingWeight.LeadingEdge.Position = (0.008,0)
VTail.WingWeight.LeadingEdge.ScaleToWing = [False, False]
VTail.WingWeight.LeadingEdge.WeightGroup = "VTail"

VTail.WingWeight.AddSpar("TrailingEdge1", 1/32*IN, 0.5*IN, (0.25,1),1.0, False)
VTail.WingWeight.TrailingEdge1.SparMat = Balsa.copy() #.LinearForceDensity = .008*LBF/(1*IN)
VTail.WingWeight.TrailingEdge1.Position = (0.915,0.2)
VTail.WingWeight.TrailingEdge1.ScaleToWing = [False, False]
VTail.WingWeight.TrailingEdge1.WeightGroup = "VTail"

VTail.WingWeight.AddSpar("TrailingEdge2", 1/32*IN, 0.5*IN, (0.25,1),1.0, False)
VTail.WingWeight.TrailingEdge2.SparMat = Balsa.copy() #.LinearForceDensity = .008*LBF/(1*IN)
VTail.WingWeight.TrailingEdge2.Position = (0.915,-0.2)
VTail.WingWeight.TrailingEdge2.ScaleToWing = [False, False]
VTail.WingWeight.TrailingEdge2.WeightGroup = "VTail"

#==============================================================================#
# LANDING GEAR
#==============================================================================#
# set material variables
Aluminum = Aluminum.copy()
Steel    = Steel.copy()

MainGear = Aircraft.MainGear # set main gear class
MainGear.GearHeight   = 8.698 * IN
##MainGear.StrutL       = 1 * IN # with theta = 0 set to distance axle sits below payload bay
##MainGear.StrutW       = 0.2 * IN
##MainGear.StrutH       = 0.1 * IN
MainGear.WheelDiam    = 6.0 * IN    # Changed Wheel Diameter to account for AC Tipping Angle
MainGear.WheelThickness = 0.25*IN
MainGear.Theta = 0.0*ARCDEG # for gear angle (strut)
MainGear.X[1] = 7.0 * IN # distance from center in y (shiggins: I am overriding the default calc here)
MainGear.Strut.Weight = 5.68*OZF 
MainGear.Strut.WeightGroup = "LandingGear"
MainGear.Wheel.Weight = 3.0*OZF # shiggins: guess for now
MainGear.Wheel.WeightGroup = "LandingGear"

NoseGear = Aircraft.NoseGear # set nose gear class
NoseGear.StrutW    = 0.1 * IN
NoseGear.StrutH    = 0.1 * IN
NoseGear.WheelDiam = 2 * IN

NoseGear.Strut.Weight = 3.0*OZF # shiggins: guess for now
NoseGear.Strut.WeightGroup = "LandingGear"
NoseGear.Wheel.Weight = 1.0*OZF # shiggins: guess for now
NoseGear.Wheel.WeightGroup = "LandingGear"

#==============================================================================#
# VISUALIZATION & RESULTS
#==============================================================================#
print 'Aircraft created'

if __name__ == '__main__':
  
    print
    print 'AIRCRAFT PERFORMANCE'
    print 'Aircraft   V_LO : ', AsUnit(Aircraft.Wing.GetV_LO(),'ft/s')
    print 'Wing       V_LO : ', AsUnit(Aircraft.Wing.GetV_LO(),'ft/s')
    #print 'V max climb     : ', AsUnit(Aircraft.self.V_max_climb(),'ft/s')
    #print 'V max           : ', AsUnit(Aircraft.Wing.Vmax(),'ft/s')
    print 'Ground Roll     : ', AsUnit(Aircraft.Groundroll(),'ft')
    print 'Lift of AoA     : ', AsUnit(Aircraft.GetAlphaFus_LO(),'deg')
    print 'Zero CM AoA     : ', AsUnit(Aircraft.Alpha_Zero_CM,'deg')
    print
    print 'WING'
    print 'Wing X          : ', AsUnit(Aircraft.Wing.X[0],'in')
    print 'Wing Y          : ', AsUnit(Aircraft.Wing.X[1],'in')
    print 'Wing Z          : ', AsUnit(Aircraft.Wing.X[2],'in') 
    print 'Wing Height     : ', AsUnit(Aircraft.Wing.Upper(0*IN),'in')
    print
    print 'TAIL'
    print 'Vertical Tail H : ', AsUnit(Aircraft.VTail.Tip()[2],'in' )
    print 'HTail Incidence : ', AsUnit(Aircraft.HTail.i,'deg')
    print 'HTail  VC       : ', AsUnit(Aircraft.HTail.VC) 
    print 'VTail  VC       : ', AsUnit(Aircraft.VTail.VC)
    print 'VTail Area      : ', AsUnit(Aircraft.VTail.S,'in**2')
    print 'HTail Area      : ', AsUnit(Aircraft.HTail.S,'in**2')
    print 'HTail Length    : ', AsUnit(Aircraft.HTail.L,'in')
    print
    print '---------- WEIGHT BREAKDOWN ----------'
    print 'Total Weight    : ', AsUnit(Aircraft.TotalWeight,'lbf')
    print 'Empty Weight    : ', AsUnit(EmptyWeight,'lbf')
    print 'Payload Weight  : ', AsUnit(Aircraft.TotalWeight-EmptyWeight,'lbf')
    print
    print 'HORIZ TAIL      : ', AsUnit(Aircraft.HTail.Weight,'ozf')
    print '   Spar Weight  : ', AsUnit(Aircraft.HTail.WingWeight.MainSpar.Weight,'ozf')
    print '   L.E. Weight  : ', AsUnit(Aircraft.HTail.WingWeight.LeadingEdge.Weight,'ozf')
    print '   T.E. Weight  : ', AsUnit(Aircraft.HTail.WingWeight.TrailingEdge1.Weight+\
                                       Aircraft.HTail.WingWeight.TrailingEdge2.Weight,'ozf')
    print '   Rib  Weight  : ', AsUnit(Aircraft.HTail.WingWeight.RibWeight(),'ozf')
    print '   Skin Weight  : ', AsUnit(Aircraft.HTail.WingWeight.SkinWeight(),'ozf')
    print '   Servo Weight : ', AsUnit(Aircraft.HTail.Elevator.Servo.Weight,'ozf')
    print
    print 'VERT  TAIL      : ', AsUnit(Aircraft.VTail.Weight,'ozf')
    print '   Spar Weight  : ', AsUnit(Aircraft.VTail.WingWeight.MainSpar.Weight,'ozf')
    print '   L.E. Weight  : ', AsUnit(Aircraft.VTail.WingWeight.LeadingEdge.Weight,'ozf')
    print '   T.E. Weight  : ', AsUnit(Aircraft.VTail.WingWeight.TrailingEdge1.Weight+\
                                       Aircraft.VTail.WingWeight.TrailingEdge2.Weight,'ozf')
    print '   Rib  Weight  : ', AsUnit(Aircraft.VTail.WingWeight.RibWeight(),'ozf')
    print '   Skin Weight  : ', AsUnit(Aircraft.VTail.WingWeight.SkinWeight(),'ozf')
    print '   Servo Weight : ', AsUnit(Aircraft.VTail.Rudder.Servo.Weight,'ozf')
    print
    print 'FUSELAGE        : ', AsUnit(Aircraft.Fuselage.Weight,'ozf')
    print 
    print
    print 'WING            : ', AsUnit(Aircraft.Wing.Weight,'ozf')
    print
    print "LowerWing Weight : ", BoxWing.LowerWing.Weight
    print "UpperWing Weight : ", BoxWing.UpperWing.Weight
    print "EndPlate Weight  : ", BoxWing.EndPlate.Weight
##
    ######### SPH: ADD THESE OUTPUTS ##########
    #Cn beta, Cm alpha, Cl beta
 
    Aircraft.Draw()
    Aircraft.WriteAVLAircraft('BAP.avl')  
    
    Aircraft.PlotPolarsSlopes(fig=2)
    Aircraft.PlotCMPolars(3, (-10*ARCDEG, -5*ARCDEG, 0*ARCDEG, +5*ARCDEG, +10 * ARCDEG), XcgOffsets=(+0.05, -0.05))
    # CG LIMITS: AFT = +12%, FWD = -22%
    HTail.Draw2DAirfoilPolars(fig=4)
    Aircraft.PlotCLCMComponents(fig = 5, del_es = (-10*ARCDEG, -5*ARCDEG, 0*ARCDEG, +5*ARCDEG, +10 * ARCDEG))
    Aircraft.PlotPropulsionPerformance(fig=6)

    VTail.WingWeight.DrawRibs = True
    VTail.WingWeight.DrawDetail = True
    #VTail.WingWeight.Draw(fig = 7)
    #VTail.Draw(fig = 8)

    HTail.WingWeight.DrawRibs = True
    HTail.WingWeight.DrawDetail = True
    #HTail.WingWeight.Draw(fig = 9)
    #HTail.Draw(fig = 10)
    
    timeEnd = time.time()
    print 
    print('Aircraft calculations complete. Time elapsed: ' +\
          str(round(timeEnd-timeStart,3)))
    pyl.show()

