from flask import render_template
from app.blog import blog

@blog.route('/')
def blog_list():
    return render_template('blog/blog_list.html')
