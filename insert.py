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
        description='Insert documents on CouchDB')
        
    #add the arguments
    parser.add_argument(
        'file_name', metavar='INPUT.(json)', help='json file to read',
        type=argparse.FileType('r'))
        
    parser.add_argument(
        '-s', '--server', help='Server of couchdb Ex.: http://localhost:5984/',
        default="http://localhost:5984/")
        
    parser.add_argument(
        '-d', '--database', help='Set the database, default: test', default="test")        

    parser.add_argument(
        '-l', '--log', type=argparse.FileType('w'), default=sys.stdout,
       help='log the inserted documents (CouchDB format)', metavar='log.json')
        
    # parse the command line
    args = parser.parse_args()
    
    server = Server(args.server)
    db = server[args.database]
    
    doc = dict(eval(args.file_name.read()))
    
    db.save(doc)