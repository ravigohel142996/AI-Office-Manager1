"""Main Streamlit Application for AI Office Manager"""
import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="AI Office Manager",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE_URL = "http://localhost:8000"

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .css-1d391kg {
        background-color: #1e2130;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

def make_request(method, endpoint, **kwargs):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.request(method, url, **kwargs, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def show_login_page():
    """Display login/register page"""
    st.title("🤖 AI Office Manager")
    st.subheader("One AI System - Five Employees")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True):
                data = {"username": username, "password": password}
                result = make_request("POST", "/auth/login", json=data)
                
                if result:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.token = result.get("access_token")
                    st.success("Login successful!")
                    st.rerun()
        
        with tab2:
            st.subheader("Register")
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_fullname = st.text_input("Full Name", key="reg_fullname")
            new_password = st.text_input("Password", type="password", key="reg_password")
            
            if st.button("Register", use_container_width=True):
                data = {
                    "username": new_username,
                    "email": new_email,
                    "full_name": new_fullname,
                    "password": new_password
                }
                result = make_request("POST", "/auth/register", json=data)
                
                if result:
                    st.success("Registration successful! Please login.")

def show_dashboard():
    """Display main dashboard"""
    st.title("📊 AI Office Manager Dashboard")
    st.markdown(f"**Welcome, {st.session_state.username}!**")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💼 Productivity Score",
            value="92%",
            delta="5%"
        )
    
    with col2:
        st.metric(
            label="💰 Cost Saving",
            value="$45K/month",
            delta="$5K"
        )
    
    with col3:
        st.metric(
            label="✅ Tasks Completed",
            value="1,247",
            delta="156"
        )
    
    with col4:
        st.metric(
            label="⚡ Active Bots",
            value="5/5",
            delta="0"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Productivity Trend")
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        productivity = [85 + i * 0.5 + (i % 7) * 2 for i in range(30)]
        
        fig = px.line(
            x=dates, y=productivity,
            labels={'x': 'Date', 'y': 'Productivity %'},
            template='plotly_dark'
        )
        fig.update_traces(line_color='#4CAF50', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🤖 Bot Performance")
        bots = ['HR Bot', 'Analyst Bot', 'Support Bot', 'Admin Bot', 'Sales Bot']
        performance = [95, 88, 92, 90, 87]
        
        fig = px.bar(
            x=bots, y=performance,
            labels={'x': 'Bot', 'y': 'Performance %'},
            template='plotly_dark',
            color=performance,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activity
    st.subheader("🔔 Recent Activity")
    activities = [
        {"time": "5 min ago", "bot": "HR Bot", "action": "Processed 3 leave requests"},
        {"time": "12 min ago", "bot": "Support Bot", "action": "Resolved 2 tickets"},
        {"time": "25 min ago", "bot": "Sales Bot", "action": "Scored 5 new leads"},
        {"time": "1 hour ago", "bot": "Admin Bot", "action": "Scheduled 8 tasks"},
        {"time": "2 hours ago", "bot": "Analyst Bot", "action": "Generated monthly report"}
    ]
    
    df_activities = pd.DataFrame(activities)
    st.dataframe(df_activities, use_container_width=True, hide_index=True)

def show_hr_module():
    """Display HR module"""
    st.title("👥 HR Bot")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Attendance", "📄 Resume Analyzer", "🏖️ Leave Requests",
        "📅 Interview Scheduler", "📈 Performance Report"
    ])
    
    with tab1:
        st.subheader("Attendance Simulator")
        if st.button("Simulate Today's Attendance"):
            result = make_request("GET", "/hr/attendance/simulate")
            if result:
                st.success(f"Attendance simulated for {result['date']}")
                df = pd.DataFrame(result['records'])
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Show all attendance
        employees = make_request("GET", "/hr/employees")
        if employees:
            st.subheader("Employee List")
            df_emp = pd.DataFrame(employees)
            if not df_emp.empty:
                st.dataframe(df_emp[['name', 'department', 'position', 'email']], 
                           use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Resume Analyzer")
        resume_text = st.text_area("Paste resume text here:", height=200)
        
        if st.button("Analyze Resume"):
            if resume_text:
                result = make_request("POST", "/hr/analyze-resume", 
                                    json={"resume_text": resume_text})
                if result:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Skills Match", f"{result['skills_match']}%")
                    with col2:
                        st.metric("Experience Level", result['experience_level'])
                    with col3:
                        st.metric("Recommendation", result['recommendation'])
                    
                    st.write("**Analysis Summary:**")
                    st.write(result['summary'])
    
    with tab3:
        st.subheader("Leave Request Form")
        
        employees = make_request("GET", "/hr/employees")
        if employees:
            emp_names = {emp['id']: emp['name'] for emp in employees}
            
            selected_emp = st.selectbox("Employee", options=list(emp_names.keys()),
                                       format_func=lambda x: emp_names[x])
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
            with col2:
                end_date = st.date_input("End Date")
            
            leave_type = st.selectbox("Leave Type", 
                                     ["Sick Leave", "Casual Leave", "Vacation", "Other"])
            reason = st.text_area("Reason")
            
            if st.button("Submit Leave Request"):
                data = {
                    "employee_id": selected_emp,
                    "start_date": start_date.isoformat() + "T00:00:00",
                    "end_date": end_date.isoformat() + "T00:00:00",
                    "leave_type": leave_type,
                    "reason": reason
                }
                result = make_request("POST", "/hr/leave-requests", json=data)
                if result:
                    st.success("Leave request submitted successfully!")
        
        # Show pending requests
        st.subheader("Pending Leave Requests")
        leaves = make_request("GET", "/hr/leave-requests")
        if leaves:
            pending = [l for l in leaves if l['status'] == 'Pending']
            if pending:
                for leave in pending:
                    with st.expander(f"Request #{leave['id']} - Employee ID: {leave['employee_id']}"):
                        st.write(f"**Type:** {leave['leave_type']}")
                        st.write(f"**Dates:** {leave['start_date'][:10]} to {leave['end_date'][:10]}")
                        st.write(f"**Reason:** {leave['reason']}")
                        if st.button(f"Approve", key=f"approve_{leave['id']}"):
                            result = make_request("PUT", f"/hr/leave-requests/{leave['id']}/approve")
                            if result:
                                st.success("Leave approved!")
                                st.rerun()
    
    with tab4:
        st.subheader("Interview Scheduler")
        st.write("Schedule interviews with AI assistance")
        
        candidate_name = st.text_input("Candidate Name")
        position = st.text_input("Position")
        interview_date = st.date_input("Interview Date")
        interview_time = st.time_input("Interview Time")
        
        if st.button("Generate Interview Questions"):
            prompt = f"Generate interview questions for {position} position"
            result = make_request("POST", "/hr/analyze-resume",
                                json={"resume_text": prompt})
            if result:
                st.write("**Suggested Questions:**")
                st.write(result['summary'])
    
    with tab5:
        st.subheader("Performance Report")
        
        employees = make_request("GET", "/hr/employees")
        if employees:
            emp_names = {emp['id']: emp['name'] for emp in employees}
            selected_emp = st.selectbox("Select Employee", 
                                       options=list(emp_names.keys()),
                                       format_func=lambda x: emp_names[x],
                                       key="perf_emp")
            
            if st.button("Generate Report"):
                report = make_request("GET", f"/hr/performance-report/{selected_emp}")
                if report:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Attendance Rate", f"{report['attendance_rate']}%")
                    with col2:
                        st.metric("Total Days", report['total_days'])
                    with col3:
                        st.metric("Present Days", report['present_days'])
                    
                    st.write(f"**Employee:** {report['employee']}")
                    st.write(f"**Department:** {report['department']}")
                    st.write(f"**Position:** {report['position']}")
                    st.write(f"**Performance Score:** {report['performance_score']}")

def show_analyst_module():
    """Display Data Analyst module"""
    st.title("📊 Analyst Bot")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Upload CSV", "📈 Generate Charts", "🔍 Trend Analysis", "📑 Reports"
    ])
    
    with tab1:
        st.subheader("Upload and Analyze CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            files = {'file': uploaded_file}
            # Note: For file upload, we need multipart/form-data
            try:
                response = requests.post(f"{API_BASE_URL}/analytics/upload-csv", 
                                       files={'file': uploaded_file.getvalue()})
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Rows", result['rows'])
                    with col2:
                        st.metric("Total Columns", result['columns'])
                    with col3:
                        st.metric("Missing Values", sum(result['missing_values'].values()))
                    
                    st.write("**Columns:**", ", ".join(result['column_names']))
                    
                    st.subheader("Sample Data")
                    df_sample = pd.DataFrame(result['sample_data'])
                    st.dataframe(df_sample, use_container_width=True)
                    
                    if result['summary_stats']:
                        st.subheader("Summary Statistics")
                        df_stats = pd.DataFrame(result['summary_stats'])
                        st.dataframe(df_stats, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("Generate Charts")
        
        # Sample datasets
        dataset = st.selectbox("Select Sample Dataset",
                              ["sales", "performance", "support"])
        
        if st.button("Load Sample Data"):
            data = make_request("GET", f"/analytics/sample-data/{dataset}")
            if data:
                df = pd.DataFrame(data)
                st.session_state.chart_data = df
                st.dataframe(df, use_container_width=True)
        
        if 'chart_data' in st.session_state:
            df = st.session_state.chart_data
            
            chart_type = st.selectbox("Chart Type", 
                                     ["Line Chart", "Bar Chart", "Pie Chart", "Area Chart"])
            
            if len(df.columns) >= 2:
                x_col = st.selectbox("X-axis", df.columns)
                y_col = st.selectbox("Y-axis", [col for col in df.columns if col != x_col])
                
                if chart_type == "Line Chart":
                    fig = px.line(df, x=x_col, y=y_col, template='plotly_dark')
                elif chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_col, y=y_col, template='plotly_dark')
                elif chart_type == "Pie Chart":
                    fig = px.pie(df, names=x_col, values=y_col, template='plotly_dark')
                else:  # Area Chart
                    fig = px.area(df, x=x_col, y=y_col, template='plotly_dark')
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Trend Analysis & Prediction")
        
        st.write("Enter historical data for trend analysis:")
        data_input = st.text_input("Enter values (comma-separated)", 
                                   "100, 120, 115, 140, 135, 160")
        
        if st.button("Analyze Trends"):
            try:
                data_values = [float(x.strip()) for x in data_input.split(',')]
                result = make_request("POST", "/analytics/analyze-trends",
                                    json={"data": data_values})
                
                if result:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Trend", result['forecast']['trend'])
                    with col2:
                        st.metric("Average", result['metrics']['average'])
                    with col3:
                        st.metric("Confidence", f"{result['forecast']['confidence']}%")
                    
                    # Plot historical and forecast
                    historical = result['historical_data']
                    forecast = result['forecast']['forecast']
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        y=historical,
                        mode='lines+markers',
                        name='Historical',
                        line=dict(color='blue')
                    ))
                    fig.add_trace(go.Scatter(
                        y=forecast,
                        mode='lines+markers',
                        name='Forecast',
                        line=dict(color='red', dash='dash')
                    ))
                    fig.update_layout(template='plotly_dark', 
                                    title='Trend Analysis with Forecast')
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab4:
        st.subheader("Generate Monthly Report")
        
        report_type = st.selectbox("Report Type",
                                   ["Sales Report", "Performance Report", 
                                    "Support Report", "Financial Report"])
        
        if st.button("Generate Report"):
            st.write(f"**{report_type}**")
            st.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write("---")
            
            # Sample report content
            st.write("### Executive Summary")
            st.write("This report provides a comprehensive analysis of key metrics...")
            
            st.write("### Key Findings")
            st.write("- Metric 1: Increased by 15%")
            st.write("- Metric 2: Stable performance")
            st.write("- Metric 3: Requires attention")
            
            st.success("Report generated successfully!")

def show_support_module():
    """Display Customer Support module"""
    st.title("💬 Support Bot")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎫 Ticket System", "🤖 AI Chatbot", "✉️ Auto Reply", "📋 Classifications"
    ])
    
    with tab1:
        st.subheader("Support Ticket System")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Create New Ticket**")
            customer_name = st.text_input("Customer Name")
            email = st.text_input("Email")
            subject = st.text_input("Subject")
            message = st.text_area("Message", height=150)
            
            if st.button("Submit Ticket"):
                data = {
                    "customer_name": customer_name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
                result = make_request("POST", "/support/tickets", json=data)
                if result:
                    st.success(f"Ticket #{result['id']} created successfully!")
                    st.write(f"**Category:** {result['category']}")
                    st.write(f"**Priority:** {result['priority']}")
        
        with col2:
            # Stats
            stats = make_request("GET", "/support/stats")
            if stats:
                st.metric("Total Tickets", stats['total_tickets'])
                st.metric("Open Tickets", stats['open'])
                st.metric("Resolution Rate", f"{stats['resolution_rate']}%")
        
        st.markdown("---")
        st.subheader("Open Tickets")
        
        tickets = make_request("GET", "/support/tickets?status=Open")
        if tickets:
            for ticket in tickets[:5]:  # Show first 5
                with st.expander(f"Ticket #{ticket['id']} - {ticket['subject']}"):
                    st.write(f"**Customer:** {ticket['customer_name']}")
                    st.write(f"**Email:** {ticket['email']}")
                    st.write(f"**Category:** {ticket['category']}")
                    st.write(f"**Priority:** {ticket['priority']}")
                    st.write(f"**Message:** {ticket['message']}")
                    
                    if ticket['ai_response']:
                        st.write("**AI Response:**")
                        st.info(ticket['ai_response'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Generate Reply", key=f"reply_{ticket['id']}"):
                            reply = make_request("POST", 
                                               f"/support/generate-reply/{ticket['id']}")
                            if reply:
                                st.success("Reply generated!")
                                st.rerun()
                    with col2:
                        if st.button("Close Ticket", key=f"close_{ticket['id']}"):
                            result = make_request("PUT", f"/support/tickets/{ticket['id']}",
                                                json={"status": "Resolved"})
                            if result:
                                st.success("Ticket closed!")
                                st.rerun()
    
    with tab2:
        st.subheader("AI Chatbot")
        st.write("Ask the AI assistant anything!")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        user_input = st.text_input("Your question:", key="chat_input")
        
        if st.button("Send"):
            if user_input:
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get AI response (using ticket classification as proxy)
                result = make_request("POST", "/support/classify",
                                    json={"ticket_text": user_input})
                
                if result:
                    response = result.get('suggested_response', 'I understand your query. How can I help you further?')
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**AI:** {msg['content']}")
        
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    with tab3:
        st.subheader("Auto Reply Generator")
        
        ticket_text = st.text_area("Enter customer message:", height=150)
        
        if st.button("Generate Auto Reply"):
            if ticket_text:
                result = make_request("POST", "/support/classify",
                                    json={"ticket_text": ticket_text})
                if result:
                    st.write("**Generated Reply:**")
                    st.info(result['suggested_response'])
                    st.write(f"**Detected Category:** {result['category']}")
                    st.write(f"**Priority:** {result['priority']}")
    
    with tab4:
        st.subheader("Complaint Classification")
        
        st.write("The AI automatically classifies tickets into categories:")
        
        categories = {
            "Technical Issue": "Problems with product functionality",
            "Billing": "Payment and invoice related queries",
            "General Inquiry": "Information requests",
            "Product Feedback": "Suggestions and feature requests",
            "Complaint": "Customer complaints and issues"
        }
        
        for category, description in categories.items():
            st.write(f"**{category}:** {description}")
        
        st.markdown("---")
        
        # Show ticket distribution
        tickets = make_request("GET", "/support/tickets")
        if tickets:
            categories_count = {}
            for ticket in tickets:
                cat = ticket['category']
                categories_count[cat] = categories_count.get(cat, 0) + 1
            
            if categories_count:
                fig = px.pie(
                    names=list(categories_count.keys()),
                    values=list(categories_count.values()),
                    title="Ticket Distribution by Category",
                    template='plotly_dark'
                )
                st.plotly_chart(fig, use_container_width=True)

def show_admin_module():
    """Display Admin module"""
    st.title("⚙️ Admin Bot")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Task Manager", "📅 Calendar", "⏰ Reminders", "✉️ Email Generator"
    ])
    
    with tab1:
        st.subheader("Task Manager")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Create New Task**")
            title = st.text_input("Task Title")
            description = st.text_area("Description")
            assigned_to = st.text_input("Assigned To")
            
            col_a, col_b = st.columns(2)
            with col_a:
                due_date = st.date_input("Due Date")
            with col_b:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            
            if st.button("Create Task"):
                data = {
                    "title": title,
                    "description": description,
                    "assigned_to": assigned_to,
                    "due_date": due_date.isoformat() + "T00:00:00",
                    "priority": priority
                }
                result = make_request("POST", "/admin/tasks", json=data)
                if result:
                    st.success("Task created successfully!")
                    st.rerun()
        
        with col2:
            stats = make_request("GET", "/admin/stats")
            if stats:
                st.metric("Total Tasks", stats['total_tasks'])
                st.metric("Pending", stats['pending'])
                st.metric("Completed", stats['completed'])
                st.metric("Completion Rate", f"{stats['completion_rate']}%")
        
        st.markdown("---")
        st.subheader("Task List")
        
        status_filter = st.selectbox("Filter by Status", 
                                    ["All", "Pending", "In Progress", "Completed"])
        
        endpoint = "/admin/tasks"
        if status_filter != "All":
            endpoint += f"?status={status_filter}"
        
        tasks = make_request("GET", endpoint)
        if tasks:
            for task in tasks[:10]:  # Show first 10
                with st.expander(f"{task['title']} - {task['priority']} Priority"):
                    st.write(f"**Description:** {task['description']}")
                    st.write(f"**Assigned To:** {task['assigned_to']}")
                    st.write(f"**Due Date:** {task['due_date'][:10]}")
                    st.write(f"**Status:** {task['status']}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if task['status'] != "In Progress" and st.button("Start", key=f"start_{task['id']}"):
                            result = make_request("PUT", f"/admin/tasks/{task['id']}",
                                                json={"status": "In Progress"})
                            if result:
                                st.rerun()
                    with col2:
                        if task['status'] != "Completed" and st.button("Complete", key=f"complete_{task['id']}"):
                            result = make_request("PUT", f"/admin/tasks/{task['id']}",
                                                json={"status": "Completed"})
                            if result:
                                st.rerun()
                    with col3:
                        if st.button("Delete", key=f"delete_{task['id']}"):
                            result = make_request("DELETE", f"/admin/tasks/{task['id']}")
                            if result:
                                st.rerun()
    
    with tab2:
        st.subheader("Calendar Scheduler")
        st.write("Upcoming tasks and deadlines")
        
        tasks = make_request("GET", "/admin/tasks?status=Pending")
        if tasks:
            # Create calendar view
            df = pd.DataFrame(tasks)
            if not df.empty and 'due_date' in df.columns:
                df['due_date'] = pd.to_datetime(df['due_date'])
                df = df.sort_values('due_date')
                
                st.dataframe(
                    df[['title', 'assigned_to', 'due_date', 'priority', 'status']],
                    use_container_width=True,
                    hide_index=True
                )
    
    with tab3:
        st.subheader("Task Reminders")
        
        reminders = make_request("GET", "/admin/reminders")
        if reminders:
            st.write(f"You have {len(reminders)} upcoming tasks:")
            
            for reminder in reminders:
                days = reminder['days_until']
                if days == 0:
                    urgency = "🔴 Due Today!"
                elif days == 1:
                    urgency = "🟡 Due Tomorrow"
                elif days <= 3:
                    urgency = f"🟢 Due in {days} days"
                else:
                    urgency = f"Due in {days} days"
                
                st.warning(f"{urgency} - **{reminder['title']}** ({reminder['priority']} Priority)")
        else:
            st.info("No upcoming task reminders")
    
    with tab4:
        st.subheader("AI Email Generator")
        
        email_subject = st.text_input("Email Subject")
        email_context = st.text_area("Context/Key Points", height=100)
        
        if st.button("Generate Email"):
            if email_subject and email_context:
                result = make_request("POST", 
                                    f"/admin/generate-email?subject={email_subject}&context={email_context}")
                if result:
                    st.write("**Generated Email:**")
                    st.text_area("", value=result['email'], height=200)
                    st.success("Email generated! You can copy and use it.")

def show_sales_module():
    """Display Sales module"""
    st.title("💼 Sales Bot")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Lead Management", "🎯 Lead Scoring", "📈 Sales Forecast", "📊 CRM Dashboard"
    ])
    
    with tab1:
        st.subheader("Lead Input Form")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            name = st.text_input("Lead Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            company = st.text_input("Company")
            
            col_a, col_b = st.columns(2)
            with col_a:
                industry = st.selectbox("Industry", [
                    "Technology", "Finance", "Healthcare", "Manufacturing",
                    "Retail", "Education", "Other"
                ])
            with col_b:
                source = st.selectbox("Source", [
                    "Website", "Referral", "Direct", "Social Media", 
                    "Advertisement", "Event"
                ])
            
            budget = st.number_input("Budget ($)", min_value=0, value=10000)
            
            if st.button("Add Lead"):
                data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "company": company,
                    "industry": industry,
                    "budget": budget,
                    "source": source
                }
                result = make_request("POST", "/sales/leads", json=data)
                if result:
                    st.success(f"Lead added with score: {result['lead']['score']}/100")
                    st.write(f"**Recommendation:** {result['scoring']['recommendation']}")
                    st.rerun()
        
        with col2:
            st.write("**Quick Stats**")
            dashboard = make_request("GET", "/sales/dashboard")
            if dashboard:
                st.metric("Total Leads", dashboard['total_leads'])
                st.metric("Conversion Rate", f"{dashboard['conversion_rate']}%")
                st.metric("Avg Score", f"{dashboard['average_score']}/100")
        
        st.markdown("---")
        st.subheader("Lead List")
        
        leads = make_request("GET", "/sales/leads")
        if leads:
            df = pd.DataFrame(leads)
            if not df.empty:
                st.dataframe(
                    df[['name', 'company', 'industry', 'budget', 'score', 'status']],
                    use_container_width=True,
                    hide_index=True
                )
    
    with tab2:
        st.subheader("Lead Scoring System")
        
        st.write("Our AI-powered lead scoring system evaluates leads based on:")
        st.write("- 💰 Budget (30 points)")
        st.write("- 🏢 Industry (25 points)")
        st.write("- 📍 Source (25 points)")
        st.write("- ✅ Company presence (20 points)")
        
        st.markdown("---")
        
        st.write("**Test Lead Scoring**")
        
        test_budget = st.number_input("Budget", min_value=0, value=50000, key="test_budget")
        test_industry = st.selectbox("Industry", [
            "Technology", "Finance", "Healthcare", "Manufacturing",
            "Retail", "Education", "Other"
        ], key="test_industry")
        test_source = st.selectbox("Source", [
            "Website", "Referral", "Direct", "Social Media"
        ], key="test_source")
        
        if st.button("Calculate Score"):
            data = {
                "name": "Test Lead",
                "company": "Test Company",
                "industry": test_industry,
                "budget": test_budget,
                "source": test_source
            }
            result = make_request("POST", "/sales/score-lead", json=data)
            if result:
                st.metric("Lead Score", f"{result['score']}/100")
                st.write("**Factors:**")
                for factor in result['factors']:
                    st.write(f"✓ {factor}")
                st.write(f"**Recommendation:** {result['recommendation']}")
    
    with tab3:
        st.subheader("Sales Forecast")
        
        if st.button("Generate Forecast"):
            forecast = make_request("GET", "/sales/forecast")
            if forecast:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Pipeline", f"${forecast['current_pipeline']:,.0f}")
                with col2:
                    st.metric("Trend", forecast['forecast']['trend'])
                with col3:
                    st.metric("High Value Leads", forecast['high_value_leads'])
                
                # Plot forecast
                forecast_values = forecast['forecast']['forecast']
                periods = [f"Q{i+1}" for i in range(len(forecast_values))]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=periods,
                    y=forecast_values,
                    name='Forecasted Revenue',
                    marker_color='lightblue'
                ))
                fig.update_layout(
                    template='plotly_dark',
                    title='Revenue Forecast',
                    yaxis_title='Revenue ($)'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("CRM Dashboard")
        
        dashboard = make_request("GET", "/sales/dashboard")
        if dashboard:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Leads", dashboard['total_leads'])
            with col2:
                st.metric("New Leads", dashboard['new_leads'])
            with col3:
                st.metric("Qualified", dashboard['qualified_leads'])
            with col4:
                st.metric("Converted", dashboard['converted_leads'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Conversion funnel
                funnel_data = {
                    'Stage': ['New', 'Qualified', 'Converted'],
                    'Count': [
                        dashboard['new_leads'],
                        dashboard['qualified_leads'],
                        dashboard['converted_leads']
                    ]
                }
                fig = px.funnel(
                    funnel_data,
                    x='Count',
                    y='Stage',
                    template='plotly_dark',
                    title='Sales Funnel'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Industry distribution
                if dashboard['industries']:
                    fig = px.pie(
                        names=list(dashboard['industries'].keys()),
                        values=list(dashboard['industries'].values()),
                        template='plotly_dark',
                        title='Leads by Industry'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Key metrics
            st.subheader("Key Performance Indicators")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Conversion Rate", f"{dashboard['conversion_rate']}%")
            with col2:
                st.metric("Total Pipeline Value", f"${dashboard['total_pipeline']:,.2f}")

def main():
    """Main application logic"""
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.title("🤖 AI Office Manager")
            st.markdown(f"**User:** {st.session_state.username}")
            
            st.markdown("---")
            
            menu = st.radio(
                "Navigation",
                ["📊 Dashboard", "👥 HR Bot", "📊 Analyst Bot", 
                 "💬 Support Bot", "⚙️ Admin Bot", "💼 Sales Bot"]
            )
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.rerun()
            
            st.markdown("---")
            st.caption("AI Office Manager v1.0")
            st.caption("Powered by AI")
        
        # Main content
        if menu == "📊 Dashboard":
            show_dashboard()
        elif menu == "👥 HR Bot":
            show_hr_module()
        elif menu == "📊 Analyst Bot":
            show_analyst_module()
        elif menu == "💬 Support Bot":
            show_support_module()
        elif menu == "⚙️ Admin Bot":
            show_admin_module()
        elif menu == "💼 Sales Bot":
            show_sales_module()

if __name__ == "__main__":
    main()
