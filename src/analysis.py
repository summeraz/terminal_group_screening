"""Define the workflow logic for the project analysis."""
from flow import FlowProject
from flow import staticlabel
import environment

loads = [5, 15, 25]

def _unwrap_str(op_name, gro_name):
    """Helper function, returns string to unwrap an XTC trajectory """
    unwrap_str = ('echo 0 | aprun gmx_mpi trjconv -f {op}.xtc -o '
                  '{op}-unwrapped.xtc -s {gro}.gro -pbc nojump')
    return unwrap_str.format(op=op_name, gro=gro_name)

def _interaction_energy_str(op_name):
    interaction_energy_str = ("echo $'Coul-SR:top_chains-bottom_chains\\n"
                              "LJ-SR:top_chains-bottom_chains\\n0' | "
                              "aprun -n 1 gmx_mpi energy -f {op}-rerun.edr "
                              "-o {op}-energy")
    return interaction_energy_str.format(op=op_name)


class ProjectAnalysis(FlowProject):

    @staticlabel()
    def shear_5nN_unwrapped(job):
        return job.isfile('shear_5nN-unwrapped.xtc')

    @staticlabel()
    def shear_15nN_unwrapped(job):
        return job.isfile('shear_15nN-unwrapped.xtc')

    @staticlabel()
    def shear_25nN_unwrapped(job):
        return job.isfile('shear_25nN-unwrapped.xtc')

    @staticlabel()
    def friction_calculated(job):
        return all([job.isfile('friction_{}nN.txt'.format(load)) for load in loads])

    @staticlabel()
    def S2_shear_calculated(job):
        return all([job.isfile('shear_{}nN-S2.txt'.format(load)) for load in loads])

    @staticlabel()
    def tilt_shear_calculated(job):
        return all([job.isfile('shear_{}nN-tilt.txt'.format(load)) for load in loads])

    @staticlabel()
    def cof_logged(job):
        return 'COF' in job.document

    @staticlabel()
    def S2_logged(job):
        return 'S2' in job.document

    @staticlabel()
    def tilt_logged(job):
        return 'tilt' in job.document

    @staticlabel()
    def mol2_created(job):
        return job.isfile('init.mol2')

    '''
    @staticlabel()
    def counted_h_bonds(job):
        return all([job.isfile('shear_{}nN-h-bonds.txt'.format(load)) for load in loads])
    '''

    @staticlabel()
    def interaction_energy_calculated_5nN(job):
        return job.isfile('shear_5nN-energy.xvg')

    @staticlabel()
    def interaction_energy_logged_5nN(job):
        return 'shear_5nN_Etotal' in job.document

    @staticlabel()
    def interaction_energy_calculated_15nN(job):
        return job.isfile('shear_15nN-energy.xvg')

    @staticlabel()
    def interaction_energy_logged_15nN(job):
        return 'shear_15nN_Etotal' in job.document

    @staticlabel()
    def interaction_energy_calculated_25nN(job):
        return job.isfile('shear_25nN-energy.xvg')

    @staticlabel()
    def interaction_energy_logged_25nN(job):
        return 'shear_25nN_Etotal' in job.document

    @staticlabel()
    def interdigitation_calculated(job):
        return 'interdigitation' in job.document

    @staticlabel()
    def roughness_calculated(job):
        return 'roughness' in job.document

    def __init__(self, *args, **kwargs):
        super(ProjectAnalysis, self).__init__(*args, **kwargs)

        def add_unwrap_op(op_name, name, gro, **kwargs):
            self.add_operation(
                name=op_name,
                cmd='cd {{job.ws}} ; {}'.format(
                    _unwrap_str(name, gro)),
                **kwargs)

        def add_gmx_energy_op(op_name, name, **kwargs):
            self.add_operation(
                name=op_name,
                cmd='cd {{job.ws}} ; {}'.format(
                    _interaction_energy_str(name)),
                **kwargs)

        add_unwrap_op(
            op_name='unwrap_shear_5nN', name='shear_5nN', gro='nvt',
            post=[self.shear_5nN_unwrapped])

        add_unwrap_op(
            op_name='unwrap_shear_15nN', name='shear_15nN', gro='nvt',
            pre=[self.shear_5nN_unwrapped],
            post=[self.shear_15nN_unwrapped])

        add_unwrap_op(
            op_name='unwrap_shear_25nN', name='shear_25nN', gro='nvt',
            pre=[self.shear_15nN_unwrapped],
            post=[self.shear_25nN_unwrapped])

        self.add_operation(
            name='calc_friction',
            cmd='python src/operations.py calc_friction {job._id}',
            pre=[self.shear_5nN_unwrapped,
                 self.shear_15nN_unwrapped,
                 self.shear_25nN_unwrapped],
            post=[self.friction_calculated])

        self.add_operation(
            name='calc_S2_shear',
            cmd='python src/operations.py calc_S2_shear {job._id}',
            pre=[self.friction_calculated],
            post=[self.S2_shear_calculated])

        self.add_operation(
            name='calc_tilt_shear',
            cmd='python src/operations.py calc_tilt_shear {job._id}',
            pre=[self.S2_shear_calculated],
            post=[self.tilt_shear_calculated])

        self.add_operation(
            name='log_cof',
            cmd='python src/operations.py log_cof {job._id}',
            pre=[self.tilt_shear_calculated],
            post=[self.cof_logged])

        self.add_operation(
            name='log_S2',
            cmd='python src/operations.py log_S2 {job._id}',
            pre=[self.cof_logged],
            post=[self.S2_logged])

        self.add_operation(
            name='log_tilt',
            cmd='python src/operations.py log_tilt {job._id}',
            pre=[self.S2_logged],
            post=[self.tilt_logged])

        self.add_operation(
            name='top_to_mol2',
            cmd='python src/operations.py top_to_mol2 {job._id}',
            pre=[self.tilt_logged],
            post=[self.mol2_created])

        '''
        self.add_operation(
            name='count_hydrogen_bonds',
            cmd='python src/operations.py count_hydrogen_bonds {job._id}',
            pre=[self.tilt_logged],
            post=[self.counted_h_bonds])
        '''
        '''
        self.add_operation(
            name='count_hydrogen_bonds',
            cmd='python src/operations.py count_hydrogen_bonds {job._id}',
            pre=[self.mol2_created],
            post=[self.counted_h_bonds])
        '''

        add_gmx_energy_op(
            op_name='get_interaction_energy_5nN', name='shear_5nN',
            pre=[self.mol2_created],
            post=[self.interaction_energy_calculated_5nN])
        '''
        add_gmx_energy_op(
            op_name='get_interaction_energy_5nN', name='shear_5nN',
            pre=[self.counted_h_bonds],
            post=[self.interaction_energy_calculated_5nN])
        '''

        self.add_operation(
            name='log_interaction_energy_5nN',
            cmd='python src/operations.py log_interaction_energy_5nN {job._id}',
            pre=[self.interaction_energy_calculated_5nN],
            post=[self.interaction_energy_logged_5nN])

        add_gmx_energy_op(
            op_name='get_interaction_energy_15nN', name='shear_15nN',
            pre=[self.interaction_energy_logged_5nN],
            post=[self.interaction_energy_calculated_15nN])

        self.add_operation(
            name='log_interaction_energy_15nN',
            cmd='python src/operations.py log_interaction_energy_15nN {job._id}',
            pre=[self.interaction_energy_calculated_15nN],
            post=[self.interaction_energy_logged_15nN])

        add_gmx_energy_op(
            op_name='get_interaction_energy_25nN', name='shear_25nN',
            pre=[self.interaction_energy_logged_15nN],
            post=[self.interaction_energy_calculated_25nN])

        self.add_operation(
            name='log_interaction_energy_25nN',
            cmd='python src/operations.py log_interaction_energy_25nN {job._id}',
            pre=[self.interaction_energy_calculated_25nN],
            post=[self.interaction_energy_logged_25nN])

        self.add_operation(
            name='calc_interdigitation',
            cmd='python src/operations.py calc_interdigitation {job._id}',
            pre=[self.interaction_energy_logged_25nN],
            post=[self.interdigitation_calculated])

        self.add_operation(
            name='calc_roughness',
            cmd='python src/operations.py calc_roughness {job._id}',
            pre=[self.interdigitation_calculated],
            post=[self.roughness_calculated])

    def write_script_header(self, script, **kwargs):
        super().write_script_header(script, **kwargs)

        script.writeline('export PATH=/ccs/proj/mat149/anaconda/titan/bin:$PATH')
        script.writeline('source activate azsconda')
        script.writeline('module load gromacs/5.1.0')
        script.writeline()

if __name__ == '__main__':
    ProjectAnalysis().main()
