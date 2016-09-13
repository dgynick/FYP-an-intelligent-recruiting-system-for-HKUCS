import os
from urllib.parse  import parse_qs, urlparse
from http.server  import BaseHTTPRequestHandler, HTTPServer
from MysqlConnection.Connector import loadAll
from MysqlConnection.Main import main, getSampleSize
from cgi import parse_header, parse_multipart
import json
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        parsed_url=urlparse(self.path)
        path=parsed_url.path
        if(path=="/" or path=="/index.html"):
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            f = open(os.path.join(__location__, 'index.html'),'rb')
            self.wfile.write(f.read())
            f.close()
        elif(path=="/index.js"):
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/javaScript')
            self.end_headers()
            # Send message back to client
            f = open(os.path.join(__location__, 'index.js'),'rb');
            self.wfile.write(f.read())
            f.close()
        elif(path=="/style.css"):
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/css')
            self.end_headers()
            # Send message back to client
            f = open(os.path.join(__location__, 'style.css'),'rb');
            self.wfile.write(f.read())
            f.close()
        elif(path=="/favicon.ico"):
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','image/x-icon')
            self.end_headers()
            # Send message back to client
            f = open(os.path.join(__location__, 'favicon.ico'),'rb');
            self.wfile.write(f.read())
            f.close()
        elif(path=="/tree.png"):
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','image/png')
            self.send_header("Cache-Control","no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")
            self.end_headers()
            # Send message back to client
            f = open(os.path.join(__location__, 'tree.png'),'rb');
            self.wfile.write(f.read())
            f.close()
        elif(path=="/treeRegression.png"):
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','image/png')
            self.send_header("Cache-Control","no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")
            self.end_headers()
            # Send message back to client
            f = open(os.path.join(__location__, 'treeRegression.png'),'rb');
            self.wfile.write(f.read())
            f.close()
        elif (path=="/loadData"):
            query_components = dict(qc.split("=") for qc in parsed_url.query.split("&"))
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            self.wfile.write(bytes(loadAll(str(query_components["year"])),"utf8"))
        return

  def do_POST(self):
        parsed_url=urlparse(self.path)
        path=parsed_url.path
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(
                    self.rfile.read(length),
                    keep_blank_values=1)
        else:
            postvars = {}
        # Send response status code
        if(path=="/train"):
            self.send_response(200)
            #self.queryString=urllib.parse.unquote(self.path.split('?',1)[1])
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            # Write content as utf-8 data
            model=str(postvars[b'model'][0].decode("utf8"))
            iv=[]
            for i in postvars[b'iv[]']:
                iv.append(int(i.decode("utf8"))+1)
            dv=int(postvars[b'dv'][0].decode("utf8"))+1
            result=main(iv,dv,model)
            self.wfile.write(bytes(json.dumps(result),"utf8"))
        elif path=="/getSampleSize":
            self.send_response(200)
            #self.queryString=urllib.parse.unquote(self.path.split('?',1)[1])
            # Send headers
            self.send_header('Content-type','text/html')
            self.end_headers()
            # Send message back to client
            # Write content as utf-8 data
            model=str(postvars[b'model'][0].decode("utf8"))
            iv=[]
            for i in postvars[b'iv[]']:
                iv.append(int(i.decode("utf8"))+1)
            dv=int(postvars[b'dv'][0].decode("utf8"))+1
            result=getSampleSize(iv,dv,model)
            self.wfile.write(bytes(json.dumps(result),"utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8083)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

run()