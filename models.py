from socketserver import StreamRequestHandler
import sqlite3
from os import path

ROOT = path.dirname(path.relpath((__file__)))

def create_post(name, content):
    con = sqlite3.connect(path.join(ROOT,' database.db'))