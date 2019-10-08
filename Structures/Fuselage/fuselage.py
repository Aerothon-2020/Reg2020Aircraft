from __future__ import division # let 5/2 = 2.5 rather than 2
#==============================================================================#
# TITLE
#==============================================================================#
# University of Cincinnati
# Aerocats - Regular Class 2017
# fuselage.py: Aerothon fuselage definition
#
# update log:
#    11/07/2015 - shiggins: original version (using old configuration)
#    11/11/2015 - shiggins: modifying to mimic bAIRcats configuration
#    11/14/2015 - shiggins: modifying fuselage design (and conforming a bit)
#                           need to make payload bay section large enough to
#                           house payload in its entirely
#    12/01/2015 - shiggins: updating mass dist and dim to better match CAD
#    12/10/2015 - shiggins: hacked ACFuselage to define payload properly
#                           also made some changes to positions of some things
#                           added nose gear servo and radio receiver
#    12/11/2015 - shiggins: updating fuselage length to match S&C Mike found
#                           **need to verify mass after build of test struct**
#    01/18/2015 - shiggins: transition to ATLAS
#    01/20/2015 - shiggins: widening the fuselage (paybay to tail)
#                           adjusting heights/lengths to maximize dimensions
#
#    10/20/2016 - dechellis: begin initial modifications for 2017 aircraft
#    11/18/2016 - dechellis: model fuselage to prototype 1, match CG and MOI
#                            to CAD
#    12/19/2016 - dechellis: adjustment to back of fuse to raise horiz tail to
#                            keep out of wing downwash from P1 flight testing,
#                            change fuse bottom for carbon gear, lengthen nose
#    01/12/2017 - dechellis: tuning of fue  mass, inertias, and CG to match P2 CAD
#==============================================================================#
# IMPORTS
#==============================================================================#
# import built-in modules
import os
import sys
trunkDir = r'C:\eclipse\workspace\AircraftDesign\trunk'
BAPDir = os.path.join(trunkDir,r'Aircraft_Models\Reg2017Aircraft_BearcatAirlines\BAP')

# link path to Aerothon
sys.path.append(trunkDir)

# import Aerothon modules
from scalar.units import IN, LBF, SLUG, FT, GRAM, gacc, OZF
from scalar.units import AsUnit
from Aerothon.ACFuselage import ACFuselage
from Aerothon.DefaultMaterialsLibrary import Basswood, Balsa, AircraftPly, Monokote,\
     Steel, Ultracote

#==============================================================================#
# REVAMPED AEROTHON CLASSES
#==============================================================================#
from Aerothon.ACFuselage_dechellis import ACFuselage
#==============================================================================#
# FUSELAGE MODEL
#==============================================================================#
# NOTES:
#    So Aerothon does some funny business here that will not match our CAD
#    perfectly, so we consider only the outer edges of the fuselage and then
#    will adjust densities of the materials being used such that the CG
#    representations match that in the CAD (and tests from prototype builds)
#
# We break the fuselage into the following sections:
# (1) Nose:     Front cap of the plane with motor bay over top of it
# (2) PayBay:   Payload bay (w/ext above for ties to main and secondary spars)
# (3) Pay2Tail: Transition from payload bay to tail
# (4) Tail:     Tail section
# (5) TailBrac: Tail bracket (to connect tail to fuselage)

Fuselage = ACFuselage() # create the fuselage class

# Create the sections of the fuselage that we intend to populate
# -> AddSection('NAME',sectionLength,alignment(-1=bot, 0=center, 1=top, None=@CG)
Fuselage.AddSection('Nose',9.125*IN,1) 
Fuselage.AddSection('PayBay',19.625*IN,1)
Fuselage.AddSection('Pay2Tail',35.0*IN,0)
Fuselage.AddSection('Tail',17.375*IN,0)
BaseWeight = 24*OZF # Weight in OZF that is multiplied in the force densities

# SECTION 1: Nose section only -------------------------------------------------#
#### SHIFT ALL X POSITIONS BY 7.03125in (Dist from payload CG to front of fuse)

# SPH 12/1/2015: from 151130 CAD target weight @ 15.5oz CG @ 1.14125in
# in SolidWorks relative to payload CG (5.89,0,-0.12)
 
# front bulkhead definition
Fuselage.Nose.FrontBulk.Width = 2.0*IN
Fuselage.Nose.FrontBulk.Height = 2.0*IN
Fuselage.Nose.FrontBulk.Material = AircraftPly.copy()
Fuselage.Nose.FrontBulk.Material.AreaForceDensity = (0.01*BaseWeight)/(2.0*IN*2.0*IN)
Fuselage.Nose.FrontBulk.WeightGroup = 'Fuselage'

# rear bulkhead definition
Fuselage.Nose.BackBulk.Width = 7.75*IN
Fuselage.Nose.BackBulk.Height = 7.75*IN
Fuselage.Nose.BackBulk.Material = AircraftPly.copy()
Fuselage.Nose.BackBulk.Material.AreaForceDensity = (0.03*BaseWeight)/(7.75*IN*7.75*IN)
Fuselage.Nose.BackBulk.WeightGroup = 'Fuselage'

# miscellaneous
Fuselage.Nose.SkinMat = Ultracote.copy()
Fuselage.Nose.StringerMat = Basswood.copy()
Fuselage.Nose.StringerMat.LinearForceDensity = 0.005*LBF/IN
Fuselage.Nose.Align = 3.978 # Top of section relative to thrust line (z=0)
Fuselage.Nose.WeightGroup = 'Fuselage'

# Add components to the fuselage
# add nose wheel servo
Fuselage.Nose.AddComponent("NoseWheelServo",0.05*LBF,(1.14*IN,1.18*IN,0.51*IN),"Front",(0.8,0.5,0.05))
Fuselage.Nose.NoseWheelServo.WeightGroup = "Controls"

Fuselage.Nose.AddComponent('MotorBattery',0.93125*LBF,(5.5*IN,1.75*IN,1.5*IN),'Back',(-0.4,0.7,0.685)) #
Fuselage.Nose.AddComponent('SpeedController', 0.28*LBF,(0.75*IN,1.5*IN,2.0*IN),'Right',(0.4,0.3,0.7)) #SPH: placeholder for now

Fuselage.Nose.AddComponent    ("Receiver"      , 0.030*LBF, (1.86*IN,0.56*IN,1.61*IN)     , "Bottom"   , (0.5 , 0.2, 0.5) )
Fuselage.Nose.Receiver.WeightGroup = "Controls"

Fuselage.Nose.MotorBattery.WeightGroup = 'Propulsion'

Fuselage.Nose.SpeedController.WeightGroup = 'Propulsion'

# SECTION 2: Payload bay section ----------------------------------------------#

# SPH 12/1/2015: target weight from 151130 CAD @ 8.8oz and CG @ 6.48125
# in SolidWorks relative to payload CG (0.55,0.00,-0.99)

# front bulkhead definition(matches the nose cross-sectional dimension)
Fuselage.PayBay.FrontBulk.Width = 7.75*IN
Fuselage.PayBay.FrontBulk.Height = 7.75*IN
Fuselage.PayBay.FrontBulk.Material = AircraftPly.copy()
Fuselage.PayBay.FrontBulk.Material.AreaForceDensity = (0.05*BaseWeight)/(7.75*IN*7.75*IN)
Fuselage.PayBay.FrontBulk.WeightGroup = 'Fuselage'

# rear bulkhead definition (matches the cross-sectional dimension of the nose and payload bay together)
Fuselage.PayBay.BackBulk.Width = 7.5*IN
Fuselage.PayBay.BackBulk.Height = 10*IN #Help
Fuselage.PayBay.BackBulk.Material = AircraftPly.copy()
Fuselage.PayBay.BackBulk.Material.AreaForceDensity = (0.1*BaseWeight)/(7.5*IN*7.25*IN)
Fuselage.PayBay.BackBulk.WeightGroup = 'Fuselage'

# miscellaneous
Fuselage.PayBay.SkinMat = Ultracote.copy()
Fuselage.PayBay.WeightGroup = 'Fuselage'
Fuselage.PayBay.StringerMat = AircraftPly.copy()
Fuselage.PayBay.StringerMat.LinearForceDensity = 0.01*LBF/IN
Fuselage.PayBay.Align = 1.0 # Top of section relative to previous section

# tennis ball size and weight insertion
Fuselage.PayBay.AddComponent    ("TennisBalls"      , 0.0*LBF, (57.75*IN,7.5*IN,2.5*IN)     , "Front"   , (0.5 , 0.5, 0.88) )
Fuselage.PayBay.TennisBalls.WeightGroup = "Fuselage"


# SECTION 3: Payload bay and tail section -------------------------------------#

# SPH 12/1/2015: target weight from 151130 CAD @ 1.12oz and CG @ 13.19125
# in SolidWorks relative to payload CG (-6.16,0,-1.73)

# front bulkhead definition(matches the nose cross-sectional dimension)
Fuselage.Pay2Tail.FrontBulk.Width = 7.5*IN
Fuselage.Pay2Tail.FrontBulk.Height = 7.5*IN
Fuselage.Pay2Tail.FrontBulk.Material = AircraftPly.copy()
Fuselage.Pay2Tail.FrontBulk.Material.AreaForceDensity = (1.08*BaseWeight)/(7.75*IN*7.75*IN)
Fuselage.Pay2Tail.FrontBulk.WeightGroup = 'Fuselage'

# rear bulkhead definition (matches the cross-sectional dimension of the nose and payload bay together)
Fuselage.Pay2Tail.BackBulk.Width = 7.5*IN
Fuselage.Pay2Tail.BackBulk.Height = 3*IN
Fuselage.Pay2Tail.BackBulk.Material = AircraftPly.copy()
Fuselage.Pay2Tail.BackBulk.Material.AreaForceDensity = (1.5*BaseWeight)/(7.5*IN*3.0*IN)
Fuselage.Pay2Tail.BackBulk.WeightGroup = 'Fuselage'

# miscellaneous
Fuselage.Pay2Tail.SkinMat = Ultracote.copy()
Fuselage.Pay2Tail.WeightGroup = 'Fuselage'
Fuselage.Pay2Tail.StringerMat = AircraftPly.copy()
Fuselage.Pay2Tail.StringerMat.LinearForceDensity = 0.0058*LBF/IN
Fuselage.Pay2Tail.Align = 1.0 # Top of section relative to previous seciton

# SECTION 4: Tail section -----------------------------------------------------#

# SPH 12/1/2015: from 151130 CAD target weight @ 4.32oz CG @ 27.04125
# in SolidWorks relative to payload CG (-20.01,0,-3.44)

# front bulkhead definition(matches the nose cross-sectional dimension)
Fuselage.Tail.FrontBulk.Width = 7.5*IN
Fuselage.Tail.FrontBulk.Height = 3.0*IN
Fuselage.Tail.FrontBulk.Material = AircraftPly.copy()
Fuselage.Tail.FrontBulk.Material.AreaForceDensity = (0.15*BaseWeight)/(7.5*IN*3.0*IN)
Fuselage.Tail.FrontBulk.WeightGroup = 'Fuselage'

# rear bulkhead definition (matches the cross-sectional dimension of the nose and payload bay together)
Fuselage.Tail.BackBulk.Width = 7.5*IN
Fuselage.Tail.BackBulk.Height = 3.0*IN
Fuselage.Tail.BackBulk.Material = AircraftPly.copy()
Fuselage.Tail.BackBulk.Material.AreaForceDensity = (0.2*BaseWeight)/(7.5*IN*3.0*IN)
Fuselage.Tail.BackBulk.WeightGroup = 'Fuselage'

# miscellaneous
Fuselage.Tail.SkinMat = Ultracote.copy()
Fuselage.Tail.WeightGroup = 'Fuselage'
Fuselage.Tail.StringerMat = AircraftPly.copy()
Fuselage.Tail.StringerMat.LinearForceDensity = 0.01*LBF/IN
Fuselage.Tail.Align = 2.4 # Top of section relative to previous section

#------------------------------------------------------------------------------#

# Define which section contains the CG of the aircraft (design CG, will be recalculated)
Fuselage.XcgSection = Fuselage.PayBay
Fuselage.XcgSecFrac = 0.694
# Define the payload shape
##Fuselage.Payload.Face = 'Top'
Fuselage.Payload.Axis = (1,0,0) # dechellis: Axis that payload is added along to hit weight based on density and dimensions
Fuselage.Payload.Width  = 7.25*IN  #changed ACFuselage pretty significantly
Fuselage.Payload.Length = 1.625*IN #changed ACFuselage pretty significantly
Fuselage.Payload.Material = Steel.copy()
Fuselage.Payload.Weight = 0.0*LBF
Fuselage.Payload.Position = (0.12,0.5,0.55) # changed ACFuselage (ACPayload class)

# Determine which bulkhead should be set by the horizontal tail
Fuselage.TailBulk = Fuselage.Tail.BackBulk
Fuselage.TailBulk.WeightGroup = 'Fuselage'

#==============================================================================#
# VISUALIZATION & RESULTS
#==============================================================================#
if __name__ == '__main__':
    import pylab as pyl
    
    noseCompWeight = 0.0*OZF # initialize the weight for the components
    noseCompCG = 0.0*OZF*Fuselage.Nose.CG().copy()
    for component in Fuselage.Nose.param.Components: # loop through nose comps
        noseCompWeight += component.Weight
        noseCompCG += component.Weight*component.CG()
    actualNoseWeight = Fuselage.Nose.FrontBulk.Weight +  \
                       Fuselage.Nose.BackBulk.Weight + \
                       noseCompWeight
    noseCG = (1/actualNoseWeight)*\
             (noseCompCG + \
              (Fuselage.Nose.FrontBulk.Weight*Fuselage.Nose.FrontBulk.CG())+\
              (Fuselage.Nose.BackBulk.Weight*Fuselage.Nose.BackBulk.CG()))
    
##    print 'Nose Weight,  w/bulk:', AsUnit(Fuselage.Nose.Weight,'ozf')
##    print 'Nose CG       w/bulk:', AsUnit(Fuselage.Nose.CG(),'in')
##    print 'shiggins weight @', AsUnit(actualNoseWeight,'ozf'), ' CG @ ', AsUnit(noseCG,'in')
##    print

    payCompWeight = 0.0*OZF # initialize the weight for the components
    payCompCG = 0.0*OZF*Fuselage.PayBay.CG().copy()
    for component in Fuselage.PayBay.param.Components: # loop through nose comps
        payCompWeight += component.Weight
        payCompCG += component.Weight*component.CG()
    actualPayWeight = Fuselage.PayBay.FrontBulk.Weight +  \
                      Fuselage.PayBay.BackBulk.Weight + \
                      payCompWeight
    payCG = (1/actualPayWeight)*\
             (payCompCG + \
             (Fuselage.PayBay.FrontBulk.Weight*Fuselage.PayBay.FrontBulk.CG())+\
             (Fuselage.PayBay.BackBulk.Weight*Fuselage.PayBay.BackBulk.CG()))
    
##    print 'PayBay Weight w/bulk:', AsUnit(Fuselage.PayBay.Weight,'ozf')
##    print 'PayBay CG     w/bulk:', AsUnit(Fuselage.PayBay.CG(),'in')
##    print 'shiggins weight @', AsUnit(actualPayWeight,'ozf'), ' CG @ ', AsUnit(payCG,'in')
##    print

    tranCompWeight = 0.0*OZF # initialize the weight for the components
    tranCompCG = 0.0*OZF*Fuselage.Pay2Tail.CG().copy()
    for component in Fuselage.Pay2Tail.param.Components: # loop through nose comps
        tranCompWeight += component.Weight
        tranCompCG += component.Weight*component.CG()
    actualTranWeight = Fuselage.Pay2Tail.FrontBulk.Weight +  \
                       Fuselage.Pay2Tail.BackBulk.Weight + \
                       tranCompWeight
    tranCG = (1/actualTranWeight)*\
              (tranCompCG + \
              (Fuselage.Pay2Tail.FrontBulk.Weight*Fuselage.Pay2Tail.FrontBulk.CG())+\
              (Fuselage.Pay2Tail.BackBulk.Weight*Fuselage.Pay2Tail.BackBulk.CG()))
    
##    print 'Pay2Tail Wgt  w/bulk:', AsUnit(Fuselage.Pay2Tail.Weight,'ozf')
##    print 'Pay2Tail CG   w/bulk:', AsUnit(Fuselage.Pay2Tail.CG(),'in')
##    print 'shiggins weight @', AsUnit(actualTranWeight,'ozf'), ' CG @ ', AsUnit(tranCG,'in')
##    print

    tailCompWeight = 0.0*OZF # initialize the weight for the components
    tailCompCG = 0.0*OZF*Fuselage.Tail.CG().copy()
    for component in Fuselage.Tail.param.Components: # loop through nose comps
        tailCompWeight += component.Weight
        tailCompCG += component.Weight*component.CG()
    actualTailWeight = Fuselage.Tail.FrontBulk.Weight +  \
                       Fuselage.Tail.BackBulk.Weight + \
                       tailCompWeight
    tailCG = (1/actualTailWeight)*\
              (tailCompCG + \
              (Fuselage.Tail.FrontBulk.Weight*Fuselage.Tail.FrontBulk.CG())+\
              (Fuselage.Tail.BackBulk.Weight*Fuselage.Tail.BackBulk.CG()))
    
##    print 'Tail Weight   w/bulk:', AsUnit(Fuselage.Tail.Weight,'ozf')
##    print 'Tail CG       w/bulk:', AsUnit(Fuselage.Tail.CG(),'in')
##    print 'shiggins weight @', AsUnit(actualTailWeight,'ozf'), ' CG @ ', AsUnit(tailCG,'in')
##    print
    print 'Fuselage Wgt  w/bulk:', AsUnit(Fuselage.Weight,'lbf')
    print 'Fuselage CG   w/bulk:', AsUnit(Fuselage.CG(),'in')
    print
    print 'Fuselage MOI        :', AsUnit(Fuselage.MOI(),'slug*ft**2')
    print 'Fuselage Desired CG :', AsUnit(Fuselage.AircraftCG(),'in')
    print
##    Fuselage.Draw()
    pyl.show()
