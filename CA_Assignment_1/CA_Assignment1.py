
"""

EH2745 Computer Applications in Power Systems
Assignment I
Submitted on Fri May 12 2023


@author1: Yashwanth Damodaran
@author2: Ran Lei

This code is our own work. When solving this assignment we took references from various code repositories on GitHub.
The solution was shared with other teams in order to verify the correctness and to encourage co-operation.


"""

import xml.etree.ElementTree as ET
import pandapower.networks
import pandapower.topology
import pandapower.plotting
import pandapower.converter
import pandapower.estimation
import pandapower.plotting 
import pandapower.plotting.to_html as html_output
import pandapower as pp
import random
import matplotlib.pyplot as plt

"""
According to the paper:"An Efficient Method for Extracting Network Information from the CIM Asset Model" initially all classes are introduced and initialized
"""

"""
This code allows the user to choose between three sets of input files, and it appears to work correctly assuming the files exist 
and are in the correct location.The code prompts the user to select between these options for a file to be parsed, 
either a reduced test file or an unreduced BE CIM case or a complicated NL CIM case. This is to show the interoperability of this code and its 
abilty to run various CIM files
"""



selection = input('Please select the assignment file or test file.\nReduced test file = 1, unreduced BE CIM case = 2, NL CIM case = 3'+'\n')

if selection == '1':
   tree_EQ = ET.parse('Assignment_EQ_reduced.xml')
   tree_SSH = ET.parse('Assignment_SSH_reduced.xml')

if selection == '2':
    tree_EQ = ET.parse('MicroGridTestConfiguration_T1_BE_EQ_V2.xml')
    tree_SSH = ET.parse('MicroGridTestConfiguration_T1_BE_SSH_V2.xml')
    
if selection == '3':
    tree_EQ = ET.parse('MicroGridTestConfiguration_T1_NL_EQ_V2.xml')
    tree_SSH = ET.parse('MicroGridTestConfiguration_T1_NL_SSH_V2.xml')
    

#accessing the root of the tree
root_EQ = tree_EQ.getroot()
root_SSH = tree_SSH.getroot()

#check
# print(root_EQ)
# print(root_SSH)
#print (root_EQ.attrib)

# To make working with the file easier, it may be useful to store the
# namespace identifiers in strings and reuse when you search for tags
ns = {'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

# Initialise the lists and extract the information from the xml into these lists

BusbarSection_list = []
ACLine_Segment_list = []
Breaker_list = []
EnergyConsumer_list = []
GeneratingUnit_list = []
LinearShuntCompensator_list = []
VoltageLevel_list = []
PowerTransformer_list = []
RatioTapChanger_list = []
SynchronousMachine_list = []
RegulatingControl_list = []
BaseVoltage_list = []
node_list = []
ConnectivityNode_list = []
Terminal_list = []
name_list = []
ACLine_Segment_length = []
ACLine_Segment_name=[]
name_list2 = []
curvex=[]
curvey=[]
ConnectivityNode_list_id = []
Terminal_list_ConductingEquipment = []
Terminal_list_ConnectivityNode = []
TE_related_to_CE_list = []
TE_related_to_CN_list = []
number_list = []
CE_list = []
Terminal_list_ssh = []
EnergyConsumer_list_ssh = []
RatioTapChanger_list_ssh = []
Breaker_list_ssh = []
CN_attached_to_busbar_list = []
CN_name = []
CN_not = []
CN_not1 = []
everything_stack = []
type_stack_list = []
a = []

"""
class Conducting_equipment:
    def __init__(self, name,rdf_id,type,CE_type):
        self.name = name
        self.rdf_id = 'rdf_id'
        self.type = 'type'
        self.CE_type = 'CE_type'
        self.terminalList = [] 
"""

class ACLineSegment:
    def __init__(self, name):
        self.name = name
        self.Terminal_List = []
        self.Num_attachTerms = 0 
        self.Node_Type = 'CE'
        self.id = 'id'
        self.r = 'r'
        self.x = 'x'
        self.bch = 'bch'
        self.gch = 'gch'
        self.r0 = 'r0'
        self.x0 = 'x0'
        self.b0ch = 'b0ch'
        self.g0ch = 'g0ch'
        self.shortCircuitEndTemperature = 'shortCircuitEndTemperature'
        self.length = 'length'
        self.CE_type='ACLineSegment'

class BaseVoltage:
    def __init__(self, name):
        self.name= name
        self.id= 'id'
        self.nominalVoltage= 'nominalVoltage'       

class Breaker:
    def __init__(self, name):
        self.name = name
        self.Terminal_List = []
        self.Num_attachTerms = 0 
        self.Node_Type = 'CE'
        self.id = 'id'
        self.state = 'false'
        self.CE_type='Breaker'

class BusbarSection:
    def __init__(self,name):
        self.name = name
        self.id = 'id'
        self.Terminal_List = []
        self.Num_attachTerms = 0 
        self.Node_Type = 'CE '
        self.Busbar_Section_rdf_id = 'Busbar_Section_rdf_id'
        self.CE_type='BusbarSection'
        self.voltage=0
    
class ConnectivityNode:
    def __init__(self, name):
        self.name = name
        self.id = 'id'
        self.Node_Type = 'CN'
        self.container_id = 'container_id'
        self.Terminal_List = []
        self.Num_attachTerms=0
        self.voltage=0
        self.CE_type = 'not CE'
        
class CurveData:
    def __init__(self, name):
        self.name = name
        self.id = 'id'
        self.x = 'x'
        self.y1= 'y1'
        self.y2= 'y2'
        
    
class EnergyConsumer:
    def __init__(self, name):
        self.name = name
        self.Terminal_List = []
        self.num_attachTerms = 0 
        self.Node_Type = 'CE'
        self.id = 'id'
        self.aggregate = 'aggregate'
        self.CE_type='load'
        self.p=0
        self.q=0

class EnergySource:
    def __init__(self, name):
        self.name = name
        self.Terminal_List = []
        self.num_attachTerms = 0 
        self.Node_Type = 'CE'
        self.id = 'id'
        self.aggregate = 'aggregate'
        self.CE_type='Sgen'
        self.p=0
        self.q=0
        self.r=0
        self.x=0
        
class GeneratingUnit:
    def __init__(self, name):
        self.name = name
        self.id = 'id'
        self.initialP = 'initialP'
        self.nominalP = 'nominalP'
        self.maxOperatingP = 'maxOperatingP'
        self.minOperatingP = 'minOperatingP'        
        self.Terminal_List = []
        self.Node_Type = 'CE'
        self.CE_type='Generator'
        self.Num_attachTerms=0
        
class LinearShuntCompensator:
    def __init__(self,name):
        self.name = name
        self.id = 'id'
        self.nomU= 0
        self.Terminal_List = []
        self.Node_Type='CE'
        self.CE_type='Compensator'
        self.Num_attachTerms=0
        self.b=0
        self.q=0
    
class PowerTransformer:
    def __init__(self, name):
        self.name = name
        self.Terminal_list = []
        self.Num_attachTerms = 0 
        self.type = 'CE'
        self.rdf_id = 'id'
        self.CE_type='Transformer'
    
class RatioTapChanger:
    def __init__(self,name):
        self.name = name
        self.id = 'id'
        self.neutralU = 'neutralU'
        self.lowStep = 'lowStep'
        self.highStep = 'highStep'
        self.neutralStep = 'neutralStep'
        self.normalStep = 'normalStep'
        self.stepVoltageIncrement = 'stepVoltageIncrement'
        self.Node_Type='CE'
        self.CE_type='TapChanger'
        self.Terminal_List=[]
        self.Num_attachTerms=0    
        
class RegulatingControl:
    def __init__(self,name):
        self.name = name
        self.id = 'id'
class SynchronousMachine:
    def __init__(self, name):
        self.name = name
        self.id = 'id'
        self.GeneratingUnit ='GeneratingUnit'
        self.p_mw= 'p_mw'
        self.ratedU = 'ratedU'
        self.ratedS = 'ratedS'
        self.ratedPowerFactor = 'ratedPowerFactor'
        self.Terminal_List = []
        self.Node_Type = 'CE'
        self.Num_attachTerms=0
        self.CE_type='SynchronousMachine'

class Terminal:
    def __init__(self, name):
        self.name = name
        self.id = 'id'
        self.type = 'TE'
        self.ConnectivityNode = 'ConnectivityNode'
        self.ConductingEquipment = 'ConductingEquipment'
        self.Terminal_List = []
    

class VoltageLevel:
    def __init__(self, name):
        self.name= name
        self.id = 'id'
        self.lowVoltageLimit= 'lowVoltageLimit'
        self.highVoltageLimit= 'highVoltageLimit'


#parsing the information from EQ file into the respective classes
for equipment in root_EQ:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}", "")
        name_list.append(name)
        if name == 'BusbarSection':
            Busbar_Section = BusbarSection(equipment)
            Busbar_Section.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Busbar_Section.id = equipment.attrib.get(ns['rdf']+'ID')
            Busbar_Section.Node_Type = 'CE'
            Busbar_Section.EquipmentContainer = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            BusbarSection_list.append(Busbar_Section)
            CE_list.append(Busbar_Section)
            Busbar_Section.CE_type = 'BusbarSection'

        elif name == 'ACLineSegment':
            ACLine_Segment = ACLineSegment(equipment)
            ACLine_Segment.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            ACLine_Segment.Node_Type = 'CE'
            ACLine_Segment.id = equipment.attrib.get(ns['rdf']+'ID')
            ACLine_Segment.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            ACLine_Segment.r = equipment.find('cim:ACLineSegment.r', ns).text
            ACLine_Segment.x = equipment.find('cim:ACLineSegment.x', ns).text
            ACLine_Segment.bch = equipment.find(
                'cim:ACLineSegment.bch', ns).text
            ACLine_Segment.gch = equipment.find(
                'cim:ACLineSegment.gch', ns).text
            ACLine_Segment.r0 = equipment.find('cim:ACLineSegment.r0', ns).text
            ACLine_Segment.x0 = equipment.find('cim:ACLineSegment.x0', ns).text
            ACLine_Segment.b0ch = equipment.find(
                'cim:ACLineSegment.b0ch', ns).text
            ACLine_Segment.g0ch = equipment.find(
                'cim:ACLineSegment.g0ch', ns).text
            ACLine_Segment.shortCircuitEndTemperature = equipment.find(
                'cim:ACLineSegment.shortCircuitEndTemperature', ns).text
            ACLine_Segment.length = equipment.find(
                'cim:Conductor.length', ns).text
            ACLine_Segment.CE_type = 'ACLineSegment'
            ACLine_Segment_list.append(ACLine_Segment)
            ACLine_Segment_name.append(ACLine_Segment.name)
            ACLine_Segment_length.append(ACLine_Segment.length)
            CE_list.append(ACLine_Segment)

        elif name == 'Breaker':
            Brea_ker = Breaker(equipment)
            Brea_ker.id = equipment.attrib.get(ns['rdf']+'ID')
            Brea_ker.Node_Type = 'CE'
            Brea_ker.container_id = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Breaker_list.append(Brea_ker)
            CE_list.append(Brea_ker)

        elif name == 'EnergyConsumer':
            Energy_Consumer = EnergyConsumer(equipment)
            Energy_Consumer.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Energy_Consumer.id = equipment.attrib.get(ns['rdf']+'ID')
            Energy_Consumer.aggregate = equipment.find(
                'cim:Equipment.aggregate', ns).text
            Energy_Consumer.container_id = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Energy_Consumer.Node_Type = 'CE '
            EnergyConsumer_list.append(Energy_Consumer)
            CE_list.append(Energy_Consumer)
           
            
        elif name == 'EnergySource':
            Energy_S = EnergySource(equipment)
            Energy_S.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Energy_S.id = equipment.attrib.get(ns['rdf']+'ID')
            Energy_S.aggregate = equipment.find(
                'cim:Equipment.aggregate', ns).text
            Energy_S.container_id = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Energy_S.Node_Type = 'CE '
            Energy_S.r = equipment.find('cim:EnergySource.r', ns).text
            Energy_S.x = equipment.find('cim:EnergySource.x', ns).text
            EnergyConsumer_list.append(Energy_Consumer)
            CE_list.append(Energy_S)
            

        elif name == 'GeneratingUnit':
            Generating_Unit = GeneratingUnit(equipment)
            Generating_Unit.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Generating_Unit.id = equipment.attrib.get(ns['rdf']+'ID')
            Generating_Unit.initialP = equipment.find(
                'cim:GeneratingUnit.initialP', ns).text
            Generating_Unit.nominalP = equipment.find(
                'cim:GeneratingUnit.nominalP', ns).text
            Generating_Unit.maxOperatingP = equipment.find(
                'cim:GeneratingUnit.maxOperatingP', ns).text
            Generating_Unit.minOperatingP = equipment.find(
                'cim:GeneratingUnit.minOperatingP', ns).text
            Generating_Unit.container_id = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Generating_Unit.Node_Type = 'CE '
            GeneratingUnit_list.append(Generating_Unit)

        elif name == 'LinearShuntCompensator':
            LinearShunt_Compensator = LinearShuntCompensator(equipment)
            LinearShunt_Compensator.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            LinearShunt_Compensator.id = equipment.attrib.get(ns['rdf']+'ID')
            LinearShunt_Compensator.container_id = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            LinearShunt_Compensator.RegulatingControl = equipment.find(
                'cim:RegulatingCondEq.RegulatingControl', ns).attrib.get(ns['rdf']+'resource')
            LinearShunt_Compensator.nomU = float(equipment.find(
                'cim:ShuntCompensator.nomU', ns).text)
            LinearShunt_Compensator.b = float(equipment.find(
                'cim:LinearShuntCompensator.bPerSection', ns).text)
            LinearShunt_Compensator.q = float(
                LinearShunt_Compensator.b*LinearShunt_Compensator.nomU*LinearShunt_Compensator.nomU)
            LinearShunt_Compensator.Node_Type = 'CE '
            LinearShuntCompensator_list.append(LinearShunt_Compensator)
            CE_list.append(LinearShunt_Compensator)

        elif name == 'VoltageLevel':
            Voltage_Level = VoltageLevel(equipment)
            Voltage_Level.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Voltage_Level.id = equipment.attrib.get(ns['rdf']+'ID')
            Voltage_Level.lowVoltageLimit = equipment.find(
                'cim:VoltageLevel.lowVoltageLimit', ns).text
            Voltage_Level.highVoltageLimit = equipment.find(
                'cim:VoltageLevel.highVoltageLimit', ns).text
            Voltage_Level.Substation = equipment.find(
                'cim:VoltageLevel.Substation', ns).attrib.get(ns['rdf']+'resource')
            Voltage_Level.BaseVoltage = equipment.find(
                'cim:VoltageLevel.BaseVoltage', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            VoltageLevel_list.append(Voltage_Level)
            
        elif name== 'CurveData':
            Curve_Data=CurveData(equipment)
            Curve_Data.id=equipment.attrib.get(ns['rdf']+'ID')
            Curve_Data.x=float(equipment.find(
                'cim:CurveData.xvalue', ns).text)
            Curve_Data.y1=float(equipment.find(
                'cim:CurveData.y1value', ns).text)
            Curve_Data.y2=float(equipment.find(
                'cim:CurveData.y2value', ns).text)
            curvex.append(Curve_Data.x)
            curvex.append(Curve_Data.x)
            curvey.append(Curve_Data.y1)
            curvey.append(Curve_Data.y2)

        elif name == 'PowerTransformer':
            Power_Transformer = PowerTransformer(equipment)
            Power_Transformer.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Power_Transformer.id = equipment.attrib.get(ns['rdf']+'ID')
            Power_Transformer.Node_Type = 'CE'
            Power_Transformer.EquipmentContainer = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            PowerTransformer_list.append(Power_Transformer)
            CE_list.append(Power_Transformer)

        elif name == 'RatioTapChanger':
            Ratio_TapChanger = RatioTapChanger(equipment)
            Ratio_TapChanger.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Ratio_TapChanger.id = equipment.attrib.get(ns['rdf']+'ID')
            Ratio_TapChanger.Node_Type = 'CE'
            Ratio_TapChanger.TapChangerControl = equipment.find(
                'cim:TapChanger.TapChangerControl', ns).attrib.get(ns['rdf']+'resource')
            Ratio_TapChanger.neutralU = equipment.find(
                'cim:TapChanger.neutralU', ns).text
            Ratio_TapChanger.lowStep = equipment.find(
                'cim:TapChanger.lowStep', ns).text
            Ratio_TapChanger.highStep = equipment.find(
                'cim:TapChanger.highStep', ns).text
            Ratio_TapChanger.neutralStep = equipment.find(
                'cim:TapChanger.neutralStep', ns).text
            Ratio_TapChanger.normalStep = equipment.find(
                'cim:TapChanger.normalStep', ns).text
            Ratio_TapChanger.stepVoltageIncrement = equipment.find(
                'cim:RatioTapChanger.stepVoltageIncrement', ns).text
            RatioTapChanger_list.append(Ratio_TapChanger)

        elif name == 'SynchronousMachine':
            Synchronous_Machine = SynchronousMachine(equipment)
            Synchronous_Machine.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Synchronous_Machine.id = equipment.attrib.get(ns['rdf']+'ID')
            SynchronousMachine_list.append(Synchronous_Machine)
            Synchronous_Machine.EquipmentContainer = equipment.find(
                'cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Synchronous_Machine.GeneratingUnit = equipment.find(
                'cim:RotatingMachine.GeneratingUnit', ns).attrib.get(ns['rdf']+'resource')
            Synchronous_Machine.ratedU = equipment.find(
                'cim:RotatingMachine.ratedU', ns).text
            Synchronous_Machine.ratedS = equipment.find(
                'cim:RotatingMachine.ratedS', ns).text
            Synchronous_Machine.ratedPowerFactor = equipment.find(
                'cim:RotatingMachine.ratedPowerFactor', ns).text
            Synchronous_Machine.Node_Type = 'CE'
            CE_list.append(Synchronous_Machine)

        elif name == 'RegulatingControl':
            Regulating_Control = RegulatingControl(equipment)
            Regulating_Control.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Regulating_Control.id = equipment.attrib.get(ns['rdf']+'ID')
            Ratio_TapChanger.Node_Type = 'CE'
            RegulatingControl_list.append(Regulating_Control)
            Regulating_Control.Terminal = equipment.find(
                'cim:RegulatingControl.Terminal', ns).attrib.get(ns['rdf']+'resource')

        elif name == 'BaseVoltage':
            Base_Voltage = BaseVoltage(equipment)
            Base_Voltage.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Base_Voltage.id = equipment.attrib.get(ns['rdf']+'ID')
            Base_Voltage.Node_Type = 'CE'
            BaseVoltage_list.append(Base_Voltage)
            Base_Voltage.nominalVoltage = equipment.find(
                'cim:BaseVoltage.nominalVoltage', ns).text

        elif name == 'ConnectivityNode':
            Connectivity_Node = ConnectivityNode(equipment)
            Connectivity_Node.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            Connectivity_Node.id = equipment.attrib.get(ns['rdf']+'ID')
            Connectivity_Node.container_id = equipment.find(
                'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            Connectivity_Node.Node_Type = 'CN'
            ConnectivityNode_list.append(Connectivity_Node)
            ConnectivityNode_list_id.append(Connectivity_Node.id)

        elif name == 'Terminal':
            T_erminal = Terminal(equipment)
            T_erminal.name = equipment.find(
                'cim:IdentifiedObject.name', ns).text
            T_erminal.id = equipment.attrib.get(ns['rdf']+'ID')
            T_erminal.ConductingEquipment = equipment.find(
                'cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            T_erminal.ConnectivityNode = equipment.find(
                'cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf']+'resource').replace('#', '')
            T_erminal.Node_Type = 'TE'
            # we need to keep track of all the attached terminals that haven’t been encountered (traversed) before.
            T_erminal.traversal_flag = 0
            # This is realized by adding an attribute called a ‘traversal flag’ to every terminal in the system with the flag value initialized at zero.
            Terminal_list.append(T_erminal)
            Terminal_list_ConductingEquipment.append(
                T_erminal.ConductingEquipment.replace('#', ''))
            Terminal_list_ConnectivityNode.append(
                T_erminal.ConnectivityNode.replace('#', ''))

for equipment in root_EQ:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}", "")
        if name == 'BusbarSection':
            for Busbar_Section in BusbarSection_list:
                for Voltage_Level in VoltageLevel_list:
                    if Busbar_Section.EquipmentContainer == Voltage_Level.id:
                        for Base_Voltage in BaseVoltage_list:
                            if Voltage_Level.BaseVoltage == Base_Voltage.id:
                                Busbar_Section.voltage = float(
                                    Base_Voltage.nominalVoltage)
        elif name == 'ConnectivityNode':
            for Connectivity_Node in ConnectivityNode_list:
                for Voltage_Level in VoltageLevel_list:
                    if Connectivity_Node.container_id == Voltage_Level.id:
                        for Base_Voltage in BaseVoltage_list:
                            if Voltage_Level.BaseVoltage == Base_Voltage.id:
                                Connectivity_Node.voltage = float(
                                    Base_Voltage.nominalVoltage)


#To check        
# print(Power_Transformer.name)
# print(Busbar_Section.voltage)
# print(ConnectivityNode_list_id)
# print(Terminal_list_ConductingEquipment)
# print(Terminal_list_ConnectivityNode)

#parsing the information from SSH file into the respective classes

for equipment in root_SSH:
    if ns['cim'] in equipment.tag:
        name = equipment.tag.replace("{"+ns['cim']+"}", "")
        name_list2.append(name)
        if name == 'Terminal':
            T_erminal = Terminal(equipment)
            T_erminal.id = equipment.attrib.get(ns['rdf']+'ID')
            Terminal_list_ssh.append(T_erminal)

        elif name == 'EnergyConsumer':
            Energy_Consumer = EnergyConsumer(equipment)
            Energy_Consumer.id = equipment.attrib.get(ns['rdf']+'ID')
            Energy_Consumer.p = equipment.find('cim:EnergyConsumer.p', ns).text
            Energy_Consumer.q = equipment.find('cim:EnergyConsumer.q', ns).text
            EnergyConsumer_list_ssh.append(Energy_Consumer.p)
        elif name == 'RatioTapChanger':
            Ratio_TapChanger = RatioTapChanger(equipment)
            Ratio_TapChanger.id = equipment.attrib.get(ns['rdf']+'ID')
            Ratio_TapChanger.step = equipment.find(
                'cim:TapChanger.step', ns).text
            Ratio_TapChanger.controlEnabled = equipment.find(
                'cim:TapChanger.controlEnabled', ns).text
            RatioTapChanger_list_ssh.append(Ratio_TapChanger)
        elif name == 'Breaker':
            B_reaker = Breaker(equipment)
            B_reaker.id = equipment.attrib.get(ns['rdf']+'ID')
            B_reaker.Switch = equipment.find('cim:Switch.open', ns).text
            Breaker_list_ssh.append(Breaker)
        elif name == 'RegulatingControl':
            Regulating_Control = RegulatingControl(equipment)
            Regulating_Control.id = equipment.attrib.get(ns['rdf']+'ID')
            Regulating_Control.targetValue = equipment.find(
                'cim:RegulatingControl.targetValue', ns).text
        elif name == 'EnergyConsumer':
            Energy_Consumer.p = equipment.find(
                        'cim:EnergyConsumer.activePower', ns).text
            Energy_Consumer.q = equipment.find(
                        'cim:EnergyConsumer.reactivePower', ns).text


"""
This part defines four functions that search through lists of objects, looking for specific objects and returning lists of related objects.
Overall, these functions appear to be designed to help with searching and organizing objects in a power system model.
"""

# try to find the terminal which are connect to CN and CE separately
def find_TE_related_to_CN(CN):
    for TE in Terminal_list:
        if CN.id == TE.ConnectivityNode:
            return(TE)
for Connectivity_Node in ConnectivityNode_list:
    TE_related_to_CN_list.append(find_TE_related_to_CN(Connectivity_Node))
#print(TE_related_to_CN_list)
def find_TE_related_to_CN_list(CN):
    TE_related_to_CN_list1 = []
    for TE in Terminal_list:
        if TE.ConnectivityNode == CN.id:
            TE_related_to_CN_list1.append(TE)
    return(TE_related_to_CN_list1)
    #print(TE_related_to_CN_list1)

def find_TE_related_to_CE(CE):
    for TE in Terminal_list:
        if CE.id == TE.ConductingEquipment:
            return(TE)
for Node in CE_list:
    # generator and tapchanger are not CE
    TE_related_to_CE_list.append(find_TE_related_to_CE(Node))
def find_TE_related_to_CE_list(CE):
    TE_related_to_CE_list1 = []
    for TE in Terminal_list:
        if CE.id == TE.ConductingEquipment:
            TE_related_to_CE_list1.append(TE)
    return(TE_related_to_CE_list1)

"""
The function (find_next_node) for movement from one node to the other is implemented via three traversal node objects, representing the previous (prev_node),
current (curr_node) and next node (next_node) to be traversed respectively. Because of the way in which the network is characterized in CIM, it can be easily seen that during traversal,
when the current traversed node (curr_node) is conducting equipment (CE) or a connectivity node (CN), the next node will always be a terminal (Te). When the current traversed
node is a terminal, then the node to be traversed next would be a CE, if the previous node was a CN and vice-versa.

Overall, this function appears to be designed to help with traversing a power system model by determining which object to move to next based on the 
current and previous objects in the sequence.
"""

def find_next_node(prev_node, curr_node):
    if curr_node.Node_Type == 'CN':
        return(random.sample(TE_related_to_CN_list, 1))
    elif curr_node.Node_Type == 'CE':
        return(random.sample(TE_related_to_CE_list, 1))
    elif curr_node.Node_Type == 'TE' and prev_node.Node_Type == 'CN':
        for Node in CE_list:  
            if curr_node.ConductingEquipment == Node.id:
                return(Node)
    elif curr_node.Node_Type == 'TE' and prev_node.Node_Type == 'CE':
        for Node in ConnectivityNode_list:
            if curr_node.ConnectivityNode == Node.id:
                return(Node)


# Num_attachTerms of connectivity node
def Num_attachTerms_of_CN(CN):
    for TE in TE_related_to_CN_list:
        if TE.ConnectivityNode == CN.id:
            number_list.append(TE)
            return(len(number_list))
        
# Num_attachTerms of ConductingEquipment
def Num_attachTerms_of_CE(CE):
    for TE in TE_related_to_CE_list:
        try:
            if TE.ConductingEquipment == CE.id:
                number_list.append(TE)
                return(len(number_list))
        except:
            pass

# find CN attach to bus
for CN in ConnectivityNode_list:
    for TE in find_TE_related_to_CN_list(CN):
        next_node = find_next_node(CN, TE)
        try:
            if next_node.CE_type == 'BusbarSection':
                CN_attached_to_busbar_list.append(CN)
                CN_name.append(CN.name)
        except:
            pass
print(CN_attached_to_busbar_list)
print(CN_name)
"""
app=[]
for cn in CN_attached_to_busbar_list:
    app.append(cn.id)
print(app)

"""


for CN in ConnectivityNode_list:
    if CN not in CN_attached_to_busbar_list:
        CN_not1.append(CN.name)
        CN_not.append(CN)


print(CN_not)
print("-----------------------------------------")
print(CN_not1)
print("-----------------------------------------")



for CN in ConnectivityNode_list:  # the current nodeis a CN
    if Num_attachTerms_of_CN(CN) > 0:
        # find an untraversed terminal from the list of attached terminals
        for TE in find_TE_related_to_CN_list(CN):
            if TE.traversal_flag == 0:  # untraversed terminal
                curr_node = CN
                CN.Num_attachTerms -= 1  # Mark the TE
                TE.traversal_flag = 1
                prev_node = curr_node
                curr_node = TE  # update the current node as nextnode
                next_node = find_next_node(
                    prev_node, curr_node)  # step 2 in paper
                CN_CE_stack = [CN]#store the CN of one side of the CE
                CN_CE_stack.append(next_node)#store CE
                CE = next_node  # current node is CE
                # there is an  terminal,except the TE before CE
                try:
                    if Num_attachTerms_of_CE(CE) > 1:
                        for TE in find_TE_related_to_CE_list(CE):
                            if TE.traversal_flag == 0:  # If there is an untraversed terminal
                                TE.traversal_flag = 1
                                # update the current node as nextnode
                                next_node = find_next_node(CE, TE)
                                # If there is no untraversed terminal remaining
                                CN_CE_stack.append(next_node)#store the CN on the other side of CE
                                # mark the next node as the CN on top of CN stack
                except:
                    pass
                
                if CN_CE_stack not in everything_stack:  # get the CE and the CN next to it to a big list
                    everything_stack.append(CN_CE_stack)
#During the loop, as CNs and CEs are first stored in a list which is later credited to another list.
print(everything_stack)
print("-----------------------------------------")

#tocheck
# print(CN_CE_stack)
#The final information obtained is an everything_stack consisting of each CE and the CN next to it in the items.


# create component for panda power
net = pp.create_empty_network()

# create busbar
# In order to make the drawing of the topology beautiful,
# the CN which is not directly connected to the busbar is also counted as
# a kind of busbar here, in order to ensure the continuity of the drawing

for Busbar_Section in BusbarSection_list:
    a.append(pp.create_bus(net, name=Busbar_Section.name,
             vn_kv=Busbar_Section.voltage, type="b"))
# print(a)

for CN in CN_not:
    pp.create_bus(net, name=CN.name, vn_kv=CN.voltage, type="n")
print(net.bus)
print("-----------------------------------------")

# By reading the ids in the xml file, after removing the CNs directly
# connected to the busbar, the remaining CNs can be determined by
# whether they are connected to the switch or not

# Here we can see that there are many items in the everything_stack, and in each item is the CN and the CE connected to it.
# and generally the first and last one is the CN. so we create the following function


def find_busbar_for_CN(CN):
    lista = find_TE_related_to_CN_list(CN)
    for TE in lista:
        bus = find_next_node(CN, TE)
        try:
            if bus.CE_type == 'BusbarSection':
                return(pp.get_element_index(net, "bus", bus.name))
            if bus.CE_type == 'Breaker':
                return(pp.get_element_index(net, "bus", CN.name))
        except:
            pass
#Once the CE device has been found, the CN of the CE can be locked and the information of the corresponding busbar can be 
#ound according to the CN to obtain the information needed by pp

# creating LIne segments
for item in everything_stack:
    for lines in item:
        try:
            if lines.CE_type == 'ACLineSegment':
                # pp.create_line(net, find_busbar_for_CN(item[0]), find_busbar_for_CN(
                #     item[-1]), length_km=(lines.length), std_type="N2XS(FL)2Y 1x300 RM/35 64/110 kV",  name=lines.name)
                pp.create_line_from_parameters(net, find_busbar_for_CN(item[0]), find_busbar_for_CN(item[-1]), length_km=(lines.length), 
                                               r_ohm_per_km=(lines.r), x_ohm_per_km=(lines.x), c_nf_per_km=(lines.bch), 
                                               max_i_ka=lines.shortCircuitEndTemperature, g_us_per_km=(lines.gch), r0_ohm_per_km=(lines.r0), 
                                               x0_ohm_per_km=(lines.x0), c0_nf_per_km=(lines.b0ch), g0_us_per_km=(lines.g0ch),name=lines.name)
        except:
            pass
print(net.line)
print("-----------------------------------------")

# creating breakers
for item in everything_stack:
    for breaker in item:
        try:
            if breaker.CE_type == 'Breaker':
                if breaker.state == 'false':
                    pp.create_switch(net, find_busbar_for_CN(item[0]), find_busbar_for_CN(
                        item[-1]), et="b", type="CB", closed=True)
                if breaker.state == 'ture':
                    pp.create_switch(net, find_busbar_for_CN(item[0]), find_busbar_for_CN(
                        item[-1]), et="b", type="CB", closed=False)
        except:
            pass
net.switch
print(net.switch)
print("-----------------------------------------")

# creating load
for item in everything_stack:
    for load in item:
        try:
            if load.CE_type == 'load':
                pp.create_load(net, find_busbar_for_CN(
                    item[0]), p_mw=(load.p), q_mvar=(load.q), name=load.name)
        except:
            pass
print(net.load)
print("-----------------------------------------")

# creating generators

for item in everything_stack:
    for generator in item:
        try:
            if generator.CE_type == 'SynchronousMachine':
                pp.create_gen(net, find_busbar_for_CN(item[0]),p_mw=(float(generator.ratedS)*float(generator.ratedPowerFactor)), 
                              sn_kva=generator.ratedS, name=generator.name,  vn_kv=generator.ratedU,cos_phi=generator.ratedPowerFactor, in_service=True)
      
            elif generator.CE_type == 'Generator':
                pp.create_gen(net, find_busbar_for_CN(item[0]),p_mw=generator.nominalP,max_p_kw=generator.maxOperatingP,
                              min_p_kw=generator.minOperatingP, name=generator.name)
        except:
            pass


print(net.gen)
print("-----------------------------------------")


#creating Static generators
for item in everything_stack:
    for Sgen in item:
        try:
            if load.CE_type == 'Sgen':
                pp.create_sgen(net, find_busbar_for_CN(
                    item[0]), p_kw=(Sgen.p), q_kvar=(Sgen.q), name=Sgen.name)
        except:
            pass
print(net.sgen)
print("-----------------------------------------")


# create Compensator
for item in everything_stack:
    for ShuntCompensator in item:
        try:
            if ShuntCompensator.CE_type == 'Compensator':
                pp.create_shunt(net, find_busbar_for_CN(
                    item[0]), q_mvar=0.01*ShuntCompensator.q, p_mw=0, name=ShuntCompensator.name)
        except:
            pass        

print(net.shunt)
print("-----------------------------------------")

# create transformer
# For transformers the high and low voltage busbars need to be determined
for item in everything_stack:
    for transformer in item:
        try:
            if transformer.CE_type == 'Transformer':
                if item[0].voltage > item[2].voltage:
                    busbar_hv = find_busbar_for_CN(item[0])
                    busbar_lv = find_busbar_for_CN(item[2])
                else:
                    busbar_hv = find_busbar_for_CN(item[2])
                    busbar_lv = find_busbar_for_CN(item[0])
                pp.create_transformer(
                    net, busbar_hv, busbar_lv, name=transformer.name, std_type="25 MVA 110/20 kV")
        except:
            pass
       


print(net)
print("-----------------------------------------")

plt.scatter(curvex, curvey)
plt.title("Reactive Capability Curve")
plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
plt.xlabel("Real Power Output(MVAR)")
plt.ylabel("Reactive Power (MW)")
plt.show()


pp.plotting.simple_plot(net)
html_output(net, 'power system model.html')

"""
References:
Website: https://www.pandapower.org/
Getting Started guide: https://www.pandapower.org/start/
API documentation: https://pandapower.readthedocs.io/en/v2.2.2/
ref paper: Methods of Converting CIM Power System Models into Bus-Branch Formats Utilizing
Topology Processing Algorithms and Minimal Schema Modifications to IEC 61968/70
ref paper:An efficient method of extracting network information from CIM asset model
(See discussions, stats, and author profiles for this publication at: https://www.researchgate.net/publication/307888085)
ref paper:An Introduction to IEC 61970-301 & 61968-11: The Common Information Model

"""



