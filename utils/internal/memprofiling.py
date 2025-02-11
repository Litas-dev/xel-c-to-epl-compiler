import sys
import os
import resource
import tracemalloc
from pycparser import parse_file, CParser
from pycparser.c_ast import NodeVisitor

def parse_c_file(filepath):
    """ Parse a C file and return its AST. """
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return None
    
    try:
        return parse_file(filepath, use_cpp=True)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None

def memory_profile():
    """ Profile memory usage while parsing C code. """
    tracemalloc.start()
    filepath = input("Enter C file path (or press Enter to use default '/tmp/197.c'): ") or "/tmp/197.c"
    
    ast = parse_c_file(filepath)
    if ast is None:
        return
    
    print('Memory usage: %s KB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    snapshot = tracemalloc.take_snapshot()
    print("[ Tracemalloc Stats ]")
    for stat in snapshot.statistics('lineno')[:10]:
        print(stat)

class CustomVisitor(NodeVisitor):
    """ Custom AST visitor to analyze function calls. """
    def __init__(self):
        super().__init__()
        self.current_parent = None

    def visit_FuncCall(self, node):
        print("\n[ Visiting Function Call ]")
        node.show()
        print('[ Parent Node ]')
        if self.current_parent:
            self.current_parent.show()
        else:
            print("No parent node.")

    def generic_visit(self, node):
        old_parent = self.current_parent
        self.current_parent = node
        for _, child in node.children():
            self.visit(child)
        self.current_parent = old_parent

if __name__ == "__main__":
    # Ask user for file input or use inline source
    source_code = input("Enter inline C code (or press Enter to use a sample): ")
    if not source_code:
        source_code = """void foo() {
            printf(\"Hello, world!\");
        }"""
    
    parser = CParser()
    try:
        ast = parser.parse(source_code, filename='<inline>')
        print("\n[ Parsed AST ]")
        ast.show()
        
        print("\n[ Running AST Visitor ]")
        visitor = CustomVisitor()
        visitor.visit(ast)
    except Exception as e:
        print(f"Parsing error: {e}")
    
    # Run memory profiling
    memory_profile()
