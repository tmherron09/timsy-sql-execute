import os
from pathlib import Path
from typing import Union


def sql_read(file_path: Union[ str | Path]) -> str:
    with open(file_path, 'r') as file:
        sql_query = file.read().strip()
    return sql_query


def get_cwd_scripts_path()-> Path:
    try:
        cwd = os.path.abspath(os.path.curdir)
        if not os.path.exists('./scripts'):
            os.makedirs('./scripts')
        return Path(cwd) / 'scripts'
    except Exception as e:
        print(e)
        raise e

def get_scripts(script_path: Union[Path | str | None] = None) -> list[Path]:
    if script_path is None:
        script_path = get_cwd_scripts_path()
    if isinstance(script_path, str):
        script_path = Path(script_path)
    if not script_path.exists():
        raise FileNotFoundError(f"Path {script_path} does not exist")
    scripts = [script for script in script_path.iterdir() if script.is_file() and script.suffix == '.sql']
    return scripts

def file_names(script_path_list: list[Path]) -> list[str]:
    return [p.name for p in script_path_list]

if __name__ == '__main__':
    s_path = get_cwd_scripts_path()
    s = get_scripts(s_path)
    print([p.name for p in s])
    print(file_names(s))