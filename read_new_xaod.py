import os

import ROOT
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')

if not ROOT.xAOD.Init().isSuccess():
    raise RuntimeError


print 30 * '*'
ch = ROOT.TChain('CollectionTree')
ch.Add('out.root')
tree = ROOT.xAOD.MakeTransientTree(ch, ROOT.xAOD.TEvent.kBranchAccess)
for i in xrange(tree.GetEntries()):
    tree.GetEntry(i)
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 
    print tree.EventInfo
    print tree.Taus
    taus = tree.Taus
    if taus.size() > 0:
        print taus[0].pt()
    # print tree.Taus[0].pt()
    # print tree.jets
    # print tree.AntiKt4LCTopoJets[0].pt()
    # print tree.TauRecContainer[0].pt()
    # taus = [tree.Taus.at(i) for i in xrange(tree.Taus.size())]
    # print [tau.pt() for tau in taus]

