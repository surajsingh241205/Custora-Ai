![Alt text](static/images/light-logo.png)
# Custora Ai – End-to-End Machine Learning SaaS Application

## Overview

**Custora AI** is a full-stack Machine Learning web application built using Flask that enables businesses to upload customer datasets and predict churn probability in real time.

This project demonstrates real-world ML deployment from model training to a working SaaS-style web interface.

It is not just a model. It is a complete product pipeline.

---

##  Problem Statement

Customer churn directly affects business revenue.  
Many companies struggle to analyze churn risk from raw customer data.

Custora AI solves this by:

- Accepting structured CSV datasets
- Processing telecom-style customer data
- Generating churn probability predictions
- Displaying percentage-based risk scores
- Helping businesses take proactive retention decisions

---

## Key Features

- 🔐 User Registration & Login System  
- 📊 Interactive Dashboard  
- 📂 CSV Upload Support  
- 🤖 Machine Learning Model Integration  
- 📈 Churn Probability Output (%)  
- 📥 Downloadable Prediction Results (CSV)  
- 🔎 First 10 Rows Preview for Large Datasets  
- ⚡ Lightweight and Fast Flask Backend  

---

## Tech Stack

### Backend
- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Pickle

### Frontend
- HTML
- CSS
- JavaScript
- Jinja2 Templates

### Database
- SQLite (Flask Instance DB)

---

## Machine Learning Pipeline

1. Data Cleaning & Preprocessing  
2. Feature Encoding  
3. Model Training (Classification Model)  
4. Model Serialization using Pickle  
5. Model Deployment inside Flask App  
6. Real-time CSV Prediction Handling  

---

## 📂 Project Structure

```
├── 📁 .ipynb_checkpoints
│   └── 📄 customer churn data analysis-checkpoint.ipynb
├── 📁 .virtual_documents
│   └── 📄 customer churn data analysis.ipynb
├── 📁 Data
│   ├── 📁 .ipynb_checkpoints
│   │   └── 📄 Telco-Customer-Churn-checkpoint.csv
│   └── 📄 Telco-Customer-Churn.csv
├── 📁 instance
├── 📁 models
│   ├── 🐍 __init__.py
│   └── 🐍 user.py
├── 📁 routes
│   ├── 🐍 __init__.py
│   ├── 🐍 auth.py
│   └── 🐍 main.py
├── 📁 services
│   ├── 🐍 __init__.py
│   ├── 🐍 ai_summary.py
│   ├── 🐍 pdf_report.py
│   └── 🐍 prediction.py
├── 📁 static
│   ├── 📁 css
│   ├── 📁 images
│   │   ├── 🖼️ 4-removebg-preview.png
│   │   ├── 🖼️ dark-logo.png
│   │   └── 🖼️ light-logo.png
│   └── 📁 js
├── 📁 templates
│   ├── 🌐 base.html
│   ├── 🌐 dashboard.html
│   ├── 🌐 landing.html
│   ├── 🌐 login.html
│   ├── 🌐 register.html
│   ├── 🌐 results.html
│   └── 🌐 upload.html
├── 📁 utils
│   ├── 🐍 __init__.py
│   └── 🐍 data_validation.py
├── ⚙️ .gitignore
├── 📄 Procfile
├── 🐍 app.py
├── 📄 churn_model.pkl
├── 🐍 config.py
├── 📄 customer churn data analysis.ipynb
├── 🐍 extensions.py
├── 📝 readme.md
├── ⚙️ render.yaml
└── 📄 requirements.txt
```
---

## Sample Output

| Churn Probability (%) | Prediction |
|------------------------|------------|
| 96.52                  | 1          |
| 2.83                   | 0          |
| 72.84                  | 1          |
| 8.10                   | 0          |

---

## Challenges Faced During Development

- API key configuration issues
- Handling large CSV uploads
- Preventing frontend crash during heavy data rendering
- file structuring
- Model integration with real-time user uploads

---

## Future Improvements

- Multi-model support (Modular ML tools)
- Admin analytics dashboard
- Deployment on cloud (AWS / Render / Railway)
- Payment integration for SaaS model
- Better UI/UX enhancements
- Role-based access control
- Model performance monitoring

---

## Learning Outcomes

- End-to-end ML deployment
- Full-stack application structuring
- SaaS-oriented thinking
- Real-world dataset handling
- Scalable project architecture design

---

## Author

Suraj Singh
[Linkedin](nkedin.com/in/suraj-singh-data-science/)  
Aspiring Data Scientist | Full Stack Developer  
Building real-world ML products for business impact.

---

## ⭐ If You Found This Project Useful

Give it a star ⭐ and connect to collaborate!
