
# Real-Time Poll Rooms (Flask + Socket.IO)

A full-stack real-time polling web application where users can create polls, share a link, vote once, and see live results update instantly without refreshing.

This project fulfills the assignment requirements:
- Poll creation with shareable link
- Join by link and vote (single choice)
- Real-time results
- Fairness / anti-abuse protections
- Data persistence
- Ready for deployment

---

## 🚀 Features

### 1. Poll Creation
Users can create a poll with:
- A question
- At least 2 options

After creation, a unique shareable link is generated.

### 2. Join by Link
Anyone with the poll link can:
- View the poll
- Vote for one option

### 3. Real-Time Results
When any user votes:
- All connected users instantly see updated results
- Implemented using WebSockets (Flask-SocketIO)

### 4. Persistence
Polls and votes are stored in SQLite database.
Refreshing the page does NOT lose data.

### 5. Enhanced UI
- Modern card-based layout
- Animated progress bars
- Live vote percentage display
- Mobile responsive design

---

## 🛡️ Fairness / Anti-Abuse Mechanisms

### Control 1: One Vote Per Browser (localStorage)
After voting, a flag is saved in browser localStorage:
```

localStorage["voted_<pollId>"] = true

```
This disables voting buttons for that poll in the same browser.

**Prevents:** Repeated voting from the same browser/device  
**Limitation:** Users can clear browser storage or use another browser/device

---

### Control 2: IP-Based Vote Restriction
The backend stores each voter’s IP address in the database.  
If the same IP tries to vote again on the same poll, the vote is rejected.

**Prevents:** Multiple votes from the same network/IP  
**Limitation:** VPNs or shared networks may bypass or block legitimate users

---

## 🧠 Tech Stack

- Backend: Flask (Python)
- Real-Time: Flask-SocketIO (WebSockets)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Styling: Custom CSS (modern responsive UI)

---

## 📁 Project Structure

```

poll-app/
│── app.py
│── requirements.txt
│── database.db (auto-created)
└── templates/
├── index.html
└── poll.html

````

---

## ⚙️ Setup Instructions (Windows / PowerShell)

### 1. Create Virtual Environment
```powershell
py -m venv venv
.\venv\Scripts\Activate
````

### 2. Install Dependencies

```powershell
pip install flask flask-socketio eventlet
```

### 3. Run the App

```powershell
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🧪 How It Works (Flow)

1. User creates poll → stored in SQLite database
2. App generates unique poll link
3. Users open link and vote
4. Vote saved in DB and IP logged
5. Server broadcasts update using WebSockets
6. All connected clients instantly see updated results

No manual refresh required.

---

## ⚠️ Edge Cases Handled

* Prevent duplicate votes from same browser
* Prevent duplicate votes from same IP
* Disable voting after user votes
* Handle page refresh without losing poll data
* Real-time sync across multiple clients

---

## 🔮 Known Limitations / Future Improvements

* VPN users can bypass IP restriction
* Users clearing browser storage can vote again
* No authentication (anonymous voting)
* Could add charts (bar/pie) for visualization
* Could add poll expiration time feature
* Could deploy with PostgreSQL for production scaling

---

## 🌍 Deployment (Suggested)

* Backend: Render
* Database: SQLite 
* Frontend: Served via Flask templates

---


