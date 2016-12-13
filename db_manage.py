from reflookup.auth.models import *
import click


@click.group()
def menu_group():
    pass


@menu_group.command()
def create_db():
    db.create_all()


@menu_group.command()
def drop_db():
    db.drop_all()


@menu_group.command()
def new_user():
    mail = ''
    passwd = ''

    while mail == '' and passwd == '':
        mail = click.prompt('Email', type=str, default='', show_default=False)
        passwd = click.prompt('Password', type=str, default='',
                              show_default=False)

    scope = -1
    while scope != 0 and scope != 1:
        scope = click.prompt('Scope (0 - admin, 1 - client):', type=int,
                             default=1)

    c = User(mail, passwd, scope)
    db.session.add(c)
    db.session.commit()

    click.echo('Done!')


menu_dict = {
    'c': create_db,
    'd': drop_db,
    'a': new_user,
    'e': exit
}


@menu_group.command()
def interactive():
    click.echo(
        '''
Choose an option:
- (C)reate database.
- (D)rop database.
- (A)dd a new client.
- (E)xit
        '''
    )

    choice = click.prompt('Enter your choice:', type=str,
                          default='E').lower()
    menu_dict[choice]()


if __name__ == '__main__':
    menu_group()
