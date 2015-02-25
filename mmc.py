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

from ROOT import MissingMassTool
mass_tool = MissingMassTool('mass_tool')
mass_tool.initialize()

for i, event in enumerate(tree):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 
    taus = event.TauRecContainer
    print len(taus)
    if len(taus) < 2:
        continue
    tau1, tau2 = taus[0], taus[1]

    jets = tree.AntiKt4LCTopoJets    
    njets_25 = 0
    for i in xrange(jets.size()):
        jet = jets.at(i)
        if jet.pt() > 25000.:
            njets_25 += 1
    print njets_25
    met = tree.MET_RefFinal[0]
    ei = tree.EventInfo
    mass_tool.apply(ei, tau1, tau2, met, njets_25)
    print ei.auxdataConst('double')('mmc0_mass')
    print ei.auxdataConst('double')('mmc1_mass')
    print ei.auxdataConst('double')('mmc2_mass')
    reso = mass_tool.GetResonanceVec(0)
    print reso.Pt(), reso.Eta(), reso.Phi()
