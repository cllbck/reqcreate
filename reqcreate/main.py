import argparse
import os
import ast
import yarg

exclude_dirs = ('env', 'venv', '.git', '__pycache__', '.idea')


def filter_files(dir, files_list):
    filtered_files = [os.path.join(dir, file) for file in files_list if file.endswith('.py')]
    return filtered_files


def get_all_files(project_dir):
    py_files = []
    tree = os.walk(project_dir, topdown=True)
    for i in tree:
        main_dirs = [os.path.join(project_dir, item) for item in i[1] if item not in exclude_dirs]
        py_files.extend(filter_files(project_dir, i[2]))
        break

    for dir in main_dirs:
        tree = os.walk(dir, topdown=True)
        for iter in tree:
            py_files.extend(filter_files(iter[0], iter[2]))

    return py_files


def find_packages_from_file(file):
    packages = []
    with open(file, 'r', encoding='utf-8') as f:
        raw_file = f.read()
        tree = ast.parse(raw_file)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for subnode in node.names:
                    if subnode.name.find('.') == -1:
                        packages.append(subnode.name)
                    else:
                        packages.append(subnode.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module.find('.') == -1:
                    packages.append(node.module)
                else:
                    packages.append(node.module.split('.')[0])
    return packages


def get_all_packages(py_files):
    packages = []
    extendet_packeges = []
    for file in py_files:
        packages.extend(find_packages_from_file(file))
        file_name = os.path.basename(file).split('.')[0]
        extendet_packeges.append(file_name)
    packages = set(packages)
    packages.difference_update(extendet_packeges)
    return packages


def clear_bultin_packages(packages):
    built_in = set()
    with open(os.path.join(os.path.dirname(__file__), 'built-in.txt'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            built_in.add(line.split('\n')[0])
    packages.difference_update(built_in)
    return packages


def pypi_names_of_package(import_names):
    result = set()
    with open(os.path.join(os.path.dirname(__file__), 'mapping.txt'), 'r') as f:
        data = dict(x.strip().split(":") for x in f)
    for name in import_names:
        result.add(data.get(name, name))
    return sorted(result, key=lambda s: s.lower())


def create_requirements_file(packages, dir):
    file = os.path.join(dir, 'requirements.txt')
    with open(file, 'w') as f:
        for item in packages:
            package = yarg.get(item)
            f.write(f'{package.name}=={package.latest_release_id}\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="project directory")
    args = parser.parse_args()
    if args.dir:
        py_files = get_all_files(args.dir)
        packages = get_all_packages(py_files)
        packages = clear_bultin_packages(packages)
        packages = pypi_names_of_package(packages)
        create_requirements_file(packages, args.dir)


if __name__ == '__main__':
    main()
