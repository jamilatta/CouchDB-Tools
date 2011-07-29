#!/usr/bin/python
#Ptyhon script to delete documents on couchDB
#Using lib: couchdb-python
#Url: http://code.google.com/p/couchdb-python/

from couchdb import *
import argparse


if __name__ == "__main__":

    #create the parser
    parser = argparse.ArgumentParser(
        description='Delete all documents by view')
        
    #add the arguments
    parser.add_argument(
        '-v', '--view', help='View name Ex.: title_id', default="")

    parser.add_argument(
        '-k', '--key', help='Key for search Ex.: S2176-94512010000500019',
        default="")

    parser.add_argument(
        '-s', '--server', help='Server of couchdb Ex.: http://localhost:5984/',
        default="http://localhost:5984/")
        
    parser.add_argument(
        '-d', '--database', help='Set the database, default: test', default="test")
        
    parser.add_argument(
        '-id', '--identify', help='The id of document', default="")

    parser.add_argument(
        '-in', '--input',
        help='Imput file with keys to delete, default: input.txt')

    parser.add_argument(
        '-p', '--path',
        help='Path of url couch for view, default: _design/couchdb/_view/',
        default="_design/couchdb/_view/")


    # parse the command line
    args = parser.parse_args()

    print "---+--- ACCESS SERVER: " + args.server
    server = Server(args.server)
    print "---+--- ACCESS DATABASE: " + args.database
    db = server[args.database]

    #Views
    if args.view:
        if args.key:
            for row in db.view(args.path + args.view, None, key=args.key):
                doc = db.get(row.id)
                print "---+--- DELETE DOCUMENT ID: " + row.id
                db.delete(doc)
        elif args.input:
            for f in open(args.input, 'r'):
                for row in db.view(args.path + args.view, None, key=f.strip()):
                    doc = db.get(row.id)
                    print "---+--- DELETE DOCUMENT ID: " + doc.id
                    db.delete(doc)
        else:
            for row in db.view(args.path + args.view):
                doc = db.get(row.id)
                print "---+--- DELETE DOCUMENT ID: " + row.id
                db.delete(doc)
    #ID
    if args.identify:
        doc = db.get(args.identify)
        print "---+--- DELETE DOCUMENT ID: " + doc.id
        db.delete(doc)
        