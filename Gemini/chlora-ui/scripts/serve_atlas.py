#!/usr/bin/env python3
"""Serve only this skill's design atlas on loopback."""
import argparse, functools, http.server, pathlib
parser=argparse.ArgumentParser()
parser.add_argument('--port',type=int,default=17869)
args=parser.parse_args()
directory=pathlib.Path(__file__).resolve().parents[1]/'assets/atlas'
handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(directory))
server=http.server.ThreadingHTTPServer(('127.0.0.1',args.port),handler)
print(f'Chlora UI atlas: http://127.0.0.1:{args.port}/index.html',flush=True)
server.serve_forever()
