# Script to run unit tests with coverage

# Tests must be run from this folder
cd ..

# Remove previous results
coverage erase

# Run tests with coverage
python -m coverage run --source="src/extractor/." src/tests/test_app.py

# Generate coverage report including only application under test
coverage report --include="src/extractor/*.py"

# Generate XML report for SonarQube
coverage xml -o src/tests/cobertura.xml