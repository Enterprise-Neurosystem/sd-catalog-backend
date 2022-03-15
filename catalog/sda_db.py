#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:50:34 2022

@author: dineshverma
"""

from dataclasses import dataclass, asdict
import json
#import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from catalog.errors import MissingArgumentException

#ID_FIELD must match the variable name in GenericEntry
ID_FIELD = "_id"          

@dataclass
class GenericEntry:
    _id: str 
    
    @classmethod
    def from_dict(cls, d):
        return cls(d)
        
    @classmethod
    def from_json(cls, entry:str):
        return cls.from_dict(json.loads(entry))
    
    def to_dict(self):
        this_dict = asdict(self)
        new_dict = dict((k, this_dict[k]) for k in this_dict.keys() if this_dict[k])
        return new_dict
    
    def to_json(self):
        this_dict = self.to_dict()
        return json.dumps(this_dict)
    
    def set_identity(self, identity):
        self._id = identity
        
class Converter:
    def entry2dict(self, entry) -> dict:
        return entry.to_dict()
    
    def entry2json(self, entry) -> str:
        return json.dumps(self.entry2dict(entry))
    
    def json2entry(self, json_string:str) -> GenericEntry:
        return self.dict2entry(json.loads(json_string))
    
    def dict2entry(self, this_dict:dict) -> GenericEntry:
        pass
    
    def get_sql_create_statement(self):
        pass
    
    def get_sql_table_name(self):
        pass
        

                

@dataclass
class SelfDescribingEntry(GenericEntry):
    data_uri: str
    scope: str
    data_type: str = None 
    metadata:str = None 

    @classmethod
    def from_dict(cls, this_dict):
        _id = this_dict.get('_id', None)
        if isinstance(_id, ObjectId):
            _id = str(_id)
        data_uri = this_dict.get('data_uri', None)
        scope = this_dict.get('scope', None)
        subtype = this_dict.get('data_type', None)
        metadata = this_dict.get('metadata', None)
        if data_uri is None: 
            raise MissingArgumentException("data_uri", "SelfDescribingentry")
        if scope is None: 
            raise MissingArgumentException("scope", "SelfDescribingentry")
        
        return SelfDescribingEntry(_id, data_uri, scope, subtype, metadata)
    
    
    
class SelfDescribingEntryConverter(Converter):
    
    def dict2entry(self, this_dict:dict) -> GenericEntry:
        return SelfDescribingEntry.from_dict(this_dict)
    
            
    
class MongoDBase:
    
    def __init__(self, converter, db_url=None, db_name = "sda_catalog", collection_name = "sda_docs"):
        self.db_url = db_url
        self.db_name = db_name
        self.collection_name = collection_name
        self.converter = converter
        
    def get_client(self):
        if self.db_url is None:
            return MongoClient()
        else:
            return MongoClient(self.db_url)
        
    
    def get_collection(self, client: MongoClient):
        this_db = client[self.db_name]
        return this_db[self.collection_name]
    
    def make_identity(self, identity):
        #return {'_id': '"'+identity+'"'}
        return ObjectId(identity)
            
        
    def create(self, entry:GenericEntry):
        post_id = None
        with self.get_client() as client: 
            docs = self.get_collection(client)
            post_id = docs.insert_one(self.converter.entry2dict(entry))
            return str(post_id.inserted_id)
    
    def retrieve(self, identity):
        with self.get_client() as client: 
            docs = self.get_collection(client)
            this_id = self.make_identity(identity)
            elem = docs.find_one(this_id)
            if elem is not None:
                item = self.converter.dict2entry(elem)
                item.set_identity(identity)
                return item
            return None
            
        
    def update(self, identity, entry:GenericEntry):
        with self.get_client() as client: 
            docs = self.get_collection(client)
            id = self.make_identity(identity)
            update_key = {'_id': id}
            update_value = { '$set': self.converter.entry2dict(entry)}
            docs.update_one(update_key, update_value)
           
    
    def delete(self, identity):
        with self.get_client() as client: 
            
            docs = self.get_collection(client)
            id = self.make_identity(identity)
            docs.delete_one({'_id': id})
            
            
    def purge(self):
        with self.get_client() as client:
            docs = self.get_collection(client)
            docs.delete_many({})
    
     #This should be replaced with an iterator 
    def get_all(self):
        with self.get_client() as client: 
             docs = self.get_collection(client)
             dict_list = docs.find()
             elements = [self.converter.dict2entry(elem) for elem in dict_list]
             return elements
             

        
        
    
    
            
            
            
        
        
    
    



