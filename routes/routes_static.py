from bottle import get, static_file, error

@get('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='static')

@get('/about')
def about():
    return static_file('about.html', root='static') 

@get("/static/<filepath:path>")
def html(filepath):
    return static_file(filepath, root = "static")

@error(404)
def error404(error):
    return static_file('404.html', root='static')