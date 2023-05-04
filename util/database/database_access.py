import psycopg2

class DatabaseAccess:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        
        self.connection = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

if __name__ == "__main__":
    print("balls")
    db_access = DatabaseAccess("lewdlocale_test2", "postgre", "", "localhost", "5432")
    print(db_access.connection.cursor())