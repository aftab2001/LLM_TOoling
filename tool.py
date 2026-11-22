#tool type
from typing import Any,Callable
from dataclasses import dataclass
from itertools import combinations
@dataclass
class Tool:
    id_type:str
    name:str
    description: str
    parameters: dict[str,Any]
    handler : Callable[...,float]
    def schema(self) -> dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":self.name,
                "description":self.description,
                "parameters":self.parameters,
            },
        }
OPERATIONS = ("add","sub","mul","div","mod") 

#repatable
def parameters(
    operations: tuple[str, ...],
    operation_required: bool = True
) -> dict[str, Any]:

    required = ["a", "b"]

    if operation_required:
        required.append("operation")

    return {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "First operand."
            },
            "b": {
                "type": "number",
                "description": "Second operand."
            },
            "operation": {
                "type": "string",
                "enum": list(operations),
                "description": "Arithmetic operation to perform."
            },
        },
        "required": required,
        "additionalProperties": False,
    }
def apply_operation(op:str,a:Any,b:Any) ->float:
    # the function expects random number between 1 and 100 , to avoid divide by 0 
    if op=="add":
        result = a+b
    elif op=="sub":
        result = a-b
    elif op == "mul":
        result = a*b
    elif op == "div":
        result = a/b
    elif op == "mod":
        result = a%b
    return float(result)
      
def create_handler(supported_operations:tuple[str,...])->Callable[...,float]:
    def handler(
        a:float,
        b:float,
        operation:str
    ) -> float:
        if operation not in supported_operations:
            raise ValueError(f"unsupported ops:{operation}")
        return apply_operation(operation,a,b)
    return handler
OPERATION_NAMES ={
    "add":"addition",
    "sub":"subtraction",
    "mul":"multiplication",
    "div":"division",
    "mod":"modulo",
}
def create_description(
    supported_operations:tuple[str,...]
)-> str:
    names = [
        OPERATION_NAMES[op]
        for op in supported_operations
    ]  
    operation_text = ", ".join(names)
    return (
        f"Perform one arithmetic operation on two numbers. "
        f"Supported operations:{operation_text}"
    )
def tool_schema() -> list[Tool]:

    tools = []
    remaining = ("sub", "mul", "div", "mod")
    tool_id = 1
    for size in range(0, len(remaining) + 1):

        for subset in combinations(remaining, size):

            supported = ("add",) + subset
            name = "_".join(supported)
            handler = create_handler(supported)
    # the below tool generates for eg:           
    # Tools(
    #     id_type="func_4",
    #     name="add_div",
    #     description="perform either of the two arithmetic operations.Supported operation addition division",
    #     parameters=parameters(["add", "div"]),
    #     handler=op_add_div,
    # ),

            tool = Tool(
                id_type=f"func_{tool_id}",
                name=name,
                description=create_description(supported),
                parameters=parameters(supported),
                handler=handler,
            )

            tools.append(tool)
            tool_id += 1

    return tools         
TOOLS = tool_schema()

TOOL_BY_NAME = {
    tool.name: tool
    for tool in TOOLS
}

TOOL_BY_ID = {
    tool.id_type: tool
    for tool in TOOLS
}


def get_tool_schemas() -> list[dict[str, Any]]:

    return [
        tool.schema()
        for tool in TOOLS
    ]
