import sqlite3 as lite
import sys

con = None

con = lite.connect('ideabank.db')
cur = con.cursor();

cur.execute("CREATE TABLE tags( id integer primary key,tag text)");
cur.execute("CREATE TABLE ideas( id integer primary key, title text, description text)");
cur.execute("CREATE TABLE ideatags( iid integer REFERENCES ideas(id), tid integer REFERENCES tags(id) )");
