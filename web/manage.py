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

    db.session.add(AuthUser(email="kanom@opf.com", name='Kanom Nom',
                            password=generate_password_hash('0000', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Kanom+Nom&background=ed5aeb&color=fff'))
    
    db.session.add(Privateblog(message="Join me on a drink tonight at 11 pm.",
                               avatar_url='https://ui-avatars.com/api/?name=Kanom+nom&background=ed5aeb&color=fff',
                               owner_id=1))

    db.session.add(AuthUser(email="mushu@opf.com", name='Mushu Hamster',
                            password=generate_password_hash('0000', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Mushu+Hamster&background=ed5a89&color=fff'))
    
    db.session.add(Privateblog(message="I'll randomize one of you to touch my body, if you subscribe to me.",
                               avatar_url='https://ui-avatars.com/api/?name=Mushu+Hamster&background=ed5a89&color=fff',
                               owner_id=2))
    
    db.session.add(Privateblog(message="Come see my cat in my room.",
                               avatar_url='https://ui-avatars.com/api/?name=Catter+kitty&background=5aedde&color=fff',
                               owner_id=3))
    
    db.session.add(AuthUser(email="cat@opf.com", name='Catt Kitty ',
                            password=generate_password_hash('0000', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Catter+Kitty&background=5aedde&color=fff'))
    
    db.session.add(Privateblog(message="I'm free to night. I can be your cat meow~.",
                               avatar_url='https://ui-avatars.com/api/?name=Catter+kitty&background=5aedde&color=fff',
                               owner_id=3))
    
    db.session.add(AuthUser(email="tea_mach@opf.com", name='Ulong loogtang',
                            password=generate_password_hash('0000', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Ulong+loogtang&background=ed5aeb&color=fff'))
    
    db.session.add(Privateblog(message="I ate six bananas and it felt so good",
                               avatar_url='https://ui-avatars.com/api/?name=Ulong+loogtang&background=ed5aeb&color=fff',
                               owner_id=4))
    
    db.session.add(AuthUser(email="three_3@opf.com", name='Sangsom BlueRebel',
                            password=generate_password_hash('0000', method='sha256'),
                            avatar_url='https://ui-avatars.com/api/?name=Sangsom+Kawazak&background=ed5aeb&color=fff'))
    
    db.session.add(Privateblog(message="Sub for pics",
                               avatar_url='https://ui-avatars.com/api/?name=Sangsom+Kawazak&background=ed5aeb&color=fff',
                               owner_id=5))
    
    db.session.commit()


if __name__ == "__main__":
    cli()