from dataclasses import fields
from semantikon.converter import parse_metadata, meta_to_dict
from pyiron_workflow import as_function_node

@as_function_node("Done")
def VisualizeDataclass(dataclass):
    DCViz(dataclass)
    return "Done"

def parse_subdataclass(field_object, nesting_level):
    k_1 = []
    v_1 = []
    f_1 = []
    for nested_field in fields(field_object):
        nested_field_object = getattr(field_object, nested_field.name)
        f_1.append(nested_field_object)
        for k,v in (field_object.__annotations__.items()):
            k_1.append(k)
            v_1.append(v)
    l_1 = list(zip(k_1, v_1, f_1))
    for item in l_1:
        print(nesting_level*'  ' + '{')
        print((nesting_level+1)*'  ' + 'sub_field_name:\033[94m', item[0], '\x1b[0m')
        print((nesting_level+1)*'  ' + 'uri:\033[95m', meta_to_dict(item[1])['uri']().IRI, '\x1b[0m')
        print((nesting_level+1)*'  ' + 'value: \033[94m', item[2], '\x1b[0m')
        print((nesting_level+1)*'  ' + 'units:\033[95m', meta_to_dict(item[1])['units'], '\x1b[0m')
        print((nesting_level+1)*'  ' + 'data_type: \033[94m', type(item[2]).__name__, '\x1b[0m')
        print(nesting_level*'  ' + '}')
    

def DCViz(dc):
    #print('node_class:\033[94m', node.__class__.__name__, '\x1b[0m uri:\033[95m', node.node_function._semantikon_metadata['uri']().IRI, '\x1b[0m\n')
    print('{')
    print('  dataclass:\033[94m', dc.__class__.__name__, '\x1b[0m')
    print('  uri:\033[95m', dc.__class__._semantikon_metadata['uri']().IRI, '\x1b[0m')
    print('}')
    print('--------------------------------------------------')
    for field in fields(dc):
        field_object=getattr(dc, field.name)
        print('  {')
        print('    field_name:\033[94m', field.name, '\x1b[0m')
        print('    uri:\033[95m', meta_to_dict(field.type)['uri']().IRI, '\x1b[0m')
        print('    value:\033[94m python id', id(field_object), '\x1b[0m')
        print('    units:\033[95m', meta_to_dict(field.type)['units'], '\x1b[0m')
        print('    data_type: \033[94m', type(field_object).__name__, '\x1b[0m')
        print('  }')
        try:
            parse_subdataclass(field_object,2)
        except:
            pass
        if type(field_object) == list:
            for item in field_object:
                print('  ', ' {')
                print('  ', '  ', 'list_item:\033[94m', '[' + str(field_object.index(item)) + ']', '\x1b[0m')
                print('  ', '  ', 'uri:\033[95m', item.__class__._semantikon_metadata['uri']().IRI, '\x1b[0m')
                print('  ', '  ', 'value:\033[94m python id', id(item), '\x1b[0m')
                print('  ', '  ', 'units:\033[95m', None, '\x1b[0m', '\x1b[0m')
                print('  ', '  ', 'data_type: \033[94m', type(item).__name__, '\x1b[0m')
                print('  ', ' }')
                try:
                    parse_subdataclass(item,3)
                except:
                    pass
        print('--------------------------------------------------')