from pathlib import Path

import pytest

# Get the root directory of the project
ROOT = Path(__file__).parent.parent.absolute()

@pytest.fixture()
def registration_schema_folder():
    "Get the location of the given schema folder."
    print(f'Root at {ROOT}')
    return ROOT / 'schema.igsn.org/json/registration/0.1/'

@pytest.fixture()
def geosample_schema_folder():
    return ROOT / 'schema.igsn.org/json/description/geoSample/0.1/'
