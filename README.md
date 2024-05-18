# Similar Design Finder Service
The main task of this service is to provide the ability to conveniently and quickly search for appropriate examples of documentation on designing machine learning systems (ML System Design Doc) among hundreds of available options. This will allow users to find relevant examples that best match the specifics and requirements of their projects.


## Repository Contents

- [src](src) - source codes of the service
- [data](data) - data folder
    - [data/raw](data/raw) - source data (raw)
    - [data/processed](data/processed) - data after processing steps
- [.env.example](.env.example) - example .env file
- [.pre-commit-config.yaml](.pre-commit-config.yaml) - pre-commit config file

TODO:
- [tests](tests) - project tests
- [.github/workflows](.github/workflows) - CI/CD Pipelines

## Local Launch

- Create a .env file based on the example [.env.example](.env.example) if there any credentials.

- Launch using [docker-compose](https://docs.docker.com/compose/):
```
docker compose up -d --build
```

## Development

Recommended OS for development: Linux, macOS, WSL v2

### Environment Setup

- Install `python 3.11.*`. Recommended version: `3.11.7`
    - Recommended installation method: pyenv

        - Install pyenv using the [official instructions](https://github.com/pyenv/pyenv)

        - Install `python 3.11.7` and set the local version in the project root
        ```bash
        pyenv install 3.11.7
        pyenv local 3.11.7
        ```
        - A `.python-version` file should appear in the project folder, indicating the python version in use


    - Windows

        Install using the [official installer](https://www.python.org/downloads/)

    - Linux

        ```bash
        sudo apt install python3.11-dev
        ```

- Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
    - Linux, macOS, Windows (WSL)

        ```bash
        curl -sSL https://install.python-poetry.org | python3 -
        ```

    - Windows `powershell`

        ```powershell
        (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
        ```

- Ensure that poetry installs virtual environments within the project
    ```bash
    poetry config virtualenvs.in-project true
    ```

- Install dependencies
    ```
    poetry install
    ```

- Activate the virtual environment
    ```
    poetry shell
    ```

### Linters and Formatters

The project uses the linter and formatter [ruff](https://docs.astral.sh/ruff/). It is written in Rust, making it very fast.

Ruff should be automatically installed from `dev` dependencies when you install the project's dependencies.

- To lint your code, use the command

    ```bash
    ruff check <path>
    ```
    ```bash
    ruff check . # to check the entire directory
    ```

- To automatically fix some errors, use the command
    ```bash
    ruff check . --fix
    ```

- For automatic code formatting, use
    ```bash
    ruff format .
    ```

### Pre-commits

Before committing code, you must install pre-commits using the command

```bash
pre-commit install
```

Now, certain checks described in the [.pre-commit-config.yaml](.pre-commit-config.yaml) file will run on any commit.

You can also run pre-commits without making a commit using
```bash
pre-commit run # runs pre-commits on all staged files (i.e., after git add)
```
or
```bash
pre-commit run --all-files # runs pre-commits on all files
```
