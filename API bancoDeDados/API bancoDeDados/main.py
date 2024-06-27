import pprint
from connector import MySQLDatabase

if __name__ == '__main__':
    print('runing')
    
    try:
        db = MyS
        print(f"Starting the connection...\nStatus: {db.conn.is_connected()}")
        
    
    except ConnectionError as err:
        raise f"Error during the connection. Message: {err}"
    
    
    
    new_instance = {
                    "id": 129,
                    "name": "estadodois",
                    "abbr": "VR",
                    "created_at":"2024-06-17",
                    "updated_at":"2024-06-17"
                    }
    
db.delete_instance('states', 'id', [88] )
        
        
