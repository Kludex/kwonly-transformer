from typing import Dict

import libcst as cst
from libcst import SimpleWhitespace

# TODO: `functions` dictionary should use <module.function> as name.


class FunctionParametersTransformer(cst.CSTTransformer):
    def __init__(self, threshold: int = 2) -> None:
        self.functions: Dict[str, cst.Parameters] = {}
        self.threshold = threshold

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        params_params = list(updated_node.params.params)
        kwonly_params = list(updated_node.params.kwonly_params)
        if len(updated_node.params.params) > self.threshold:
            new_params = updated_node.params.with_changes(
                params=[], kwonly_params=params_params + kwonly_params
            )
            self.functions[original_node.name.value] = new_params
            return updated_node.with_changes(params=new_params)
        return updated_node


class CallArgumentsTransformer(cst.CSTTransformer):
    def __init__(self, functions: Dict[str, cst.Parameters]) -> None:
        self.functions = functions

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        params = None
        if isinstance(original_node.func, cst.Name):
            params = self.functions.get(original_node.func.value)
        elif isinstance(original_node.func, cst.Attribute):
            params = self.functions.get(original_node.func.attr.value)
        if params:
            posonly_args_len = len(params.posonly_params)
            posonly_args = list(original_node.args[:posonly_args_len])
            kwonly_args = [
                arg.with_changes(
                    keyword=params.kwonly_params[idx].name,
                    equal=cst.AssignEqual(
                        whitespace_before=SimpleWhitespace(value=""),
                        whitespace_after=SimpleWhitespace(value=""),
                    ),
                )
                for idx, arg in enumerate(original_node.args[posonly_args_len:])
            ]
            return updated_node.with_changes(args=posonly_args + kwonly_args)
        return original_node
