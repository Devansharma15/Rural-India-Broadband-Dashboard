🚀 Rural India Broadband Dashboard

Description:
This dashboard provides comprehensive insights into broadband connectivity trends, demographic patterns, and digital disparities in rural India using public datasets and advanced visualizations.

📈 Features

1. Interactive map of broadband penetration
2. Growth trends in rural internet subscriptions
3. Demographic comparison: urban vs rural
4. Public data sources (TRAI, Census, NSS, MoSPI)

📁 Structure

1.Feature	Source
2.State data	TRAI, Census
3.Time-series	TRAI reports
4.Demographics	NSSO
5.Visuals	Plotly, Streamlit

🗂️ Suggested GitHub Repo Structure
```
rural-broadband-analysis/
├── app.py
├── README.md
├── requirements.txt
├── utils/
│   ├── data_generator.py
│   └── helper.py
├── assets/
│   ├── screenshots/
│   └── geojson/
├── docs/
│   └── report.pdf
```
🖼️ Screenshots : 

1. Geographic Analysis - 
   ![image](https://github.com/user-attachments/assets/53254755-3495-483f-9196-c01cadcd3fbf)
   ![image](https://github.com/user-attachments/assets/742b39d8-e1c4-451e-8416-984c6eec2430)

2. Demographic Analysis -
   ![image](https://github.com/user-attachments/assets/8f838769-9c08-46c4-a703-dd94d00a6212)
   ![image](https://github.com/user-attachments/assets/9117952e-992b-4a58-ad91-9607a262ac54)

3. Time Analysis -
   ![image](https://github.com/user-attachments/assets/f22b05c2-c1c4-4acb-91a8-34d3cfa96125)

4. Usage Patterns -
   ![image](https://github.com/user-attachments/assets/4c4cf160-ff6d-4f06-a415-9ff5a751802d)
   ![image](https://github.com/user-attachments/assets/b1eeefdb-f0b9-48ab-901e-3940a761f5ee)

5. Insights and Recommnedations -
   ![image](https://github.com/user-attachments/assets/054838db-8f9c-4c70-b095-f9cce2006d16)
   ![image](https://github.com/user-attachments/assets/e2ec6dda-018d-428f-8909-3c02beca73cb)
   ![image](https://github.com/user-attachments/assets/cd835039-f601-495b-bf57-286c3d1f3979)
   
💻 Run Locally

git clone https://github.com/yourusername/rural-broadband-analysis.git
cd rural-broadband-analysis
streamlit run app.py
