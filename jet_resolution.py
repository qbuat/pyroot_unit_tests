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
from ROOT import JERTool, JERSmearingTool

store_helper = ROOT.xAOD.StorePyHelper()

jer_tool = JERTool('JERTool')
jer_tool.setProperty('std::string')("PlotFileName", "JetResolution/JERProviderPlots_2012.root")
jer_tool.setProperty('std::string')("CollectionName", "AntiKt4LCTopoJets")
jer_tool.setProperty('std::string')("BeamEnergy", "8TeV")
jer_tool.setProperty('std::string')("SimulationType", "FullSim")
jer_tool.initialize()

jer_smearing_tool = JERSmearingTool('JERSmearingTool')
jer_smearing_tool.setProperty('std::string')('JERToolName', 'JERTool')
jer_smearing_tool.setJERTool(jer_tool)
jer_smearing_tool.setNominalSmearing(True)
jer_smearing_tool.initialize()


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
    jer_smearing_tool.applyCorrection(jet_copy)
    print 'AFTER Jet: pt(orig), pt(copy) = ', jet.pt(), jet_copy.pt()
    # getattr(store, 'print')()
    store.clear()

