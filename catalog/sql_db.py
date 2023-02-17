#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:50:34 2022

@author: dineshverma
"""

from dataclasses import dataclass, asdict
import json
import os

# import pymongo
import sqlite3 as sql
from catalog.errors import MissingArgumentException


@dataclass
class GericSQLEntry:
    _id: int

    @classmethod
    def from_json(cls, entry: str):
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

    @classmethod
    def check_table_command(cls):
        table_name = cls.__name__
        return f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name={table_name}"

    @classmethod
    def entry_retrieve_command(cls, field="_id"):
        return f"SELECT * FROM {cls.__name__} WHERE {field}=?"

    @classmethod
    def entry_delete_command(cls, field="_id"):
        return f"DELETE FROM {cls.__name__} WHERE {field}=?"

    @classmethod
    def class_purge_command(cls):
        return f"DELETE FROM {cls.__name__}"

    @classmethod
    def class_fetchall_command(cls):
        return f"SELECT * FROM {cls.__name__}"

    @classmethod
    def create_table_command(cls):
        table_name = cls.__name__
        return f"create table  if not exists {table_name} (_id INTEGER PRIMARY KEY AUTOINCREMENT, {cls.create_table_suffix()})"

    @classmethod
    def entry_create_command(cls):
        return f"INSERT into {cls.__name__} {cls.create_entry_suffix()}"

    def entry_update_command(self):
        return f"UPDATE {self.__class__.__name__} SET {self.entry_update_suffix()} where _id = {self._id}"

    @classmethod
    def create_table_suffix(cls):
        raise NotImplementedError("")

    @classmethod
    def create_entry_suffix(cls):
        raise NotImplementedError("")

    @classmethod
    def update_entry_suffix(cls):
        raise NotImplementedError("")


@dataclass
class UserEntry(GericSQLEntry):
    name: str
    password: str
    email: str

    @classmethod
    def from_dict(cls, d):
        for key in ["name", "password", "email"]:
            value = d.get(key, None)
            if value is None:
                raise MissingArgumentException(key, "UserEntry")
        return UserEntry(d.get("_id", -1), d["name"], d["password"], d["email"])

    @classmethod
    def create_table_suffix(cls):
        return "name TEXT UNIQUE NOT NULL, email TEXT NOT NULL, password TEXT"

    @classmethod
    def create_entry_suffix(cls):
        return "(name, password, email) values (?,?,?)"

    def to_tuple_create(self):
        return self.name, self.password, self.email

    def entry_update_suffix(self):
        return "name=?, password=?, email=?"


class GenericSQLDBase:
    def __init__(self, sqdb_file, this_cls):
        self.sqdb_file = sqdb_file
        self.this_cls = this_cls
        # Check if the path to sqdb_file exists and if not create it
        abspath = os.path.abspath(sqdb_file)
        if not os.path.exists(abspath):
            if not os.path.exists(os.path.dirname(abspath)):
                os.makedirs(os.path.dirname(abspath))
                # Check if the table exists, otherwise create the tables
        with sql.connect(sqdb_file) as con:
            con.execute(self.this_cls.create_table_command())
            con.commit()

        # At the end of this, the table exists and is available

    def create(self, entry):
        with sql.connect(self.sqdb_file) as con:
            cur = con.cursor()
            # Start from here - fixing
            cur.execute(self.this_cls.entry_create_command(), entry.to_tuple_create())
            answer = cur.lastrowid
            con.commit()
            return answer

    def retrieve(self, identity: int):
        with sql.connect(self.sqdb_file) as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute(self.this_cls.entry_retrieve_command(), (identity,))
            elem = cur.fetchall()[0]
            if elem is not None:
                item = self.this_cls.from_dict(dict(elem))
                return item
            return None

    def search(self, field: str, value):
        with sql.connect(self.sqdb_file) as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute(self.this_cls.entry_retrieve_command(field), (value,))
            elems = cur.fetchall()
            items = [self.this_cls.from_dict(dict(e)) for e in elems]
            return items

    def update(self, identity: int, entry):
        with sql.connect(self.sqdb_file) as con:
            cur = con.cursor()
            cur.execute(entry.entry_update_command(), entry.to_tuple_create())
            con.commit()

    def delete(self, identity):
        with sql.connect(self.sqdb_file) as con:
            cur = con.cursor()
            cur.execute(self.this_cls.entry_delete_command(), (identity,))
            con.commit()

    def purge(self):
        with sql.connect(self.sqdb_file) as con:
            cur = con.cursor()
            cur.execute(self.this_cls.class_purge_command())
            con.commit()

    # This should be replaced with an iterator
    def get_all(self):
        with sql.connect(self.sqdb_file) as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute(self.this_cls.class_fetchall_command())
            elems = cur.fetchall()
            items = [self.this_cls.from_dict(dict(e)) for e in elems]
            return items


class UserSQLDBase(GenericSQLDBase):
    def __init__(self, sqdb_file):
        super().__init__(sqdb_file, UserEntry)
