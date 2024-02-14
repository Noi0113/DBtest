import streamlit as st

x = 5
y = 3
def is_user_active():
    if 'user_active' in st.session_state.keys() and st.session_state['user_active']:
        return True
    else:
        return False
# if st.button('press here to edit'):
if is_user_active():
    with st.form('form'):
        new_x = st.text_input('edit the value', x)
        new_y = st.text_input('edit the value', y)
        if st.form_submit_button('submit'):
            x = new_x
            y = new_y
        st.text(f'{x},{y}')
        #You can as well save your user input to a database and access later(sqliteDB will be nice)
        st.success('updated successfully')
        if st.form_submit_button('cancel'):
            st.warning('cancelled')
        
        st.info("Kindly reload your browser to start again!!!!")
else:
    if st.button('press here to edit'):
        st.session_state['user_active']=True
        st.experimental_rerun()
