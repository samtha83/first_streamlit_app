import streamlit
import pandas
import snowflake.connector

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

streamlit.header('Fruitvice Adice')
import requests


fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
streamlit.text(fruityvice_response.json())

fruityvice_normailized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normailized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT *  from FRUIT_LOAD_LIST")
#my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_toadd = streamlit.text_input('What fruit would you like to add to the above list?')
streamlit.write('Thanks for adding ', fruit_toadd)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")

               
