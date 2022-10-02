from libcst.metadata import FullRepoManager, FullyQualifiedNameProvider

from kwonly_transformer import CallArgumentsTransformer, FunctionParametersTransformer

files = {"potato/main.py", "potato/another.py"}
mgr = FullRepoManager(".", files, {FullyQualifiedNameProvider})

transformer = FunctionParametersTransformer()
for file in files:
    wrapper = mgr.get_metadata_wrapper_for_path(file)
    modified_tree = wrapper.visit(transformer)
    print(modified_tree.code)

transformer = CallArgumentsTransformer(transformer.functions)
for file in files:
    wrapper = mgr.get_metadata_wrapper_for_path(file)
    modified_tree = wrapper.visit(transformer)
    print(modified_tree.code)
