# Live Order Tracking System

## 📌 Overview
The Live Order Tracking System is a backend service designed for logistics and delivery platforms to track orders in real time.  
It supports order creation, controlled status updates, live notifications, and complete historical traceability for auditing and reporting.

This project focuses on **correctness, reliability, and system behavior** rather than UI complexity.

---

## 🛠 Tech Stack
- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Real-Time Updates:** WebSockets
- **Language:** Python 3

---

## 🚀 Features
- Create new delivery orders
- Update order status with strict validation
- Prevent invalid status transitions
- Retrieve current order state
- Retrieve full order status history
- List all active (non-delivered) orders
- Real-time order updates via WebSockets
- Clear error handling and validation

---

## 🔄 Order Status Flow
The system enforces valid order state transitions:


Invalid transitions are rejected with meaningful errors.

---

## 📡 API Endpoints

### Orders
- **POST** `/orders`  
  Create a new order

- **GET** `/orders`  
  Retrieve all active orders

- **GET** `/orders/{order_id}`  
  Retrieve current state of an order

- **PATCH** `/orders/{order_id}/status`  
  Update order status

- **GET** `/orders/{order_id}/history`  
  Retrieve complete status history

### Health Check
- **GET** `/`  
  API health status

---

## 🔴 Real-Time Updates (WebSocket)
The system supports live order updates using WebSockets.

**WebSocket Endpoint:**

Clients connected to this endpoint receive real-time notifications whenever an order is created or updated.

> Note: WebSocket endpoints do not appear in Swagger UI by design.

---

## 🧱 Data Model

### Orders Table
Stores the current state of each order:
- Order ID (UUID)
- Customer details
- Merchant reference
- Current status
- Created & updated timestamps
- Version (for concurrency safety)

### Order Status History Table
Stores immutable historical records:
- Order ID
- Status
- Update source
- Timestamp

This design ensures full traceability and auditability.

---

## 🔐 Reliability & Concurrency Handling
- Strict validation of order status transitions
- Database transactions ensure atomic updates
- Immutable history prevents data loss
- Versioning supports optimistic locking
- Clear HTTP error responses for invalid operations

---

## ▶️ How to Run Locally

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Seban007/live-order-tracking-system.git
cd live-order-tracking-system
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install fastapi uvicorn sqlalchemy

4️⃣ Run the Server
uvicorn app.main:app --reload

5️⃣ Open Swagger UI
http://127.0.0.1:8000/docs

🧪 Testing

All APIs can be tested using Swagger UI

Invalid status transitions return proper error messages

WebSocket functionality can be tested using browser console or WebSocket clients

📌 Future Improvements

Authentication & authorization

Role-based access control

PostgreSQL support

Containerization with Docker

Deployment to cloud platforms

👤 Author

Seban007

📄 License

This project is created for educational and interview evaluation purposes.


---
1. Save this as **README.md**
2. Run:
```powershell
git add README.md
git commit -m "Add complete README documentation"
git push
