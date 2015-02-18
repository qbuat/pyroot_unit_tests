import ROOT
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
ROOT.xAOD.Init().ignore()
ROOT.xAOD.AuxContainerBase()


store = ROOT.xAOD.TStore()
event = ROOT.xAOD.TEvent()
TOOLS = ROOT.asg.ToolStore()
TOOLS_NAME = [
    'jet_calib_tool',
    'tau_smearing_tool',
    'jet_uncert_tool',
    'met_maker_tool',
    'met_systematic_tool',
    'jer_smearing_tool',
]

# --> jet calibration tool
from ROOT import JetCalibrationTool
jet_calib_tool = JetCalibrationTool('jet_calib_tool')
jet_calib_tool.setProperty('std::string')('JetCollection', 'AntiKt4LCTopo')
jet_calib_tool.setProperty('std::string')('ConfigFile', 'JES_Full2012dataset_May2014.config')
jet_calib_tool.setProperty('std::string')('CalibSequence', 'JetArea_Residual_Origin_EtaJES_GSC')
jet_calib_tool.setProperty('bool')('IsData', False)
jet_calib_tool.initialize()

# --> jet resolution tool
from ROOT import JERTool, JERSmearingTool
jer_tool = JERTool('jer_tool')
jer_tool.setProperty('std::string')("PlotFileName", "JetResolution/JERProviderPlots_2012.root")
jer_tool.setProperty('std::string')("CollectionName", "AntiKt4LCTopoJets")
jer_tool.setProperty('std::string')("BeamEnergy", "8TeV")
jer_tool.setProperty('std::string')("SimulationType", "FullSim")
jer_tool.initialize()
jer_smearing_tool = JERSmearingTool('jer_smearing_tool')
jer_smearing_tool.setProperty('std::string')('JERToolName', 'jer_tool')
jer_smearing_tool.setJERTool(jer_tool)
jer_smearing_tool.setNominalSmearing(True)
jer_smearing_tool.initialize()

# --> tau smearing tool
from ROOT.TauAnalysisTools import TauSmearingTool
tau_smearing_tool = TauSmearingTool('tau_smearing_tool')
tau_smearing_tool.setProperty('bool')('IsData', False)
tau_smearing_tool.initialize()

# --> jet uncertainties tool
from ROOT import JetUncertaintiesTool
jet_uncert_tool = JetUncertaintiesTool('jet_uncert_tool')
jet_uncert_tool.setProperty('std::string')('JetDefinition', 'AntiKt4LCTopo')
jet_uncert_tool.setProperty('std::string')('MCType', 'MC12')
jet_uncert_tool.setProperty('std::string')('ConfigFile', 'JES_2012/Final/InsituJES2012_23NP_ByCategory.config')
jet_uncert_tool.initialize()

# --> MET maker tool
from ROOT.met import METMaker
met_making_tool = METMaker('met_maker_tool')
met_making_tool.initialize()

# --> MET Syst tool
from ROOT.met import METSystematicsTool
met_syst_tool = METSystematicsTool('met_systematic_tool')
met_syst_tool.setProperty('std::string')('ConfigSoftTrkFile', 'TrackSoftTerms.config')
met_syst_tool.setProperty('std::string')('ConfigSoftCaloFile', 'METRefFinal.config')
met_syst_tool.initialize()


print 40 * '='
for name in TOOLS_NAME:
    print '-------- {0} -------'.format(name)
    tool = TOOLS.get(name)
    if hasattr(tool, 'recommendedSystematics'):
        print tool.name(), hasattr(tool, 'applySystematicVariation')
        systs = tool.recommendedSystematics()
        print [syst.name() for syst in systs]


        # for syst in systs:
        #     print syst.name()
        #     syst_set = ROOT.CP.SystematicSet()
        #     syst_set.insert(syst)
        #     tool.applySystematicVariation(syst_set)

        # systs_l = [syst for syst in systs]
        # print
        # print systs_l[0].name(), systs_l[0] in systs
