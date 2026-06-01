import streamlit as st
import requests

# Configuración de la página al estilo Japón
st.set_page_config(page_title="Diccionario Nihongo ⛩️", page_icon="🍣", layout="centered")

st.title("⛩️ Diccionario Japonés-Inglés Kawaii 🍡👘⛩️🌸🌟")
st.write("Escribe una palabra en inglés o romaji (ej. *kawaii*, *sushi*, *friend*) para obtener su escritura y significado.")

# Input de usuario
palabra = st.text_input("¿Qué palabra quieres investigar?", placeholder="Ej. kakkoii, sensei, cat...").strip()

if palabra:
    # URL de la API pública de Jisho
    url = f"https://jisho.org/api/v1/search/words?keyword={palabra}"
    
    with st.spinner(f"Buscando '{palabra}' en los archivos de Kyoto..."):
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json().get("data", [])
                
                if data:
                    st.success(f"¡Se encontraron {len(data)} resultados!")
                    st.write("---")
                    
                    # Mostrar las primeras 3 coincidencias más relevantes
                    for item in data[:3]:
                        japanese_info = item.get("japanese", [{}])[0]
                        kanji = japanese_info.get("word")
                        lectura = japanese_info.get("reading")
                        
                        # 1. Cabecera con la escritura japonesa
                        # Si la palabra no tiene Kanji (ej. es solo Hirakana), usa la lectura directa
                        if kanji:
                            st.header(f"🏮 {kanji}")
                            st.subheader(f"🗣️ Lectura (Kana): {lectura}")
                        else:
                            st.header(f"🏮 {lectura}")
                        
                        # Mostrar nivel de JLPT (Examen oficial de japonés) si existe
                        jlpt = item.get("jlpt", [])
                        if jlpt:
                            st.caption(f"🏆 **Nivel del examen:** {', '.join(jlpt).upper()}")
                        
                        # 2. Significados (Senses) de la API
                        st.write("**Significados y partes de la lengua:**")
                        senses = item.get("senses", [])
                        
                        for idx, sense in enumerate(senses[:3]): # Limitamos a 3 para no saturar
                            pos = ", ".join(sense.get("parts_of_speech", []))
                            definitions = ", ".join(sense.get("english_definitions", []))
                            
                            st.markdown(f"{idx+1}. **[{pos}]** {definitions}")
                            
                            # Etiqueta extra si es una palabra común
                            if sense.get("tags"):
                                st.caption(f"💡 *Nota:* {', '.join(sense.get('tags'))}")
                                
                        st.write("---")
                else:
                    st.warning(f"❌ No se encontró nada para '{palabra}'. Prueba con términos comunes.")
            else:
                st.error("Error al conectar con el servidor de Jisho.")
        except Exception as e:
            st.error("Hubo un problema de red. Revisa tu conexión.")