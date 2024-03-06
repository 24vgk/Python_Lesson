from sqlalchemy import insert, select, update, delete, MetaData, Table
from sqlalchemy.orm import Session

from Config_BD.Basemodul import engine


class SQL:
    # session = Session(engine)

    def __init__(self):
        self.engine = engine()
        metadate = MetaData()
        self.Users = Table('Users', metadate, autoload_replace=True, autoload_with=self.engine)

    def INSERT(self, user_id: int, first_name: str, user_name: str, is_admin: bool = False, is_block: bool = False):
        """
        Добавляет пользователей в БД users.
        :param user_id: int
        :param first_name: str
        :param user_name: str
        :param is_admin: bool
        :param is_block: bool
        """
        conn = self.engine.connect()
        ins = insert(self.Users).values(
            User_id=user_id,
            First_name=first_name,
            User_name=user_name,
            Is_admin=is_admin,
            Is_block=is_block
        )
        conn.execute(ins)
        conn.commit()
        self.engine.dispose()

    def UPDATE(self, name: str, User_id: int) -> None:
        """
        Метод меняет имя в БД
        :param name: str
        :return: None
        """
        conn = self.engine.connect()
        up = update(self.Users).where(self.Users.c.User_id == User_id).values(First_name=name)
        conn.execute(up)
        conn.commit()
        conn.close()
        self.engine.dispose()

    def SELECT(self, name: str) -> list:
        """
        """
        conn = self.engine.connect()
        up = select(self.Users).where(self.Users.c.First_name == name)
        re = conn.execute(up)
        result = re.fetchall()
        conn.commit()
        conn.close()
        self.engine.dispose()
        return result[0]


    def DELETE(self, name: str) -> None:
        """
        """
        conn = self.engine.connect()
        up = delete(self.Users).where(self.Users.c.First_name == name)
        re = conn.execute(up)
        conn.commit()
        conn.close()
        self.engine.dispose()


if __name__ == '__main__':
    sql = SQL()
    print(sql.SELECT('NEW_NAME'))