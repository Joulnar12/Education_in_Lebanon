# Education in Lebanon - Interactive Dashboard

## 1.Project Overview
This project explores the relationship between education resources and education levels in Lebanon.  
We combined two datasets:
1. *Education Levels* (illiteracy, dropout, university, etc.)  
2. *Education Resources* (public/private schools, universities, vocational institutes).  

After cleaning and merging, we built an interactive Streamlit dashboard.

## 2. Visualizations
1. Bar Chart + Trend Line 
   - Bar chart shows number of resources per district.  
   - Line shows illiteracy or dropout % (toggle available).  
   - Hover tooltip show additional breakdowns of education levels.
   - Filterable by governorate or district and by illiteracy or dropout.

2. Donut Chart  
   - Shows distribution of education resources (schools, universities, vocational).  
   - Filterable by governorate or district.  

## 3. Technologies Used
- Python (Pandas, Plotly, Streamlit)  
- GitHub for version control  
- Streamlit Cloud for deployment  

## 4. Live App
👉 [Streamlit App Link] https://educationinlebanon-n33mf3binqoqjyiq6ibvrq.streamlit.app/ 

## 5. GitHub Repository
👉 [Repo Link]https://github.com/Joulnar12/Education_in_Lebanon  

---

## How to Run Locally
```bash
# Clone repo
git clone https://github.com/Joulnar12/Education_in_Lebanon 
# Install requirements
pip install -r requirements.txt

# Run app
streamlit run app.py
