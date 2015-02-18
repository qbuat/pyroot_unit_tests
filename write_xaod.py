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
    event.copy('AntiKt4LCTopoJets').ignore()
    event.fill()

event.finishWritingTo(out_file).ignore()

