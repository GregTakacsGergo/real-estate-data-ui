from db_config import func_real_db


class ApartmentDataDatabase:
    def __init__(self):
        self.real_db = func_real_db()
        self.my_cursor = self.real_db.cursor()

    def create_table(self):
        self.connection = self.real_db
        try:
            self.my_cursor.execute("USE real_db")  
            self.my_cursor.execute("""
                CREATE TABLE IF NOT EXISTS real_estate_market_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                universal_sqm_price_huf DECIMAL(10, 2),
                universal_sqm_price_eur DECIMAL(10, 2),
                one_million_huf_to_eur DECIMAL(10, 2))""")
            self.connection.commit()
        except Exception as e:
            print(f"Error creating table: {e}")


    def check_existing_data(self, date):
        query = "SELECT * FROM real_estate_market_data WHERE date = %s"
        self.my_cursor.execute(query, (date, ))
        result = self.my_cursor.fetchall()
        return len(result) > 0

    def insert_data_db(self, date, universal_sqm_price_huf, universal_sqm_price_eur, one_million_huf_to_eur):
        if not self.check_existing_data(date):
            SQL_statement = """INSERT INTO real_estate_market_data (date, universal_sqm_price_huf, universal_sqm_price_eur,
                               one_million_huf_to_eur) VALUES (%s, %s, %s, %s)"""
            self.my_cursor.execute(SQL_statement, (date, universal_sqm_price_huf, universal_sqm_price_eur, one_million_huf_to_eur))
            self.real_db.commit()
        else:
            print("data already exists in the database")
    
    def fetch_data_from_db(self):
        query = "SELECT date, universal_sqm_price_huf, universal_sqm_price_eur, one_million_huf_to_eur FROM real_estate_market_data ORDER BY date ASC"
        self.my_cursor.execute(query)
        result = self.my_cursor.fetchall()
        return result
    
    def close(self):
        self.my_cursor.close()  
        self.connection.close()  
def main():
    handler = ApartmentDataDatabase()
    handler.create_table()
    handler.close()
   
if __name__ == "__main__":
    main()
