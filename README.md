# jsonschema-testing

Playground for IGSN 2040 JSON Schemas

### Installation

We're using [pipenv]() to manage dependencies - the following should get you going

```bash
$ pip install pipenv  # if you don't already have pipenv
$ pipenv install
```

If you want the development dependencies then add a `--dev` flag (i.e. 
`pipenv install --dev`) - this will install a few optional but heavy packages 
(like ipykernel, lxml and pandas) we're using to play with data.

If you want to use the environment in a jupyter notebook, then you need to 
install the dev dependencies and then create a Jupyter kernel reference as follows:

```bash
$ pipenv install --dev  # if you haven't already done this
$ pipenv shell
(jsonschema-testing) $ python -m ipykernel install --user --name 'igsn-jsonschema-testing'
(jsonschema-testing) $ exit
$ jupyter lab  # or notebook
```

Now you should be able to load the `igsn-jsonschema-testing` kernel in jupyter. 
Note we're assuming you have jupyter installed in some system environment.

### Locations of things

We're basically keeping all our schemas in the folder structure as we want to publish them.

```
schema.igsn.org/
    /vXXX           # XML schemas and definitions
    /json/vXXX      # JSON schemas & definitions
```

This structure is likely to be subject to change (i.e. it might be nice to have an XML tag as well as a json tag).