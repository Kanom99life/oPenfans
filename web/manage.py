from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.contact import Contact
from app.models.blogEntry import BlogEntry
from app.models.authuser import AuthUser, PrivateContact

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        Contact(firstname='สมชาย', lastname='ทรงแบด', phone='081-111-1111'))


    db.session.add(AuthUser(email="kanom1@gmail.com", name='Kanom1 Nom',
                            password=generate_password_hash('1111', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Kanom+Nom&background=83ee03&color=fff'))

    db.session.add(AuthUser(email="kanom2@gmail.com", name='Kanom2 Nom',
                            password=generate_password_hash('1111', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Kanom2+Nom&background=83ee03&color=fff'))
    
    db.session.add(
       PrivateContact(firstname='ส้มโอ', lastname='โอเค',
                      phone='081-111-1112', owner_id=1))

   
    db.session.commit()


if __name__ == "__main__":
    cli()