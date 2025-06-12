import streamlit as st
from groq import Groq

def crear_usuario_groq():
    clave_secreta = st.secrets["API_Key"]
    return Groq(api_key=clave_secreta)

st.set_page_config(page_title="Mi chat de IA", page_icon="🤖")

MODELOS = ['llama3-8b-8192' , 'llama3-70b-8192' , 'mixtral-8x7b-32768']

def configuracion_pagina():
    st.title("Mi primer Chat de IA")
    st.sidebar.title("Configuracion de la IA")

    elegirModelo = st.sidebar.selectbox('Elegir un Modelo', options=MODELOS)

    return elegirModelo

elegirModelo = configuracion_pagina()
clienteUsuario = crear_usuario_groq()
if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])
mensaje = st.chat_input('Escribí tu mensaje')

if mensaje:
    with st.chat_message("user"):
        st.markdown(mensaje)
    st.session_state.mensajes.append({"role": "user", "content": mensaje})
    
    respuesta_stream = clienteUsuario.chat.completions.create(
        model=elegirModelo,
        messages=st.session_state.mensajes,
        stream=True
    )
    
    with st.chat_message("assistant"):
        respuesta_completa = ""
        respuesta_area = st.empty()
        for chunk in respuesta_stream:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                respuesta_completa += delta.content
                respuesta_area.markdown(respuesta_completa + "▌")

        respuesta_area.markdown(respuesta_completa)  # Mostrar sin cursor al final
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta_completa})
