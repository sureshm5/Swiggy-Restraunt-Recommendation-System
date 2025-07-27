import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ---------------- Load Data & Models ----------------
cleaned_data_path = r'C:\Users\sures\OneDrive\Desktop\from_tuf_gaming\Swiggy_Recommendation_System\swiggy_dataset\cleaned_data.csv'
encoded_data_path = r'C:\Users\sures\OneDrive\Desktop\from_tuf_gaming\Swiggy_Recommendation_System\swiggy_dataset\encoded_clustered_data.csv'
ohe_path = r'C:\Users\sures\OneDrive\Desktop\from_tuf_gaming\Swiggy_Recommendation_System\swiggy_dataset\ohe_encoder.pkl'
scaler_path = r'C:\Users\sures\OneDrive\Desktop\from_tuf_gaming\Swiggy_Recommendation_System\swiggy_dataset\scaler.pkl'
label_encoder_path = r'C:\Users\sures\OneDrive\Desktop\from_tuf_gaming\Swiggy_Recommendation_System\swiggy_dataset\label_encoder_name.pkl'
kmeans_path = r'C:\Users\sures\OneDrive\Desktop\from_tuf_gaming\Swiggy_Recommendation_System\swiggy_dataset\kmeans_model.pkl'

@st.cache_data
def load_all():
    df_cleaned = pd.read_csv(cleaned_data_path)
    df_encoded = pd.read_csv(encoded_data_path)
    df_cleaned['cluster'] = df_encoded['cluster']
    ohe_encoder = joblib.load(ohe_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(label_encoder_path)
    kmeans_model = joblib.load(kmeans_path)
    ohe_feature_names = ohe_encoder.get_feature_names_out(['place', 'city', 'cuisine_1', 'cuisine_2'])
    return df_cleaned, df_encoded, ohe_encoder, scaler, label_encoder, kmeans_model, ohe_feature_names

df_cleaned, df_encoded, ohe_encoder, scaler, label_encoder, kmeans_model, ohe_feature_names = load_all()

# ------------------- UI -------------------
st.title("🍽️ Restaurant Recommendation App")
st.markdown("""
Enter your location and preferences to get restaurant suggestions based on your area.  
> If you're not from the main city itself, please mention the place you live in that city.
""")

# --- Session State ---
if 'availability_checked' not in st.session_state:
    st.session_state.availability_checked = False

# --- Place/City input ---
place_input = st.text_input("Place (Your area):", key="place_input").strip().lower()
city_input = st.text_input("City:", key="city_input").strip().lower()

# Check availability
if st.button("Check Availability ✅"):
    matched = df_cleaned[(df_cleaned['place'] == place_input) & (df_cleaned['city'] == city_input)]
    if not matched.empty:
        st.session_state.availability_checked = True
        st.success(f"✅ Found {len(matched)} restaurants in {place_input}, {city_input}.")
    else:
        st.session_state.availability_checked = False
        st.warning(f"⚠️ No restaurants found for {place_input}, {city_input}.")

# --- Proceed with filters ---
if st.session_state.availability_checked:
    cuisine_input = st.text_input("Cuisine (e.g., pizza, biryani):", key="cuisine_input").strip().lower()
    name_input = st.text_input("Restaurant Name (optional):", key="name_input").strip().lower()
    max_cost = st.number_input("Max Cost (₹)", min_value=0, value=350, key="max_cost")
    min_rating_count = st.number_input("Minimum Rating Count", min_value=0, value=50, key="rating_count")
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 2.5, key="min_rating")
    sort_by = st.selectbox("Sort by", ['rating', 'rating_count', 'cost', 'name'], key="sort_by")
    order = st.radio("Order", ['Descending', 'Ascending'], key="order")
    top_n = st.selectbox("Show Top N Results", [10, 20, 30, 50, 100], index=0, key="top_n")

    median_name_encoded = int(df_encoded['name_encoded'].median())

    if name_input:
        try:
            name_encoded = label_encoder.transform([name_input])[0]
        except ValueError:
            st.warning(f"⚠️ '{name_input}' not found in encoder. Using Median Fallback.")
            name_encoded = median_name_encoded
    else:
        name_encoded = median_name_encoded

    if st.button("🔍 Get Recommendations"):
        try:
            # Encode place, city, cuisine
            input_dict = {
                'place': [place_input],
                'city': [city_input],
                'cuisine_1': [cuisine_input if cuisine_input else ''],
                'cuisine_2': ['']
            }
            input_df = pd.DataFrame(input_dict)
            ohe_input = ohe_encoder.transform(input_df[['place', 'city', 'cuisine_1', 'cuisine_2']])
            ohe_df = pd.DataFrame(ohe_input, columns=ohe_feature_names)

            dummy_num = pd.DataFrame({
                'rating': [min_rating],
                'rating_count': [min_rating_count],
                'cost': [max_cost],
                'name_encoded': [name_encoded]
            })
            scaled = scaler.transform(dummy_num)
            scaled_df = pd.DataFrame(scaled, columns=['rating', 'rating_count', 'cost', 'name_encoded'])

            final_input = pd.concat([ohe_df, scaled_df], axis=1)
            cluster_label = kmeans_model.predict(final_input)[0]

            filtered = df_cleaned[df_cleaned['cluster'] == cluster_label]
            filtered = filtered[(filtered['place'] == place_input) & (filtered['city'] == city_input)]

            name_shown = False
            if name_input:
                name_match = df_cleaned[(df_cleaned['place'] == place_input) &
                                        (df_cleaned['city'] == city_input) &
                                        (df_cleaned['name'].str.lower().str.contains(name_input))]

                if not name_match.empty:
                    st.subheader(f"🍴 Restaurant matching '{name_input}':")
                    for _, row in name_match.iterrows():
                        cuisines = f"{row['cuisine_1']}, {row['cuisine_2']}"
                        st.markdown(f"""
                        **{row['name']}**  
                        _Cuisine_: {cuisines}  
                        📍 {row['place']}, {row['city']}
                        💸 ₹{row['cost']} | ⭐ {row['rating']} ({row['rating_count']} reviews)  
                        🔗 [Restaurant Link]({row['link']})
                        """, unsafe_allow_html=True)
                        matched_cluster = row['cluster']
                        name_shown = True

                    # Get similar restaurants in same cluster/place/city
                    st.subheader("📍 Other similar restaurants nearby:")
                    filtered = df_cleaned[(df_cleaned['cluster'] == matched_cluster) &
                                          (df_cleaned['place'] == place_input) &
                                          (df_cleaned['city'] == city_input) &
                                          (df_cleaned['name'].str.lower() != row['name'].lower())
                                          ]

            if cuisine_input:
                filtered = filtered[(filtered['cuisine_1'] == cuisine_input) | (filtered['cuisine_2'] == cuisine_input)]

            filtered = filtered[(filtered['cost'] <= max_cost) &
                                (filtered['rating_count'] >= min_rating_count) &
                                (filtered['rating'] >= min_rating)]

            if filtered.empty and not name_shown:
                st.warning("⚠️ No matching restaurants found.")
            else:
                filtered = filtered.sort_values(by=sort_by, ascending=(order == 'Ascending')).head(top_n)
                st.success(f"🍽️ {len(filtered)} Restaurants Found")
                for _, row in filtered.iterrows():
                    cuisines = f"{row['cuisine_1']}, {row['cuisine_2']}"
                    st.markdown(f"""
                    **{row['name']}**  
                    _Cuisine_: {cuisines}  
                    📍 {row['place']}, {row['city']}  
                    💸 ₹{row['cost']} | ⭐ {row['rating']} ({row['rating_count']} reviews)  
                    🔗 [Restaurant Link]({row['link']})
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")
