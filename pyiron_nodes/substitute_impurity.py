from pyiron_workflow import as_function_node
from dataclasses import dataclass
from semantikon.typing import u
from semantikon.converter import semantikon_class
from semantics import onto
from typing import Optional
from pyiron_nodes.create_structure import AtomisticSample, parse_chem_species_atoms
import numpy as np

@semantikon_class
@u(label="substitutional_impurity", uri=onto.SubstitutionalImpurity)
@dataclass
class SampleSubstitutionDefect:
    substitution_count: u(int, label="substitution_count", uri=onto.SubstitutionalImpurity) = None
    substitution_positions: u(np.ndarray, label="substitution_positions", uri=onto.Position) = None
    substitution_element: u(np.ndarray, label="substitution_element", uri=onto.Atom) = None
    substituted_elements: u(list, label="substituted_elements", uri=onto.Atom) = None

@as_function_node("structure_dataclass")
@u(uri=onto.StructureManipulationNode, semantic_operation=(AtomisticSample, 'append', ['crystal_defect'], SampleSubstitutionDefect))
def SubstituteImpurityAtom(structure_dataclass: u(AtomisticSample, label="atomistic_sample", uri=onto.AtomicScaleSample), substitute_species: u(str, label="substitute_species", uri=onto.Atom) = 'Mo', 
                           substitute_magmom: Optional[int|float] = 0.0, subs_indices:  Optional[str|list[int]] = "5 10") -> AtomisticSample:
    import copy
    if isinstance(subs_indices, str):
        subs_indices = [int(i) for i in subs_indices.split()]
    subs_structure_dataclass = copy.copy(structure_dataclass)
    subs_structure = subs_structure_dataclass.class_object.copy()
    for index in subs_indices:
        subs_structure[index] = substitute_species
        subs_structure[index].magmom = substitute_magmom
    subs_structure_dataclass.class_object = subs_structure

    subs_structure_dataclass = populate_cdict_substitute_impurity_atom_node(subs_structure_dataclass, structure_dataclass, subs_structure, substitute_species, subs_indices)

    return subs_structure_dataclass

def populate_cdict_substitute_impurity_atom_node(subs_structure_dataclass, structure_dataclass, subs_structure, substitute_species, subs_indices):
    import copy
    subs_structure_dataclass.provenance_object.append(structure_dataclass.class_object)
    
    subs_sim_cell_dataclass = copy.copy(structure_dataclass.simulation_cell)
    subs_structure_dataclass.simulation_cell=subs_sim_cell_dataclass

    subs_chem_species_dataclass = copy.copy(structure_dataclass.chemical_species)
    parse_chem_species_atoms(subs_chem_species_dataclass, subs_structure)
    subs_structure_dataclass.chemical_species=subs_chem_species_dataclass

    subs_unit_cell_dataclass = copy.copy(structure_dataclass.unit_cell)
    subs_structure_dataclass.unit_cell=subs_unit_cell_dataclass

    if SubstituteImpurityAtom.node_function._semantikon_metadata['semantic_operation'][1] == 'append':
        subs_defect_dataclass_list = copy.copy(structure_dataclass.crystal_defect)
    elif SubstituteImpurityAtom.node_function._semantikon_metadata['semantic_operation'][1] == 'overwrite':
        subs_defect_dataclass_list = []

    subs_defect_dataclass = SampleSubstitutionDefect()
    subs_defect_dataclass.vacancy_count = len(subs_indices)
    positions = []
    for index in subs_indices:
        positions.append(structure_dataclass.class_object.get_positions()[index])
    subs_defect_dataclass.substitution_positions = positions
    elements = []
    for index in subs_indices:
        elements.append(structure_dataclass.class_object.get_chemical_symbols()[index])
    subs_defect_dataclass.substituted_elements = elements

    subs_defect_dataclass.substitution_element = substitute_species

    subs_defect_dataclass_list.append(subs_defect_dataclass)
    subs_structure_dataclass.crystal_defect=subs_defect_dataclass_list

    subs_analysis_dataclass_list = copy.copy(structure_dataclass.analysis)
    subs_structure_dataclass.analysis=subs_analysis_dataclass_list

    return subs_structure_dataclass