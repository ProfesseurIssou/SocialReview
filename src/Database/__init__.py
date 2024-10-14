"""
    Différent types de données utilisés dans le projet
"""
from sqlite3worker import Sqlite3Worker
from dataclasses import dataclass
from datetime import datetime, date
from typing import Union

import os
import ast

@dataclass
class Base_Platform:
    id: int
    name: str
    base_url: str
@dataclass
class Base_Repport_Tag:
    id: int
    tag_name: str
@dataclass
class Base_Repport_Account:
    id: int
    platform_id: int
    account_id: str
    account_name: str
    account_url: str
@dataclass
class Base_Repport:
    id: int
    account_id: int
    repport_date: date
    repport_tag_id: int
    repport_text: str




class Database:
    database_file: str
    db: Sqlite3Worker

    def __init__(self) -> None:
        """
            - Open the database, create the tables if not exists
        """
        self.database_file = "database.db"

        if not os.path.exists(self.database_file):
            self.__Generate_Database()
        self.db = Sqlite3Worker(self.database_file)
        return
            

    def __Generate_Database(self) -> None:
        """
            - Generate the database
            - If the database already exists, remove it
        """
        if os.path.exists(self.database_file):
            os.remove(self.database_file)

        db: Sqlite3Worker = Sqlite3Worker(self.database_file)

        # Create the tables
        db.execute("CREATE TABLE IF NOT EXISTS platform (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, base_url TEXT NOT NULL);")
        db.execute("CREATE TABLE IF NOT EXISTS repport_tag (id INTEGER PRIMARY KEY AUTOINCREMENT, tag_name TEXT NOT NULL UNIQUE);")
        db.execute("CREATE TABLE IF NOT EXISTS repport_account (id INTEGER PRIMARY KEY AUTOINCREMENT, platform_id INTEGER REFERENCES platform (id) ON DELETE CASCADE, account_id TEXT NOT NULL, account_name TEXT NOT NULL, account_url TEXT NOT NULL);")
        db.execute("CREATE TABLE IF NOT EXISTS repport (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER REFERENCES account (id) ON DELETE CASCADE, repport_date TEXT NOT NULL, repport_tag_id INTEGER REFERENCES tag (id) ON DELETE CASCADE, repport_text TEXT NOT NULL);")

        # Insert the default platforms
        db.execute("INSERT INTO platform (name) VALUES ('twitter');")
        db.execute("INSERT INTO platform (name) VALUES ('meta');")
        db.execute("INSERT INTO platform (name) VALUES ('discord');")
        
        db.close()
        return

    ### PLATFORM ###
    def Platform_GetAll(self) -> list[Base_Platform]:
        """
            Get all the platforms
            Return:
                list[Base_Platform]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, name, base_url FROM platform;")
        return [Base_Platform(id=result[0], name=result[1], base_url=result[2]) for result in results]
    def Platform_GetBy_ID(self, id: int) -> Union[Base_Platform, None]:
        """
            Get the platform by id
            Params:
                id: int
            Return:
                Base_Platform or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, name, base_url FROM platform WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Platform(id=result[0], name=result[1], base_url=result[2])
    def Platform_GetBy_Name(self, name: str) -> Union[Base_Platform, None]:
        """
            Get the platform by name
            Params:
                name: str
            Return:
                Base_Platform or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, name, base_url FROM platform WHERE name = ?;", [name])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Platform(id=result[0], name=result[1], base_url=result[2])
    ################

    ### REPPORT_TAG ###
    def RepportTag_GetAll(self) -> list[Base_Repport_Tag]:
        """
            Get all the repport tags
            Return:
                list[Base_Repport_Tag]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, tag_name FROM repport_tag;")
        return [Base_Repport_Tag(id=result[0], tag_name=result[1]) for result in results]
    def RepportTag_GetBy_ID(self, id: int) -> Union[Base_Repport_Tag, None]:
        """
            Get the repport tag by id
            Params:
                id: int
            Return:
                Base_Repport_Tag or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, tag_name FROM repport_tag WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Repport_Tag(id=result[0], tag_name=result[1])
    def RepportTag_GetBy_Name(self, tag_name: str) -> Union[Base_Repport_Tag, None]:
        """
            Get the repport tag by name
            Params:
                tag_name: str
            Return:
                Base_Repport_Tag or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, tag_name FROM repport_tag WHERE tag_name = ?;", [tag_name])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Repport_Tag(id=result[0], tag_name=result[1])
    
    def RepportTag_Insert(self, tag_name: str) -> None:
        """
            Insert the repport tag
            Params:
                tag_name: str
        """
        self.db.execute("INSERT INTO repport_tag (tag_name) VALUES (?);", [tag_name])
        return
    ####################

    ### REPPORT_ACCOUNT ###
    def RepportAccount_GetAll(self) -> list[Base_Repport_Account]:
        """
            Get all the repport accounts
            Return:
                list[Base_Repport_Account]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, platform_id, account_id, account_name, account_url FROM repport_account;")
        return [Base_Repport_Account(id=result[0], platform_id=result[1], account_id=result[2], account_name=result[3], account_url=result[4]) for result in results]
    def RepportAccount_GetBy_ID(self, id: int) -> Union[Base_Repport_Account, None]:
        """
            Get the repport account by id
            Params:
                id: int
            Return:
                Base_Repport_Account or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, platform_id, account_id, account_name, account_url FROM repport_account WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Repport_Account(id=result[0], platform_id=result[1], account_id=result[2], account_name=result[3], account_url=result[4])
    def RepportAccount_GetBy_AccountID(self, account_id: str) -> Union[Base_Repport_Account, None]:
        """
            Get the repport account by account id
            Params:
                account_id: str
            Return:
                Base_Repport_Account or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, platform_id, account_id, account_name, account_url FROM repport_account WHERE account_id = ?;", [account_id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Repport_Account(id=result[0], platform_id=result[1], account_id=result[2], account_name=result[3], account_url=result[4])
    
    def RepportAccount_Insert(self, platform_id: int, account_id: str, account_name: str, account_url: str) -> None:
        """
            Insert the repport account
            Params:
                platform_id: int
                account_id: str
                account_name: str
                account_url: str
        """
        self.db.execute("INSERT INTO repport_account (platform_id, account_id, account_name, account_url) VALUES (?, ?, ?, ?);", [platform_id, account_id, account_name, account_url])
        return
    #####################

    ### REPPORT ###
    def Repport_GetAll(self) -> list[Base_Repport]:
        """
            Get all the repports
            Return:
                list[Base_Repport]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, repport_date, repport_tag_id, repport_text FROM repport;")
        return [Base_Repport(id=result[0], account_id=result[1], repport_date=datetime.strptime(result[2], "%Y-%m-%d").date(), repport_tag_id=result[3], repport_text=result[4]) for result in results]
    def Repport_GetBy_ID(self, id: int) -> Union[Base_Repport, None]:
        """
            Get the repport by id
            Params:
                id: int
            Return:
                Base_Repport or None
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, repport_date, repport_tag_id, repport_text FROM repport WHERE id = ?;", [id])
        if results == []:
            return None
        result: tuple = results[0]
        return Base_Repport(id=result[0], account_id=result[1], repport_date=datetime.strptime(result[2], "%Y-%m-%d").date(), repport_tag_id=result[3], repport_text=result[4])
    def Repport_GetBy_AccountID(self, account_id: int) -> list[Base_Repport]:
        """
            Get the repport by account id
            Params:
                account_id: int
            Return:
                list[Base_Repport]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, repport_date, repport_tag_id, repport_text FROM repport WHERE account_id = ?;", [account_id])
        return [Base_Repport(id=result[0], account_id=result[1], repport_date=datetime.strptime(result[2], "%Y-%m-%d").date(), repport_tag_id=result[3], repport_text=result[4]) for result in results]
    def Repport_GetBy_TagID(self, tag_id: int) -> list[Base_Repport]:
        """
            Get the repport by tag id
            Params:
                tag_id: int
            Return:
                list[Base_Repport]
        """
        results: list[list[tuple]] = self.db.execute("SELECT id, account_id, repport_date, repport_tag_id, repport_text FROM repport WHERE repport_tag_id = ?;", [tag_id])
        return [Base_Repport(id=result[0], account_id=result[1], repport_date=datetime.strptime(result[2], "%Y-%m-%d").date(), repport_tag_id=result[3], repport_text=result[4]) for result in results]
    
    def Repport_Insert(self, account_id: int, repport_date: date, repport_tag_id: int, repport_text: str) -> None:
        """
            Insert the repport
            Params:
                account_id: int
                repport_date: date
                repport_tag_id: int
                repport_text: str
        """
        self.db.execute("INSERT INTO repport (account_id, repport_date, repport_tag_id, repport_text) VALUES (?, ?, ?, ?);", [account_id, repport_date.strftime("%Y-%m-%d"), repport_tag_id, repport_text])
        return
    #################
