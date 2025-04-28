from pyiron_workflow import as_function_node
from semantikon.typing import u
from semantikon.converter import parse_input_args
from semantics import onto

@as_function_node("result")
def RestrictedNode(
    inp1: u(object, class_restrictions=[("crystal_defect", "type", "all", onto.PointDefect)], value_restrictions=[]), 
    inp2: u(object, value_restrictions=[("unit_cell", "bravais_lattice", "bcc")])
):

    check_1 = check_first_restriction(inp1)
    check_2 = check_second_restriction(inp2)

    if check_1 == True and check_2 == True:
        print("")
        final_check = ("You may pass.")
    else:
        raise ValueError("YOU SHALL NOT PASS!!!")
    
    return final_check

def check_first_restriction(inp1):
    restriction_key = parse_input_args(RestrictedNode.node_function)['inp1']['class_restrictions'][0][0]
    restriction_field =  parse_input_args(RestrictedNode.node_function)['inp1']['class_restrictions'][0][1]
    restriction_class = parse_input_args(RestrictedNode.node_function)['inp1']['class_restrictions'][0][3]

    incoming_class_objects = []
    for item in eval('inp1.' + restriction_key):
        incoming_class_objects.append(item.__class__._semantikon_metadata['uri'])

    checking_mode = parse_input_args(RestrictedNode.node_function)['inp1']['class_restrictions'][0][2]
    if checking_mode == 'any':
        check = False
        for obj_class in incoming_class_objects:
            obj = obj_class()
            if isinstance(obj, restriction_class): 
                check = True
    elif checking_mode == 'all':
        check = True
        for obj_class in incoming_class_objects:
            obj = obj_class()
            if not isinstance(obj, restriction_class):
                check = False

    incoming_class_objects_names = []
    for item in incoming_class_objects:
        incoming_class_objects_names.append(item.__name__)

    print('Restriction target: "' + restriction_key + '" has continuant part "' + restriction_field + '"')
    print('Incoming class(es): ', incoming_class_objects_names)
    print('Checking mode: ' + checking_mode)
    print ('Restriction class: ', restriction_class.__name__)
    print('')
    print('Result: ', check)
    print('')

    return check

def check_second_restriction(inp2):
    restriction_key = parse_input_args(RestrictedNode.node_function)['inp2']['value_restrictions'][0][0]
    restriction_field =  parse_input_args(RestrictedNode.node_function)['inp2']['value_restrictions'][0][1]
    restriction_value = parse_input_args(RestrictedNode.node_function)['inp2']['value_restrictions'][0][2]

    incoming_value = eval('inp2.' + restriction_key + '.' + restriction_field)

    if incoming_value == restriction_value:
        check = True
    else:
        check = False

    print('Restriction target: "' + restriction_key + '" has continuant part "' + restriction_field + '"')
    print('Incoming value(s): ', incoming_value)
    print ('Restriction value: ', restriction_value)
    print('')
    print('Result: ', check)
    print('')

    return check
