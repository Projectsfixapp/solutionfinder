import streamlit as st
import pandas as pd
import math
import base64
from fpdf import FPDF

# --- FUNKTIONEN FÜR DESIGN ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_design():
    try:
        bg_base64 = get_base64('background.jpg')
        logo_base64 = get_base64('logo.png')
        design_html = f'''
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_base64}");
            background-size: cover; background-repeat: no-repeat; background-attachment: fixed;
        }}
        .logo-container {{ text-align: center; margin-bottom: 20px; background: rgba(255,255,255,0.8); padding: 10px; border-radius: 10px; }}
        .eingabe-box {{ background-color: rgba(240, 248, 248, 0.95); padding: 20px; border-radius: 8px; border-top: 4px solid #004e54; margin-bottom: 20px; }}
        .result-card {{ background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #004e54; text-align: center; margin-bottom: 10px; }}
        </style>
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" width="200">
        </div>
        '''
        st.markdown(design_html, unsafe_allow_html=True)
    except:
        st.title("Rieber Solutionfinder")

# --- PDF GENERIERUNG ---
def create_pdf(data_list, gesamt_invest):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Rieber Stückliste & Bedarfsanalyse", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    for item in data_list:
        pdf.cell(200, 10, txt=item, ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Gesamtinvestition Netto: {gesamt_invest:,.2f} EUR", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- APP SETUP ---
st.set_page_config(page_title="Rieber META cooking Solutionfinder", layout="wide")
set_design()

# --- STANDORT-EINGABE ---
st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
st.subheader("1. Standort-Bedarfsplanung")
num_locations = st.number_input("Anzahl der Standorte", min_value=1, value=1)

locations = []
total_persons = 0
for i in range(int(num_locations)):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Name Standort {i+1}", value=f"Standort {i+1}")
    with col2:
        count = st.number_input(f"Essensteilnehmer {name}", min_value=1, value=50)
    locations.append({"name": name, "count": count})
    total_persons += count
st.markdown('</div>', unsafe_allow_html=True)

# --- SYSTEM-PARAMETER ---
st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
st.subheader("2. System & Konditionen")
c1, c2, c3 = st.columns(3)
with c1:
    verfahren = st.selectbox("Verfahren", ["Cook & Chill", "Cook & Hold"])
    tage = st.number_input("Tage/Woche", value=5)
with c2:
    anwendung = st.selectbox("Bereich", ["Kita", "Schule", "Altenheim", "Betrieb"])
    puffer = st.number_input("Umlauf-Puffer (%)", value=20) / 100
with c3:
    kundengruppe = st.selectbox("Kundengruppe", ["Endkunde", "Fachhandel", "Großkunde"])
    rabatt_extra = st.number_input("Projekt Zu/Abschlag (%)", value=0.0)
st.markdown('</div>', unsafe_allow_html=True)

# --- BERECHNUNG ---
gramm_map = {"Kita": 280, "Schule": 360, "Altenheim": 435, "Betrieb": 430}
pro_portion = gramm_map[anwendung]

# Thermoport Modell wählen
tp_modell = "thermoport® 1000K" if verfahren == "Cook & Chill" else "thermoport® 1000KB 4.0 (beheizt)"
tp_preis_basis = 850.0 if verfahren == "Cook & Chill" else 1250.0

# Mengen pro Standort berechnen
results = []
total_tp = 0
total_gn = 0
total_rp = 0

for loc in locations:
    # Kapazitäts-Check
    vol_l = (pro_portion * loc["count"]) / 1000
    gn_loc = math.ceil(vol_l / 5)
    gn_puffer = math.ceil(gn_loc * (1 + puffer))
    tp_loc = math.ceil(gn_puffer / 5)
    rp_loc = math.ceil(tp_loc / 2) # 2 Thermoporte pro Rolliport
    
    total_tp += tp_loc
    total_gn += gn_puffer
    total_rp += rp_loc
    results.append(f"{loc['name']}: {loc['count']} Essen -> {tp_loc}x {tp_modell}, {rp_loc}x Rolliport")

# Preise berechnen
rabatt_hdl = 0.3 if kundengruppe == "Fachhandel" else (0.4 if kundengruppe == "Großkunde" else 0.0)
def calc_netto(lp): return round(lp * (1 - rabatt_hdl) * (1 + (rabatt_extra/100)), 2)

n_tp = calc_netto(tp_preis_basis)
n_gn = calc_netto(35.0) # Behälter
n_dk = calc_netto(15.0) # Deckel
n_rp = calc_netto(280.0) # Rolliport

invest = (total_tp * n_tp) + (total_gn * n_gn) + (total_gn * n_dk) + (total_rp * n_rp)

# --- AUSGABE ---
st.header("Empfohlene Ausstattung (Gesamt)")
res1, res2, res3, res4 = st.columns(4)
with res1: st.markdown(f'<div class="result-card"><b>{tp_modell}</b><br><h3>{total_tp} Stk.</h3>à {n_tp:.2f}€</div>', unsafe_allow_html=True)
with res2: st.markdown(f'<div class="result-card"><b>GN-Behälter 1/1 65</b><br><h3>{total_gn} Stk.</h3>à {n_gn:.2f}€</div>', unsafe_allow_html=True)
with res3: st.markdown(f'<div class="result-card"><b>Steckdeckel (Dichtung)</b><br><h3>{total_gn} Stk.</h3>à {n_dk:.2f}€</div>', unsafe_allow_html=True)
with res4: st.markdown(f'<div class="result-card"><b>Rolliport</b><br><h3>{total_rp} Stk.</h3>à {n_rp:.2f}€</div>', unsafe_allow_html=True)

st.subheader("Investition Gesamt: " + f"{invest:,.2f} € (Netto)")

# PDF Download
pdf_list = [
    f"Verfahren: {verfahren}",
    f"Anwendung: {anwendung}",
    "--- Standorte ---"
] + results + [
    "--- Stückliste Gesamt ---",
    f"{total_tp}x {tp_modell}",
    f"{total_gn}x GN-Behälter 1/1 65mm",
    f"{total_gn}x GN-Steckdeckel mit Dichtung",
    f"{total_rp}x Rolliport"
]

pdf_data = create_pdf(pdf_list, invest)
st.download_button("Stückliste als PDF herunterladen", data=pdf_data, file_name="Rieber_Angebot.pdf", mime="application/pdf")
