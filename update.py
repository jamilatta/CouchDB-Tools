#!/usr/bin/python
# -*- encoding: utf-8 -*-
#Ptyhon script to update documents on couchDB
#Using lib: couchdb-python
#Lib Url: http://code.google.com/p/couchdb-python/

from couchdb import *
import argparse
import sys

if __name__ == "__main__":

    #create the parser
    parser = argparse.ArgumentParser(
        description='update documents on CouchDB')

    #add the arguments
    parser.add_argument(
        'file_name', metavar='INPUT.(json)', help='json file to read',
        type=argparse.FileType('r'))
        
    parser.add_argument(
        '-s', '--server', help='server of couchdb Ex.: http://localhost:5984/',
        default="http://localhost:5984/")

    parser.add_argument(
        '-d', '--database', help='set the database, default: test', default="test")

    parser.add_argument(
        '-l', '--log', type=argparse.FileType('w'), default=sys.stdout,
       help='Log the inserted documents (CouchDB format)', metavar='log.json')
       
    # parse the command line
    args = parser.parse_args()

    server = Server(args.server)
    db = server[args.database]
    
    for l in args.file_name.readlines():
        ldict = dict(eval(l))
        try:
           print db.save(ldict)
        except Exception, e:
           args.log.write('{"Erro":"' + str(e) + '"},\n')