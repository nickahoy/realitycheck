import click
from .src import estimate_transaction_fees

@click.command()
@click.option('--price',
              type=click.INT,
              prompt='How much is the property?',
              help='The asking price of the property.')
@click.option('--is_new',
              type=click.BOOL,
              prompt='Is this a new property? (Y/N)',
              help='Whether the property is new. This affects tax calculations.')
def cli(price, is_new):
    d = estimate_transaction_fees(price, is_new)
    click.echo(d)