from __future__ import division # let 5/2 = 2.5 rather than 2

# import built-in modules
import os
import sys
import numpy as npy
import cmath as math
import pylab as pyl

# (USER) set-up directories
#trunkDir = r'C:\eclipse\workspace\AircraftDesign\trunk'
#BAPDir = os.path.join(trunkDir,r'Aircraft_Models\Reg2017Aircraft_BearcatAirlines\BAP')

# link path to Aerothon
#sys.path.append(trunkDir)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Optimum Prop None
from Aerothon.ACMotor import ACMotor
import numpy as npy
import cmath as math
from scalar.units import MM, IN, OZF, RPM, HP, V, A, OHM, GRAM, gacc, mAh, W, LBF, inHg, K
from scalar.units import AsUnit
from Aerothon.AeroUtil import STDCorrection

#sys.path.append(os.path.join(BAPDir,r'Propulsion\Batteries'))

#from Electrolux_6Cell_3100 import Electrolux_6Cell_3100
from Batteries.Turnigy_6Cell_3000 import Turnigy_6Cell_3000

#sys.path.append(os.path.join(BAPDir,r'Propulsion\SpeedControllers'))
from SpeedControllers.Phoenix import Phoenix100 # note: Phoenix contains multiple models

# Set Motor properties
Motor  = ACMotor()
Motor.name = 'Scorpion250KV'
Motor.Battery = Turnigy_6Cell_3000
Motor.SpeedController = Phoenix100
#Manufacturer Data
# Motor.Ri  = 0.02*OHM        #Coil resistance
# Motor.Io  = 1.5*A          #Idle current
# Motor.Kv  = 250*RPM/V      #RPM/Voltage ratio
#Matched Data
Motor.Ri  = 0.037*OHM
Motor.Io  = 0.69*A
Motor.Kv  = 250*RPM/V
#
Motor.Vmax = 23.5*V
Motor.Imax = 65*A
Motor.ThrustUnit = LBF
Motor.ThrustUnitName = 'lbf'

Motor.xRm =  100000
Motor.Pz  = 0.0

Motor.Weight = 450*GRAM*gacc
Motor.LenDi = [48.8*MM, 64.9*MM]

# Assign objects to weight classes
Motor.Battery.WeightGroup = 'Electronics'
Motor.SpeedController.WeightGroup = 'Electronics'

Motor.WeightGroup = 'Propulsion'

#
# This data has been corrected for standard day
STD = STDCorrection( 30.2*inHg, (16.1+273.15)*K )
Arm=19.5*IN
#            RPM,        Torque     Current   Voltage
TestData = [(6030  *RPM, (7.3*Arm*OZF)*STD,    32.0*A,    22.8*V),
            (5670  *RPM, (8.3*Arm*OZF)*STD,    36.0*A,    22.2*V),
            (5430  *RPM, (9.3*Arm*OZF)*STD,    39.5*A,    21.5*V),
            (5340  *RPM, (9.0*Arm*OZF)*STD,    38.7*A,    21.1*V),
            (5370  *RPM, (8.3*Arm*OZF)*STD,    35.3*A,    20.9*V)] #this is actual test data from a test stand

Motor.TestData = TestData

if __name__ == '__main__':
    import pylab as pyl
    
    print "V to Motor : ", AsUnit( Motor.Vmotor(Ib=3.75*A), 'V' )
    print "Efficiency : ", Motor.Efficiency(Ib=3.75*A)
    print "Max efficiency : ", Motor.Effmax()
    print "Max efficiency current : ", AsUnit( Motor.I_Effmax(), 'A' )
    print "Max efficiency RPM : ", AsUnit( Motor.N_Effmax(), 'rpm' )
    
    Motor.PlotTestData()
    
    pyl.show()
