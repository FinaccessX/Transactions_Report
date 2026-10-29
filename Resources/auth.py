import streamlit as st
from cryptography.fernet import Fernet
import time
import gc
from streamlit_autorefresh import st_autorefresh
from Resources import crypto as cp

def verificar_acceso(password_encriptado, kit_funciones, idioma):
    """
    Maneja la lógica completa de acceso. 
    Retorna True si el usuario está autenticado, False de lo contrario.
    idioma: Se tiene las opciones de ES para español y EN para inglés
    """
    v_idioma=[]

    if idioma == "ES":
        v_idioma=["Validación de acceso","Ingresa tu acceso","Confirmar","Validación incorrecta","Validar"]
    elif idioma=="EN":
        v_idioma=["Access validation", "Enter your access", "Confirm", "Invalid validation", "Validate"]

    # 1. Lógica interna de desencriptación
    clave = kit_funciones.cargar_clave()
    fernet = Fernet(clave)
    pswd_ok = kit_funciones.desencriptar_con_manejo_errores(password_encriptado, fernet)

    # 2. Definición del diálogo (interno para que no estorbe en el main)
    @st.dialog(v_idioma[0])
    def validar_contrasena():
        with st.form("validar_pswd", enter_to_submit=True):
            password = st.text_input(v_idioma[1], type="password")
            if st.form_submit_button(v_idioma[2]):
                if password == pswd_ok:
                    st.session_state["pswd"] = True
                    st.rerun()
                else:
                    st.error(v_idioma[3], icon=':material/error:')

    # 3. Control de estado
    if "pswd" not in st.session_state:
        st.session_state["pswd"] = False

    # 4. Renderizado en Sidebar si no está validado
    if not st.session_state["pswd"]:
        with st.sidebar:
            if st.button(v_idioma[4], icon=":material/lock_person:"):
                validar_contrasena()
        return False
    
    return True

def _limpieza_total():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state.clear()
    gc.collect()
    st.rerun()


def gestionar_sesion_segura(contenido_principal_func, password_secreta, idioma, timeout_segundos=1200, log_out=None,crypto_obj=cp):
    """
    Engloba la validación de acceso, el autorefresh y el cierre de sesión.
    """
    v_idioma=[]

    if idioma == "ES":
        v_idioma=["Por favor, acceda en el menú lateral", "Cerrar sesión"]
    elif idioma=="EN":
        v_idioma=["Please, login on the side bar menu.", "Log out"]

    #Latido de actividad
    st_autorefresh(interval=300000, key="auth_heartbeat")
    
    ahora = time.time()
    if "ultima_actividad" not in st.session_state:
        st.session_state.ultima_actividad = ahora

    #Verificación de Inactividad
    diferencia = ahora - st.session_state.ultima_actividad
    
    if diferencia > timeout_segundos:
        _limpieza_total()

    # Validación de Acceso (Tu lógica actual)
    acceso_concedido = verificar_acceso(password_secreta, crypto_obj, idioma)

    if not acceso_concedido:
        st.info(v_idioma[0])
        return 

    # --- SI EL ACCESO ES CORRECTO ---
    if st.session_state.get("heartbeat_timer") == 0: 
        # El valor es 0 justo cuando el usuario interactúa con otro widget
        st.session_state.ultima_actividad = time.time()

    #contenido principal que se usará en cada proyecto
    contenido_principal_func()

    if log_out:
        pass
    else:
        #  Botón de Logout en el sidebar
        if st.sidebar.button(v_idioma[1]):
            _limpieza_total()

