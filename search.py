#!/usr/bin/python
# -*- encoding: utf-8 -*-
#Ptyhon script to search documents on couchDB
#Using lib: couchdb-python
#Lib Url: http://code.google.com/p/couchdb-python/

from couchdb import *
import argparse
import sys
import time

if __name__ == "__main__":
	
    #create the parser
    parser = argparse.ArgumentParser(description='search documents on CouchDB')
        
	#add the arguments
    parser.add_argument('-s', '--server',
        help='server of couchdb Ex.: http://localhost:5984/',
        default="http://localhost:5984/")
        
    parser.add_argument('-d', '--database', help='set the database, default: test',
        default="test")
        
    parser.add_argument('-v', '--view', help='siew name Ex.: title_id')

    parser.add_argument('-p', '--path',
        help='path of url couch for view, default: _design/couchdb/_view/',
        default="_design/couchdb/_view/")

    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
        default=sys.stdout,
        help='the file where the JSON output should be written'
             ' (default: write to stdout)', metavar='output.json')

    parser.add_argument('-l', '--length', help='view name Ex.: title_id',
        action='store_true')

    parser.add_argument(
        '-k', '--key', help='key for search Ex.: S2176-94512010000500019',
        default="")

    parser.add_argument('-b', '--bulk', help='save like CouchDB Bulk',
        action='store_true')

    parser.add_argument("-t", "--time", type=float,
        help="Delay between returned docs", default=0.0)
        
    # parse the command line
    args = parser.parse_args()
    
    server = Server(args.server)
    db = server[args.database]
    
    if args.view:
        if args.length:
            results = db.view(args.path + args.view)
            args.output.write(str(results.total_rows) + '\n')
            sys.exit(1)
            
        if args.bulk:
            args.output.write('{ "docs" : ')
            args.output.write('\n[')
            
        endline = ',\n' if args.bulk else '\n'

        if args.key:
            for row in db.view(args.path + args.view, None, key=args.key):
                doc = db.get(row.id)
                print row.id
                args.output.write(json.encode(doc).encode('utf-8') + endline)
                time.sleep(args.time)
        else:
            for row in db.view(args.path + args.view):
                doc = db.get(row.id)
                print row.id
                args.output.write(json.encode(doc).encode('utf-8') + endline)
                time.sleep(args.time)

        if args.bulk:
            args.output.write(']')
            args.output.write('\n}')
        args.output.close()
        
    else:

        if args.length:
            results = db.view('_all_docs')
            args.output.write(str(results.total_rows) + '\n')
            sys.exit(1)
            
        if args.bulk:
            args.output.write('{ "docs" : ')
            args.output.write('\n[')

        endline = ',\n' if args.bulk else '\n'

        for row in db.view('_all_docs', include_docs=True):
                doc = db.get(row.id)
                print row.id
                args.output.write(json.encode(doc).encode('utf-8') + endline)
                time.sleep(args.time)

        if args.bulk:
            args.output.write(']')
            args.output.write('\n}')
        args.output.close()