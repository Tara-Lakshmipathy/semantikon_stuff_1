from pyiron_workflow import as_function_node, as_macro_node, as_dataclass_node
from typing import Optional, Literal

@as_function_node("sum")
def Addition(variable1: int|float, variable2: int|float) -> int|float:
    sum_ = variable1 + variable2
    return sum_

@as_function_node("difference")
def Subtraction(variable1, variable2: int|float) -> int|float:
    diff = variable1 - variable2
    return diff

@as_function_node("product")
def Multiplication(variable1, variable2: int|float) -> int|float:
    prod = variable1 * variable2
    return prod

@as_function_node("quotient")
def Division(variable1, variable2: int|float) -> int|float:
    qnt = variable1 / variable2
    return qnt

@as_function_node("choice_1", "choice_2", "choice_3")
def LiterallyJustANode(inp_1: Literal["J.R.R. Tolkien", "Robert Jordan", "Brandon Sanderson"],
                       inp_2: Literal[123456789, 987654321, 101010101],
                       inp_3: Literal["Isaac Asimov", 147258369, "Stephen Baxter", 963852741]
                      ):
    return inp_1, inp_2, inp_3

@as_function_node("choice_1", "choice_2", "choice_3")
def LiterallyJustADummy(inp_1, inp_2, inp_3):
    return inp_1, inp_2, inp_3

@as_macro_node("choice_1", "choice_2_minus1", "choice_3")
def LiterallyJustAMacro(self,
                        inp_1: Literal["Ludwig Boltzmann", "Paul Dirac", "Richard Feynman"],
                        inp_2: Literal[123456789, 987654321, 101010101],
                        inp_3: Literal["Carl Sagan", 147258369, "Michio Kaku", 963852741]
                       ):
    self.LiterallyJustADummy = LiterallyJustADummy(inp_1, inp_2, inp_3)
    self.Subtraction = Subtraction()
    self.Subtraction.set_input_values(variable2=1)
    self.Subtraction.inputs.variable1.connect(self.LiterallyJustADummy.outputs.choice_2)
    return self.LiterallyJustADummy.outputs.choice_1, self.Subtraction, self.LiterallyJustADummy.outputs.choice_3

@as_dataclass_node
class LiterallyJustADataclass:
    choice_1: Literal["Iron Maiden", "Blind Guardian", "Wintersun"]
    choice_2: Literal[123456789, 987654321, 101010101]
    choice_3: Literal["Nightwish", 147258369, "Amon Amarth", 963852741]

@as_function_node("dataframe")
def LiterallyJustADataframe(dataclass: LiterallyJustADataclass.dataclass):
    import pandas as pd
    data = {"fields": ["choice_1", "choice_2", "choice_3"],
            "chosen": [dataclass.choice_1, dataclass.choice_2, dataclass.choice_3]
           }
    df = pd.DataFrame(data)
    return df

