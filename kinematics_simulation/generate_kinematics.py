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

output_path = Path("./output/kinematics/kinsimtest.h5")

target = GasTarget(
    TargetData(compound=[(1, 2, 2)], pressure=300.0, thickness=None), nuclear_map
)

nevents = 10000

beam_energy = 184.131 # MeV

pipeline = KinematicsPipeline(
    [
        Reaction(
            target=nuclear_map.get_data(1, 2), # deuteron
            projectile=nuclear_map.get_data(6, 16), # 16C
            ejectile=nuclear_map.get_data(1, 2), # deuteron
        )
    ],
    [ExcitationGaussian(0.0, 0.001)], # No width to ground state
    [PolarUniform(0.0, np.pi)], # Full angular range 0 deg to 180 deg
    beam_energy=184.131, # MeV
    target_material=KinematicsTargetMaterial(
        material=target, z_range=(0.0, 1.0), rho_sigma=0.007
    ),
)
def main():
    run_kinematics_pipeline(pipeline, nevents, output_path)

if __name__ == "__main__":
    main()