from pathlib import Path

from fastjsonschema import compile as compile_schema, JsonSchemaException
import jsonref as json
import pytest

SCHEMA_FOLDER = Path("../schema.igsn.org/json/registration/0.1/").absolute()


def get_validator(base_folder, schema_file, defn):
    "Generate a schema for some definition fragment."
    schema = json.loads(
        f'{{ "$ref": "#/definitions/{defn}" }}',
        base_uri=(base_folder / schema_file).as_uri(),
    )
    return compile_schema(schema)


def check(validator, obj, expected):
    """ Test a definition in our JSON schema using some examples

    Examples take the form of a Python object and the expected
    validation outcome (i.e. True or False)

    Parameters:
        validator - A validation instance
        obj - the object to check
        expected - True if the object should validate, False
            otherwise
    """
    try:
        validator(obj)
        if not expected:
            raise AssertionError(f"Object {obj} unexpectedly validated")
    except JsonSchemaException as err:
        if expected:
            raise AssertionError(
                f"Object {obj} failed to validate. Error is {err.message()}"
            )


@pytest.mark.parametrize(
    "obj,expected",
    [
        ({"kind": "orcid", "id": "0234-4568-7895-1655"}, True),
        ({"kind": "orcid", "id": "0234 4568 7895 1655"}, True),
        ({"kind": "orcid", "id": "0234-XXXXD-7895-1655"}, False),
        ({"kind": "orcid", "id": "0234-4581-7895-1655-4561"}, False),
        ({"kind": "orcid", "id": "http://orcid.com/0234-4568-7895-1655"}, True),
        ({"kind": "orcid", "id": "http://orcid.com/0234 4568 7895 1655"}, False),
        ({"kind": "orcid", "id": "http://orcid.com/0234-XXXX-7895-1655"}, False),
        ({"kind": "orcid", "id": "http://orcid.com/0234-4581-7895-1655-4561"}, False),
        ({"kind": "orcid", "id": "https://orcid.com/0234-4568-7895-1655"}, True),
        ({"kind": "orcid", "id": "https://orcid.com/0234 4568 7895 1655"}, False),
        ({"kind": "orcid", "id": "https://orcid.com/0234-XXXX-7895-1655"}, False),
        ({"kind": "orcid", "id": "https://orcid.com/0234-4581-7895-1655-4561"}, False),
    ],
)
def test_orcids(registration_schema_folder, obj, expected):
    validator = get_validator(registration_schema_folder, "identifiers.json", "orcid")
    check(validator, obj, expected)


@pytest.mark.parametrize(
    "obj,expected",
    [
        ({"kind": "researcherId", "id": "X-1238-2347"}, True),
        ({"kind": "researcherId", "id": "S-4816-2540"}, True),
        ({"kind": "researcherID", "id": "S-4816-2540"}, False),
        ({"kind": "researcherId", "id": "S-XXXX-7895-1655"}, False),
        ({"kind": "researcherId", "id": "S-4581-7895-1655"}, False),
        ({"kind": "researcherId", "id": "lorem ipsum"}, False)
    ]
)
def test_researcherId(registration_schema_folder, obj, expected):
    validator = get_validator(
        registration_schema_folder, "identifiers.json", "researcherId"
    )
    check(validator, obj, expected)
