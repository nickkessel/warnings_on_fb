import tomllib # use 'tomllib' for Python 3.11+

def get_local_version(file_path="pyproject.toml"):
    with open(file_path, mode="rb") as f:
        toml_data = tomllib.load(f)
    # The version can be under [project] or [tool.poetry], depending on the setup
    try:
        return toml_data["project"]["version"]
    except KeyError:
        # Fallback for poetry specific structure if needed
        return toml_data["tool"]["poetry"]["version"]

if __name__ == '__main__':
    version = get_local_version()
    print(f"Local file version: {version}")