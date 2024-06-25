# About

This is simple python database server/client library on TCP.

# Installation

## Server

```bash
pip install requests colorama keyboard socket base64 argparse
```

## Client

```bash
pip install socket base64
```
# Usage

## Server

```bash
python server.py <arg> <value> ...
```

Arguments:
| Argument | Description                    | Default   |
| -------- | ------------------------------ | --------- |
| -p port  | Port                           | 3304      |
| -r recv  | Receive buffer size (bytes)    | 1024      |
| -f file  | Database file (.xml)           | db.xml    |
| -k pwd   | Password                       | PDB       |
| -l bool  | Logging (true/false)           | false     |
| -s host  | Host                           | localhost |
| -c max   | Max clients                    | 100       |

## Client

Setup

```python
import client

db = PlexusClient( host:str, port:int, password:str, recv:int )
```

Communication with server

```python
# Commands available at section "Client Commands"

# Execute command on server, without returning value. 
db.query( command:str )

# Execute command on server, with returning value.
data = db.exquery( command:str )

# Ping server, returns True if available, or False.
db.ping()
```


# Additional

## Special Response

| Response                     | Description                |
| ---------------------------- | -------------------------- |
| <pdb.SUCCESS>                | Operation completed. 		|
| <pdb.ERR_REQUEST_MISS>       | Server miss the request.   |
| <pdb.ERR_WRONG_PWD>          | Wrong password.            |


## Client Commands

| Command         | Arguments              | Description                                | Returns				   |
| --------------- | ---------------------- | ------------------------------------------ | ------------------------ |
| CREATE_GROUP    | item                   | Creates group in database.                 | `None`
| REMOVE_GROUP    | item                   | Removes group from database.               | `None`
| WRITE           | group item             | Creates new item in group.                 | `None`
| ERASE           | group item             | Removes item from group.                   | `None`
| ITEM_COUNT      | group                  | Gets total count of items in group.        | `value` **:int**
| GROUP_COUNT     |                        | Gets total count of groups in database.    | `value` **:int**
| GROUPS		  |                        | Gets all groups from database.             | `value` **:str**
| ITEMS           | group                  | Gets all items from group.                 | `value` **:str**
| CHECK           | group item             | Checks presence of item in group.          | `True/False` **:bool**
| SETATTRIB       | group item attr value  | Set attribute value of item in group.      | `None`
| GETATTRIB       | group item attr        | Get attribute value of item from group.    | `value` **:str**


(C) 2024 h1ntefr
