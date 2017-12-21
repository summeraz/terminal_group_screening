"""Define the project's workflow logic."""
from flow import FlowProject
from flow import staticlabel
import environment

def _grompp_str(root, op_name, gro_name, sys_name):
    """Helper function, returns grompp command string for operation

    The -maxwarn 1 flag is added, so that the grompp command will succeed
    despite Gromacs complaining about the use of pbc=xyz with
    ewald_geometry=3dc. Since the z-dimension is sufficiently expanded and
    systems remain in a slab configuration throughout the duration, this
    warning can be safely ignored.
    """
    grompp_str = ('gmx_mpi grompp -f {root}/src/util/mdp_files/{op}.mdp -c '
                  '{gro}.gro -p {sys}.top -n {sys}.ndx -o {op}.tpr '
                  '-maxwarn 1')
    return grompp_str.format(root=root, op=op_name, gro=gro_name, sys=sys_name)

def _mdrun_str(op_name):
    """Helper function, returns mdrun command string for operation """
    mdrun_str = ('gmx_mpi mdrun -v -deffnm {op} -s {op}.tpr -cpi {op}.cpt '
                 '-ntomp 1')
    return mdrun_str.format(op=op_name)

def _grompp_extend_str(op_name):
    grompp_extend_str = ('gmx_mpi convert-tpr -s {op}.tpr -extend 5000 -o '
                         '{op}-extended.tpr')
    return grompp_extend_str.format(op=op_name)

def _mdrun_extend_str(op_name):
    mdrun_extend_str = ('gmx_mpi mdrun -v -s {op}-extended.tpr -cpi {op}.cpt '
                        '-ntomp 1 -deffnm {op} -px {op}_pullx.xvg '
                        '-pf {op}_pullf.xvg')
    return mdrun_extend_str.format(op=op_name)

def _grompp_rerun_str(root, op_name, gro_name, sys_name):
    grompp_rerun_str = ('gmx_mpi grompp -f {root}/src/util/mdp_files/{op}-rerun.mdp '
                  '-c {gro}.gro -p {sys}.top -n {sys}.ndx -o {op}-rerun.tpr '
                  '-maxwarn 1')
    return grompp_rerun_str.format(root=root, op=op_name, gro=gro_name, sys=sys_name)

def _mdrun_rerun_str(op_name):
    mdrun_rerun_str = ('gmx_mpi mdrun -v -deffnm {op}-rerun -s {op}-rerun.tpr '
                 '-rerun {op}.trr -nb cpu -ntomp 1')
    return mdrun_rerun_str.format(op=op_name)

class MyProject(FlowProject):

    @staticlabel()
    def initialized(job):
        return job.isfile('init.lammps') and job.isfile('init.top')
    @staticlabel()
    def fixed_overlaps(job):
        return job.isfile('minimize.xtc')
    @staticlabel()
    def lmp_to_gmx(job):
        return job.isfile('minimized.gro')
    @staticlabel()
    def ready_to_minimize(job):
        return job.isfile('em.tpr')
    @staticlabel()
    def minimized(job):
        return job.isfile('em.gro')
    @staticlabel()
    def ready_to_equilibrate(job):
        return job.isfile('nvt.tpr')
    @staticlabel()
    def equilibrated(job):
        return job.isfile('nvt.gro')
    @staticlabel()
    def ready_to_compress(job):
        return job.isfile('compress.tpr')
    @staticlabel()
    def compressed(job):
        return job.isfile('compress.gro')
    @staticlabel()
    def ready_to_shear_at_5nN(job):
        return job.isfile('shear_5nN.tpr')
    @staticlabel()
    def sheared_at_5nN(job):
        return job.isfile('shear_5nN.gro')
    @staticlabel()
    def ready_to_extend_shear_at_5nN(job):
        return job.isfile('shear_5nN-extended.tpr')
    @staticlabel()
    def extended_shear_at_5nN(job):
        return job.isfile('#shear_5nN.gro.1#')
    @staticlabel()
    def ready_to_rerun_shear_at_5nN(job):
        return job.isfile('shear_5nN-rerun.tpr')
    @staticlabel()
    def shear_reran_at_5nN(job):
        return job.isfile('shear_5nN-rerun.edr')
    @staticlabel()
    def ready_to_shear_at_15nN(job):
        return job.isfile('shear_15nN.tpr')
    @staticlabel()
    def sheared_at_15nN(job):
        return job.isfile('shear_15nN.gro')
    @staticlabel()
    def ready_to_extend_shear_at_15nN(job):
        return job.isfile('shear_15nN-extended.tpr')
    @staticlabel()
    def extended_shear_at_15nN(job):
        return job.isfile('#shear_15nN.gro.1#')
    @staticlabel()
    def ready_to_rerun_shear_at_15nN(job):
        return job.isfile('shear_15nN-rerun.tpr')
    @staticlabel()
    def shear_reran_at_15nN(job):
        return job.isfile('shear_15nN-rerun.edr')
    @staticlabel()
    def ready_to_shear_at_25nN(job):
        return job.isfile('shear_25nN.tpr')
    @staticlabel()
    def sheared_at_25nN(job):
        return job.isfile('shear_25nN.gro')
    @staticlabel()
    def ready_to_extend_shear_at_25nN(job):
        return job.isfile('shear_25nN-extended.tpr')
    @staticlabel()
    def extended_shear_at_25nN(job):
        return job.isfile('#shear_25nN.gro.1#')
    @staticlabel()
    def ready_to_rerun_shear_at_25nN(job):
        return job.isfile('shear_25nN-rerun.tpr')
    @staticlabel()
    def shear_reran_at_25nN(job):
        return job.isfile('shear_25nN-rerun.edr')

    def __init__(self, *args, **kwargs):
        super(MyProject, self).__init__(*args, **kwargs)

        env = environment.get_environment()

        def add_grompp_op(op_name, name, gro, sys, **kwargs):
            self.add_operation(
                name=op_name,
                cmd=('-n 1 --w-cd {{job.ws}} -- {}'
                     ''.format(_grompp_str(self.root_directory(), name,
                     gro, sys))),
                **kwargs)

        def add_mdrun_op(op_name, name, **kwargs):
            self.add_operation(
                name=op_name,
                cmd=('-n 16 -N 16 --w-cd {{job.ws}} -- {} -gpu_id '
                     '{}'.format(_mdrun_str(name), '0'*16)),
                **kwargs)

        def add_grompp_extend_op(op_name, name, **kwargs):
            self.add_operation(
                name=op_name,
                cmd=('-n 1 --w-cd {{job.ws}} -- {}'
                     ''.format(_grompp_extend_str(name))),
                **kwargs)

        def add_mdrun_extend_op(op_name, name, **kwargs):
            self.add_operation(
                name=op_name,
                cmd=('-n 16 -N 16 --w-cd {{job.ws}} -- {} -gpu_id '
                     '{}'.format(_mdrun_extend_str(name), '0'*16)),
                **kwargs)

        def add_grompp_rerun_op(op_name, name, gro, sys, **kwargs):
            self.add_operation(
                name=op_name,
                cmd=('-n 1 --w-cd {{job.ws}} -- {}'
                     ''.format(_grompp_rerun_str(self.root_directory(), name,
                     gro, sys))),
                **kwargs)

        def add_mdrun_rerun_op(op_name, name, **kwargs):
            self.add_operation(
                name=op_name,
                cmd=('-n 1 --w-cd {{job.ws}} -- {}'
                     ''.format(_mdrun_rerun_str(name))),
                **kwargs)

        self.add_operation(
            name='initialize',
            cmd='python src/operations.py initialize {job._id}',
            post=[self.initialized])

        self.add_operation(
            name='fix_overlaps',
            cmd=('-n 16 --w-cd {{job.ws}} -- lmp_titan -in '
                '{0}/src/util/mdp_files/in.minimize -log minimize.log'
                ''.format(self.root_directory())),
            np=16,
            pre=[self.initialized],
            post=[self.fixed_overlaps])

        self.add_operation(
            name='lammps_to_gmx',
            cmd=('echo 0 | aprun gmx_mpi trjconv -s {job.ws}/init.gro -f '
                '{job.ws}/minimize.xtc -o {job.ws}/minimized.gro -b 1.0 -e 1.0'),
            pre=[self.fixed_overlaps],
            post=[self.lmp_to_gmx])

        add_grompp_op(
            op_name='minimize_grompp', name='em', gro='minimized', sys='init',
            pre=[self.lmp_to_gmx],
            post=[self.ready_to_minimize])

        add_mdrun_op(
            op_name='minimize', name='em',
            pre=[self.ready_to_minimize],
            post=[self.minimized])

        add_grompp_op(
            op_name='equilibrate_grompp', name='nvt', gro='em', sys='init',
            pre=[self.minimized],
            post=[self.ready_to_equilibrate])

        add_mdrun_op(
            op_name='equilibrate', name='nvt',
            pre=[self.ready_to_equilibrate],
            post=[self.equilibrated])

        add_grompp_op(
            op_name='compress_grompp', name='compress', gro='nvt', sys='init',
            pre=[self.equilibrated],
            post=[self.ready_to_compress])

        add_mdrun_op(
            op_name='compress', name='compress',
            pre=[self.ready_to_compress],
            post=[self.compressed])

        add_grompp_op(
            op_name='shear_5nN_grompp', name='shear_5nN', gro='compress', sys='init',
            pre=[self.compressed],
            post=[self.ready_to_shear_at_5nN])

        add_mdrun_op(
            op_name='shear_5nN', name='shear_5nN',
            pre=[self.ready_to_shear_at_5nN],
            post=[self.sheared_at_5nN])

        add_grompp_extend_op(
            op_name='shear_5nN_extend_grompp', name='shear_5nN',
            pre=[self.sheared_at_25nN],
            post=[self.ready_to_extend_shear_at_5nN])

        add_mdrun_extend_op(
            op_name='shear_5nN_extend', name='shear_5nN',
            pre=[self.ready_to_extend_shear_at_5nN],
            post=[self.extended_shear_at_5nN])

        add_grompp_rerun_op(
            op_name='shear_5nN_rerun_grompp', name='shear_5nN', gro='compress',
            sys='init',
            pre=[self.extended_shear_at_5nN],
            post=[self.ready_to_rerun_shear_at_5nN])

        add_mdrun_rerun_op(
            op_name='shear_5nN_rerun', name='shear_5nN',
            pre=[self.ready_to_rerun_shear_at_5nN],
            post=[self.shear_reran_at_5nN])

        add_grompp_op(
            op_name='shear_15nN_grompp', name='shear_15nN', gro='compress',
            sys='init',
            pre=[self.sheared_at_5nN],
            post=[self.ready_to_shear_at_15nN])

        add_mdrun_op(
            op_name='shear_15nN', name='shear_15nN',
            pre=[self.ready_to_shear_at_15nN],
            post=[self.sheared_at_15nN])

        add_grompp_extend_op(
            op_name='shear_15nN_extend_grompp', name='shear_15nN',
            pre=[self.shear_reran_at_5nN],
            post=[self.ready_to_extend_shear_at_15nN])

        add_mdrun_extend_op(
            op_name='shear_15nN_extend', name='shear_15nN',
            pre=[self.ready_to_extend_shear_at_15nN],
            post=[self.extended_shear_at_15nN])

        add_grompp_rerun_op(
            op_name='shear_15nN_rerun_grompp', name='shear_15nN', gro='compress',
            sys='init',
            pre=[self.extended_shear_at_15nN],
            post=[self.ready_to_rerun_shear_at_15nN])

        add_mdrun_rerun_op(
            op_name='shear_15nN_rerun', name='shear_15nN',
            pre=[self.ready_to_rerun_shear_at_15nN],
            post=[self.shear_reran_at_15nN])

        add_grompp_op(
            op_name='shear_25nN_grompp', name='shear_25nN', gro='compress',
            sys='init',
            pre=[self.shear_reran_at_15nN],
            post=[self.ready_to_shear_at_25nN])

        add_mdrun_op(
            op_name='shear_25nN', name='shear_25nN',
            pre=[self.ready_to_shear_at_25nN],
            post=[self.sheared_at_25nN])

        add_grompp_extend_op(
            op_name='shear_25nN_extend_grompp', name='shear_25nN',
            pre=[self.extended_shear_at_15nN],
            post=[self.ready_to_extend_shear_at_25nN])

        add_mdrun_extend_op(
            op_name='shear_25nN_extend', name='shear_25nN',
            pre=[self.ready_to_extend_shear_at_25nN],
            post=[self.extended_shear_at_25nN])

        add_grompp_rerun_op(
            op_name='shear_25nN_rerun_grompp', name='shear_25nN', gro='compress',
            sys='init',
            pre=[self.shear_reran_at_15nN],
            post=[self.ready_to_rerun_shear_at_25nN])

        add_mdrun_rerun_op(
            op_name='shear_25nN_rerun', name='shear_25nN',
            pre=[self.ready_to_rerun_shear_at_25nN],
            post=[self.shear_reran_at_25nN])

    def write_script_header(self, script, **kwargs):
        super().write_script_header(script, **kwargs)
        script.writeline('export CRAY_CUDA_MPS=1')
        script.writeline()

    def write_script_operations(self, script, operations, background=False,
                                **kwargs):
        op_list = list(operations)
        op_names = [op.name for op in op_list]
        # Assert that all operation names are the same
        if 'initialize' in op_names:
            script.writeline('export PATH=/ccs/proj/mat149/anaconda/titan/bin:$PATH')
            script.writeline('source activate azsconda')
        elif 'fix_overlaps' in op_names:
            script.writeline('module swap PrgEnv-pgi PrgEnv-gnu')
            script.writeline('module load fftw')
            script.writeline('module load lammps')
        else:
            script.writeline('module load gromacs/5.1.0')
        script.writeline()
        if len(op_list) > 50:
            cmds = [op.cmd for op in op_list]
            cmds = ('{}'.format(cmd) for cmd in cmds)
            cmd = 'wraprun {}'.format(' : '.join(cmds))
            if background:
                cmd = script._env.bg(cmd)
            script.writeline('module load python')
            script.writeline('module load wraprun')
            script.writeline(cmd)
        else:
            for op in op_list:
                self.write_human_readable_statepoint(script, op.job)
                if op.mpi:
                    script.write_cmd(op.cmd.format(job=op.job), np=op.np,
                                     bg=background)
                else:
                    script.write_cmd(op.cmd.format(job=op.job), bg=background)
                script.writeline()

if __name__ == '__main__':
    MyProject().main()
