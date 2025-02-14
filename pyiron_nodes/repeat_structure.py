from pyiron_workflow import as_function_node
from dataclasses import dataclass
from semantikon.typing import u
from semantikon.converter import semantikon_class
from semantics import onto
from pyiron_nodes.create_structure import AtomisticSample, parse_sim_cell, parse_chem_species_atoms

@as_function_node("structure_dataclass")
@u(uri=onto.StructureManipulationNode, semantic_operation=(AtomisticSample, 'update', ['simulation_cell', 'chemical_species']))
def RepeatStructure(structure_dataclass: u(AtomisticSample, label="atomistic_sample", uri=onto.AtomicScaleSample), x_repeat: int = 3, y_repeat: int = 3, z_repeat: int = 3) -> AtomisticSample:
    import copy
    repeated_structure_dataclass = copy.copy(structure_dataclass)
    repeated_structure = repeated_structure_dataclass.class_object.repeat([x_repeat, y_repeat, z_repeat])
    repeated_structure_dataclass.class_object = repeated_structure

    repeated_structure_dataclass = populate_cdict_repeat_structure_node(repeated_structure_dataclass, structure_dataclass, repeated_structure)
    
    return repeated_structure_dataclass

def populate_cdict_repeat_structure_node(repeated_structure_dataclass, structure_dataclass, repeated_structure):
    import copy
    repeated_structure_dataclass.provenance_object = [structure_dataclass.class_object]

    if RepeatStructure.node_function._semantikon_metadata['semantic_operation'][1] == 'update':
    
        repeated_sim_cell_dataclass = copy.copy(structure_dataclass.simulation_cell)
        parse_sim_cell(repeated_sim_cell_dataclass, repeated_structure)
        repeated_structure_dataclass.simulation_cell=repeated_sim_cell_dataclass

        repeated_chem_species_dataclass = copy.copy(structure_dataclass.chemical_species)
        parse_chem_species_atoms(repeated_chem_species_dataclass, repeated_structure)
        repeated_structure_dataclass.chemical_species=repeated_chem_species_dataclass

    else:
        raise KeyError("Unsupported semantic operation for this node")

    repeated_unit_cell_dataclass = copy.copy(structure_dataclass.unit_cell)
    repeated_structure_dataclass.unit_cell=repeated_unit_cell_dataclass

    repeated_defect_dataclass_list = copy.copy(structure_dataclass.crystal_defect)
    repeated_structure_dataclass.crystal_defect=repeated_defect_dataclass_list

    repeated_analysis_dataclass_list = copy.copy(structure_dataclass.analysis)
    repeated_structure_dataclass.analysis=repeated_analysis_dataclass_list

    return repeated_structure_dataclass