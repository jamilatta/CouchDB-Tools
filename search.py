#!/usr/bin/python
#Ptyhon script to search documents on couchDB
#Using lib: couchdb-python
#Lib Url: http://code.google.com/p/couchdb-python/

from couchdb import *
import argparse
import sys

if __name__ == "__main__":
	
    #create the parser
    parser = argparse.ArgumentParser(
        description='Search documents on couchDB')
        
	#add the arguments
    parser.add_argument(
        '-s', '--server', help='Server of couchdb Ex.: http://localhost:5984/',
        default="http://localhost:5984/")
        
    parser.add_argument(
        '-d', '--database', help='Set the database, default: test', default="test")        
        
    parser.add_argument(
        '-v', '--view', help='View name Ex.: title_id', default="")        	

    parser.add_argument(
        '-p', '--path',
        help='Path of url couch for view, default: _design/couchdb/_view/',
        default="_design/couchdb/_view/")

    parser.add_argument(
        '-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
       help='the file where the JSON output should be written'
             ' (default: write to stdout)', metavar='output.json')

    parser.add_argument(
        '-l', '--length', help='View name Ex.: title_id', action='store_true')

    parser.add_argument(
        '-k', '--key', help='Key for search Ex.: S2176-94512010000500019',
        default="")
        
    # parse the command line
    args = parser.parse_args()
    
    server = Server(args.server)
    db = server[args.database]
    
    if args.view:
        if args.length:
            results = db.view(args.path + args.view, None, key=args.key)
            args.output.write(str(results.total_rows) + '\n')
            sys.exit()

    if args.view:
        args.output.write('{ "docs" : ')
        args.output.write('\n[\n')
        
        for row in db.view(args.path + args.view, None, key=args.key):
            doc = db.get(row.id)
            args.output.write(json.encode(doc).encode('utf-8') + ',\n')
            
        args.output.write('\n]')
        args.output.write('\n}')
        args.output.close()