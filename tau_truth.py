import os

import ROOT
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
ROOT.xAOD.Init().ignore()
ROOT.xAOD.AuxContainerBase()

files = [
    '/cluster/data01/qbuat/xaod_skims/testinput/mc12_powhegpythia_ztautau/mc14_8TeV.147808.PowhegPythia8_AU2CT10_Ztautau.merge.AOD.e2372_s1933_s1911_r5591_r5625/AOD.01512482._001049.pool.root.1',
]

chain = ROOT.TChain('CollectionTree')
for f in files:
    chain.Add(f)

tree = ROOT.xAOD.MakeTransientTree(chain)
print tree



from ROOT.TauAnalysisTools import TauTruthMatchingTool
tau_truth_tool = TauTruthMatchingTool('tau_truth_tool')

for i, event in enumerate(tree):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 

    truth_parts = event.TruthParticle
    tau_truth_tool.setTruthParticleContainer(truth_parts)
    tau_truth_tool.createTruthTauContainer()

    truth_taus = tau_truth_tool.getTruthTauContainer()
    truth_taus_aux = tau_truth_tool.getTruthTauAuxContainer()
    truth_taus.setNonConstStore(truth_taus_aux)
    for truth_tau in truth_taus:
        print 'pt_vis: {0}'.format(truth_tau.auxdataConst('double')('pt_vis'))
        print 'eta_vis: {0}'.format(truth_tau.auxdataConst('double')('eta_vis'))

