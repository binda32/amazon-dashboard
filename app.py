import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("📊 Amazon Dashboard")

# Load data
df = pd.read_csv("amazon.csv")

# -------- SAFE CLEANING --------
df.columns = df.columns.str.strip()

df['discounted_price'] = pd.to_numeric(
    df['discounted_price'].astype(str).str.replace('₹','').str.replace(',',''),
    errors='coerce'
)

df['actual_price'] = pd.to_numeric(
    df['actual_price'].astype(str).str.replace('₹','').str.replace(',',''),
    errors='coerce'
)

df['discount_percentage'] = pd.to_numeric(
    df['discount_percentage'].astype(str).str.replace('%',''),
    errors='coerce'
)

df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

df['rating_count'] = pd.to_numeric(
    df['rating_count'].astype(str).str.replace(',',''),
    errors='coerce'
)

df['main_category'] = df['category'].astype(str).apply(lambda x: x.split('|')[0])

# Drop null safely
df = df.dropna(subset=['discounted_price','rating'])

# -------- KPIs --------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(df))
col2.metric("Avg Rating", round(df['rating'].mean(), 2))
col3.metric("Avg Discount", round(df['discount_percentage'].mean(), 2))

# -------- CATEGORY CHART --------
st.subheader("Top Categories")

cat = df['main_category'].value_counts().head(5)

fig, ax = plt.subplots()
cat.plot(kind='bar', ax=ax)
st.pyplot(fig)

# -------- PRICE VS RATING --------
st.subheader("Price vs Rating")

fig, ax = plt.subplots()
ax.scatter(df['discounted_price'], df['rating'])
st.pyplot(fig)

# -------- DATA TABLE --------
st.subheader("Sample Data")
st.dataframe(df.head(10))