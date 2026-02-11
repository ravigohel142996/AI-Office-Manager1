# 🚀 Quick Start Guide - AI Office Manager

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ravigohel142996/AI-Office-Manager1.git
cd AI-Office-Manager1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env if you want to use OpenAI API
```

### 4. Start the Backend Server
```bash
python -m uvicorn backend.main:app --reload
```

The API will be available at: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 5. Start the Frontend (New Terminal)
```bash
streamlit run app.py
```

The web app will open at: http://localhost:8501

## First Time Usage

### Step 1: Register an Account
1. Open http://localhost:8501
2. Click the "Register" tab
3. Fill in your details:
   - Username: admin
   - Email: admin@example.com
   - Full Name: Admin User
   - Password: admin123
4. Click "Register"

### Step 2: Login
1. Switch to "Login" tab
2. Enter your credentials
3. Click "Login"

### Step 3: Explore the Dashboard
You'll see the main dashboard with:
- 📊 KPI cards (Productivity, Cost Saving, Tasks, Active Bots)
- 📈 Productivity trend chart
- 🤖 Bot performance chart
- 🔔 Recent activity log

### Step 4: Try Each Module

#### 👥 HR Bot
- Click "HR Bot" in the sidebar
- Try "Simulate Today's Attendance"
- Paste a resume in "Resume Analyzer"
- Create leave requests
- Generate performance reports

#### 📊 Analyst Bot
- Upload CSV files (sample files in `data/samples/`)
- Generate interactive charts
- Analyze trends
- Get AI-powered insights

#### 💬 Support Bot
- Create support tickets
- Use the AI chatbot
- Generate auto-replies
- View ticket statistics

#### ⚙️ Admin Bot
- Create and manage tasks
- Generate professional emails
- View upcoming reminders
- Track task completion

#### 💼 Sales Bot
- Add new leads
- View lead scores (AI-powered)
- Check sales forecasts
- Explore CRM dashboard

## Sample Data

Sample CSV files are included in `data/samples/`:
- `sales_data.csv` - Monthly sales data
- `employee_performance.csv` - Employee metrics
- `support_tickets.csv` - Ticket statistics

Use these to test the Data Analyst Bot!

## API Testing

### Using cURL

**Create a ticket:**
```bash
curl -X POST http://localhost:8000/support/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "email": "john@example.com",
    "subject": "Product Issue",
    "message": "The product is not working as expected"
  }'
```

**Get support stats:**
```bash
curl http://localhost:8000/support/stats
```

**Simulate attendance:**
```bash
curl http://localhost:8000/hr/attendance/simulate
```

### Using API Docs

Visit http://localhost:8000/docs for interactive API documentation with a "Try it out" feature!

## Common Tasks

### Add Sample Employees
```bash
curl -X POST http://localhost:8000/hr/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@company.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "salary": 85000
  }'
```

### Create a Task
```bash
curl -X POST http://localhost:8000/admin/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review Q4 Reports",
    "description": "Analyze quarterly performance",
    "assigned_to": "admin",
    "due_date": "2024-12-31T00:00:00",
    "priority": "High"
  }'
```

### Add a Lead
```bash
curl -X POST http://localhost:8000/sales/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Corp",
    "email": "contact@techcorp.com",
    "phone": "+1234567890",
    "company": "Tech Corp",
    "industry": "Technology",
    "budget": 50000,
    "source": "Website"
  }'
```

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Ensure all dependencies are installed
- Check for Python version (3.11+ recommended)

### Frontend won't start
- Check if port 8501 is available
- Ensure backend is running first
- Clear browser cache if page doesn't load

### Database issues
- Delete `ai_office_manager.db` file
- Restart the backend (it will recreate the database)

### API connection errors
- Ensure backend is running at http://localhost:8000
- Check firewall settings
- Verify no other service is using port 8000

## Configuration Options

### Using OpenAI API
Edit `.env` file:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
USE_MOCK_AI=false
```

### Using Mock AI (Default)
No configuration needed! The system uses intelligent mock responses by default.

### Custom Database
Edit `.env` file:
```bash
DATABASE_URL=sqlite:///./custom_database.db
```

### Custom Ports
Edit `.env` file:
```bash
API_HOST=0.0.0.0
API_PORT=8080
```

Then start with:
```bash
python -m uvicorn backend.main:app --port 8080
```

## Next Steps

1. **Explore all modules** - Try each bot's features
2. **Add your data** - Upload your own CSV files
3. **Customize** - Modify prompts in `backend/services/ai_service.py`
4. **Deploy** - Use Streamlit Cloud for easy deployment
5. **Integrate** - Connect to your existing systems via API

## Need Help?

- 📚 Check the main README.md for detailed documentation
- 🐛 Report issues on GitHub
- 💬 API Docs: http://localhost:8000/docs
- 📊 Sample Data: `data/samples/` directory

---

**Enjoy automating your workforce with AI!** 🤖✨
