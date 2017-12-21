import os
from pkg_resources import resource_filename

from atools.fileio import write_monolayer_ndx
from atools.lib.chains import Alkylsilane
from atools.recipes import DualSurface, SilicaInterface, SurfaceMonolayer
from mbuild.lib.atoms import H
import numpy as np
import parmed as pmd
from scipy.stats import linregress
from util.decorators import job_chdir
from util.index_groups import generate_index_groups


@job_chdir
def initialize(job):
    "Initialize the simulation configuration."

    '''
    ---------------------------
    Read statepoint information
    ---------------------------
    '''
    chainlength = job.statepoint()['chainlength']
    n_chains = job.statepoint()['n']
    seed = job.statepoint()['seed']
    terminal_group = job.statepoint()['terminal_group']

    '''
    -----------------------------------
    Generate amorphous silica interface
    -----------------------------------
    '''
    surface = SilicaInterface(thickness=1.2, seed=seed)

    '''
    ------------------------------------------------------
    Generate prototype of functionalized alkylsilane chain
    ------------------------------------------------------
    '''
    chain_prototype = Alkylsilane(chain_length=chainlength,
                                  terminal_group=terminal_group)

    '''
    ----------------------------------------------------------
    Create monolayer on surface, backfilled with hydrogen caps
    ----------------------------------------------------------
    '''
    monolayer = SurfaceMonolayer(surface=surface, chains=chain_prototype,
                                 n_chains=n_chains, seed=seed,
                                 backfill=H(), rotate=False)

    '''
    ------------------------------------------
    Duplicate to yield two opposing monolayers
    ------------------------------------------
    '''
    dual_monolayer = DualSurface(monolayer, separation=2.0)

    '''
    --------------------------------------------------------
    Make sure box is elongated in z to be pseudo-2D periodic
    --------------------------------------------------------
    '''
    box = dual_monolayer.boundingbox
    dual_monolayer.periodicity += np.array([0, 0, 5. * box.lengths[2]])

    '''
    -------------------------------------------------------------------
    - Save to .GRO, .TOP, and .LAMMPS formats
    - Atom-type the system using Foyer, with parameters from the OPLS
      force field obtained from GROMACS. Parameters are located in a
      Foyer XML file in the `atools` git repo, with references provided
      as well as notes where parameters have been added or altered to
      reflect the literature.
    -------------------------------------------------------------------
    '''
    forcefield_dir = resource_filename('atools', 'forcefields')
    dual_monolayer.save('init.gro', overwrite=True)
    dual_monolayer.save('init.top', 
        forcefield_files=os.path.join(forcefield_dir, 'oplsaa.xml'),
        combining_rule='geometric', overwrite=True)
    dual_monolayer.save('init.lammps',
        forcefield_files=os.path.join(forcefield_dir, 'oplsaa.xml'),
        combining_rule='geometric', overwrite=True)

    '''
    --------------------------------------
    Specify index groups and write to file
    --------------------------------------
    '''
    index_groups = generate_index_groups(system=dual_monolayer,
                                         terminal_group=terminal_group,
                                         freeze_thickness=0.5)
    write_monolayer_ndx(rigid_groups=index_groups, filename='init.ndx')

@job_chdir
def calc_S2_nvt(job):
    _calc_S2('nvt', job.sp['n'])

@job_chdir
def calc_tilt_nvt(job):
    _calc_tilt('nvt', job.sp['n'])

@job_chdir
def calc_S2_shear(job):
    for load in [5, 15, 25]:
        _calc_S2('shear_{}nN'.format(load), job.sp['n'])

@job_chdir
def calc_tilt_shear(job):
    for load in [5, 15, 25]:
        _calc_tilt('shear_{}nN'.format(load), job.sp['n'])

@job_chdir
def calc_friction(job):
    import MDAnalysis as mda

    for load in [5, 15, 25]:
        trr_file = 'shear_{}nN.trr'.format(load)
        out_file = 'friction_{}nN.txt'.format(load)
        if os.path.isfile(trr_file):
            fric = []
            trr = mda.coordinates.TRR.TRRReader(trr_file)
            for frame in trr:
                forces_on_bottom = frame.forces[:int(frame.n_atoms/2)]
                fric.append([frame.time, np.sum(forces_on_bottom[:,0]) * 0.0166])
            np.savetxt(out_file, fric)

@job_chdir
def log_cof(job):
    loads = [5, 15, 25]
    friction_forces = []
    for load in loads:
        friction_data = np.loadtxt('friction_{}nN.txt'.format(load))
        friction_data = friction_data[int(len(friction_data)*0.6):, 1]
        friction_forces.append(np.mean(friction_data))
    cof, intercept, r, p, stderr = linregress(loads, friction_forces)
    job.document['COF'] = cof
    job.document['intercept'] = intercept

@job_chdir
def log_S2(job):
    loads = [5, 15, 25]
    s2_dict = {}
    for load in loads:
        s2_data = np.loadtxt('shear_{}nN-S2.txt'.format(load))
        s2_data = s2_data[int(len(s2_data)*0.6):, 1]
        s2_dict['{}nN'.format(load)] = np.mean(s2_data)
    job.document['S2'] = s2_dict

@job_chdir
def log_tilt(job):
    loads = [5, 15, 25]
    tilt_dict = {}
    for load in loads:
        tilt_data = np.loadtxt('shear_{}nN-tilt.txt'.format(load))
        tilt_data = tilt_data[int(len(tilt_data)*0.6):, 1]
        tilt_dict['{}nN'.format(load)] = np.mean(tilt_data)
    job.document['tilt'] = tilt_dict

@job_chdir
def count_hydrogen_bonds(job):
    for load in [5, 15, 25]:
        _count_hydrogen_bonds('shear_{}nN'.format(load), job.sp['n'])

@job_chdir
def calc_interdigitation(job):
    loads = [5, 15, 25]
    interdigitation_dict = {}
    for load in loads:
        _calc_interdigitation('shear_{}nN'.format(load))
        interdigitation_data = np.loadtxt('shear_{}nN-interdigitation.txt'.format(load))
        interdigitation_data = interdigitation_data[int(len(interdigitation_data)*0.6):, 1]
        interdigitation_dict['{}nN'.format(load)] = np.mean(interdigitation_data)
    job.document['interdigitation'] = interdigitation_dict

@job_chdir
def calc_roughness(job):
    loads = [5, 15, 25]
    roughness_dict = {}
    for load in loads:
        _calc_roughness('shear_{}nN'.format(load))
        roughness_data = np.loadtxt('shear_{}nN-roughness.txt'.format(load))
        roughness_data = roughness_data[int(len(roughness_data)*0.6):, 1]
        roughness_dict['{}nN'.format(load)] = np.mean(roughness_data)
    job.document['roughness'] = roughness_dict

@job_chdir
def log_interaction_energy_5nN(job):
    _log_interaction_energy(job, 'shear_5nN')

@job_chdir
def log_interaction_energy_15nN(job):
    _log_interaction_energy(job, 'shear_15nN')

@job_chdir
def log_interaction_energy_25nN(job):
    _log_interaction_energy(job, 'shear_25nN')

@job_chdir
def top_to_mol2(job):
    struct = pmd.load_file('init.top')
    struct.save('init.mol2')

def _calc_interdigitation(name):
    from atools.structure import calc_interdigitation
    gro_file = '{}.gro'.format(name)
    out_file= '{}-interdigitation.txt'.format(name)
    ndx_file = 'init.ndx'
    traj = '{}.xtc'.format(name)
    if os.path.isfile(gro_file) and os.path.isfile(traj):
        calc_interdigitation(traj, gro_file, out_file, ndx_file)

def _calc_roughness(name):
    from atools.structure import calc_monolayer_roughness
    gro_file = '{}.gro'.format(name)
    out_file= '{}-roughness.txt'.format(name)
    ndx_file = 'init.ndx'
    traj = '{}.xtc'.format(name)
    if os.path.isfile(gro_file) and os.path.isfile(traj):
        calc_monolayer_roughness(traj, gro_file, out_file, ndx_file)

def _calc_S2(name, n_chains):
    from atools.structure import calc_nematic_order
    gro_file = '{}.gro'.format(name)
    out_file = '{}-S2.txt'.format(name)
    traj = '{}-unwrapped.xtc'.format(name)
    if os.path.isfile(gro_file) and os.path.isfile(traj):
        calc_nematic_order(traj, gro_file, out_file, n_chains)

def _calc_tilt(name, n_chains):
    from atools.structure import calc_avg_tilt_angle
    gro_file = '{}.gro'.format(name)
    out_file = '{}-tilt.txt'.format(name)
    traj = '{}-unwrapped.xtc'.format(name)
    if os.path.isfile(gro_file) and os.path.isfile(traj):
        calc_avg_tilt_angle(traj, gro_file, out_file, n_chains)

def _count_hydrogen_bonds(name, n_chains):
    from atools.structure import count_hydrogen_bonds
    mol2_file = 'init.mol2'
    ndx_file = 'init.ndx'
    gro_file = '{}.gro'.format(name)
    out_file = '{}-h-bonds.txt'.format(name)
    traj = '{}.xtc'.format(name)
    if os.path.isfile(gro_file) and os.path.isfile(traj):
        count_hydrogen_bonds(traj, gro_file, out_file, mol2_file, ndx_file,
                             top_group='top_termini', bottom_group='bottom_termini')

def _log_interaction_energy(job, name):
    data = np.loadtxt('{}-energy.xvg'.format(name), skiprows=24)
    coul_energy = data[int(len(data)*0.5):, 1]
    lj_energy = data[int(len(data)*0.5):, 2]
    total_energy = coul_energy + lj_energy
    coul_mean = np.mean(coul_energy)
    coul_std = np.std(coul_energy)
    lj_mean = np.mean(lj_energy)
    lj_std = np.std(lj_energy)
    total_mean = np.mean(total_energy)
    total_std = np.std(total_energy)
    job.document['{}_qq'.format(name)] = (coul_mean, coul_std)
    job.document['{}_lj'.format(name)] = (lj_mean, lj_std)
    job.document['{}_Etotal'.format(name)] = (total_mean, total_std)

if __name__ == '__main__':
    import flow
    flow.run()
