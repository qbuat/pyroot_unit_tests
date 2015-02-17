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

muon_tool = ROOT.CP.MuonSelectionTool('MuonSelectionTool')
# use loose quality and |eta|>2.5
muon_tool.setProperty('int')('MuQuality', 2)
muon_tool.initialize()

def veto_event_with_muon(event):
   for muon in event.Muons:
      if muon.pt() <= 10 * GeV:
           continue
      if not muon_tool.accept(muon):
          continue
      return False
   return True



for i, event in enumerate(tree):
    if i > 10:
        break
    print '######  EVENT {0} ######'.format(i) 
    for muon in event.Muons:
        if muon.pt() <= 10000.:
            continue
        if not muon_tool.accept(muon):
            continue
        print 'This is good muon with pt, eta, phi, m =', muon.p4().Print()
    print 20 * '-'

