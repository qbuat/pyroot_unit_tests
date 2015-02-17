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
from ROOT import JetUncertaintiesTool

store_helper = ROOT.xAOD.StorePyHelper()


from ROOT import JetUncertaintiesTool
jet_uncert_tool = JetUncertaintiesTool('JESProvider')
jet_uncert_tool.setProperty('std::string')('JetDefinition', 'AntiKt4LCTopo')
jet_uncert_tool.setProperty('std::string')('MCType', 'MC12')
jet_uncert_tool.setProperty('std::string')('ConfigFile', 'JES_2012/Final/InsituJES2012_23NP_ByCategory.config')
jet_uncert_tool.initialize()

syst_set = ROOT.CP.SystematicSet()
syst_set.insert(ROOT.CP.SystematicVariation('Flavor_Response', -3.0))
syst_set.insert(ROOT.CP.SystematicVariation('Flavor_Composition', -2.0))

jet_uncert_tool.applySystematicVariation(syst_set)



store = ROOT.xAOD.TStore()
for i, event in enumerate(tree):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 

    jets = tree.AntiKt4LCTopoJets
    jets_copy = store_helper.shallowCopyJetContainer(jets)
    jet = jets[0]

    jet_copy = jets_copy[0]
    print 'BEFORE Jet: pt(orig), pt(copy) = ', jet.pt(), jet_copy.pt()
    jet_uncert_tool.applyCorrection(jet_copy)
    print 'AFTER Jet: pt(orig), pt(copy) = ', jet.pt(), jet_copy.pt()
    store.clear()

