class CMSO_mod():
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/"

class PODO_mod():
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/podo/"

#--------------------------------------------------------------------------------------------------------#

class ComputationalSample(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/ComputationalSample"
class AtomicScaleSample(ComputationalSample):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/AtomicScaleSample"

#--------------------------------------------------------------------------------------------------------#
    
class SimulationCell(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/SimulationCell"

#--------------------------------------------------------------------------------------------------------#
    
class UnitCell(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/UnitCell"

#--------------------------------------------------------------------------------------------------------#
    
class LatticeParameter(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/LatticeParameter"

#--------------------------------------------------------------------------------------------------------#
    
class SpaceGroup(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/SpaceGroup"

#--------------------------------------------------------------------------------------------------------#
    
class BravaisLattice(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/BravaisLattice"

#--------------------------------------------------------------------------------------------------------#
    
class ChemicalComposition(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/ChemicalComposition"

#--------------------------------------------------------------------------------------------------------#
    
class Vector(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Vector"
class LatticeVector(Vector):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/LatticeVector"
class SimulationCellVector(Vector):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/SimulationCellVector"

#--------------------------------------------------------------------------------------------------------#
    
class Angle(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Angle"
class LatticeAngle(Angle):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/LatticeAngle"
class SimulationCellAngle(Angle):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/SimulationCellAngle"

#--------------------------------------------------------------------------------------------------------#
    
class Volume(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Volume"
class LatticeVolume(Volume):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/LatticeVolume"
class SimulationCellVolume(Volume):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/SimulationCellVolume"

#--------------------------------------------------------------------------------------------------------#
    
class ChemicalSpecies(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/ChemicalSpecies"
class Atom(ChemicalSpecies):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Atom"
class Molecule(ChemicalSpecies):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Molecule"

#--------------------------------------------------------------------------------------------------------#

class CrystalDefect(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/CrystalDefect"
class PointDefect(CrystalDefect, PODO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/podo/PointDefect"
class Vacancy(PointDefect):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/podo/Vacancy"
class Impurity(PointDefect):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/podo/Impurity"
class SubstitutionalImpurity(PointDefect):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/podo/SubstitutionalImpurity"

#--------------------------------------------------------------------------------------------------------#

class Position(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Position"

#--------------------------------------------------------------------------------------------------------#

class Length(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Length"

#--------------------------------------------------------------------------------------------------------#

class Unit(CMSO_mod):
    @property
    def IRI(self):
        return "http://qudt.org/schema/qudt/Unit"

#--------------------------------------------------------------------------------------------------------#

class Path(CMSO_mod):
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/cmso/Path"

#--------------------------------------------------------------------------------------------------------#

class Value():
    @property
    def IRI(self):
        return "https://www.w3.org/TR/rdf12-schema/#ch_value"

#--------------------------------------------------------------------------------------------------------#

class Label():
    @property
    def IRI(self):
        return "http://www.w3.org/2000/01/rdf-schema#label"

#--------------------------------------------------------------------------------------------------------#

class ProcessMetadata():
    @property
    def IRI(self):
        return "http://id-from-pmdco-pending/ProcessMetadata"

#--------------------------------------------------------------------------------------------------------#

class Pyiron():
    @property
    def IRI(self):
        return "http://demo.fiz-karlsruhe.de/matwerk/E457491"

#--------------------------------------------------------------------------------------------------------#

class AnalysingProcess():
    @property
    def IRI(self):
        return "https://w3id.org/pmd/co/AnalysingProcess"

#--------------------------------------------------------------------------------------------------------#

class Software():
    @property
    def IRI(self):
        return "http://www.ebi.ac.uk/swo/SWO_0000001"

#--------------------------------------------------------------------------------------------------------#

class InputParameter():
    @property
    def IRI(self):
        return "http://purls.helmholtz-metadaten.de/asmo/InputParameter"

#--------------------------------------------------------------------------------------------------------#

class PMDCO_mod():
    @property
    def IRI(self):
        return "https://w3id.org/pmd/co/"


class IAO():
    @property
    def IRI(self):
        return "http://purl.obolibrary.org/obo/iao.owl"

#--------------------------------------------------------------------------------------------------------#

class InformationContentEntity(IAO):
    @property
    def IRI(self):
        return "http://purl.obolibrary.org/obo/IAO_0000030"
class DirectiveInformationEntity(InformationContentEntity):
    @property
    def IRI(self):
        return "http://purl.obolibrary.org/obo/IAO_0000033"    
class PlanSpecification(DirectiveInformationEntity):
    @property
    def IRI(self):
        return "http://purl.obolibrary.org/obo/IAO_0000104"
class Algorithm(PlanSpecification):
    @property
    def IRI(self):
        return "http://purl.obolibrary.org/obo/IAO_0000064"
class SpaceGroupAnalysingAlgorithm(PMDCO_mod, Algorithm):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/SpaceGroupAnalysingAlgorithm"
class Software(PlanSpecification):
    @property
    def IRI(self):
        return "http://purl.obolibrary.org/obo/IAO_0000010"

#--------------------------------------------------------------------------------------------------------#

class ComputerWorkflow(InformationContentEntity, PMDCO_mod):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/ComputerWorkflow"

#--------------------------------------------------------------------------------------------------------#

class NodeClass(InformationContentEntity, PMDCO_mod):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/NodeClass"

#--------------------------------------------------------------------------------------------------------#

class Node(InformationContentEntity, PMDCO_mod):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/Node"      
class StructureCreationNode(Node):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/StructureCreationNode"
class StructureManipulationNode(Node):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/StructureManipulationNode"

#--------------------------------------------------------------------------------------------------------#

class Handle(InformationContentEntity, PMDCO_mod):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/Handle" 
class SourceHandle(Handle):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/SourceHandle"
class TargetHandle(Handle):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/TargetHandle"

#--------------------------------------------------------------------------------------------------------#

class WorkflowObject(InformationContentEntity, PMDCO_mod):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/WorkflowObject"
class InputObject(WorkflowObject):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/InputObject"
class OutputObject(WorkflowObject):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/OutputObject"

#--------------------------------------------------------------------------------------------------------#

class Edge(InformationContentEntity, PMDCO_mod):
    @property
    def IRI(self):
        return "https://id-from-pmdco-pending/Edge"