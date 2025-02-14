from pyiron_workflow import as_function_node
from dataclasses import dataclass
from semantikon.typing import u
from semantikon.converter import semantikon_class
from semantics import onto
from typing import Optional
from pyiron_nodes.create_structure import AtomisticSample, parse_chem_species_atoms
import numpy as np

@semantikon_class
@u(label="vacancy", uri=onto.Vacancy)
@dataclass
class SampleVacancyDefect:
    vacancy_count: u(int, label="vacancy_count", uri=onto.Vacancy) = None
    vacancy_positions: u(np.ndarray, label="vacancy_positions", uri=onto.Position) = None
    removed_elements: u(list, label="removed_elements", uri=onto.Atom) = None

@as_function_node("structure_dataclass")
@u(uri=onto.StructureManipulationNode, semantic_operation=(AtomisticSample, 'append', ['crystal_defect'], SampleVacancyDefect))
def CreateVacancy(structure_dataclass: u(AtomisticSample, label="atomistic_sample", uri=onto.AtomicScaleSample), vacancy_indices: Optional[str|list[int]] = '0 3') -> AtomisticSample:
    import copy
    if isinstance(vacancy_indices, str):
        vacancy_indices = [int(i) for i in vacancy_indices.split()]
    vacancy_structure_dataclass = copy.copy(structure_dataclass)
    vacancy_structure = vacancy_structure_dataclass.class_object.copy()
    for index in vacancy_indices:
        del vacancy_structure[index]
    vacancy_structure_dataclass.class_object = vacancy_structure
    
    vacancy_structure_dataclass = populate_cdict_create_vacancy_node(vacancy_structure_dataclass, structure_dataclass, vacancy_structure, vacancy_indices)

    return vacancy_structure_dataclass

def populate_cdict_create_vacancy_node(vacancy_structure_dataclass, structure_dataclass, vacancy_structure, vacancy_indices):
    import copy
    vacancy_structure_dataclass.provenance_object.append(structure_dataclass.class_object)
    
    vacancy_sim_cell_dataclass = copy.copy(structure_dataclass.simulation_cell)
    vacancy_structure_dataclass.simulation_cell=vacancy_sim_cell_dataclass
    
    vacancy_chem_species_dataclass = copy.copy(structure_dataclass.chemical_species)
    parse_chem_species_atoms(vacancy_chem_species_dataclass, vacancy_structure)
    vacancy_structure_dataclass.chemical_species=vacancy_chem_species_dataclass
    
    vacancy_unit_cell_dataclass = copy.copy(structure_dataclass.unit_cell)
    vacancy_structure_dataclass.unit_cell=vacancy_unit_cell_dataclass

    if CreateVacancy.node_function._semantikon_metadata['semantic_operation'][1] == 'append':
        vacancy_defect_dataclass_list = copy.copy(structure_dataclass.crystal_defect)
    elif CreateVacancy.node_function._semantikon_metadata['semantic_operation'][1] == 'overwrite':
         vacancy_defect_dataclass_list = []
    else:
        KeyError("Unsupported semantic operation for this node")

    vacancy_defect_dataclass = SampleVacancyDefect()
    vacancy_defect_dataclass.vacancy_count = len(vacancy_indices)
    positions = []
    for index in vacancy_indices:
        positions.append(structure_dataclass.class_object.get_positions()[index])
    vacancy_defect_dataclass.vacancy_positions = positions
    elements = []
    for index in vacancy_indices:
        elements.append(structure_dataclass.class_object.get_chemical_symbols()[index])
    vacancy_defect_dataclass.removed_elements = elements

    vacancy_defect_dataclass_list.append(vacancy_defect_dataclass)
    vacancy_structure_dataclass.crystal_defect=vacancy_defect_dataclass_list

    vacancy_analysis_dataclass_list = copy.copy(structure_dataclass.analysis)
    vacancy_structure_dataclass.analysis=vacancy_analysis_dataclass_list

    return vacancy_structure_dataclass