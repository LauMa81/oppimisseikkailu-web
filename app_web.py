#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oppimisseikkailu Web-versio v1.0.0
Streamlit-pohjainen web-sovellus keskittymisvaikeuksien kanssa kamppaileville lapsille

© 2025 Laura - Kaikki oikeudet pidätetään
Tämä teos on suojattu tekijänoikeudella ja kansainvälisillä tekijänoikeus sopimuksilla.
Luvaton kopiointi, jakelu tai muokkaus on kielletty ja saattaa johtaa oikeustoimiin.

KÄYTTÖLISENSSI:
- Henkilökohtainen käyttö sallittu
- Kaupallinen käyttö kielletty ilman lupaa
- Koodin kopiointi tai jakelu kielletty
- Muokkaukset sallittu vain omaan käyttöön

Yhteystiedot: [lisää sähköpostiosoitteesi tähän]

Versio: 1.0.0 Web
Päivitetty: 26.9.2025
"""

import streamlit as st
import random
import json
import os
from datetime import datetime
import time

# Sivun konfiguraatio
st.set_page_config(
    page_title="🌟 Oppimisseikkailu v1.0.0 🌟",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Teemajärjestelmä
def get_theme_colors(teema):
    teemat = {
        "sateenkaari": {
            "bg_gradient": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)",
            "primary": "#FF6B9D",
            "secondary": "#4ECDC4"
        },
        "metsä": {
            "bg_gradient": "linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%)",
            "primary": "#2E8B57",
            "secondary": "#90EE90"
        },
        "meri": {
            "bg_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "primary": "#4682B4",
            "secondary": "#87CEEB"
        },
        "avaruus": {
            "bg_gradient": "linear-gradient(135deg, #2c3e50 0%, #4a6741 100%)",
            "primary": "#9b59b6",
            "secondary": "#f39c12"
        }
    }
    return teemat.get(teema, teemat["sateenkaari"])

# CSS-tyylit teemoilla  
# Varmista että teema on alustettu
if 'teema' not in st.session_state:
    st.session_state.teema = "sateenkaari"
    
theme = get_theme_colors(st.session_state.teema)
st.markdown(f"""
<style>
    .stApp {{
        background: {theme['bg_gradient']};
    }}
    .main-header {{
        text-align: center;
        font-size: 5rem;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8), 1px 1px 3px rgba(0,0,0,0.9);
        font-weight: bold;
        margin-bottom: 2rem;
    }}
    .game-card {{
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        text-align: center;
        font-size: 1.7rem;
        border: 2px solid rgba(0,0,0,0.1);
    }}
    .user-info {{
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 10px;
        color: #333;
        text-align: center;
        margin: 1rem 0;
        font-size: 1.3rem;
        font-weight: bold;
        border: 2px solid rgba(0,0,0,0.2);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    .stButton > button {{
        background-color: {theme['primary']};
        color: white;
        border: 2px solid rgba(0,0,0,0.3);
        border-radius: 10px;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    .stButton > button:hover {{
        background-color: {theme['secondary']};
        transform: scale(1.02);
    }}
    .stButton > button {{
        font-size: 1.5rem !important;
        padding: 1.2rem 2rem !important;
    }}
    .stTextInput > div > div > input {{
        font-size: 1.4rem !important;
        padding: 0.8rem !important;
    }}
    .stTextInput label {{
        font-size: 1.8rem !important;
        font-weight: bold !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}
    .stMarkdown p {{
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }}
    .stMarkdown h1 {{
        font-size: 2rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        font-weight: bold !important;
    }}
    .stMarkdown h2 {{
        font-size: 1.7rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        font-weight: bold !important;
    }}
    .stMarkdown h3 {{
        font-size: 1.4rem !important;
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
        font-weight: bold !important;
    }}
    .stRadio > div {{
        font-size: 1.1rem !important;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        font-weight: 500 !important;
    }}
    .stRadio label {{
        font-size: 1.1rem !important;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        font-weight: bold !important;
    }}
    .stSelectbox label {{
        font-size: 1.1rem !important;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        font-weight: bold !important;
    }}
    .stAlert {{
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }}
</style>
""", unsafe_allow_html=True)

# Session state muuttujat
if 'kayttaja_nimi' not in st.session_state:
    st.session_state.kayttaja_nimi = ""
if 'teema' not in st.session_state:
    st.session_state.teema = "sateenkaari"
if 'pisteet' not in st.session_state:
    st.session_state.pisteet = 0
if 'suoritetut_tehtavat' not in st.session_state:
    st.session_state.suoritetut_tehtavat = 0
if 'oikeat_vastaukset' not in st.session_state:
    st.session_state.oikeat_vastaukset = 0
if 'current_page' not in st.session_state:
    st.session_state.current_page = "nimi" if not st.session_state.kayttaja_nimi else "menu"

def tallenna_edistyminen():
    """Tallentaa edistymisen JSON-tiedostoon"""
    try:
        data = {
            'kayttaja_nimi': st.session_state.kayttaja_nimi,
            'pisteet': st.session_state.pisteet,
            'suoritetut_tehtavat': st.session_state.suoritetut_tehtavat,
            'oikeat_vastaukset': st.session_state.oikeat_vastaukset,
            'paivitetty': datetime.now().isoformat()
        }
        with open('web_edistyminen.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Tallentaminen epäonnistui: {e}")

def lataa_edistyminen():
    """Lataa edistymisen JSON-tiedostosta"""
    try:
        if os.path.exists('web_edistyminen.json'):
            with open('web_edistyminen.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('kayttaja_nimi') == st.session_state.kayttaja_nimi:
                    st.session_state.pisteet = data.get('pisteet', 0)
                    st.session_state.suoritetut_tehtavat = data.get('suoritetut_tehtavat', 0)
                    st.session_state.oikeat_vastaukset = data.get('oikeat_vastaukset', 0)
    except Exception:
        pass

def nimi_sivu():
    """Näyttää nimen kysymissivun"""
    st.title("🌟 Oppimisseikkailu 🌟")
    
    # Ohjepainike ylänurkkaan
    if st.button("ℹ️ Mitä tämä on?", help="Lue tarina ja ohjeet"):
        st.session_state.current_page = "ohje"
        st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("💝 Tervetuloa oppimaan!")
        
        st.info("""
        💕 **Tämä sovellus syntyi rakkaudesta omaa poikaa kohtaan.** 
        
        Huomasin, miten vaikeaa keskittyminen ja oppiminen voi olla, kun aivot toimivat eri tavalla. 
        Halusin luoda turvallisen paikan, jossa jokainen lapsi voi oppia omaan tahtiin ja löytää onnistumisen iloa. ❤️
        """)
        
        st.markdown("**Tämä on sinun turvallinen oppimistilasi**")
        st.markdown("Kerro meille nimesi, niin voimme seurata edistymistäsi:")
        
        nimi = st.text_input("Mikä on nimesi?", placeholder="Kirjoita nimesi tähän...", key="nimi_input", 
                            help="Syötä nimesi isolla fontilla!")
        
        if st.button("Aloita seikkailu! 🚀", type="primary", use_container_width=True):
            if nimi.strip():
                st.session_state.kayttaja_nimi = nimi.strip()
                lataa_edistyminen()
                st.session_state.current_page = "menu"
                st.rerun()
            else:
                st.error("Syötä nimesi ennen jatkamista!")

def paa_menu():
    """Näyttää päävalikon"""
    st.title("🌟 Oppimisseikkailu 🌟")
    
    # Ohjepainike ylänurkkaan
    col_ohje1, col_ohje2 = st.columns([6, 1])
    with col_ohje2:
        if st.button("ℹ️ Ohjeet", help="Lue tarina ja käyttöohjeet"):
            st.session_state.current_page = "ohje"
            st.rerun()
    
    # Käyttäjätiedot
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="user-info">
            <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">Hei {st.session_state.kayttaja_nimi}! 👋</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">Pisteet: {st.session_state.pisteet} | Tehtäviä suoritettu: {st.session_state.suoritetut_tehtavat}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # KORJATTU PÄÄVALIKKO - Täsmälleen samat pelit kuin työpöydässä
    st.markdown('<h3 style="font-size: 1.4rem; color: white; text-align: center; margin: 2rem 0;">Valitse peli:</h3>', unsafe_allow_html=True)
    
    # Ensimmäinen rivi - 2 peliä vierekkäin
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Sanojen Seikkailu\nLukemispeli", use_container_width=True, type="primary"):
            st.session_state.current_page = "lukeminen"
            st.rerun()
            
        if st.button("💭 Tunnetilat\nMiten voit?", use_container_width=True):
            st.session_state.current_page = "tunteet"
            st.rerun()
            
    with col2:
        if st.button("🔢Numeromagia\nMatematiikkapeli", use_container_width=True):
            st.session_state.current_page = "matematiikka"
            st.rerun()
            
        if st.button("💫 Keskittymishetki\nRauhoittuminen", use_container_width=True):
            st.session_state.current_page = "keskittyminen"
            st.rerun()
    
    # Toinen rivi - Tilanteen käsittely
    if st.button("🤝 Tilanteen käsittely\nMitä tapahtuu jos...", use_container_width=True):
        st.session_state.current_page = "sosiaaliset"
        st.rerun()
    
    # Alareunan napit
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Edistymisraportti"):
            st.session_state.current_page = "raportti"
            st.rerun()
    
    with col2:
        if st.button("👤 Vaihda käyttäjää"):
            st.session_state.kayttaja_nimi = ""
            st.session_state.current_page = "nimi"
            st.rerun()
    
    with col3:
        if st.button("🔄 Nollaa edistyminen"):
            if st.button("Vahvista nollaus", type="secondary"):
                st.session_state.pisteet = 0
                st.session_state.suoritetut_tehtavat = 0
                st.session_state.oikeat_vastaukset = 0
                tallenna_edistyminen()
                st.success("Edistyminen nollattu!")
                st.rerun()
    
    # Teemavalitsin
    st.markdown("---")
    st.markdown("### 🎨 Valitse teema:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌈 Sateenkaari", use_container_width=True):
            st.session_state.teema = "sateenkaari"
            st.rerun()
    with col2:
        if st.button("🌲 Metsä", use_container_width=True):
            st.session_state.teema = "metsä"
            st.rerun()
    with col3:
        if st.button("🌊 Meri", use_container_width=True):
            st.session_state.teema = "meri"
            st.rerun()
    with col4:
        if st.button("🌌 Avaruus", use_container_width=True):
            st.session_state.teema = "avaruus"
            st.rerun()
    
    # Ohje-painike keskitetysti
    st.markdown("---")
    col_ohje1, col_ohje2, col_ohje3 = st.columns([1, 2, 1])
    with col_ohje2:
        if st.button("💝 **Tarina & Ohjeet** 💝", key="ohje_btn", use_container_width=True):
            st.session_state.current_page = "ohje"
            st.rerun()

def matematiikka_peli():
    """Laajempi matematiikkapeli kuten työpöytäversiossa"""
    st.markdown('<h1 class="main-header">🔢 Numeromagia - Valitse laskutyyppi</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin päävalikkoon"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    st.markdown('<h3 style="font-size: 1.4rem; color: white; text-align: center;">Mitä laskuja haluat harjoitella tänään?</h3>', unsafe_allow_html=True)
    
    # Alusta session state
    if 'math_mode' not in st.session_state:
        st.session_state.math_mode = "menu"
    if 'math_operation' not in st.session_state:
        st.session_state.math_operation = "+"
    if 'math_question' not in st.session_state:
        st.session_state.math_question = None
    if 'math_answer' not in st.session_state:
        st.session_state.math_answer = None
    if 'math_feedback' not in st.session_state:
        st.session_state.math_feedback = ""
    
    if st.session_state.math_mode == "menu":
        # Näytä laskutyypit ruudukossa
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ Yhteenlasku", use_container_width=True, type="primary"):
                st.session_state.math_mode = "game"
                st.session_state.math_operation = "+"
                generate_math_question()
                st.rerun()
            
            if st.button("✖️ Kertolasku", use_container_width=True):
                st.session_state.math_mode = "game" 
                st.session_state.math_operation = "*"
                generate_math_question()
                st.rerun()
            
            if st.button("⚖️ Painot (g/kg)", use_container_width=True):
                st.session_state.math_mode = "weight"
                generate_weight_question()
                st.rerun()
        
        with col2:
            if st.button("➖ Vähennyslasku", use_container_width=True):
                st.session_state.math_mode = "game"
                st.session_state.math_operation = "-"
                generate_math_question()
                st.rerun()
                
            if st.button("➗ Jakolasku", use_container_width=True):
                st.session_state.math_mode = "game"
                st.session_state.math_operation = "/"
                generate_math_question()
                st.rerun()
                
            if st.button("📏 Pituudet (mm/cm/m)", use_container_width=True):
                st.session_state.math_mode = "length"
                generate_length_question()
                st.rerun()
        
        # Sekalaiset laskut koko leveydellä
        if st.button("🎲 Sekalaiset laskut", use_container_width=True):
            st.session_state.math_mode = "game"
            st.session_state.math_operation = "mix"
            generate_math_question()
            st.rerun()
    
    elif st.session_state.math_mode == "game":
        show_math_game()
    elif st.session_state.math_mode == "weight":
        show_weight_game()
    elif st.session_state.math_mode == "length":
        show_length_game()

def generate_math_question():
    """Generoi matemaattisen kysymyksen"""
    if st.session_state.math_operation == "mix":
        operation = random.choice(["+", "-", "*"])
    else:
        operation = st.session_state.math_operation
    
    if operation == "+":
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        answer = a + b
        question = f"{a} + {b} = ?"
        operation_name = "➕ Yhteenlaskut"
    elif operation == "-":
        a = random.randint(10, 50)
        b = random.randint(1, a)
        answer = a - b
        question = f"{a} - {b} = ?"
        operation_name = "➖ Vähennyslaskut"
    elif operation == "*":
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        answer = a * b
        question = f"{a} × {b} = ?"
        operation_name = "✖️ Kertolaskut"
    elif operation == "/":
        b = random.randint(2, 12)
        answer = random.randint(1, 12)
        a = b * answer
        question = f"{a} ÷ {b} = ?"
        operation_name = "➗ Jakolaskut"
    
    st.session_state.math_question = question
    st.session_state.math_answer = answer
    st.session_state.math_operation_name = operation_name
    st.session_state.math_feedback = ""

def show_math_game():
    """Näyttää matematiikkapelin"""
    if st.session_state.math_question:
        st.markdown(f'<h2 style="text-align: center; color: white;">{st.session_state.math_operation_name}</h2>', unsafe_allow_html=True)
        
        # Näytä kysymys
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 15px; margin: 1.5rem 0; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.1);'>
            <h1 style='color: #2C3E50; font-size: 2.5rem; margin: 0; font-weight: bold;'>{st.session_state.math_question}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Vastauskenttä
        user_answer = st.number_input("Mikä on vastaus?", min_value=-1000, max_value=1000, step=1, value=0, key="math_user_answer")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Tarkista vastaus", type="primary"):
                check_math_answer(user_answer)
        
        with col2:
            if st.button("🎲 Uusi lasku"):
                generate_math_question()
                st.rerun()
        
        with col3:
            if st.button("🔄 Vaihda tyyppiä"):
                st.session_state.math_mode = "menu"
                st.rerun()
        
        # Näytä palaute
        if st.session_state.math_feedback:
            if "OIKEIN" in st.session_state.math_feedback or "🎉" in st.session_state.math_feedback:
                st.success(st.session_state.math_feedback)
            else:
                st.error(st.session_state.math_feedback)

def check_math_answer(user_answer):
    """Tarkistaa matematiikan vastauksen"""
    if user_answer == st.session_state.math_answer:
        # Eri pisteet eri laskutyypeille
        pisteet = 3 if st.session_state.math_operation in ['+', '-'] else 5
        if st.session_state.math_operation == '/':
            pisteet = 7
        
        st.session_state.pisteet += pisteet
        st.session_state.suoritetut_tehtavat += 1
        st.session_state.oikeat_vastaukset += 1
        tallenna_edistyminen()
        
        kannustus = [
            f"🎉 OIKEIN! Mahtavaa! +{pisteet} pistettä",
            f"✨ Loistavaa! Sait {pisteet} pistettä!",
            f"🌟 Hienoa työtä! +{pisteet} pistettä",
            f"💫 Erinomaista! Ansaitsit {pisteet} pistettä!"
        ]
        st.session_state.math_feedback = random.choice(kannustus)
    else:
        st.session_state.suoritetut_tehtavat += 1
        tallenna_edistyminen()
        
        virheilmoitukset = [
            f"❌ Ei aivan! Oikea vastaus oli: {st.session_state.math_answer}",
            f"🤔 Lähellä! Vastaus on: {st.session_state.math_answer}",
            f"💭 Ei haittaa! Oikea vastaus: {st.session_state.math_answer}"
        ]
        st.session_state.math_feedback = random.choice(virheilmoitukset)

def generate_weight_question():
    """Generoi painomuunnostehtävän"""
    muunnostyyppi = random.choice(['g_to_kg', 'kg_to_g'])
    
    if muunnostyyppi == 'g_to_kg':
        gramma = random.choice([500, 1000, 1500, 2000, 2500, 3000, 4000, 5000])
        answer = gramma / 1000
        question = f"{gramma} g = ? kg"
        unit = "kg"
    else:
        kilogramma = random.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
        if kilogramma == int(kilogramma):
            kilogramma = int(kilogramma)
        answer = kilogramma * 1000
        question = f"{kilogramma} kg = ? g"
        unit = "g"
    
    st.session_state.weight_question = question
    st.session_state.weight_answer = answer
    st.session_state.weight_unit = unit
    st.session_state.weight_feedback = ""

def show_weight_game():
    """Näyttää painomuunnospelin"""
    st.markdown('<h2 style="text-align: center; color: white;">⚖️ Painomuunnokset</h2>', unsafe_allow_html=True)
    
    # Ohje
    st.info("💡 Muista: 1 kg = 1000 g")
    
    if hasattr(st.session_state, 'weight_question'):
        # Näytä kysymys
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 15px; margin: 1.5rem 0; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.1);'>
            <h1 style='color: #E67E22; font-size: 2.5rem; margin: 0; font-weight: bold;'>{st.session_state.weight_question}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Vastauskenttä
        user_answer = st.number_input(f"Vastaus ({st.session_state.weight_unit}):", min_value=0.0, step=0.1, key="weight_user_answer")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Tarkista", type="primary"):
                check_weight_answer(user_answer)
        
        with col2:
            if st.button("🔄 Uusi tehtävä"):
                generate_weight_question()
                st.rerun()
        
        with col3:
            if st.button("⬅️ Takaisin"):
                st.session_state.math_mode = "menu"
                st.rerun()
        
        # Näytä palaute
        if hasattr(st.session_state, 'weight_feedback') and st.session_state.weight_feedback:
            if "OIKEIN" in st.session_state.weight_feedback or "🎉" in st.session_state.weight_feedback:
                st.success(st.session_state.weight_feedback)
            else:
                st.error(st.session_state.weight_feedback)

def check_weight_answer(user_answer):
    """Tarkistaa painomuunnoksen vastauksen"""
    if abs(user_answer - st.session_state.weight_answer) < 0.001:
        st.session_state.pisteet += 6
        st.session_state.suoritetut_tehtavat += 1
        st.session_state.oikeat_vastaukset += 1
        tallenna_edistyminen()
        
        kannustus = [
            "🎉 OIKEIN! Osaat muunnokset! +6 pistettä",
            "⚖️ Mahtavaa! Painot hallussa! +6 pistettä",
            "✨ Loistavaa muunnostyötä! +6 pistettä"
        ]
        st.session_state.weight_feedback = random.choice(kannustus)
    else:
        st.session_state.suoritetut_tehtavat += 1
        tallenna_edistyminen()
        
        oikea = int(st.session_state.weight_answer) if st.session_state.weight_answer == int(st.session_state.weight_answer) else st.session_state.weight_answer
        st.session_state.weight_feedback = f"❌ Ei aivan! Oikea vastaus: {oikea}"

def generate_length_question():
    """Generoi pituusmuunnostehtävän"""
    muunnostyypit = ['mm_to_cm', 'cm_to_mm', 'cm_to_m', 'm_to_cm', 'mm_to_m', 'm_to_mm']
    muunnostyyppi = random.choice(muunnostyypit)
    
    if muunnostyyppi == 'mm_to_cm':
        mm = random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200])
        answer = mm / 10
        question = f"{mm} mm = ? cm"
        unit = "cm"
    elif muunnostyyppi == 'cm_to_mm':
        cm = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20])
        answer = cm * 10
        question = f"{cm} cm = ? mm"
        unit = "mm"
    elif muunnostyyppi == 'cm_to_m':
        cm = random.choice([100, 150, 200, 250, 300, 350, 400, 500])
        answer = cm / 100
        question = f"{cm} cm = ? m"
        unit = "m"
    elif muunnostyyppi == 'm_to_cm':
        m = random.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
        answer = m * 100
        question = f"{m} m = ? cm"
        unit = "cm"
    elif muunnostyyppi == 'mm_to_m':
        mm = random.choice([1000, 1500, 2000, 2500, 3000, 4000, 5000])
        answer = mm / 1000
        question = f"{mm} mm = ? m"
        unit = "m"
    else:  # m_to_mm
        m = random.choice([0.5, 1, 1.5, 2, 2.5, 3])
        answer = m * 1000
        question = f"{m} m = ? mm"
        unit = "mm"
    
    st.session_state.length_question = question
    st.session_state.length_answer = answer
    st.session_state.length_unit = unit
    st.session_state.length_feedback = ""

def show_length_game():
    """Näyttää pituusmuunnospelin"""
    st.markdown('<h2 style="text-align: center; color: white;">📏 Pituusmuunnokset</h2>', unsafe_allow_html=True)
    
    # Ohjeet
    st.info("💡 Muista: 1 m = 100 cm = 1000 mm | 1 cm = 10 mm")
    
    if hasattr(st.session_state, 'length_question'):
        # Näytä kysymys
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 15px; margin: 1.5rem 0; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.1);'>
            <h1 style='color: #16A085; font-size: 2.5rem; margin: 0; font-weight: bold;'>{st.session_state.length_question}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Vastauskenttä
        user_answer = st.number_input(f"Vastaus ({st.session_state.length_unit}):", min_value=0.0, step=0.1, key="length_user_answer")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Tarkista", type="primary"):
                check_length_answer(user_answer)
        
        with col2:
            if st.button("🔄 Uusi tehtävä"):
                generate_length_question()
                st.rerun()
        
        with col3:
            if st.button("⬅️ Takaisin"):
                st.session_state.math_mode = "menu"
                st.rerun()
        
        # Näytä palaute
        if hasattr(st.session_state, 'length_feedback') and st.session_state.length_feedback:
            if "OIKEIN" in st.session_state.length_feedback or "🎉" in st.session_state.length_feedback:
                st.success(st.session_state.length_feedback)
            else:
                st.error(st.session_state.length_feedback)

def check_length_answer(user_answer):
    """Tarkistaa pituusmuunnoksen vastauksen"""
    if abs(user_answer - st.session_state.length_answer) < 0.001:
        st.session_state.pisteet += 6
        st.session_state.suoritetut_tehtavat += 1
        st.session_state.oikeat_vastaukset += 1
        tallenna_edistyminen()
        
        kannustus = [
            "🎉 OIKEIN! Osaat pituudet! +6 pistettä",
            "📏 Mahtavaa! Mittayksikkös hallussa! +6 pistettä",
            "✨ Loistavaa muunnostyötä! +6 pistettä"
        ]
        st.session_state.length_feedback = random.choice(kannustus)
    else:
        st.session_state.suoritetut_tehtavat += 1
        tallenna_edistyminen()
        
        oikea = int(st.session_state.length_answer) if st.session_state.length_answer == int(st.session_state.length_answer) else st.session_state.length_answer
        st.session_state.length_feedback = f"❌ Ei aivan! Oikea vastaus: {oikea}"

def lukemis_peli():
    """Lukemispeli - sanojen tunnistus"""
    st.markdown('<h1 class="main-header">📚 Lukemispeli</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin päävalikkoon"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    # Laajempi valikoima sanoja ja kuvauksia
    sanat_ja_kuvaukset = [
        # Eläimet
        ("KISSA", "Pehmeä lemmikkieläin, joka sanoo 'miau'"),
        ("KOIRA", "Uskollinen ystävä, joka sanoo 'hau'"),
        ("LINTU", "Laulava eläin, joka lentää taivaalla"),
        ("KALA", "Ui vedessä ja on hyvää ruokaa"),
        ("HEVONEN", "Iso eläin, jolla voi ratsastaa"),
        ("KANI", "Pörröinen eläin, jolla on pitkät korvat"),
        ("SIKA", "Älykkäs eläin, joka rakastaa mutaa"),
        ("SAMMAKKO", "Vihreä eläin, joka hyppii ja ui"),
        
        # Luonto
        ("KUKKA", "Kaunis kasvi, joka tuoksuu hyvältä"),
        ("PUU", "Iso kasvi, jossa on lehtiä ja oksia"),
        ("PILVI", "Valkoinen tai harmaa pallo taivaalla"),
        ("SADE", "Vettä tippuu taivaalta"),
        ("LUMI", "Valkoista, putoaa talvella"),
        ("AURINKO", "Keltainen pallo, joka lämmittää"),
        ("KIVI", "Kova esine maassa"),
        ("JÄRVI", "Iso vesilammikko"),
        
        # Koti ja esineet
        ("KOTI", "Paikka, jossa asut perheen kanssa"),
        ("SÄNKY", "Siinä nukutaan yöllä"),
        ("TUOLI", "Sillä istutaan pöydän ääressä"),
        ("PÖYTÄ", "Tasainen pinta, jonka ääressä syödään"),
        ("LAUTANEN", "Pyöreä esine, jolta syödään ruokaa"),
        ("LUSIKKA", "Sillä syödään keittoa"),
        ("LASI", "Siitä juodaan vettä tai maitoa"),
        ("PEILI", "Siitä näkee oman kuvan"),
        
        # Ruoka ja juoma
        ("RUOKA", "Sitä syödään kun on nälkä"),
        ("LEIPÄ", "Ruskea tai valkoinen, syödään voileipänä"),
        ("MAITO", "Valkoista juotavaa lehmältä"),
        ("OMENA", "Punainen tai vihreä pyöreä hedelmä"),
        ("BANAANI", "Keltainen pitkä hedelmä"),
        ("KEKSI", "Makea pieni pyöreä herkku"),
        ("JUUSTO", "Keltaista tai valkoista, maistuu hyvälle"),
        ("MARJA", "Pieni pyöreä makea hedelmä"),
        
        # Kulkuneuvot ja liikenne
        ("AUTO", "Kulkuneuvo, jolla ajetaan tiellä"),
        ("BUSSI", "Iso auto, jossa on monta paikkaa"),
        ("JUNA", "Pitkä kulkuneuvo, joka kulkee kiskoilla"),
        ("PYÖRÄ", "Sillä poljetaan, siinä on kaksi rengasta"),
        ("LENTOKONE", "Lentää korkealla taivaalla"),
        ("LAIVA", "Kulkee vedessä ja ui pinnan päällä"),
        
        # Harrastukset ja lelut
        ("PALLO", "Pyöreä esine, jolla pelataan"),
        ("KIRJA", "Siitä voi lukea tarinoita"),
        ("KYNÄ", "Sillä kirjoitetaan paperille"),
        ("PAPERI", "Valkoista, sille voi piirtää"),
        ("NALLE", "Pehmeä karhu-lelu"),
        ("NUKKE", "Lelu, joka näyttää ihmiseltä"),
        ("PALAPELI", "Monta palaa, jotka sopivat yhteen"),
        
        # Kehon osat
        ("KÄSI", "Sillä tartutaan asioihin"),
        ("JALKA", "Sillä kävellään ja juostaan"),
        ("SILMÄ", "Sillä katsotaan ja nähdään"),
        ("SUU", "Sillä syödään ja puhutaan"),
        ("NENÄ", "Sillä haistetaan tuoksuja"),
        ("KORVA", "Sillä kuullaan ääniä"),
        
        # Värit
        ("PUNAINEN", "Väri kuin tomaatti tai mansikka"),
        ("SININEN", "Väri kuin taivas tai meri"),
        ("VIHREÄ", "Väri kuin ruoho tai lehdet"),
        ("KELTAINEN", "Väri kuin aurinko tai banaani"),
        ("VALKOINEN", "Väri kuin lumi tai maito"),
        ("MUSTA", "Väri kuin yö tai hiili"),
        
        # Muut hyödylliset sanat
        ("VESI", "Sitä juodaan kun on jano"),
        ("YSTÄVÄ", "Mukava henkilö, jonka kanssa leikitään"),
        ("PERHE", "Äiti, isä, sisarukset ja muut läheiset"),
        ("KOULU", "Paikka, jossa opitaan uusia asioita"),
        ("OPETTAJA", "Henkilö, joka opettaa koulussa"),
        ("KIITOS", "Sana, jonka sanoo kun saa jotain"),
        ("ANTEEKSI", "Sana, jonka sanoo kun on tehnyt väärin")
    ]
    
    # Alusta peli
    if 'reading_word' not in st.session_state:
        st.session_state.reading_word = None
        st.session_state.reading_desc = None
        st.session_state.scrambled_letters = []
        st.session_state.reading_feedback = ""
    
    if st.button("🎲 Uusi sana", type="primary"):
        word, desc = random.choice(sanat_ja_kuvaukset)
        st.session_state.reading_word = word
        st.session_state.reading_desc = desc
        st.session_state.scrambled_letters = list(word)
        random.shuffle(st.session_state.scrambled_letters)
        st.session_state.reading_feedback = ""
    
    if st.session_state.reading_word:
        # Näytä kuvaus selkeästi
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; margin: 1.5rem 0; box-shadow: 0 6px 12px rgba(0,0,0,0.1);'>
            <h3 style='color: #8E44AD; font-size: 1.6rem; margin-bottom: 1rem;'>🤔 Mikä sana sopii kuvaukseen:</h3>
            <p style='font-size: 1.4rem; color: #333; font-weight: bold; font-style: italic; line-height: 1.4;'>"{st.session_state.reading_desc}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Näytä sekoitetut kirjaimet
        st.markdown("### Käytä näitä kirjaimia:")
        letters_display = "  ".join(st.session_state.scrambled_letters)
        st.markdown(f"<div style='background-color: #F8C471; padding: 1.5rem; border-radius: 10px; text-align: center; font-size: 2rem; font-weight: bold; letter-spacing: 0.5rem; margin: 1rem 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>{letters_display}</div>", unsafe_allow_html=True)
        
        # Vastauskenttä
        user_answer = st.text_input("Kirjoita sana:", placeholder="Kirjoita vastauksesi tähän...", key="reading_input").upper()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Tarkista vastaus", type="primary"):
                if user_answer == st.session_state.reading_word:
                    st.session_state.pisteet += 15
                    st.session_state.suoritetut_tehtavat += 1
                    st.session_state.oikeat_vastaukset += 1
                    st.session_state.reading_feedback = f"🎉 Oikein! Sana oli '{st.session_state.reading_word}'. Sait 15 pistettä!"
                    tallenna_edistyminen()
                else:
                    st.session_state.suoritetut_tehtavat += 1
                    st.session_state.reading_feedback = f"❌ Väärin. Oikea sana oli '{st.session_state.reading_word}'"
                    tallenna_edistyminen()
        
        with col2:
            if st.button("💡 Vinkki"):
                hint = st.session_state.reading_word[0] + "___"
                st.info(f"Vinkki: Sana alkaa kirjaimella '{st.session_state.reading_word[0]}' ja on {len(st.session_state.reading_word)} kirjainta pitkä: {hint}")
        
        # Näytä palaute
        if st.session_state.reading_feedback:
            if "Oikein" in st.session_state.reading_feedback:
                st.success(st.session_state.reading_feedback)
            else:
                st.error(st.session_state.reading_feedback)

def tunteiden_kasittely():
    """Tunteiden käsittely - Tunnista ja käsittele tunteitasi"""
    st.markdown('<h1 class="main-header">💭 Tunteiden käsittely</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin päävalikkoon"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    # Kuvaus (desktop-versiosta)
    st.markdown("""
    ### Miltä sinusta tuntuu juuri nyt? 
    **Valitse tunne, niin saat kannustavan viestin! 💝**
    """)
    
    # Tunneviestit desktop-versiosta
    if 'tunne_viesti' not in st.session_state:
        st.session_state.tunne_viesti = ""
    
    # Tunneviestit (samat kuin desktop-versiossa)
    tunneviestit = {
        "onnellinen": {
            "otsikko": "✨ Ihana kuulla että olet onnellinen!",
            "viesti": ("Onnellisuutesi on kuin auringonsäde! ☀️\n\n" + 
                     "💡 Vinkkejä onnellisuuden jakamiseen:\n" +
                     "• Hymyile muille - se tarttuu!\n" +
                     "• Kirjoita onnellisuudestasi päiväkirjaan\n" +
                     "• Tee jotain kivaa ystävän kanssa\n" +
                     "• Nauti tästä hetkestä täysillä!\n\n" +
                     "🌟 Sinä olet tähti joka loistaa kirkkaasti!")
        },
        "innostunut": {
            "otsikko": "🚀 Vau, sinulla on paljon energiaa!",
            "viesti": ("Innostuksesi on mahtava voima! 🔥\n\n" +
                     "💡 Käytä energiasi hyvin:\n" +
                     "• Keskity yhteen asiaan kerrallaan\n" +
                     "• Ota välillä hengähdystauko\n" +
                     "• Jaa innostuksesi muiden kanssa\n" +
                     "• Tee lista kaikista kivoisista ideoista\n\n" +
                     "🌈 Innostuksesi tekee maailmasta värikkäämmän!")
        },
        "rauhallinen": {
            "otsikko": "🧘‍♀️ Rauhallisuutesi on lahja!",
            "viesti": ("Olet kuin tyyni järvi - niin rauhallinen! 🏞️\n\n" +
                     "💡 Säilytä rauhallisuutesi:\n" +
                     "• Hengitä syvään kun tuntuu hyvältä\n" +
                     "• Anna itsellesi aikaa miettiä\n" +
                     "• Auta muita rauhoittumaan läsnäolollasi\n" +
                     "• Nauti hiljaisista hetkistä\n\n" +
                     "🕯️ Rauhallisuutesi tuo valoa maailmaan!")
        },
        "vasynyt": {
            "otsikko": "😴 Ole kiltti itsellesi, olet väsynyt",
            "viesti": ("Väsymys on merkki siitä, että kehosi tarvitsee lepoa 💤\n\n" +
                     "💡 Jaksamisen vinkit:\n" +
                     "• Nuku riittävästi (lapset tarvitsevat 9-11h)\n" +
                     "• Syö terveellistä ruokaa antamaan energiaa\n" +
                     "• Ota pieniä taukoja opiskelusta\n" +
                     "• Pyydä apua jos se tuntuu liian vaikealta\n\n" +
                     "🌙 Huomenna jaksat taas paremmin!")
        },
        "hermostunut": {
            "otsikko": "💙 Hermostuneisuus on normaalia",
            "viesti": ("Kaikki jännittävät joskus, se on ihan okei! 🤗\n\n" +
                     "💡 Rauhoittumisen keinot:\n" +
                     "• Hengitä rauhallisesti: sisään 4, ulos 4\n" +
                     "• Laske hiljaa 1-10 tai 10-1\n" +
                     "• Muistuta itseäsi: 'Selviän tästä'\n" +
                     "• Puhu luotettavalle aikuiselle\n\n" +
                     "🌊 Tunteet ovat kuin aallot - ne tulevat ja menevät")
        },
        "vihainen": {
            "otsikko": "🔥 Viha on voimakas tunne",
            "viesti": ("On okei tuntea vihaa, mutta käsitellään se viisaasti! 💪\n\n" +
                     "💡 Vihan käsittely:\n" +
                     "• Laske 10:een ennen kuin toimit\n" +
                     "• Hengitä syvään muutaman kerran\n" +
                     "• Kerro mitä tunteet - älä huuda\n" +
                     "• Liiku: juokse, hyppii tai lyö tyynyä\n\n" +
                     "⚡ Vihasi kertoo että jokin on tärkeää sinulle!")
        },
        "surullinen": {
            "otsikko": "💜 Suru on tärkeä tunne",
            "viesti": ("Itku pesee sydämen puhtaaksi 🌧️➡️🌈\n\n" +
                     "💡 Surun kanssa selviytyminen:\n" +
                     "• Anna itsellesi lupa tuntea surua\n" +
                     "• Puhu jollekulle joka välittää sinusta\n" +
                     "• Tee jotain lempeää itsellesi\n" +
                     "• Muista että suru ei kestä ikuisesti\n\n" +
                     "🤗 Ansaitset hellyyttä ja ymmärrystä!")
        },
        "huolestunut": {
            "otsikko": "🌈 Huolet ovat kuin pilvet",
            "viesti": ("Huolet tulevat ja menevät - aurinko paistaa pilven takaa! ☁️☀️\n\n" +
                     "💡 Huolten käsittely:\n" +
                     "• Kerro huolesi ääneen tai paperille\n" +
                     "• Kysy itseltäsi: 'Voinko tehdä tälle jotain?'\n" +
                     "• Keskity siihen mitä voit kontrolloida\n" +
                     "• Muista kaikki kerrat kun olet selvinnyt\n\n" +
                     "🦋 Olet vahvempi kuin luuletkaan!")
        },
        "sekava": {
            "otsikko": "🧩 Sekavuus on osa oppimista",
            "viesti": ("Kuin palapeli joka järjestyy hitaasti - se on normaalia! 🔄\n\n" +
                     "💡 Selkeyden löytäminen:\n" +
                     "• Ota hetki hengitellä rauhassa\n" +
                     "• Kirjaa ylös ajatuksiasi\n" +
                     "• Kysy apua kun tuntuu sekavalta\n" +
                     "• Tee yksi pieni askel kerrallaan\n\n" +
                     "🔍 Jokaisesta sekavuudesta löytyy selvyys lopulta!")
        }
    }
    
    # Tunnenapit samassa järjestyksessä kuin desktop-versiossa
    st.markdown("### Valitse tunne:")
    
    # Rivi 1: Positiiviset
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("😊\nOnnellinen", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["onnellinen"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    with col2:
        if st.button("🤩\nInnostunut", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["innostunut"] 
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    with col3:
        if st.button("😌\nRauhallinen", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["rauhallinen"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    
    # Rivi 2: Neutraalit/haasteet
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("😴\nVäsynyt", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["vasynyt"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    with col2:
        if st.button("😰\nHermostunut", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["hermostunut"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    with col3:
        if st.button("😠\nVihainen", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["vihainen"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    
    # Rivi 3: Syvemmät tunteet  
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("😢\nSurullinen", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["surullinen"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    with col2:
        if st.button("😟\nHuolestunut", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["huolestunut"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    with col3:
        if st.button("🤔\nSekava", use_container_width=True):
            st.session_state.tunne_viesti = tunneviestit["sekava"]
            st.session_state.pisteet += 5
            tallenna_edistyminen()
    
    # Näytä tunneviesti jos valittu
    if st.session_state.tunne_viesti:
        viesti_data = st.session_state.tunne_viesti
        
        # Näytä viesti popup-tyylisesti
        st.markdown("---")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 6px 12px rgba(0,0,0,0.2);'>
            <h2 style='color: white; text-align: center; margin-bottom: 1rem;'>{viesti_data['otsikko']}</h2>
            <div style='background: white; padding: 1.5rem; border-radius: 10px; color: #333;'>
                <pre style='white-space: pre-wrap; font-family: Arial; font-size: 1rem; line-height: 1.4;'>{viesti_data['viesti']}</pre>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💝 Kiitos tsempistä! (+5 pistettä)", type="primary"):
            st.session_state.tunne_viesti = ""
            st.success("Hyvin tehty kun tunnistit tunteesi!")
            st.rerun()

def keskittymishetki():
    """Keskittymisharjoitukset ja rauhoittuminen"""
    st.markdown('<h1 class="main-header">💫 Keskittymishetki</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin päävalikkoon"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; margin: 1.5rem 0; box-shadow: 0 6px 12px rgba(0,0,0,0.1);'>
        <h3 style='color: #9B59B6; font-size: 1.4rem; margin-bottom: 1rem;'>🌸 Valitse harjoitus rauhoittumiseen:</h3>
        <p style='font-size: 1.1rem; color: #666; line-height: 1.5;'>Nämä harjoitukset auttavat sinua keskittymään ja rauhoittumaan</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Harjoitukset 2x2 ruudukossa
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💨 Hengitysharjoitus\nSyvään sisään ja ulos", use_container_width=True, type="primary"):
            st.session_state.current_page = "hengitys"
            st.rerun()
            
        if st.button("🤸‍♂️ Taukoliikunta\nLiikuta kehoasi", use_container_width=True):
            st.session_state.current_page = "liikunta" 
            st.rerun()
            
    with col2:
        if st.button("🌟 Tarkkaavaisuus\nHuomaa ympärilläsi", use_container_width=True):
            st.session_state.current_page = "mindfulness"
            st.rerun()
            
        if st.button("🎵 Rauhoittava musiikki\nKuuntele rauhallisia ääniä", use_container_width=True):
            st.session_state.current_page = "musiikki"
            st.rerun()

def hengitysharjoitus():
    """Hengitysharjoitus rauhoittumiseen"""
    st.markdown('<h1 class="main-header">💨 Hengitysharjoitus</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin keskittymishetkeen"):
        st.session_state.current_page = "keskittyminen"
        st.rerun()
    
    # Hengitysohje
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #1ABC9C, #16A085); border-radius: 20px; margin: 2rem 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
        <h2 style='font-size: 1.8rem; margin-bottom: 1.5rem;'>🌊 Rauhoittava hengitysharjoitus</h2>
        <p style='font-size: 1.3rem; line-height: 1.6;'>
            Seuraa näitä ohjeita rauhallisesti:<br><br>
            <strong>1.</strong> Istu mukavasti ja sulje silmäsi<br>
            <strong>2.</strong> Hengitä syvään sisään nenän kautta (4 sekuntia)<br>
            <strong>3.</strong> Pidätä hengitystä hetki (2 sekuntia)<br> 
            <strong>4.</strong> Hengitä hitaasti ulos suun kautta (6 sekuntia)<br>
            <strong>5.</strong> Toista tätä 5 kertaa
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Aloita hengitysharjoitus
    if 'hengitys_kaynnissa' not in st.session_state:
        st.session_state.hengitys_kaynnissa = False
        st.session_state.hengitys_vaihe = "valmis"
        st.session_state.hengitys_aika = 0
    
    if not st.session_state.hengitys_kaynnissa:
        if st.button("🌬️ Aloita hengitysharjoitus", type="primary", use_container_width=True):
            st.session_state.hengitys_kaynnissa = True
            st.session_state.hengitys_vaihe = "sisään"
            st.session_state.hengitys_aika = time.time()
            st.rerun()
    else:
        # Yksinkertainen ja selkeä hengityksen ohjaus
        kulunut = time.time() - st.session_state.hengitys_aika
        
        if st.session_state.hengitys_vaihe == "sisään" and kulunut >= 4:
            st.session_state.hengitys_vaihe = "pidätä"
            st.session_state.hengitys_aika = time.time()
        elif st.session_state.hengitys_vaihe == "pidätä" and kulunut >= 2:
            st.session_state.hengitys_vaihe = "ulos" 
            st.session_state.hengitys_aika = time.time()
        elif st.session_state.hengitys_vaihe == "ulos" and kulunut >= 6:
            st.session_state.hengitys_vaihe = "sisään"
            st.session_state.hengitys_aika = time.time()
        
        # Yksinkertainen visuaalinen ohje ilman monimutkkaista animaatiota
        if st.session_state.hengitys_vaihe == "sisään":
            pallo_emoji = "🔵"  # Sininen pallo
            pallo_koko = "Iso"
            ohje_teksti = "🌬️ Hengitä SISÄÄN nenän kautta..."
            ohje_vari = "#1ABC9C"
            tausta_vari = "linear-gradient(135deg, #1ABC9C, #16A085)"
        elif st.session_state.hengitys_vaihe == "pidätä":
            pallo_emoji = "🟡"  # Keltainen pallo
            pallo_koko = "Iso"
            ohje_teksti = "⏸️ Pidätä hengitystä hetki..."
            ohje_vari = "#F39C12"
            tausta_vari = "linear-gradient(135deg, #F39C12, #D68910)"
        else:  # ulos
            pallo_emoji = "🔴"  # Punainen pallo
            pallo_koko = "Pieni"
            ohje_teksti = "💨 Hengitä ULOS suun kautta..."
            ohje_vari = "#E67E22"
            tausta_vari = "linear-gradient(135deg, #E67E22, #CA6F1E)"
        
        # Näytä selkeä visuaalinen ohje
        st.markdown(f"""
        <div style='text-align: center; margin: 3rem 0;'>
            <div style='
                background: {tausta_vari};
                padding: 3rem;
                border-radius: 20px;
                margin: 2rem 0;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            '>
                <div style='font-size: 6rem; margin-bottom: 1rem;'>
                    {pallo_emoji}
                </div>
                <div style='
                    font-size: 1.8rem; 
                    color: white; 
                    font-weight: bold; 
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                    margin: 1rem 0;
                '>
                    {ohje_teksti}
                </div>
                <div style='
                    font-size: 1.3rem; 
                    color: white; 
                    opacity: 0.9;
                    margin-top: 1rem;
                '>
                    Pallo: {pallo_koko} • {int(kulunut)} sekuntia
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
            
        if st.button("⏹️ Lopeta harjoitus", use_container_width=True):
            st.session_state.hengitys_kaynnissa = False
            st.session_state.pisteet += 10
            tallenna_edistyminen()
            st.success("Hienoa! Sait 10 pistettä rauhoittumisesta! 🌟")
            st.rerun()
            
        # Auto-refresh - hitaammin ja tasaisemmin
        time.sleep(1)  # Pidempi tauko
        st.rerun()

def mindfulness_harjoitus():
    """Tarkkaavaisuus/mindfulness-harjoitus"""
    st.markdown('<h1 class="main-header">🌟 Tarkkaavaisuusharjoitus</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin keskittymishetkeen"):
        st.session_state.current_page = "keskittyminen"
        st.rerun()
    
    # Mindfulness-ohje
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #F39C12, #D68910); border-radius: 20px; margin: 2rem 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
        <h2 style='font-size: 1.8rem; margin-bottom: 1.5rem;'>🧘‍♀️ Tarkkaavaisuusharjoitus</h2>
        <p style='font-size: 1.2rem; line-height: 1.6;'>
            Ole tässä hetkessä ja huomaa ympärilläsi:<br><br>
            <strong>👀 Näe:</strong> 5 asiaa, jotka näet ympärilläsi<br>
            <strong>👂 Kuule:</strong> 4 ääntä, jotka kuulet<br>
            <strong>🤲 Tunne:</strong> 3 asiaa, joihin kosketat<br>
            <strong>👃 Haista:</strong> 2 tuoksua ilmassa<br>
            <strong>👅 Maista:</strong> 1 maku suussasi
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Harjoituksen vaiheet
    mindfulness_asiat = [
        ("👀 Näe 5 asiaa", "Katso ympärillesi ja nimeä 5 asiaa, jotka näet"),
        ("👂 Kuule 4 ääntä", "Kuuntele tarkasti ja tunnista 4 ääntä"),  
        ("🤲 Tunne 3 asiaa", "Kosketa 3 asiaa ja tunne niiden tekstuuri"),
        ("👃 Haista 2 tuoksua", "Hengitä syvään ja huomaa 2 tuoksua"),
        ("👅 Maista 1 asia", "Keskity makuun, joka on suussasi nyt")
    ]
    
    for i, (otsikko, ohje) in enumerate(mindfulness_asiat):
        if st.button(f"{otsikko}", use_container_width=True, key=f"mindful_{i}"):
            st.info(f"✨ {ohje}")
            st.session_state.pisteet += 2
            tallenna_edistyminen()
    
    if st.button("🌟 Olen valmis! Suoritin harjoituksen", type="primary", use_container_width=True):
        st.session_state.pisteet += 15
        tallenna_edistyminen()
        st.success("Mahtavaa! Olit todella tarkkaavainen! Sait 15 pistettä! 🎉")
        st.balloons()

def rauhoittava_musiikki():
    """Rauhoittava musiikki ja äänet"""
    st.markdown('<h1 class="main-header">🎵 Rauhoittava musiikki</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin keskittymishetkeen"):
        st.session_state.current_page = "keskittyminen"
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #8E44AD, #732D91); border-radius: 20px; margin: 2rem 0; color: white; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
        <h2 style='font-size: 1.8rem; margin-bottom: 1.5rem;'>🎼 Rauhoittavat äänet</h2>
        <p style='font-size: 1.2rem; line-height: 1.6;'>
            Kuuntele näitä rauhallisia ääniä rentoutuaksesi.<br>
            Voit kuvitella olevasi näissä paikoissa.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Valinta audio/video
    st.markdown("### 🎧 Valitse tila:")
    audio_tai_video = st.radio("Valitse toistotila", ["🔊 Vain ääni (suositeltu mobiiliin)", "📹 Video + ääni"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("### Valitse rauhoittava ääni:")
    
    # Musiikkivaihtoehdot upotettuina
    musiikit = [
        ("🌊 Meren aaltojen ääni", "WHPEKLQID4U", "Kuvittele olevasi rannalla kuuntelemassa aaltoja"),
        ("🌧️ Sateen ropina", "q76bMs-NwRk", "Rauhallinen sateen ääni ikkunassa"),
        ("🐦 Lintujen laulu", "LYekcN76hF4", "Kauniita laulavia lintuja puistossa"),
        ("🔥 Takkatuli putoilee", "L_LUpnjgPso", "Lämmin takkatuli särisee rauhallisesti"),
        ("🌳 Metsän äänet", "xNN7iTA57jM", "Tuulen huminaa lehvistössä"),
        ("🎼 Pehmeä pianomusiikki", "1ZYbU82GVz4", "Rauhallinen klassinen piano")
    ]
    
    for nimi, video_id, kuvaus in musiikit:
        if st.button(nimi, use_container_width=True):
            st.info(f"🎧 {kuvaus}")
            
            # Upotettava YouTube-video
            if "📹 Video" in audio_tai_video:
                # Video näkyvissä
                video_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&loop=1&playlist={video_id}"
                st.markdown(f"""
                <div style='text-align: center; margin: 1rem 0;'>
                    <iframe width="100%" height="315" 
                    src="{video_url}" 
                    frameborder="0" 
                    allow="autoplay; encrypted-media" 
                    allowfullscreen>
                    </iframe>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Vain ääni - pienempi pelaaja
                video_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&loop=1&playlist={video_id}&controls=1"
                st.markdown(f"""
                <div style='text-align: center; margin: 1rem 0;'>
                    <iframe width="100%" height="120" 
                    src="{video_url}" 
                    frameborder="0" 
                    allow="autoplay; encrypted-media">
                    </iframe>
                    <p style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>
                        💡 Voit säätää äänenvoimakkuutta videon ohjaimista, tai laitteestasi.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.session_state.pisteet += 3
            tallenna_edistyminen()
            st.success("Hienoa! Nauti rauhoittavista äänistä! +3 pistettä 🎶")
            
    st.markdown("---")
    
    
    if st.button("😌 Olen rauhoittunut musiikilla", type="primary", use_container_width=True):
        st.session_state.pisteet += 10 
        tallenna_edistyminen()
        st.success("Mahtavaa! Rauhoittuminen on tärkeä taito! Sait 10 pistettä! 🎶")
        st.balloons()

def taukoliikunta():
    """Taukoliikunta-harjoitukset"""
    st.markdown('<h1 class="main-header">🤸‍♂️ Taukoliikunta</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin päävalikkoon"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    # Liikuntaharjoitukset (desktop-versiosta)
    liikunta_harjoitukset = [
        ("Hyppele paikallaan", "10 kertaa ylös-alas!"),
        ("Nosta kädet ylös", "Venyttele korkealle 5 kertaa!"),
        ("Pyörittele olkapäitä", "Eteen ja taakse 5 kertaa!"),
        ("Taputtele käsiä", "10 taputusta!"),
        ("Nosta polvia", "Vuorotellen 10 kertaa!"),
        ("Tähtihypyt", "Avaa ja sulje kädet ja jalat 5 kertaa!"),
        ("Pyöri ympäri", "3 kierrosta hitaasti!"),
        ("Venyttele sormia", "Avaa ja sulje nyrkki 10 kertaa!")
    ]
    
    # Alusta harjoitus
    if 'liikunta_harjoitus' not in st.session_state:
        st.session_state.liikunta_harjoitus = None
        st.session_state.liikunta_aika = 15
        st.session_state.liikunta_kaynnissa = False
        st.session_state.liikunta_aloitusaika = None
    
    # Keskitetty näkymä
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎲 Uusi harjoitus", type="primary", use_container_width=True):
            st.session_state.liikunta_harjoitus = random.choice(liikunta_harjoitukset)
            st.session_state.liikunta_aika = 15
            st.session_state.liikunta_kaynnissa = False
            st.session_state.liikunta_aloitusaika = None
        
        if st.session_state.liikunta_harjoitus:
            harjoitus = st.session_state.liikunta_harjoitus
            
            # Näytä harjoitus
            st.markdown(f"""
            <div style='text-align: center; background: linear-gradient(135deg, #FADBD8, #F8C471); padding: 3rem; border-radius: 20px; margin: 2rem 0; box-shadow: 0 6px 12px rgba(0,0,0,0.1);'>
                <h2 style='color: #C0392B; font-size: 1.8rem; margin-bottom: 1rem;'>🏃‍♂️ {harjoitus[0]}</h2>
                <p style='font-size: 1.3rem; color: #922B21; font-weight: bold;'>{harjoitus[1]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Lasketaan jäljellä oleva aika
            if st.session_state.liikunta_kaynnissa and st.session_state.liikunta_aloitusaika:
                kulunut_aika = time.time() - st.session_state.liikunta_aloitusaika
                jaljella = max(0, 15 - int(kulunut_aika))
                
                if jaljella == 0:
                    st.session_state.liikunta_kaynnissa = False
                    st.success("⏰ Aika loppui! Hienoa työtä! 🎉")
                    st.balloons()
            else:
                jaljella = 15
            
            # Ajastin väri
            if st.session_state.liikunta_kaynnissa:
                timer_color = "#E74C3C" if jaljella <= 5 else "#D35400"
            else:
                timer_color = "#D35400"
            
            # Näytä ajastin
            st.markdown(f"""
            <div style='text-align: center; font-size: 2.5rem; color: {timer_color}; font-weight: bold; margin: 1.5rem 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                ⏱️ {jaljella} sekuntia
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            if st.session_state.liikunta_kaynnissa and st.session_state.liikunta_aloitusaika:
                progress_value = (kulunut_aika / 15)
                st.progress(min(1.0, progress_value))
            
            # Napit
            col_a, col_b = st.columns(2)
            
            with col_a:
                if not st.session_state.liikunta_kaynnissa:
                    if st.button("🚀 Aloita liikunta!", use_container_width=True, type="primary"):
                        st.session_state.liikunta_kaynnissa = True
                        st.session_state.liikunta_aloitusaika = time.time()
                        st.balloons()
                        st.rerun()
                else:
                    if st.button("⏸️ Pysäytä", use_container_width=True):
                        st.session_state.liikunta_kaynnissa = False
                        st.session_state.liikunta_aloitusaika = None
                        st.rerun()
                    
            with col_b:
                if st.button("✅ Suoritettu!", use_container_width=True):
                    st.session_state.pisteet += 5
                    st.session_state.suoritetut_tehtavat += 1
                    st.session_state.oikeat_vastaukset += 1
                    st.session_state.liikunta_kaynnissa = False
                    st.session_state.liikunta_aloitusaika = None
                    tallenna_edistyminen()
                    st.success("Hienoa liikuntaa! Sait 5 pistettä! 💪")
                    st.rerun()
            
            # Ohjeistus ja automaattinen päivitys
            if st.session_state.liikunta_kaynnissa:
                st.info("💪 Tee harjoitus ajastimen mukaan! Aika tikittää...")
                # Päivitä sivu sekunnin välein kun ajastin käynnissä
                time.sleep(1)
                st.rerun()
            else:
                st.info("🎯 Paina 'Aloita liikunta!' niin ajastin käynnistyy!")

def sosiaaliset_taidot():
    """Sosiaaliset taidot - Tilanteen käsittely"""
    st.markdown('<h1 class="main-header">🤝 Sosiaaliset taidot</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin päävalikkoon"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    # Tilanteet desktop-versiosta
    tilanteet = [
        {
            "tilanne": "Kaveri kiusaa sinua koulussa",
            "vaihtoehdot": [
                "Lyön takaisin heti",
                "Kerron opettajalle asiasta",
                "Jätän väliin ja menen pois"
            ],
            "oikea": 1,
            "selitys": "Opettajalle kertominen on viisasta! Aikuiset voivat auttaa ratkaisemaan kiusaamisen turvallisesti. Väkivalta vain pahentaa tilannetta."
        },
        {
            "tilanne": "En halua noudattaa sääntöjä kotona",
            "vaihtoehdot": [
                "Uhmaan ja teen mitä haluan", 
                "Puhun vanhempien kanssa miksi sääntö tuntuu vaikealta",
                "Katoan huoneeseeni ääntelemättä"
            ],
            "oikea": 1,
            "selitys": "Avoin keskustelu on parasta! Vanhemmat voivat selittää sääntöjen tarkoituksen ja ehkä löydetään yhdessä ratkaisu."
        },
        {
            "tilanne": "Haluan läpsiä kaveria leikkimielisesti",
            "vaihtoehdot": [
                "Läpsin vaikka kaveri ei tykkäisi",
                "Kysyn ensin: 'Saanko läpsiä sinua leikissä?'", 
                "En läpsi, vaan keksin muun tavan leikkiä"
            ],
            "oikea": 2,
            "selitys": "Fyysistä kontaktia ei kannata harrastaa edes leikissä! Joskus leikkimielinen läpsiminen voi johtaa väärään käsitykseen. On turvallisempaa keksiä muita tapoja leikkiä yhdessä."
        },
        {
            "tilanne": "Haluan olla koko ajan kaverin vieressä",
            "vaihtoehdot": [
                "Seuraan kaveriani kaikkialle",
                "Annan kaverille tilaa ja löydän myös muuta tekemistä",
                "Suutun jos kaveri haluaa olla muiden kanssa"
            ],
            "oikea": 1,
            "selitys": "Jokaisella on oikeus omaan tilaan! Hyvä ystävyys antaa tilaa toisillekin ystäville ja harrastuksille. Se tekee ystävyydestä vahvempaa."
        },
        {
            "tilanne": "Kaveri ei halua lainata minulle leluaan",
            "vaihtoehdot": [
                "Otan lelun väkisin",
                "Hyväksyn kaverin päätöksen ja etsin muuta tekemistä",
                "Valitan niin kauan kunnes kaveri antaa lelun"
            ],
            "oikea": 1,
            "selitys": "Jokainen saa päättää omista tavaroistaan! Kunnioita kaverin päätöstä. Ehkä voitte keksiä yhdessä jotain muuta mukavaa."
        },
        {
            "tilanne": "Olen vihainen opettajalle",
            "vaihtoehdot": [
                "Huudan opettajalle luokassa",
                "Otan syvään henkeä ja puhun asiasta rauhallisesti myöhemmin",
                "En puhu opettajalle enää koskaan"
            ],
            "oikea": 1,
            "selitys": "Tunteet ovat okei, mutta niitä voi käsitellä viisaasti! Hengitä syvään ja puhu asiat läpi rauhallisesti. Aikuiset arvostavat kypsää keskustelua."
        },
        {
            "tilanne": "Kaverini tekee jotain vaarallista",
            "vaihtoehdot": [
                "Teen samoin että en jää ulkopuolelle",
                "Kerron aikuiselle koska olen huolissani kaveristani", 
                "En välitä, jokainen tekee mitä haluaa"
            ],
            "oikea": 1,
            "selitys": "Oikeat kaverit välittävät toisistaan! Aikuiselle kertominen ei ole paljastamista vaan huolenpitoa. Turvallisuus on tärkeämpää kuin mukana olo."
        },
        {
            "tilanne": "En osaa tehtävää koulussa",
            "vaihtoehdot": [
                "Jätän tehtävän tekemättä ja toivon ettei kukaan huomaa",
                "Pyydän apua opettajalta tai kavereilta",
                "Ärsyynnyn ja häiritsen muita kun en osaa"
            ],
            "oikea": 1,
            "selitys": "Avun pyytäminen on rohkeutta, ei heikkoutta! Opettajat ja kaverit haluavat auttaa. Kun pyydät apua, opit uutta ja kasvat ihmisenä."
        }
    ]
    
    # Alusta peli
    if 'social_scenario' not in st.session_state:
        st.session_state.social_scenario = None
        st.session_state.social_feedback = ""
    
    # Keskitetty näkymä
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("### Mitä voisi tapahtua jos teet näin? Valitse parhaiten sopiva vaihtoehto:")
        
        if st.button("🎭 Uusi tilanne", type="primary", use_container_width=True):
            st.session_state.social_scenario = random.choice(tilanteet)
            st.session_state.social_feedback = ""
        
        if st.session_state.social_scenario:
            scenario = st.session_state.social_scenario
            
            # Näytä tilanne
            st.markdown(f"""
            <div style='text-align: center; background: white; padding: 2rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='color: #8E44AD; font-size: 1.4rem; margin-bottom: 1rem;'>🤔 Tilanne:</h3>
                <p style='font-size: 1.2rem; color: #333; font-weight: bold;'>{scenario['tilanne']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Vastausvaihtoehdot
            st.markdown("### Mitä teet?")
            choice = st.radio("", scenario['vaihtoehdot'], key="social_choice", 
                            label_visibility="collapsed")
            
            if st.button("Vastaa", type="primary", use_container_width=True):
                chosen_index = scenario['vaihtoehdot'].index(choice)
                if chosen_index == scenario['oikea']:
                    st.session_state.pisteet += 25
                    st.session_state.suoritetut_tehtavat += 1
                    st.session_state.oikeat_vastaukset += 1
                    st.session_state.social_feedback = f"🌟 Loistavaa! {scenario['selitys']} Sait 25 pistettä!"
                    tallenna_edistyminen()
                else:
                    st.session_state.suoritetut_tehtavat += 1
                    st.session_state.social_feedback = f"🤔 Mieti uudelleen. {scenario['selitys']}"
                    tallenna_edistyminen()
            
            # Näytä palaute
            if st.session_state.social_feedback:
                if "Loistavaa" in st.session_state.social_feedback:
                    st.success(st.session_state.social_feedback)
                else:
                    st.info(st.session_state.social_feedback)

def edistymis_raportti():
    """Näyttää edistymisraportin"""
    st.markdown('<h1 class="main-header">📊 Edistymisraportti</h1>', unsafe_allow_html=True)
    
    if st.button("← Takaisin päävalikkoon"):
        st.session_state.current_page = "menu"
        st.rerun()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pisteet yhteensä", st.session_state.pisteet)
    
    with col2:
        st.metric("Suoritetut tehtävät", st.session_state.suoritetut_tehtavat)
    
    with col3:
        if st.session_state.suoritetut_tehtavat > 0:
            prosentti = round((st.session_state.oikeat_vastaukset / st.session_state.suoritetut_tehtavat) * 100)
            st.metric("Onnistumisprosentti", f"{prosentti}%")
        else:
            st.metric("Onnistumisprosentti", "0%")
    
    # Kannustava viesti
    if st.session_state.pisteet > 100:
        st.success("🌟 Loistavaa työtä! Olet todellinen oppimistähti!")
    elif st.session_state.pisteet > 50:
        st.info("👏 Hienoa edistystä! Jatka samaan malliin!")
    elif st.session_state.pisteet > 0:
        st.info("💪 Hyvä alku! Jatka harjoittelua!")
    else:
        st.info("🚀 Aloita seikkailusi suorittamalla tehtäviä!")

# Pääsovellus
def main():
    """Pääfunktio"""
    
    # Copyright-suojaus
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; font-size: 0.8rem; color: #666;'>
        <p>© 2025 Laura - Oppimisseikkailu<br>
        Kaikki oikeudet pidätetään.<br>
        Tämä sovellus on tekijänoikeussuojattu.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_page == "nimi":
        nimi_sivu()
    elif st.session_state.current_page == "menu":
        paa_menu()
    elif st.session_state.current_page == "matematiikka":
        matematiikka_peli()
    elif st.session_state.current_page == "raportti":
        edistymis_raportti()
    elif st.session_state.current_page == "lukeminen":
        lukemis_peli()
    elif st.session_state.current_page == "tunteet":
        tunteiden_kasittely()
    elif st.session_state.current_page == "liikunta":
        taukoliikunta()
    elif st.session_state.current_page == "sosiaaliset":
        sosiaaliset_taidot()
    elif st.session_state.current_page == "keskittyminen":
        keskittymishetki()
    elif st.session_state.current_page == "hengitys":
        hengitysharjoitus()
    elif st.session_state.current_page == "mindfulness":
        mindfulness_harjoitus()
    elif st.session_state.current_page == "musiikki":
        rauhoittava_musiikki()
    elif st.session_state.current_page == "ohje":
        ohje_sivu()
    else:
        st.error("Sivu ei ole vielä valmis! Palaa päävalikkoon.")
        if st.button("← Takaisin päävalikkoon"):
            st.session_state.current_page = "menu"
            st.rerun()

def ohje_sivu():
    """Tarina ja ohjeet sovelluksesta"""
    st.title("💝 Oppimisseikkailu - Tarina & Ohjeet")
    
    if st.button("← Takaisin"):
        if st.session_state.kayttaja_nimi:
            st.session_state.current_page = "menu"
        else:
            st.session_state.current_page = "nimi"
        st.rerun()
    
    st.markdown("---")
    
    # Tarina
    st.subheader("❤️ Miksi tämä sovellus syntyi?")
    
    st.markdown("""
    **Tämä sovellus syntyi äidin rakkaudesta** ja tarpeesta auttaa omaa poikaa. 
    
    Huomasin arjessa, miten vaikeaa keskittyminen ja oppiminen voi olla, kun aivot toimivat eri tavalla. 
    Perinteiset oppimismenetelmät tuntuivat liian raskailta, ja tarvitsimme jotain **lempeämpää, mukavampaa ja rohkaisevampaa**.
    
    Aloin kehittää sovellusta, joka **ymmärtää lapsen tarpeet**:
    
    - 🕐 **Lyhyet sessiot** - ei väsytä keskittymistä
    - 🎉 **Välitön palaute** - kannustaa jatkamaan  
    - 🌈 **Visuaalisuus** - tukee oppimista
    - 💪 **Positiivisuus** - rakentaa itsetuntoa
    - 🧘‍♀️ **Rauhoittuminen** - hallitsee stressiä
    
    > *"Halusin luoda turvallisen paikan, jossa jokainen lapsi voi oppia omaan tahtiin ja löytää onnistumisen iloa."*
    """)
    
    st.markdown("---")
    
    # Kenelle tarkoitettu
    st.subheader("🎯 Kenelle tämä on tarkoitettu?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📚 Erityisesti:**")
        st.markdown("""
        - Lapsille, joilla on **keskittymisvaikeuksia**
        - ADHD-diagnoosin saaneille lapsille
        - Lapsille, jotka tarvitsevat **rauhallisemman oppimisympäristön**
        - Oppimisvaikeuksien kanssa kamppaileville
        """)
    
    with col2:
        st.markdown("**🌟 Mutta myös:**")
        st.markdown("""
        - Kaikille lapsille, jotka haluavat oppia leikkien
        - Vanhemmille, jotka etsivät **turvallista opiskeluapua**
        - Opettajille täydentävänä työkaluna
        - Perheille, jotka haluavat **positiivista oppimista** kotona
        """)
    
    st.markdown("---")
    
    # Käyttöohjeet
    st.subheader("📖 Miten käyttää?")
    
    st.markdown("""
    **1. 📝 Aloita nimellä** - Anna lapselle oma käyttäjätunnus
    
    **2. 🎮 Valitse peli** - 5 erilaista oppimisaluetta
    
    **3. 🏆 Kerää pisteitä** - Jokainen yritys palkitaan
    
    **4. 📊 Seuraa edistymistä** - Katso kuinka hyvin menee
    
    **5. 💆‍♀️ Rauhoitu tarpeen mukaan** - Käytä keskittymisharjoituksia
    """)
    
    st.info("💡 **Vinkki vanhemmille:** Istukaa lapsen viereen ensimmäisillä kerroilla. Kannustakaa ja juhlitaan yhdessä onnistumisia - pienetkin ovat tärkeitä! 🎉")
    
    st.markdown("---")
    
    # Turvallisuus
    st.subheader("🔒 Turvallisuus & Yksityisyys")
    
    st.markdown("""
    - ✅ Ei kerää henkilötietoja internetiin
    - ✅ Ei mainoksia tai häiritseviä elementtejä
    - ✅ Lapsiystävällinen ja turvallinen ympäristö
    - ✅ Edistyminen tallennetaan vain laitteelle
    - ✅ Ei maksullista sisältöä tai yllätyksiä
    """)
    
    st.markdown("---")
    
    # Tekijänoikeussuojaus
    st.subheader("⚖️ Tekijänoikeudet & Käyttöehdot")
    
    st.warning("""
    **© 2025 Laura - Kaikki oikeudet pidätetään**
    
    🛡️ Tämä sovellus on tekijänoikeussuojattu. Henkilökohtainen käyttö sallittu. 
    Kopiointi, jakelu tai kaupallinen käyttö kielletty ilman lupaa.
    
    📧 Lisenssikysymykset: laura.makila@lauramakila.fi
    """)

if __name__ == "__main__":
    main()