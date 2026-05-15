# 🚆 Railway Intelligence System

This repository contains the source code and project files for our graduation project on Railway Data Analysis & Engineering. The project aims to resolve "Data Fragmentation" by transforming raw, siloed records (tickets, delays, stations) into Actionable Insights that support strategic decision-making and protect company revenue.

---

## 🎯 Problem & Solution
**The Problem:** Management suffered from "operational blind spots" due to data being scattered across various CSV files. This made it difficult to track revenue leakage (such as refund claims) and accurately evaluate station performance.
**The Solution:** We built a comprehensive **End-to-End ELT Pipeline** that extracts, cleans, and loads data into a structured Data Warehouse. This data is then visualized through interactive executive dashboards and supported by an AI-powered analytical Chatbot.

---

## 🏗️ Tech Stack & Architecture

This project bridges the gap between Software Engineering and Data Analytics:
1. **Data Engineering (Python & Pandas):** Automated scripts for data cleansing, handling missing values, and transforming raw unstructured data.
2. **Data Warehouse (SQL Server):** - Architected an optimized **Star Schema** (Fact & Dimension Tables).
   - Fully relied on **SQL Stored Procedures** to handle large datasets efficiently, ensuring high-speed queries and completely avoiding standard table imports.
3. **Business Intelligence (Power BI & DAX):** Designed 6 comprehensive analytical dashboards utilizing complex DAX measures for performance ranking and scoring.
4. **AI & NLP (Chatbot & ML):** Integrated an NLP-powered Chatbot for conversational data access, alongside Machine Learning layers for anomaly and fraud detection.

---

## 📊 Dashboards & Analytics

The BI solution consists of 6 core pillars covering all operational aspects:
1. **Executive Overview:** High-level summary of total revenue, ticket sales, and key performance indicators.
2. **Operational Delays:** Root cause analysis for train delays (Technical, Weather, Signal Failures).
3. **Sales & Revenue:** Performance of sales channels (Online vs. Station) and ticket class profitability.
4. **Time Analysis:** Heatmaps and trend lines to identify peak hours and busiest days for optimal resource allocation.
5. **Route Intelligence:** Spatial profitability analysis, tracking traffic flow, and identifying bottleneck routes.
6. **Service Quality (Station Ranking):** Advanced visual analytics (Scatter Charts & Treemaps) correlating station revenue generation with operational reliability.

---

## 🛡️ Fraud & Anomaly Detection
A critical feature of this system is **Revenue Protection**. We developed a multi-layered defense system to detect high-risk anomalies in refund requests:
- Flagging multiple refund claims for single operational incidents.
- Identifying high-frequency refund requests from specific user accounts.
- Detecting high-value claims that lack corresponding actual operational delay logs.
- The system automatically cross-references these claims with actual train performance logs to alert management.

---

## 🚀 The Roadmap Ahead
- **Real-Time Streaming:** Integrating live GPS and sensor data for instantaneous tracking.
- **Predictive Analytics:** Deploying Machine Learning models to proactively predict delays and optimize maintenance cycles.
- **Mobile Integration:** Extending the dashboard and chatbot capabilities to mobile platforms for on-the-go executives.

---

## 👥 The Team
This project was executed collaboratively by a dedicated team of specialists:
- **Roayda Alaa** (Team Leader / Data Analyst)
- **Mariam Hassan** (Data Analyst)
- **Hamsa Ebrahim** (Data Analyst)
- **Farah Osama** (Data Engineer)
- **Abdelrahman Diaa** (Data Engineer)
- **Shahd Nasser** (AI Specialist)

🎓 **Supervised by:** Dr. Maged Magdy  
📍 **Faculty of Computers and Artificial Intelligence, Fayoum University**
