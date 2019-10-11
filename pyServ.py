import cgi

form = b'''
<html>
    <head>
        <title>Hello User!</title>
    </head>
    <body>
        <form method="post">
            <label>Hello</label>
            <br />
            <input type=checkbox name="name" id="name" value="Bob">Bob<br />
            <input type=checkbox name="name" id="name" value="Steve">Steve<br />
            <input type="submit" value="Go">
        </form>
    </body>
</html>
'''

def app(environ, start_response):
    html = form
    getlist = ""
    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        fh = open("./tmpStore",'w')

        try:
            for n in post['name']:
                print(n)
                getlist += str(n.value) + "," 
                html += b'Hello, ' + n.value + '!' + "<br />"
        except TypeError:
            getlist += str(post['name'].value)

        getlist= getlist.rstrip(",")
        fh.write(getlist)  
        fh.close()
        print(getlist)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [html]

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8080, app)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')
