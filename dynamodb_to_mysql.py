import boto3
from db_config import func_real_db
from mysql.connector import Error

# AWS DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('real_estate_market_data')

# MySQL real_db setup
def connect_mysql_real_db():
    try:
        real_db = func_real_db()
        if real_db.is_connected():
            db_info = real_db.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            return real_db
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def close_mysql_real_db(real_db):
    if real_db.is_connected():
        real_db.close()
        print("MySQL real_db is closed")

def fetch_data_from_dynamodb():
    try:
        response = table.scan()
        data = response['Items']
        return data
    except Exception as e:
        print("Error fetching data from DynamoDB", e)
        return None

def update_mysql_table(data):
    real_db = connect_mysql_real_db()
    if real_db is None:
        return
    try:
        cursor = real_db.cursor()

        for item in data:
            # Customize the following query and data as per your MySQL table structure and the data from DynamoDB
            query = """INSERT INTO real_estate_market_data (date, avg_sqm_price_eur, avg_sqm_price_huf,
                               one_million_huf_to_eur) 
                        VALUES (%s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE 
                        avg_sqm_price_huf = VALUES(avg_sqm_price_huf),
                        avg_sqm_price_eur = VALUES(avg_sqm_price_eur), 
                        one_million_huf_to_eur = VALUES(one_million_huf_to_eur)"""
            cursor.execute(query, (item['date'], item['avg_sqm_price_eur'], item['avg_sqm_price_huf'], item['one_million_huf_to_eur']))
        real_db.commit()
        print("Data updated in MySQL table successfully")
        
    except Error as e:
        print("Error updating MySQL table", e)
    finally:
        cursor.close()
        close_mysql_real_db(real_db)
        return True
def fetch_data_from_mysqldb():
    real_db = connect_mysql_real_db()    
    if real_db is None:
        return
    try:
        cursor = real_db.cursor()
        query = "SELECT date, avg_sqm_price_huf, avg_sqm_price_eur, one_million_huf_to_eur FROM real_estate_market_data ORDER BY date"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print("Error updating MySQL table", e)
    finally:
        cursor.close()
        close_mysql_real_db(real_db)

def main():
    data = fetch_data_from_dynamodb()
    if data:
        try:
            update_mysql_table(data)
            print("1")
            return True  # Indicate success
        except Exception as e:
            print(f"Error during update: {e}")
            print("2")
            return False  # Indicate failure
    else:
        print("No data fetched from DynamoDB")
        print("3")
        return False 
if __name__ == "__main__":
    main()
