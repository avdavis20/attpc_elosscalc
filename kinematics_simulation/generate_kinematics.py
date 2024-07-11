# IMPORT LIBRARIES
from attpc_engine.kinematics import (
    KinematicsPipeline,
    KinematicsTargetMaterial,
    ExcitationGaussian,
    PolarUniform,
    run_kinematics_pipeline,
    Reaction,
)
from attpc_engine import nuclear_map
from spyral_utils.nuclear.target import TargetData, GasTarget
from pathlib import Path
import numpy as np
import json


# INITIALIZE OUTPUT PATH
output_path = Path('/workspaces/attpc_elosscalc/kinematics_simulation/output/kinematics/kinsimtest.h5')


# OPEN JSON CONFIG FILE
with open('/workspaces/attpc_elosscalc/eloss_program/eloss_config.json') as f:
  data = json.load(f)


# DEFINE NUM OF EVENTS AND BEAM ENERGY
nevents = 10000
beam_energy = 184.131 # MeV


# DEFINE TARGET
target = GasTarget(
  TargetData(compound = [(1,2,2)],pressure = 300.0, thickness = None),
  nuclear_map
  )


# DEFINE REACTION CONSITITUENTS
pipeline = KinematicsPipeline(
  [
    Reaction(
    target = nuclear_map.get_data(1,2),
    projectile = nuclear_map.get_data(6,16),
    ejectile = nuclear_map.get_data(1,2), 
    )
  ],
  [PolarUniform(0.0, np.pi)],
  [ExcitationGaussian(0.0,0.001)],
  beam_energy=184.131,
  target_material=KinematicsTargetMaterial(
  material = target, z_range = (0.0,1.0), rho_sigma = 0.007
  ),
)


# EXECUTE TASKS
def main():
  run_kinematics_pipeline(pipeline, nevents, output_path)

