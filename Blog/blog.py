import webapp2
import jinja2
import logging
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *arg, **karg):
        self.response.out.write(*arg, **karg)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.get_ten_records()
        
    def get_ten_records(self):
        blogs = db.GqlQuery("SELECT * FROM Blog")
        self.render("main.html", blogs=blogs.run())
        

class AddNewBlog(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render("new_form.html", output='')    
        



class SaveBlog(Handler):
 
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            blog = Blog(subject=subject, content=content)
            blog.put()

        self.redirect("/")
        #self.response.out.write("Success: " + subject + " " + content)
        
    def save_to_database(self, input_data):
        self.response.out.write("YES")


class PageHandler(Handler):
    def get(self, post_id):
        logging.info(dir(Blog))
        p = Blog.get_by_id(int(post_id))
        p = [p,]
        self.response.headers['Content-Type'] = 'text/html'
        self.render("main.html", blogs=p) 
        

app = webapp2.WSGIApplication([('/', MainPage),('/new_form', AddNewBlog),
                               ('/save_blog', SaveBlog), ('/blog/([0-9]+)', PageHandler)], debug=True)