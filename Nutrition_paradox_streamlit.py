import mysql.connector
import pandas as pd
import streamlit as st
from datetime import date

# SQL database connection setup
conn = mysql.connector.connect(host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
                               user='3AgaX31voqjKoCg.root',
                               password='B0VUhselpkYfTPPK',
                               database="nutrition_paradox",
                               port = 4000)

# title
st.markdown("<h1 style='text-align: center; font-size: 26px;'> 🌍⚖️ Nutrition Paradox: Obesity vs Malnutrition 🍔🥦 </h1>", unsafe_allow_html=True)

# Primary filter selection
table_choice = st.selectbox("Select Data Category", [
    "-- Select --",
    "Obesity Data",
    "Malnutrition Data",
    "Combined Data"
])

# Obesity Queries
obesity_sql_queries = {
    "1.Top 5 regions with the highest average obesity levels in 2022": """
        select avg(Mean_Estimate) as average_obesity, Region from obesity
        where Year = 2022
        group by Region
        order by average_obesity desc
        limit 5;	
    """,
    "2.Top 5 countries with highest obesity estimates": """
        select Country, max(Mean_Estimate) as higest_obesity from obesity
        group by Country
        order by higest_obesity desc
        limit 5;
    """,
    "3.Obesity trend in India over the years(Mean_estimate)":"""
        select avg(Mean_estimate), Year from obesity
        where Country = "India"
        group by Year
        order by Year asc; 
    """,
    "4.Average obesity by gender":"""
        select avg(Mean_estimate) as avg_obesity, Gender from obesity
        group by Gender;
    """,
    "5.Country count by obesity level category and age group":"""
        select count(DISTINCT Country), obesity_level, age_group from obesity
        group by obesity_level, age_group
        order by obesity_level, age_group;
    """,
    "6.Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)":"""
        select * from (select country, avg(ci_width) as avg_ci_width, 'least reliable' as category from obesity
        group by country
        order by avg_ci_width desc
        limit 5) as least_reliable
        union all
        select * from (select country, avg(ci_width) as avg_ci_width,'most consistent' as category from obesity
        group by country
        order by avg_ci_width asc
        limit 5) as most_consistent;
     """,
     "7.Average obesity by age group":"""
        select avg(Mean_estimate) as avg_obesity, age_group from obesity
        group by age_group
    """,
    "8.Top 10 Countries with consistent low obesity (low average + low CI)over the years":"""
        select country, avg(mean_estimate) as avg_obesity, avg(ci_width) as avg_ci_width
        from obesity
        group by country
        order by avg_obesity asc, avg_ci_width asc
        limit 10;
    """,
    "9.Countries where female obesity exceeds male by large margin (same year)":"""
        select f.country, f.year, f.mean_estimate as female_obesity, m.mean_estimate as male_obesity from obesity f
        join obesity m on f.country = m.country and f.year = m.year
        where f.gender = 'female' and m.gender = 'male' and f.mean_estimate > m.mean_estimate
        order by f.mean_estimate - m.mean_estimate desc;
""",
    "10.Global average obesity percentage per year":""" 
        select year, avg(mean_estimate) as global_avg_obesity from obesity
        group by year
        order by year;  
    """
}

# Malnutrition Queries
malnutrition_sql_queries = {
    "1.Avg. malnutrition by age group": """
        select avg(mean_estimate) as avg_malnutrition, age_group from malnutrition
        group by age_group;
    """,
    
    "2.Top 5 countries with highest malnutrition (mean_estimate)": """
        select country, max(mean_estimate) as highest_malnutrition from malnutrition
        group by country
        order by highest_malnutrition desc
        limit 5;
    """,
    
    "3.Malnutrition trend in African region over the years": """
        select avg(mean_estimate), year from malnutrition
        where region = 'Africa'
        group by year
        order by year;
    """,
    
    "4.Gender-based average malnutrition": """
        select avg(mean_estimate) as avg_malnutrition, gender from malnutrition
        group by gender;
    """,
    
    "5.Malnutrition level-wise (average CI_Width by age group)": """
        select case when mean_estimate < 10 then 'low' when mean_estimate between 10 and 20 then 'moderate' else 'high'end as malnutrition_level,age_group,avg(ci_width) as avg_ci_width from malnutrition
        group by malnutrition_level, age_group
        order by malnutrition_level, age_group;

    """,
    
    "6.Yearly malnutrition change in specific countries (India, Nigeria, Brazil)": """
        select avg(mean_estimate), year, country from malnutrition
        where country in ('India', 'Nigeria', 'Brazil')
        group by country, year
        order by country, year;
    """,
    
    "7.Regions with lowest malnutrition averages": """
        select avg(mean_estimate) as avg_malnutrition, region from malnutrition
        group by region
        order by avg_malnutrition asc
        limit 5;
    """,
    
    "8.Countries with increasing malnutrition": """
        select country, min(mean_estimate) as min_malnutrition, max(mean_estimate) as max_malnutrition
        from malnutrition
        group by country
        having max(mean_estimate) > min(mean_estimate)
        order by (max(mean_estimate) - min(mean_estimate)) desc;
    """,
    
    "9.Min/Max malnutrition levels year-wise comparison": """
        select year, min(mean_estimate) as min_malnutrition, max(mean_estimate) as max_malnutrition
        from malnutrition
        group by year
        order by year;
    """,
    
    "10.High CI_Width flags for monitoring (CI_Width > 5)": """
        select country, year, age_group, ci_width from malnutrition
        where ci_width > 5
        order by ci_width desc;
    """
}

#combined queries
combined_sql_queries = {
    "1.Obesity vs malnutrition comparison by country (any 5 countries)": """
        select o.country, avg(o.mean_estimate) as avg_obesity, avg(m.mean_estimate) as avg_malnutrition from obesity o 
        join malnutrition m on o.country = m.country and o.year = m.year and o.gender = m.gender and o.age_group = m.age_group 
        where o.country in ('India', 'Nigeria', 'Brazil', 'USA', 'Germany') 
        group by o.country;
    """,

    "2.Gender-based disparity in both obesity and malnutrition": """
        select o.gender, avg(o.mean_estimate) as avg_obesity, avg(m.mean_estimate) as avg_malnutrition from obesity o 
        join malnutrition m on o.country = m.country and o.year = m.year and o.gender = m.gender and o.age_group = m.age_group 
        group by o.gender;
    """,

    "3.Region-wise avg estimates side-by-side (Africa and America)": """
        select o.region, avg(o.mean_estimate) as avg_obesity, avg(m.mean_estimate) as avg_malnutrition from obesity o 
        join malnutrition m on o.country = m.country and o.year = m.year and o.gender = m.gender and o.age_group = m.age_group 
        where o.region in ('Africa', 'America') 
        group by o.region;
    """,

    "4.Countries with obesity up & malnutrition down": """
        select o.country, max(o.mean_estimate) - min(o.mean_estimate) as obesity_rise, min(m.mean_estimate) - max(m.mean_estimate) as malnutrition_drop from obesity o 
        join malnutrition m on o.country = m.country and o.year = m.year and o.gender = m.gender and o.age_group = m.age_group 
        group by o.country 
        having obesity_rise > 0 and malnutrition_drop > 0 
        order by obesity_rise desc, malnutrition_drop desc;
    """,

    "5.Age-wise trend analysis": """
        select o.age_group, avg(o.mean_estimate) as avg_obesity, avg(m.mean_estimate) as avg_malnutrition from obesity o 
        join malnutrition m on o.country = m.country and o.year = m.year and o.gender = m.gender and o.age_group = m.age_group 
        group by o.age_group 
        order by o.age_group;
    """
}


# Select query set
if table_choice == "Obesity Data":
    selected_query = st.selectbox("Select an Obesity Query", list(obesity_sql_queries.keys()))
    if selected_query:
        st.markdown(f"#### 🔍 Result for: **{selected_query}**")
        try:
            result_df = pd.read_sql(obesity_sql_queries[selected_query], conn)
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")

elif table_choice == "Malnutrition Data":
    selected_query = st.selectbox("Select a Malnutrition Query", list(malnutrition_sql_queries.keys()))
    if selected_query:
        st.markdown(f"#### 🔍 Result for: **{selected_query}**")
        try:
            result_df = pd.read_sql(malnutrition_sql_queries[selected_query], conn)
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")

elif table_choice    == "Combined Data":
    selected_query = st.selectbox("Select a Combined Query", list(combined_sql_queries.keys()))
    if selected_query:
        st.markdown(f"#### 🔍 Result for: **{selected_query}**")
        try:
            result_df = pd.read_sql(combined_sql_queries[selected_query], conn)
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Query failed: {e}")