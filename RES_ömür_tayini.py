import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Çanakkale RES",
    layout="wide"
)

# Çanakkale RES Demo Verileri
df = pd.DataFrame([
["T01",92,14.8,2.1,110,61,0.21,8],
["T02",88,12.7,2.8,130,63,0.26,9],
["T03",83,10.1,3.5,180,66,0.31,11],
["T04",61,3.2,8.3,470,84,0.74,19],
["T05",78,8.4,4.2,220,71,0.43,12],
["T06",91,15.2,2.0,105,60,0.19,7],
["T07",75,7.1,4.8,260,73,0.49,13],
["T08",69,5.4,5.6,310,77,0.58,15],
["T09",94,16.3,1.8,95,58,0.15,7],
["T10",86,11.8,3.1,150,65,0.29,10],
["T11",72,6.0,5.2,290,76,0.61,14],
["T12",89,13.5,2.7,125,62,0.24,8],
["T13",58,2.4,8.7,520,86,0.81,21]
], columns=[
"Turbine",
"Health",
"RUL",
"Vibration",
"Oil",
"Sicaklik",
"Miner",
"Turbulence"
])

st.title("⚡ ÇANAKKALE RES")

st.subheader("📍 Çanakkale RES Saha Haritası")

c1, c2, c3 = st.columns([1,2,1])

with c2:
    st.image(
        "images/çanakkale.png",
        width=600
    )
c1,c2,c3 = st.columns(3)

c1.success("🟢 Sağlıklı Türbinler")
c2.warning("🟡 İzleme Gereken Türbinler")
c3.error("🔴 Kritik Türbinler")

st.caption(
    "AI Destekli Türbin Ömür Yönetimi ve Repowering Karar Sistemi"
)

kritik = len(df[df["Health"] < 65])
ortalama_health = round(df["Health"].mean())
ortalama_rul = round(df["RUL"].mean(),1)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Kurulu Güç","29.9 MW")
c2.metric("Türbin Sayısı","13")
c3.metric("Kritik Türbin",kritik)
c4.metric("Ortalama RUL",f"{ortalama_rul} yıl")
st.divider()
st.subheader("🚨 Kritik Alarm Paneli")

kritikler = df[df["Health"] < 65]

for _, r in kritikler.iterrows():

    st.error(
        f"{r['Turbine']} | Health: {r['Health']} | RUL: {r['RUL']} yıl"
    )
options = []

for _, r in df.iterrows():

    if r["Health"] >= 80:
        durum = "🟢"
    elif r["Health"] >= 65:
        durum = "🟡"
    else:
        durum = "🔴"

    options.append(
        f"{durum} {r['Turbine']} | Health:{r['Health']} | RUL:{r['RUL']} yıl"
    )

st.subheader("🎯 Türbin Seç")

selected_text = st.selectbox(
    "Detaylarını görmek istediğiniz türbini seçin",
    options
)

selected = selected_text.split()[1]

row = df[df["Turbine"] == selected].iloc[0]

st.markdown("""
### Durum Açıklaması

🟢 Sağlıklı Türbin (Health > 80)

🟡 İzleme Gerekiyor (65 - 80)

🔴 Kritik / Repowering Adayı (Health < 65)
""")

if row["Health"] >= 80:

    st.success(
        f"{selected} Sağlıklı Çalışıyor"
    )

elif row["Health"] >= 65:

    st.warning(
        f"{selected} Yakın Takip Gerektiriyor"
    )

else:

    st.error(
        f"{selected} Kritik Durumda - Repowering Öneriliyor"
    )

a,b,c = st.columns(3)

a.metric(
    "Health Score",
    f"{row['Health']}/100"
)

b.metric(
    "RUL",
    f"{row['RUL']} yıl"
)

if row["RUL"] < 5:
    c.error("REP0WERING ÖNER")
else:
    c.success("NORMAL")

st.divider()

s1,s2,s3,s4,s5 = st.columns(5)

s1.metric(
    "Titreşim",
    f"{row['Vibration']} mm/s"
)

s2.metric(
    "Yağ Partikül",
    f"{row['Oil']} ppm"
)

s3.metric(
    "Sıcaklık",
    f"{row['Sicaklik']} °C"
)

s4.metric(
    "Miner Damage",
    row["Miner"]
)

s5.metric(
    "Türbülans",
    f"%{row['Turbulence']}"
)

st.divider()

st.subheader("Sensör Analizi")
st.subheader("Risk Dağılımı")

st.write("Titreşim Riski")
st.progress(min(int(row["Vibration"]*10),100))

st.write("Yağ Aşınma Riski")
st.progress(min(int(row["Oil"]/5),100))

st.write("Sıcaklık Riski")
st.progress(min(int(row["Sicaklik"]),100))

st.write("Yorulma Hasarı")
st.progress(min(int(row["Miner"]*100),100))
st.write(f"""
### Titreşim Sensörü
**{row['Vibration']} mm/s**

Mekanik aşınmayı ve rulman sağlığını gösterir.

### Yağ Partikül Sensörü
**{row['Oil']} ppm**

Dişli kutusu içindeki metal aşınmasını gösterir.

### Sıcaklık Sensörü
**{row['Sicaklik']} °C**

Yüksek sıcaklık erken arıza belirtisidir.

### Strain Gauge (Miner Damage)
**{row['Miner']}**

Yapısal yorulma seviyesini gösterir.

### Türbülans Analizi
**%{row['Turbulence']}**

Türbinin maruz kaldığı yorulma yükünü gösterir.
""")

st.divider()

st.subheader("Türbin Bazlı RUL")

fig = px.bar(
    df,
    x="Turbine",
    y="RUL"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Türbin Sağlık Skorları")

fig2 = px.bar(
    df,
    x="Turbine",
    y="Health"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

st.subheader("🤖 AI Karar Motoru")

vib_loss = min(row["Vibration"] * 2, 20)
oil_loss = min(row["Oil"] / 30, 20)
temp_loss = max((row["Sicaklik"] - 60) * 0.8, 0)
miner_loss = row["Miner"] * 30
turb_loss = row["Turbulence"] * 0.5

st.write(f"🔻 Titreşim Etkisi: -{vib_loss:.1f}")
st.write(f"🔻 Yağ Aşınması: -{oil_loss:.1f}")
st.write(f"🔻 Sıcaklık Etkisi: -{temp_loss:.1f}")
st.write(f"🔻 Miner Damage Etkisi: -{miner_loss:.1f}")
st.write(f"🔻 Türbülans Etkisi: -{turb_loss:.1f}")

health = (
    100
    - vib_loss
    - oil_loss
    - temp_loss
    - miner_loss
    - turb_loss
)

health = max(0, round(health))

st.progress(health)

st.metric(
    "AI Hesaplanan Sağlık Skoru",
    health
)

if health < 50:
    st.error("🔴 REPOWERING ÖNERİLİYOR")
elif health < 70:
    st.warning("🟡 YAKIN TAKİP GEREKLİ")
else:
    st.success("🟢 NORMAL OPERASYON")

st.subheader("📋 AI Karar Özeti")

if row["Health"] < 65:

    st.error(f"""
Repowering Öneriliyor

Neden?

• RUL: {row['RUL']} yıl

• Miner Damage: {row['Miner']}

• Yağ Partikül Seviyesi: {row['Oil']} ppm

• Türbülans: %{row['Turbulence']}

Beklenen Üretim Kazancı:
+%15 ila +20
""")

else:

    st.success(f"""
Türbin normal operasyon sınırları içerisindedir.

Kalan Tahmini Ömür:
{row['RUL']} yıl
""")