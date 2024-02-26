import os
import ast

def get_classes_in_file(filepath):
    """Returns a list of class names defined in the specified Python file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        file_content = file.read()
    tree = ast.parse(file_content)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

def generate_init_py(package_path):
    """Generates __init__.py files that import classes or modules as needed."""
    for root, dirs, files in os.walk(package_path):
        init_content = []
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = file[:-3]
                classes = get_classes_in_file(os.path.join(root, file))
                relative_path = os.path.relpath(root, package_path).replace(os.path.sep, '.')
                
                # Import the module itself
                if relative_path == '.':
                    import_statement = f"from . import {module_name}"
                else:
                    import_statement = f"from .{relative_path} import {module_name}"
                init_content.append(import_statement)
                
                if classes:
                    # Generate import statements for each class.
                    for cls in classes:
                        if relative_path == '.':
                            import_statement = f"from .{module_name} import {cls}"
                        else:
                            import_statement = f"from .{relative_path}.{module_name} import {cls}"
                        init_content.append(import_statement)
                
        
        init_path = os.path.join(root, '__init__.py')
        with open(init_path, 'w', encoding='utf-8') as init_file:
            init_file.write('\n'.join(init_content) + '\n')

package_path = '/usr/local/lib/python3.8/site-packages/oasisabm'
generate_init_py(package_path)
