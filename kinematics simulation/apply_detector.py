# IMPORT LIBRARIES
from attpc_engine.detector import (
    DetectorParams,
    ElectronicsParams,
    PadParams,
    Config,
    run_simulation,
    SpyralWriter,
)
from attpc_engine import nuclear_map
from spyral_utils.nuclear.target import TargetData, GasTarget
from pathlib import Path
import json


# DEFINE INPUT/OUTPUT PATHS
input_path = "kinematics simulation/output/kinematics/kinsimtest.h5"
output_path = Path("output/detector/run_0001.h5")


# DEFINE DETECTOR GAS
gas = GasTarget(TargetData([(1, 2, 2)], pressure=300.0), nuclear_map)


# DEFINE DETECTOR, ELECTRONICS, AND PAD PARAMETERS
detector = DetectorParams(
    length=1.0,
    efield=45000.0,
    bfield=2.85,
    mpgd_gain=175000,
    gas_target=gas,
    diffusion=0.277,
    fano_factor=0.2,
    w_value=34.0,
)

electronics = ElectronicsParams(
    clock_freq=6.25,
    amp_gain=900,
    shaping_time=1000,
    micromegas_edge=10,
    windows_edge=560,
    adc_threshold=40.0,
)

pads = PadParams()


# CONFIGURE SETTINGS, RUN AND SAVE SIMULATION TO H5 FILE
config = Config(detector, electronics, pads)
writer = SpyralWriter(output_path, config)

def main():
    run_simulation(
        config,
        input_path,
        writer,
    )

if __name__ == "__main__":
    main()