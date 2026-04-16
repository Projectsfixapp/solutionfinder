# TEST-CODE: Zeigt alle Dateien auf dem Server an
st.write("Dateien auf dem Server:", os.listdir())
import streamlit as st
import pandas as pd
import math
import base64
import os
from fpdf import FPDF

# --- DESIGN FUNKTIONEN ---
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
        .logo-container {{ text-align: center; margin-bottom: 10px; padding: 10px; }}
        .eingabe-box {{ 
            background-color: rgba(240, 248, 248, 0.95); 
            padding: 20px; border-radius: 8px; 
            border-top: 4px solid #004e54; margin-bottom: 20px; 
        }}
        .result-card {{ 
            background-color: white; padding: 15px; border-radius: 10px; 
            border: 1px solid #004e54; text-align: center; height: 100%;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .roi-card {{ 
            background-color: #e8f4f4; padding: 15px; border-radius: 10px; 
            border-left: 5px solid #004e54; text-align: center; height: 100%;
        }}
        .esg-card {{ 
            background-color: #f0f9f0; padding: 15px; border-radius: 10px; 
            border-left: 5px solid #5cb85c; text-align: center; height: 100%;
        }}
        .metric-title {{ color: #004e54; font-weight: bold; margin-bottom: 5px; }}
        .metric-value {{ font-size: 1.5em; font-weight: bold; color: #333; }}
        </style>
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" width="250">
        </div>
        '''
        st.markdown(design_html, unsafe_allow_html=True)
    except:
        st.title("Rieber Solutionfinder")

# --- PDF GENERATOR ---
def create_pdf(verfahren, anwendung, total_p_day, standort_bericht, 
               tp_modell, total_tp, total_gn, total_rp, n_tp, n_gn, n_dk, n_rp, 
               invest, einweg_jahr, amort_monat, plastik_jahr, co2_jahr):
    
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Logo einbinden (falls vorhanden)
    if os.path.exists('logo.png'):
        pdf.image('logo.png', 10, 8, 60)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Rieber META cooking - Bedarfsanalyse & ROI", ln=True, align='C')
    pdf.ln(10)
    
    # 2. Projekt-Parameter
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="1. Projekt-Parameter", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, txt=f"Verfahren: {verfahren}", ln=True)
    pdf.cell(0, 6, txt=f"Anwendungsbereich: {anwendung}", ln=True)
    pdf.cell(0, 6, txt=f"Essensteilnehmer Gesamt: {total_p_day} Personen pro Tag", ln=True)
    pdf.ln(5)
    
    # 3. Standort-Aufteilung
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="2. Standort-Aufteilung", ln=True)
    pdf.set_font("Arial", '', 11)
    for loc_text in standort_bericht:
        pdf.cell(0, 6, txt=f"- {loc_text}", ln=True)
    pdf.ln(5)
    
    # 4. Stückliste (ordentlich formatiert)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="3. Empfohlene Ausstattung (Stueckliste)", ln=True)
    pdf.set_font("Arial", '', 11)
    
    # Formatierte Liste mit Abständen
    pdf.cell(30, 6, txt=f"{total_tp} Stk.", border=0)
    pdf.cell(90, 6, txt=f"{tp_modell}", border=0)
    pdf.cell(0, 6, txt=f"à {n_tp:,.2f} EUR", border=0, ln=True)
    
    pdf.cell(30, 6, txt=f"{total_gn} Stk.", border=0)
    pdf.cell(90, 6, txt="GN-Behaelter 1/1 65mm", border=0)
    pdf.cell(0, 6, txt=f"à {n_gn:,.2f} EUR", border=0, ln=True)
    
    pdf.cell(30, 6, txt=f"{total_gn} Stk.", border=0)
    pdf.cell(90, 6, txt="GN-Steckdeckel (Dichtung)", border=0)
    pdf.cell(0, 6, txt=f"à {n_dk:,.2f} EUR", border=0, ln=True)
    
    pdf.cell(30, 6, txt=f"{total_rp} Stk.", border=0)
    pdf.cell(90, 6, txt="Rolliport", border=0)
    pdf.cell(0, 6, txt=f"à {n_rp:,.2f} EUR", border=0, ln=True)
    
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt=f"Gesamtinvestition Netto: {invest:,.2f} EUR", ln=True)
    pdf.ln(5)
    
    # 5. Business Case (ROI & ESG)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="4. Business Case & Nachhaltigkeit (pro Jahr)", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, txt=f"- Kosten fuer bisheriges Einweg-System: {einweg_jahr:,.2f} EUR", ln=True)
    pdf.cell(0, 6, txt=f"- Amortisation der Rieber-Loesung nach: ca. {amort_monat:.1f} Monaten", ln=True)
    pdf.cell(0, 6, txt=f"- Eingesparter Plastikmuell: {plastik_jahr:,.0f} kg", ln=True)
    pdf.cell(0, 6, txt=f"- CO2-Reduktion: {co2_jahr:,.0f} kg", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- APP START ---
st.set_page_config(page_title="Rieber Solutionfinder", layout="wide")
set_design()

# --- 1. STANDORT-PLANUNG ---
st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
st.subheader("1. Standort-Bedarf")
num_locs = st.number_input("Anzahl der Standorte", min_value=1, value=1)
loc_data = []
total_p_day = 0

for i in range(int(num_locs)):
    c1, c2 = st.columns(2)
    with c1: name = st.text_input(f"Name Standort {i+1}", value=f"Standort {i+1}")
    with c2: count = st.number_input(f"Teilnehmer {name}", min_value=1, value=50)
    loc_data.append({"name": name, "count": count})
    total_p_day += count
st.markdown('</div>', unsafe_allow_html=True)

# --- 2. SYSTEM-PARAMETER ---
st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
st.subheader("2. System & Kalkulation")
k1, k2, k3 = st.columns(3)
with k1:
    verfahren = st.selectbox("Verfahren", ["Cook & Chill", "Cook & Hold"])
    tage = st.number_input("Tage/Woche", value=5)
with k2:
    anwendung = st.selectbox("Bereich", ["Kita", "Schule", "Altenheim", "Betrieb"])
    puffer = st.number_input("Umlauf-Puffer (%)", value=20) / 100
with k3:
    kundengruppe = st.selectbox("Kundengruppe", ["Endkunde", "Fachhandel", "Großkunde"])
    p_adj = st.number_input("Projekt Zu/Abschlag (%)", value=0.0)
    einweg_kosten = st.number_input("Einweg-Kosten (€/Portion)", value=0.35)
st.markdown('</div>', unsafe_allow_html=True)

# --- BERECHNUNGSLOGIK ---
# Equipment-Typen
tp_modell = "thermoport® 1000K" if verfahren == "Cook & Chill" else "thermoport® 1000KB 4.0"
tp_preis_lp = 890.0 if verfahren == "Cook & Chill" else 1350.0

# Kalkulations-Grammatur
gramm_map = {"Kita": 280, "Schule": 360, "Altenheim": 435, "Betrieb": 430}
g_pro_p = gramm_map[anwendung]

# Summen bilden
total_tp, total_gn, total_rp = 0, 0, 0
standort_bericht = []

for loc in loc_data:
    vol_l = (g_pro_p * loc["count"]) / 1000
    gn_bedarf = math.ceil(vol_l / 5)
    gn_final = math.ceil(gn_bedarf * (1 + puffer))
    tp_bedarf = math.ceil(gn_final / 5)
    rp_bedarf = math.ceil(tp_bedarf / 2) # 2 TP pro Rolli
    
    total_tp += tp_bedarf
    total_gn += gn_final
    total_rp += rp_bedarf
    standort_bericht.append(f"{loc['name']}: {loc['count']} Pers. -> {tp_bedarf}x TP, {rp_bedarf}x Rolli")

# Preis-Berechnung
rabatt_base = 0.3 if kundengruppe == "Fachhandel" else (0.4 if kundengruppe == "Großkunde" else 0.0)
def get_netto(lp): return round(lp * (1 - rabatt_base) * (1 + (p_adj/100)), 2)

n_tp, n_gn, n_dk, n_rp = get_netto(tp_preis_lp), get_netto(38.0), get_netto(18.0), get_netto(295.0)
invest = (total_tp * n_tp) + (total_gn * n_gn) + (total_gn * n_dk) + (total_rp * n_rp)

# ROI & ESG
einweg_jahr = einweg_kosten * total_p_day * tage * 52
amort_monat = (invest / (einweg_kosten * total_p_day)) / (tage * 4.33) if einweg_kosten > 0 else 0
plastik_jahr = total_p_day * 0.03 * tage * 52 # 30g pro Portion
co2_jahr = plastik_jahr * 3.5

# --- AUSGABE IN KARTEN ---
st.header("Hardware-Bedarf & Investition")
c_res1, c_res2, c_res3, c_res4 = st.columns(4)
with c_res1: st.markdown(f'<div class="result-card"><p class="metric-title">{tp_modell}</p><p class="metric-value">{total_tp} Stk.</p><p>à {n_tp:.2f}€</p></div>', unsafe_allow_html=True)
with c_res2: st.markdown(f'<div class="result-card"><p class="metric-title">GN-Behälter 1/1 65</p><p class="metric-value">{total_gn} Stk.</p><p>à {n_gn:.2f}€</p></div>', unsafe_allow_html=True)
with c_res3: st.markdown(f'<div class="result-card"><p class="metric-title">Steckdeckel (Dichtung)</p><p class="metric-value">{total_gn} Stk.</p><p>à {n_dk:.2f}€</p></div>', unsafe_allow_html=True)
with c_res4: st.markdown(f'<div class="result-card"><p class="metric-title">Rolliport</p><p class="metric-value">{total_rp} Stk.</p><p>à {n_rp:.2f}€</p></div>', unsafe_allow_html=True)

st.markdown(f'<h2 style="text-align: center; color: #004e54;">Gesamtinvestition: {invest:,.2f} € (Netto)</h2>', unsafe_allow_html=True)

st.header("Business Case (ROI & ESG)")
c_roi1, c_roi2, c_esg1, c_esg2 = st.columns(4)
with c_roi1: st.markdown(f'<div class="roi-card"><p class="metric-title">Einweg-Kosten / Jahr</p><p class="metric-value" style="color: #d9534f;">{einweg_jahr:,.2f} €</p></div>', unsafe_allow_html=True)
with c_roi2: st.markdown(f'<div class="roi-card"><p class="metric-title">Amortisation nach</p><p class="metric-value">{amort_monat:.1f} Monaten</p></div>', unsafe_allow_html=True)
with c_esg1: st.markdown(f'<div class="esg-card"><p class="metric-title">Plastik-Ersparnis</p><p class="metric-value" style="color: #5cb85c;">{plastik_jahr:,.0f} kg / Jahr</p></div>', unsafe_allow_html=True)
with c_esg2: st.markdown(f'<div class="esg-card"><p class="metric-title">CO2-Reduktion</p><p class="metric-value" style="color: #5cb85c;">{co2_jahr:,.0f} kg / Jahr</p></div>', unsafe_allow_html=True)

# PDF Button
pdf_bytes = create_pdf(
    verfahren, anwendung, total_p_day, standort_bericht, 
    tp_modell, total_tp, total_gn, total_rp, n_tp, n_gn, n_dk, n_rp, 
    invest, einweg_jahr, amort_monat, plastik_jahr, co2_jahr
)
st.download_button("Angebot als PDF speichern", data=pdf_bytes, file_name="Rieber_Solution.pdf", mime="application/pdf")
