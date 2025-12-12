---
title: "記憶領航者 (Memory Navigator)"
subtitle: "產品技術與價值提案報告"
author: "技術專案經理"
date: "2025-12-12"
---

# 記憶領航者：基於 LSTM 時序分析的主動預防照護系統
### *從「被動定位」跨越至「行為預測」的技術實現*

---

## 1. 市場痛點與技術缺口 (Why Now?)

### 📉 剛性需求數據
*   **超高齡化**：2025 年台灣 65 歲以上人口將超過 **20%**。(來源：國家發展委員會)
*   **失智症規模**：65 歲以上長者失智症盛行率約 **7.8%**，且逐年攀升。(來源：衛生福利部)

### 🚧 現有技術瓶頸
*   **競品 (GPS 手錶)**：僅提供空間座標 $(x, y)$，缺乏時間維度 $t$ 的行為關聯。只能做到「走失後的尋找」。
*   **我們的突破**：引入 AI 時序分析，做到 **「走失前的預警」**。

---

## 2. 核心解決方案 - 混合式引擎 (Hybrid Engine)

**設計理念**：解決純 AI 產品常見的「冷啟動 (Cold Start)」問題，確保用戶 **Day 1** 即可使用。

### 🛡️ 雙層防護架構

#### **L1 規則引擎 (Rule-Based, Day 1)**
*   **機制**：基於幾何圍籬 (Geofence) 與時間閾值 (Time Threshold) 的硬規則判定。
*   **作用**：處理新用戶初期數據不足的問題，提供即時、確定性的基礎防護。

#### **L2 AI 預測引擎 (AI Prediction Engine, Day 14+)**
*   **機制**：隨著數據累積，啟動 **LSTM 深度學習模型**。
*   **作用**：接手處理非線性、複雜的行為異常偵測（如：還在圍籬內但路徑異常徘徊）。

---

## 3. AI 核心技術 - LSTM 深度學習模型

### 🧠 模型選擇：長短期記憶網路 (LSTM)
*   **選擇理由**：
    *   長者走失行為具有高度的 **時間依賴性 (Temporal Dependency)**。
    *   LSTM 能有效解決 RNN 的梯度消失問題，適合處理長序列的時間資料（記憶長者過去 30 天的作息慣性）。

### 🔢 特徵工程 (Feature Engineering)
| 類別 | 特徵變數 |
| :--- | :--- |
| **空間特徵** | Latitude, Longitude, Distance_from_Home |
| **生理特徵** | Heart_Rate (心率變異), Step_Cadence (步頻) |
| **時間特徵** | Time_of_Day (日夜), Day_of_Week (平假日) |

### 🎯 模型輸出
*   **異常機率 (Risk Score)**：$0 \sim 100$ 的動態風險分數。

---

## 4. 系統架構與硬體解耦 (System Architecture)

**架構優勢**：我們打造的是「純軟體平台」，不被單一硬體綁架。

### 🔄 數據流向 (Data Pipeline)
1.  **Device Layer**: 穿戴裝置 (Garmin, IoT)
2.  **Ingestion Layer**: `POST /telemetry` (批次數據) & `POST /events` (即時事件)
3.  **Processing Layer**: n8n (ETL 清洗) $\rightarrow$ 規則引擎 + LSTM 模型
4.  **Storage Layer**: TimescaleDB (時序資料庫) + AES-256 加密存儲
5.  **Application Layer**: Family App (Dashboard/Notification)

---

## 5. API 整合策略 (Integration Strategy)

*   **標準化接口**：RESTful API over HTTPS (TLS 1.2+)。
*   **資安驗證**：Header `X-Partner-Token` 認證 + Payload 加密。

### ⚡️ 傳輸優化機制
*   **Telemetry (省電策略)**：支援 **Batch Upload** (批次上傳)，允許裝置累積 5-10 分鐘數據後一次傳送，大幅降低 IoT 裝置喚醒頻率，延長電池壽命。
*   **Critical Events (即時策略)**：設計為 **Real-time Push** (即時推播)，繞過常規排程佇列，確保警示在 3 秒內送達後端。

---

## 6. 核心 API 規格詳情 (Core API Specifications)

### 📡 1. 持續性數據上傳
**Endpoint**: `POST /api/v1/ingestion/telemetry`

**Payload 範例**:
```json
{
  "device_id": "WATCH-001",
  "records": [
    { 
      "timestamp": "2025-12-11T10:00:00Z", 
      "lat": 24.16, 
      "lon": 120.64, 
      "heart_rate": 78 
    }
  ]
}
```

### 🚨 2. 關鍵事件觸發
**Endpoint**: `POST /api/v1/ingestion/events`

**Payload 範例**:
```json
{
  "device_id": "WATCH-001",
  "event_type": "FALL_DETECTED",
  "timestamp": "2025-12-11T10:05:00Z"
}
```

---

## 7. 商業價值與競爭優勢 (Business Value)

### 💎 從「賣硬體」轉向「賣服務 (SaaS)」
*   硬體是一次性收入，我們的 AI 訂閱是 **持續性收入 (MRR)**。

### 🏰 數據護城河
*   隨著用戶使用時間越長，LSTM 模型累積的個人化數據越多，預測越準確。
*   **高轉換成本**：家屬不會輕易更換一個「已經熟悉長者習性」的 AI 系統。

### 🌏 生態系擴展
*   API 架構允許我們快速接入新的硬體合作夥伴 (如 Apple Watch, 小米)，擴大市佔率。

---

## 8. 結論 (Conclusion)

*   **技術可行性**：混合引擎架構有效平衡了系統穩定性 (Rule) 與技術先進性 (AI)。
*   **準備就緒**：API 規格已定案，核心演算法已驗證。
*   **下一步**：啟動後端開發，並與硬體合作夥伴進行對接測試。