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

mc_vec = ROOT.std.vector('string')()
data_vec = ROOT.std.vector('string')()
mc_vec.push_back("PileupReweighting/mc14v1_defaults.prw.root")
data_vec.push_back('./../lumi/2012/ilumicalc_histograms_None_200842-215643.root')

pileup_tool = ROOT.CP.PileupReweightingTool('pileup_tool')
pileup_tool.setProperty('ConfigFiles', mc_vec)
pileup_tool.setProperty('LumiCalcFiles', data_vec)
pileup_tool.setProperty('int')('DefaultChannel', 0)
pileup_tool.initialize()
getattr(pileup_tool, 'print')()

for i, event in enumerate(tree):
    ei = event.EventInfo
    pileup_tool.apply(ei)
    print '######  EVENT {0} ######'.format(i) 
    print 'PileUp weight =', ei.auxdataConst('double')('PileupWeight')
    print 20 * '-'
    

