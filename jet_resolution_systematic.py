import ROOT
ROOT.gROOT.Macro('$ROOTCOREDIR/scripts/load_packages.C')
ROOT.xAOD.Init().ignore()
ROOT.xAOD.AuxContainerBase()

store = ROOT.xAOD.TStore()
event = ROOT.xAOD.TEvent()
TOOLS = ROOT.asg.ToolStore()

# # --> jet resolution tool
from ROOT import JERTool, JERSmearingTool
jer_tool = JERTool('JERTool')
jer_tool.setProperty('std::string')("PlotFileName", "JetResolution/JERProviderPlots_2012.root")
jer_tool.setProperty('std::string')("CollectionName", "AntiKt4LCTopoJets")
jer_tool.setProperty('std::string')("BeamEnergy", "8TeV")
jer_tool.setProperty('std::string')("SimulationType", "FullSim")
jer_tool.initialize()

jer_smearing_tool = JERSmearingTool('JERSmearingTool')
jer_smearing_tool.setProperty('std::string')('JERToolName', 'JERTool')
jer_smearing_tool.setJERTool(jer_tool)
jer_smearing_tool.setNominalSmearing(True)
jer_smearing_tool.initialize()

systs = jer_smearing_tool.recommendedSystematics()
print systs
for syst in systs:
    print syst.name()
