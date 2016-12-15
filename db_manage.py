from reflookup.auth.models import *
import click


@click.group()
def menu_group():
    pass


@menu_group.command(help='Create the SQLite DB.')
def create_db():
    db.create_all()


@menu_group.command(help='Drop the SQLite DB.')
def drop_db():
    db.drop_all()


@menu_group.command(help='Create a new user.')
@click.option('--email', prompt='Email', help='Login email for new user.')
@click.option('--password', prompt='Password', help='Login password for new user.')
@click.option('--scope', prompt='Scope', help='User access scope (0 or 1)', default=1)
def new_user(email, password, scope):

    c = User(email, password, scope)
    db.session.add(c)
    db.session.commit()

    token = c.create_token()

    click.echo('Done!')
    click.echo('Access token for {}: {}'.format(email, token))


@menu_group.command(help='Create a new access token for an existing user.')
@click.option('--email', prompt='Email', help='The login email.')
@click.option('--password', prompt='Password', help='The login password.')
def renew_access_token(email, password):

    user = User.login(email, password)

    if user is None:
        click.echo('Wrong credentials.')
        exit(-1)

    token = user.create_token()
    click.echo('Access token for {}: {}'.format(email, token))

if __name__ == '__main__':
    menu_group()
