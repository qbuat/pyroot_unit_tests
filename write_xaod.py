import os

import ROOT
try:
    ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
    ROOT.xAOD.Init().isSuccess()
except:
    raise RuntimeError

files = [
    '/cluster/data01/qbuat/xaod_skims/testinput/mc12_powhegpythia_ztautau/mc14_8TeV.147808.PowhegPythia8_AU2CT10_Ztautau.merge.AOD.e2372_s1933_s1911_r5591_r5625/AOD.01512482._001049.pool.root.1',
]

in_file = ROOT.TFile(files[0], 'read')

event = ROOT.xAOD.TPyEvent()
store = ROOT.xAOD.TPyStore()
store_helper = ROOT.xAOD.StorePyHelper()

# event.readFrom(in_file).ignore()
try:
    out_file = ROOT.TFile('out.root', 'recreate')
    event.writeTo(out_file).isSuccess()
except:
    raise RuntimeError

tree = ROOT.xAOD.MakeTransientTree(in_file)


for i, evt in enumerate(tree):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 
    print 'Copy containers ...'
    ei = evt.EventInfo
    taus = evt.TauRecContainer
    taus_copy = store_helper.shallowCopyTauJets(taus)
    jets = evt.AntiKt4LCTopoJets
    event.record(ei, 'EventInfo', ei.__class__.__name__).isSuccess()
    # event.record(
    #     ei.getConstStore(), 'EventInfoAux', 
    #     ei.getConstStore().__class__.__name__).isSuccess()

    event.record(taus, 'Taus', taus.__class__.__name__).isSuccess()
    event.record(
        taus.getConstStore(), 'TausAux', 
        taus.getConstStore().__class__.__name__).isSuccess()

    # taus_copy.second.setShallowIO(False)
    # event.record(taus_copy.first, 'Taus_copy', taus_copy.first.__class__.__name__).isSuccess()
    # event.record(taus_copy.second, 'TausAux_copy', taus_copy.second.__class__.__name__).isSuccess()
    event.record(jets, 'Jets', jets.__class__.__name__).isSuccess()
    event.record(jets.getConstStore(), 'JetsAux', jets.getConstStore().__class__.__name__).isSuccess()
    
    event.fill()
    store.clear()

try: 
    event.finishWritingTo(out_file).isSuccess()
    out_file.Close()
    in_file.Close()
except:
    raise RuntimeError


print 30 * '*'
ch = ROOT.TChain('CollectionTree')
ch.Add('out.root')
tree = ROOT.xAOD.MakeTransientTree(ch)

for i in xrange(tree.GetEntries()):
    tree.GetEntry(i)
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 
    # print tree.EventInfo
    print tree.Taus
    # tree.Taus.setStore(tree.TausAuxDyn)
    # print tree.jets
    # print tree.AntiKt4LCTopoJets[0].pt()
    # print tree.TauRecContainer[0].pt()
    # taus = [tree.Taus.at(i) for i in xrange(tree.Taus.size())]
    # print [tau.pt() for tau in taus]

