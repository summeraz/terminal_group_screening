import flow
from flow.environment import get_environment
from flow.environment import format_timedelta


__all__ = ['get_environment']


class TitanEnvironment(flow.environment.DefaultTorqueEnvironment):
    hostname_pattern = 'titan'
    cores_per_node = 16

    @classmethod
    def mpi_cmd(cls, cmd, np=16, wrap=False):
        return cmd
        '''
        if wrap:
            return cmd
        else:
            cmd = 'aprun {}'.format(cmd)
            return cmd
        '''

    @classmethod
    def script(cls, _id, nn, walltime, **kwargs):
        js = super(TitanEnvironment, cls).script(_id)
        js.writeline('#PBS -j oe')
        js.writeline('#PBS -l nodes={}'.format(nn))
        js.writeline('#PBS -l walltime={}'.format(format_timedelta(walltime)))
        js.writeline('#PBS -A MAT149')
        js.writeline('#PBS -m abe')
        js.writeline('#PBS -M andrew.z.summers@gmail.com')
        return js
