import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. UI/UX SETUP (Rieber Design)
# ==========================================
st.set_page_config(page_title="Rieber Lösungs-Konfigurator", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Hintergrundbild (Muss background.jpg heißen) */
    .stApp {
        background-image: url('background.jpg'); 
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* Eingabebereich Styling */
    .eingabe-box {
        background-color: rgba(240, 248, 248, 0.95);
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #004e54;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .stButton>button { background-color: #004e54 !important; color: white !important; font-weight: bold; }
    .result-card { 
        background-color: white; padding: 15px; border-radius: 10px; 
        border: 1px solid #004e54; text-align: center; height: 100%;
    }
    .metric-title { color: #004e54; font-weight: bold; font-size: 1.1em; }
    .metric-value { font-size: 1.8em; font-weight: bold; color: #333; margin: 0; }
    .price-value { font-size: 1.5em; color: #d9534f; font-weight: bold; } 
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='color: #004e54; margin-bottom: 0;'>Lösungs-Konfigurator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #555; margin-top: 0;'>Planungstool für Speisenverteilung</h3>", unsafe_allow_html=True)

# ==========================================
# 2. EINGABEMASKE
# ==========================================
with st.container():
    st.markdown("<div class='eingabe-box'>", unsafe_allow_html=True)
    
    st.subheader("1. Systemparameter")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: anwendung = st.selectbox("Anwendungsbereich", ["Kita", "Schule", "Altenheim", "Betrieb"])
    with c2: verfahren = st.selectbox("Verfahren", ["Cook & Chill", "Cook & Hold"])
    with c3: komponenten = st.selectbox("Komponenten", ["3-Komp.", "4-Komp."])
    with c4: tage = st.number_input("Tage/Woche", min_value=1, max_value=7, value=5)
    with c5: personen_ist = st.number_input("Personen", min_value=1, value=150)
    with c6: puffer = st.number_input("Umlauf-Faktor (%)", min_value=0, value=20) / 100
    
    st.markdown("---")
    
    st.subheader("2. Kaufmännische Parameter")
    k1, k2, k3 = st.columns(3)
    with k1: kundengruppe = st.selectbox("Kundengruppe", ["Endkunde", "Fachhandel", "Großkunde"])
    with k2: preis_anpassung = st.number_input("Projekt-Zu/Abschlag (%)", value=0.0, step=0.1)
    with k3: einweg_kosten = st.number_input("Einweg-Kosten (€/Portion)", value=0.30, step=0.05)
            
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. LOGIK & BERECHNUNG (1-zu-1 aus ODS)
# ==========================================
def get_kalk_personen(p):
    for s in [10, 12, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500]:
        if p <= s: return s
    return p

calc_p = get_kalk_personen(personen_ist)
# Grammaturen je nach Zielgruppe
gramm_map = {"Kita": 280, "Schule": 360, "Altenheim": 435, "Betrieb": 430}
vol_l = (gramm_map[anwendung] * calc_p) / 1000
anz_gn = math.ceil(vol_l / 5) # 5L Kapazität pro GN 1/1 65mm
anz_gn_final = math.ceil(anz_gn * (1 + puffer))
# DEINE KORREKTUR: 5x GN 1/1 65mm pro thermoport 4.0
anz_tp = math.ceil(anz_gn_final / 5)

# Kaufmännische Berechnung
p_gn, p_dk, p_tp = 35.00, 15.00, 850.00 # Brutto-Listenpreise
rabatt = 0.3 if kundengruppe == "Fachhandel" else (0.4 if kundengruppe == "Großkunde" else 0.0)

def netto(lp):
    return round(lp * (1 - rabatt) * (1 + (preis_anpassung / 100)), 2)

n_gn, n_dk, n_tp = netto(p_gn), netto(p_dk), netto(p_tp)
invest = (anz_gn_final * (n_gn + n_dk)) + (anz_tp * n_tp)

# ROI & Nachhaltigkeit
einweg_jahr = einweg_kosten * personen_ist * tage * 52
amort_monat = (invest / (einweg_kosten * personen_ist)) / (tage * 4.33) if einweg_kosten > 0 else 0
plastik_jahr = personen_ist * 0.03 * tage * 52
co2_jahr = plastik_jahr * 3.5

# ==========================================
# 4. AUSGABE
# ==========================================
st.header("Konfiguration & Investition")
r1, r2, r3 = st.columns(3)
with r1: st.markdown(f'<div class="result-card"><p class="metric-title">thermoport®</p><p class="metric-value">{anz_tp} Stk.</p><p>à {n_tp:.2f} €</p></div>', unsafe_allow_html=True)
with r2: st.markdown(f'<div class="result-card"><p class="metric-title">GN-Behälter Sets</p><p class="metric-value">{anz_gn_final} Stk.</p><p>à {n_gn+n_dk:.2f} €</p></div>', unsafe_allow_html=True)
with r3: st.markdown(f'<div class="result-card"><p class="metric-title">Investition (Netto)</p><p class="price-value">{invest:,.2f} €</p></div>', unsafe_allow_html=True)

st.markdown("---")
st.header("Business Case & Nachhaltigkeit")
c_roi, c_esg = st.columns(2)
with c_roi:
    st.subheader("Finanzielle Amortisation")
    st.info(f"Die Lösung amortisiert sich nach ca. **{amort_monat:.1f} Monaten**.")
with c_esg:
    st.subheader("Umwelt-Impact")
    st.success(f"Einsparung: **{plastik_jahr:,.0f} kg Plastik** und **{co2_jahr:,.0f} kg CO2** pro Jahr.")
