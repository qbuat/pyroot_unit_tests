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

from ROOT.met import METMaker

met_making_tool = METMaker('met_maker_tool')
# met_making_tool.setProperty('double')('JetPtCut', 20000.)
# met_making_tool.setProperty('double')('JetJVFCut', 0.25)
# met_making_tool.setProperty('double')('JetMinEFrac', 0.5)
# met_making_tool.setProperty('double')('JetMinWeightedPt', 0.)
# met_making_tool.setProperty('bool')('DoJetJVFCut', True)
# met_making_tool.setProperty('bool')('CorrectJetPhi', False)
met_making_tool.initialize()

store_helper = ROOT.xAOD.StorePyHelper()
store = ROOT.xAOD.TStore()

count_10_events = 0
for i, event in enumerate(tree):
    if count_10_events > 10:
        break
    mets = tree.MET_RefFinal
    met = mets[0]

    if met.met() > 0:
        count_10_events +=1
    mets_copy = store_helper.shallowCopyMissingETContainer(mets)
    met_copy = mets_copy[0]
    taus = event.TauRecContainer
    taus_copy = store_helper.shallowCopyTauJetContainer(taus)
    electrons = event.ElectronCollection
        
    if met.met() > 0:
        print 20 * '-'
        print '######  EVENT {0} ######'.format(i) 
        print 'BEFORE Met: pt(orig), pt(copy) = ', met.met(), met_copy.met()
    # met_calib_tool.applyCalibration(met_copy)
        print 'AFTER Met: pt(orig), pt(copy) = ', met.met(), met_copy.met()

    store.clear()

