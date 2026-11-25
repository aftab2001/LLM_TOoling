#tool type
from typing import Any,Callable
from dataclasses import dataclass
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
def parameters(operations: tuple[str, ...]) -> dict[str, Any]:
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
        "required": ["a", "b", "operation"],
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
    else:
        raise ValueError(f"unknown op: {op}")
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

    # nested chain: func_1=add, func_2=add+sub, ..., func_N=all OPERATIONS
    tools = []
    for i in range(1, len(OPERATIONS) + 1):
        supported = OPERATIONS[:i]
        tools.append(Tool(
            id_type=f"func_{i}",
            name="_".join(supported),
            description=create_description(supported),
            parameters=parameters(supported),
            handler=create_handler(supported),
        ))
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
