import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="MedQuery AI - Hospital Equipment Intelligence", layout="wide")

st.title("⚙️ MedQuery AI: Hospital Equipment Uptime & Operational Intelligence")
st.markdown("Monitor biomedical equipment status, track operational downtime, and query clinical hardware logs using natural language.")

# Database Connection Helper (matching your 'medquery_ops' file)
def run_equipment_query(user_query):
    conn = sqlite3.connect('medquery_ops')
    q = user_query.lower()
    
    if "degraded" in q or "maintenance" in q or "down" in q:
        sql = "SELECT * FROM equipment WHERE status != 'Active'"
    elif "radiology" in q or "imaging" in q:
        sql = "SELECT * FROM equipment WHERE department = 'Radiology'"
    elif "summary" in q or "status" in q:
        sql = "SELECT department, status, COUNT(equipment_id) as total_units FROM equipment GROUP BY department, status"
    else:
        sql = "SELECT * FROM equipment"
        
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return sql, df

# Executive KPI Summary Cards for Equipment Operations
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Monitored Assets", "42 Units")
col2.metric("Operational Uptime", "94.2%", delta="+1.5% vs Last Mo")
col3.metric("Critical Equipment Down", "3 Units", delta="Immediate Action", delta_color="inverse")
col4.metric("Avg Maintenance Turnaround", "4.2 Hours", delta="-0.8 hrs")

st.divider()

# Natural Language Search Interface
user_input = st.text_input("Ask an equipment or operational question (e.g., 'Show degraded equipment', 'Radiology assets', 'Department status summary'):")

if st.button("Run Equipment Intelligence Query"):
    if user_input:
        with st.spinner("Analyzing operational database schema..."):
            sql_executed, result_df = run_equipment_query(user_input)
            
            st.subheader("Executed SQL Command")
            st.code(sql_executed, language="sql")
            
            st.subheader("Query Results")
            st.dataframe(result_df, use_container_width=True)
            
            if "status" in result_df.columns:
                active_count = len(result_df[result_df["status"] == "Active"])
                st.info(f"💡 Records retrieved: **{len(result_df)} rows** (Active operational units in view: {active_count})")