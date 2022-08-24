import os
import importlib


def import_tables():  # pragma: no cover
    for dir_path, _, file_names in os.walk("src/domain"):
        for file_name in file_names:
            if file_name.endswith("py") and file_name not in "__init__.py":
                file_path_wo_ext, _ = os.path.splitext((os.path.join(dir_path, file_name)))
                module_name = file_path_wo_ext.replace(os.sep, ".")
                importlib.import_module(module_name)
