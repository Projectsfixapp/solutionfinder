import streamlit as st
import pandas as pd
import math
import base64
import os
from fpdf import FPDF

# --- BASIS-FUNKTIONEN ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_design():
    # Versuche Bilder zu laden, sonst Standard-Hintergrund
    bg_style = ""
    logo_html = ""
    try:
        if os.path.exists('background.jpg'):
            bg_base64 = get_base64('background.jpg')
            bg_style = f'background-image: url("data:image/jpg;base64,{bg_base64}"); background-size: cover; background-attachment: fixed;'
        
        if os.path.exists('logo.png'):
            logo_base64 = get_base64('logo.png')
            logo_html = f'<div style="text-align: center; margin-bottom: 10px;"><img src="data:image/png;base64,{logo_base64}" width="250"></div>'
    except:
        pass

    st.markdown(f'''
        <style>
        .stApp {{ {bg_style} }}
        .eingabe-box {{ 
            background-color: rgba(240, 248, 248, 0.95); 
            padding: 20px; border-radius: 8px; 
            border-top: 4px solid #004e54; margin-bottom: 20px; 
        }}
        .result-card {{ 
            background-color: white; padding: 15px; border-radius: 10px; 
            border: 1px solid #004e54; text-align: center; height: 100%;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px;
        }}
        .roi-card {{ background-color: #e8f4f4; padding: 15px; border-radius: 10px; border-left: 5px solid #004e54; text-align: center; height: 100%; }}
        .esg-card {{ background-color: #f0f9f0; padding: 15px; border-radius: 10px; border-left: 5px solid #5cb85c; text-align: center; height: 100%; }}
        .metric-title {{ color: #004e54; font-weight: bold; margin-bottom: 5px; }}
        .metric-value {{ font-size: 1.4em; font-weight: bold; color: #333; }}
        </style>
        {logo_html}
    ''', unsafe_allow_html=True)

# --- PDF GENERATOR ---
def create_pdf(v, a, t_p, s_list, tp_m, t_tp, t_gn, t_rp, n_tp, n_gn, n_dk, n_rp, inv, e_j, a_m, p_j, c_j):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists('logo.png'): pdf.image('logo.png', 10, 8, 50)
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Rieber Solutionfinder - Bedarfsanalyse", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, txt=f"Verfahren: {v} | Bereich: {a} | Teilnehmer: {t_p}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="Stueckliste:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, txt=f"- {t_tp}x {tp_m} (a {n_tp:,.2f} EUR)", ln=True)
    pdf.cell(0, 6, txt=f"- {t_gn}x GN-Behaelter 1/1 65mm (a {n_gn:,.2f} EUR)", ln=True)
    pdf.cell(0, 6, txt=f"- {t_gn}x GN-Steckdeckel (a {n_dk:,.2f} EUR)", ln=True)
    pdf.cell(0, 6, txt=f"- {t_rp}x Rolliport (a {n_rp:,.2f} EUR)", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt=f"Gesamtinvestition: {inv:,.2f} EUR Netto", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="Business Case:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, txt=f"Amortisation: {a_m:.1f} Monate", ln=True)
    pdf.cell(0, 6, txt=f"Einsparung Plastik: {p_j:,.0f} kg / Jahr", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- APP START ---
st.set_page_config(page_title="Rieber Solutionfinder", layout="wide")
set_design()

# --- EINGABE ---
st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
n_loc = st.number_input("Anzahl Standorte", min_value=1, value=1)
total_p = 0
loc_reports = []
for i in range(int(n_loc)):
    c1, c2 = st.columns(2)
    with c1: name = st.text_input(f"Name {i+1}", value=f"Standort {i+1}")
    with c2: count = st.number_input(f"Teilnehmer {i+1}", min_value=1, value=50)
    total_p += count
    loc_reports.append((name, count))

st.markdown("---")
k1, k2, k3 = st.columns(3)
with k1:
    v_sys = st.selectbox("Verfahren", ["Cook & Chill", "Cook & Hold"])
    tage = st.number_input("Tage/Woche", value=5)
with k2:
    bereich = st.selectbox("Bereich", ["Kita", "Schule", "Altenheim", "Betrieb"])
    puf = st.number_input("Puffer (%)", value=20) / 100
with k3:
    gruppe = st.selectbox("Kunde", ["Endkunde", "Fachhandel", "Großkunde"])
    einweg = st.number_input("Einweg €/Portion", value=0.35)
st.markdown('</div>', unsafe_allow_html=True)

# --- LOGIK ---
tp_m = "thermoport 1000K" if v_sys == "Cook & Chill" else "thermoport 1000KB 4.0"
tp_lp = 895.0 if v_sys == "Cook & Chill" else 1340.0
g_map = {"Kita": 280, "Schule": 360, "Altenheim": 435, "Betrieb": 430}
g_p = g_map[bereich]

t_tp, t_gn, t_rp = 0, 0, 0
for _, c in loc_reports:
    gn_loc = math.ceil(((g_p * c)/1000) / 5)
    gn_f = math.ceil(gn_loc * (1+puf))
    tp_f = math.ceil(gn_f / 5)
    t_tp += tp_f
    t_gn += gn_f
    t_rp += math.ceil(tp_f / 2)

rab = 0.3 if gruppe == "Fachhandel" else (0.4 if gruppe == "Großkunde" else 0.0)
n_tp, n_gn, n_dk, n_rp = tp_lp*(1-rab), 38.0*(1-rab), 18.0*(1-rab), 290.0*(1-rab)
inv = (t_tp*n_tp) + (t_gn*(n_gn+n_dk)) + (t_rp*n_rp)

roi_j = einweg * total_p * tage * 52
amo = (inv / (einweg * total_p)) / (tage * 4.33) if total_p > 0 else 0
pla = total_p * 0.03 * tage * 52
co2 = pla * 3.5

# --- OUTPUT ---
st.header("Bedarf & Investition")
r1, r2, r3, r4 = st.columns(4)
r1.markdown(f'<div class="result-card"><p class="metric-title">{tp_m}</p><p class="metric-value">{t_tp} Stk.</p></div>', unsafe_allow_html=True)
r2.markdown(f'<div class="result-card"><p class="metric-title">GN 1/1 65mm</p><p class="metric-value">{t_gn} Stk.</p></div>', unsafe_allow_html=True)
r3.markdown(f'<div class="result-card"><p class="metric-title">Steckdeckel</p><p class="metric-value">{t_gn} Stk.</p></div>', unsafe_allow_html=True)
r4.markdown(f'<div class="result-card"><p class="metric-title">Rolliport</p><p class="metric-value">{t_rp} Stk.</p></div>', unsafe_allow_html=True)

st.markdown(f'<h2 style="text-align: center; color: #004e54;">Investition: {inv:,.2f} € Netto</h2>', unsafe_allow_html=True)

st.header("ROI & Nachhaltigkeit")
o1, o2, o3, o4 = st.columns(4)
o1.markdown(f'<div class="roi-card"><p class="metric-title">Einweg/Jahr</p><p class="metric-value">{roi_j:,.0f}€</p></div>', unsafe_allow_html=True)
o2.markdown(f'<div class="roi-card"><p class="metric-title">Amortisation</p><p class="metric-value">{amo:.1f} Mon.</p></div>', unsafe_allow_html=True)
o3.markdown(f'<div class="esg-card"><p class="metric-title">Plastik gespart</p><p class="metric-value">{pla:,.0f}kg</p></div>', unsafe_allow_html=True)
o4.markdown(f'<div class="esg-card"><p class="metric-title">CO2 gespart</p><p class="metric-value">{co2:,.0f}kg</p></div>', unsafe_allow_html=True)

# PDF
pdf_b = create_pdf(v_sys, bereich, total_p, loc_reports, tp_m, t_tp, t_gn, t_rp, n_tp, n_gn, n_dk, n_rp, inv, roi_j, amo, pla, co2)
st.download_button("Angebot als PDF speichern", data=pdf_b, file_name="Rieber_Angebot.pdf", mime="application/pdf")
