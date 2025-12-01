import streamlit as st
from services.LoginService import LoginService

def login_view():
    st.subheader("Login Necessário")

    st.form("login_form")
    user_input = st.text_input("Nome de Usuário")
    pass_input = st.text_input("Senha", type="password")

    submitted = st.form_submit_button("Entrar")

    login_service = LoginService(username=user_input, 
                                 password=pass_input,
                                 submitted_value= submitted)
    
    login_service.authenticate()



    
