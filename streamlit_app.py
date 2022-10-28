import streamlit
import pandas
import snowflake.connector
from urllib.error import URLError
import requests

streamlit.title('My New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruits_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruits_list= my_fruits_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruits_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruits_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normailized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normailized
  
  
  
streamlit.header('Fruitvice Adice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    #streamlit.write('The user entered ', fruit_choice)
    back_from_function = get_fruityvice_data(fruit_choice)
    #streamlit.text(fruityvice_response.json())
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()


def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT *  from FRUIT_LOAD_LIST")
    return my_cur.fetchall()

if streamlit.button("The fruit load list contains:"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row=get_fruit_load_list()
  streamlit.dataframe(my_data_row)

# Allow end user to add fruit to the list     

def insert_row_snowflake(fruit_toadd):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values (fruit_toadd)")
    return ('Thanks for adding ', fruit_toadd)
    

fruit_toadd = streamlit.text_input('What fruit would you like to add to the above list?')
if streamlit.button("Add fruit to the list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function=insert_row_snowflake(fruit_toadd)
  streamlit.text(back_from_function)



   
