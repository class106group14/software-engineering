import sae
from QAapp import wsgi
application=sae.create_wsgi_app(wsgi.application)