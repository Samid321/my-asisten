from flask import Flask, render_template, redirect, request, url_for,jsonify
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
cek=CKEditor(app)
# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

class my_form(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    subtitle=StringField('subtitle',validators=[DataRequired()])
    body = CKEditorField(
        'body',
       validators=[DataRequired()]
    )
    your_name=StringField('your_name',validators=[DataRequired()])
    image=StringField('image',validators=[DataRequired()])
   

with app.app_context():
    db.create_all()
WTF_CSRF_SECRET_KEY = '3321'
@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    data=db.session.execute(db.select(BlogPost)).scalars().all()
    
    return render_template("index.html", all_posts=data)

@app.route('/show_post/<int:post_id>')
def show_post(post_id):
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalars().first()
    return render_template("post.html", post=requested_post)

@app.route('/edit<int:post_id>',methods=['POST', 'GET'])
def edit(post_id):
    form=my_form()
    
    
    request_post=db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalars().first()
    
    if form.validate_on_submit():
        request_post.title = form.title.data
        request_post.subtitle = form.subtitle.data
        request_post.body = form.body.data
        request_post.author = form.your_name.data
        request_post.img_url = form.image.data
        db.session.commit()
        return redirect(url_for('show_post',post_id=post_id))
    
       
    return render_template ('edit.html', post=request_post,form=form,)  

# TODO: add_new_post() to create a new blog post

# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_delete=db.session.execute(db.select(BlogPost).where(BlogPost.id==post_id)).scalars().first()
    db.session.delete(post_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route('/make_new_content', methods=['POST','GET'])
def make_content():

    form = my_form()
    try:
        if form.validate_on_submit():

            new = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                date=date.today().strftime("%B %d, %Y"),
                body=form.body.data,
                author=form.your_name.data,
                img_url=form.image.data
            )

            db.session.add(new)
            db.session.commit()
            print('New content added to database')

            return redirect('/')
    except Exception as e:
        print('Error adding content to database:', e)
    return render_template('make-post.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5003)