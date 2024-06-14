import streamlit as st


def welcome_page():
    st.title("Добро пожаловать в Defect Detection App")

    st.markdown("""
        ## Что может?
        Загрузите фотографию сварочного шва или включите камеру и находите дефекты в режиме реального времени.
        
        ## Как использовать? 
        На вкладке слева выберите формат (загрузка изображения или захват видео).
    """)

    st.sidebar.success("Выберите страницу")
