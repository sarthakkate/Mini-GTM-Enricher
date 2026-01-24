# AI Resume Builder - Project Documentation

## 📋 Project Overview

**AI Resume Builder** is a full-stack web application that helps users create, edit, and manage professional resumes with AI-powered assistance. The application leverages Google's Generative AI to provide intelligent resume content suggestions.

---

## 🛠️ Technologies Used

### **Backend**
- **Runtime**: Node.js
- **Framework**: Express.js ^4.19.2
- **Database**: MongoDB (via Mongoose ^8.5.1)
- **Authentication**: JWT (jsonwebtoken ^9.0.2)
- **Security**: 
  - bcrypt ^5.1.1 (password hashing)
  - CORS ^2.8.5 (Cross-Origin Resource Sharing)
- **Utilities**:
  - cookie-parser ^1.4.6
  - dotenv ^16.5.0 (environment variables)

### **Frontend**
- **Framework**: React ^18.3.1
- **Build Tool**: Vite
- **Styling**: 
  - Tailwind CSS
  - PostCSS with Autoprefixer
- **State Management**: Redux Toolkit ^2.2.5
- **UI Components**:
  - Radix UI (alert-dialog, dialog, popover)
  - Custom UI components (button, input, textarea, etc.)
- **Rich Text Editors**:
  - react-draft-wysiwyg ^1.15.0
  - react-simple-wysiwyg ^3.0.3
- **HTTP Client**: axios ^1.7.2
- **Authentication**: Clerk (@clerk/clerk-react ^5.2.5)
- **AI Integration**: Google Generative AI (@google/generative-ai ^0.14.0)
- **Other Libraries**:
  - react-router-dom ^6.24.0 (routing)
  - framer-motion ^11.3.6 (animations)
  - lucide-react ^0.397.0 (icons)
  - react-icons ^5.2.1
  - sonner ^1.5.0 (notifications)
  - next-themes ^0.3.0 (dark mode)

---

## ✨ Unique Features

### 1. **AI-Powered Content Generation**
   - Integrates Google Generative AI (Gemini 1.5 Flash)
   - Intelligent resume content suggestions
   - Context-aware AI chat for resume improvement

### 2. **Multi-Section Resume Management**
   - Personal Details
   - Professional Summary
   - Work Experience
   - Education
   - Skills with ratings
   - Projects

### 3. **Real-time Preview**
   - Live preview component alongside form
   - Theme color customization
   - WYSIWYG editing experience

### 4. **Secure Authentication**
   - JWT-based token authentication
   - Password encryption with bcrypt
   - Cookie-based session management
   - Clerk integration for frontend authentication

### 5. **Full CRUD Operations**
   - Create multiple resumes
   - Read and view resumes
   - Update resume content
   - Delete resumes

### 6. **Rich Text Editing**
   - Multiple WYSIWYG editors
   - Formatted content support
   - Summary sections with rich formatting

---

## 🏗️ System Architecture

### **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Frontend)                     │
│  React + Redux + Vite                                        │
│  ├─ Authentication (Clerk)                                  │
│  ├─ Resume Management (Dashboard, Edit, View)               │
│  ├─ Form Components (Personal, Experience, Education, etc.) │
│  ├─ Preview Components                                       │
│  └─ AI Integration (Gemini)                                 │
└─────────────────────────────────────────────────────────────┘
                            ↕ (HTTP/REST)
┌─────────────────────────────────────────────────────────────┐
│                     SERVER (Backend)                         │
│  Express.js + Node.js                                        │
│  ├─ Authentication Routes (/api/users)                      │
│  ├─ Resume Routes (/api/resumes) [JWT Protected]            │
│  ├─ Controllers (Business Logic)                             │
│  ├─ Middleware (Auth, CORS)                                 │
│  └─ Database Models (User, Resume, etc.)                    │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              MongoDB Database                                │
│  ├─ Users Collection                                         │
│  └─ Resumes Collection (with nested data)                   │
└─────────────────────────────────────────────────────────────┘
```

### **Data Flow**

1. **Authentication Flow**:
   - User registers/logs in via frontend
   - Server validates credentials and hashes password with bcrypt
   - JWT token generated and sent as secure cookie
   - Frontend stores and sends token with subsequent requests

2. **Resume Operations Flow**:
   - User creates/edits resume in React components
   - Redux state manages local resume data
   - Frontend sends to backend API via Axios
   - Backend validates user with JWT middleware
   - MongoDB stores/updates resume data
   - Response sent back to frontend

3. **AI Integration Flow**:
   - User requests AI suggestions
   - Frontend sends context to Gemini API
   - AI generates suggestions in JSON format
   - Results displayed in UI in real-time

---

## 🔐 JWT Authentication & Middleware

### **JWT Middleware Implementation**

**File**: `Backend/src/middleware/auth.js`

```javascript
import User from "../models/user.model.js";
import jwt from "jsonwebtoken";
import { ApiResponse } from "../utils/ApiResponse.js";
import { ApiError } from "../utils/ApiError.js";

const isUserAvailable = async (req, res, next) => {
  let { token } = req.cookies;

  // Check if token exists
  if (!token) {
    return res.status(404).json(new ApiError(404, "User not authenticated."));
  }

  try {
    // Verify JWT token using secret key
    const decodedToken = await jwt.verify(token, process.env.JWT_SECRET_KEY);
    
    // Fetch user from database
    const user = await User.findById(decodedToken.id);

    if (!user) {
      return res.status(404).json(new ApiError(404, "User not found."));
    }

    // Attach user to request object
    req.user = user;
    next();
  } catch (err) {
    console.error("Error verifying token:", err);
    return res.status(500).json(new ApiError(500, "Internal Server Error.", [], err.stack));
  }
};

export { isUserAvailable };
```

### **JWT Workflow**:

1. **Token Generation** (Login):
   - User successfully authenticates with email/password
   - Server creates JWT with user ID as payload
   - Token structure: `{ id: userId, iat: timestamp, exp: expiration }`
   - Token sent to client via secure HTTP-only cookie

2. **Token Verification** (Middleware):
   - Client sends request with token in cookies
   - `isUserAvailable` middleware intercepts request
   - Token verified against `JWT_SECRET_KEY` environment variable
   - User retrieved from database by decoded ID
   - If valid: `req.user` populated and `next()` called
   - If invalid: 404 or 500 error response returned

3. **Protected Routes**:
   - All resume CRUD routes require JWT middleware
   - Only authenticated users can create/read/update/delete resumes
   - Prevents unauthorized resume access and manipulation

### **Security Features**:
- ✅ Password hashing with bcrypt (10 salt rounds)
- ✅ JWT token verification with secret key
- ✅ Secure HTTP-only cookie storage
- ✅ CORS origin validation
- ✅ Comprehensive error handling
- ✅ User validation on each request

---

## 🚀 Getting Started & Run Commands

### **Backend Setup**

```bash
# Navigate to backend directory
cd Backend

# Install all dependencies
npm install

# Create .env file in Backend directory with:
PORT=5000
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
JWT_SECRET_KEY=your_super_secret_key_change_in_production
ALLOWED_SITE=http://localhost:3000

# Development mode (with auto-reload using nodemon)
npm run dev

# Production mode
npm start
```

### **Frontend Setup**

```bash
# Navigate to frontend directory
cd Frontend

# Install all dependencies
npm install

# Create .env file in Frontend directory with:
VITE_BASE_URL=http://localhost:5000/
VITE_GOOGLE_GENERATIVE_AI_KEY=your_gemini_api_key_from_makersuite
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key

# Development mode (Vite dev server)
npm run dev

# Build for production
npm build

# Preview production build locally
npm run preview
```

### **Run Full Stack Locally**

```bash
# Terminal 1 - Start Backend
cd Backend
npm install
npm run dev
# Backend runs on http://localhost:5000

# Terminal 2 - Start Frontend
cd Frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173 (Vite default)
```

---

## 📁 Project Structure

### **Backend Structure**
```
Backend/
├── src/
│   ├── app.js                    # Express app & middleware setup
│   ├── index.js                  # Server entry point
│   ├── controller/
│   │   ├── user.controller.js    # Auth & user logic (register, login, logout)
│   │   └── resume.controller.js  # Resume CRUD operations
│   ├── models/
│   │   ├── user.model.js         # User schema with bcrypt hashing
│   │   ├── resume.model.js       # Resume schema with nested data
│   │   ├── education.model.js    # Education sub-schema
│   │   ├── experience.model.js   # Experience sub-schema
│   │   ├── project.model.js      # Project sub-schema
│   │   └── skill.model.js        # Skill sub-schema
│   ├── routes/
│   │   ├── user.routes.js        # User endpoints (auth)
│   │   └── resume.routes.js      # Resume endpoints (CRUD)
│   ├── middleware/
│   │   └── auth.js               # JWT verification middleware
│   ├── db/
│   │   └── index.js              # MongoDB connection
│   └── utils/
│       ├── ApiError.js           # Error response formatter
│       └── ApiResponse.js        # Success response formatter
└── package.json
```

### **Frontend Structure**
```
Frontend/
├── src/
│   ├── App.jsx                   # Root app component with routing
│   ├── main.jsx                  # Vite entry point
│   ├── components/
│   │   ├── custom/               # Custom components
│   │   │   ├── Header.jsx        # Navigation header
│   │   │   ├── RichTextEditor.jsx
│   │   │   └── SimpeRichTextEditor.jsx
│   │   └── ui/                   # Radix UI components
│   ├── pages/
│   │   ├── auth/                 # Authentication pages
│   │   │   ├── Sign-In/
│   │   │   └── customAuth/
│   │   ├── dashboard/            # Resume management
│   │   │   ├── Dashboard.jsx
│   │   │   ├── components/
│   │   │   ├── edit-resume/
│   │   │   └── view-resume/
│   │   ├── home/                 # Home page
│   │   └── index.js
│   ├── features/                 # Redux slices
│   │   ├── resume/
│   │   └── user/
│   ├── Services/                 # API & AI integration
│   │   ├── GlobalApi.js          # API calls with Axios
│   │   ├── AiModel.js            # Gemini AI integration
│   │   ├── login.js              # Login service
│   │   └── resumeAPI.js          # Resume API calls
│   ├── store/                    # Redux store configuration
│   ├── config/                   # Configuration files
│   ├── lib/                      # Utility functions
│   └── assets/                   # Static assets
├── vite.config.js
├── tailwind.config.js
└── package.json
```

---

## 🔄 API Endpoints

### **User Routes** - `/api/users`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | ❌ | Register new user |
| POST | `/login` | ❌ | Login user & get JWT token |
| GET | `/start` | ✅ JWT | Get logged-in user data |
| POST | `/logout` | ✅ JWT | Logout user |

### **Resume Routes** - `/api/resumes`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | ❌ | Health check |
| POST | `/createResume` | ✅ JWT | Create new resume |
| GET | `/getAllResume` | ✅ JWT | Get all user resumes |
| GET | `/getResume` | ✅ JWT | Get specific resume by ID |
| PUT | `/updateResume` | ✅ JWT | Update resume content |
| DELETE | `/removeResume` | ✅ JWT | Delete resume |

---

## 📊 Database Schema (MongoDB)

### **User Collection**
```javascript
{
  _id: ObjectId,
  fullName: String,
  email: String (unique),
  password: String (hashed with bcrypt),
  createdAt: Date,
  updatedAt: Date
}
```

### **Resume Collection**
```javascript
{
  _id: ObjectId,
  firstName: String,
  lastName: String,
  email: String,
  jobTitle: String,
  phone: String,
  address: String,
  title: String (required),
  summary: String (rich text),
  user: ObjectId (reference to User),
  experience: [{
    title: String,
    companyName: String,
    city: String,
    state: String,
    startDate: String,
    endDate: String,
    currentlyWorking: String,
    workSummary: String
  }],
  education: [{
    universityName: String,
    startDate: String,
    endDate: String,
    degree: String,
    major: String,
    description: String
  }],
  skills: [{
    name: String,
    rating: Number
  }],
  projects: [{
    projectName: String,
    techStack: String,
    projectSummary: String
  }],
  themeColor: String (required),
  createdAt: Date,
  updatedAt: Date
}
```

---

## 🎨 Key Implementation Details

### **1. Password Security**
- Uses bcrypt with 10 salt rounds
- Pre-save MongoDB middleware hashes passwords automatically
- `comparePassword()` method for login validation
- Passwords never stored in plain text

### **2. Resume Versioning**
- Users can create multiple resumes
- Each resume has independent theme color
- Separate edit and view-only modes
- Resume ownership enforced via user reference

### **3. Real-time Editing**
- Live preview component updates as user types
- WYSIWYG editors for rich content
- Redux state for local state management
- Theme color applied instantly

### **4. AI Integration**
- Uses Google Gemini 1.5 Flash model
- JSON-formatted AI responses
- Context-aware resume content suggestions
- Real-time streaming of AI suggestions

### **5. State Management**
- Redux Toolkit for global state
- Persistent user authentication
- Resume data caching
- Automatic state synchronization

---

## 🔧 Environment Variables

### **Backend (.env)**
```
# Server Configuration
PORT=5000

# Database
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/resume_db

# JWT Configuration
JWT_SECRET_KEY=your_super_secret_jwt_key_min_32_chars

# CORS Configuration
ALLOWED_SITE=http://localhost:3000
```

### **Frontend (.env)**
```
# API Configuration
VITE_BASE_URL=http://localhost:5000/

# AI Configuration
VITE_GOOGLE_GENERATIVE_AI_KEY=your_gemini_api_key_from_ai.google.dev

# Authentication
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
```

---

## 📚 API Usage Examples

### **Register User**
```bash
POST http://localhost:5000/api/users/register
Content-Type: application/json

{
  "fullName": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

### **Login User**
```bash
POST http://localhost:5000/api/users/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePassword123"
}

# Response includes JWT token in cookies
```

### **Create Resume** (Requires JWT)
```bash
POST http://localhost:5000/api/resumes/createResume
Content-Type: application/json
Cookie: token=your_jwt_token

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "title": "My Professional Resume",
  "jobTitle": "Software Engineer",
  "themeColor": "#FF5733"
}
```

### **Get All Resumes** (Requires JWT)
```bash
GET http://localhost:5000/api/resumes/getAllResume
Cookie: token=your_jwt_token
```

---

## 🎯 Features Summary

| Feature | Status | Details |
|---------|--------|---------|
| User Authentication | ✅ | JWT + bcrypt |
| Resume CRUD | ✅ | Full create, read, update, delete |
| AI Suggestions | ✅ | Gemini API integration |
| Real-time Preview | ✅ | Live resume preview |
| Rich Text Editing | ✅ | WYSIWYG editors |
| Multi-theme Support | ✅ | Customizable theme colors |
| Responsive Design | ✅ | Mobile-friendly UI |
| Redux State Management | ✅ | Global state management |

---

## 💡 Future Enhancements

- [ ] Resume templates gallery
- [ ] PDF export functionality
- [ ] Social media links integration
- [ ] Resume analytics (view count, downloads)
- [ ] Collaboration features
- [ ] Resume ATS optimization suggestions
- [ ] Multi-language support
- [ ] Dark mode theme

---

## 📄 License

This project is open source and available under the ISC License.

---

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For support, please open an issue in the repository.