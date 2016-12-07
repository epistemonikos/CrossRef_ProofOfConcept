from reflookup.auth.models import *
import click


def create_db():
    db.create_all()


def delete_db():
    db.drop_all()


def new_user():
    mail = ''
    passwd = ''

    while mail == '' and passwd == '':
        mail = click.prompt('Email', type=str, default='', show_default=False)
        passwd = click.prompt('Password', type=str, default='', show_default=False)

    scope = -1
    while scope != 0 and scope != 1:
        scope = click.prompt('Scope (0 - admin, 1 - client):', type=int, default=1)

    c = User(mail, passwd, scope)
    db.session.add(c)
    db.session.commit()

    click.echo('Done!')


menu_dict = {
    'c': create_db,
    'd': delete_db,
    'a': new_user,
    'e': exit
}


def menu():
    click.echo(
        '''
Choose an option:
- (C)reate database.
- (D)elete database.
- (A)dd a new client.
- (E)xit
        '''
    )

    choice = click.prompt('Enter your choice:', type=str, default='E').lower()
    menu_dict[choice]()


if __name__ == '__main__':
    menu()
