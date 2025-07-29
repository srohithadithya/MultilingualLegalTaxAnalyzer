---

# **Multi-Lingual Legal Tax Analyzer**

## **Unleash the Power of AI for Seamless Tax Document Analysis**

Welcome to the **Multi-Lingual Legal Tax Analyzer**, an innovative application designed to revolutionize how individuals and businesses manage their tax-related documents. Leveraging cutting-edge AI and advanced OCR technology, this platform offers a secure, accurate, and incredibly efficient way to process, translate, and understand your financial records across multiple languages.

---

## **Why Choose Our Analyzer?**

Traditional tax document processing is often manual, time-consuming, and prone to errors, especially when dealing with diverse languages. Our Multi-Lingual Legal Tax Analyzer stands out by offering:

* **Hybrid OCR Accuracy:** We combine the robustness of **Tesseract** for foundational text extraction with the cutting-edge intelligence of **Ollama Vision** (a local multi-modal LLM like LLaVA) for deep contextual understanding. This powerful duo ensures highly accurate data extraction from even the most complex and varied document formats.  
* **Intelligent Data Extraction:** Beyond simple OCR, our AI intelligently identifies and extracts crucial details such as **dates, GST/VAT numbers, company names, line items, totals, and more** from unstructured invoices and receipts.  
* **Seamless Multilingual Support:** Upload documents in one language, choose your preferred analysis and output language, and receive perfectly translated, structured data. This breaks down language barriers in financial compliance.  
* **Structured & Actionable Output:** Get your analyzed data presented in a clean, organized, and downloadable **PDF report**.  
* **Speak Your Data:** Experience the unique feature of **speech synthesis**, allowing you to listen to your translated, formatted tax data in your chosen language – making review incredibly convenient.  
* **Secure & Intuitive:** Your financial data is handled with the highest security standards. Our user-friendly interface boasts modern design, responsive layouts, and subtle animations for a truly impressive user experience.

---

## **Features At a Glance**

* **Secure Authentication:** Robust Login and Signup with high-end security.  
* **Personalized Dashboard:** Access and manage all your previously analyzed documents.  
* **Flexible Document Upload:** Supports all common formats (PDF, JPG, PNG, TIFF) with easy drag-and-drop or direct scan options.  
* **Dynamic Language Selection:** Choose your analysis and output language from a wide range of options.  
* **Precision Data Extraction:** Automated recognition and extraction of critical tax entities (dates, GSTs, names, amounts, etc.).  
* **Structured PDF Reports:** Generate professional, easy-to-understand summaries of your tax data.  
* **Interactive Speech Output:** Listen to your translated, formatted data for convenient review.  
* **Robust & Responsive Design:** Built with performance and user experience in mind, ensuring a smooth flow across all devices.

---

## **Technologies Used**

This project is built using a powerful and modern tech stack:

* **Backend:** Python 3.12.0 with Flask  
* **Database:** PostgreSQL  
* **OCR & AI Analysis:** Tesseract OCR and Ollama Vision (local LLaVA-like models)  
* **Frontend:** React with Vite, SASS/SCSS for styling, and engaging CSS/JS animations.  
* **Deployment:** Frontend on Netlify, Backend on Render (or similar PaaS).

---

## **Project Structure**

This project follows a clear **separation of concerns**, with distinct directories for the backend Flask application and the frontend React application. This modularity ensures scalability, maintainability, and allows for independent development and deployment.

multi-lingual-tax-analyzer/  
├── .gitignore                    \# Specifies intentionally untracked files (e.g., venv, node\_modules, .env, build/dist)  
├── README.md                     \# Project overview, setup, and structure  
├── CNAME (optional)              \# For custom domain with Netlify  
│  
├── backend/                      \# Root directory for the Flask backend application  
│   ├── .env                      \# Environment variables (sensitive data \- DO NOT COMMIT\!)  
│   ├── .flaskenv                 \# Flask CLI environment variables (FLASK\_APP, FLASK\_ENV)  
│   ├── requirements.txt          \# Python dependencies for the backend  
│   ├── run.py                    \# Script to run Flask development server  
│   ├── wsgi.py                   \# Entry point for production WSGI servers (Gunicorn/uWSGI)  
│   ├── instance/                 \# Instance-specific configurations (local settings, sensitive data not in .env)  
│   │   └── config.py             \# Example: machine-specific paths, very secret keys  
│   │  
│   ├── migrations/               \# Database migrations managed by Flask-Migrate (Alembic)  
│   │   ├── env.py                \# Alembic environment script  
│   │   ├── script.py.mako        \# Template for new migration files  
│   │   ├── versions/             \# Directory where migration scripts are generated  
│   │   │   └── \<timestamp\>\_initial\_migration.py \# Example: First migration creating tables  
│   │   └── README                \# Alembic's default README  
│   │  
│   ├── tests/                    \# Unit and integration tests for backend components  
│   │   ├── \_\_init\_\_.py           \# Makes 'tests' a Python package  
│   │   ├── conftest.py           \# Pytest fixtures for app setup, test client, mock data  
│   │   ├── test\_auth.py          \# Tests for user authentication  
│   │   ├── test\_dashboard.py     \# Tests for user dashboard data retrieval  
│   │   ├── test\_document\_upload.py \# Tests for file upload and initial processing  
│   │   ├── test\_analysis.py      \# Tests for analysis results, PDF/speech generation  
│   │   └── test\_ocr.py           \# Core tests for Tesseract and Ollama Vision integration  
│   │  
│   ├── venv/                     \# Python virtual environment (IGNORED BY GIT)  
│   │   └── \<various\_venv\_files\_and\_folders\>  
│   │  
│   └── app/                      \# The core Flask application package  
│       ├── \_\_init\_\_.py           \# Flask app factory, extension initialization, blueprint registration, logging  
│       ├── config.py             \# Application configuration classes (Base, Development, Production, Testing)  
│       ├── models.py             \# SQLAlchemy ORM models defining database schema  
│       ├── schemas.py            \# Marshmallow schemas for API data validation and serialization/deserialization  
│       │  
│       ├── routes/               \# Flask Blueprints for API endpoints  
│       │   ├── \_\_init\_\_.py       \# Initializes routes package  
│       │   ├── auth.py           \# Authentication routes  
│       │   ├── dashboard.py      \# User dashboard routes  
│       │   ├── document\_upload.py \# Document upload/scan routes  
│       │   └── analysis.py       \# Document analysis routes  
│       │  
│       ├── services/             \# Business logic and external API integrations  
│       │   ├── \_\_init\_\_.py       \# Initializes services package  
│       │   ├── ocr\_service.py    \# Tesseract and Ollama Vision integration  
│       │   ├── data\_extraction\_service.py \# Data refinement and validation  
│       │   ├── translation\_service.py     \# Translation APIs integration  
│       │   ├── pdf\_generation\_service.py  \# PDF report generation  
│       │   └── speech\_synthesis\_service.py \# Text-to-speech generation  
│       │  
│       ├── utils/                \# Helper functions and general utilities  
│       │   ├── \_\_init\_\_.py       \# Initializes utils package  
│       │   ├── security.py       \# Password hashing, key generation  
│       │   └── validators.py     \# Input validation, file handling helpers  
│       │  
│       ├── templates/            \# Jinja2 templates for server-rendered HTML (e.g., error pages)  
│       │   ├── base.html         \# Base HTML template  
│       │   ├── auth/             \# Basic HTML forms for auth (optional, if not fully React-rendered)  
│       │   │   ├── login.html  
│       │   │   └── signup.html  
│       │   └── errors/           \# HTML templates for HTTP error pages  
│       │       ├── 404.html  
│       │       └── 500.html  
│       │  
│       └── static/               \# Static assets served directly by Flask (for templates, favicon)  
│           ├── css/  
│           │   └── style.css     \# Basic CSS for Flask-rendered HTML  
│           ├── js/  
│           │   └── main.js       \# Minimal JavaScript for Flask-rendered HTML  
│           └── images/  
│               ├── logo.png      \# Project logo for Flask pages (placeholder)  
│               └── favicon.ico   \# Website favicon (placeholder)  
│  
└── frontend/                     \# Root directory for the React frontend application  
    ├── index.html                \# Main entry HTML file  
    ├── vite.config.js            \# Vite configuration file  
    ├── package.json              \# Frontend dependencies and scripts  
    ├── package-lock.json         \# Locks dependency versions  
    ├── .env.development          \# Environment variables for dev (VITE\_API\_BASE\_URL)  
    ├── .env.production           \# Environment variables for prod  
    ├── .gitignore                \# Git ignore for frontend-specific files (node\_modules, dist)  
    ├── netlify.toml              \# Netlify configuration for deployment  
    ├── public/                   \# Static assets served directly (e.g., favicon, robots.txt)  
    │   ├── favicon.ico  
    │   └── robots.txt  
    │  
    └── src/                      \# Core application source code  
        ├── main.jsx              \# Entry point for your React application  
        ├── App.jsx               \# Main application component (handles routing, global context)  
        ├── index.css             \# Global CSS styles  
        │  
        ├── assets/               \# Static assets imported into components (images, fonts, icons)  
        │   ├── images/  
        │   │   └── analyzer-logo.svg \# Project logo (example SVG provided)  
        │   ├── fonts/  
        │   │   └── Roboto-Regular.ttf \# Example font (placeholder)  
        │   └── icons/  
        │       ├── upload-icon.svg    \# Icon for document upload (example SVG provided)  
        │       ├── download-icon.svg  \# Icon for PDF download (example SVG provided)  
        │       └── play-icon.svg      \# Icon for speech playback (example SVG provided)  
        │  
        ├── components/           \# Reusable UI components (generic, presentational)  
        │   ├── Button/  
        │   │   ├── Button.jsx  
        │   │   └── Button.module.scss  
        │   ├── Modal/  
        │   │   ├── Modal.jsx  
        │   │   └── Modal.module.scss  
        │   ├── LoadingSpinner/  
        │   │   ├── LoadingSpinner.jsx  
        │   │   └── LoadingSpinner.module.scss  
        │   ├── LanguageSelector/  
        │   │   ├── LanguageSelector.jsx  
        │   │   └── LanguageSelector.module.scss  
        │   └── DataTable/  
        │       ├── DataTable.jsx  
        │       └── DataTable.module.scss  
        │  
        ├── layouts/              \# Components for overall page structure/layouts  
        │   ├── MainLayout.jsx    \# Layout for authenticated users (with header, footer, global messages)  
        │   ├── MainLayout.module.scss  
        │   ├── AuthLayout.jsx    \# Layout for login/signup pages (minimal)  
        │   └── AuthLayout.module.scss  
        │  
        ├── pages/                \# Route-level components (represent full pages)  
        │   ├── HomePage/         \# Introduction page with login/signup forms  
        │   │   ├── HomePage.jsx  
        │   │   └── HomePage.module.scss  
        │   ├── DashboardPage/    \# User dashboard  
        │   │   ├── DashboardPage.jsx  
        │   │   └── DashboardPage.module.scss  
        │   ├── AnalysisResultPage/ \# Displays detailed analysis results  
        │   │   ├── AnalysisResultPage.jsx  
        │   │   └── AnalysisResultPage.module.scss  
        │   └── NotFoundPage.jsx  \# 404 Not Found page  
        │  
        ├── features/             \# Grouping files by domain-specific features  
        │   ├── auth/  
        │   │   ├── components/   \# Auth-specific components (LoginForm, SignupForm)  
        │   │   │   ├── LoginForm.jsx  
        │   │   │   └── SignupForm.jsx  
        │   │   │   └── AuthForms.module.scss  
        │   │   ├── hooks/        \# Auth-specific custom hooks  
        │   │   │   └── useAuth.js  
        │   │   └── authService.js \# API calls related to authentication  
        │   │   └── AuthProvider.jsx \# Context provider for authentication state (serves as auth store)  
        │   │  
        │   └── document-analysis/  
        │       ├── components/   \# Components specific to document analysis (UploadForm, AnalysisDisplay)  
        │       │   ├── DocumentUploader.jsx  
        │       │   │   └── DocumentUploader.module.scss  
        │       │   ├── PreviousAnalysisTable.jsx  
        │       │   │   └── PreviousAnalysisTable.module.scss  
        │       │   ├── AnalysisDisplay.jsx  
        │       │   │   └── AnalysisDisplay.module.scss  
        │       │   └── (other analysis-specific components)  
        │       ├── hooks/        \# Hooks specific to analysis  
        │       │   └── useDocumentAnalysis.js  
        │       └── analysisService.js \# API calls/orchestration for document analysis  
        │  
        ├── hooks/                \# Global/reusable custom React hooks  
        │   └── useDebounce.js  
        │  
        ├── services/             \# API clients and external service integrations  
        │   ├── api.js            \# Axios instance configuration  
        │   └── documentApi.js    \# Specific API calls for documents/analysis (used by analysisService)  
        │  
        ├── store/                \# Global state management (Context API)  
        │   ├── messageStore.js   \# Manages global success/error/info messages  
        │   └── appStore.js       \# General application state (e.g., theme, global loading)  
        │  
        ├── styles/               \# Global styling assets (variables, mixins, theme, shared utilities)  
        │   ├── \_variables.scss   \# SCSS variables  
        │   ├── \_mixins.scss      \# SCSS mixins  
        │   ├── \_animations.scss  \# Keyframe animations  
        │   ├── \_utilities.scss   \# Utility classes  
        │   └── global.scss       \# Main global SCSS file  
        │  
        ├── utils/                \# Small, pure utility functions  
        │   ├── dateUtils.js      \# Date formatting utilities  
        │   └── validationUtils.js \# Client-side form validation  
        │  
        └── router/               \# React Router configuration  
            └── AppRouter.jsx     \# Defines routes and handles route protection

---

## **Project Setup & Local Development**

Follow these steps to get the Multi-Lingual Legal Tax Analyzer running on your local machine.

### **Prerequisites**

* **Git** (version control)  
* **Python 3.12.0** and pip (for backend)  
* **Node.js** and npm (for frontend)  
* **PostgreSQL** (database server, running locally)  
* **Tesseract OCR** (installed system-wide, added to PATH)  
* **Ollama Desktop Application / Server** (running locally, with a vision model like llava pulled)

### **1\. Clone the Repository**

git clone https://github.com/your-username/multi-lingual-tax-analyzer.git  
cd multi-lingual-tax-analyzer

### **2\. Backend Setup**

cd backend

\# Create and activate a Python virtual environment  
python3.12 \-m venv venv  
\# On Windows: .\\venv\\Scripts\\activate  
\# On macOS/Linux: source venv/bin/activate

\# Install Python dependencies  
pip install \-r requirements.txt

\# Create your .env file  
\# IMPORTANT: This file should NOT be committed to Git\!  
\# Replace placeholders with your actual secrets and database credentials.  
\# Make sure your PostgreSQL server is running and accessible.  
touch .env

**backend/.env example (copy and paste this into your .env file):**

SECRET\_KEY=your\_very\_secret\_key\_here\_generate\_a\_long\_random\_one  
DATABASE\_URL=postgresql://tax\_analyzer\_user:your\_secure\_password@127.0.0.1:5432/tax\_analyzer\_db  
OLLAMA\_API\_BASE\_URL=http://localhost:11434  
\# Optional: Path to your Google Cloud service account key if using Google Cloud APIs for translation/TTS  
\# GOOGLE\_APPLICATION\_CREDENTIALS=/path/to/your/google\_cloud\_service\_account\_key.json

*(Remember to replace your\_very\_secret\_key\_here\_generate\_a\_long\_random\_one, tax\_analyzer\_user, your\_secure\_password, and tax\_analyzer\_db with your actual values.)*

\# Initialize and apply database migrations  
\# This will create your PostgreSQL tables based on models.py  
flask db init              \# One-time setup  
flask db migrate \-m "Create users, documents, and analysis\_results tables"  
flask db upgrade

**3\. Frontend Setup**

Open a **new terminal window** and navigate to the frontend directory:

cd ../frontend \# Go back to the root project directory, then into frontend

\# Install Node.js dependencies  
npm install

\# Create your .env.development file  
\# This tells your frontend where to find the backend API during development.  
touch .env.development

**frontend/.env.development example (copy and paste this into your .env.development file):**

VITE\_API\_BASE\_URL=http://localhost:5000

### **4\. Running the Application**

Open **two separate terminal windows**.

**Terminal 1 (Backend):**

cd multi-lingual-tax-analyzer/backend  
.\\venv\\Scripts\\activate \# Windows  
\# OR  
source venv/bin/activate \# macOS/Linux

flask run \# Starts the Flask backend API server

The backend will typically run on http://localhost:5000.

**Terminal 2 (Frontend):**

cd multi-lingual-tax-analyzer/frontend  
npm run dev \# Starts the React development server

The frontend will typically open in your browser at http://localhost:5173 (or similar).

---

## **Deployment**

### **Frontend (Netlify)**

Your frontend is configured for easy deployment to Netlify via netlify.toml. Simply connect your GitHub repository to Netlify, and it will automatically build and deploy your React app on every push to the main branch.

### **Backend (Render / PaaS)**

The Flask backend can be deployed to a Platform as a Service (PaaS) like Render. You'll connect your backend repository to Render, configure build and start commands (gunicorn), and securely add your environment variables.

---

## **Contributing**

We welcome contributions\! Please refer to our CONTRIBUTING.md (to be created) for guidelines on how to get involved.

---

