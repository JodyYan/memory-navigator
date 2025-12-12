import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 頁面基本設定 ---
st.set_page_config(
    page_title="記憶領航者 | AI 主動預防照護系統",
    page_icon="🧭",
    layout="wide"
)

# --- Session State 初始化 ---
if 'geofence' not in st.session_state: st.session_state['geofence'] = 500
if 'night_mode' not in st.session_state: st.session_state['night_mode'] = False
if 'elder_name' not in st.session_state: st.session_state['elder_name'] = "王大明"

# 預設住家座標 (台北信義區)
DEFAULT_HOME_LAT = 25.0330
DEFAULT_HOME_LON = 121.5654

if 'home_lat' not in st.session_state: st.session_state['home_lat'] = DEFAULT_HOME_LAT
if 'home_lon' not in st.session_state: st.session_state['home_lon'] = DEFAULT_HOME_LON
if 'center_mode' not in st.session_state: st.session_state['center_mode'] = "預設住家"
if 'address_input' not in st.session_state: st.session_state['address_input'] = ""

# --- 模擬地址定位功能 (Mock Geocoding) ---
def mock_geocode(address):
    locs = {
        "台北": (25.0330, 121.5654),
        "新北": (25.0123, 121.4657),
        "桃園": (24.9936, 121.3010),
        "新竹": (24.8138, 120.9675),
        "台中": (24.1617, 120.6478),
        "台南": (22.9997, 120.2270),
        "高雄": (22.6273, 120.3014),
        "基隆": (25.1276, 121.7392),
        "宜蘭": (24.7021, 121.7377),
        "花蓮": (23.9756, 121.6044),
        "台東": (22.7972, 121.0714)
    }
    for city, coords in locs.items():
        if city in address:
            return coords
    return None

# 定位回呼函式
def trigger_geocode():
    addr = st.session_state.addr_input_widget
    new_coords = mock_geocode(addr)
    if new_coords:
        # 1. 更新背景座標
        st.session_state['home_lat'] = new_coords[0]
        st.session_state['home_lon'] = new_coords[1]
        
        # 2. 強制同步輸入框 (Input Widgets) 的內部狀態
        st.session_state['lat_input'] = new_coords[0]
        st.session_state['lon_input'] = new_coords[1]
        
        st.toast(f"✅ 已成功定位至：{addr}，監控面板已同步更新！", icon="📍")
    else:
        st.toast("⚠️ 找不到此地址 (Demo版僅支援台灣主要縣市關鍵字)", icon="❓")

# --- 模擬資料生成邏輯 (Hybrid Engine) ---
def get_mock_data(scenario, geofence_radius, is_night_mode_active):
    home_lat = st.session_state['home_lat']
    home_lon = st.session_state['home_lon']
    
    # 基礎數據生成
    if scenario == "Normal":
        lat = home_lat + np.random.normal(0, 0.0001)
        lon = home_lon + np.random.normal(0, 0.0001)
        hr = np.random.randint(60, 75)
        steps = np.random.randint(100, 500)
    elif scenario == "Wandering":
        offset = (geofence_radius / 111000) * 0.9 
        lat = home_lat + offset
        lon = home_lon + offset
        hr = np.random.randint(80, 100)
        steps = np.random.randint(2000, 3000)
    else: # Critical
        offset = (geofence_radius / 111000) * 1.5
        lat = home_lat + offset
        lon = home_lon + offset
        hr = np.random.randint(110, 145)
        steps = np.random.randint(5000, 6000)

    # 混合引擎運算
    risk_score = 10 
    dist = np.sqrt((lat - home_lat)**2 + (lon - home_lon)**2) * 111000
    if dist > geofence_radius:
        risk_score = 100 
    elif is_night_mode_active:
        risk_score += 20 
    if hr > 100:
        risk_score += 30
    
    return lat, lon, hr, steps, min(100, risk_score), dist

# --- 主介面 ---
st.title("🧭 記憶領航者 (Memory Navigator)")

tab1, tab2 = st.tabs(["⚙️ 家屬設定 (規則建立)", "🏠 即時監控儀表板"])

# --- TAB 1: 設定頁面 ---
with tab1:
    st.header("建立長者防護檔案")
    st.caption("在此設定的規則將作為 AI 系統初期的判斷依據。")
    
    # 1. 基本資料
    st.subheader("1. 基本資料")
    c1_1, c1_2 = st.columns(2)
    with c1_1:
        st.session_state['elder_name'] = st.text_input("長者姓名", st.session_state['elder_name'])
    with c1_2:
        st.text_input("穿戴裝置 ID", "WATCH-G001-998877", disabled=True)
    
    st.divider()

    # 2. 安全圍籬設定
    st.subheader("2. 安全圍籬與中心點設定")
    
    col_mode, col_radius = st.columns([1, 1])
    with col_mode:
        center_mode = st.radio(
            "圍籬中心點來源", 
            ["預設住家", "自訂位置 (輸入地址/座標)"], 
            index=0 if st.session_state['center_mode'] == "預設住家" else 1,
            horizontal=True
        )
        st.session_state['center_mode'] = center_mode

    with col_radius:
        st.session_state['geofence'] = st.slider(
            "安全活動半徑 (公尺)", 
            min_value=100, max_value=2000, 
            value=st.session_state['geofence']
        )

    if center_mode == "自訂位置 (輸入地址/座標)":
        st.info("💡 提示：輸入包含縣市的地址（如：台中市政府）後按下 Enter 即可定位。")
        
        c_addr, c_btn = st.columns([3, 1])
        with c_addr:
            st.text_input(
                "地址搜尋 (模擬)", 
                placeholder="例如：台中市西屯區...", 
                key="addr_input_widget",
                on_change=trigger_geocode
            )
        with c_btn:
            st.write("") 
            st.write("") 
            st.button("📍 定位", on_click=trigger_geocode)

        c_lat, c_lon = st.columns(2)
        new_lat = c_lat.number_input("中心點緯度", value=st.session_state['home_lat'], format="%.4f", key="lat_input")
        new_lon = c_lon.number_input("中心點經度", value=st.session_state['home_lon'], format="%.4f", key="lon_input")
        
        if new_lat != st.session_state['home_lat'] or new_lon != st.session_state['home_lon']:
            st.session_state['home_lat'] = new_lat
            st.session_state['home_lon'] = new_lon
            st.rerun()
    else:
        st.session_state['home_lat'] = DEFAULT_HOME_LAT
        st.session_state['home_lon'] = DEFAULT_HOME_LON
        st.caption(f"目前使用預設住家座標：{DEFAULT_HOME_LAT}, {DEFAULT_HOME_LON}")

    # 地圖預覽 (統一使用綠色代表家)
    st.write("📍 **圍籬中心點預覽：**")
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: #00FF00; border-radius: 50%; margin-right: 5px;"></span>
            <span style="font-size: 14px; color: #555;">安全中心點 (家)</span>
        </div>
    """, unsafe_allow_html=True)
    st.map(
        pd.DataFrame({
            'lat': [st.session_state['home_lat']], 
            'lon': [st.session_state['home_lon']],
            'color': ['#00FF00']
        }), 
        zoom=14,
        color='color'
    )

    st.divider()
    
    # 3. 進階規則
    st.subheader("3. 進階規則")
    st.session_state['night_mode'] = st.toggle("開啟夜間模式 (Night Mode)", value=st.session_state['night_mode'])
    
    st.caption("""
    **功能說明：**
    開啟此模式後，系統將針對 **夜間時段 (22:00 - 06:00)** 提高監測敏感度。
    若長者在此時段有移動跡象，風險分數將自動 **+20 分**，以便家屬能更早收到警示，預防夜間走失。
    """)
    
    if st.button("💾 儲存設定"):
        st.success("設定已更新！")

# --- TAB 2: 監控儀表板 ---
with tab2:
    st.sidebar.header("🛠 開發者模擬面板")
    scenario = st.sidebar.radio("長者行為模擬:", ["Normal", "Wandering", "Critical"])

    explanations = {
        "Normal": """
        **🟢 運作規則：**
        * **位置**：家附近 (圍籬內)
        * **心率**：正常 (60-75 bpm)
        
        **系統反應：**
        * 風險分數維持低檔 (10-30)。
        * 顯示「狀態安全」。
        """,
        "Wandering": """
        **🟡 運作規則：**
        * **位置**：接近圍籬邊緣 (90% 半徑處)
        * **心率**：微升 (80-100 bpm)
        
        **系統反應：**
        * AI 判定為「徘徊徵兆」。
        * 風險分數升高 (50-70)。
        * 發出黃色「注意」預警。
        """,
        "Critical": """
        **🔴 運作規則：**
        * **位置**：**已超出圍籬** (>1.5倍 半徑)
        * **心率**：**異常飆升** (110+ bpm)
        
        **系統反應：**
        * 觸發電子圍籬規則 (Hard Rule)。
        * 風險分數直接鎖定 100。
        * 觸發紅色「緊急」警報與推播。
        """
    }
    st.sidebar.info(explanations[scenario])
    
    # 加入風險分數定義表
    st.sidebar.markdown("""
    ---
    **📊 風險分數定義：**
    * **0-49 (安全)**：正常活動範圍。
    * **50-79 (注意)**：輕微異常 (如徘徊、心率微升)。
    * **80-100 (緊急)**：極高風險 (超出圍籬、跌倒)。
    """)

    cur_lat, cur_lon, hr, steps, risk, dist = get_mock_data(
        scenario, 
        st.session_state['geofence'], 
        st.session_state['night_mode']
    )
    
    st.subheader(f"長者：{st.session_state['elder_name']} | 狀態監控")
    
    if risk >= 80:
        st.error(f"🚨 【緊急警報】偵測到高度風險！(分數: {risk})")
    elif risk >= 50:
        st.warning(f"⚠️ 【注意】偵測到異常行為 (分數: {risk})")
    else:
        st.success(f"✅ 狀態安全 (分數: {risk})")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("❤️ 心率", f"{hr} bpm", delta=f"{hr-70} bpm", delta_color="inverse")
    m2.metric("🤖 風險分數", f"{risk}/100")
    dist_status = "圍籬內" if dist < st.session_state['geofence'] else "超出範圍"
    m3.metric("📍 離家距離", f"{int(dist)} m", delta=dist_status, delta_color="inverse")
    m4.metric("🛡️ 目前圍籬設定", f"{st.session_state['geofence']} m")
    
    # --- 地圖顯示 (修正圖層順序) ---
    # 1. 家 (綠點) 在第一層，作為背景
    # 2. 長者 (紅點) 在第二層，作為前景
    map_data = pd.DataFrame({
        'lat': [st.session_state['home_lat'], cur_lat],
        'lon': [st.session_state['home_lon'], cur_lon],
        'color': ['#00FF00', '#FF0000'], 
        'size': [200, 100] 
    })
    
    # 加入圖例
    st.markdown("""
        <div style="display: flex; justify-content: flex-start; gap: 20px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center;">
                <span style="display: inline-block; width: 12px; height: 12px; background-color: #FF0000; border-radius: 50%; margin-right: 5px;"></span>
                <span style="font-size: 14px; font-weight: bold;">🔴 長者目前位置</span>
            </div>
            <div style="display: flex; align-items: center;">
                <span style="display: inline-block; width: 12px; height: 12px; background-color: #00FF00; border-radius: 50%; margin-right: 5px;"></span>
                <span style="font-size: 14px; font-weight: bold;">🟢 安全圍籬中心 (家)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.map(map_data, color='color', size='size', zoom=14)