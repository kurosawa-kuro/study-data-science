import click

from model import User, Role, RoleType
from session import SessionLocal
import auth


@click.group()
def cli():
    pass

@cli.command()
@click.argument("user_name")
@click.option("-r", "--role", "role_type", type=click.Choice([rt.value for rt in RoleType]), required=True)
@click.option("-p", "--password", required=True)
def create_user(user_name, role_type, password):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.username == user_name).first()
        if user:
            raise Exception(f"{user_name} is already exists.")

        role = session.query(Role).filter(Role.name == role_type).first()
        if role is None:
            raise Exception(f"{role_type} is not exists.")

        user = User(
            username=user_name,
            hashed_password=auth.hash(password),
            age=20,
            roles=[role],
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    finally:
        session.close()

@cli.command()
@click.argument("user_name", type=str)
def delete_user(user_name):
    with SessionLocal() as session:
        # userの重複確認
        user = session.query(User).filter(User.username == user_name).first()
        if user is None:
            raise Exception(f"{user_name} is already exists.")
        session.delete(user)
        session.commit()

if __name__ == "__main__":
    cli()
