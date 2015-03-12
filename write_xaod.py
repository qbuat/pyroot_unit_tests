import os

import ROOT
try:
    ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
    ROOT.xAOD.Init().isSuccess()
except:
    raise RuntimeError

files = [
    '/cluster/data01/qbuat/xaod_skims/'\
    'testinput/mc12_powhegpythia_ztautau/'
    'mc14_8TeV.147808.PowhegPythia8_AU2CT10_Ztautau.'
    'merge.AOD.e2372_s1933_s1911_r5591_r5625/AOD.01512482._001049.pool.root.1',
]

in_file = ROOT.TFile(files[0], 'read')

from xAODRootAccess.TPyEvent import TPyEvent
from xAODRootAccess.TPyStore import TPyStore
event = TPyEvent()
store = TPyStore()
store_helper = ROOT.xAOD.StorePyHelper()

# event.readFrom(in_file).ignore()
out_file = ROOT.TFile('out.root', 'recreate')
if not event.writeTo(out_file).isSuccess():
    raise RuntimeError

in_tree = ROOT.xAOD.MakeTransientTree(in_file)


for i, evt in enumerate(in_tree):
    if i > 10:
        break
    print 20 * '-'
    print '######  EVENT {0} ######'.format(i) 
    print 'Copy containers ...'
    ei = evt.EventInfo
    taus = evt.TauRecContainer
    jets = evt.AntiKt4LCTopoJets

    if not event.record(ei, 'EventInfo').isSuccess():
        raise RuntimeError

    if not event.record(ei.getConstStore(), 'EventInfoAux.').isSuccess(): 
        raise RuntimeError

    if not event.record(taus, 'Taus').isSuccess():
        raise RuntimeError
    if not event.record(taus.getConstStore(), 'TausAux.') .isSuccess():
        raise RuntimeError


    # taus_copy = store_helper.shallowCopyTauJets(taus)
    # print taus_copy
    # taus_copy.second.setShallowIO(False)
    # if not event.record(taus_copy.first, 'TausCopy', taus_copy.first.__class__.__name__).isSuccess():
    #     raise RuntimeError
    # if not event.record(taus_copy.second, 'TausCopyAux.', taus_copy.second.__class__.__name__).isSuccess():
    #     raise RuntimeError
    

    if not event.record(jets, 'Jets').isSuccess():
        raise RuntimeError
    if not event.record(jets.getConstStore(), 'JetsAux.').isSuccess():
        raise RuntimeError
    
    event.fill()
    getattr(store, 'print')()
    store.clear()

event.finishWritingTo(out_file).isSuccess()

out_file.Close()
in_file.Close()

