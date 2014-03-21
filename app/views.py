from flask import render_template, flash, redirect, session, url_for, request, g
from flask import render_template
from app import  app, db
from myparser import parse
from forms import CommentForm
from models import User, Project, Comment, ROLE_USER, ROLE_ADMIN
from datetime import datetime
from censorLib import censor


@app.route('/')
@app.route('/index')
def index():
    allprojects = parse()
    currproj =  allprojects.getProject("HW0")
    return render_template("index.html",
        title = 'Home',
        project = currproj)

@app.route('/project/<name>')
def project(name):
	allprojects = parse()
	currproj = allprojects.getProject(name)
	return render_template("project.html", project = currproj)

@app.route('/comments/<name>', methods = ['GET', 'POST'])
def comments(name):
	allprojects = parse()
	currproj = allprojects.getProject(name)
	form = CommentForm()
	commentObj = db.session.query(Comment).filter(Comment.project_name == name)
	if form.validate_on_submit():
		c = Comment(user_name=form.username.data, content=censor(form.comment.data), project_name = name, timestamp = datetime.now())
		db.session.add(c)
		db.session.commit()
		flash("Comment successfully posted")
		return redirect('/comments/'+ name)
	return render_template("comments.html", project = currproj, form = form, commentData = commentObj)
