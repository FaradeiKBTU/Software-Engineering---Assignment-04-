import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from smart_campus.server import create_server

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
print("Open http://127.0.0.1:%d  (Ctrl+C to stop)" % port)
create_server(port).serve_forever()
