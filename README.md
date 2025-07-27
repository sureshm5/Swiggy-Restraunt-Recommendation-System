# Swiggy-Restraunt-Recommendation-System

# 🍽️ Swiggy Restaurant Recommendation System

An interactive **Streamlit-based recommendation system** that helps users discover restaurants based on **location**, **cuisine**, **rating**, **cost**, and more, using **clustering (KMeans)** on encoded restaurant data.

---

## 🔍 Project Overview

### ✅ Data Source:
- 📄 Dataset: `swiggy.csv` (cleaned and processed in this project)
- Format: `.csv` with columns:  
  `id`, `name`, `place`, `city`, `cost`, `rating`, `rating_count`, `cuisine_1`, `cuisine_2`, `link`

### ⚠️ Cleaned and encoded data are saved in the **`swiggy_dataset` folder**.

---

## ⚙️ Preprocessing & Clustering

### 📓 Notebook: `main.ipynb`

#### ✅ Tasks Performed:
- Removed **duplicates**, handled **missing values**
- Split combined cuisine column into `cuisine_1`, `cuisine_2`

### 🔄 Encoding:
- **OneHotEncoding** for: `place`, `city`, `cuisine_1`, `cuisine_2`  
- **LabelEncoding** for: `name`

### 📊 Scaling:
- Features `rating`, `rating_count`, `cost`, `name_encoded` scaled using `StandardScaler`

### 📈 Clustering:
- Applied **KMeans** clustering with `10 clusters`
- Saved models and data:
  - `ohe_encoder.pkl`
  - `label_encoder_name.pkl`
  - `scaler.pkl`
  - `kmeans_model.pkl`
  - `encoded_clustered_data.csv`

---

## 🚀 Streamlit Application: `app.py`

### 🔧 Features:

#### 1️⃣ User Input:
- Mandatory: **Place**, **City**
- Optional Filters:  
  `Restaurant Name`, `Cuisine`, `Max Cost`, `Min Rating`, `Min Rating Count`

#### 2️⃣ Recommendation Engine:
- Predicts **user's cluster** using KMeans and retrieves:
  - Restaurants in same **place, city, and cluster**
  - If `name` is specified and found → shows matching restaurant and similar restaurants from the same cluster

#### 3️⃣ Output Display:
- **Top N restaurants** sorted by `Rating`, `Cost`, `Rating Count`, or `Name`
- Displayed with:
  - **Cuisine**
  - **Location**
  - **Cost, Rating, Reviews**
  - 🔗 **Restaurant Link**

---

## 💻 How to Run This Project

### 🧪 Step 1: Create Virtual Environment
```bash
python -m venv venv
```

### ▶️ Step 2: Activate Environment
#### Windows
```bash
.\venv\Scripts\activate
```
#### macOS/Linx
```bash
source venv/bin/activate
```
### 📦 Step 3: Install Dependencies
```bash
pip install numpy pandas streamlit matplotlib scikit-learn
```
### 🚀 Step 4: Launch Streamlit App
```bash
streamlit run app.py
```
