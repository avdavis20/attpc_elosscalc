import h5py

# Open the HDF5 file
file = '/workspaces/attpc_elosscalc/kinematics_simulation/output/kinematics/kinsimtest.h5'  # Adjust the file name as necessary
with h5py.File(file, 'r') as hdf:
    # List all groups
    print("Keys: %s" % hdf.keys())
    a_group_key = list(hdf.keys())[0]  # Take the first group

    # Get the data
    data = list(hdf[a_group_key])