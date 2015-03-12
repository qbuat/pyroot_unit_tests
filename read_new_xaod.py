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
    print tree.EventInfo.runNumber()
    
    taus = tree.Taus
    if taus.size() > 0:
        print 'First tau pT = ', taus[0].pt()
        
    jets = tree.Jets
    if jets.size() > 0:
        print 'First jet pT = ', jets[0].pt()
