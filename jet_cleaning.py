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


pt_thresh = 20000.
eta_max = 4.5
from ROOT import JetCleaningTool
jet_cleaning_tool = JetCleaningTool(JetCleaningTool.LooseBad)


for i, event in enumerate(tree):
    print i
    jets = event.AntiKt4LCTopoJets
    event_pass = True
    for jet in jets:
        if jet.pt() <= pt_thresh or abs(jet.eta()) >= eta_max:
            continue
        isbadloose = jet_cleaning_tool.accept(jet)
        if isbadloose == True:
            print '######  EVENT {0} ######'.format(i) 
            print 'bad jet'
            print 20 * '-'
            event_pass = False

