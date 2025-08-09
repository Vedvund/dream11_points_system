import os

from core.config import settings


def get_root_dir(project_dir_name=settings.PROJECT_DIR_NAME):
    current_path = os.path.abspath(__file__)
    path_parts = current_path.split(os.sep)

    if project_dir_name in path_parts:
        project_index = path_parts.index(project_dir_name)
        root_dir = os.sep.join(path_parts[:project_index + 1])
        return root_dir
    else:
        raise FileNotFoundError(f"Project folder '{project_dir_name}' not found in the path.")


def read_file_context(path):
    with open(path, 'r') as f:
        return f.read()


if __name__ == '__main__':
    print(get_root_dir())
