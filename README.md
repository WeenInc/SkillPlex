# SkillPlex

SkillPlex is a project for [brief description of your project].

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

2. Install the package and its dependencies in editable mode:
```bash
pip install -e .
pip install pytest python-dotenv
```

3. Create a `.env` file in the root directory of the project and add your environment variables:
```
OPENAI_API_KEY=your_openai_api_key
DB_URL=your_db_url  # optional
SKILLPLEX_ENDPOINT=your_skillplex_endpoint
```

## Testing

To run the tests for this project, follow these steps:

1. Ensure you're in the project root directory and your virtual environment is activated.

2. Run all tests:
```bash
pytest
```

3. To run tests specifically from `tests/tests_skillplex.py`:
```bash
pytest tests/tests_skillplex.py
```

These commands will automatically load the environment variables from your `.env` file before running the tests.
