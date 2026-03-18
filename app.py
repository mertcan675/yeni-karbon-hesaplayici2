import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import datetime
import io

# --- PDF RAPOR MOTORU ---
def generate_pdf(firma_adi, elektrik, dogalgaz, motorin, toplam_co2, vergi):
# Bu satırların hepsi içerde (tab veya 4 boşluk) olmalı
buffer = io.BytesIO()
c = canvas.Canvas(buffer, pagesize=letter)
tarih = datetime.datetime.now().strftime("%d.%m.%Y")

# Başlık Alanı
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 750, "AB SINIRDA KARBON DUZENLEME (CBAM) ANALIZ RAPORU")
c.setFont("Helvetica", 10)
c.drawString(50, 735, f"Rapor No: {datetime.datetime.now().strftime('%Y%m%d')}-01 | Tarih: {tarih}")
c.line(50, 725, 550, 725)

# Firma Bilgisi
c.setFont("Helvetica-Bold", 12)
c.drawString(50, 700, f"Musteri: {firma_adi}")

# Veri Tablosu
c.setFont("Helvetica-Bold", 11)
c.drawString(50, 660, "Tuketim Kalemi")
c.drawString(200, 660, "Miktar")
c.drawString(350, 660, "Karbon Ayak Izi (kg CO2)")

c.setFont("Helvetica", 10)
y = 640
items = [
("Elektrik", f"{elektrik:,} kWh", f"{elektrik * 0.45:,.2f}"),
("Dogalgaz", f"{dogalgaz:,} m3", f"{dogalgaz * 1.90:,.2f}"),
("Motorin", f"{motorin:,} L", f"{motorin * 2.68:,.2f}")
]

for label, qty, res in items:
c.drawString(50, y, label)
c.drawString(200, y, qty)
c.drawString(350, y, res)
y -= 20

# Sonuc Ozeti
c.line(50, y, 550, y)
y -= 40
c.setFont("Helvetica-Bold", 14)
c.setFillColor(colors.red)
c.drawString(50, y, f"TOPLAM EMISYON: {toplam_co2:.2f} Ton CO2")
y -= 25
c.drawString(50, y, f"TAHMINI AB VERGI YUKU: {vergi:,.2f} EUR")

# Yasal Uyari
c.setFillColor(colors.black)
c.setFont("Helvetica-Oblique", 8)
y -= 60
warning = "YASAL UYARI: Bu rapor bir on analizdir. Resmi gumruk beyani yerine gecmez."
c.drawString(50, y, warning)

c.save()
buffer.seek(0)
return buffer

# --- STREAMLIT ARAYÜZÜ ---
st.set_page_config(page_title="Karbon Analiz Paneli", page_icon="🌱")

st.title("🌱 AB Karbon Vergisi (CBAM) Takip Sistemi")
st.write("İhracatçı firmalar için hızlı uyum ve maliyet analiz paneli.")

with st.sidebar:
st.header("📊 Veri Girişi")
firma = st.text_input("Firma Adı", "Örnek Sanayi A.Ş.")
el = st.number_input("Elektrik (kWh)", min_value=0, value=10000)
dg = st.number_input("Doğalgaz (m3)", min_value=0, value=2000)
mo = st.number_input("Motorin (Litre)", min_value=0, value=500)

hesapla = st.button("Analizi Başlat")

if hesapla:
# Hesaplamalar
toplam_kg = (el * 0.45) + (dg * 1.90) + (mo * 2.68)
toplam_ton = toplam_kg / 1000
tahmini_vergi = toplam_ton * 85 # 85 EUR/Ton varsayılan

# Ekran Metrikleri
col1, col2 = st.columns(2)
col1.metric("Toplam Karbon", f"{toplam_ton:.2f} Ton")
col2.metric("Vergi Riski", f"€{tahmini_vergi:,.2f}", delta="Risk")

st.write("---")

# PDF Oluşturma ve İndirme Butonu
pdf_file = generate_pdf(firma, el, dg, mo, toplam_ton, tahmini_vergi)

st.success("✅ Analiz tamamlandı. Profesyonel raporunuz hazır.")
st.download_button(
label="📄 PDF Analiz Raporunu İndir",
data=pdf_file,
file_name=f"Karbon_Raporu_{firma}.pdf",
mime="application/pdf"
)
