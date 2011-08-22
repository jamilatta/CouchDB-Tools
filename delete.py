#!/usr/bin/python
# -*- encoding: utf-8 -*-
#Ptyhon script to delete documents on couchDB
#Using lib: couchdb-python
#Lib Url: http://code.google.com/p/couchdb-python/

from couchdb import *
import argparse

if __name__ == "__main__":

    #create the parser
    parser = argparse.ArgumentParser(
        description='delete documents on CouchDB')
        
    #add the arguments
    parser.add_argument(
        '-v', '--view', help='view name Ex.: title_id', default="")

    parser.add_argument(
        '-k', '--key', help='key for search Ex.: S2176-94512010000500019',
        default="")

    parser.add_argument(
        '-s', '--server', help='server of couchdb Ex.: http://localhost:5984/',
        default="http://localhost:5984/")
        
    parser.add_argument(
        '-d', '--database', help='set the database, default: test', default="test")
        
    parser.add_argument(
        '-id', '--identify', help='the id of document', default="")

    parser.add_argument(
        '-in', '--input',
        help='input file with keys to delete, default: input.txt')

    parser.add_argument(
        '-p', '--path',
        help='path of url couch for view, default: _design/couchdb/_view/',
        default="_design/couchdb/_view/")


    # parse the command line
    args = parser.parse_args()

    server = Server(args.server)
    db = server[args.database]

    #Views
    if args.view:
        if args.key:
            for row in db.view(args.path + args.view, None, key=args.key):
                doc = db.get(row.id)
                db.delete(doc)
        elif args.input:
            for f in open(args.input, 'r'):
                for row in db.view(args.path + args.view, None, key=f.strip()):
                    doc = db.get(row.id)
                    db.delete(doc)
        else:
            for row in db.view(args.path + args.view):
                doc = db.get(row.id)
                db.delete(doc)
    #ID
    if args.identify:
        doc = db.get(args.identify)
        db.delete(doc)
    
    
    
        
