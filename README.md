# <div align="center">💤 Sleep Health AI Analyzer</div>

<div align="center">
  <em>An end-to-end Machine Learning solution for predicting sleep disorders with a custom-engineered UI/UX.</em>
</div>

---

### 🚀 <span style="color:#4E342E">Technical Architecture</span>
**The system is built on a robust pipeline that bridges the gap between raw data and real-time inference.**

#### **1. Data Processing Pipeline**
* **Feature Engineering:** Calculated **BMI** from height/weight and transformed categorical data (Occupation, Mental Health) using **Label Encoding**.
* **Data Normalization:** Implemented **StandardScaler** to ensure uniform feature contribution, preventing model bias toward large-scale values.
* **Categorical Handling:** Customized mappings for sensitive lifestyle indicators like Caffeine and Alcohol consumption.

#### **2. Machine Learning Core**
* **Algorithm:** Utilizing **XGBoost (Extreme Gradient Boosting)** for its superior performance with structured tabular data.
* **Evaluation:** Optimized using **Avona Correlation analysis** to identify key sleep quality drivers.
* **Inference:** A dedicated serialization pipeline using **Joblib** for model and scaler persistence.

#### **3. UI/UX Design (The "Premium" Interface)**
* **Theming:** A sophisticated **"Beige & Brown"** palette inspired by Earth tones.
* **Dynamic Components:** Custom-styled `st.segmented_control` for full-width responsive layouts.
* **Accessibility:** **Large-font typography** and high-contrast labels for improved readability.

---

### 🛠️ <span style="color:#4E342E">Tech Stack</span>

| Category | Tools |
| :--- | :--- |
| **Language** | Python |
| **Frontend** | Streamlit (Custom CSS Injection) |
| **Analysis** | Pandas, NumPy, Matplotlib, Seaborn |
| **ML Framework** | XGBoost, Scikit-Learn |
| **Serialization** | Joblib / Pickle |

---

### 🎯 <span style="color:#4E342E">Conclusion</span>
The **Sleep Health AI Analyzer** is a demonstration of how high-performance Machine Learning can be packaged into a user-centric, aesthetically pleasing software product. It bridges the gap between complex statistical boosting and everyday health tracking.
