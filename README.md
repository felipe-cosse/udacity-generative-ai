# Udacity Generative AI Exercises

This repository uses one root Python 3.13 virtual environment for all course notebooks and exercises.

## Quick Start

```sh
uv venv --no-project --python 3.13.12 .venv
uv pip install --python .venv/bin/python -r "Generative AI Fundamentals/Exercise/requirements-macos.txt"
.venv/bin/python -m jupyter lab
```

The environment includes JupyterLab, LiteLLM, PyTorch with Apple MPS support, Transformers, datasets, evaluation libraries, PEFT, and TRL. Open any course notebook and select the root `.venv` Python kernel.

Exercises that call a model require an API key. Export it only in your terminal before starting JupyterLab:

```sh
export OPENAI_API_KEY="your-key"
.venv/bin/python -m jupyter lab
```

Never save credentials in a notebook or commit them to Git. For a shell inside the environment, run `source .venv/bin/activate`.
