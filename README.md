# jsonschema-testing

Playground for IGSN 2040 JSON Schemas 

[![Build Status](https://travis-ci.com/IGSN/jsonschema-testing.svg?branch=master)](https://travis-ci.com/IGSN/jsonschema-testing) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/559a4d6f385e4b70b276124e466863e8)](https://www.codacy.com/gh/IGSN/jsonschema-testing?utm_source=github.com&utm_medium=referral&utm_content=IGSN/jsonschema-testing&utm_campaign=Badge_Grade)

## Installation

We're using [pipenv](https://pipenv.readthedocs.io/en/latest/) to manage dependencies - the following should get you going

```bash
pip install pipenv  # if you don't already have pipenv
pipenv install
```

If you want the development dependencies then add a `--dev` flag (i.e. 
`pipenv install --dev`) - this will install a few optional but heavy packages 
(like ipykernel, lxml and pandas) we're using to play with data.

### Running tests

Tests are run with pytest - these are mostly sanity tests to check that the schemas are behaving as we expect. 
To run them, do

```bash
$ pipenv run pytest
```

in the root directory

### Jupyter kernel

If you want to use the environment in a jupyter notebook, then you need to 
install the dev dependencies and then create a Jupyter kernel reference as follows:

```bash
$ pipenv install --dev  # if you haven't already done this
$ pipenv shell
Launching subshell in virtual environment…
(jsonschema-testing) $ python -m ipykernel install --user --name 'igsn-jsonschema-testing'
Installed kernelspec igsn-jsonschema-testing in /path/to/jupyter/kernels/igsn-jsonschema-testing
(jsonschema-testing) $ exit
$ jupyter lab  # or notebook
```

Now you should be able to load the `igsn-jsonschema-testing` kernel in jupyter. 
Note we're assuming you have jupyter installed in some system environment.

## Finding your way around

We're basically keeping all our schemas in the folder structure as we want to publish them. This is an attempt
to stay consistent with the [metadata](https://github.com/igsn/metadata) repository naming scheme

    schema.igsn.org/
        /xml                               # XML schemas and definitions
            registration/$version/...
            description/$version/...
        /json                              # JSON schemas & definitions
            registration/$version/...      # Core registry metadata
            description/
                geoSamples/$version        # ...an example of a descriptive schema
                bioSamples/$version        # ...another community descritive schema
                materialSamples/$version
                ...

This structure is likely to be subject to change! Version numbers being used are semVer but with only major and 
minor increments (i.e. `$major.$minor`). 

## JSON Schema/JSON-LD info and philosophy

We're using the [draft-07](https://json-schema.org/specification-links.html#draft-7) version of JSON Schema as 
that's the one that is implemented by most validators. However there are some nice things in the newer draft 
([2019-09](https://json-schema.org/draft/2019-09/release-notes.html) - like better keywords, `$anchor` references 
and vocabulary support through JSON MetaSchema) that we should keep our eyes on.

We're aiming to incorporate JSON-LD into our definitions to constrain keywords and support linked data workflows, 
however it's still useful to have a canonical document representation (essentially in JSON-LD terms this would 
be a graph + a framing) since this is still the way most developers think. Hence we're using JSON Schema to constrain
representations for now.

Note that we won't generate a 1:1 relationship between the XML schemas and the JSON representation - this is 
undesireable for a number of reasons (not least being that XML-dressed-as-JSON is a pain to work with), while
also being impossible to do canonically (i.e. we're going to make some editing decisions anyway so why not go the
whole hog?).
