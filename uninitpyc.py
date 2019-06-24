# uninitpyc.py
# Tool that scans C source code to find variables that aren't initialized in
# their declaration. It's a best practice.

import sys
from pycparser import c_generator, parse_file, c_ast

def ast_traverse(block_items):
    # Check all supported C syntax structures.
    for block_item in block_items:
        check_uninitialized_variable(block_item)
        check_body(block_item)
        check_if_block(block_item)
        check_for_loop(block_item)
        check_while_dowhile_loop(block_item)
        check_scope_block(block_item)
        check_switch_statement(block_item)
        check_case_default_statement(block_item)

def check_uninitialized_variable(block_item):
    # Declaring multiple variables in one line splits into multiple block_items,
    # so we don't need to explicitly write code to handle this.
    if type(block_item) == c_ast.Decl and hasattr(block_item, 'init') and block_item.init is None:
        generator = c_generator.CGenerator() # TODO: do I need to instantiate this every time?
        print("line %s: %s" % (block_item.coord.line, generator.visit(block_item)))

def check_body(block_item):
    # Function body, traverse downwards
    if type(block_item) == c_ast.FuncDef and hasattr(block_item, 'body'):
        ast_traverse(block_item.body.block_items)

def check_if_block(block_item):
    if type(block_item) == c_ast.If or type(block_item) == c_ast.Compound:
        # has child iftrues, iffalses, block_items
        if hasattr(block_item, 'iftrue'): 
            traverse_if_block(block_item.iftrue)
        if hasattr(block_item, 'iffalse'):
            traverse_if_block(block_item.iffalse)

def check_switch_statement(block_item):
    if type(block_item) == c_ast.Switch:
        ast_traverse(block_item.stmt.block_items)

def check_case_default_statement(block_item):
    if type(block_item) == c_ast.Case or type(block_item) == c_ast.Default:
        ast_traverse(block_item.stmts)


def traverse_if_block(if_block):
    # 'if_block' isn't a list, so we can't just pass this back into ast_traverse
    # and iterate over block_items
    if hasattr(if_block, 'block_items'):
        ast_traverse(if_block.block_items)
    if hasattr(if_block, 'iftrue'):
        traverse_if_block(if_block.iftrue)
    if hasattr(if_block, 'iffalse'):
        traverse_if_block(if_block.iffalse)

def check_while_dowhile_loop(block_item):
    # while and do/while loops have the same structure in pycparser.
    if type(block_item) == c_ast.While or type(block_item) == c_ast.DoWhile:
        ast_traverse(block_item.stmt.block_items) # traverse for loop block

def check_for_loop(block_item):
    # like a while or do/while loop, but with initializations for traversal
    if type(block_item) == c_ast.For:
        ast_traverse(block_item.init.decls)
        ast_traverse(block_item.stmt.block_items) # traverse for loop block

def check_scope_block(block_item):
    # eg. something defined like this:
    #   {
    #       int a;
    #   }
    if type(block_item) == c_ast.Compound:
        ast_traverse(block_item.block_items)

if __name__ == "__main__":
    # TODO: parse_file doesn't remove comments from the source 😱 Try using
    # these preprocessor args? https://stackoverflow.com/questions/2394017

    # TODO: don't include fake_libc_include in our source, use dependency
    # management instead

    if len(sys.argv) > 1:
        ast = parse_file(sys.argv[1], use_cpp=True, cpp_args=r'-Ipycparser/utils/fake_libc_include')
        # TODO: is passing in ext as "block_items" accurate terminology?
        ast_traverse(ast.ext)
    else:
        print("Please provide a file name as an argument")
