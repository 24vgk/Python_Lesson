from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from Config_BD.Basemodul import engine, users


class SQL:
    session = Session(engine)

    def INSERT(self, user_id: int, first_name: str, user_name: str, is_admin: bool = False, is_block: bool = False):
        """
        Добавляет пользователей в БД users.
        :param user_id: int
        :param first_name: str
        :param user_name: str
        :param is_admin: bool
        :param is_block: bool
        """
        ins = insert(users).values(
            User_id=user_id,
            First_name=first_name,
            User_name=user_name,
            Is_admin=is_admin,
            Is_block=is_block
        )
        self.session.execute(ins)
        self.session.commit()


if __name__ == '__main__':
    sql = SQL()
    sql.INSERT('Andrey', 11111, True)