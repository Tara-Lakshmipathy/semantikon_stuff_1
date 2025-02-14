from pyiron_workflow import as_function_node
from semantikon.typing import u
from semantics import onto
from pyiron_nodes.create_structure import AtomisticSample

@as_function_node("view")
def VisualizeStructure(structure_dataclass: u(AtomisticSample, label="atomistic_sample", uri=onto.AtomicScaleSample)):
    """
    structure: ase object from pyiron_atomistics
    """
    
    structure_object = structure_dataclass.class_object.copy()
    
    return structure_object.plot3d()