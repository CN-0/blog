from flask import Flask, render_template, request, session, make_response, redirect, url_for
from src.models.user import User
from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post


app = Flask(__name__)
app.secret_key = "jose"


@app.route('/')
def home_template():
    return render_template('index.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
    return make_response(my_blogs())


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return make_response(my_blogs())


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def my_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()
    postsno = 0
    for blog in blogs:
        blog = Blog.from_mongo(blog._id)
        posts = blog.get_posts()
        postsno = postsno + len(posts)

    return render_template("my_blog.html", blogs=blogs, user=user, postsno=postsno)


@app.route('/all_blogs')
def all_blogs():
    blogs = User.get_all_blogs()
    return render_template("all_blogs.html", blogs=blogs)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('my_new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(my_blogs(user._id))


@app.route('/delete/<string:blog_id>')
def delete(blog_id):
    blog = Blog.from_mongo(blog_id)
    blog.delete_blog()
    return make_response(my_blogs())


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('my_posts.html', posts=posts, blog=blog)


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':  # when first this method is accessed it will be a GET request,
        return render_template('my_new_post.html', blog_id=blog_id)    # so it redirects to new_post.html
    else:
        title = request.form['title']    # new_post.html action is also this method only so it redirects to this method,
        content = request.form['content']    # but this time with a POST request
        user = User.get_by_email(session['email'])  # so when second time this method is accessed a new post is created

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))


@app.route('/edit_profile', methods=['POST', 'GET'])
def edit_profile():
    if request.method == 'GET':
        return render_template('edit_profile.html')
    else:
        email = request.form['email']
        present_email = session['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if email != present_email:
            return render_template('editing_profile.html', message=1)
        else:
            user = User.get_by_email(email)
            password = user.password
            if password != password1:
                return render_template('editing_profile.html', message=2)
            else:
                user.password = password2
                user.change_in_mongo()
                return render_template('editing_profile.html', message=3)


@app.route('/all_posts/<string:blog_id>')
def all_blog_posts(blog_id):
    blog = Blog.blog_from_mongo(blog_id)
    id = blog['_id']
    posts = Post.from_blog(id)

    return render_template('all_posts.html', posts=posts, blog=blog)


@app.route('/search', methods=['POST'])
def search():
    search = request.form['q']
    blogs = User.get_all_blogs()
    search_results = []
    for blog in blogs:
        if blog['author'] == search:
            search_results.append(blog)
    return render_template('search_results.html', blogs=search_results)


@app.route('/logout')
def to_logout():
    session.clear()
    return redirect(url_for('home_template'))


if __name__ == '__main__':
    app.run(port=4995)
