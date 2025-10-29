# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smothie!
  """
)



# Get the current credentials
# session = get_active_session()
# option=st.selectbox(
#     'What is your favourite fruit?'# label,
#     ,('Banana','Straberries','Peaches')# options,
#     # index=0,
#     # format_func=special_internal_function,
#     # key=None,
#     # help=None,
#     # on_change=None,
#     # args=None,
#     # kwargs=None,
#     # *,
#     # placeholder=None,
#     # disabled=False,
#     # label_visibility="visible",
#     # accept_new_options=False, width="stretch"
#     )

# st.write(f'Your favourite fruit is {option}')

name_on_order = st.text_input(
    "Name on smoothie:"
)
st.write(f'Name on smoothie will be: {name_on_order}')

# session = get_active_session()
cnx=st.connection('snowflake')
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string+=fruit + ' '
        st.subheader(fruit+ ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit)
        st_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    # st.stop()
    time_to_insert=st.button('Submit Order')

    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{name_on_order}!', icon="✅")







