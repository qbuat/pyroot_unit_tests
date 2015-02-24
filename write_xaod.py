import os

import ROOT
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
ROOT.xAOD.Init().ignore()
ROOT.xAOD.AuxContainerBase()

files = [
    '/cluster/data01/qbuat/xaod_skims/testinput/mc12_powhegpythia_ztautau/mc14_8TeV.147808.PowhegPythia8_AU2CT10_Ztautau.merge.AOD.e2372_s1933_s1911_r5591_r5625/AOD.01512482._001049.pool.root.1',
]

in_file = ROOT.TFile(files[0], 'read')
out_file = ROOT.TFile('out.root', 'recreate')

event = ROOT.xAOD.TEvent()
event.readFrom(in_file).ignore()
event.writeTo(out_file).ignore()

for i in xrange(event.getEntries()):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 
    event.getEntry(i)
    print 'Copy containers ...'
    event.copy('EventInfo')
    event.copy('AntiKt4LCTopoJets')
    event.copy('TauRecContainer')
    event.fill()
event.finishWritingTo(out_file)

out_file.Close()
in_file.Close()

print 30 * '*'

ch = ROOT.TChain('CollectionTree')
ch.Add('out.root')
tree = ROOT.xAOD.MakeTransientTree(ch)

for i in xrange(tree.GetEntries()):
    tree.GetEntry(i)
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 
    print [tau.pt() for tau in tree.TauRecContainer]

