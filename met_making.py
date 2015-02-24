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

# TOOLS = ROOT.asg.ToolStore()


tree = ROOT.xAOD.MakeTransientTree(chain)
print tree

# from ROOT.met import METMaker
# met_making_tool = METMaker('met_maker_tool')
# met_making_tool.setProperty('double')('JetPtCut', 20000.)
# met_making_tool.setProperty('double')('JetJVFCut', 0.25)
# met_making_tool.setProperty('double')('JetMinEFrac', 0.5)
# met_making_tool.setProperty('double')('JetMinWeightedPt', 0.)
# met_making_tool.setProperty('bool')('DoJetJVFCut', True)
# met_making_tool.setProperty('bool')('CorrectJetPhi', False)
# sc = met_making_tool.initialize()

from ROOT import METHandler
met_tool = METHandler(False)

store_helper = ROOT.xAOD.StorePyHelper()
store = ROOT.xAOD.TStore()

for i, event in enumerate(tree):
    if i > 100:
        break
    mets = tree.MET_RefFinal
    met = mets[0]


    mets_copy = store_helper.shallowCopyMissingETContainer(mets)
    met_copy = mets_copy[0]
    # taus_copy = store_helper.shallowCopyTauJetContainer(taus)

    electrons = event.ElectronCollection
    photons = event.PhotonCollection
    taus = event.TauRecContainer
    muons = event.Muons
    jets = event.AntiKt4LCTopoJets
    met_map = event.METMap_RefFinal
    sc = met_tool.setMET(
        mets_copy, met_map, electrons, photons,
        taus, muons, jets)
    calib_mets = met_tool.getCalibratedMET()
    met_calib = calib_mets[0]
    # print calib_met, calib_met[0].met()
    if met.met() > 0:
        print 20 * '-'
        print '######  EVENT {0} ######'.format(i) 
        print 'MET (orig), (copy), (calib) = ', met.met(), met_copy.met(), met_calib.met()
    store.clear()

