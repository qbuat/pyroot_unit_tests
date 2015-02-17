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


from ROOT.TauAnalysisTools import TauEfficiencyCorrectionsTool
tau_eff_tool = TauEfficiencyCorrectionsTool('tau_eff_tool')
tau_eff_tool.setProperty('int')('IDLevel', 3)
tau_eff_tool.initialize()

systs = tau_eff_tool.recommendedSystematics()

for i, event in enumerate(tree):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 

    taus = tree.TauRecContainer
    for tau in taus:
        if tau.pt() > 20000 and abs(tau.eta()) < 2.4:
            tau_eff_tool.applyEfficiencyScaleFactor(tau)
            print 'Nominal: TauScaleFactorJetID = %f' % tau.auxdataConst('double')('TauScaleFactorJetID')
            for s in systs:
                s_set = ROOT.CP.SystematicSet()
                s_set.insert(s)
                tau_eff_tool.applySystematicVariation(s_set)
                tau_eff_tool.applyEfficiencyScaleFactor(tau)
                print "%s: TauScaleFactorJetID = %f" % (s.name(), tau.auxdataConst('double')('TauScaleFactorJetID'))

