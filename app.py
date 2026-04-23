import streamlit as st
import pandas as pd
import math
import base64
import os
from fpdf import FPDF

# --- APP START & NAVIGATION ---
st.set_page_config(page_title="Rieber Solutionfinder", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- BASIS-FUNKTIONEN (AUS ORIGINAL-CODE) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- PRO-DESIGN (NUR APP ICON & BRUTALIST UI) ---
def set_pro_design():
    bg_style = ""
    apple_icon = ""
    try:
        if os.path.exists('background.jpg'):
            bg_base64 = get_base64('background.jpg')
            bg_style = f'background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), url("data:image/jpg;base64,{bg_base64}"); background-size: cover; background-attachment: fixed;'
        
        # Das Bild wird NUR noch als App-Icon für iOS im Hintergrund geladen
        if os.path.exists('Solutionfinder.jpeg'):
            logo_base64 = get_base64('Solutionfinder.jpeg')
            apple_icon = f'<link rel="apple-touch-icon" href="data:image/jpeg;base64,{logo_base64}">'
    except:
        pass

    st.markdown(f'''
        {apple_icon}
        <style>
        .stApp {{ {bg_style} }}
        .eingabe-box {{ background-color: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 12px; border: 3px solid #000000; margin-bottom: 25px; box-shadow: 6px 6px 0px rgba(0,0,0,0.15); }}
        .result-card {{ background-color: #ffffff; padding: 20px; border-radius: 12px; border: 3px solid #000000; text-align: center; height: 100%; box-shadow: 6px 6px 0px #000000; margin-bottom: 15px; }}
        .roi-card {{ background-color: #f8f9fa; border: 3px solid #000000; text-align: center; height: 100%; box-shadow: 6px 6px 0px #000000; padding: 15px; border-radius: 12px; }}
        .esg-card {{ background-color: #ffffff; border: 3px solid #000000; text-align: center; height: 100%; box-shadow: 6px 6px 0px #000000; padding: 15px; border-radius: 12px; }}
        .metric-title {{ color: #000000; font-weight: 900; font-size: 1.05em; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .metric-value {{ font-size: 1.8em; font-weight: 900; color: #000000; }}
        .main-title {{ font-size: 2.8em; font-weight: 900; color: #000000; text-align: center; margin-top: 10px; margin-bottom: 30px; text-shadow: 2px 2px 0px #ffffff; letter-spacing: -0.5px; }}
        .stButton>button {{ border: 3px solid black !important; color: black !important; font-weight: 900; width: 100%; box-shadow: 4px 4px 0px black; transition: all 0.2s; }}
        .stButton>button:active {{ box-shadow: 0px 0px 0px black; transform: translate(4px, 4px); }}
        </style>
        <h1 class="main-title">SOLUTIONFINDER</h1>
    ''', unsafe_allow_html=True)

# --- PDF GENERATOR SOLUTIONFINDER ---
def create_pdf(v, a, komp, t_p, s_list, tp_m, t_tp, t_gn, t_rp, n_tp, n_gn, n_dk, n_rp, inv, e_j, a_m, p_j, c_j):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Rieber Solutionfinder - Bedarfsanalyse", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, txt=f"Verfahren: {v} | Bereich: {a}", ln=True)
    pdf.cell(0, 7, txt=f"Menuekomponenten: {komp} | Teilnehmer Gesamt: {t_p}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, txt="Detaillierte Stueckliste (Netto-Einzelpreise):", ln=True)
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
    pdf.cell(0, 8, txt="Business Case & Nachhaltigkeit:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, txt=f"- Amortisation: ca. {a_m:.1f} Monate", ln=True)
    pdf.cell(0, 6, txt=f"- Eingespartes Plastik: {p_j:,.0f} kg / Jahr", ln=True)
    pdf.cell(0, 6, txt=f"- CO2-Reduktion: {c_j:,.0f} kg / Jahr", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- LOGIK & PDF FÜR NEUEN BAIN MARIE RECHNER ---
LOGIK_DATEN_BM = {
    "Trocken Bain Marie": {"ersparnis": 490.34, "prozent": 81},
    "Varithek 800": {"ersparnis": 496.06, "prozent": 82},
    "EST Infrarot": {"ersparnis": 515.96, "prozent": 85}
}

def create_pdf_bain_marie(kundenname, anzahl, verfahren, ersparnis, gesamt_ersparnis):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Rieber - Wirtschaftlichkeitsanalyse Bain Marie", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, txt=f"Kunde: {kundenname}", ln=True)
    pdf.cell(0, 10, txt=f"Anzahl zu ersetzender Becken: {anzahl}", ln=True)
    pdf.cell(0, 10, txt=f"Gewaehltes System: {verfahren}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, txt="Ergebnisse der Berechnung:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, txt=f"Einsparung pro Becken: {ersparnis:,.2f} Euro / Jahr", ln=True)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 15, txt=f"Gesamtersparnis: {gesamt_ersparnis:,.2f} Euro / Jahr", ln=True)
    
    pdf.set_font("Arial", "I", 10)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="Berechnungsgrundlage: 0,372 Euro/kWh bei 365 Betriebstagen pro Jahr. Referenzwert: Klassisches Wasser-Bain-Marie (1,2 kW).")
    
    return pdf.output(dest="S").encode("latin-1")


# ==========================================
# PAGE ROUTING
# ==========================================

# --- STARTSEITE ---
if st.session_state.page == 'home':
    set_pro_design()
    st.markdown("<h3 style='text-align: center; margin-top: -20px; margin-bottom: 20px;'>Bitte wählen Sie ein Tool:</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
    if st.button("▶ Bedarfsanalyse (Solutionfinder)"):
        st.session_state.page = 'solutionfinder'
        st.rerun()
    st.write("")
    if st.button("▶ Bain Marie Ersparnis-Berechnung"):
        st.session_state.page = 'ersparnis'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- ORIGINAL SOLUTIONFINDER CODE ---
elif st.session_state.page == 'solutionfinder':
    c_nav1, c_nav2 = st.columns([1, 5])
    with c_nav1:
        if st.button("← Zurück zum Menü"):
            st.session_state.page = 'home'
            st.rerun()
            
    set_pro_design()

    # --- EINGABE ---
    st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
    n_loc = st.number_input("Anzahl Standorte", min_value=1, value=1)
    total_p = 0
    loc_reports = []

    for i in range(int(n_loc)):
        c1, c2 = st.columns(2)
        with c1: name = st.text_input(f"Name Standort {i+1}", value=f"Standort {i+1}")
        with c2: count = st.number_input(f"Teilnehmer Standort {i+1}", min_value=1, value=50)
        total_p += count
        loc_reports.append((name, count))

    st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    with k1:
        v_sys = st.selectbox("Verfahren", ["Cook & Chill", "Cook & Hold"])
        komp = st.selectbox("Menükomponenten", ["1", "2", "3", "4"], index=2)
        tage = st.number_input("Tage pro Woche", value=5)
    with k2:
        bereich = st.selectbox("Anwendungsbereich", ["Kita", "Schule", "Altenheim", "Betrieb"])
        puf = st.number_input("Umlauf-Puffer (%)", value=20) / 100
    with k3:
        gruppe = st.selectbox("Kundengruppe", ["Endkunde", "Fachhandel", "Großkunde"])
        p_adj = st.number_input("Projekt Zu/Abschlag (%)", value=0.0)
        einweg = st.number_input("Einweg €/Portion", value=0.35)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LOGIK ---
    tp_m = "thermoport 1000K" if v_sys == "Cook & Chill" else "thermoport 1000KB 4.0"
    tp_lp = 920.0 if v_sys == "Cook & Chill" else 1380.0
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

    def calc_final_netto(lp, r_base, adjustment):
        return round(lp * (1 - r_base) * (1 + (adjustment / 100)), 2)

    n_tp = calc_final_netto(tp_lp, rab, p_adj)
    n_gn = calc_final_netto(42.0, rab, p_adj)
    n_dk = calc_final_netto(22.0, rab, p_adj)
    n_rp = calc_final_netto(310.0, rab, p_adj)

    inv = (t_tp * n_tp) + (t_gn * (n_gn + n_dk)) + (t_rp * n_rp)

    roi_j = einweg * total_p * tage * 52
    amo = (inv / (einweg * total_p)) / (tage * 4.33) if total_p > 0 and einweg > 0 else 0
    pla = total_p * 0.03 * tage * 52
    co2 = pla * 3.5

    # --- OUTPUT ---
    st.header("BEDARF & INVESTITION")
    r1, r2, r3, r4 = st.columns(4)
    r1.markdown(f'<div class="result-card"><p class="metric-title">{tp_m}</p><p class="metric-value">{t_tp}</p><p style="margin-top: 10px; font-weight: bold;">à {n_tp:.2f}€</p></div>', unsafe_allow_html=True)
    r2.markdown(f'<div class="result-card"><p class="metric-title">GN 1/1 65mm</p><p class="metric-value">{t_gn}</p><p style="margin-top: 10px; font-weight: bold;">à {n_gn:.2f}€</p></div>', unsafe_allow_html=True)
    r3.markdown(f'<div class="result-card"><p class="metric-title">Steckdeckel</p><p class="metric-value">{t_gn}</p><p style="margin-top: 10px; font-weight: bold;">à {n_dk:.2f}€</p></div>', unsafe_allow_html=True)
    r4.markdown(f'<div class="result-card"><p class="metric-title">Rolliport</p><p class="metric-value">{t_rp}</p><p style="margin-top: 10px; font-weight: bold;">à {n_rp:.2f}€</p></div>', unsafe_allow_html=True)

    st.markdown(f'<h2 style="text-align: center; color: white; background: black; padding: 20px; border-radius: 12px; border: 3px solid #000000; box-shadow: 6px 6px 0px rgba(0,0,0,0.5); font-weight: 900; margin-top: 20px; margin-bottom: 30px;">Gesamtinvestition: {inv:,.2f} € Netto</h2>', unsafe_allow_html=True)

    st.header("ROI & NACHHALTIGKEIT")
    o1, o2, o3, o4 = st.columns(4)
    o1.markdown(f'<div class="roi-card"><p class="metric-title">Einweg/Jahr</p><p class="metric-value" style="color:#d9534f;">{roi_j:,.0f}€</p></div>', unsafe_allow_html=True)
    o2.markdown(f'<div class="roi-card"><p class="metric-title">Amortisation</p><p class="metric-value">{amo:.1f} Mon.</p></div>', unsafe_allow_html=True)
    o3.markdown(f'<div class="esg-card"><p class="metric-title">Plastik (kg)</p><p class="metric-value">{pla:,.0f}</p></div>', unsafe_allow_html=True)
    o4.markdown(f'<div class="esg-card"><p class="metric-title">CO2 (kg)</p><p class="metric-value">{co2:,.0f}</p></div>', unsafe_allow_html=True)

    # PDF Button
    pdf_b = create_pdf(v_sys, bereich, komp, total_p, loc_reports, tp_m, t_tp, t_gn, t_rp, n_tp, n_gn, n_dk, n_rp, inv, roi_j, amo, pla, co2)
    st.download_button("Angebot als PDF speichern", data=pdf_b, file_name="Rieber_Bedarfsanalyse.pdf", mime="application/pdf")

# --- BAIN MARIE ERSPARNIS-RECHNER ---
elif st.session_state.page == 'ersparnis':
    c_nav1, c_nav2 = st.columns([1, 5])
    with c_nav1:
        if st.button("← Zurück zum Menü"):
            st.session_state.page = 'home'
            st.rerun()
            
    set_pro_design()
    st.markdown("<h3 style='text-align: center; margin-top: -20px; margin-bottom: 30px;'>BAIN MARIE ERSPARNIS</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="eingabe-box">', unsafe_allow_html=True)
    k_name = st.text_input("Kundenname", placeholder="z. B. Muster GmbH")
    anzahl = st.number_input("Anzahl zu ersetzender Wasser-Bain-Maries", min_value=1, value=1)
    system = st.selectbox("Auswahl neue Rieber Technik", options=list(LOGIK_DATEN_BM.keys()))
    
    if st.button("Ersparnis berechnen"):
        daten = LOGIK_DATEN_BM[system]
        gesamt = anzahl * daten["ersparnis"]
        
        st.markdown(f"""
            <div class="result-card" style="margin-top: 20px; border-color: #d9534f; border-width: 4px;">
                <p class="metric-title" style="margin-bottom: 10px;">Ergebnis für {k_name if k_name else 'Ihren Standort'}</p>
                <p style="font-size: 1.1em; margin-bottom: 5px;">Einsparung gegenüber klassischem Wasserbad:</p>
                <p class="metric-value" style="color: #d9534f; font-size: 2.5em; margin: 10px 0;">+ {gesamt:,.2f} € / Jahr</p>
                <p style="font-size: 1em; font-weight: bold; margin-bottom: 0;">Reduktion des Stromverbrauchs um {daten['prozent']}%</p>
            </div>
        """, unsafe_allow_html=True)
        
        # PDF Generierung Bain Marie
        pdf_data_bm = create_pdf_bain_marie(k_name if k_name else 'Kunde', anzahl, system, daten["ersparnis"], gesamt)
        st.download_button(
            label="Bain Marie Berechnung als PDF speichern",
            data=pdf_data_bm,
            file_name=f"Rieber_Bain_Marie_Ersparnis_{k_name if k_name else 'Kunde'}.pdf",
            mime="application/pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True)
