import os

import ROOT
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
ROOT.xAOD.Init().ignore()
ROOT.xAOD.AuxContainerBase()

files = [
    '/cluster/data01/qbuat/xaod_skims/testinput/data12/data12_8TeV.00203335.physics_JetTauEtmiss.merge.DAOD_HIGG4D1.r5723_p1751_p1784_tid04275621_00/DAOD_HIGG4D1.04275621._000007.pool.root.1',
]

chain = ROOT.TChain('CollectionTree')
for f in files:
    chain.Add(f)

tree = ROOT.xAOD.MakeTransientTree(chain)
print tree

grl_vec = ROOT.std.vector('string')()
grl_vec.push_back("../hhntup/grl/2012/data12_8TeV.periodAllYear_DetStatus-v61-pro14-02_DQDefects-00-01-00_PHYS_StandardGRL_All_Good.xml")

from ROOT import GoodRunsListSelectionTool
grl_tool = GoodRunsListSelectionTool('grl_tool')
grl_tool.setProperty('GoodRunsListVec', grl_vec)
grl_tool.initialize()

for i, event in enumerate(tree):
    if i > 10:
        break
    ei = event.EventInfo
    print '######  EVENT {0} ######'.format(i) 
    print grl_tool.passRunLB(ei)
    

