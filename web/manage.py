from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.authuser import AuthUser,Privateblog

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():

    db.session.add(AuthUser(email="test0@gmail.com", name='Test 0',
                            password=generate_password_hash('0000', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Test+0&background=83ee03&color=fff'))
    
    db.session.add(Privateblog(name='Test 0', email="test0@gmail.com", message="test 0 - 1",
                               avatar_url='https://ui-avatars.com/api/?name=Test+0&background=83ee03&color=fff',
                               owner_id=1))

    db.session.add(AuthUser(email="test1@gmail.com", name='Test 1',
                            password=generate_password_hash('1111', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Test+1&background=83ee03&color=fff'))
    
    db.session.add(Privateblog(name='Test 1', email="test1@gmail.com", message="test 1 - 1",
                               avatar_url='https://ui-avatars.com/api/?name=Test+1&background=83ee03&color=fff',
                               owner_id=2))
    
    
    db.session.add(AuthUser(email="test2@gmail.com", name='Test 2',
                            password=generate_password_hash('2222', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Test+2&background=83ee03&color=fff'))
    
    db.session.add(Privateblog(name='Test 2', email="test2@gmail.com", message="test 2 - 1",
                               avatar_url='https://ui-avatars.com/api/?name=Test+2&background=83ee03&color=fff',
                               owner_id=3))
    
    
    db.session.commit()


if __name__ == "__main__":
    cli()