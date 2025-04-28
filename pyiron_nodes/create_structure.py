from pyiron_workflow import Workflow, as_function_node
from dataclasses import dataclass
from semantikon.typing import u
from semantikon.converter import semantikon_class
from semantics import onto
from typing import Optional
import numpy as np
from ase import Atoms

@semantikon_class
@u(label="atomistic_sample", uri=onto.AtomicScaleSample)
@dataclass
class AtomisticSample:
    class_object: u(Atoms, uri=onto.InformationContentEntity) = None
    simulation_cell: u(object, label="simulation_cell", uri=onto.SimulationCell) = None
    chemical_species: u(object, label="chemical_species", uri=onto.ChemicalSpecies) = None
    unit_cell: u(list, label="unit_cell", uri=onto.UnitCell) = None
    crystal_defect: u(list, label="crystal_defect", uri=onto.CrystalDefect) = None
    analysis: u(list, label="analysis", uri=onto.AnalysingProcess) = None
    provenance_objects: u(list, uri=onto.InformationContentEntity) = None

@dataclass
class SampleSimulationCell:
    simulation_cell_lengths: u(np.ndarray, units="ANGSTROM", label="simulation_cell_lengths", uri=onto.Length) = None
    simulation_cell_vectors: u(np.ndarray, units="ANGSTROM", label="simulation_cell_vectors", uri=onto.SimulationCellVector) = None
    simulation_cell_angles: u(np.ndarray, units="DEGREES", label="simulation_cell_angles", uri=onto.SimulationCellAngle) = None
    simulation_cell_volume: u(float, units="ANGSTROM3", label="simulation_cell_volume", uri=onto.SimulationCellVolume) = None

@dataclass
class SampleChemicalSpecies:
    atoms: u(list|str, label="atoms", uri=onto.Atom) = None
    molecules: u(dict, label="molecules", uri=onto.Molecule) = None

@dataclass
class SampleUnitCell:
        lattice_parameter_a: u(Optional[int|float], units="ANGSTROM", label="lattice_parameter_a", uri=onto.LatticeParameter) = None
        lattice_parameter_b: u(Optional[int|float], units="ANGSTROM", label="lattice_parameter_b", uri=onto.LatticeParameter) = None
        lattice_parameter_c: u(Optional[int|float], units="ANGSTROM", label="lattice_parameter_c", uri=onto.LatticeParameter) = None
        lattice_angle_alpha: u(Optional[int|float], units="DEGREES", label="lattice_angle_alpha", uri=onto.LatticeAngle) = None
        lattice_angle_beta: u(Optional[int|float], units="DEGREES", label="lattice_angle_beta", uri=onto.LatticeAngle) = None
        lattice_angle_gamma: u(Optional[int|float], units="DEGREES", label="lattice_angle_gamma", uri=onto.LatticeAngle) = None
        lattice_volume: u(float, units="ANGSTROM3", label="lattice_volume", uri=onto.LatticeVolume) = None
        bravais_lattice: u(str, label="bravais_lattice", uri=onto.BravaisLattice) = None

@dataclass
@u(label="space_group_analysis", uri=onto.SpaceGroupAnalysingAlgorithm)
class SpaceGroupAnalysis:
    space_group: u(str, label="space_group", uri=onto.SpaceGroup) = None
    analysis_libraray: u(str, label="analysis_libraray", uri=onto.Software) = None
    analysis_precision: u(float, units="ANGSTROM", label="analysis_precision", uri=onto.InputParameter) = None

@as_function_node("structure_dataclass")
@u(uri=onto.StructureCreationNode)
def CreateStructure(pr_name: str, element: u(str, label="element", uri=onto.Atom) = 'Fe', 
                    bravais_lattice: u(str, label="bravais_lattice", uri=onto.BravaisLattice) = 'bcc', 
                    a: u(Optional[int|float], label="lattice_parameter_a", uri=onto.LatticeParameter) = 2.87, 
                    c: u(Optional[int|float], label="lattice_parameter_a", uri=onto.LatticeParameter) = None, 
                    cubic:bool = True,
                   ) -> AtomisticSample:
    from pyiron_atomistics import Project
    pr = Project(pr_name)
    if bravais_lattice != 'hcp' and c == None:
        structure = pr.create.structure.bulk(element, crystalstructure=bravais_lattice, cubic=cubic, a=a)
    elif bravais_lattice == 'hcp' and c == None:
        structure = pr.create.structure.bulk(element, crystalstructure=bravais_lattice, cubic=cubic, a=a)
    else:
        structure = pr.create.structure.bulk(element, crystalstructure=bravais_lattice, cubic=cubic, a=a, c=c)

    structure_dataclass = populate_cdict_create_structure_node(structure, bravais_lattice)

    return structure_dataclass

def populate_cdict_create_structure_node(structure, bravais_lattice):

    structure_dataclass = AtomisticSample(class_object=structure)

    sim_cell_dataclass = SampleSimulationCell()
    parse_sim_cell(sim_cell_dataclass, structure)
    structure_dataclass.simulation_cell = sim_cell_dataclass

    chem_species_dataclass = SampleChemicalSpecies()
    parse_chem_species_atoms(chem_species_dataclass, structure)
    structure_dataclass.chemical_species = chem_species_dataclass

    unit_cell_dataclass = SampleUnitCell()
    parse_unit_cell(unit_cell_dataclass, structure, bravais_lattice)
    structure_dataclass.unit_cell = unit_cell_dataclass

    structure_dataclass.crystal_defect = []

    space_group_dataclass = SpaceGroupAnalysis()
    parse_space_group_spglib(space_group_dataclass, structure)
    structure_dataclass.analysis = []
    structure_dataclass.analysis.append(space_group_dataclass)    

    return structure_dataclass

def parse_sim_cell(dc: SampleSimulationCell, structure:Atoms):
    dc.simulation_cell_lengths=[np.round(structure.cell.cellpar()[0],4),np.round(structure.cell.cellpar()[1],4),np.round(structure.cell.cellpar()[2],4)]
    dc.simulation_cell_vectors=[np.round(structure.cell[0],4),np.round(structure.cell[1],4),np.round(structure.cell[2],4)]
    dc.simulation_cell_angles=[np.round(structure.cell.cellpar()[3],4),np.round(structure.cell.cellpar()[4],4),np.round(structure.cell.cellpar()[5],4)]
    dc.simulation_cell_volume=np.round(structure.get_volume(),4)

def parse_chem_species_atoms(dc: SampleChemicalSpecies, structure:Atoms):
    natoms = structure.get_number_of_atoms()
    species_dict = dict(structure.get_number_species_atoms())
    atoms_list = []
    for k in species_dict.keys():
        element = {}
        element["value"] = species_dict[k]
        element["label"] = k
        atoms_list.append(element)
    atoms_list.append({'value': natoms, 'label': 'total_number_atoms'})
    dc.atoms=atoms_list

def get_unit_cell_parameters(structure, bravais_lattice):
    if bravais_lattice == "bcc":
        if structure.get_number_of_atoms() == 1:
            structure_parameters = {
                'a': np.round(structure.cell[1][0]*2, 4),
                'alpha': 90.0,
                'beta': 90.0,
                'gamma': 90.0,
                'volume': np.round((structure.cell[1][0]*2)**3, 4),
                'bravais_lattice': 'bcc'
            }
        else:
            structure_parameters = {
                'a': np.round(structure.cell[1][1], 4),
                'alpha': 90.0,
                'beta': 90.0,
                'gamma': 90.0,
                'volume': np.round(structure.get_volume(),4),
                'bravais_lattice': 'bcc'
            }
    elif bravais_lattice == "fcc":
        if structure.get_number_of_atoms() == 1:
            structure_parameters = {
                'a': np.round(structure.cell[1][0]*2, 4),
                'alpha': 90.0,
                'beta': 90.0,
                'gamma': 90.0,
                'volume': np.round((structure.cell[1][0]*2)**3, 4),
                'bravais_lattice': 'fcc'
            }
        else:
            structure_parameters = {
                'a': np.round(structure.cell[1][1], 4),
                'alpha': 90.0,
                'beta': 90.0,
                'gamma': 90.0,
                'volume': np.round(structure.get_volume(),4),
                'bravais_lattice': 'fcc'
            }
    elif bravais_lattice == "hcp":
        if structure.get_number_of_atoms() == 2:
            structure_parameters = {
                'a': np.round(structure.cell[0][0], 4),
                'c': np.round(structure.cell[2][2], 4),
                'alpha': 90.0,
                'beta': 90.0,
                'gamma': 120.0,
                'volume': np.round(structure.get_volume()*3,4),
                'bravais_lattice': 'hcp'
            }
        else:
            structure_parameters = {
                'a': np.round(structure.cell[0][0], 4),
                'c': np.round(structure.cell[2][2], 4),
                'alpha': 90.0,
                'beta': 90.0,
                'gamma': 120.0,
                'volume': np.round(structure.get_volume(),4),
                'bravais_lattice': 'hcp'
            }

    return structure_parameters

def parse_unit_cell(dc: SampleUnitCell, structure:Atoms, bravais_lattice:str):
    structure_parameters = get_unit_cell_parameters(structure, bravais_lattice)
    dc.lattice_parameter_a=structure_parameters['a']
    if 'b' not in structure_parameters.keys(): 
        dc.lattice_parameter_b=structure_parameters['a']
    else:
        dc.lattice_parameter_b=structure_parameters['b']
    if 'c' not in structure_parameters.keys(): 
        dc.lattice_parameter_c=structure_parameters['a']
    else:
        dc.lattice_parameter_c=structure_parameters['c']
    dc.lattice_angle_alpha=structure_parameters['alpha']
    dc.lattice_angle_beta=structure_parameters['beta']
    dc.lattice_angle_gamma=structure_parameters['gamma']
    dc.lattice_volume=structure_parameters['volume']
    dc.bravais_lattice=structure_parameters['bravais_lattice']

def parse_space_group_spglib(dc: SpaceGroupAnalysis, structure:Atoms):
    from inspect import signature
    dc.space_group = structure.get_symmetry().spacegroup['InternationalTableSymbol']
    dc.analysis_libraray = "spglib"
    dc.analysis_precision = float(str(signature(structure.get_symmetry).parameters['symprec']).split("=")[1])


