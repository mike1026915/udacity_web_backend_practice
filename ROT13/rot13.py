import webapp2
import jinja2
import os

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

class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render("main.html", output='') 
 

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        input_data = self.request.get("text")
        self.render("main.html", output=self.rot13(input_data))     
        
    def rot13(self, input_data):
        new_data = []
        for c in input_data:
            if c.isalpha():
                base_number = ord('a') if c.islower() else ord('A')
                c_num = ord(c) - base_number
                c_num += 13
                c_num %= 26
                new_data.append(chr(c_num+base_number))
            else:
                new_data.append(c)
        return ''.join(new_data)

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)