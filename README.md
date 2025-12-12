# 🧭 Memory Navigator (記憶領航者)

**AI-Powered Proactive Care System for Dementia Elders**
**基於 LSTM 時序分析的主動預防照護系統**

## 📖 專案簡介 (Project Overview)
Memory Navigator 是一個針對失智症長者設計的主動照護系統。不同於傳統 GPS 僅能在走失後尋人，本系統結合 **幾何圍籬 (Geofence)** 與 **AI 行為預測**，旨在「走失發生前」即發出預警。

本專案包含兩個核心組件 (Dual-Component MVP)：
1.  **Visual Dashboard (Streamlit)**: 供家屬使用的視覺化監控介面 (模擬環境)。
2.  **API Server (FastAPI)**: 供硬體廠商串接的後端資料接口。

---

## 🚀 快速開始 (Quick Start)

### 1. 安裝依賴 (Installation)
```bash
pip install -r requirements.txt
```

### 2. 啟動監控儀表板 (Launch Dashboard)
這是給家屬使用的前端介面，包含地圖監控與規則設定功能。
```bash
streamlit run dashboard.py
```
> 啟動後請用瀏覽器開啟 `http://localhost:8501`

### 3. 啟動後端 API (Launch API Server)
這是給 IoT 裝置上傳數據的後端服務。
```bash
uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
```
> API 文件位置：`http://localhost:8000/docs`

---

## 🛠️ 技術架構 (Tech Stack)

*   **Frontend**: [Streamlit](https://streamlit.io/) (Rapid Prototyping)
*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (High Performance API)
*   **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
*   **Visualization**: Pandas, NumPy, Streamlit Map

## 📂 檔案結構 (File Structure)

*   `dashboard.py`: Streamlit 儀表板主程式 (含 Hybrid Engine 模擬邏輯)。
*   `api_server.py`: FastAPI 後端伺服器 (Telemetry & Events)。
*   `test_api.py`: 測試 API 功能的腳本。
*   `doc.pdf`: 產品技術白皮書。
*   `DEPLOYMENT.md`: 部署指南。

## 💡 功能亮點 (Key Features)

*   **Hybrid Engine**: 結合 Rule-Based (冷啟動) 與 AI 模擬邏輯。
*   **Mock Geocoding**: 內建台灣主要縣市模擬定位功能。
*   **Scenario Simulation**: 支援 Normal / Wandering / Critical 三種情境模擬。
*   **Night Mode**: 夜間加權風險運算模式。

---

##  Memory Navigator MVP Demo.
`https://memory-navigator-fj7xqjusmjbg4bjycp4hfd.streamlit.app/`