import pymysql 
import os 
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
            host=os.getenv("AWS_HOST"),
            port=3306, # hm
            user=os.getenv("AWS_USER"),
            password= os.getenv("AWS_ACCESS_KEY_ID"),
            autocommit=True
        )

mycursor = conn.cursor()

def get_all(): 
    mycursor.execute("SELECT * FROM blurb_analysis")
    results = mycursor.fetchall()
    return results