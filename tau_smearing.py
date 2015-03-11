import os

import ROOT
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
ROOT.xAOD.Init().ignore()
ROOT.xAOD.AuxContainerBase()

files = [
    '/cluster/data01/qbuat/xaod_skims/testinput/'
    'mc12_powhegpythia_ztautau/'
    'mc14_8TeV.147808.PowhegPythia8_AU2CT10_Ztautau'
    '.merge.AOD.e2372_s1933_s1911_r5591_r5625/AOD.01512482._001049.pool.root.1',
    ]

chain = ROOT.TChain('CollectionTree')
for f in files:
    chain.Add(f)

tree = ROOT.xAOD.MakeTransientTree(chain)
print tree

from ROOT.TauAnalysisTools import TauSmearingTool
tau_smearing_tool = TauSmearingTool('tau_smearing_tool')
# Just a test - This is wrong to apply the shift on MC
tau_smearing_tool.setProperty('bool')('IsData', True)
tau_smearing_tool.initialize()
systs = tau_smearing_tool.recommendedSystematics()

store_helper = ROOT.xAOD.StorePyHelper()

store = ROOT.xAOD.TPyStore()
for i, event in enumerate(tree):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 

    taus = tree.TauRecContainer
    taus_copy = store_helper.shallowCopyTauJetContainer(taus)
    tau = taus[0]
    tau_copy = taus_copy[0]

    print 'BEFORE Tau: pt(orig), pt(copy) = ', tau.pt(), tau_copy.pt()
    cc = tau_smearing_tool.applyCorrection(tau_copy)
    print cc
    print 'AFTER Tau: pt(orig), pt(copy) = ', tau.pt(), tau_copy.pt()
    for sys in systs:
        print sys.name()
        s_set = ROOT.CP.SystematicSet()
        s_set.insert(sys)
        sc = tau_smearing_tool.applySystematicVariation(s_set)
        print sc
        taus_mod =  store_helper.shallowCopyTauJetContainer(taus, 'Taus_' + sys.name())
        tau_mod = taus_mod[0]
        cc = tau_smearing_tool.applyCorrection(tau_mod)
        print cc
        print '\t', sys.name(), tau_mod.pt()
    getattr(store, 'print')()

    store.clear()

