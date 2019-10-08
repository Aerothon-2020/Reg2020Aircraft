from __future__ import division # let 5/2 = 2.5 rather than 2
from scalar.units import LBF, SEC, ARCDEG, FT, IN, SLUG
from scalar.units import AsUnit
from Aerothon.ACWing import ACBiWing
from Aerothon.DefaultMaterialsLibrary import PinkFoam, Monokote, Basswood, Balsa, CarbonBar
from Aerothon.ACWingWeight import ACSolidWing, ACRibWing

#
# Create the wing
#
BoxWing = ACBiWing(1, 4, 5)
BoxWing.Lift_LO       = 35 * LBF
BoxWing.Lift_Ratio    = 0.5
BoxWing.V_max_climb   = 65 * FT/SEC
BoxWing.V_Stall       = 32.3 * FT/SEC
BoxWing.Alt_LO        = 920 * FT


###############################################################################
#
# Geometric properties
#
###############################################################################

BoxWing.FullWing = True

BoxWing.Gap        = 0.21
BoxWing.Stagger    = -.075

BoxWing.b             = 76.5*IN
#BoxWing.UpperWing.b   = 4.5*FT
#BoxWing.LowerWing.b   = 4*FT

BoxWing.LowerWing.TR      = [1,1]
BoxWing.LowerWing.Gam     = [0*ARCDEG, 0*ARCDEG]
BoxWing.LowerWing.Lam     = [0*ARCDEG, 0*ARCDEG]
BoxWing.LowerWing.Fb      = [0.6,1]

BoxWing.UpperWing.TR      = [1,1]
BoxWing.UpperWing.Gam     = [0*ARCDEG, 0*ARCDEG]
BoxWing.UpperWing.Lam     = [0*ARCDEG, 0*ARCDEG]
BoxWing.UpperWing.Fb      = [0.6,1]

#
# Create and Endplate 
#
BoxWing.CreateEndPlate()

#
# DO NOT specify an Fb of 1 for the end plate!!!
# An Fb of 1 is at the Upper Wing and does not need to be specified
#
BoxWing.EndPlate.Fb      = [0.5]
BoxWing.EndPlate.TR      = [0.5]
BoxWing.EndPlate.Gam     = [0*ARCDEG]
BoxWing.EndPlate.Lam     = [0*ARCDEG]
BoxWing.EndPlate.Symmetric = True
BoxWing.EndPlate.CEdge   = 'TE'


###############################################################################
#
# Aerodynamic properties
#
###############################################################################


#
# Set the airfoils
#
BoxWing.UpperWing.Airfoil = 'e423'
BoxWing.LowerWing.Airfoil = 'e423'
BoxWing.EndPlate.Airfoil =  'NACA0012'

#
# Set up the variation of Oswald efficiency vs. gap
#
BoxWing.GapInterp  = [0.1   ,0.2   ,0.3   ,0.4]
BoxWing.OeffInterp = [1.1832,1.3371,1.4617,1.5676]

#
# Determine the correct Biwing correction factor for the given wing
# TODO: Correct BWCFInterp
#
BoxWing.BWCFInterp     = [0.85,0.85,0.85,0.85]  #They assumed 85% lift to adjust for the biwing
BoxWing.LowerWing.FWCF = 1 
BoxWing.UpperWing.FWCF = 1

#
# Polar slope evaluations
#
BoxWing.ClSlopeAt = (0*ARCDEG, 1*ARCDEG)
BoxWing.CmSlopeAt = (0*ARCDEG, 1*ARCDEG)

BoxWing.LowerWing.ClSlopeAt = (6*ARCDEG, 7*ARCDEG)
BoxWing.LowerWing.CmSlopeAt = (-1*ARCDEG, 0*ARCDEG)

BoxWing.UpperWing.ClSlopeAt = BoxWing.LowerWing.ClSlopeAt
BoxWing.UpperWing.CmSlopeAt = BoxWing.LowerWing.CmSlopeAt

###############################################################################
#
# Control surfaces
#
###############################################################################

#
# Define the control surfaces
#
BoxWing.LowerWing.AddControl('Aileron')
BoxWing.LowerWing.Aileron.Fc = 0.25
BoxWing.LowerWing.Aileron.Fb = 0.42
BoxWing.LowerWing.Aileron.Ft = 0.2
BoxWing.LowerWing.Aileron.SgnDup = -1.

BoxWing.LowerWing.Aileron.Servo.Fc     = 0.3
BoxWing.LowerWing.Aileron.Servo.Weight = 0.01*LBF

###############################################################################
#
# Structural properties
#
###############################################################################
#
# Spar material (basswood, 1/4in width at max airfoil thickness + d-spar skin, balsa 1/16in)
#
sparw = 0.25*IN
Basswood = Basswood.copy()
Balsa    = Balsa.copy()
BoxWing.Refresh() # refresh so the thicknesses can be calculated
UWthick  = BoxWing.UpperWing.Thickness(0*FT)
LWthick  = BoxWing.LowerWing.Thickness(0*FT)
LsparFD  = Basswood.ForceDensity * sparw * LWthick
UsparFD  = Basswood.ForceDensity * sparw * UWthick
# Dspar density as balsa at 1/16in thick and the distance around the front of the airfoil
#  approximated as 2 times the airfoil thickness at the root
LDsparFD = Balsa.ForceDensity * 0.0625*IN * 2.0*LWthick
UDsparFD = Balsa.ForceDensity * 0.0625*IN * 2.0*UWthick 

#
# Rib material (1/8in balsa)
#
BWRibMat = Balsa.copy()
BWRibMat.Thickness = 0.125*IN

#BoxWing.LowerWing.SetWeightCalc(ACRibWing)
#BoxWing.LowerWing.WingWeight.SparMat.LinearForceDensity = LsparFD + LDsparFD
#BoxWing.LowerWing.WingWeight.SkinMat                    = Monokote.copy()
#BoxWing.LowerWing.WingWeight.RibMat                     = BWRibMat
#BoxWing.LowerWing.WingWeight.RibSpace                   = 6*IN

BoxWing.LowerWing.SetWeightCalc(ACSolidWing)
BoxWing.LowerWing.WingWeight.AddTubeSpar("MainSpar",0.75*IN,0.625*IN)
BoxWing.LowerWing.WingWeight.MainSpar.SparMat = CarbonBar.copy()
BoxWing.LowerWing.WingWeight.SkinMat                    = Monokote.copy()
BoxWing.LowerWing.WingWeight.WingMat                    = PinkFoam.copy()
BoxWing.LowerWing.WingWeight.WingMat.ForceDensity      *= 0.5

#BoxWing.UpperWing.SetWeightCalc(ACRibWing)
#BoxWing.UpperWing.WingWeight.SparMat.LinearForceDensity = UsparFD + UDsparFD
#BoxWing.UpperWing.WingWeight.SkinMat                    = Monokote.copy()
#BoxWing.UpperWing.WingWeight.RibMat                     = BWRibMat
#BoxWing.UpperWing.WingWeight.RibSpace                   = 6*IN

BoxWing.UpperWing.SetWeightCalc(ACSolidWing)
BoxWing.UpperWing.WingWeight.AddTubeSpar("MainSpar",0.75*IN,0.625*IN)
BoxWing.UpperWing.WingWeight.MainSpar.SparMat = CarbonBar.copy()
BoxWing.UpperWing.WingWeight.SkinMat                    = Monokote.copy()
BoxWing.UpperWing.WingWeight.WingMat                    = PinkFoam.copy()
BoxWing.UpperWing.WingWeight.WingMat.ForceDensity      *= 0.5

BoxWing.EndPlate.SetWeightCalc(ACSolidWing)
BoxWing.EndPlate.WingWeight.AddSpar("MainSpar",0.25*IN,0.125*IN)
BoxWing.EndPlate.WingWeight.MainSpar.SparMat = CarbonBar.copy()
BoxWing.EndPlate.WingWeight.SkinMat                    = Monokote.copy()
BoxWing.EndPlate.WingWeight.WingMat                    = PinkFoam.copy()
BoxWing.EndPlate.WingWeight.WingMat.ForceDensity      *= 0.4


if __name__ == '__main__':
    import pylab as pyl
    
    print "V lift of   : ", AsUnit( BoxWing.GetV_LO(), 'ft/s' )
    print "V stall     : ", AsUnit( BoxWing.V_Stall, 'ft/s' )
    print "Wing Area   : ", AsUnit( BoxWing.S, 'in**2' )
    print "Wing Span   : ", AsUnit( BoxWing.b, 'ft' )
    print "Wing AR     : ", BoxWing.AR
    print "Wing MAC    : ", AsUnit( BoxWing.MAC(), 'in' )
    print "Wing Xac    : ", BoxWing.Xac()
    print "Wing dCM_da : ", BoxWing.dCM_da()
    print "Wing dCL_da : ", BoxWing.dCL_da()
    print "Lift of Load: ", AsUnit( BoxWing.Lift_LO, 'lbf' )
    print "Wing BWFC   : ", BoxWing.BWCF()
    print
    print "Wing Thickness: ", BoxWing.LowerWing.Thickness(0*FT)
    print "Wing Chord    : ", BoxWing.LowerWing.Chord(0*FT)
    print "LowerWing Area: ", BoxWing.LowerWing.S
    print "UpperWing Area: ", BoxWing.UpperWing.S
    print "LowerWing lift: ", BoxWing.LowerWing.Lift_LO
    print "UpperWing lift: ", BoxWing.UpperWing.Lift_LO
    print
    print "Wing Weight : ",  AsUnit( BoxWing.Weight, 'lbf' )
    print "Wing MOI    : ",  AsUnit( BoxWing.MOI(), 'slug*ft**2' )
    print
    print "LowerWing Weight : ", BoxWing.LowerWing.Weight
    print "UpperWing Weight : ", BoxWing.UpperWing.Weight
    print "EndPlate Weight  : ", BoxWing.EndPlate.Weight
    
    BoxWing.WriteAVLWing('BoxWing.avl')
    
#    BoxWing.LowerWing.Draw3DWingPolars(fig=7)
#    BoxWing.LowerWing.Draw2DAirfoilPolars(fig=6)
#
#    BoxWing.UpperWing.Draw3DWingPolars(fig=5)
#    BoxWing.UpperWing.Draw2DAirfoilPolars(fig=4)
#    
#    BoxWing.Draw3DWingPolars(fig=3)
#    BoxWing.Draw2DAirfoilPolars(fig=2)

    BoxWing.Draw(fig = 1)
    pyl.show()