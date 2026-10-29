import streamlit as st
from PIL import Image
from pathlib import Path
from os import path
import numpy as np
# import FISCO_Sources

#ruta base para la lectura de las imagenes
ruta_base = path.dirname(Path(__file__))
st.write(ruta_base)

def imagen_f(title):
    """
    Función para poner la imagen en la pestaña de la página
    title: nombre que se le pondra, ej. "Rendimientos México"
    """

    st.set_page_config(page_icon=Image.open(path.join(ruta_base, "Imagenes", "Logo_finaccess_f.png")),
                        page_title = title)
    return

@st.cache_data(show_spinner=False)
def imagen_f_azul():
    """
    Función para poner la imagen de finaccess del logo azul
    """

    image_azul = Image.open(path.join(ruta_base, "Imagenes", "Logo_finaccess_azul.png"))
    st.image(image_azul, width=700)

    return 


@st.cache_data(show_spinner=False)
def imagen_home(inst):
    """
    Función para poner la imagen de l institución correspondiente
    inst: Nombre de la institución a la que corresponde el proyecto
    """

    image_h = Image.open(path.join(ruta_base, "Imagenes", f"Logo{inst}.png"))
    st.image(image_h, width=700)

    return

# imagen_f("Advised Funds Metrics")
# imagen_f_azul()
# imagen_home()


# st.write(f"la ruta base es: {ruta_base}")
