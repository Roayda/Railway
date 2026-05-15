# ==========================================
# 1. IMPORTS & REQUIREMENTS
# ==========================================
import streamlit as st
import pandas as pd
import pyodbc
from groq import Groq
import plotly.express as px
import time

# ==========================================
# 2. PAGE CONFIG & SESSION STATE
# ==========================================
st.set_page_config(
    page_title="Railways Master — Intelligence Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "messages" not in st.session_state: st.session_state.messages = []
if "theme" not in st.session_state: st.session_state.theme = "Dark"

defaults = {
    "api_key": "API KEY", # ضعِ مفتاح Groq الخاص بكِ هنا
    "db_server": r".\SQLEXPRESS",
    "db_name": "railway_dw",
    "response_lang": "Arabic",
    "analysis_tone": "Professional",
    "ai_model": "llama-3.3-70b-versatile"
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

# ==========================================
# 3. ADVANCED UI & THEME LOGIC
# ==========================================
if st.session_state["theme"] == "Dark":
    css_vars = "--bg: #0B090F; --surf: #15121D; --acc: #FFD700; --txt: #E8EDF5; --brd: rgba(255,255,255,0.1);"
    plotly_template = "plotly_dark"; chart_color = "#FFD700"
else:
    css_vars = "--bg: #F8F9FA; --surf: #FFFFFF; --acc: #D4AF37; --txt: #1A1A1A; --brd: rgba(0,0,0,0.2);"
    plotly_template = "plotly_white"; chart_color = "#D4AF37"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&family=Chakra+Petch:wght@700&display=swap');
:root {{ {css_vars} --font-head: 'Chakra Petch', sans-serif; }}
html, body, [data-testid="stAppViewContainer"] {{ background: var(--bg) !important; color: var(--txt) !important; font-family: 'DM Sans', sans-serif !important; }}
[data-testid="stHeader"] {{ display: none !important; }}
.rail-header {{ background: var(--surf); border: 1px solid var(--brd); border-radius: 12px; padding: 25px; border-bottom: 4px solid var(--acc); margin-bottom: 25px; }}
.metric-card {{ background: var(--surf); border: 1px solid var(--brd); padding: 15px; border-radius: 12px; text-align: center; border-left: 5px solid var(--acc); }}
[data-testid="stChatInput"] {{ background-color: var(--surf) !important; border: 2px solid var(--acc) !important; border-radius: 15px !important; margin-top: 30px !important; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATA ENGINE (MARS ENABLED) & LLM SCHEMA
# ==========================================
@st.cache_resource
def get_db_conn():
    try:
        conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={st.session_state['db_server']};DATABASE={st.session_state['db_name']};TrustServerCertificate=yes;Trusted_Connection=yes;Mars_Connection=Yes;"
        return pyodbc.connect(conn_str)
    except Exception as e:
        return None


DB_SCHEMA = """
Database Schema & Keys:
1. fact_table: Contains numerical metrics [Price], [Delay Minutes].
   Foreign Keys: [Purchase_Date_Key], [Journey_Date_Key], [Purchase_Time_Key], [Departure_Time_Key], [Arrival_Time_Key], [Actual_Arrival_Time_Key], [From_Station_Key], [To_Station_Key], [Ticket_Key], [Payment_Key], [Status_Key].
2. dim_station: [Station_Key], [Station_Name].
3. dim_ticket: [Ticket_Key], [Ticket Class], [Ticket Type], [Railcard].
4. dim_payment: [Payment_Key], [Payment Method], [Purchase Type].
5. dim_status: [Status_Key], [Journey Status], [Reason for Delay], [Refund Request].
6. dim_date: [Date_Key], [Day], [Month], [Year], [Month_Name].
7. dim_time: [Time_Key], [Time], [Hour], [Minute], [Seconds].

Join Logic (Strict):
- Departure Station: fact_table.From_Station_Key = dim_station.Station_Key
- Arrival Station: fact_table.To_Station_Key = dim_station.Station_Key
- Status: fact_table.Status_Key = dim_status.Status_Key
- Date: fact_table.Journey_Date_Key = dim_date.Date_Key
- Time: fact_table.Departure_Time_Key = dim_time.Time_Key (or use Arrival_Time_Key / Purchase_Time_Key based on user query context)

IMPORTANT BUSINESS RULES (Must Follow):
1. Revenue Calculation: If the user asks for "Net Revenue" or "Revenue after refunds", calculate SUM(fact_table.Price) and exclude refunded tickets (WHERE dim_status.[Refund Request] != 'Yes'). If the user asks for "Gross Revenue" or just "Total Revenue" without specifying, calculate SUM(fact_table.Price) WITHOUT excluding refunds. Be clear in your SQL aliases.
2. If the user asks about "Top Stations" or "Stations by Revenue", ALWAYS join using the Departure Station (fact_table.From_Station_Key = dim_station.Station_Key) unless they explicitly ask for arrival destinations.
"""

# ==========================================
# 5. SIDEBAR - ADVANCED CONTROL CENTER
# ==========================================
with st.sidebar:
    st.markdown(f"<h1 style='color:var(--acc); font-family:var(--font-head);'>RAILWAYS MASTER</h1>", unsafe_allow_html=True)
    
    # 🟢 Data Health Indicator
    conn = get_db_conn()
    if conn: st.success("Connected to Data Warehouse")
    else: st.error("Warehouse Offline")

    with st.expander("🎨 Interface Settings", expanded=True):
        t_opt = st.selectbox("UI Theme", ["Dark", "Light"], index=0 if st.session_state["theme"] == "Dark" else 1)
        if t_opt != st.session_state["theme"]: st.session_state["theme"] = t_opt; st.rerun()
        st.session_state["response_lang"] = st.selectbox("Response Language", ["Arabic", "English"], index=0)
    
    with st.expander("⚙️ Analysis Tone", expanded=False):
        st.session_state["analysis_tone"] = st.select_slider("Select Persona", ["Executive", "Professional", "Creative"], value="Professional")

    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []; st.rerun()

# ==========================================
# 6. MAIN INTERFACE
# ==========================================
st.markdown('<div class="rail-header"><h1 style="color:var(--acc); margin:0; font-family:var(--font-head);">RAILWAY MASTER INTELLIGENCE</h1><p>Strategic Analytics & Multi-Model AI Hub</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Intelligent Analyst", "📈 Strategic Dashboard"])

# --- TAB 1: AI CHAT ---
with tab1:
    # Top KPI Display
    if conn:
        rev_query = """
            SELECT SUM(f.Price) as v 
            FROM fact_table f 
            JOIN dim_status s ON f.Status_Key = s.Status_Key 
            WHERE s.[Refund Request] != 'Yes'
        """
        rev = pd.read_sql(rev_query, conn).iloc[0]['v']
        dly = pd.read_sql("SELECT AVG([Delay Minutes]) as v FROM fact_table WHERE [Delay Minutes] > 0", conn).iloc[0]['v']
        c1, c2 = st.columns(2)
        c1.markdown(f'<div class="metric-card"><p style="opacity:0.6; font-size:0.8rem">TOTAL REVENUE (NET)</p><div style="font-size:1.6rem; font-weight:700; color:var(--acc)">£{rev:,.0f}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><p style="opacity:0.6; font-size:0.8rem">AVG SYSTEM DELAY</p><div style="font-size:1.6rem; font-weight:700; color:var(--acc)">{dly:.1f} Min</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if user_query := st.chat_input("Ask a question about the Warehouse performance..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.markdown(user_query)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Warehouse..."):
                try:
                    client = Groq(api_key=st.session_state["api_key"])
                    
                    # 1. SQL Generation
                    sql_p = f"Write T-SQL for SQL Server. Use JOINs. Schema: {DB_SCHEMA}. Question: {user_query}. Return ONLY SQL code. Do not include markdown code block syntax."
                    query = client.chat.completions.create(model=st.session_state["ai_model"], messages=[{"role": "user", "content": sql_p}], temperature=0.1).choices[0].message.content.strip().replace("```sql", "").replace("```", "")
                    
                    df = pd.read_sql(query, get_db_conn())
                    
                    
                    ans_p = f"Analyze results: {df.to_string()}. Question: {user_query}. You MUST reply entirely in {st.session_state['response_lang']} with a {st.session_state['analysis_tone']} tone."
                    ans = client.chat.completions.create(model=st.session_state["ai_model"], messages=[{"role": "user", "content": ans_p}]).choices[0].message.content
                    
                    st.markdown(ans)
                    if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
                    with st.expander("🛠️ View SQL Logic"): st.code(query, language="sql")
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except Exception as e: st.error(f"Analysis failed: {e}")

# --- TAB 2: ACTIVE STRATEGIC DASHBOARD ---
with tab2:
    st.markdown("### 🎯 Strategic Performance Visuals")
    if conn:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**Monthly Net Revenue Trend**")
            query_rev = """
                SELECT d.Month_Name, d.Month, SUM(f.Price) as Rev 
                FROM fact_table f 
                JOIN dim_date d ON f.Purchase_Date_Key = d.Date_Key 
                JOIN dim_status s ON f.Status_Key = s.Status_Key
                WHERE s.[Refund Request] != 'Yes'
                GROUP BY d.Month_Name, d.Month 
                ORDER BY d.Month
            """
            df_rev = pd.read_sql(query_rev, conn)
            st.plotly_chart(px.area(df_rev, x="Month_Name", y="Rev", template=plotly_template, color_discrete_sequence=[chart_color]), use_container_width=True)
        
        with col_b:
            st.markdown("**Net Revenue Breakdown (Class & Type Hierarchy)**")
            query_tree = """
                SELECT t.[Ticket Class], t.[Ticket Type], SUM(f.Price) as Rev 
                FROM fact_table f 
                JOIN dim_ticket t ON f.Ticket_Key = t.Ticket_Key 
                JOIN dim_status s ON f.Status_Key = s.Status_Key
                WHERE s.[Refund Request] != 'Yes'
                GROUP BY t.[Ticket Class], t.[Ticket Type]
            """
            df_tree = pd.read_sql(query_tree, conn)
            fig_sun = px.sunburst(df_tree, path=['Ticket Class', 'Ticket Type'], values='Rev', template=plotly_template)
            st.plotly_chart(fig_sun, use_container_width=True)
        
        st.markdown("**Top 10 High-Traffic Routes (Departure Stations)**")
        query_st = """
            SELECT TOP 10 s.Station_Name, COUNT(*) as Trips 
            FROM fact_table f 
            JOIN dim_station s ON f.From_Station_Key = s.Station_Key 
            GROUP BY s.Station_Name 
            ORDER BY Trips DESC
        """
        df_st = pd.read_sql(query_st, conn)
        st.plotly_chart(px.bar(df_st, x="Station_Name", y="Trips", template=plotly_template, color_discrete_sequence=[chart_color]), use_container_width=True)