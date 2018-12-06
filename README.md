# Screening monolayer terminal groups for influences on lubrication

## Installation/Set-up

#### Download and install anaconda
Note: I did this and in the /ccs/proj/ directory on Titan

#### Create a new environment (3.5 is preferred)
`>> conda create --name myconda python=3.5`

#### Activate the environment
`>> source activate myconda`

Note: You may have to first append to your path the directory where anaconda
is located, e.g.

`>> export PATH=/ccs/proj/xxx000/anaconda/titan/bin:$PATH`

#### Clone and install atools
commit 320523d91535e497b5dbc2b6a821cc0453985055

`>> git clone https://github.com/summeraz/atools.git`
`>> pip install .`

#### Clone and install mbuild
commit fa2bc651823d8c0a93cac8721e0abf10a7b5e168

`>> git clone https://github.com/mosdef-hub/mbuild.git`
`>> pip install .`

#### Clone and install foyer
commit 1aa97bbebed22c94ad8d9d68486fbdbe7a3bd6d7

`>> git clone https://github.com/mosdef-hub/foyer.git`
`>> pip install .`

#### Install signac-flow
`>> conda install signac-flow=0.5.4 -c glotzer`

#### Install dependencies
Note: If mBuild and Foyer are installed via conda or pip, these dependencies
should be installed automatically.
```
>> conda config --add channels omnia mosdef
>> conda install lxml requests networkx mdtraj oset parmed openmm plyplus
>> pip install mdanalysis
```

#### Clone the terminal_group_screening repository
`>> git clone https://github.com/summeraz/terminal_group_screening.git`

#### Initialize the project
Note: All flow commands must be performed from the project root directory.

Note: The -n 5 1 signifies that five statepoints will be created for each
parameter state, each with a different random seed (incrementing from 1)

`>> python src/init.py -n 5 1`

----------
## Signac workflow

#### Initialize/construct systems
This will submit jobs in bundles of 6 statepoints to be executed on
a single node. Although each node contains 16 processors, memory issues
limit the number of simultaneous systems that can be initialized.

`>> python src/project.py submit -o initialize --bundle 6 --nn 1 -w 0.5`

#### Run minimization in LAMMPS to fix overlaps
`>> python src/project.py submit -o fix_overlaps --bundle 400 --nn 400 -w 1`

#### Convert last frame of LAMMPS trajectory to a GROMACS structure file
`>> python src/project.py submit -o lammps_to_gmx --bundle 48 --nn 3 -w 0.5`

#### Create TPR file for GROMACS energy minimization
`>> python src/project.py submit -o minimize_grompp --bundle 400 --nn 400 -w 0.5`

#### Run GROMACS energy minimization
`>> python src/project.py submit -o minimize --bundle 400 --nn 400 -w 0.5`

#### Create TPR file for GROMACS NVT equilibration
`>> python src/project.py submit -o equilibrate_grompp --bundle 400 --nn 400 -w 0.5`

#### Run GROMACS NVT equilibration
`>> python src/project.py submit -o equilibrate --bundle 400 --nn 400 -w 2`

#### Create TPR file for GROMACS compression
`>> python src/project.py submit -o compress_grompp --bundle 400 --nn 400 -w 0.5`

#### Run GROMACS compression
`>> python src/project.py submit -o compress --bundle 400 --nn 400 -w 1`

#### Create TPR file for GROMACS shear at a normal load of 5nN
`>> python src/project.py submit -o shear_5nN_grompp --bundle 400 --nn 400 -w 0.5`

#### Run GROMACS shear at a normal load of 5nN

Note: Shear was originally performed for 5ns and then extended another 5ns. The MDP files have been updated to include the full 10ns now.

`>> python src/project.py submit -o shear_5nN --bundle 400 --nn 400 -w 4`

#### Create TPR file for GROMACS shear at a normal load of 15nN
`>> python src/project.py submit -o shear_15nN_grompp --bundle 400 --nn 400 -w 0.5`

#### Run GROMACS shear at a normal load of 15nN
`>> python src/project.py submit -o shear_15nN --bundle 400 --nn 400 -w 4`

#### Create TPR file for GROMACS shear at a normal load of 25nN
`>> python src/project.py submit -o shear_25nN_grompp --bundle 400 --nn 400 -w 0.5`

#### Run GROMACS shear at a normal load of 25nN
`>> python src/project.py submit -o shear_25nN --bundle 400 --nn 400 -w 4`

----------
## Post-processing/Analysis
#### Unwrap trajectories
```
>> python src/analysis.py submit -o unwrap_shear_5nN --bundle 48 --nn 3 -w 1
>> python src/analysis.py submit -o unwrap_shear_15nN --bundle 48 --nn 3 -w 1
>> python src/analysis.py submit -o unwrap_shear_25nN --bundle 48 --nn 3 -w 1
```

#### Calculate friction forces for each shear trajectory
`>> python src/analysis.py submit -o calc_friction --bundle 48 --nn 3 -w 1`

#### Calculate monolayer nematic order for each shear trajectory
`>> python src/analysis.py submit -o calc_S2_shear --bundle 18 --nn 3 -w 1`

#### Log COF
`>> python src/analysis.py submit -o log_cof --bundle 48 --nn 3 -w 1`
