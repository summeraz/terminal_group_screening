#!/usr/bin/env python
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories."""
import logging
import argparse
from hashlib import sha1

import signac
import numpy as np


'''
-----------------------------
16 terminal group chemistries
-----------------------------
'''
terminal_groups = ['acetyl', 'amino', 'carboxyl', 'cyano', 'cyclopropyl',
                   'ethylene', 'fluorophenyl', 'hydroxyl', 'isopropyl', 
                   'methoxy', 'methyl', 'nitro', 'nitrophenyl',
                   'perfluoromethyl', 'phenyl', 'pyrrole']

'''
----------------------
Initialize the project
----------------------
'''
def main(args, random_seed):
    project = signac.init_project('TerminalGroupScreening')
    statepoints = []
    for replication_index in range(args.num_replicas):
        for terminal_group in terminal_groups:
            for chainlength in np.linspace(5, 17, 5):
                statepoint = dict(
                        # Carbon backbone length
                        chainlength = int(chainlength),
                        # Number of monolayer chains
                        n = 100,
                        # Random seed
                        seed = random_seed*(replication_index + 1),
                        # Terminal group chemistry
                        terminal_group = terminal_group)
                project.open_job(statepoint).init()
                statepoints.append(statepoint)

    '''
    ------------------------------------------
    Writing statpoints to hash table as backup
    ------------------------------------------
    '''
    project.write_statepoints(statepoints)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Initialize the data space.")
    parser.add_argument(
        'random',
        type=str,
        help="A string to generate a random seed.")
    parser.add_argument(
        '-n', '--num-replicas',
        type=int,
        default=1,
        help="Initialize multiple replications.")
    args = parser.parse_args()

    # Generate an integer from the random str.
    try:
        random_seed = int(args.random)
    except ValueError:
        random_seed = int(sha1(args.random.encode()).hexdigest(), 16) % (10 ** 8)

    logging.basicConfig(level=logging.INFO)
    main(args, random_seed)
