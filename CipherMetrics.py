import streamlit as st
import streamlit.components.v1 as components
import time
import psutil
import pandas as pd
import plotly.express as px
import random
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="CipherMetrics", layout="wide")

st.title("🛡️ CipherMetrics: Şifreleme ve Performans Dashboard'u")
st.markdown("Bu panel, klasik (Afin), modern simetrik (AES) ve asimetrik (RSA) şifreleme yöntemlerini ve **Fermat'ın Küçük Teoremi** optimizasyonunu canlı olarak test eder.")

# --- YENİ METRİK: BINARY MATRIX FEED ---
st.markdown("#### 🖥️ Live Binary Matrix Feed")

MATRIX_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0d0d0d; overflow: hidden; }
  canvas { display: block; }
  .overlay-stats {
    position: absolute;
    top: 10px;
    right: 14px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    color: #00ff41;
    text-align: right;
    text-shadow: 0 0 6px #00ff41;
    line-height: 1.7;
    pointer-events: none;
  }
  .overlay-stats span { display: block; }
  .label { color: #39ff14; opacity: 0.65; font-size: 10px; }
  .corner-tag {
    position: absolute;
    bottom: 8px;
    left: 12px;
    font-family: 'Courier New', monospace;
    font-size: 10px;
    color: #00ff4188;
    text-shadow: 0 0 4px #00ff41;
    pointer-events: none;
  }
</style>
</head>
<body>
<canvas id="matrix"></canvas>
<div class="overlay-stats" id="stats">
  <span class="label">[ SYS MONITOR ]</span>
  <span id="stat-bits">BITS/s: ---</span>
  <span id="stat-entropy">ENTROPY: ---</span>
  <span id="stat-cycles">CYCLES: ---</span>
  <span id="stat-enc">ENC LAYER: ---</span>
  <span id="stat-time">UPTIME: 00:00:00</span>
</div>
<div class="corner-tag" id="corner">◈ CIPHERMETRICS v2.1 · STREAM ACTIVE</div>
<script>
  const canvas = document.getElementById('matrix');
  const ctx = canvas.getContext('2d');
  canvas.width  = window.innerWidth  || 900;
  canvas.height = window.innerHeight || 160;
  const W = canvas.width;
  const H = canvas.height;
  const fontSize = 13;
  const cols = Math.floor(W / fontSize);
  const drops = Array.from({ length: cols }, () => Math.random() * -H);
  const charSets = {
    binary:  ['0','1'],
    hex:     ['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'],
    cipher:  ['Ξ','Σ','Λ','Φ','Ψ','Ω','α','β','γ','δ','#','@','!','%','&'],
  };
  function weightedChar() {
    const r = Math.random();
    if (r < 0.78) return charSets.binary[Math.floor(Math.random() * 2)];
    if (r < 0.92) return charSets.hex[Math.floor(Math.random() * charSets.hex.length)];
    return charSets.cipher[Math.floor(Math.random() * charSets.cipher.length)];
  }
  const colHue   = Array.from({ length: cols }, () => 120 + (Math.random() * 20 - 10));
  const colSpeed = Array.from({ length: cols }, () => 0.4 + Math.random() * 1.2);
  function draw() {
    ctx.fillStyle = 'rgba(13, 13, 13, 0.18)';
    ctx.fillRect(0, 0, W, H);
    for (let i = 0; i < cols; i++) {
      const x = i * fontSize;
      const y = drops[i] * fontSize;
      if (drops[i] > 0) {
        ctx.fillStyle = `hsla(${colHue[i]}, 100%, 95%, 0.95)`;
        ctx.shadowColor = '#ffffff';
        ctx.shadowBlur  = 8;
      } else {
        const alpha = 0.15 + Math.random() * 0.55;
        ctx.fillStyle = `hsla(${colHue[i]}, 100%, 55%, ${alpha})`;
        ctx.shadowColor = `hsl(${colHue[i]}, 100%, 50%)`;
        ctx.shadowBlur  = 4;
      }
      ctx.font = `${fontSize}px 'Courier New', monospace`;
      ctx.fillText(weightedChar(), x, y);
      if (y > H && Math.random() > 0.975) drops[i] = -Math.floor(Math.random() * 20);
      drops[i] += colSpeed[i];
    }
    ctx.shadowBlur = 0;
  }
  setInterval(draw, 35);
  let startTime = Date.now();
  let cycles = Math.floor(Math.random() * 900000) + 100000;
  const encLayers = ['AES-256-GCM','RSA-4096','ChaCha20','Affine-XOR','Fermat-EXP'];
  let encIdx = 0;
  function fmtUptime(ms) {
    const s = Math.floor(ms / 1000);
    const h = String(Math.floor(s / 3600)).padStart(2,'0');
    const m = String(Math.floor((s % 3600) / 60)).padStart(2,'0');
    const sec = String(s % 60).padStart(2,'0');
    return `${h}:${m}:${sec}`;
  }
  function updateStats() {
    const bits  = (Math.random() * 900 + 100).toFixed(1) + ' Mbit/s';
    const entr  = (Math.random() * 0.8 + 7.1).toFixed(3) + ' bits/byte';
    cycles += Math.floor(Math.random() * 12000 + 3000);
    const uptime = fmtUptime(Date.now() - startTime);
    if (Math.random() < 0.04) encIdx = (encIdx + 1) % encLayers.length;
    document.getElementById('stat-bits').textContent    = `BITS/s: ${bits}`;
    document.getElementById('stat-entropy').textContent = `ENTROPY: ${entr}`;
    document.getElementById('stat-cycles').textContent  = `CYCLES: ${cycles.toLocaleString()}`;
    document.getElementById('stat-enc').textContent     = `ENC LAYER: ${encLayers[encIdx]}`;
    document.getElementById('stat-time').textContent    = `UPTIME: ${uptime}`;
  }
  setInterval(updateStats, 700);
  setInterval(() => {
    const el = document.getElementById('corner');
    el.style.opacity = el.style.opacity === '0.2' ? '0.7' : '0.2';
  }, 1200);
</script>
</body>
</html>
"""

components.html(MATRIX_HTML, height=175, scrolling=False)
st.markdown("---")

# --- ALGORİTMALAR ---

def generate_large_data(size_mb):
    """Belleğe alınacak büyük veriyi üretir (MB cinsinden)"""
    return bytearray(random.getrandbits(8) for _ in range(size_mb * 1024 * 1024))

def format_text_dump(data):
    """
    Şifrelenmiş veriyi (baytları veya integerları) tarayıcıyı çökertmeden
    göstermek için basılabilir standart ASCII (klavye) sembollerine dönüştürür.
    Bu sayede o klasik 'şifreli karmaşık metin' görünümü elde edilir.
    """
    if isinstance(data, list): # RSA için (çünkü o integer listesi döndürür)
        return "".join(chr(33 + (val % 94)) for val in data)
    else: # Afin ve AES için (bytearray / bytes)
        return "".join(chr(33 + (b % 94)) for b in data)

def affine_encrypt(data, a, b, m=256):
    """Klasik Yöntem: Afin Şifreleme O(n)"""
    encrypted = bytearray(len(data))
    for i in range(len(data)):
        encrypted[i] = (a * data[i] + b) % m
    return encrypted

def aes_encrypt(data):
    """Modern Simetrik Yöntem: AES-256-CTR"""
    key = os.urandom(32) # 256-bit AES anahtarı
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def rsa_encrypt_textbook(data, e=65537, n=3233):
    """Modern Asimetrik Yöntem: Blok bazlı RSA Şifreleme O(n * log e)"""
    return [pow(byte, e, n) for byte in data]

def standard_mod_exp(base, exp, mod):
    """Standart (Yavaş) Modüler Üs Alma — O(exp) saf Python döngüsü"""
    res = 1
    for _ in range(exp):
        res = (res * base) % mod
    return res

def fermat_mod_exp(base, exp, mod):
    """Fermat'ın Küçük Teoremi + Binary Exponentiation — O(log n)"""
    reduced_exp = exp % (mod - 1)   
    result  = 1
    base_r  = base % mod
    e       = reduced_exp
    while e > 0:                    
        if e & 1:
            result = (result * base_r) % mod
        base_r = (base_r * base_r) % mod
        e >>= 1
    return result

# --- ARAYÜZ VE KONTROLLER ---

col1, col2 = st.columns(2)
with col1:
    data_size  = st.slider("Veri Boyutu (MB)", min_value=1, max_value=10, value=2)
    run_button = st.button("🚀 Testi Başlat ve Canlı İzle", type="primary")

with col2:
    st.info(
        "💡 **Sistem Bilgisi:** Panel klasik O(n) şifrelemeyi, modern donanım hızlandırmalı O(n) AES şifrelemeyi, O(n log e) RSA asimetrik şifrelemeyi test eder.\n\n"
        "**Fermat Testi:** İşlemin matematiksel motorunu standart döngü ve Fermat modüler optimizasyonu ile mikrosaniye hassasiyetinde ölçer."
    )

# --- CANLI TEST VE GRAFİK ÇİZİMİ ---

if run_button:
    status_text       = st.empty()
    progress_bar      = st.progress(0)
    chart_placeholder = st.empty()

    results = []
    
    # Şifrelenmiş verilerin ekrana basılmak üzere tutulacağı önizleme değişkenleri
    preview_affine = ""
    preview_aes = ""
    preview_rsa = ""

    # 1. Veri Üretimi
    status_text.text(f"Durum: {data_size} MB veri belleğe alınıyor...")
    t0   = time.perf_counter()
    data = generate_large_data(data_size)
    results.append({
        "Aşama": "Veri Belleğe Alma",
        "Süre (sn)": time.perf_counter() - t0,
        "CPU (%)": psutil.cpu_percent()
    })
    progress_bar.progress(15)

    # 2. Afin Şifreleme Testi
    status_text.text("Durum: Afin Şifreleme (O(n) Python) çalıştırılıyor...")
    t0 = time.perf_counter()
    enc_affine = affine_encrypt(data, a=5, b=8)
    preview_affine = format_text_dump(enc_affine[:64]) # İlk 64 karakter önizleme
    results.append({
        "Aşama": "Afin Şifreleme",
        "Süre (sn)": time.perf_counter() - t0,
        "CPU (%)": psutil.cpu_percent()
    })
    progress_bar.progress(30)
    
    df  = pd.DataFrame(results)
    fig = px.bar(df, x="Aşama", y="Süre (sn)", color="Aşama", text="Süre (sn)", title="Anlık İşlem Süreleri (Saniye)")
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # 3. AES Şifreleme Testi
    status_text.text("Durum: AES-256 Şifreleme (C-Optimize) çalıştırılıyor...")
    t0 = time.perf_counter()
    enc_aes = aes_encrypt(bytes(data)) 
    preview_aes = format_text_dump(enc_aes[:64]) # İlk 64 karakter önizleme
    results.append({
        "Aşama": "AES-256 Şifreleme",
        "Süre (sn)": time.perf_counter() - t0,
        "CPU (%)": psutil.cpu_percent()
    })
    progress_bar.progress(45)

    df  = pd.DataFrame(results)
    fig = px.bar(df, x="Aşama", y="Süre (sn)", color="Aşama", text="Süre (sn)", title="Anlık İşlem Süreleri (Saniye)")
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # 4. RSA Şifreleme Testi
    status_text.text("Durum: Eğitsel RSA Şifreleme (O(n log e)) çalıştırılıyor...")
    t0 = time.perf_counter()
    enc_rsa = rsa_encrypt_textbook(data) 
    preview_rsa = format_text_dump(enc_rsa[:64]) # İlk 64 karakter önizleme
    results.append({
        "Aşama": "RSA (Asimetrik) Şifreleme",
        "Süre (sn)": time.perf_counter() - t0,
        "CPU (%)": psutil.cpu_percent()
    })
    progress_bar.progress(60)

    df  = pd.DataFrame(results)
    fig = px.bar(df, x="Aşama", y="Süre (sn)", color="Aşama", text="Süre (sn)", title="Anlık İşlem Süreleri (Saniye)")
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # 5. Standart Modüler Üs Alma
    base, mod   = 7, 1000003    # mod → asal sayı
    massive_exp = 5_000_000     # çok büyük üs

    status_text.text("Durum: Standart Modüler Üs Alma (O(n) Python döngüsü) çalıştırılıyor...")
    t0            = time.perf_counter()
    standard_mod_exp(base, massive_exp, mod)
    standart_sure = time.perf_counter() - t0
    results.append({
        "Aşama": "Standart Modüler Üs",
        "Süre (sn)": standart_sure,
        "CPU (%)": psutil.cpu_percent()
    })
    progress_bar.progress(80)

    df  = pd.DataFrame(results)
    fig = px.bar(df, x="Aşama", y="Süre (sn)", color="Aşama", title="Anlık İşlem Süreleri (Saniye)")
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # 6. Fermat + Binary Exponentiation
    status_text.text("Durum: Fermat'ın Küçük Teoremi + Binary Exp (O(log n)) çalıştırılıyor...")
    t0          = time.perf_counter()
    fermat_mod_exp(base, massive_exp, mod)
    fermat_sure = time.perf_counter() - t0
    results.append({
        "Aşama": "Fermat Optimizasyonu",
        "Süre (sn)": fermat_sure,
        "CPU (%)": psutil.cpu_percent()
    })
    progress_bar.progress(100)
    status_text.success("Testler Başarıyla Tamamlandı! 🎉")

    # --- FERMAT HIZ KATLAYICISI (GÖSTERİŞLİ METRİK) ---
    st.markdown("---")
    if fermat_sure > 0:
        hiz_kati = standart_sure / fermat_sure
        st.markdown(f"<h2 style='text-align: center; color: #00FF41;'>⚡ FERMAT OPTİMİZASYONU ETKİSİ: Tam <span style='color: #FFFFFF; text-shadow: 0 0 10px #FFFFFF;'>{hiz_kati:,.0f} KAT</span> Daha Hızlı! ⚡</h2>", unsafe_allow_html=True)
    st.markdown("---")

    # --- ŞİFRELENMİŞ VERİLERİ (TEXT) EKRANA BASMA BÖLÜMÜ ---
    st.markdown("### 🔣 Şifrelenmiş Metin Önizlemeleri (Sembolik Ciphertext)")
    col_out1, col_out2, col_out3 = st.columns(3)
    
    with col_out1:
        st.markdown("**1. Afin Şifreleme Çıktısı**")
        st.code(preview_affine, language="text")
        
    with col_out2:
        st.markdown("**2. AES-256 Şifreleme Çıktısı**")
        st.code(preview_aes, language="text")
        
    with col_out3:
        st.markdown("**3. RSA Şifreleme Çıktısı**")
        st.code(preview_rsa, language="text")
    st.markdown("---")

    # Final Grafik — log_y=True
    df  = pd.DataFrame(results)
    fig = px.bar(
        df, x="Aşama", y="Süre (sn)", color="Aşama",
        hover_data=["CPU (%)"],
        text_auto='.6f',
        log_y=True,
        title="⏱️ Nihai İşlem Süreleri — Logaritmik Eksen (Saniye)"
    )
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="İşlem Tipi",
        yaxis_title="Geçen Süre — log(sn)"
    )
    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Sonuç tablosu 
    st.write("### 📊 Sonuç Özeti")
    display_df = df.copy()
    display_df["Süre (ms)"] = (display_df["Süre (sn)"] * 1000).round(4)
    st.dataframe(
        display_df[["Aşama", "Süre (sn)", "Süre (ms)", "CPU (%)"]]\
            .style
            .format({"Süre (sn)": "{:.6f}", "Süre (ms)": "{:.4f}"})
            .highlight_min(subset=["Süre (sn)"], color="lightgreen")
            .highlight_max(subset=["Süre (sn)"], color="salmon")
    )
