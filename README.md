# 📌 Client Query Management System

A full-stack Support Query Management application that allows **clients to submit queries** and **support teams to track and resolve them**.  
This project aims to improve communication, reduce response time, and analyze support efficiency.

---

## 🎯 Project Objective
To build a real-time system where:
- Clients can raise support tickets
- Support team can monitor and close queries
- Queries are stored in a relational database (MySQL)
- Role-based login controls access
- Real-time updates visible on Streamlit UI

---

## 🏗 Tech Stack
| Component | Technology |
|----------|------------|
| Programming Language | Python |
| Frontend UI | Streamlit |
| Database | MySQL |
| Data Handling | Pandas |
| Security | SHA-256 password hashing |
| Libraries | mysql-connector-python, pandas, datetime |

---

## 📂 Project Features

### 👤 **User Authentication System**
- Register new users (Client / Support)
- Secure password storage using SHA-256 hashing
- Role-based login and redirection

### 📨 **Client Features**
- Submit queries via Streamlit form
- Automatically records timestamp using `datetime.now()`
- Status automatically set to `Open`
- Stored directly into MySQL table `queries`

### 🛠 **Support Team Features**
- View all Open / Closed / All queries
- Filter by status
- Select and close a query
- Automatically updates status to `Closed` with closing timestamp

### 🗄 Database Integration
- CSV dataset imported into MySQL
- Two main tables:
  - `users`
  - `queries`

---

## 🗃 Database Structure

### **users**
| Column | Type |
|--------|------|
| user_id | INT (Primary Key) |
| username | VARCHAR(100) |
| password_hash | VARCHAR(255) |
| role | ENUM('Client', 'Support') |

### **queries**
| Column | Type |
|--------|------|
| id | INT (Primary Key) |
| csv_query_id | VARCHAR(20) |
| client_email | VARCHAR(255) |
| client_mobile | BIGINT |
| query_heading | VARCHAR(255) |
| query_description | TEXT |
| status | ENUM('Open','Closed') |
| date_raised | DATETIME |
| date_closed | DATETIME |

---

## 🚀 How to Run the Project

### 1️⃣ Install Dependencies
pip install streamlit mysql-connector-python pandas


### 2️⃣ Run the Streamlit Application

### 3️⃣ Ensure MySQL Is Running
- Database name: `client_management`
- Import CSV data using Python into MySQL (already completed)

---

## 📁 Project Folder Structure
Client_Query_Management/
│── app.py
│── synthetic_client_queries.csv
│── requirements.txt
│── README.md


---

## 🧠 Learning Outcomes
- Python full-stack development
- Streamlit UI design
- MySQL database handling (insert, update, select)
- User authentication system
- Password hashing using SHA-256
- Data connectivity between Python & SQL
- Form handling and query operations

---

## 🔮 Future Enhancements
- Add analytics and visualization (Open vs Closed, trends)
- Average resolution time metrics
- Client “My Query Status” dashboard tab
- Better UI styling and themes

---

## 📸 Screenshots (To be added later)
- Login Page
- Register Page
- Client Query Form
- Support Dashboard

---

## 🧑‍💻 Developer
**Lokesh Madhavan**  
Python / Data Engineering / Streamlit / MySQL

---

## 📝 Project Status
**Core functionality completed**  
🔜 Next: visual charts & analytics + upload screenshots
