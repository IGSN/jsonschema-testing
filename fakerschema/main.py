"""Entrypoint for fakerschema CLI."""

import click
import jsonref as json

from .generator import generate


@click.command()
@click.option("-l", "--lines", is_flag=True, help="Output in JSONLines format")
@click.argument("schema", type=click.File(mode="r", encoding="utf-8", errors="strict"))
def main(schema, number, lines):
    """Main script entry."""
    output = {
        'schema': json.load(schema),
        "format": "JSONlines" if lines else "JSON",
        "n_objects": number,
    }

    click.echo(json.dumps(output))


if __name__ == "__main__":
    main()  # pylint: disable=E1120
