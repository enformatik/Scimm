#!/usr/bin/env python
import os

############################################################
# install_physcimm.py
#
# Compile source and set paths for Physcimm.
#
# Author: David Kelley
############################################################

prior_phymm_dir = ''

############################################################
# main
############################################################
def main():
    print 'Please note that this will install Phymm, which \
           will likely take ~24 hours and use ~50 GB of \
           space. If you already have Phymm installed, \
           edit this script and set "prior_phymm_dir" to \
           the package directory path'

    installdir = os.getcwd()

    # IMM code
    os.chdir('glimmer3.02/src')
    os.system('make clean; make')
    os.chdir('../..')
    if not os.path.isfile('bin/simple-score'):
        os.chdir('bin')
        os.system('ln -s ../glimmer3.02/bin/simple-score')
        os.chdir('..')
    if not os.path.isfile('bin/build-icm'):
        os.chdir('bin')
        os.system('ln -s ../glimmer3.02/bin/build-icm')
        os.chdir('..')
    
    # Scimm
    os.system('sed -i \'s,scimm_bin = "[a-zA-Z/]*",scimm_bin = "%s/bin",\' bin/scimm.py' % installdir) 
    os.system('rm bin/scimm.py.bak')

    # Phymm
    os.system('sed -i \'s,phymmdir = "[a-zA-Z/]*",phymmdir = "%s/phymm",\' bin/physcimm.py' % installdir) 
    os.system('rm bin/physcimm.py.bak')
    if prior_phymm_dir:
        os.system('ln -s %s phymm' % prior_phymm_dir)
    else:
        os.chdir('phymm')
        os.system('./phymmInstall.pl')
        os.chdir('..')    

############################################################
# __main__
############################################################
if __name__ == '__main__':
    main()