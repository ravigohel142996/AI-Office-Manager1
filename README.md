# 🤖 AI Office Manager

## AI Workforce Automation Platform

**One AI System that Replaces 5 Employees**: HR, Data Analyst, Customer Support, Admin Assistant, Sales Manager

---

## 🌟 Features

### 1. **HR Bot** 👥
- Attendance tracking and simulation
- AI-powered resume analyzer
- Leave request management
- Interview scheduler with AI suggestions
- Automated performance reports

### 2. **Data Analyst Bot** 📊
- CSV file upload and analysis
- Interactive chart generation (Line, Bar, Pie, Area)
- Trend analysis and predictions
- AI-powered insights
- Automated monthly reports

### 3. **Customer Support Bot** 💬
- Intelligent ticket system
- AI chatbot for instant responses
- Auto-reply generator
- Smart complaint classification
- Real-time ticket statistics

### 4. **Admin Assistant Bot** ⚙️
- Task management system
- Calendar scheduler
- Smart reminder system
- AI email generator
- Task prioritization

### 5. **Sales Bot** 💼
- Lead management system
- ML-based lead scoring
- Sales forecasting
- CRM dashboard
- Pipeline analytics

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ravigohel142996/AI-Office-Manager1.git
cd AI-Office-Manager1
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment** (optional)
```bash
cp .env.example .env
# Edit .env with your settings (OpenAI API key, etc.)
```

4. **Start the backend API**
```bash
python -m uvicorn backend.main:app --reload
```

5. **Start the Streamlit frontend** (in a new terminal)
```bash
streamlit run app.py
```

6. **Access the application**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 📁 Project Structure

```
AI-Office-Manager1/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── runtime.txt                # Python version for deployment
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── backend/
│   ├── __init__.py
│   ├── main.py                # FastAPI application
│   ├── models/
│   │   ├── database.py        # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── hr.py              # HR module endpoints
│   │   ├── support.py         # Support module endpoints
│   │   ├── admin.py           # Admin module endpoints
│   │   ├── sales.py           # Sales module endpoints
│   │   └── analytics.py       # Analytics endpoints
│   ├── services/
│   │   └── ai_service.py      # AI/ML service layer
│   └── utils/
│       └── auth.py            # Authentication utilities
├── config/
│   └── settings.py            # Configuration settings
└── data/
    └── samples/               # Sample CSV files
        ├── sales_data.csv
        ├── employee_performance.csv
        └── support_tickets.csv
```

---

## 🎯 Core Technologies

- **Frontend**: Streamlit (Modern UI with dark theme)
- **Backend**: FastAPI (High-performance API)
- **Database**: SQLite (Lightweight, file-based)
- **AI**: OpenAI API (with mock fallback)
- **Data**: Pandas, NumPy, Plotly
- **ML**: Scikit-learn
- **Authentication**: JWT tokens

---

## 📊 Key Performance Indicators

The dashboard displays real-time KPIs:
- 💼 **Productivity Score**: Overall system efficiency
- 💰 **Cost Saving**: Monthly savings vs traditional hiring
- ✅ **Tasks Completed**: Total automated tasks
- ⚡ **Active Bots**: System health status

---

## 🔐 Security Features

- User authentication with JWT tokens
- Password hashing with bcrypt
- Session management
- Secure API endpoints
- Environment-based configuration

---

## 🤖 AI Engine

The AI engine supports:
- **OpenAI Integration**: Full GPT-3.5-turbo support
- **Mock AI Mode**: For testing without API key
- **Smart Prompt Templates**: Specialized for each department
- **Context-Aware Responses**: Department-specific AI behavior

### Using OpenAI (Optional)
Set your OpenAI API key in `.env`:
```
OPENAI_API_KEY=your_actual_api_key_here
USE_MOCK_AI=false
```

### Using Mock AI (Default)
The system works out-of-the-box with intelligent mock responses:
```
USE_MOCK_AI=true
```

---

## 📖 API Documentation

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### HR Module
- `GET /hr/employees` - List all employees
- `POST /hr/employees` - Create employee
- `GET /hr/attendance/simulate` - Simulate attendance
- `POST /hr/analyze-resume` - Analyze resume with AI
- `POST /hr/leave-requests` - Create leave request
- `GET /hr/performance-report/{id}` - Get performance report

### Support Module
- `GET /support/tickets` - List tickets
- `POST /support/tickets` - Create ticket
- `POST /support/classify` - Classify ticket with AI
- `POST /support/generate-reply/{id}` - Generate AI reply
- `GET /support/stats` - Get support statistics

### Admin Module
- `GET /admin/tasks` - List tasks
- `POST /admin/tasks` - Create task
- `PUT /admin/tasks/{id}` - Update task
- `GET /admin/reminders` - Get reminders
- `POST /admin/generate-email` - Generate email with AI

### Sales Module
- `GET /sales/leads` - List leads
- `POST /sales/leads` - Create and score lead
- `POST /sales/score-lead` - Score lead with AI
- `GET /sales/forecast` - Get sales forecast
- `GET /sales/dashboard` - Get CRM dashboard

### Analytics Module
- `POST /analytics/upload-csv` - Upload and analyze CSV
- `POST /analytics/analyze-trends` - Analyze trends
- `GET /analytics/sample-data/{dataset}` - Get sample data

---

## 🎨 UI Features

- **Modern Dark Theme**: Professional, eye-friendly design
- **Responsive Layout**: Works on all screen sizes
- **Interactive Charts**: Plotly visualizations
- **Real-time Updates**: Live data refresh
- **Intuitive Navigation**: Sidebar menu system

---

## 📦 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click
4. Add secrets in Streamlit dashboard

### Local Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Run frontend
streamlit run app.py --server.port 8501
```

### Docker (Optional)

```dockerfile
# Dockerfile example
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## 🧪 Testing

### Test User Registration
1. Open the app
2. Go to "Register" tab
3. Create account
4. Login with credentials

### Test Each Module
1. **HR**: Simulate attendance, analyze resume
2. **Analytics**: Upload sample CSV from `data/samples/`
3. **Support**: Create ticket, test chatbot
4. **Admin**: Create task, generate email
5. **Sales**: Add lead, view forecast

---

## 📈 Sample Data

Sample CSV files are included in `data/samples/`:
- `sales_data.csv` - Monthly sales data
- `employee_performance.csv` - Employee metrics
- `support_tickets.csv` - Ticket statistics

Use these for testing the Analytics Bot.

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
USE_MOCK_AI=true

# Security
SECRET_KEY=your_secret_key_for_jwt

# Database
DATABASE_URL=sqlite:///./ai_office_manager.db

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

---

## 🎯 Production Ready

This system is built for production with:
- ✅ Scalable architecture
- ✅ Error handling throughout
- ✅ Secure authentication
- ✅ Database persistence
- ✅ API documentation
- ✅ Clean, maintainable code
- ✅ Modular design
- ✅ Comprehensive logging

---

## 💡 Use Cases

1. **Small Businesses**: Reduce overhead by 5 employees
2. **Startups**: Automate operations from day one
3. **Enterprises**: Departmental automation pilot
4. **Agencies**: Multi-client management
5. **Consulting**: Scalable service delivery

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Ravi Gohel**
- GitHub: [@ravigohel142996](https://github.com/ravigohel142996)

---

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- FastAPI for high-performance APIs
- OpenAI for AI capabilities
- The open-source community

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Create Issue](https://github.com/ravigohel142996/AI-Office-Manager1/issues)

---

## 🎉 Getting Started Tutorial

### Step 1: First Login
1. Start both servers (backend + frontend)
2. Open http://localhost:8501
3. Register a new account
4. Login with your credentials

### Step 2: Explore Dashboard
- View KPIs and metrics
- Check bot performance
- Review recent activity

### Step 3: Try Each Module
- **HR**: Add employees, simulate attendance
- **Analytics**: Upload CSV, generate charts
- **Support**: Create tickets, use chatbot
- **Admin**: Manage tasks, generate emails
- **Sales**: Add leads, view forecasts

### Step 4: Use AI Features
- Analyze resumes
- Score leads
- Generate email templates
- Get data insights
- Forecast trends

---

## 🚀 Roadmap

Future enhancements:
- [ ] Multi-language support
- [ ] Advanced ML models
- [ ] Mobile app
- [ ] Team collaboration features
- [ ] Integration with external services
- [ ] Voice interface
- [ ] Advanced analytics

---

**Built with ❤️ for automating the future of work**
