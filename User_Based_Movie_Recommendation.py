import streamlit as st
import joblib
import pandas as pd
import requests

# Load joblib files
model = joblib.load("model.pkl")
df, user_movie = joblib.load("data.pkl")

st.set_page_config(layout="wide")

# Sidebar Background Color
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1E3C72,#2A5298);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
h1, h2, h3 {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# Header Background Color
st.markdown("""
<style>
header[data-testid="stHeader"] {
    background: linear-gradient(
        to right,
        rgba(15,32,39,0.6),
        rgba(32,58,67,0.6),
        rgba(44,83,100,0.6)
    );
}
</style>
""", unsafe_allow_html=True)


# Page Background Color
st.markdown("""
<style>
.stApp {
background: linear-gradient(
135deg,
#0B0F2A,
#1A1F5C,
#2B2F77,
#0F5F5A,
#1E8A7A
);
}
</style>
""", unsafe_allow_html=True)

# Header Color
st.markdown("""
<style>
h1, h2, h3, h4, h5, h6 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

#Header height reduce and arrow visible
st.markdown("""
<style>
header[data-testid="stHeader"] {
    height: 50px;
}

/* Top gap remove */
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# Sidebar color, font weight and font size
st.markdown("""
<style>
section[data-testid="stSidebar"] * {
    color: white;
    font-weight: bold;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

#Sidebar image down
st.markdown("""
<style>
section[data-testid="stSidebar"] .stImage {
    margin-top: -10px;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.image("User Based.png", width=1000)

# Sidebar
st.sidebar.title("About Project")
st.sidebar.write("This project suggests movies by finding users with similar preferences and recommending movies they liked.")

st.sidebar.title("Features")   
st.sidebar.write("""
💠 Recommend movies based on similar users preferences \n
💠 Uses user-item similarity (collaborative filtering) \n 
💠 Personalized movie recommendations \n
💠 Helps provide personalized movie recommendations based on user behavior and ratings
""")

st.sidebar.title("Libraries")
st.sidebar.markdown("""
⚫ 🔢 Numpy \n
⚫ 🐼 Pandas \n
⚫ 🤖 Scikit(sklearn)
""")

st.sidebar.title("Cloud")
st.sidebar.markdown("☁️ Streamlit")

st.sidebar.title("Contact")
st.sidebar.markdown("📞9999999999")

st.image("User Based.png", width=1000)

# Banner Text 
st.markdown("""
<style>
img {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.banner {
        background: linear-gradient(to right,#0F2027,#1E4D4D,#2E8B57);
        padding: 15px;
        border-radius: 10px;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: white;
    }
</style>
<div class="banner">
🎬 User Based Movie Recommendation System
</div>
""", unsafe_allow_html=True)

st.write("\n")

# 🔥 USER INPUT (main change)
userId = st.number_input("Enter User ID", min_value=1, step=1)

# Button
if st.button("Recommend Movies"):

    if userId in user_movie.index:

        target_user = user_movie.loc[userId]

        distances, indexes = model.kneighbors([target_user], n_neighbors=2)
        index = indexes[0][1]
        similar_user = user_movie.loc[index + 1]

        rec = similar_user[similar_user > 0]
        rec = rec.drop(target_user[target_user > 0].index, errors='ignore')

        rec_df = pd.DataFrame({
            'movieId': rec.index,
            'rating': rec.values
        })

        rec_df = rec_df.sort_values(
            by=['rating','movieId'],
            ascending=[False, True]
        ).head(5)

        final_ids = rec_df.movieId.values

        movies = df[df.movieId.isin(final_ids)] \
                    .drop_duplicates(subset='movieId') \
                    .title.values

        st.subheader("🎯 Recommended Movies")

        for m in movies:
            st.write("👉", m)

    else:
        st.error("User not found ❌")