from utils.logger import logger
from repository.database import Database

ADD_NOTIFICATION = """
INSERT INTO {table_name} (NAME, "TYPE", TOKEN, CHAT_ID) VALUES(?, ?, ?, ?);
"""

GET_NOTIFICATION = """
SELECT NAME, "TYPE", TOKEN, CHAT_ID FROM {table_name};
"""

UPDATE_NOTIFICATION = """
UPDATE
	{table_name}
SET
	"TYPE" =?,
	TOKEN =?,
	CHAT_ID =?
WHERE
	NAME =?;	
"""

DELETE_NOTIFICATION = """
DELETE FROM {table_name} WHERE NAME=?;
"""

class Notification():

    def __init__(self, name: str, type: str, token: str, chatId: str) -> None:
        self.name = name
        self.type = type
        self.token = token
        self.chatId = chatId
        pass

    def to_tuple(self) -> tuple:
        return (self.name, self.type, self.token, self.chatId)

    def to_json(self) -> dict: 
        return {
            "name": self.name,
            "type": self.type,
            "token": self.token,
            "cahtId": self.chatId,
        }

class Notifications(Database):

    def __init__(self) -> None:
        super().__init__()

    def add_notification(self, notification: Notification) -> bool:
        query = self.query(ADD_NOTIFICATION, self.notification_table_name)
        logger.info("Add notifictaion")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, notification.to_tuple())
            conn.commit()

        return cursor.rowcount == 1
    
    def get_notification(self) -> list[Notification]:
        query = self.query(GET_NOTIFICATION, self.notification_table_name)
        logger.info("Get notifications")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        return list(map(lambda x: Notification(*x), result))
  

    def update_notification(self, name: str, notification: Notification) -> bool:
        query = self.query(UPDATE_NOTIFICATION, self.notification_table_name)
        logger.info(f"Update notification for: [{name}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*notification.to_tuple(), name))
            conn.commit()

        return cursor.rowcount == 1


    def delete_notification(self, name: str) -> bool:
        query = self.query(DELETE_NOTIFICATION, self.notification_table_name)
        logger.info(f"Delete notification for: [{name}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [name])
            conn.commit()

        return cursor.rowcount == 1  
