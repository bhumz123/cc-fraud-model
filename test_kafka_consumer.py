import json
import pandas as pd
import numpy as np
import psycopg2
from kafka import KafkaConsumer
from json import loads
from api.rfm import rfm_calculate
from api.Model import model

existing_df= pd.read_csv('Existing_dataset_transactions.csv').reset_index(drop=True)
# final_df = pd.DataFrame()
# make different functions for each operation here
try:
    # Establish connection to the PostgreSQL database
    connection = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='Noida@120',
        database='amex_db'
    )
    cursor = connection.cursor()
    # Connection is successful
    print("Connection to PostgreSQL successful")
    # Close the connection
except (psycopg2.Error, Exception) as error:
    print("Error while connecting to PostgreSQL:", error)

def update_db(prediction_value, key):
    if prediction_value==0:
        new_prediction_value = "NotFraud"
    else:
        new_prediction_value="Fraud"
    # Execute the PostgreSQL update query
    update_query = "UPDATE demo SET predicted_value = %s WHERE event_key = %s;"
    cursor.execute(update_query, (new_prediction_value,key))
    query_2="update demo set status= %s WHERE event_key = %s;"
    cursor.execute(query_2, ("PROCESSED", key))
    connection.commit()
    print("Prediction result added to Database")

def converting_dtype(df):
    # Assuming `df` is your DataFrame
    columns_int64 = ['city_pop', 'trans_month', 'Weekday', 'category_food_dining', 'category_gas_transport',
                     'category_grocery_net', 'category_grocery_pos', 'category_health_fitness', 'category_home',
                     'category_kids_pets', 'category_misc_net', 'category_misc_pos', 'category_personal_care',
                     'category_shopping_net', 'category_shopping_pos', 'category_travel']
    columns_float64 = [col for col in df.columns if col not in columns_int64]
    # Convert specified columns to int64 data type
    df[columns_int64] = df[columns_int64].astype('int64')
    # Convert remaining columns to float64 data type
    df[columns_float64] = df[columns_float64].astype('float64')
    # Print the updated DataFrame
    return df


def encode_category(df):
    category = df["category"].iloc[0]
    # Iterate over each category column in the existing DataFrame
    for column in existing_df.columns:
        if column.startswith('category'):
            if column[9:]== category :
                df[column] = 1
            else:
                df[column] = 0
            # df[column] = np.where(df[column] == category, 1, 0)
    return df


def preprocess_data(data):
    event_key = data.pop('event_key')
    existing_df.loc[len(existing_df)] = data
    existing_df.reset_index(drop=True)
    # Converting json format to dataframe
    df = pd.DataFrame([data]).reset_index(drop=True)
    # Removing unwanted columns
    df.drop(['first','last','job','dob','street','city','zip','trans_num','state','unix_time','gender'],axis=1,inplace=True)
    # extracting useful columns
    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['trans_month'] = df['trans_date_trans_time'].dt.month
    df['trans_day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
    df['Weekday'] = (df['trans_day_of_week'] <= 5).astype(int)
    df.drop('trans_day_of_week',axis=1,inplace=True)
    # Deriving Category
    e_df = encode_category(df)
    e_df['is_fraud']=0
    # Performing rfm on incoming transaction
    c_result = rfm_calculate.get_customer_spending_behaviour_features(existing_df[existing_df["cc_num"].values == e_df["cc_num"].values])
    m_result = rfm_calculate.merchant_risk_window(existing_df, c_result,df["merchant"])
    category_result = rfm_calculate.category_risk_window(existing_df, m_result, df["category"])
    n_df = pd.DataFrame(category_result).transpose()
    n_df = n_df.sort_values('trans_date_trans_time').reset_index(drop=True)
    # Distance b/w merchant and customer
    n_df['distance']=n_df.apply(lambda row:rfm_calculate.calculate_distance(row["cust_locn"], row["merchant_locn"]),axis=1)
    # Dropping columns which are not required for model
    n_df.drop(['trans_date_trans_time','cc_num','merchant',"category","merchant_locn","cust_locn","Frequency_7DAY_WINDOW",
               "Frequency_30DAY_WINDOW","Monetary_30DAY_WINDOW","merchant_Trnscn_count7Day","merchant_Trnscn_count30Day",
               "merchant_Risk_Score30Day","category_Trnscn_count7Day","category_Risk_Score7Day","category_Trnscn_count30Day",
               "category_Risk_Score30Day"],axis=1,inplace=True)
    final_df=converting_dtype(n_df)
    # print(final_df.info())
    result=int(model.combined_predctns(final_df))
    update_db(result,event_key)


def sample_consumer():
    consumer = KafkaConsumer('amex-source', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest',
                             enable_auto_commit=True, group_id='my-group',
                             value_deserializer=lambda x: loads(x.decode('utf-8')))

    for message in consumer:
        message = message.value
        print(message)
        preprocess_data(message)
        # print(message['event_key'])

if __name__ == "__main__":
    print("Consuming events from Kafka")
    sample_consumer()