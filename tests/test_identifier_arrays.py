from fastjsonschema import compile as compile_schema, JsonSchemaException
import jsonref as json
import pytest


def get_validator(base_folder):
    """ Generates the validator for this test suite.
    """
    schema = json.loads(
        """
        {
            "type": "array",
            "items": {
                "anyOf": [
                    { "$ref": "identifiers.json#/definitions/viaf" },
                    { "$ref": "identifiers.json#/definitions/researcherId" },
                    { "$ref": "identifiers.json#/definitions/isni" },
                    { "$ref": "identifiers.json#/definitions/orcid" }
                ]
            }
        }
        """,
        base_uri=(base_folder / 'registry.json').as_uri(),
    )
    return compile_schema(schema)


@pytest.mark.parametrize(
    "obj,expected",
    [
        (
            [
                {"kind": "orcid", "id": "0000-0002-4553-9697"},
                {"kind": "researcherId", "id": "I-4625-2012"},
            ],
            True,
        ),
        ([{"kind": "orcid", "id": "0000-0002-4553-9697"}], True),
        ([{"kind": "researcherId", "id": "I-4625-2012"}], True),
        ([], True),
    ]
)
def test_multiid(registration_schema_folder, obj, expected):
    """
    Test a definition in our JSON schema using some examples.

    Examples take the form of a Python object and the expected
    validation outcome (i.e. True or False)

    Parameters:
        registration_schema_folder - handled by pytest fixtures
        obj - the object to test
        expected - whether the object should pass validation or not
    """
    validator = get_validator(registration_schema_folder)
    try:
        validator(obj)
        if not expected:
            raise AssertionError(f"Object {obj} unexpectedly validated")
    except JsonSchemaException as err:
        if expected:
            raise AssertionError(
                f"Object {obj} failed to validate. Error is {err.message}"
            )
