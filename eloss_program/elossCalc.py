# IMPORT LIBRARIES
import numpy as np
import pandas as pd
import json
from pathlib import Path

import spyral_utils.nuclear.target as spytar
import spyral_utils.nuclear as spynuc

from attpc_engine import nuclear_map
from attpc_engine.kinematics import (
  KinematicsPipeline,
  KinematicsTargetMaterial,
  ExcitationGaussian,
  run_kinematics_pipeline,
  Reaction
)


# READ IN JSON FILE
with open('/workspaces/attpc_elosscalc/eloss_program/eloss_config.json') as f:
  data = json.load(f)


# DEFINE TARGET MATERIAL
print("TARGET MEDIUM: PROPANE GAS\n")
targ = spytar.load_target()


# DEFINE PROJECTILE 
print("PROJECTILE: PROTON\n")
proj = spynuc.get_data(zbeam_entry, mbeam_entry)


# DEFINE EXPERIMENTAL ENERGY RANGE

Exp_Emin = 0.                            # define minimum projectile energy (MeV/u)
Exp_Emax = 25.                           # define maximum projectile energy (MeV/u)
Exp_stepsize = 50                        # define step size for energy distribution points
Exp_Erange = np.linspace(Exp_Emin, Exp_Emax, num = Exp_stepsize)


# INITIALIZE DATA STORAGE
proj_ranges = []
event_validities = []


# NOW, LET'S TEST IF WE SEE THE EVENT

def test_event_validity(x0,y0,z0,vx,vy,vz,range):
    # Parametric equations of the particle's path:
    # x(t) = x0 + vx * t
    # y(t) = y0 + vy * t
    # z(t) = z0 + vz * t

    # Cylindrical surface boundary:
    # x^2 + y^2 = R^2

    #Finding the quadratic roots:
    a = vx**2 + vy**2
    b = 2 * (x0 * vx + y0 * vy)
    c = x0**2 + y0**2 - R**2

    discriminant = b**2 - 4*a*c
    if discriminant < 0: 
        return False
    
    t1 = -b + np.sqrt(discriminant) / (2*a)
    t2 = -b - np.sqrt(discriminant) / (2*a)

    # Remove the t that is negative, as it's trajectory was in the wrong direction
    for i in [t1,t2]:
        if i > 0: t = i
    
    # Calculate intersection point
    x_intersect = x0 + vx * t
    y_intersect = y0 + vy * t
    z_intersect = z0 + vz * t

    # Check z bound
    if z_intersect < 0 or z_intersect > H:
        return False
    
    # Calculate geometric distance
    geo_dist = np.sqrt((x_intersect - x0)**2 + (y_intersect - y0)**2 + (z_intersect - z0)**2)

    # Check if it'll hit the wall 
    return geo_dist <= range



# CALCULATE ENERGY RANGE AND TEST EVENT:

for i in Exp_Erange:
    range = spytar.GasTarget.get_range(proj,i) # calculate results for projectile with energy i
    proj_ranges.append(range) 
    event_validities.append(test_event_validity(x0,y0,z0,vx,vy,vz,range))