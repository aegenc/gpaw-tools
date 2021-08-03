import numpy as np
from ase import *
from gpaw import GPAW, PW
# Sample Cut-off Energy Optimization GPAW Input for LRG Studies
# by Sefer Bora Lisesivdin
# July 2021 - Corrected version
# March 2020 - First Version 
# Usage: $ gpaw python script.py
#
#-------------------------------------------------------------
# ENTER PARAMETERS
# -------------------------------------------------------------
cutoff_min = 200
cutoff_max = 400
cutoff_step = 50

kpts_x = 7
kpts_y = 7
kpts_z = 7



# -------------------------------------------------------------
# Bulk Configuration
# -------------------------------------------------------------
bulk_configuration = Atoms(
    [
    Atom('Si', ( 0.0, 0.0, 0.0 )),
    Atom('Si', ( 1.35765, 1.35765, 1.35765 )),
    ],
    cell=[(0.0, 2.7153, 2.7153), (2.7153, 0.0, 2.7153), (2.7153, 2.7153, 0.0)],
    pbc=True,
    )
# -------------------------------------------------------------
# CONVERGE CUTOFF
# -------------------------------------------------------------
cell0 = bulk_configuration.cell
f = open('Table-CutOff.txt', 'a')
f.write('Cut-off_Energy  Total_Energy\n')
for ecut in range(cutoff_min, cutoff_max+1, cutoff_step):
    bulk_configuration.calc = GPAW(mode=PW(ecut),
                              xc='PBE',
                              kpts=(kpts_x, kpts_y, kpts_z),
                              parallel={'band': 1},
                              basis='dzp',
                              txt='Optimize-0-1-CutOff-%d.txt' % ecut)
    print ("Cut-off energy:"+str(ecut))
#    for eps in np.linspace(-0.02, 0.02, 5):
#        bulk_configuration.cell = (1 + eps) * cell0
#        bulk_configuration.get_potential_energy()
#        print ("eps:"+str(eps))
    f.write(str(ecut)+'  '+str(bulk_configuration.get_potential_energy())+'\n')
f.close()

