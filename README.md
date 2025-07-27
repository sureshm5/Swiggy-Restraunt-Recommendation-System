# Swiggy-Restraunt-Recommendation-System

🔍 Project Overview
✅ Data Source:
📥 Dataset: swiggy.csv (cleaned and processed in this project)

Format: .csv with columns:

name, place, city, cost, rating, rating_count, cuisine_1, cuisine_2, link

⚠️ Cleaned and encoded data are saved in the swiggy_dataset folder.

⚙️ Preprocessing & Clustering
📓 Notebook: main.ipynb
✅ Tasks Performed:
Data Cleaning:

Removed duplicates, filled missing values

Feature Engineering:

Split cuisine into cuisine_1 and cuisine_2

Encoding:

OneHotEncoding for: place, city, cuisine_1, cuisine_2

LabelEncoding for: name

Scaling:

Scaled rating, rating_count, cost, name_encoded using StandardScaler

Clustering:

Used KMeans clustering with 10 clusters

Saved the following:

encoded_clustered_data.csv

cleaned_data.csv (with cluster column)

Models: ohe_encoder.pkl, scaler.pkl, label_encoder_name.pkl, kmeans_model.pkl

📁 Folder Structure
bash
Copy
Edit
Swiggy_Recommendation_System/
│
├── swiggy_dataset/
│   ├── cleaned_data.csv
│   ├── encoded_clustered_data.csv
│   ├── ohe_encoder.pkl
│   ├── scaler.pkl
│   ├── label_encoder_name.pkl
│   └── kmeans_model.pkl
│
├── app.py                 # Streamlit dashboard
├── main.ipynb             # Preprocessing, encoding, clustering
└── README.md              # Project overview (this file)
📊 Streamlit Dashboard: app.py
🔧 Key Features
1️⃣ Location-Based Search
Enter your place and city

System checks if restaurants are available in the location before proceeding

2️⃣ Optional Filters
Restaurant Name (e.g., kfc, a2b)

Cuisine (e.g., pizza, biryani)

Maximum Cost (₹)

Minimum Rating Count (default: 50)

Minimum Rating (default: 2.5 stars)

3️⃣ Sorting Options
Sort by:

Rating, Rating Count, Cost, or Name

Order: Ascending / Descending

Results: Top 10 / 20 / 30 / 50 / 100

4️⃣ Recommendations Logic
Input is encoded and cluster predicted

Filters are applied after cluster match for optimized recommendations

If a name is given:

Shows exact match from cleaned data

Then shows similar restaurants in the same cluster, place, and city

5️⃣ Result Display
Restaurant Name

Cuisine: Merged cuisine_1 and cuisine_2

Location: Place, City

Cost, Rating, Rating Count

Direct Link to restaurant page

💻 How to Run the Project
🧪 Step 1: Set up a virtual environment
bash
Copy
Edit
python -m venv venv
▶️ Step 2: Activate the environment
Windows:
bash
Copy
Edit
.\venv\Scripts\activate
macOS/Linux:
bash
Copy
Edit
source venv/bin/activate
📦 Step 3: Install dependencies
bash
Copy
Edit
pip install streamlit pandas numpy scikit-learn joblib
🚀 Step 4: Launch the Streamlit App
bash
Copy
Edit
streamlit run app.py
