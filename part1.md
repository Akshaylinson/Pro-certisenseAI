<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 200px 0 20px 0;">

<div style="font-size: 24px; margin-bottom: 12px;"><strong>Amazon Q</strong></div>
<div style="background: rgba(128, 128, 128, 0.15); border: 1px solid rgba(128, 128, 128, 0.25); border-radius: 8px; padding: 8px; margin: 4px 0; text-align: center;">
<div style="font-size: 14px; margin-bottom: 4px;"><strong>Did you know?</strong></div>
<div>Compact your conversation with /compact</div>
</div>

Select code & ask me to explain, debug or optimize it, or type `/` for quick actions

</div>

---

i need to know whether i can host this paticular project into vercel, so they are asking for some of the input filed- New Project
importing from GitHub

Akshaylinson/Pro-certisenseAI
main
Choose where you want to create the project and give it a name.

Vercel Team

akshay&#39;s projects
Hobby
Slash Divider
Project Name
pro-certisense-ai
Application Preset
Framework logo
Other
Root Directory
./
Build Command
`npm run vercel-build` or `npm run build`
Output Directory
`public` if it exists, or `.`
Install Command
`yarn install`, `pnpm install`, `npm install`, or `bun install`
Key
EXAMPLE_NAME
Value
I9JU23NF394R6HH
or paste the .env contents above. Learn more
//refer the project and say whether we can host it in vercel

---

Let me check the project structure first.

---


Here's the honest breakdown of whether you can host this on Vercel:

---

## Short Answer: Partially — Frontend YES, Backend NO (not directly)

---

### Frontend (React/Vite) → ✅ Works on Vercel

Your `frontend/web` is a standard Vite + React app. Vercel handles this perfectly.

Vercel settings for the frontend:
- Root Directory: `frontend/web`
- Framework Preset: `Vite`
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

---

### Backend (FastAPI/Python) → ❌ Not supported on Vercel (Hobby plan)

Your backend is a full FastAPI server with:
- SQLite database (`certisense.db`) with file writes
- File uploads stored locally (`backend/uploads/certificates/`)
- A 3B parameter LLM model file (`qwen2.5-3b-instruct-q4_k_m.gguf` — likely 2–4GB)
- Long-running processes (AI inference, blockchain calls)

Vercel's serverless functions have:
- 50MB deployment size limit (your model alone exceeds this)
- No persistent filesystem
- 10s execution timeout on Hobby (your AI inference will exceed this)
- No support for SQLite file-based databases

---

### What you should actually do

| Component | Recommended Platform |
|-----------|---------------------|
| Frontend (React) | Vercel ✅ |
| Backend (FastAPI) | Railway / Render / AWS EC2 |
| Database (SQLite) | Migrate to PostgreSQL (Railway/Supabase) |
| File uploads | AWS S3 or Cloudflare R2 |
| AI model | Keep on backend server (too large for serverless) |

---

### For Vercel specifically — the env variable they're asking for

The `EXAMPLE_NAME` / value field is just for your environment variables. You'd set things like:

```
VITE_API_URL=https://your-backend-url.railway.app
```

in the Vercel env vars so your frontend knows where the backend lives.

---

**Bottom line**: Deploy only the frontend to Vercel, and host the backend on a platform that supports persistent processes like Railway, Render, or AWS. The AI model file alone makes full Vercel deployment impossible.

---

so which hosting do u prefer for this project

---


Based on your project's specific needs (FastAPI + SQLite + file uploads + AI model + blockchain), here's what I'd recommend:

---

## Best Stack for CertiSense AI

### Frontend → Vercel ✅ (keep your current plan)
- Free, fast, auto-deploys from GitHub
- Perfect for Vite/React

---

### Backend → Railway 🏆 (best fit)

Why Railway over others:
- Supports Python/FastAPI natively
- Persistent disk (your uploads + SQLite work as-is initially)
- No cold starts (unlike Render free tier which sleeps after 15min)
- Simple GitHub auto-deploy
- ~$5/month on Starter plan
- Environment variables UI is clean

---

### The problem components and solutions

| Problem | Quick Fix |
|---------|-----------|
| SQLite on server | Fine for now on Railway, migrate to PostgreSQL later (Railway provides it free) |
| `uploads/certificates/` | Move to **Cloudflare R2** (free 10GB) or **AWS S3** |
| `qwen2.5-3b-instruct-q4_k_m.gguf` (2-4GB model) | This is the biggest issue — Railway's free tier won't fit it. You need at least the $20/month plan or swap to an API-based AI (OpenAI, Groq, etc.) |
| `certisense.db` | Keep on Railway volume or migrate to Railway PostgreSQL |

---

### The AI Model is your real bottleneck

That `.gguf` model is heavy. Two options:

- Option A — Keep it: Use Railway's $20/month plan with a volume mount, works but costly
- Option B — Replace it: Swap to **Groq API** (free tier, very fast, llama3 models) — minimal code change in your `ai_service.py`

Option B is what I'd recommend for a hosted demo/portfolio project.

---

### Recommended Final Setup

```
Vercel          → frontend (free)
Railway         → FastAPI backend (~$5/month)
Railway         → PostgreSQL database (free addon)
Cloudflare R2   → certificate file storage (free 10GB)
Groq API        → replace local .gguf model (free tier)
```

This gets your full app live for roughly **$5/month** total.

Want me to help set up any of these — like the Railway config files, migrating SQLite to PostgreSQL, or swapping the AI model to Groq?

---

can we host the enitr porjoect into in one particular hosting server

---


Yes! For hosting the **entire project** (frontend + backend) on a single platform, here are your best options:

---

## Single-Server Hosting Options

### 🏆 Option 1 — Railway (Most Recommended)

Railway can host everything in one project:

```
Railway Project
├── Service 1: Frontend (React/Vite) 
├── Service 2: Backend (FastAPI)
├── Service 3: PostgreSQL Database
└── Volume: File uploads
```

- Each service auto-deploys from same GitHub repo
- Internal networking between services (fast)
- ~$5-10/month total
- BUT: still the AI model size problem

---

### Option 2 — Render

Same concept as Railway:
```
Render
├── Static Site: Frontend
├── Web Service: Backend (FastAPI)
└── PostgreSQL: Database
```
- Free tier available but **sleeps after 15min** inactivity
- Paid starts at $7/month per service

---

### Option 3 — AWS EC2 / VPS (Full Control) 🔧

Single Ubuntu server running everything:
```
EC2 / DigitalOcean / Contabo VPS
├── Nginx (reverse proxy)
├── React build (served as static files)
├── FastAPI (uvicorn)
├── SQLite or PostgreSQL
└── AI model (stored on disk)
```
- **Only option that can handle your .gguf AI model** without extra cost
- DigitalOcean Droplet: ~$12/month (2GB RAM) — too small for model
- Contabo VPS: ~$7/month (8GB RAM, 200GB disk) ✅ fits everything
- Requires manual setup (Nginx, systemd, etc.)

---

## My Honest Recommendation

| Platform | Handles AI Model | Price | Ease |
|----------|-----------------|-------|------|
| Railway | ⚠️ Costly | $20+/month | Easy |
| Render | ⚠️ Costly | $20+/month | Easy |
| **Contabo VPS** | ✅ Yes | **~$7/month** | Medium |
| AWS EC2 t3.medium | ✅ Yes | ~$30/month | Hard |

---

### 🎯 Best Single-Server Choice: Contabo VPS

**Specs for ~$7/month:**
- 4 vCPU, 8GB RAM, 200GB SSD
- Fits your `.gguf` model, SQLite, uploads, everything
- Run Nginx + FastAPI + React build on one machine

**Setup would be:**
```
Nginx
 ├── / → serves React build (static)
 └── /api → proxies to FastAPI (port 8000)
```

---

Want me to create the Nginx config, systemd service files, and a deployment script to get this running on a single VPS?

---

so if we convert all the containers as single container, instead currently we have frontend contianer, backed contianer seperatley, so if we can build the entire project in as one docker command is it possbile to run the project

---

Yes! Absolutely possible. Let me check your existing Docker setup first.

---

Yes, 100% possible! The idea is:

1. Build React as static files
2. Let FastAPI serve those static files
3. Single container, single port, one Docker command

Here's the plan:

- Create a single `Dockerfile` at the root
- React builds to `dist/` → copied into FastAPI's static folder
- Nginx or FastAPI serves everything on port `80`
- One command: `docker build` + `docker run`

Let me build this:

---

Now I have everything I need. Here's the plan:

- Single `Dockerfile` at root using **multi-stage build**:
  - Stage 1: Build React → produces `dist/`
  - Stage 2: Python + FastAPI, copies `dist/` into it, serves static files + API on port `8000`
- FastAPI already has `StaticFiles` support, just need to mount the React build
- One command to build and run everything

I need to make 2 changes:
1. Create root `Dockerfile` (multi-stage)
2. Update `certisense_main.py` to serve React static files

---

Multi-stage Dockerfile: Stage 1 builds React, Stage 2 runs FastAPI and serves the React build as static files.

---

Now update `certisense_main.py` to serve the React build and handle client-side routing:

---

Now update the frontend's API URL to use relative paths when deployed:

---

Now let me check how the frontend sets the API base URL:

---

Check how the frontend constructs API URLs

---

shell

---

Find API URL references in frontend source

---

shell

---

Find hardcoded localhost:8000 references in frontend

---

shell

---

There are hardcoded `localhost:8000` URLs across many files. The cleanest fix is a single shared API config file that all components import from:

---

Central API config — uses empty string (same origin) in production, localhost:8000 in dev.

---

Now create a `.env` for local dev and `.env.production` for the Docker build:

---

Local dev env — points to localhost backend

---

Production env — empty string means same-origin (FastAPI serves both)

---

Now replace all hardcoded `localhost:8000` in the components. Let me do them all at once:

---

Now I'll replace all `localhost:8000` references across all components at once:

---

Now fix the remaining files with hardcoded URLs:

---

Now update the CORS in the backend to also allow same-origin (no origin header) requests from the container:

---


All done! Here's a summary of everything that was done and how to use it:

---

## What was changed

| File | Change |
|------|--------|
| `Dockerfile` (new, root) | Multi-stage: builds React → copies into FastAPI |
| `frontend/web/src/api.js` (new) | Central API base URL config |
| `frontend/web/.env` | `VITE_API_URL=http://localhost:8000` for local dev |
| `frontend/web/.env.production` | `VITE_API_URL=` (empty = same origin) for Docker |
| `frontend/web/vite.config.js` | Added dev proxy + build output dir |
| `backend/certisense_main.py` | Serves React `static/` folder + catch-all SPA route |
| All 7 frontend components | Replaced hardcoded `localhost:8000` with `API_URL` import |

---

## Single Docker commands

```bash
# Build
docker build -t certisense-ai .

# Run
docker run -p 8000:8000 -v ./data:/app/data certisense-ai
```

Then open `http://localhost:8000` — frontend and backend both served from one container on one port.

---

## How it works inside the container

```
Port 8000
  ├── /auth, /admin, /institute, /student, /verifier  → FastAPI
  ├── /uploads  → static file serving (certificates)
  ├── /assets   → React JS/CSS bundles
  └── /*        → serves React index.html (SPA routing)
```

---

PS E:\AI+Blockchain\Pro-1-cert-verifier&gt; docker build -t certisense-ai
ERROR: docker: &#39;docker buildx build&#39; requires 1 argument

Usage:  docker buildx build [OPTIONS] PATH | URL | -

Run &#39;docker buildx build --help&#39; for more information
PS E:\AI+Blockchain\Pro-1-cert-verifier&gt; //these were the errors in the console while building

---


You're missing the `.` (build context path) at the end of the command. Run:

```bash
docker build -t certisense-ai .
```

The `.` tells Docker to use the current directory as the build context. That's all — your command was missing it.

---

1 vCPU Core
4 GB RAM
50 GB NVMe Disk Space
4 TB Bandwidth
1 Snapshot
Weekly Backups
Dedicated IP Address
Full Root Access
AI Assistant
Malware Scanner// i already have a server, in hostinger ,s o i need to know whether i can use this server for this certisenseai project

---


Yes! That Hostinger VPS is perfectly capable of running your CertiSense AI project. Let me break it down:

---

## Compatibility Check

| Requirement | Your Server | Status |
|-------------|-------------|--------|
| Docker support | Full root access ✅ | ✅ Can install Docker |
| RAM for FastAPI + React | 4GB | ✅ More than enough |
| AI model (qwen 3B .gguf ~2GB) | 4GB RAM | ⚠️ Tight but workable |
| Storage for certificates + DB | 50GB NVMe | ✅ Plenty |
| Dedicated IP | Yes | ✅ Direct access |

---

## The Only Concern — AI Model RAM

Your `.gguf` model needs ~2-2.5GB RAM to load. With 4GB total:
- OS uses ~300-500MB
- FastAPI + React uses ~200-300MB
- Model uses ~2-2.5GB
- Leaves ~700MB-1GB free — **tight but should work**

If it crashes due to RAM, the fix is to swap the model to Groq API (free) instead of running it locally.

---

## Deployment Steps on Hostinger VPS

### 1. SSH into your server
```bash
ssh root@your-server-ip
```

### 2. Install Docker
```bash
curl -fsSL https://get.docker.com | sh
```

### 3. Clone your repo
```bash
git clone https://github.com/Akshaylinson/Pro-certisenseAI.git
cd Pro-certisenseAI
```

### 4. Build and run
```bash
docker build -t certisense-ai .
docker run -d \
  --name certisense \
  -p 80:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/backend/uploads:/app/uploads \
  --restart unless-stopped \
  certisense-ai
```

### 5. Access your app
```
http://your-dedicated-ip
```

---

## Optional — Add a Domain + HTTPS

If you have a domain pointed to your server IP, install Nginx + Certbot:

```bash
apt install nginx certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com
```

---

## Summary

Your Hostinger VPS is a solid fit for this project. The single Docker container approach we set up earlier works perfectly here — one `docker build`, one `docker run`, everything live on port 80. The weekly backups and snapshot also protect your SQLite database and uploaded certificates.

Want me to help with anything specific like setting up the domain, HTTPS, or handling the AI model RAM issue?

---

so if we convert all the containers as single container, instead currently we have frontend contianer, backed contianer seperatley, so if we can build the entire project in as one docker command is it possbile to run the project

////we have undo this update as the build getting error after the update so we going with the run build commands// oi ned to know whtner we can deoply this project in the considtion with 2 bulid commands for frotnend and  backend// is that possible

---

Yes! Absolutely possible to deploy with 2 separate containers on the same Hostinger VPS. Let me check your current docker-compose setup:

---

Yes, 100% deployable as-is with the existing 2-container setup. You just need **one command** — `docker compose up` — which handles both containers together.

---

## On Your Hostinger VPS

### 1. SSH in
```bash
ssh root@your-server-ip
```

### 2. Install Docker + Compose
```bash
curl -fsSL https://get.docker.com | sh
apt install docker-compose-plugin -y
```

### 3. Clone your repo
```bash
git clone https://github.com/Akshaylinson/Pro-certisenseAI.git
cd Pro-certisenseAI
```

### 4. One command to build + run everything
```bash
docker compose up -d --build
```

This automatically:
- Builds backend container
- Builds frontend container
- Creates the shared network between them
- Starts both containers

---

## Access Your App

| Service | URL |
|---------|-----|
| Frontend | `http://your-server-ip:5173` |
| Backend API | `http://your-server-ip:8000` |

---

## One Problem to Fix First

Your frontend `Dockerfile` runs `npm run dev` which is the **development server** — not suitable for production. You need to update it to build and serve static files:

---

Now create the nginx config:

---

Nginx config to serve React SPA and proxy API calls to backend container.

---

Now update `docker-compose.yml` to use the correct ports:

---


---

## Final Setup

Before deploying, replace `your-server-ip` in `docker-compose.yml` with your actual Hostinger VPS IP:

```yaml
- VITE_API_URL=http://YOUR_ACTUAL_IP:8000
```

Then on the server:

```bash
# Build and start both containers
docker compose up -d --build

# Check both are running
docker compose ps

# View logs if needed
docker compose logs -f
```

---

## Result

| Service | URL |
|---------|-----|
| Frontend | `http://your-server-ip` (port 80) |
| Backend API | `http://your-server-ip:8000` |

Two containers, one command, fully deployed on your Hostinger VPS. ✅

---

[+] up 3/4
 ✔ Image pro-1-cert-verifier-frontend       Built                  72.6s
 ✔ Image pro-1-cert-verifier-backend        Built                  72.6s
 - Container pro-1-cert-verifier-backend-1  Starting               1.3s 
 ✔ Container pro-1-cert-verifier-frontend-1 Recreated              0.2s
Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint pro-1-cert-verifier-backend-1 (b5fe5c35a12099a5e1bb7f41ed55286f6d32ed2998e798effec3f5ea577e0ec4): Bind for 0.0.0.0:8000 failed: port is already allocated        
PS E:\AI+Blockchain\Pro-1-cert-verifier&gt; //still getting the error in the build

---

Port 8000 is already in use on your machine. Something else is already running on that port (probably a previous container or your local backend).

Fix it with these steps:

---

Check what containers are currently running and using port 8000

---

shell

---

Found it — `certisense-test` container is already running on port 8000. Stop it first:

---

Stop and remove the old certisense-test container that is occupying port 8000

---

shell

---

Now run compose again:

---

Start both containers now that port 8000 is free

---

shell

---

Both containers are running! Let's verify:

---

Confirm both containers are up and check their ports

---

shell

---


Both containers are up and running! ✅

| Container | Status | URL |
|-----------|--------|-----|
| Backend | ✅ Up | `http://localhost:8000` |
| Frontend | ✅ Up | `http://localhost:80` |

The issue was your old `certisense-test` container from earlier testing was still holding port 8000.

**Open your browser:**
- Frontend → `http://localhost`
- Backend API → `http://localhost:8000/health`

Also, you can safely ignore the `version is obsolete` warning — it's just a cosmetic warning from newer Docker versions, not an error. You can remove the `version: '3.8'` line from `docker-compose.yml` to clean it up.

---

generate a absstract for this project

---


Here's a professional abstract for CertiSense AI:

---

**CertiSense AI: A Blockchain-Powered Certificate Verification System with AI Validation**

In the modern digital landscape, the authenticity of academic and professional certificates has become increasingly difficult to verify, leading to widespread credential fraud. CertiSense AI v3.0 is a full-stack web application designed to address this challenge through the integration of blockchain technology, artificial intelligence, and a role-based access control system.

The system implements a hierarchical entity model comprising four distinct roles — Administrator, Institute, Student, and Verifier — each with dedicated dashboards and controlled access to system functionalities. Educational institutes can register on the platform, enroll students, and issue certificates that are cryptographically hashed using SHA-256 and recorded on an immutable blockchain ledger. Each certificate is assigned a unique identifier and chain hash, ensuring tamper-proof storage and traceability throughout its lifecycle.

The AI validation layer performs content analysis on uploaded certificate files, computing confidence scores and generating intelligent explanations for verification outcomes. Verifiers, such as employers or third-party organizations, can upload certificates for instant authenticity checks, with results cross-referenced against the blockchain registry. The system also incorporates role-specific AI chatbot assistants powered by a locally hosted large language model, enabling natural language queries over live database records.

Built with React and Tailwind CSS on the frontend and FastAPI with SQLAlchemy on the backend, the application is fully containerized using Docker, enabling seamless deployment on any cloud or VPS infrastructure. Additional features include real-time analytics dashboards, AI-generated visual reports, certificate download support, a verifier feedback mechanism, and JWT-based authentication across all roles.

CertiSense AI demonstrates a practical and scalable approach to digital credential management, combining the immutability of blockchain with the intelligence of modern AI to deliver a trustworthy, transparent, and efficient certificate verification ecosystem.

---

**Keywords:** Blockchain, Certificate Verification, Artificial Intelligence, Role-Based Access Control, FastAPI, React, SHA-256, JWT Authentication, Docker, Credential Fraud Prevention

---

generate intorduction for this project

---


Here's a detailed introduction for CertiSense AI:

---

**1. Introduction**

In an era defined by rapid digitalization and global connectivity, the verification of academic qualifications and professional certifications has emerged as a critical challenge for institutions, employers, and individuals alike. The proliferation of fraudulent credentials has undermined trust in traditional paper-based and digitally issued certificates, creating significant risks for organizations that rely on the authenticity of such documents during hiring, admissions, and compliance processes. According to various industry reports, credential fraud is a growing global concern, with thousands of forged certificates circulating across educational and professional sectors each year.

Conventional certificate verification methods are largely manual, time-consuming, and prone to human error. They typically involve contacting the issuing institution directly, cross-referencing physical documents, or relying on centralized databases that are vulnerable to tampering, data breaches, and single points of failure. These limitations highlight the urgent need for a more robust, transparent, and automated solution that can verify the authenticity of certificates instantly and reliably.

Blockchain technology has emerged as a transformative solution to the problem of data integrity and trust. By storing records in a decentralized, cryptographically secured, and immutable ledger, blockchain eliminates the possibility of unauthorized modification or deletion of data. Each transaction recorded on the blockchain is permanent and verifiable by any authorized party, making it an ideal foundation for a certificate verification system. When combined with Artificial Intelligence, which can analyze document content, detect anomalies, and generate confidence-based assessments, the resulting system becomes significantly more intelligent and capable than any traditional approach.

CertiSense AI v3.0 is developed in response to these challenges. It is a comprehensive, role-based blockchain certificate verification platform that brings together the immutability of blockchain, the analytical power of artificial intelligence, and the accessibility of modern web technologies. The system is designed to serve four key stakeholders in the certificate lifecycle — Administrators who oversee the entire platform, Institutes that issue certificates to students, Students who hold and track their credentials, and Verifiers such as employers or third-party organizations who need to confirm the authenticity of submitted certificates.

The platform enables educational institutes to register on the system, add students, and issue certificates that are processed through an AI validation layer before being hashed using the SHA-256 cryptographic algorithm and recorded on the blockchain. Each certificate receives a unique identifier and a chain hash that links it permanently to the issuing institution and the student. Verifiers can upload any certificate file to the platform, which instantly computes its hash and cross-references it against the blockchain registry, returning a detailed verification result along with an AI-generated confidence score and explanation.

Beyond core verification functionality, CertiSense AI incorporates a suite of advanced features including role-specific AI chatbot assistants that allow users to query live system data using natural language, automated visual report generation with AI-powered insights, real-time analytics dashboards for all roles, certificate download capabilities, and a structured feedback mechanism for verifiers to report suspicious documents.

The system is built using a modern technology stack — React with Tailwind CSS for the frontend, FastAPI with SQLAlchemy for the backend, SQLite for persistent data storage, and Docker for containerized deployment. This architecture ensures that the platform is scalable, maintainable, and deployable across a wide range of infrastructure environments, from local development machines to cloud-based virtual private servers.

The primary objectives of CertiSense AI are to eliminate certificate fraud through blockchain-backed immutability, reduce the time and effort required for credential verification, provide a transparent and auditable record of all verification activities, and empower all stakeholders with intelligent tools to manage and interact with the certificate ecosystem efficiently.

The remainder of this paper is organized as follows: Section 2 reviews related work in the areas of blockchain-based credential systems and AI-driven document verification. Section 3 describes the system architecture and design. Section 4 details the implementation of key modules. Section 5 presents the results and system evaluation. Section 6 concludes the paper with a discussion of future enhancements.

---

---

generate OBJECTIVES for this project

---


Here are the objectives for CertiSense AI:

---

**2. Objectives**

The primary aim of CertiSense AI is to design and implement a secure, intelligent, and scalable certificate verification platform that addresses the limitations of conventional credential management systems. The following objectives define the scope and direction of the project:

---

**2.1 Primary Objectives**

**1. To develop a blockchain-based certificate registry that ensures tamper-proof storage of credentials**
The system aims to leverage blockchain technology to store cryptographic hashes of issued certificates in an immutable ledger. By recording each certificate's SHA-256 hash and chain hash on the blockchain, the platform guarantees that no certificate can be altered, duplicated, or deleted without detection, thereby establishing a permanent and trustworthy record of all issued credentials.

**2. To implement an AI-powered validation layer for intelligent certificate authentication**
The project seeks to integrate an artificial intelligence module capable of analyzing the content of uploaded certificate files, computing confidence scores, detecting anomalies, and generating human-readable explanations for verification outcomes. This AI layer adds an additional dimension of intelligence beyond simple hash matching, enabling the system to assess document quality and authenticity with greater accuracy.

**3. To design a hierarchical role-based access control system for multi-stakeholder management**
The platform is intended to serve four distinct user roles — Administrator, Institute, Student, and Verifier — each with clearly defined permissions, dedicated dashboards, and controlled access to system functionalities. This objective ensures that sensitive operations such as certificate issuance and student registration are restricted to authorized entities, while verification remains accessible to approved third parties.

**4. To automate the end-to-end certificate lifecycle from issuance to verification**
The system aims to streamline the entire certificate lifecycle, beginning from institute registration and student enrollment, through certificate issuance and blockchain recording, to third-party verification and feedback submission. Automation of these processes reduces manual intervention, minimizes human error, and accelerates the overall verification workflow.

---

**2.2 Secondary Objectives**

**5. To provide real-time analytics and AI-generated reports for system stakeholders**
The project aims to equip administrators, institutes, and verifiers with comprehensive dashboards that display real-time statistics, performance metrics, and activity trends. Additionally, the system will generate AI-powered visual reports with intelligent insights to support data-driven decision-making across all roles.

**6. To integrate role-specific AI chatbot assistants for natural language interaction**
The platform seeks to deploy intelligent chatbot assistants for each user role, enabling stakeholders to query live database records, retrieve statistics, and obtain system information using natural language. This objective enhances user experience and accessibility by reducing the need for manual navigation through complex interfaces.

**7. To ensure secure authentication and authorization across all system roles**
The project aims to implement JSON Web Token based authentication for all user roles, with password hashing, token expiration, and role-based endpoint protection. This objective ensures that all API endpoints are secured against unauthorized access and that user sessions are managed safely throughout the platform.

**8. To enable transparent verification history and audit trails for all certificates**
The system intends to maintain a complete and accessible record of every verification event associated with each certificate, including the verifier's identity, timestamp, result, and confidence score. This audit trail promotes accountability and transparency across the verification ecosystem.

**9. To build a fully containerized and deployment-ready application**
The project aims to package the entire application — frontend, backend, database, and file storage — into Docker containers that can be deployed consistently across any infrastructure environment. This objective ensures that the system is portable, scalable, and easy to maintain in both development and production settings.

**10. To provide a feedback and reporting mechanism for verifiers to flag suspicious certificates**
The platform seeks to empower verifiers with the ability to submit structured feedback reports when they encounter suspicious or potentially fraudulent certificates. This objective supports continuous monitoring of the verification ecosystem and enables administrators to take corrective action when necessary.

---

**2.3 Summary of Objectives**

| # | Objective | Category |
|---|-----------|----------|
| 1 | Blockchain-based tamper-proof certificate storage | Primary |
| 2 | AI-powered certificate content validation | Primary |
| 3 | Role-based access control for four stakeholders | Primary |
| 4 | Automated end-to-end certificate lifecycle management | Primary |
| 5 | Real-time analytics and AI-generated visual reports | Secondary |
| 6 | Role-specific AI chatbot assistants | Secondary |
| 7 | JWT-based secure authentication and authorization | Secondary |
| 8 | Transparent verification history and audit trails | Secondary |
| 9 | Fully containerized Docker deployment | Secondary |
| 10 | Verifier feedback and suspicious certificate reporting | Secondary |

---

---

generate as a single paragrapgh

---


Here are the objectives in a single paragraph:

---

**2. Objectives**

The primary objective of CertiSense AI is to develop a secure, intelligent, and scalable blockchain-based certificate verification platform that eliminates credential fraud through tamper-proof storage of cryptographic hashes using the SHA-256 algorithm, ensuring that no issued certificate can be altered, duplicated, or deleted without detection. The system further aims to integrate an AI-powered validation layer capable of analyzing certificate content, computing confidence scores, and generating human-readable verification explanations, thereby adding an intelligent dimension beyond simple hash matching. A hierarchical role-based access control system is designed to serve four distinct stakeholders — Administrator, Institute, Student, and Verifier — each with dedicated dashboards and controlled access to system functionalities, ensuring that sensitive operations remain restricted to authorized entities while verification remains accessible to approved third parties. The project also seeks to automate the complete certificate lifecycle from institute registration, student enrollment, and certificate issuance through blockchain recording to third-party verification and feedback submission, minimizing manual intervention and human error throughout the process. Additionally, the system aims to provide real-time analytics dashboards and AI-generated visual reports for data-driven decision-making, deploy role-specific AI chatbot assistants for natural language interaction with live system data, implement JWT-based authentication with password hashing and role-based endpoint protection for comprehensive security, maintain complete audit trails of all verification events to promote transparency and accountability, package the entire application into Docker containers for consistent and portable deployment across any infrastructure environment, and provide a structured feedback mechanism that empowers verifiers to flag suspicious certificates and enables administrators to monitor and maintain the integrity of the verification ecosystem.

---

---

generate SCOPE AND RELEVANCE OF THE PROJECT

---


Here is the Scope and Relevance of the project in a single paragraph:

---

**3. Scope and Relevance of the Project**

The scope of CertiSense AI encompasses the complete design, development, and deployment of a multi-role blockchain certificate verification platform that addresses the growing global challenge of academic and professional credential fraud. The system covers the entire certificate lifecycle, from the registration of educational institutes and enrollment of students, through the AI-validated issuance and blockchain recording of certificates, to the real-time verification of credentials by third-party verifiers such as employers, recruitment agencies, and regulatory bodies, making it applicable across a wide range of industries including education, healthcare, finance, legal services, and corporate hiring. The platform is scoped to support four distinct user roles — Administrator, Institute, Student, and Verifier — each operating within a clearly defined boundary of permissions and functionalities, ensuring that the system remains organized, secure, and scalable as the number of users and certificates grows over time. From a technical perspective, the scope includes the implementation of SHA-256 cryptographic hashing, blockchain-based immutable storage, JWT authentication, AI-powered content validation, natural language chatbot assistants, automated visual report generation, file upload and management, and fully containerized Docker deployment, collectively forming a production-ready system capable of operating on standard cloud or VPS infrastructure. The relevance of this project is underscored by the increasing digitalization of academic records and professional qualifications worldwide, where the absence of a reliable, automated, and universally accessible verification mechanism has created significant vulnerabilities that fraudulent actors continue to exploit. By combining the immutability and transparency of blockchain with the analytical intelligence of artificial intelligence, CertiSense AI offers a technically sound and practically viable solution that reduces verification time from days to seconds, eliminates dependence on manual cross-referencing with issuing institutions, and provides all stakeholders with a trustworthy, auditable, and intelligent platform for managing the authenticity of credentials in the digital age, making it highly relevant to the current demands of educational institutions, employers, and regulatory authorities seeking modern alternatives to outdated certificate verification practices.

---

---

Scope of the Project, as bullted points

---


Here are the Scope of the Project as bulleted points:

---

**3. Scope of the Project**

- Covers the complete certificate lifecycle management including institute registration, student enrollment, certificate issuance, blockchain recording, third-party verification, and feedback submission

- Supports four distinct user roles — Administrator, Institute, Student, and Verifier — each with dedicated dashboards, controlled permissions, and role-specific functionalities

- Encompasses the implementation of SHA-256 cryptographic hashing for generating unique and tamper-proof certificate identifiers that are stored permanently on the blockchain ledger

- Includes an AI-powered certificate content validation module that analyzes uploaded documents, computes confidence scores, and generates intelligent verification explanations

- Covers the development of role-specific AI chatbot assistants that allow users to interact with live system data using natural language queries

- Encompasses real-time analytics dashboards for all user roles, providing up-to-date statistics on certificates, verifications, students, and institutes

- Includes automated AI-generated visual report generation with charts and intelligent insights for administrators and institutes

- Covers secure JWT-based authentication and authorization across all user roles with password hashing and role-based API endpoint protection

- Encompasses complete audit trail maintenance for all verification events, recording verifier identity, timestamp, result, and confidence score for every certificate check

- Includes a structured verifier feedback and suspicious certificate reporting mechanism that enables administrators to monitor and maintain platform integrity

- Covers file upload, storage, and download management for certificate PDF files issued by institutes and submitted by verifiers

- Encompasses full containerization of the application using Docker, enabling consistent and portable deployment across local, cloud, and VPS infrastructure environments

- Applicable across multiple industries including education, healthcare, finance, legal services, and corporate recruitment where credential verification is a critical requirement

- Limited in scope to certificate verification and does not extend to certificate design, printing, or physical distribution processes

- Currently scoped to use SQLite as the database for persistent storage, with the architecture designed to support migration to PostgreSQL or other relational databases for larger scale deployments

- Does not include integration with external government databases or third-party educational registries in the current version, though the system architecture supports such extensions in future iterations

---

---

relevance of the project

---


Here is the Relevance of the Project as bulleted points:

---

**4. Relevance of the Project**

- Directly addresses the growing global problem of academic and professional credential fraud, which affects millions of hiring decisions, university admissions, and regulatory compliance processes every year

- Provides a technologically advanced alternative to traditional manual certificate verification methods that are slow, error-prone, and heavily dependent on direct communication with issuing institutions

- Leverages blockchain technology, one of the most trusted and widely recognized solutions for data integrity and immutability, to ensure that certificate records cannot be tampered with, forged, or deleted once issued

- Highly relevant to the current digital transformation wave in the education sector, where institutions worldwide are transitioning from paper-based credentials to digital certificates that require robust and scalable verification infrastructure

- Addresses the needs of employers and recruitment agencies who face significant risks when hiring candidates with fraudulent qualifications, reducing the time and cost associated with background verification processes

- Aligns with the increasing global demand for instant, automated, and remotely accessible credential verification systems, particularly in the context of remote hiring, international recruitment, and online education

- Demonstrates practical relevance by reducing certificate verification time from days or weeks to a matter of seconds, significantly improving operational efficiency for all stakeholders involved in the verification process

- Relevant to regulatory and compliance-driven industries such as healthcare, law, finance, and engineering, where the authenticity of professional certifications directly impacts public safety and organizational accountability

- Contributes to the broader academic and research discourse on the application of blockchain and artificial intelligence in solving real-world trust and security challenges beyond financial transactions

- Supports the United Nations Sustainable Development Goal 4 on Quality Education by promoting transparency, accessibility, and integrity in the recognition of educational achievements across borders and institutions

- Relevant to students and certificate holders who benefit from having a secure, verifiable, and permanently accessible digital record of their qualifications that cannot be lost, damaged, or disputed

- Demonstrates the practical viability of combining multiple emerging technologies — blockchain, artificial intelligence, containerization, and modern web frameworks — into a single cohesive and production-ready application

- Highly relevant to developing nations and regions where institutional trust is limited and the need for independent, technology-driven verification mechanisms is particularly acute

- Addresses data privacy and security concerns by ensuring that sensitive certificate data is protected through cryptographic hashing, JWT authentication, and role-based access control rather than being stored or transmitted in plain text

- Relevant to the growing ecosystem of EdTech platforms, online learning providers, and digital credentialing initiatives such as Open Badges and Verifiable Credentials, where automated verification infrastructure is a foundational requirement

- Establishes a scalable and extensible foundation for future enhancements such as integration with government identity systems, cross-institutional blockchain networks, mobile verification applications, and international credential recognition frameworks

---

---

generate 2.1	 INTRODUCTION TO SYSTEM ANALYSIS

---


Here is the Introduction to System Analysis as a single paragraph:

---

**2.1 Introduction to System Analysis**

System analysis is the process of examining and evaluating an existing or proposed system to understand its components, interactions, data flows, and functional requirements in order to design a solution that effectively meets the needs of its intended users. In the context of CertiSense AI, system analysis plays a foundational role in identifying the core problems associated with traditional certificate verification methods, understanding the requirements of each stakeholder group, and defining the functional and non-functional specifications that guide the design and development of the platform. The analysis begins with a thorough examination of the existing certificate verification landscape, where manual processes, centralized databases, and paper-based records create significant vulnerabilities including credential fraud, verification delays, data tampering, and lack of transparency. By studying the workflows of educational institutes, students, employers, and system administrators, the analysis reveals the need for a multi-role platform that automates the certificate lifecycle, enforces strict access controls, and provides real-time visibility into verification activities. The system analysis for CertiSense AI encompasses the identification of functional requirements such as certificate issuance, blockchain recording, AI validation, role-based authentication, and verification history tracking, as well as non-functional requirements including system security, scalability, performance, usability, and deployment portability. It further involves the evaluation of appropriate technologies and architectural patterns, leading to the selection of FastAPI for the backend, React for the frontend, SQLite for data persistence, SHA-256 for cryptographic hashing, Docker for containerization, and a blockchain service layer for immutable certificate storage, collectively forming a technically sound and practically viable system architecture that addresses the identified challenges comprehensively and efficiently.

---

---

generate for EXISTING SYSTEM

---


Here is the Existing System section:

---

**2.2 Existing System**

**Overview**

The existing approaches to certificate verification rely predominantly on manual, centralized, and paper-based processes that have remained largely unchanged for decades despite the rapid advancement of digital technologies. In the current landscape, when an employer, academic institution, or regulatory body needs to verify the authenticity of a certificate presented by an individual, the process typically involves directly contacting the issuing institution via telephone, email, or postal correspondence, waiting for a response that can take anywhere from several days to several weeks, and manually cross-referencing the submitted document against institutional records. This approach is not only time-consuming and resource-intensive but also highly susceptible to human error, institutional delays, and deliberate manipulation by fraudulent actors who exploit the lack of a centralized and automated verification mechanism.

**Drawbacks of the Existing System**

- Verification is entirely manual and dependent on direct communication with the issuing institution, making the process slow, inefficient, and impractical for large-scale or time-sensitive hiring and admissions decisions

- Centralized databases maintained by individual institutions represent single points of failure that are vulnerable to data breaches, unauthorized modifications, insider tampering, and permanent data loss due to system failures or disasters

- Paper-based certificates are easily forged, photocopied, or digitally manipulated using widely available graphic editing tools, making visual inspection an unreliable method of authentication

- There is no standardized global framework for certificate verification, resulting in inconsistent processes across institutions, industries, and countries that create confusion and inefficiency for employers and regulatory bodies operating across borders

- The absence of a real-time verification mechanism means that fraudulent certificates can remain undetected for extended periods, causing significant harm to organizations that unknowingly hire or admit unqualified individuals

- Existing digital certificate systems, where they exist, are typically siloed within individual institutions and lack interoperability, preventing verifiers from accessing a unified and trustworthy source of certificate records

- Manual verification processes place a significant administrative burden on issuing institutions, diverting staff time and resources away from core educational and operational activities

- There is no audit trail or verification history maintained in traditional systems, making it impossible to track who verified a certificate, when it was verified, and what the outcome was, thereby eliminating accountability from the verification process

- Students and certificate holders have no visibility into the verification status of their credentials, leaving them uninformed about whether their qualifications have been checked and by whom

- Traditional systems offer no mechanism for detecting or flagging suspicious verification attempts, forged documents, or patterns of fraudulent activity, leaving organizations entirely reactive rather than proactive in their approach to credential fraud

- The lack of cryptographic security in existing systems means that digital copies of certificates can be altered without any detectable trace, undermining the integrity of even digitally issued credentials

- Existing verification platforms that do exist are often proprietary, expensive, and accessible only to large institutions with significant technical and financial resources, excluding smaller organizations and individuals from benefiting from automated verification capabilities

**Summary**

The collective limitations of existing certificate verification systems — including manual processes, centralized vulnerabilities, lack of transparency, absence of audit trails, and susceptibility to fraud — clearly demonstrate the need for a modern, automated, and technologically robust solution. These shortcomings form the primary motivation for the development of CertiSense AI, which addresses each of these drawbacks through the integration of blockchain technology, artificial intelligence, and a secure multi-role web platform designed to make certificate verification instant, reliable, transparent, and accessible to all stakeholders.

---

---

generate limitations of existing system

---


Here are the Limitations of the Existing System:

---

**2.3 Limitations of the Existing System**

**1. Manual Verification Process**
The existing certificate verification process is entirely manual, requiring verifiers to individually contact issuing institutions through phone, email, or physical correspondence. This approach is time-consuming, labor-intensive, and highly inefficient, particularly in scenarios involving large volumes of certificate verification requests such as mass recruitment drives, university admissions, or regulatory compliance audits, where the sheer number of certificates to be verified makes manual processing practically infeasible.

**2. Lack of Real-Time Verification**
Traditional verification systems offer no mechanism for instant or real-time certificate authentication. The time required to verify a single certificate through conventional channels can range from several days to several weeks, creating significant delays in hiring processes, academic admissions, and professional licensing decisions that depend on the timely confirmation of an individual's qualifications.

**3. Vulnerability to Certificate Forgery**
Existing paper-based and digitally issued certificates are highly susceptible to forgery and manipulation. Widely available graphic editing software enables fraudulent actors to alter names, grades, dates, and institutional seals on certificate documents with relative ease, and the absence of cryptographic security measures means that such alterations leave no detectable trace, making visual inspection an entirely unreliable method of authentication.

**4. Centralized and Single Point of Failure**
Certificate records maintained in centralized institutional databases represent critical single points of failure that are vulnerable to data breaches, unauthorized access, insider tampering, accidental deletion, and catastrophic system failures. The loss or corruption of such centralized records can render entire batches of legitimate certificates unverifiable, causing significant harm to the individuals whose qualifications can no longer be confirmed.

**5. Absence of Immutable Record Keeping**
Unlike blockchain-based systems, traditional certificate databases offer no guarantee of immutability. Records stored in conventional databases can be modified, deleted, or overwritten by authorized or unauthorized users without leaving a permanent and auditable trace, undermining the fundamental trustworthiness of the verification process and creating opportunities for institutional misconduct or data manipulation.

**6. No Standardized Global Framework**
There is no universally accepted standard or interoperable framework for certificate verification across institutions, industries, and countries. Each institution maintains its own verification process, format, and timeline, resulting in a fragmented and inconsistent ecosystem that creates confusion, inefficiency, and inequity for employers, regulatory bodies, and individuals operating across different jurisdictions and sectors.

**7. Lack of Audit Trail and Accountability**
Existing verification systems maintain no systematic record of verification activities, making it impossible to determine who verified a certificate, when the verification took place, what the outcome was, and whether the verification was conducted legitimately. This absence of an audit trail eliminates accountability from the verification process and prevents organizations from detecting patterns of suspicious or fraudulent verification behavior.

**8. No Transparency for Certificate Holders**
Students and certificate holders in traditional systems have no visibility into the verification status of their own credentials. They are unable to determine whether their certificates have been checked, by whom, how many times, or with what result, leaving them entirely uninformed about the use and authentication of their own qualifications and creating a fundamental imbalance of information between certificate holders and verifiers.

**9. High Administrative Burden on Institutions**
The manual nature of existing verification processes places a disproportionate administrative burden on issuing institutions, which must dedicate significant staff time, resources, and infrastructure to responding to individual verification requests. This burden diverts institutional capacity away from core educational and operational activities and scales poorly as the volume of verification requests increases over time.

**10. Limited Accessibility and Inclusivity**
Existing automated verification platforms, where they do exist, are typically proprietary, expensive, and accessible only to large and well-resourced institutions. Smaller educational organizations, vocational training centers, and institutions in developing regions are often excluded from such systems due to cost and technical barriers, creating a significant disparity in the quality and reliability of certificate verification across different segments of the education and employment ecosystem.

**11. Inability to Detect Suspicious Patterns**
Traditional verification systems offer no analytical or intelligence-driven capability to detect suspicious patterns of certificate submission, such as multiple verifications of the same forged document, unusually high volumes of verification requests from a single source, or certificates with inconsistent formatting and metadata. This reactive rather than proactive approach to fraud detection allows fraudulent activity to persist undetected for extended periods.

**12. No Integration Between Stakeholders**
Existing systems operate in isolation, with no integrated platform connecting institutes, students, employers, and administrators in a unified ecosystem. The lack of interoperability between these stakeholders means that information must be exchanged through fragmented and inefficient channels, increasing the risk of miscommunication, data loss, and verification errors that could have serious consequences for all parties involved.

**Summary Table**

| # | Limitation | Impact |
|---|-----------|--------|
| 1 | Manual verification process | Slow and inefficient |
| 2 | No real-time verification | Delays in critical decisions |
| 3 | Vulnerability to forgery | High fraud risk |
| 4 | Centralized single point of failure | Data loss and breach risk |
| 5 | No immutable record keeping | Data manipulation risk |
| 6 | No standardized global framework | Inconsistent verification |
| 7 | No audit trail | Lack of accountability |
| 8 | No transparency for certificate holders | Information imbalance |
| 9 | High administrative burden | Resource inefficiency |
| 10 | Limited accessibility | Exclusion of smaller institutions |
| 11 | No suspicious pattern detection | Reactive fraud management |
| 12 | No stakeholder integration | Fragmented ecosystem |

---

---

make each poinst short

---


Here are the Limitations of the Existing System in short points:

---

**2.3 Limitations of the Existing System**

**1. Manual Verification Process**
Certificate verification relies entirely on manual communication with issuing institutions through phone or email, making the process slow, labor-intensive, and impractical for large-scale verification requirements.

**2. Lack of Real-Time Verification**
Traditional systems offer no mechanism for instant authentication, with verification turnaround times ranging from several days to weeks, causing significant delays in hiring, admissions, and licensing decisions.

**3. Vulnerability to Certificate Forgery**
Paper-based and digital certificates are easily forged or manipulated using widely available graphic editing tools, with no cryptographic security measures in place to detect alterations or tampering.

**4. Centralized Single Point of Failure**
Certificate records stored in centralized institutional databases are vulnerable to data breaches, unauthorized access, accidental deletion, and system failures that can render legitimate certificates permanently unverifiable.

**5. No Immutable Record Keeping**
Records in conventional databases can be modified or deleted without leaving a detectable trace, undermining the trustworthiness of the verification process and creating opportunities for data manipulation.

**6. No Standardized Global Framework**
The absence of a universally accepted verification standard results in a fragmented ecosystem with inconsistent processes across institutions, industries, and countries, creating confusion for cross-border employers and regulatory bodies.

**7. No Audit Trail or Accountability**
Existing systems maintain no record of verification activities, making it impossible to track who verified a certificate, when it was verified, and what the outcome was, eliminating accountability from the process entirely.

**8. No Transparency for Certificate Holders**
Students have no visibility into the verification status of their own credentials, leaving them uninformed about whether their certificates have been checked, by whom, and with what result.

**9. High Administrative Burden**
Manual verification places a heavy administrative load on issuing institutions, diverting staff time and resources away from core activities and scaling poorly as verification volumes increase.

**10. Limited Accessibility**
Existing automated verification platforms are typically proprietary and expensive, excluding smaller institutions and organizations in developing regions from accessing reliable and automated verification capabilities.

**11. No Suspicious Pattern Detection**
Traditional systems lack any analytical capability to identify fraudulent patterns such as repeated submission of forged documents or unusually high verification volumes, resulting in a purely reactive approach to fraud.

**12. No Stakeholder Integration**
Existing systems operate in isolation with no unified platform connecting institutes, students, employers, and administrators, leading to fragmented communication, data loss, and increased verification errors.

---

---

prospssed system

---


Here is the Proposed System:

---

**2.4 Proposed System**

CertiSense AI is a proposed blockchain-powered certificate verification platform designed to overcome all the limitations identified in existing systems by integrating modern technologies including blockchain, artificial intelligence, cryptographic hashing, and role-based access control into a single unified and production-ready web application.

**1. Blockchain-Based Certificate Storage**
The proposed system stores the SHA-256 cryptographic hash of every issued certificate permanently on an immutable blockchain ledger, ensuring that certificate records cannot be altered, duplicated, or deleted once recorded. Each certificate is assigned a unique identifier and a chain hash that links it permanently to the issuing institution and the student, providing a tamper-proof and universally verifiable record of authenticity.

**2. AI-Powered Certificate Validation**
The system incorporates an artificial intelligence validation layer that analyzes the content of uploaded certificate files, computes confidence scores, detects anomalies, and generates intelligent human-readable explanations for every verification outcome, adding a layer of intelligent assessment beyond simple hash comparison.

**3. Role-Based Access Control**
The platform implements a hierarchical four-role access control system comprising Administrator, Institute, Student, and Verifier, each operating within clearly defined permission boundaries and accessing dedicated dashboards tailored to their specific responsibilities within the certificate ecosystem.

**4. Automated Certificate Lifecycle Management**
The proposed system automates the complete certificate lifecycle from institute registration, student enrollment, and AI-validated certificate issuance through blockchain recording to real-time third-party verification and structured feedback submission, eliminating manual intervention at every stage of the process.

**5. Real-Time Instant Verification**
Verifiers can upload any certificate file to the platform and receive an instant verification result within seconds, as the system automatically computes the file hash and cross-references it against the blockchain registry, reducing verification time from days or weeks to a matter of seconds.

**6. Complete Audit Trail and Transparency**
The system maintains a comprehensive and permanent record of every verification event, including the verifier identity, timestamp, result, and confidence score, providing full transparency and accountability across the entire verification ecosystem for all stakeholders.

**7. Student Certificate Visibility**
Students are provided with a dedicated dashboard where they can view all their issued certificates, track verification history, monitor who has verified their credentials, download certificate files, and access detailed blockchain and hash information for each of their qualifications.

**8. Role-Specific AI Chatbot Assistants**
The platform deploys intelligent AI chatbot assistants for each user role, enabling administrators, institutes, and verifiers to interact with live system data using natural language queries, retrieve statistics, and obtain system insights without navigating complex interfaces.

**9. Real-Time Analytics and Visual Reports**
All user roles are equipped with real-time analytics dashboards displaying up-to-date statistics and performance metrics. Administrators can additionally generate AI-powered visual reports with charts and intelligent insights covering institute performance, certificate analytics, verification trends, and system-wide activity.

**10. Secure JWT Authentication**
The system implements JSON Web Token based authentication across all user roles with SHA-256 password hashing, token expiration management, and role-based API endpoint protection, ensuring that all system operations are secured against unauthorized access and session hijacking.

**11. Verifier Feedback Mechanism**
The platform provides verifiers with a structured feedback submission system that allows them to report suspicious certificates, flag fraudulent documents, and communicate verification issues to administrators, enabling proactive monitoring and rapid response to credential fraud attempts.

**12. Containerized Deployment**
The entire application is packaged into Docker containers that can be deployed consistently and reliably across any infrastructure environment including local machines, cloud platforms, and virtual private servers, ensuring portability, scalability, and ease of maintenance throughout the system lifecycle.

**Comparison with Existing System**

| Feature | Existing System | Proposed System |
|---------|----------------|-----------------|
| Verification Speed | Days to Weeks | Seconds |
| Fraud Detection | Manual | AI-Powered |
| Record Immutability | No | Blockchain-Based |
| Audit Trail | No | Complete |
| Student Visibility | No | Full Dashboard |
| Real-Time Analytics | No | Yes |
| Stakeholder Integration | Fragmented | Unified Platform |
| Authentication | Basic | JWT + SHA-256 |
| Deployment | Manual | Docker Containerized |
| Accessibility | Limited | Web-Based, Open |

---

---

2.3.1	ADVANTAGES OF THE PROPOSED SYSTEM

---


Here are the Advantages of the Proposed System:

---

**2.3.1 Advantages of the Proposed System**

**1. Instant Certificate Verification**
The proposed system reduces certificate verification time from days or weeks to a matter of seconds by automating the entire verification process through cryptographic hash comparison against the blockchain registry, enabling employers, academic institutions, and regulatory bodies to authenticate credentials instantly without any manual intervention or institutional communication.

**2. Tamper-Proof Certificate Records**
By storing SHA-256 cryptographic hashes of all issued certificates on an immutable blockchain ledger, the system guarantees that certificate records cannot be altered, forged, duplicated, or deleted once recorded, providing a permanently trustworthy and mathematically verifiable source of truth for all credentials managed within the platform.

**3. AI-Powered Intelligent Validation**
The integration of an artificial intelligence validation layer adds a sophisticated dimension of document analysis beyond simple hash matching, enabling the system to assess certificate content quality, detect anomalies, compute confidence scores, and generate intelligent explanations that provide verifiers with deeper insight into the authenticity of submitted credentials.

**4. Elimination of Certificate Fraud**
The combination of blockchain immutability and AI-powered validation creates a dual-layer fraud prevention mechanism that makes it virtually impossible for fraudulent certificates to pass verification undetected, significantly reducing the risk of credential fraud across all industries and sectors that rely on the platform for authentication.

**5. Unified Multi-Stakeholder Platform**
The proposed system brings together all certificate ecosystem stakeholders — Administrators, Institutes, Students, and Verifiers — into a single unified platform with role-specific dashboards and controlled access, eliminating the fragmented and siloed communication channels that characterize existing verification systems and creating a cohesive and efficient ecosystem for all parties.

**6. Complete Transparency and Audit Trail**
Every verification event is permanently recorded with full details including verifier identity, timestamp, result, and confidence score, providing complete transparency and accountability across the verification ecosystem and enabling administrators to monitor all system activities, detect suspicious patterns, and maintain a comprehensive historical record of all credential authentications.

**7. Student Empowerment and Visibility**
Students are provided with full visibility into the status of their own credentials through a dedicated dashboard that displays all issued certificates, verification history, verifier details, blockchain hash information, and download capabilities, empowering certificate holders with information and control over their own qualifications for the first time.

**8. Reduced Administrative Burden**
By automating the certificate issuance, recording, and verification processes, the system significantly reduces the administrative workload on issuing institutions, freeing staff from the time-consuming task of responding to individual verification requests and allowing institutional resources to be redirected toward core educational and operational activities.

**9. Real-Time Analytics and Insights**
Comprehensive real-time analytics dashboards and AI-generated visual reports provide all stakeholders with up-to-date statistics, performance metrics, and intelligent insights that support data-driven decision-making, enabling administrators and institutes to monitor system health, track verification trends, and identify areas for improvement at any time.

**10. Role-Specific AI Chatbot Assistance**
The deployment of intelligent AI chatbot assistants for each user role enables natural language interaction with live system data, making the platform significantly more accessible and user-friendly by allowing stakeholders to retrieve information, query statistics, and obtain system insights through conversational interfaces without requiring technical expertise.

**11. Enhanced Security and Data Protection**
The implementation of JWT-based authentication, SHA-256 password hashing, role-based API endpoint protection, and CORS security measures ensures that all system operations, user sessions, and sensitive data are comprehensively protected against unauthorized access, session hijacking, and cross-origin attacks throughout the platform.

**12. Scalable and Portable Deployment**
The fully containerized Docker architecture ensures that the entire application can be deployed consistently and reliably across any infrastructure environment, from local development machines to cloud platforms and virtual private servers, providing exceptional portability, scalability, and ease of maintenance that supports the long-term growth and evolution of the platform.

**13. Proactive Fraud Monitoring**
The structured verifier feedback mechanism combined with administrative oversight tools enables proactive monitoring of the verification ecosystem, allowing administrators to receive reports of suspicious certificates, flag fraudulent documents, and take corrective action before credential fraud causes significant harm to organizations or individuals.

**14. Cost-Effective Solution**
By eliminating the need for manual verification staff, third-party verification services, and proprietary credentialing platforms, the proposed system offers a significantly more cost-effective approach to certificate authentication that is accessible to institutions of all sizes, including smaller organizations and those in developing regions that have historically been excluded from automated verification capabilities.

**15. Future-Ready and Extensible Architecture**
The modular and well-structured architecture of CertiSense AI is designed to support future enhancements including integration with government identity systems, cross-institutional blockchain networks, mobile verification applications, and international credential recognition frameworks, ensuring that the platform remains relevant and adaptable as the digital credentialing landscape continues to evolve.

---

---

2.4	FEASIBILITY STUDY

---


Here is the Feasibility Study:

---

**2.4 Feasibility Study**

A feasibility study is a systematic evaluation conducted prior to the development of a system to determine whether the proposed project is technically achievable, economically viable, operationally practical, and legally compliant within the given constraints of time, resources, and infrastructure. For CertiSense AI, the feasibility study examines four key dimensions — technical feasibility, economic feasibility, operational feasibility, and legal feasibility — to establish that the proposed blockchain certificate verification platform can be successfully developed, deployed, and sustained in a real-world environment.

---

**2.4.1 Technical Feasibility**

Technical feasibility assesses whether the technologies, tools, and infrastructure required to build and operate the proposed system are available, mature, and capable of meeting the functional and non-functional requirements identified during system analysis.

- **Frontend Technology:** React 18 with Tailwind CSS and Vite provides a modern, component-based, and highly performant frontend framework that is widely adopted, well-documented, and fully capable of delivering the dynamic, role-specific dashboards and interactive interfaces required by CertiSense AI.

- **Backend Technology:** FastAPI, a high-performance Python web framework, provides the necessary capabilities for building secure, scalable, and well-documented RESTful API endpoints with built-in support for asynchronous processing, JWT authentication, file uploads, and dependency injection, making it an ideal choice for the backend of the proposed system.

- **Blockchain Integration:** The blockchain service layer implemented using Web3.py and the SHA-256 cryptographic hashing algorithm provides a technically sound and proven mechanism for generating tamper-proof certificate identifiers and maintaining an immutable verification registry that meets the core security requirements of the platform.

- **AI Validation:** The integration of a locally hosted large language model in the GGUF format along with a custom AI validation service provides the necessary intelligence for certificate content analysis, confidence scoring, and natural language chatbot interactions, all of which are technically achievable using available open-source AI frameworks and libraries.

- **Database:** SQLAlchemy with SQLite provides a reliable, lightweight, and fully functional relational database solution for the current scale of the system, with the architecture designed to support seamless migration to PostgreSQL or other enterprise-grade databases as the platform scales.

- **Containerization:** Docker and Docker Compose provide a mature, widely adopted, and technically proven containerization solution that ensures consistent, portable, and reliable deployment of the entire application stack across any infrastructure environment.

- **Verdict:** The proposed system is fully technically feasible using available, mature, and well-supported technologies that collectively meet all identified functional and non-functional requirements.

---

**2.4.2 Economic Feasibility**

Economic feasibility evaluates whether the proposed system can be developed and operated within acceptable cost boundaries and whether the financial benefits it delivers justify the investment required for its development and maintenance.

- **Development Cost:** The entire system is built using open-source technologies including React, FastAPI, Python, SQLite, Docker, and various open-source AI libraries, eliminating licensing costs and making the development investment primarily a function of developer time and effort rather than software procurement.

- **Deployment Cost:** The containerized architecture of CertiSense AI enables deployment on affordable VPS infrastructure such as Hostinger, DigitalOcean, or Contabo, with monthly hosting costs ranging from approximately 7 to 20 US dollars depending on the selected plan, making the platform economically accessible to institutions of all sizes.

- **Operational Cost:** Once deployed, the system requires minimal ongoing operational expenditure, as the automated nature of certificate issuance, blockchain recording, and verification eliminates the need for dedicated verification staff and reduces the administrative overhead associated with manual credential authentication processes.

- **Cost Savings:** Organizations adopting CertiSense AI can expect significant cost savings from the elimination of manual verification processes, reduction in credential fraud-related losses, decreased reliance on third-party verification services, and improved operational efficiency across hiring, admissions, and compliance workflows.

- **Return on Investment:** The combination of low development and operational costs with significant savings in verification time, fraud prevention, and administrative efficiency delivers a compelling return on investment for educational institutions, employers, and regulatory bodies that adopt the platform.

- **Verdict:** The proposed system is economically feasible, offering a cost-effective development and deployment model with clear and measurable financial benefits that justify the investment required for its implementation.

---

**2.4.3 Operational Feasibility**

Operational feasibility determines whether the proposed system can be effectively integrated into the existing workflows and practices of its intended users and whether those users possess the skills and motivation necessary to adopt and operate the platform successfully.

- **User Interface:** The React-based frontend with Tailwind CSS delivers an intuitive, responsive, and visually consistent user interface that minimizes the learning curve for all user roles, enabling administrators, institute staff, students, and verifiers to navigate and operate the platform with minimal training.

- **Role-Based Workflows:** The hierarchical role-based access control system ensures that each user interacts only with the functionalities relevant to their specific responsibilities, reducing cognitive complexity and making the platform operationally straightforward for all stakeholder groups regardless of their technical background.

- **AI Chatbot Assistance:** The deployment of role-specific AI chatbot assistants provides users with on-demand guidance and information retrieval capabilities through natural language interaction, further reducing the operational barrier to adoption and ensuring that users can access the help they need without external support.

- **Automated Processes:** The automation of certificate issuance, blockchain recording, hash generation, and verification eliminates the need for users to understand or manage the underlying technical processes, making the system operationally transparent and accessible to non-technical users across all roles.

- **Training Requirements:** The intuitive design of the platform, combined with role-specific dashboards and AI assistance, means that minimal formal training is required for users to become proficient in operating the system, reducing the operational cost and effort associated with platform adoption.

- **Verdict:** The proposed system is operationally feasible, offering an intuitive and automated user experience that can be effectively integrated into the existing workflows of educational institutions, employers, and regulatory bodies with minimal disruption and training requirements.

---

**2.4.4 Legal Feasibility**

Legal feasibility examines whether the proposed system complies with applicable laws, regulations, and ethical standards governing data privacy, security, intellectual property, and digital transactions in the jurisdictions where it will be deployed and operated.

- **Data Privacy:** The system handles personal data including student names, email addresses, and certificate information in compliance with data protection principles by implementing role-based access controls, JWT authentication, and password hashing to ensure that sensitive information is accessible only to authorized users.

- **Cryptographic Standards:** The use of SHA-256, a widely recognized and legally accepted cryptographic standard, for certificate hashing ensures that the system's security mechanisms are compliant with international cryptographic regulations and standards applicable to digital document authentication.

- **Open Source Compliance:** All third-party libraries and frameworks used in the development of CertiSense AI are open-source and distributed under permissive licenses including MIT, Apache 2.0, and BSD, ensuring full compliance with intellectual property laws and eliminating any licensing conflicts or proprietary software obligations.

- **Digital Records:** The blockchain-based immutable record keeping mechanism aligns with the principles of digital evidence admissibility and electronic record integrity recognized in many jurisdictions, supporting the legal validity of certificate verification outcomes produced by the platform.

- **Verdict:** The proposed system is legally feasible, operating in compliance with applicable data protection principles, cryptographic standards, open-source licensing requirements, and digital record keeping regulations.

---

**2.4.5 Feasibility Summary**

| Feasibility Dimension | Assessment | Verdict |
|----------------------|------------|---------|
| Technical Feasibility | Mature technologies, proven frameworks, available infrastructure | ✅ Feasible |
| Economic Feasibility | Low development cost, affordable deployment, high ROI | ✅ Feasible |
| Operational Feasibility | Intuitive UI, automated workflows, minimal training required | ✅ Feasible |
| Legal Feasibility | Data privacy compliant, open-source licensed, cryptographic standards | ✅ Feasible |

The feasibility study conclusively demonstrates that CertiSense AI is technically achievable, economically viable, operationally practical, and legally compliant, confirming that the proposed system can be successfully developed, deployed, and sustained as a production-ready blockchain certificate verification platform.

---

---

2.4.1 TECHNICAL FEASIBILITY

---


Here is the Technical Feasibility section:

---

**2.4.1 Technical Feasibility**

Technical feasibility assesses whether the technologies, tools, frameworks, and infrastructure required to design, develop, and operate the proposed system are available, mature, and collectively capable of meeting all the functional and non-functional requirements identified during the system analysis phase. For CertiSense AI, the technical feasibility evaluation examines each component of the system stack to confirm that the chosen technologies are appropriate, reliable, and sufficient for delivering a production-ready blockchain certificate verification platform.

**1. Frontend Technology**
The frontend of CertiSense AI is built using React 18, a widely adopted and extensively documented JavaScript library for building dynamic and component-based user interfaces, combined with Tailwind CSS for responsive and consistent styling and Vite as the build tool for fast development and optimized production builds. This technology combination is technically mature, actively maintained, and fully capable of delivering the interactive, role-specific dashboards, real-time data displays, file upload interfaces, and chatbot components required by the platform. The use of Axios for API communication and the Context API for state management further ensures that the frontend can reliably handle authentication flows, dynamic data fetching, and role-based rendering across all four user dashboards.

**2. Backend Technology**
The backend is developed using FastAPI, a modern and high-performance Python web framework that provides built-in support for asynchronous request handling, automatic API documentation, JWT authentication, file upload processing, form data handling, and dependency injection. FastAPI is technically well-suited for the demands of CertiSense AI, offering the speed, flexibility, and security features necessary to support multiple concurrent user roles, complex business logic, blockchain integration, AI service calls, and file management operations within a single cohesive application.

**3. Database Technology**
SQLAlchemy with SQLite is used as the database layer for persistent storage of all system entities including institutes, students, verifiers, certificates, verifications, and feedback records. SQLite provides a lightweight, serverless, and fully functional relational database solution that is technically sufficient for the current scale of the system, while the SQLAlchemy ORM ensures that the data access layer is abstracted and portable, supporting seamless migration to PostgreSQL or other enterprise-grade databases as the platform grows and scales beyond its initial deployment.

**4. Blockchain Integration**
The blockchain service layer is implemented using Web3.py, a Python library for interacting with Ethereum-compatible blockchain networks, combined with Hardhat for smart contract development and deployment. The SHA-256 cryptographic hashing algorithm is used to generate unique and tamper-proof certificate identifiers that are stored on the blockchain, providing a technically proven and mathematically secure mechanism for ensuring the immutability and verifiability of all certificate records managed by the platform.

**5. Cryptographic Security**
The system employs SHA-256, one of the most widely recognized and technically robust cryptographic hash functions available, for generating certificate hashes and securing user passwords. SHA-256 produces a fixed-length 256-bit hash that is computationally infeasible to reverse or forge, providing a technically sound foundation for the platform's fraud prevention and data integrity mechanisms.

**6. AI Validation Service**
The AI validation layer is implemented using a locally hosted large language model in the GGUF format, supported by a custom AI validation service that analyzes certificate content, computes confidence scores, and generates intelligent verification explanations. Additionally, role

---

You stopped your current work, please provide additional examples or ask another question.

---

2.4.2 OPERATIONAL FEASIBILITY

---


Here is the Operational Feasibility section:

---

**2.4.2 Operational Feasibility**

Operational feasibility determines whether the proposed CertiSense AI system can be effectively integrated into the existing workflows and daily practices of its intended users, and whether the platform delivers sufficient practical value to justify its adoption across all stakeholder groups. It evaluates the ease of use, accessibility, training requirements, workflow compatibility, and overall user acceptance of the system in a real-world operational environment.

**1. Ease of Use**
The React-based frontend developed with Tailwind CSS delivers a clean, modern, and visually consistent user interface that prioritizes simplicity and intuitiveness across all four user roles. Each dashboard is designed with role-specific navigation, clearly labeled actions, and contextual feedback mechanisms that guide users through their respective workflows without requiring any prior technical knowledge or specialized training, ensuring that the platform is accessible to a broad and diverse user base.

**2. Role-Specific Workflows**
The hierarchical role-based access control system ensures that each user interacts exclusively with the functionalities relevant to their specific responsibilities within the certificate ecosystem. Administrators manage institutes and monitor system analytics, institutes enroll students and issue certificates, students track their credentials and verification history, and verifiers authenticate certificates and submit feedback, with each role operating within a clearly defined and operationally straightforward workflow that minimizes confusion and reduces the risk of user error.

**3. Automated Certificate Processes**
The automation of core operational processes including certificate issuance, SHA-256 hash generation, blockchain recording, AI validation, and verification result generation eliminates the need for users to understand or manually manage the underlying technical mechanisms of the system. Users simply upload files, fill forms, and receive results, while the platform handles all complex backend operations transparently and efficiently in the background.

**4. AI Chatbot Assistance**
The deployment of role-specific AI chatbot assistants provides all users with on-demand guidance, information retrieval, and system interaction capabilities through natural language conversation. Administrators, institutes, and verifiers can ask questions about system statistics, recent activities, and operational data in plain language and receive accurate, context-aware responses without navigating complex menus or generating manual reports, significantly enhancing the operational accessibility of the platform.

**5. Minimal Training Requirements**
The intuitive design of the platform, combined with role-specific dashboards, automated workflows, contextual alerts, and AI chatbot assistance, means that users across all roles can become proficient in operating the system with minimal formal training. The self-explanatory nature of the interface reduces onboarding time and training costs, making the platform operationally practical for institutions with limited IT support capacity.

**6. Real-Time Feedback and Notifications**
The system provides users with immediate operational feedback at every stage of their workflow, including success confirmations upon certificate issuance, instant verification results upon file upload, real-time dashboard updates reflecting the latest system statistics, and clear error messages that guide users toward corrective action when issues arise, ensuring a smooth and responsive operational experience throughout the platform.

**7. Compatibility with Existing Workflows**
CertiSense AI is designed as a web-based platform accessible through any modern browser on desktop or mobile devices, requiring no software installation or hardware upgrades on the part of end users. This browser-based accessibility ensures seamless compatibility with the existing digital workflows of educational institutions, corporate HR departments, and regulatory bodies, minimizing operational disruption during the transition from traditional verification methods to the proposed system.

**8. Scalability of Operations**
The platform is operationally designed to handle growing volumes of users, certificates, and verification requests without degrading performance or requiring significant changes to operational workflows. The containerized Docker architecture and modular backend design ensure that the system can be scaled horizontally to accommodate increasing operational demands as the platform is adopted by more institutions and verifiers over time.

**9. Verifier Feedback Operations**
The structured feedback submission mechanism enables verifiers to report suspicious certificates, flag fraudulent documents, and communicate operational issues to administrators through a simple and intuitive form interface. This operational capability ensures that the platform supports proactive fraud monitoring and continuous improvement of the verification ecosystem without requiring complex administrative procedures or external communication channels.

**10. System Availability and Reliability**
The Docker-based deployment with restart policies ensures that both the frontend and backend containers automatically recover from unexpected failures, maintaining high system availability and operational continuity for all users. The use of persistent volume mounts for the SQLite database and certificate file storage further ensures that operational data is preserved across container restarts and system updates without any loss of critical information.

**Operational Feasibility Summary**

| Operational Factor | Assessment |
|-------------------|------------|
| User Interface | Intuitive, role-specific, browser-based |
| Workflow Integration | Compatible with existing digital workflows |
| Training Requirements | Minimal, self-explanatory interface |
| Process Automation | Full automation of core certificate operations |
| AI Assistance | Role-specific natural language chatbot support |
| Real-Time Feedback | Instant results and dashboard updates |
| Scalability | Horizontally scalable containerized architecture |
| System Availability | Auto-restart Docker deployment with data persistence |

The operational feasibility assessment conclusively confirms that CertiSense AI can be effectively integrated into the real-world workflows of educational institutions, employers, and regulatory bodies with minimal disruption, training, and operational overhead, delivering a practical, accessible, and reliable certificate verification solution that all stakeholder groups can adopt and operate with confidence.

---

---

2.4.3 ECONOMICAL FEASIBILITY

---


Here is the Economic Feasibility section:

---

**2.4.3 Economic Feasibility**

Economic feasibility evaluates whether the proposed CertiSense AI system can be developed, deployed, and maintained within acceptable cost boundaries, and whether the financial benefits and cost savings delivered by the platform justify the investment required for its implementation. It examines the development costs, deployment expenses, operational expenditure, and the overall return on investment that the system offers to educational institutions, employers, and regulatory bodies that adopt it as their primary certificate verification solution.

**1. Low Development Cost**
The entire CertiSense AI platform is built exclusively using open-source technologies including React, FastAPI, Python, SQLite, SQLAlchemy, Docker, Web3.py, and various open-source AI libraries, eliminating all software licensing and procurement costs from the development budget. The investment required for development is therefore primarily a function of developer time and effort rather than expensive proprietary software acquisition, making the platform economically accessible to academic projects, startups, and small to medium-sized institutions with limited development budgets.

**2. Affordable Deployment Infrastructure**
The fully containerized Docker architecture of CertiSense AI enables deployment on widely available and cost-effective virtual private server infrastructure. Platforms such as Hostinger, Contabo, DigitalOcean, and Railway offer VPS plans with sufficient computing resources to run the entire application stack at monthly costs ranging from approximately 7 to 20 US dollars, representing a significantly more affordable deployment model compared to proprietary certificate verification platforms that typically charge substantial subscription or per-verification fees.

**3. Minimal Operational Expenditure**
Once deployed, the system requires minimal ongoing operational expenditure due to the highly automated nature of its core processes. Certificate issuance, blockchain recording, hash generation, AI validation, and verification are all handled automatically by the platform without requiring dedicated operational staff, reducing the recurring costs associated with running and maintaining the system to little more than the monthly hosting fee and occasional software updates.

**4. Elimination of Third-Party Verification Costs**
Organizations that currently rely on third-party background verification services or manual institutional communication for certificate authentication incur significant per-verification costs that accumulate rapidly at scale. CertiSense AI eliminates these recurring third-party expenses entirely by providing an in-house, automated verification capability that delivers instant results at no additional cost per verification, regardless of the volume of certificates authenticated through the platform.

**5. Reduction in Credential Fraud Losses**
Credential fraud imposes substantial financial costs on organizations through the hiring of unqualified individuals, the subsequent performance failures, legal liabilities, and reputational damage that result from employing candidates with fraudulent qualifications. By providing a reliable and instant certificate authentication mechanism, CertiSense AI significantly reduces the financial exposure of organizations to credential fraud-related losses, delivering measurable economic value that far exceeds the modest cost of deploying and operating the platform.

**6. Reduced Administrative Overhead**
The automation of certificate verification processes eliminates the need for dedicated administrative staff to handle verification requests, communicate with issuing institutions, and maintain manual verification records. This reduction in administrative overhead translates directly into cost savings for educational institutions, corporate HR departments, and regulatory bodies that currently allocate significant human resources to manual credential authentication activities.

**7. Scalable Cost Structure**
Unlike traditional verification systems where costs scale linearly with verification volume due

---

You stopped your current work, please provide additional examples or ask another question.

---

3.1	 INTRODUCTION TO SYSTEM DESIGN

---


Here is the Introduction to System Design:

---

**3.1 Introduction to System Design**

System design is the process of defining the architecture, components, modules, interfaces, and data flows of a proposed system in order to satisfy the specified functional and non-functional requirements identified during the system analysis phase. It serves as the blueprint for the entire development process, translating the abstract requirements and objectives of the system into concrete technical specifications, structural diagrams, and implementation guidelines that guide developers in building a coherent, efficient, and maintainable software solution. In the context of CertiSense AI, system design plays a critical role in establishing the overall architectural framework, defining the interactions between the frontend, backend, blockchain, and AI components, and ensuring that the platform is built in a manner that is secure, scalable, and aligned with the needs of all four stakeholder roles.

The system design of CertiSense AI follows a layered architectural approach that separates concerns across distinct functional layers, each responsible for a specific aspect of the platform's operation. The presentation layer, implemented using React with Tailwind CSS, is responsible for rendering role-specific user interfaces and managing user interactions across the four dashboards. The application layer, built on FastAPI with SQLAlchemy, handles all business logic, API endpoint management, authentication, file processing, and coordination between the blockchain and AI service components. The data layer, comprising SQLite for relational data storage and a file system for certificate document management, is responsible for the persistent storage and retrieval of all system data. The blockchain layer manages the immutable recording and verification of certificate hashes, while the AI layer provides content validation, confidence scoring, and natural language chatbot capabilities across all user roles.

The design of CertiSense AI is guided by several core principles that ensure the platform meets its stated objectives effectively. The principle of separation of concerns ensures that each component of the system is responsible for a clearly defined set of functionalities, reducing complexity and improving maintainability. The principle of role-based access control ensures that all system operations are governed by strict permission boundaries that prevent unauthorized access and protect sensitive data. The principle of modularity ensures that individual components such as the authentication service, blockchain service, AI validation service, and report generation service can be developed, tested, and updated independently without affecting the overall system. The principle of scalability ensures that the architecture can accommodate growing volumes of users, certificates, and verification requests without requiring fundamental redesign. The principle of security ensures that all data transmissions, user sessions, and stored records are protected through cryptographic mechanisms, token-based authentication, and input validation at every layer of the system.

The system design phase of CertiSense AI encompasses the development of several key design artifacts including the system architecture diagram, database schema design, entity relationship diagram, data flow diagrams, use case diagrams, and API endpoint specifications. These artifacts collectively provide a comprehensive and detailed representation of the system's structure, behavior, and data management strategy, serving as the authoritative reference for all implementation decisions made during the development phase. Together, they ensure that the final implemented system is consistent with the original design vision, meets all identified requirements, and delivers a reliable, secure, and user-friendly certificate verification platform for all stakeholders.

---

---

3.2	DATABASE DESIGN

---


Here is the Database Design section:

---

**3.2 Database Design**

Database design is the process of defining the logical and physical structure of the data storage system that underpins the application, including the identification of entities, attributes, relationships, constraints, and indexing strategies that collectively ensure efficient, reliable, and secure management of all system data. In CertiSense AI, the database is implemented using SQLite with SQLAlchemy as the Object Relational Mapper, providing a lightweight yet fully functional relational database solution that supports all the data management requirements of the platform across its four user roles and core functional modules.

---

**3.2.1 Database Entities and Tables**

The CertiSense AI database comprises six core entities that represent the primary data objects managed by the system. Each entity is mapped to a corresponding database table with clearly defined attributes, primary keys, foreign keys, and constraints that enforce data integrity and support the relational structure of the platform.

**1. Institute Table**
The Institute table stores all information related to registered educational institutions on the platform. Each institute record contains a unique system-generated UUID as the primary key, a human-readable institute identifier, the institution name, email address, hashed password, geographic location, approval status, and timestamps for record creation and last modification. The institute identifier serves as the prefix for all student IDs generated within that institution, establishing a direct and traceable link between students and their parent institution.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique system identifier |
| institute_id | String | Unique, Not Null | Human-readable institute code |
| name | String | Not Null | Institute name |
| email | String | Unique, Not Null | Login email address |
| password | String | Not Null | SHA-256 hashed password |
| location | String | Nullable | Geographic location |
| approval_status | String | Default: approved | Account approval status |
| created_at | DateTime | Not Null | Record creation timestamp |
| updated_at | DateTime | Nullable | Last modification timestamp |

**2. Student Table**
The Student table stores all information related to students registered by institutes on the platform. Each student record contains a unique UUID primary key, a system-generated student identifier formatted as the institute ID followed by a sequential number, the student name, email address, hashed password, and a foreign key reference to the parent institute. The student identifier is automatically generated during registration and serves as the primary login credential for student authentication.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique system identifier |
| student_id | String | Unique, Not Null | Auto-generated student code |
| name | String | Not Null | Student full name |
| email | String | Unique, Not Null | Student email address |
| password | String | Not Null | SHA-256 hashed password |
| institute_id | String (UUID) | Foreign Key | Reference to Institute table |
| created_at | DateTime | Not Null | Record creation timestamp |

**3. Verifier Table**
The Verifier table stores all information related to third-party verifiers registered on the platform, including employers, recruitment agencies, and regulatory bodies. Each verifier record contains a unique UUID primary key, username, email address, hashed password, company name, verifier type classification, account status, and a count of total verifications performed by that verifier.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique system identifier |
| username | String | Unique, Not Null | Login username |
| email | String | Unique, Not Null | Verifier email address |
| password | String | Not Null | SHA-256 hashed password |
| company_name | String | Nullable | Employer or organization name |
| verifier_type | String | Default: employer | Type of verifier |
| status | String | Default: active | Account status |
| verification_count | Integer | Default: 0 | Total verifications performed |
| created_at | DateTime | Not Null | Record creation timestamp |

**4. Certificate Table**
The Certificate table is the central entity of the CertiSense AI database, storing all information related to certificates issued by institutes to students. Each certificate record contains a unique certificate identifier, the original filename, the SHA-256 hash of the certificate file, the blockchain chain hash, references to the issuing institute and student, the certificate status, issue date, verification count, and timestamps. The hash field serves as the primary mechanism for certificate verification, enabling instant cross-referencing of uploaded files against the blockchain registry.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | String | Primary Key | Unique certificate identifier |
| name | String | Not Null | Original certificate filename |
| hash | String | Unique, Not Null | SHA-256 file hash |
| chain_hash | String | Nullable | Blockchain chain hash |
| student_id | String (UUID) | Foreign Key | Reference to Student table |
| institute_id | String (UUID) | Foreign Key | Reference to Institute table |
| issuer_id | String (UUID) | Foreign Key | Reference to issuing institute |
| status | Enum | Default: active | Certificate status |
| issue_date | DateTime | Not Null | Certificate issuance date |
| verification_count | Integer | Default: 0 | Total verification count |
| created_at | DateTime | Not Null | Record creation timestamp |

**5. Verification Table**
The Verification table maintains a complete and permanent audit trail of every certificate verification event performed on the platform. Each verification record stores the verification identifier, a reference to the verified certificate, the hash of the uploaded file, the verifier identity, the verification result, AI confidence score, blockchain integrity status, verification status classification, and a precise timestamp of the verification event.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique verification identifier |
| certificate_id | String | Foreign Key, Nullable | Reference to Certificate table |
| certificate_hash | String | Not Null | Hash of uploaded file |
| verifier_id | String (UUID) | Foreign Key | Reference to Verifier table |
| result | Boolean | Not Null | Verification outcome |
| confidence_score | Float | Nullable | AI confidence score |
| status | Enum | Not Null | Verification status |
| blockchain_integrity | Boolean | Default: False | Blockchain verification result |
| is_suspicious | Boolean | Default: False | Suspicious activity flag |
| timestamp | DateTime | Not Null | Verification timestamp |

**6. Feedback Table**
The Feedback table stores all feedback submissions made by verifiers through the platform, providing administrators with a structured record of reported issues, suspicious certificates, and general observations from the verification community. Each feedback record contains the feedback identifier, verifier reference, message content, category classification, priority level, status, flagged indicator, and submission timestamp.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | String (UUID) | Primary Key | Unique feedback identifier |
| verifier_id | String (UUID) | Foreign Key | Reference to Verifier table |
| message | String | Not Null | Feedback message content |
| category | String | Not Null | Feedback category type |
| priority | String | Default: medium | Priority level |
| status | String | Default: open | Feedback status |
| flagged | Boolean | Default: False | Administrative flag |
| timestamp | DateTime | Not Null | Submission timestamp |

---

**3.2.2 Entity Relationships**

The six database entities are connected through a set of clearly defined relationships that reflect the hierarchical and operational structure of the CertiSense AI platform:

- An **Institute** can have many **Students** — one-to-many relationship with cascade management
- An **Institute** can issue many **Certificates** — one-to-many relationship
- A **Student** can hold many **Certificates** — one-to-many relationship
- A **Certificate** can have many **Verifications** — one-to-many relationship
- A **Verifier** can perform many **Verifications** — one-to-many relationship
- A **Verifier** can submit many **Feedback** records — one-to-many relationship

---

**3.2.3 Database Design Principles**

The database design of CertiSense AI adheres to the following core principles that ensure data integrity, security, and performance:

- **Normalization:** All tables are designed to Third Normal Form to eliminate data redundancy and ensure consistency across all records
- **UUID Primary Keys:** System-generated UUIDs are used as primary keys across all tables to prevent enumeration attacks and ensure global uniqueness
- **Password Security:** All passwords are stored as SHA-256 hashes, ensuring that plaintext credentials are never persisted in the database
- **Referential Integrity:** Foreign key constraints enforce referential integrity across all related tables, preventing orphaned records and maintaining data consistency
- **Enum Constraints:** Certificate status and verification status fields use enumerated types to restrict values to predefined valid states, preventing invalid data entry
- **Timestamp Tracking:** Creation and modification timestamps are maintained across all entities to support audit trail requirements and chronological reporting
- **Indexing:** Unique constraints on hash, email, username, and student identifier fields provide implicit indexing that optimizes query performance for the most frequent lookup operations in the system

---

---

ENTITY-RELATIONSHIP MODEL

---


Here is the Entity-Relationship Model section:

---

**3.3 Entity-Relationship Model**

The Entity-Relationship Model of CertiSense AI provides a comprehensive visual and descriptive representation of the data entities, their attributes, and the relationships that exist between them within the database. The ER model serves as the foundational blueprint for the database design, capturing the structural and associative properties of all data objects managed by the system and ensuring that the database schema accurately reflects the real-world relationships between the stakeholders and operational entities of the certificate verification platform.

---

**3.3.1 Entities and Attributes**

The CertiSense AI ER model comprises six primary entities, each representing a distinct real-world object within the certificate verification ecosystem:

**1. INSTITUTE**
- **id** *(Primary Key)* — Unique UUID system identifier
- institute_id — Human-readable institute code
- name — Full name of the institution
- email — Registered email address
- password — SHA-256 hashed password
- location — Geographic location of the institute
- approval_status — Current approval state of the account
- created_at — Record creation timestamp
- updated_at — Last modification timestamp

**2. STUDENT**
- **id** *(Primary Key)* — Unique UUID system identifier
- student_id — Auto-generated student code
- name — Full name of the student
- email — Student email address
- password — SHA-256 hashed password
- *institute_id* *(Foreign Key → INSTITUTE)* — Parent institute reference
- created_at — Record creation timestamp

**3. VERIFIER**
- **id** *(Primary Key)* — Unique UUID system identifier
- username — Login username
- email — Registered email address
- password — SHA-256 hashed password
- company_name — Employer or organization name
- verifier_type — Classification of verifier type
- status — Current account status
- verification_count — Total verifications performed
- created_at — Record creation timestamp

**4. CERTIFICATE**
- **id** *(Primary Key)* — Unique certificate identifier
- name — Original certificate filename
- hash — SHA-256 cryptographic file hash
- chain_hash — Blockchain chain hash
- *student_id* *(Foreign Key → STUDENT)* — Certificate holder reference
- *institute_id* *(Foreign Key → INSTITUTE)* — Issuing institute reference
- *issuer_id* *(Foreign Key → INSTITUTE)* — Issuer reference
- status — Current certificate status
- issue_date — Date of certificate issuance
- verification_count — Total number of verifications
- created_at — Record creation timestamp

**5. VERIFICATION**
- **id** *(Primary Key)* — Unique UUID verification identifier
- *certificate_id* *(Foreign Key → CERTIFICATE)* — Verified certificate reference
- certificate_hash — Hash of the uploaded certificate file
- *verifier_id* *(Foreign Key → VERIFIER)* — Performing verifier reference
- result — Boolean verification outcome
- confidence_score — AI-generated confidence score
- status — Verification status classification
- blockchain_integrity — Blockchain verification result
- is_suspicious — Suspicious activity indicator
- timestamp — Precise verification timestamp

**6. FEEDBACK**
- **id** *(Primary Key)* — Unique UUID feedback identifier
- *verifier_id* *(Foreign Key → VERIFIER)* — Submitting verifier reference
- message — Feedback message content
- category — Feedback category classification
- priority — Priority level of the feedback
- status — Current feedback status
- flagged — Administrative flag indicator
- timestamp — Feedback submission timestamp

---

**3.3.2 Relationships**

The following relationships define the associations between the six entities in the CertiSense AI ER model:

**1. INSTITUTE — STUDENT (One-to-Many)**
- One institute can register and manage many students
- Each student belongs to exactly one institute
- The relationship is enforced through the institute_id foreign key in the STUDENT table
- Cardinality: 1 : N

**2. INSTITUTE — CERTIFICATE (One-to-Many)**
- One institute can issue many certificates to its students
- Each certificate is issued by exactly one institute
- The relationship is enforced through the institute_id foreign key in the CERTIFICATE table
- Cardinality: 1 : N

**3. STUDENT — CERTIFICATE (One-to-Many)**
- One student can hold many certificates issued by their institute
- Each certificate belongs to exactly one student
- The relationship is enforced through the student_id foreign key in the CERTIFICATE table
- Cardinality: 1 : N

**4. CERTIFICATE — VERIFICATION (One-to-Many)**
- One certificate can be verified many times by different verifiers
- Each verification event is associated with exactly one certificate
- The relationship is enforced through the certificate_id foreign key in the VERIFICATION table
- Cardinality: 1 : N

**5. VERIFIER — VERIFICATION (One-to-Many)**
- One verifier can perform many certificate verification events
- Each verification event is performed by exactly one verifier
- The relationship is enforced through the verifier_id foreign key in the VERIFICATION table
- Cardinality: 1 : N

**6. VERIFIER — FEEDBACK (One-to-Many)**
- One verifier can submit many feedback records to the platform
- Each feedback record is submitted by exactly one verifier
- The relationship is enforced through the verifier_id foreign key in the FEEDBACK table
- Cardinality: 1 : N

---

**3.3.3 ER Diagram Representation**

```
┌─────────────────┐         ┌─────────────────┐
│    INSTITUTE    │         │     STUDENT     │
│─────────────────│         │─────────────────│
│ PK id           │1      N │ PK id           │
│    institute_id │─────────│ FK institute_id │
│    name         │         │    student_id   │
│    email        │         │    name         │
│    password     │         │    email        │
│    location     │         │    password     │
│    approval_    │         │    created_at   │
│    status       │         └────────┬────────┘
│    created_at   │                  │
└────────┬────────┘                  │ 1
         │                           │
         │ 1                         │ N
         │                           │
         │         ┌─────────────────▼────────────────┐
         │         │           CERTIFICATE            │
         │         │──────────────────────────────────│
         └─────────│ PK id                            │
               N   │ FK student_id                    │
                   │ FK institute_id                  │
                   │ FK issuer_id                     │
                   │    name                          │
                   │    hash                          │
                   │    chain_hash                    │
                   │    status                        │
                   │    issue_date                    │
                   │    verification_count            │
                   │    created_at                    │
                   └─────────────┬────────────────────┘
                                 │ 1
                                 │
                                 │ N
                   ┌─────────────▼────────────────────┐
                   │           VERIFICATION           │
                   │──────────────────────────────────│
                   │ PK id                            │
                   │ FK certificate_id                │
                   │ FK verifier_id                   │
                   │    certificate_hash              │
                   │    result                        │
                   │    confidence_score              │
                   │    status                        │
                   │    blockchain_integrity          │
                   │    is_suspicious                 │
                   │    timestamp                     │
                   └─────────────▲────────────────────┘
                                 │ N
                                 │
                                 │ 1
                   ┌─────────────┴────────────────────┐
                   │            VERIFIER              │
                   │──────────────────────────────────│
                   │ PK id                            │
                   │    username                      │
                   │    email                         │
                   │    password                      │
                   │    company_name                  │
                   │    verifier_type                 │
                   │    status                        │
                   │    verification_count            │
                   │    created_at                    │
                   └─────────────┬────────────────────┘
                                 │ 1
                                 │
                                 │ N
                   ┌─────────────▼────────────────────┐
                   │            FEEDBACK              │
                   │──────────────────────────────────│
                   │ PK id                            │
                   │ FK verifier_id                   │
                   │    message                       │
                   │    category                      │
                   │    priority                      │
                   │    status                        │
                   │    flagged                       │
                   │    timestamp                     │
                   └──────────────────────────────────┘
```

---

**3.3.4 ER Model Summary**

| Relationship | Entity 1 | Entity 2 | Cardinality | Foreign Key |
|-------------|----------|----------|-------------|-------------|
| Registers | INSTITUTE | STUDENT | 1 : N | student.institute_id |
| Issues | INSTITUTE | CERTIFICATE | 1 : N | certificate.institute_id |
| Holds | STUDENT | CERTIFICATE | 1 : N | certificate.student_id |
| Verified By | CERTIFICATE | VERIFICATION | 1 : N | verification.certificate_id |
| Performs | VERIFIER | VERIFICATION | 1 : N | verification.verifier_id |
| Submits | VERIFIER | FEEDBACK | 1 : N | feedback.verifier_id |

The Entity-Relationship Model of CertiSense AI accurately captures the complete data structure and associative relationships of the platform, providing a clear and comprehensive foundation for the database implementation and ensuring that all data management requirements of the certificate verification ecosystem are fully represented and enforced at the database level.

---

---

3.3.1 DATA DICTIONARY

---


Here is the Data Dictionary section:

---

**3.3.1 Data Dictionary**

A data dictionary is a centralized repository of information about the data elements, attributes, data types, constraints, and descriptions of all entities within the system database. It serves as the authoritative reference document for developers, database administrators, and system analysts, providing a precise and comprehensive definition of every field stored in the CertiSense AI database to ensure consistency, clarity, and accuracy throughout the development and maintenance lifecycle of the platform.

---

**Table 1: INSTITUTE**

| Field Name | Data Type | Size | Constraints | Default | Description |
|------------|-----------|------|-------------|---------|-------------|
| id | VARCHAR | 36 | Primary Key, Not Null | UUID | Unique system-generated identifier for each institute |
| institute_id | VARCHAR | 20 | Unique, Not Null | — | Human-readable institute code used as prefix for student IDs |
| name | VARCHAR | 255 | Not Null | — | Full registered name of the educational institution |
| email | VARCHAR | 255 | Unique, Not Null | — | Official email address used for institute login authentication |
| password | VARCHAR | 255 | Not Null | — | SHA-256 hashed password for secure account authentication |
| location | VARCHAR | 255 | Nullable | NULL | Geographic location or address of the institute |
| approval_status | VARCHAR | 20 | Not Null | approved | Current approval state of the institute account on the platform |
| created_at | DATETIME | — | Not Null | Current Time | Timestamp recording when the institute account was created |
| updated_at | DATETIME | — | Nullable | NULL | Timestamp recording the most recent modification to the record |

---

**Table 2: STUDENT**

| Field Name | Data Type | Size | Constraints | Default | Description |
|------------|-----------|------|-------------|---------|-------------|
| id | VARCHAR | 36 | Primary Key, Not Null | UUID | Unique system-generated identifier for each student |
| student_id | VARCHAR | 30 | Unique, Not Null | Auto-generated | System-generated student code formatted as INSTXXXXX-XXXXX |
| name | VARCHAR | 255 | Not Null | — | Full name of the registered student |
| email | VARCHAR | 255 | Unique, Not Null | — | Student email address used for communication and identification |
| password | VARCHAR | 255 | Not Null | — | SHA-256 hashed password for secure student authentication |
| institute_id | VARCHAR | 36 | Foreign Key, Not Null | — | Reference to the parent institute that registered the student |
| created_at | DATETIME | — | Not Null | Current Time | Timestamp recording when the student account was created |

---

**Table 3: VERIFIER**

| Field Name | Data Type | Size | Constraints | Default | Description |
|------------|-----------|------|-------------|---------|-------------|
| id | VARCHAR | 36 | Primary Key, Not Null | UUID | Unique system-generated identifier for each verifier |
| username | VARCHAR | 100 | Unique, Not Null | — | Login username chosen by the verifier during registration |
| email | VARCHAR | 255 | Unique, Not Null | — | Registered email address of the verifier |
| password | VARCHAR | 255 | Not Null | — | SHA-256 hashed password for secure verifier authentication |
| company_name | VARCHAR | 255 | Nullable | NULL | Name of the employer or organization the verifier represents |
| verifier_type | VARCHAR | 50 | Not Null | employer | Classification of the verifier as employer, organization, or recruiter |
| status | VARCHAR | 20 | Not Null | active | Current operational status of the verifier account |
| verification_count | INTEGER | — | Not Null | 0 | Running total of all verification events performed by the verifier |
| created_at | DATETIME | — | Not Null | Current Time | Timestamp recording when the verifier account was created |

---

**Table 4: CERTIFICATE**

| Field Name | Data Type | Size | Constraints | Default | Description |
|------------|-----------|------|-------------|---------|-------------|
| id | VARCHAR | 30 | Primary Key, Not Null | — | Unique certificate identifier formatted as CERT-XXXXXXXXXXXX |
| name | VARCHAR | 255 | Not Null | — | Original filename of the uploaded certificate document |
| hash | VARCHAR | 64 | Unique, Not Null | — | SHA-256 cryptographic hash of the certificate file content |
| chain_hash | VARCHAR | 255 | Nullable | NULL | Blockchain chain hash linking the certificate to the ledger |
| student_id | VARCHAR | 36 | Foreign Key, Not Null | — | Reference to the student who holds the certificate |
| institute_id | VARCHAR | 36 | Foreign Key, Not Null | — | Reference to the institute that issued the certificate |
| issuer_id | VARCHAR | 36 | Foreign Key, Not Null | — | Reference to the specific issuer within the institute |
| status | ENUM | — | Not Null | active | Current status of the certificate: active, revoked, or suspicious |
| issue_date | DATETIME | — | Not Null | Current Time | Date and time when the certificate was officially issued |
| verification_count | INTEGER | — | Not Null | 0 | Running total of all verification events for this certificate |
| created_at | DATETIME | — | Not Null | Current Time | Timestamp recording when the certificate record was created |

---

**Table 5: VERIFICATION**

| Field Name | Data Type | Size | Constraints | Default | Description |
|------------|-----------|------|-------------|---------|-------------|
| id | VARCHAR | 36 | Primary Key, Not Null | UUID | Unique system-generated identifier for each verification event |
| certificate_id | VARCHAR | 30 | Foreign Key, Nullable | NULL | Reference to the certificate that was verified, null if not found |
| certificate_hash | VARCHAR | 64 | Not Null | — | SHA-256 hash of the certificate file uploaded by the verifier |
| verifier_id | VARCHAR | 36 | Foreign Key, Not Null | — | Reference to the verifier who performed the verification |
| result | BOOLEAN | — | Not Null | — | Outcome of the verification: True for valid, False for invalid |
| confidence_score | FLOAT | — | Nullable | NULL | AI-generated confidence score between 0.0 and 1.0 |
| status | ENUM | — | Not Null | — | Verification status classification: valid, invalid, or tampered |
| blockchain_integrity | BOOLEAN | — | Not Null | False | Result of the blockchain integrity check for the certificate |
| is_suspicious | BOOLEAN | — | Not Null | False | Flag indicating whether the verification was marked as suspicious |
| timestamp | DATETIME | — | Not Null | Current Time | Precise date and time when the verification event occurred |

---

**Table 6: FEEDBACK**

| Field Name | Data Type | Size | Constraints | Default | Description |
|------------|-----------|------|-------------|---------|-------------|
| id | VARCHAR | 36 | Primary Key, Not Null | UUID | Unique system-generated identifier for each feedback record |
| verifier_id | VARCHAR | 36 | Foreign Key, Not Null | — | Reference to the verifier who submitted the feedback |
| message | TEXT | — | Not Null | — | Full text content of the feedback message submitted by the verifier |
| category | VARCHAR | 50 | Not Null | — | Classification of feedback type: suspicious, issue, or general |
| priority | VARCHAR | 20 | Not Null | medium | Priority level assigned to the feedback: low, medium, or high |
| status | VARCHAR | 20 | Not Null | open | Current processing status of the feedback: open or resolved |
| flagged | BOOLEAN | — | Not Null | False | Administrative flag indicating feedback requires urgent attention |
| timestamp | DATETIME | — | Not Null | Current Time | Date and time when the feedback was submitted to the platform |

---

**Data Dictionary Summary**

| Table | Total Fields | Primary Key | Foreign Keys | Unique Fields |
|-------|-------------|-------------|--------------|---------------|
| INSTITUTE | 9 | id | — | institute_id, email |
| STUDENT | 7 | id | institute_id | student_id, email |
| VERIFIER | 9 | id | — | username, email |
| CERTIFICATE | 11 | id | student_id, institute_id, issuer_id | hash |
| VERIFICATION | 10 | id | certificate_id, verifier_id | — |
| FEEDBACK | 8 | id | verifier_id | — |

**Data Type Reference**

| Data Type | Description |
|-----------|-------------|
| VARCHAR | Variable-length character string with defined maximum size |
| TEXT | Variable-length character string with no defined maximum size |
| INTEGER | Whole number value without decimal places |
| FLOAT | Floating-point number value with decimal precision |
| BOOLEAN | Binary value representing True or False states |
| DATETIME | Date and time value stored in ISO 8601 format |
| ENUM | Restricted string value limited to a predefined set of valid options |
| UUID | Universally unique identifier generated automatically by the system |

---

---

3.4 OBJECT-ORIENTED DESIGN – UML DIAGRAMS

---


Here is the UML Diagrams section:

---

**3.4 Object-Oriented Design – UML Diagrams**

Unified Modeling Language diagrams provide a standardized visual representation of the structural and behavioral aspects of the CertiSense AI system, enabling developers, analysts, and stakeholders to understand the architecture, interactions, and workflows of the platform from multiple perspectives. The UML diagrams developed for CertiSense AI include the Use Case Diagram, Class Diagram, Sequence Diagram, and Activity Diagram, each capturing a distinct dimension of the system design.

---

**3.4.1 Use Case Diagram**

The Use Case Diagram illustrates the functional interactions between the four user roles and the core system functionalities of CertiSense AI, defining the boundaries of the system and the actions available to each actor.

**Actors:**
- **Admin** — System administrator responsible for platform management
- **Institute** — Educational institution responsible for student and certificate management
- **Student** — Certificate holder who tracks and manages their credentials
- **Verifier** — Third-party entity responsible for certificate authentication

**Use Cases:**

```
                    ┌─────────────────────────────────────────────────────┐
                    │                  CertiSense AI System               │
                    │                                                     │
┌─────────┐         │  ┌─────────────────┐   ┌─────────────────┐        │
│         │─────────│─▶│   Login/Logout  │   │  View Dashboard │        │
│  ADMIN  │         │  └─────────────────┘   └─────────────────┘        │
│         │─────────│─▶┌─────────────────┐   ┌─────────────────┐        │
└─────────┘         │  │Manage Institutes│   │ Generate Reports│        │
                    │  └─────────────────┘   └─────────────────┘        │
                    │  ┌─────────────────┐   ┌─────────────────┐        │
                    │  │ Manage Verifiers│   │  Monitor System │        │
                    │  └─────────────────┘   └─────────────────┘        │
                    │                                                     │
┌─────────┐         │  ┌─────────────────┐   ┌─────────────────┐        │
│         │─────────│─▶│  Add Students   │   │Issue Certificate│        │
│INSTITUTE│         │  └─────────────────┘   └─────────────────┘        │
│         │─────────│─▶┌─────────────────┐   ┌─────────────────┐        │
└─────────┘         │  │ Manage Profile  │   │   AI Assistant  │        │
                    │  └─────────────────┘   └─────────────────┘        │
                    │                                                     │
┌─────────┐         │  ┌─────────────────┐   ┌─────────────────┐        │
│         │─────────│─▶│  View Profile   │   │View Certificates│        │
│ STUDENT │         │  └─────────────────┘   └─────────────────┘        │
│         │─────────│─▶┌─────────────────┐   ┌─────────────────┐        │
└─────────┘         │  │Download Cert    │   │  View Verifiers │        │
                    │  └─────────────────┘   └─────────────────┘        │
                    │                                                     │
┌─────────┐         │  ┌─────────────────┐   ┌─────────────────┐        │
│         │─────────│─▶│Verify Certificate│  │ Submit Feedback │        │
│VERIFIER │         │  └─────────────────┘   └─────────────────┘        │
│         │─────────│─▶┌─────────────────┐   ┌─────────────────┐        │
└─────────┘         │  │  View History   │   │   AI Assistant  │        │
                    │  └─────────────────┘   └─────────────────┘        │
                    └─────────────────────────────────────────────────────┘
```

---

**3.4.2 Class Diagram**

The Class Diagram represents the static structure of the CertiSense AI system, showing the core classes, their attributes, methods, and the relationships between them.

```
┌──────────────────────────────┐
│           Institute          │
│──────────────────────────────│
│ - id: String                 │
│ - institute_id: String       │
│ - name: String               │
│ - email: String              │
│ - password: String           │
│ - location: String           │
│ - approval_status: String    │
│ - created_at: DateTime       │
│──────────────────────────────│
│ + register(): Boolean        │
│ + login(): Token             │
│ + addStudent(): Boolean      │
│ + issueCertificate(): String │
│ + getDashboard(): Dict       │
│ + updateProfile(): Boolean   │
└──────────────┬───────────────┘
               │ 1
               │ has many
               │ N
┌──────────────▼───────────────┐        ┌──────────────────────────────┐
│           Student            │        │          Verifier            │
│──────────────────────────────│        │──────────────────────────────│
│ - id: String                 │        │ - id: String                 │
│ - student_id: String         │        │ - username: String           │
│ - name: String               │        │ - email: String              │
│ - email: String              │        │ - password: String           │
│ - password: String           │        │ - company_name: String       │
│ - institute_id: String       │        │ - verifier_type: String      │
│ - created_at: DateTime       │        │ - status: String             │
│──────────────────────────────│        │ - verification_count: Int    │
│ + login(): Token             │        │──────────────────────────────│
│ + getProfile(): Dict         │        │ + register(): Boolean        │
│ + updateProfile(): Boolean   │        │ + login(): Token             │
│ + getCertificates(): List    │        │ + verifyCertificate(): Dict  │
│ + downloadCertificate(): File│        │ + submitFeedback(): Boolean  │
└──────────────┬───────────────┘        │ + getHistory(): List        │
               │ 1                      └──────────────┬───────────────┘
               │ holds many                            │ 1
               │ N                                     │ performs many
┌──────────────▼───────────────┐                       │ N
│         Certificate          │        ┌──────────────▼───────────────┐
│──────────────────────────────│        │         Verification         │
│ - id: String                 │        │──────────────────────────────│
│ - name: String               │        │ - id: String                 │
│ - hash: String               │        │ - certificate_id: String     │
│ - chain_hash: String         │        │ - certificate_hash: String   │
│ - student_id: String         │        │ - verifier_id: String        │
│ - institute_id: String       │        │ - result: Boolean            │
│ - status: Enum               │        │ - confidence_score: Float    │
│ - issue_date: DateTime       │        │ - status: Enum               │
│ - verification_count: Int    │        │ - blockchain_integrity: Bool │
│──────────────────────────────│        │ - is_suspicious: Boolean     │
│ + generateHash(): String     │        │ - timestamp: DateTime        │
│ + storeOnBlockchain(): String│        │──────────────────────────────│
│ + getDetails(): Dict         │        │ + recordVerification(): Bool │
│ + updateStatus(): Boolean    │        │ + flagSuspicious(): Boolean  │
│ + incrementVerification():  │        │ + getResult(): Dict          │
└──────────────┬───────────────┘        └──────────────────────────────┘
               │ 1
               │ verified by many
               │ N
               │
┌──────────────▼───────────────┐        ┌──────────────────────────────┐
│       BlockchainService      │        │       AIValidationService    │
│──────────────────────────────│        │──────────────────────────────│
│ - chain: List                │        │ - model: LLM                 │
│ - blockchain_name: String    │        │ - confidence_threshold: Float│
│──────────────────────────────│        │──────────────────────────────│
│ + storeCertificateHash()     │        │ + validateContent(): Dict    │
│ + verifyCertificateHash()    │        │ + computeConfidence(): Float │
│ + getCertificateChain()      │        │ + generateExplanation(): Str │
│ + addVerification()          │        │ + detectAnomalies(): Boolean │
│ + generateFileHash()         │        │ + processQuery(): String     │
└──────────────────────────────┘        └──────────────────────────────┘
```

---

**3.4.3 Sequence Diagram**

The Sequence Diagrams illustrate the chronological interactions between system components for the two most critical workflows in CertiSense AI.

**Sequence Diagram 1: Certificate Issuance**

```
Institute    Frontend    Backend API    AI Service    Blockchain    Database
    │            │            │              │             │            │
    │──Login────▶│            │              │             │            │
    │            │──POST /auth/institute/login──▶          │            │
    │            │◀──JWT Token─────────────────            │            │
    │            │            │              │             │            │
    │─Upload─────▶            │              │             │            │
    │ Certificate│            │              │             │            │
    │            │──POST /institute/certificates──▶        │            │
    │            │            │──validateContent()──▶      │            │
    │            │            │◀──AI Result──────────      │            │
    │            │            │              │             │            │
    │            │            │──generateHash()            │            │
    │            │            │              │             │            │
    │            │            │──storeCertificateHash()───▶│            │
    │            │            │◀──chain_hash───────────────│            │
    │            │            │              │             │            │
    │            │            │──saveCertificate()────────────────────▶│
    │            │            │◀──Certificate Record──────────────────│
    │            │            │              │             │            │
    │            │◀──Success Response──────────            │            │
    │◀──Certificate ID─────────            │             │            │
```

**Sequence Diagram 2: Certificate Verification**

```
Verifier     Frontend    Backend API    AI Service    Blockchain    Database
    │            │            │              │             │            │
    │──Login─────▶            │              │             │            │
    │            │──POST /auth/verifier/login──▶           │            │
    │            │◀──JWT Token──────────────────           │            │
    │            │            │              │             │            │
    │─Upload─────▶            │              │             │            │
    │ Certificate│            │              │             │            │
    │            │──POST /verifier/verify──▶ │             │            │
    │            │            │──generateHash()            │            │
    │            │            │              │             │            │
    │            │            │──queryCertificate()───────────────────▶│
    │            │            │◀──Certificate Record──────────────────│
    │            │            │              │             │            │
    │            │            │──validateContent()──▶      │            │
    │            │            │◀──Confidence Score───      │            │
    │            │            │              │             │            │
    │            │            │──verifyHash()─────────────▶│            │
    │            │            │◀──Blockchain Result────────│            │
    │            │            │              │             │            │
    │            │            │──saveVerification()───────────────────▶│
    │            │            │◀──Verification Record─────────────────│
    │            │            │              │             │            │
    │            │◀──Verification Result───────            │            │
    │◀──Valid/Invalid──────────            │             │            │
```

---

**3.4.4 Activity Diagram**

The Activity Diagrams illustrate the step-by-step workflows for the primary operational processes in CertiSense AI.

**Activity Diagram 1: Certificate Issuance Workflow**

```
        ┌─────────────────┐
        │      START      │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Institute Login │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Select Student  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Upload Certificate│
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  AI Validation  │
        └────────┬────────┘
                 │
         ┌───────▼────────┐
         │  Valid Content? │
         └───┬────────┬───┘
             │ NO     │ YES
    ┌────────▼──┐  ┌──▼─────────────┐
    │  Reject   │  │ Generate SHA256 │
    │Certificate│  │     Hash       │
    └───────────┘  └──────┬─────────┘
                          │
                 ┌────────▼────────┐
                 │Store on Blockchain│
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │  Save to Database│
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │ Return Certificate│
                 │    ID and Hash  │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │      END        │
                 └─────────────────┘
```

**Activity Diagram 2: Certificate Verification Workflow**

```
        ┌─────────────────┐
        │      START      │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Verifier Login  │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │Upload Certificate│
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │Generate SHA256  │
        │     Hash        │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │Query Database   │
        │  for Hash Match │
        └────────┬────────┘
                 │
         ┌───────▼────────┐
         │  Hash Found?   │
         └───┬────────┬───┘
             │ NO     │ YES
    ┌────────▼──┐  ┌──▼─────────────┐
    │  Mark as  │  │  AI Validation  │
    │  Invalid  │  │    Analysis    │
    └─────┬─────┘  └──────┬─────────┘
          │               │
          │      ┌────────▼────────┐
          │      │Blockchain Verify│
          │      └────────┬────────┘
          │               │
          │      ┌────────▼────────┐
          │      │  Mark as Valid  │
          │      └────────┬────────┘
          │               │
          └───────┬────────┘
                  │
        ┌─────────▼───────┐
        │Save Verification │
        │    Record       │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Return Result to │
        │    Verifier     │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │      END        │
        └─────────────────┘
```

---

**3.4.5 UML Diagram Summary**

| Diagram Type | Purpose | Key Elements |
|-------------|---------|--------------|
| Use Case Diagram | Defines system boundaries and actor interactions | 4 Actors, 16 Use Cases |
| Class Diagram | Represents static structure and relationships | 8 Classes, 6 Relationships |
| Sequence Diagram 1 | Certificate issuance interaction flow | 6 Components, 12 Steps |
| Sequence Diagram 2 | Certificate verification interaction flow | 6 Components, 14 Steps |
| Activity Diagram 1 | Certificate issuance workflow | 10 Activities, 1 Decision |
| Activity Diagram 2 | Certificate verification workflow | 11 Activities, 2 Decisions |

The UML diagrams collectively provide a comprehensive and multi-dimensional representation of the CertiSense AI system design, capturing the functional scope, structural organization, behavioral interactions, and operational workflows of the platform in a standardized and universally understood visual format that supports both development implementation and stakeholder communication throughout the project lifecycle.

---

---

Activity Diagram:

---


Here is a detailed Activity Diagram section:

---

**3.4.4 Activity Diagrams**

Activity Diagrams represent the dynamic behavioral aspects of the CertiSense AI system by illustrating the step-by-step flow of activities, decision points, parallel processes, and termination conditions for each major operational workflow within the platform. The following activity diagrams cover all four primary user role workflows.

---

**Activity Diagram 1: Admin Workflow**

```
        ┌──────────────────┐
        │      START       │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │   Access Login   │
        │      Page        │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │  Enter Admin     │
        │  Credentials     │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Validate JWT     │
        │    Token         │
        └────────┬─────────┘
                 │
         ┌───────▼────────┐
         │ Credentials    │
         │   Valid?       │
         └───┬────────┬───┘
         NO  │        │ YES
    ┌────────▼──┐  ┌──▼──────────────┐
    │   Show    │  │  Load Admin     │
    │   Error   │  │   Dashboard     │
    └───────────┘  └──────┬──────────┘
                          │
              ┌───────────▼───────────┐
              │   Select Module       │
              └──┬──┬──┬──┬──┬───┬───┘
                 │  │  │  │  │   │
        ┌────────▼┐ │ ┌▼──┐ │ ┌──▼────┐
        │ Manage  │ │ │Ana│ │ │Manage │
        │Institute│ │ │lyt│ │ │Verify │
        └────┬────┘ │ │ics│ │ └───┬───┘
             │      │ └─┬─┘ │     │
        ┌────▼────┐ │   │   │ ┌───▼───┐
        │Add/Edit/│ │   │   │ │Flag / │
        │ Delete  │ │   │   │ │Monitor│
        └────┬────┘ │   │   │ └───┬───┘
             │      │   │   │     │
        ┌────▼──────▼───▼───▼─────▼────┐
        │     View Results / Reports   │
        └──────────────┬───────────────┘
                       │
              ┌────────▼────────┐
              │  Continue or    │
              │    Logout?      │
              └───┬─────────┬───┘
              YES │         │ NO
        ┌─────────▼──┐  ┌───▼──────────┐
        │  Return to  │  │   Logout     │
        │  Dashboard  │  │Clear Session │
        └─────────────┘  └──────┬───────┘
                                │
                       ┌────────▼────────┐
                       │      END        │
                       └─────────────────┘
```

---

**Activity Diagram 2: Institute Workflow**

```
        ┌──────────────────┐
        │      START       │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │Register/Login as │
        │    Institute     │
        └────────┬─────────┘
                 │
         ┌───────▼────────┐
         │ Authenticated? │
         └───┬────────┬───┘
         NO  │        │ YES
    ┌────────▼──┐  ┌──▼──────────────┐
    │   Show    │  │  Load Institute │
    │   Error   │  │   Dashboard     │
    └───────────┘  └──────┬──────────┘
                          │
              ┌───────────▼───────────┐
              │     Select Action     │
              └──┬──────────┬─────────┘
                 │          │
        ┌────────▼───┐  ┌───▼──────────┐
        │  Add New   │  │    Issue     │
        │  Student   │  │ Certificate  │
        └─────┬──────┘  └──────┬───────┘
              │                │
        ┌─────▼──────┐  ┌──────▼───────┐
        │Enter Student│  │Select Student│
        │  Details   │  │Upload File   │
        └─────┬──────┘  └──────┬───────┘
              │                │
        ┌─────▼──────┐  ┌──────▼───────┐
        │ Validate   │  │  AI Content  │
        │   Data     │  │  Validation  │
        └─────┬──────┘  └──────┬───────┘
              │                │
         ┌────▼───┐      ┌─────▼──────┐
         │ Valid? │      │  Valid PDF? │
         └──┬──┬──┘      └──┬──────┬──┘
         NO │  │ YES      NO │      │ YES
    ┌───────▼┐ │      ┌─────▼─┐ ┌──▼──────────┐
    │ Show   │ │      │Reject │ │Generate Hash│
    │ Error  │ │      │ File  │ │& Store Chain│
    └────────┘ │      └───────┘ └──────┬───────┘
               │                       │
        ┌──────▼──────┐        ┌────────▼────────┐
        │Register     │        │ Save Certificate │
        │Student &    │        │  to Database    │
        │Generate ID  │        └────────┬────────┘
        └──────┬──────┘                 │
               │                ┌───────▼────────┐
               └────────────────▶  View Dashboard │
                                │   Analytics    │
                                └───────┬────────┘
                                        │
                                ┌───────▼────────┐
                                │     Logout     │
                                └───────┬────────┘
                                        │
                                ┌───────▼────────┐
                                │      END       │
                                └────────────────┘
```

---

**Activity Diagram 3: Student Workflow**

```
        ┌──────────────────┐
        │      START       │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │  Login with      │
        │  Student ID      │
        └────────┬─────────┘
                 │
         ┌───────▼────────┐
         │ Authenticated? │
         └───┬────────┬───┘
         NO  │        │ YES
    ┌────────▼──┐  ┌──▼──────────────┐
    │   Show    │  │  Load Student   │
    │   Error   │  │   Dashboard     │
    └───────────┘  └──────┬──────────┘
                          │
              ┌───────────▼───────────┐
              │     Select Action     │
              └──┬──────────┬─────────┘
                 │          │
        ┌────────▼───┐  ┌───▼──────────┐
        │    View    │  │     View     │
        │  Profile   │  │Certificates  │
        └─────┬──────┘  └──────┬───────┘
              │                │
        ┌─────▼──────┐  ┌──────▼───────┐
        │   Edit     │  │  Select a    │
        │  Profile?  │  │ Certificate  │
        └─────┬──────┘  └──────┬───────┘
              │                │
         ┌────▼───┐    ┌───────▼──────┐
         │ YES/NO │    │  View Details│
         └──┬──┬──┘    │  Hash/Chain  │
         YES│  │NO     └──────┬───────┘
    ┌───────▼┐ │              │
    │Update  │ │       ┌──────▼───────┐
    │Profile │ │       │  Download    │
    │& Save  │ │       │ Certificate? │
    └───┬────┘ │       └──┬───────┬───┘
        │      │       YES│       │NO
        │      │   ┌──────▼──┐    │
        │      │   │Download │    │
        │      │   │   PDF   │    │
        │      │   └────┬────┘    │
        │      │        │         │
        └──────┴────────┴─────────┘
                        │
               ┌────────▼────────┐
               │ Continue or     │
               │    Logout?      │
               └───┬─────────┬───┘
               YES │         │ NO
         ┌─────────▼──┐  ┌───▼──────────┐
         │  Return to  │  │   Logout     │
         │  Dashboard  │  │Clear Session │
         └─────────────┘  └──────┬───────┘
                                 │
                        ┌────────▼────────┐
                        │      END        │
                        └─────────────────┘
```

---

**Activity Diagram 4: Verifier Workflow**

```
        ┌──────────────────┐
        │      START       │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │Register/Login as │
        │    Verifier      │
        └────────┬─────────┘
                 │
         ┌───────▼────────┐
         │ Authenticated? │
         └───┬────────┬───┘
         NO  │        │ YES
    ┌────────▼──┐  ┌──▼──────────────┐
    │   Show    │  │  Load Verifier  │
    │   Error   │  │   Dashboard     │
    └───────────┘  └──────┬──────────┘
                          │
              ┌───────────▼───────────┐
              │     Select Action     │
              └──┬──────┬──────┬──────┘
                 │      │      │
        ┌────────▼──┐ ┌─▼────┐ ┌▼──────────┐
        │  Verify   │ │View  │ │  Submit   │
        │Certificate│ │History│ │ Feedback  │
        └─────┬─────┘ └──┬───┘ └─────┬─────┘
              │          │           │
        ┌─────▼──────┐   │     ┌─────▼──────┐
        │Upload Cert │   │     │Fill Feedback│
        │   File     │   │     │    Form    │
        └─────┬──────┘   │     └─────┬──────┘
              │          │           │
        ┌─────▼──────┐   │     ┌─────▼──────┐
        │Generate    │   │     │  Submit to  │
        │SHA256 Hash │   │     │   Admin    │
        └─────┬──────┘   │     └─────┬──────┘
              │          │           │
        ┌─────▼──────┐   │           │
        │Match Hash  │   │           │
        │in Database │   │           │
        └─────┬──────┘   │           │
              │          │           │
         ┌────▼───┐      │           │
         │ Found? │      │           │
         └──┬──┬──┘      │           │
         NO │  │ YES     │           │
    ┌───────▼┐ │         │           │
    │ Return │ │         │           │
    │Invalid │ │         │           │
    └───┬────┘ │         │           │
        │   ┌──▼──────┐  │           │
        │   │AI Verify│  │           │
        │   │& Score  │  │           │
        │   └──┬──────┘  │           │
        │      │         │           │
        │   ┌──▼──────┐  │           │
        │   │Blockchain│  │           │
        │   │ Verify  │  │           │
        │   └──┬──────┘  │           │
        │      │         │           │
        │   ┌──▼──────┐  │           │
        │   │ Return  │  │           │
        │   │  Valid  │  │           │
        │   └──┬──────┘  │           │
        │      │         │           │
        └──────┴─────────┴───────────┘
                         │
                ┌────────▼────────┐
                │ Save Verification│
                │    Record       │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │ Continue or     │
                │    Logout?      │
                └───┬─────────┬───┘
                YES │         │ NO
          ┌─────────▼──┐  ┌───▼──────────┐
          │  Return to  │  │   Logout     │
          │  Dashboard  │  │Clear Session │
          └─────────────┘  └──────┬───────┘
                                  │
                         ┌────────▼────────┐
                         │      END        │
                         └─────────────────┘
```

---

**Activity Diagram Summary**

| Diagram | Actor | Key Activities | Decision Points |
|---------|-------|---------------|-----------------|
| Admin Workflow | Administrator | Login, Manage Institutes, Monitor Verifications, Generate Reports | Credential Validation, Module Selection |
| Institute Workflow | Institute | Login, Add Students, Issue Certificates, View Analytics | Authentication, AI Content Validation |
| Student Workflow | Student | Login, View Profile, Track Certificates, Download Files | Authentication, Edit Profile, Download |
| Verifier Workflow | Verifier | Login, Verify Certificate, View History, Submit Feedback | Authentication, Hash Match, Valid/Invalid |

---

---

Sequence Diagram:

---


Here is a detailed Sequence Diagram section:

---

**3.4.3 Sequence Diagrams**

Sequence Diagrams illustrate the chronological order of interactions and message exchanges between system components, objects, and actors for each primary workflow in CertiSense AI. They capture the dynamic behavior of the system by showing how requests flow from the user interface through the backend services, database, blockchain, and AI components, and how responses are returned to the user at each stage of the process.

---

**Sequence Diagram 1: Admin Login and Dashboard Access**

```
Admin       Browser      Frontend     Backend API    Database
  │            │             │              │             │
  │──Open App─▶│             │              │             │
  │            │──Load Page─▶│              │             │
  │            │◀──Login Form│              │             │
  │            │             │              │             │
  │─Enter─────▶│             │              │             │
  │ Credentials│             │              │             │
  │            │──Submit────▶│              │             │
  │            │             │──POST /auth/admin/login───▶│
  │            │             │              │──Query User─▶
  │            │             │              │◀──User Data──
  │            │             │              │             │
  │            │             │              │──Verify Hash│
  │            │             │              │──Generate JWT
  │            │             │◀──JWT Token──│             │
  │            │◀──Store Token│             │             │
  │            │             │              │             │
  │            │──Load Admin─▶             │             │
  │            │   Dashboard │              │             │
  │            │             │──GET /admin/analytics────▶│
  │            │             │              │◀──Analytics──
  │            │             │◀──Dashboard Data──────────│
  │            │◀──Render────│              │             │
  │◀──Dashboard│             │              │             │
```

---

**Sequence Diagram 2: Institute Registration and Login**

```
Institute   Browser      Frontend     Backend API    Database
  │            │             │              │             │
  │──Register─▶│             │              │             │
  │            │──Load Form─▶│              │             │
  │            │◀──Register  │              │             │
  │            │   Form      │              │             │
  │            │             │              │             │
  │─Fill Form─▶│             │              │             │
  │            │──Submit────▶│              │             │
  │            │             │──POST /auth/institute/register─▶
  │            │             │              │──Check Email│
  │            │             │              │◀──Not Found─│
  │            │             │              │──Hash Password
  │            │             │              │──Generate ID│
  │            │             │              │──Save Record▶
  │            │             │              │◀──Success───│
  │            │             │◀──Registered─│             │
  │            │◀──Success───│              │             │
  │            │             │              │             │
  │──Login────▶│             │              │             │
  │            │──Submit────▶│              │             │
  │            │             │──POST /auth/institute/login─▶
  │            │             │              │──Query User─▶
  │            │             │              │◀──User Data──
  │            │             │              │──Verify Hash│
  │            │             │              │──Generate JWT
  │            │             │◀──JWT Token──│             │
  │            │◀──Dashboard─│              │             │
  │◀──Institute│             │              │             │
  │  Dashboard │             │              │             │
```

---

**Sequence Diagram 3: Student Registration by Institute**

```
Institute   Frontend     Backend API    Database     Auth Service
  │             │              │             │             │
  │─Add Student▶│              │             │             │
  │             │──POST /institute/students─▶│             │
  │             │              │──Verify JWT─────────────▶│
  │             │              │◀──Valid Token────────────│
  │             │              │             │             │
  │             │              │──Check Institute Ownership
  │             │              │──▶Query Institute────────▶
  │             │              │◀──Institute Data──────────
  │             │              │             │             │
  │             │              │──Generate Student ID      │
  │             │              │──Hash Password            │
  │             │              │──Save Student────────────▶│
  │             │              │◀──Student Record──────────│
  │             │◀──Student ID─│             │             │
  │◀──Success + │              │             │             │
  │  Student ID │              │             │             │
```

---

**Sequence Diagram 4: Certificate Issuance**

```
Institute  Frontend  Backend API  AI Service  Blockchain  Database
  │           │           │            │            │          │
  │─Upload───▶│           │            │            │          │
  │ Certificate           │            │            │          │
  │           │──POST /institute/certificates──────▶│          │
  │           │           │──Verify JWT│            │          │
  │           │           │──Read File │            │          │
  │           │           │──generateHash()         │          │
  │           │           │            │            │          │
  │           │           │──validateContent()─────▶│          │
  │           │           │            │──Analyze───│          │
  │           │           │            │  Content   │          │
  │           │           │◀──AI Result│            │          │
  │           │           │            │            │          │
  │           │    ┌──────▼──────┐     │            │          │
  │           │    │  Valid PDF? │     │            │          │
  │           │    └──┬───────┬──┘     │            │          │
  │           │    NO │       │ YES    │            │          │
  │           │◀─Error│       │        │            │          │
  │           │       │       │        │            │          │
  │           │       │──storeCertificateHash()────▶│          │
  │           │       │       │        │◀──chain_hash│         │
  │           │       │       │        │            │          │
  │           │       │──Check Duplicate Hash──────────────────▶
  │           │       │       │        │            │◀─Not Found
  │           │       │       │        │            │          │
  │           │       │──Save Certificate File      │          │
  │           │       │──Save Certificate Record───────────────▶
  │           │       │       │        │            │◀─Success──
  │           │◀──Certificate │        │            │          │
  │           │   ID + Hash   │        │            │          │
  │◀──Success─│               │        │            │          │
```

---

**Sequence Diagram 5: Certificate Verification**

```
Verifier  Frontend  Backend API  AI Service  Blockchain  Database
  │          │           │            │            │          │
  │─Upload──▶│           │            │            │          │
  │ Certificate          │            │            │          │
  │          │──POST /verifier/verify─────────────▶│          │
  │          │           │──Verify JWT│            │          │
  │          │           │──Read File │            │          │
  │          │           │──generateHash()         │          │
  │          │           │            │            │          │
  │          │           │──Query Certificate by Hash────────▶│
  │          │           │            │            │◀─Result───│
  │          │           │            │            │          │
  │          │    ┌──────▼──────┐     │            │          │
  │          │    │ Hash Found? │     │            │          │
  │          │    └──┬───────┬──┘     │            │          │
  │          │    NO │       │ YES    │            │          │
  │          │       │       │──validateContent()─▶│          │
  │          │       │       │        │◀─Confidence │         │
  │          │       │       │        │   Score    │          │
  │          │       │       │──verifyHash()──────▶│          │
  │          │       │       │        │◀─Blockchain │         │
  │          │       │       │        │   Result   │          │
  │          │       │       │──Get Student Details──────────▶│
  │          │       │       │        │            │◀─Details──│
  │          │       │       │──Get Institute Details─────────▶
  │          │       │       │        │            │◀─Details──│
  │          │       │       │──Update Verification Count─────▶
  │          │       │       │──Save Verification Record──────▶
  │          │       │       │        │            │◀─Success──│
  │          │◀─Invalid      │◀─Valid Result       │          │
  │          │  Result       │  + Details          │          │
  │◀─Result──│               │                     │          │
```

---

**Sequence Diagram 6: Student Certificate Tracking**

```
Student    Frontend     Backend API    Database     Blockchain
  │            │              │             │             │
  │──Login────▶│              │             │             │
  │            │──POST /auth/student/login─▶│             │
  │            │              │──Query User─▶             │
  │            │              │◀──User Data──             │
  │            │              │──Generate JWT             │
  │            │◀──JWT Token──│             │             │
  │            │              │             │             │
  │─View Certs▶│              │             │             │
  │            │──GET /student/certificates─▶             │
  │            │              │──Query Certs▶             │
  │            │              │◀──Cert List──             │
  │            │◀──Certificate│             │             │
  │            │   List       │             │             │
  │            │              │             │             │
  │─View Details▶             │             │             │
  │            │──GET /student/certificate/{hash}─────────▶
  │            │              │             │             │
  │            │              │──getCertificateChain()───▶│
  │            │              │◀──Chain Data──────────────│
  │            │◀──Hash/Chain │             │             │
  │            │   Details    │             │             │
  │            │              │             │             │
  │─Download──▶│              │             │             │
  │            │──GET /student/certificates/{id}/download─▶
  │            │              │──Query Cert─▶             │
  │            │              │◀──File Path──             │
  │            │              │──Read File  │             │
  │            │◀──PDF File───│             │             │
  │◀──Download─│              │             │             │
```

---

**Sequence Diagram 7: Verifier Feedback Submission**

```
Verifier   Frontend     Backend API    Database     Admin
  │            │              │             │          │
  │─Submit────▶│              │             │          │
  │ Feedback   │              │             │          │
  │            │──POST /verifier/feedback──▶│          │
  │            │              │──Verify JWT │          │
  │            │              │──Validate   │          │
  │            │              │   Form Data │          │
  │            │              │──Generate   │          │
  │            │              │   UUID      │          │
  │            │              │──Save Feedback────────▶│
  │            │              │◀──Success──────────────│
  │            │◀──Submitted──│             │          │
  │◀──Success──│              │             │          │
  │            │              │             │          │
  │            │              │             │──Notify──▶
  │            │              │             │  Admin   │
  │            │              │             │          │
  │─View───────▶              │             │          │
  │ Feedback   │              │             │          │
  │            │──GET /verifier/feedback───▶│          │
  │            │              │──Query Feedbacks──────▶│
  │            │              │◀──Feedback List────────│
  │            │◀──Feedback───│             │          │
  │◀──List─────│              │             │          │
```

---

**Sequence Diagram 8: Admin Report Generation**

```
Admin      Frontend     Backend API    Database    AI Service  FileSystem
  │            │              │             │           │           │
  │─Generate──▶│              │             │           │           │
  │ Report     │              │             │           │           │
  │            │──GET /admin/reports/{type}─▶           │           │
  │            │              │──Verify JWT │           │           │
  │            │              │──Query Analytics───────▶│           │
  │            │              │◀──System Data───────────│           │
  │            │              │             │           │           │
  │            │              │──Generate Chart─────────────────────▶
  │            │              │             │           │◀─Chart URL─│
  │            │              │             │           │           │
  │            │              │──processAdminQuery()───▶│           │
  │            │              │             │           │──Analyze───│
  │            │              │             │           │  Data      │
  │            │              │◀──AI Summary────────────│           │
  │            │              │             │           │           │
  │            │              │──Build Report Object    │           │
  │            │◀──Report Data│             │           │           │
  │            │   + Chart URL│             │           │           │
  │◀──Report───│              │             │           │           │
  │  Displayed │              │             │           │           │
```

---

**Sequence Diagram Summary**

| Diagram | Primary Actor | Key Interactions | Components Involved |
|---------|--------------|-----------------|---------------------|
| Admin Login | Administrator | Authentication, Dashboard Load | Frontend, Backend, Database |
| Institute Registration | Institute | Register, Login, Dashboard | Frontend, Backend, Database |
| Student Registration | Institute | Add Student, Generate ID | Frontend, Backend, Database |
| Certificate Issuance | Institute | Upload, AI Validate, Blockchain Store | Frontend, Backend, AI, Blockchain, Database |
| Certificate Verification | Verifier | Upload, Hash Match, AI Score, Blockchain | Frontend, Backend, AI, Blockchain, Database |
| Student Certificate Tracking | Student | View Certs, Details, Download | Frontend, Backend, Database, Blockchain |
| Feedback Submission | Verifier | Submit, Store, View Feedback | Frontend, Backend, Database |
| Report Generation | Administrator | Query, AI Analyze, Chart Generate | Frontend, Backend, AI, Database, FileSystem |

The sequence diagrams collectively provide a comprehensive and chronologically accurate representation of all primary system interactions in CertiSense AI, capturing the precise flow of messages, data, and responses between the user interface, backend services, AI components, blockchain layer, and database across every major operational workflow of the platform.

---

---

Compact chat history?

---

You stopped your current work, please provide additional examples or ask another question.

---

3.5	 MODULAR DESIGN

---


Here is the Modular Design section:

---

**3.5 Modular Design**

Modular design is a software engineering principle that involves decomposing a complex system into smaller, self-contained, and independently manageable units called modules, each responsible for a specific and well-defined set of functionalities. In CertiSense AI, the modular design approach ensures that the platform is organized into clearly separated functional components that can be developed, tested, maintained, and updated independently without affecting the overall system integrity. The modular architecture of CertiSense AI is structured across two primary layers — the frontend module layer and the backend module layer — with each layer comprising several distinct modules that collectively deliver the complete functionality of the certificate verification platform.

---

**3.5.1 Frontend Modules**

The frontend of CertiSense AI is built using React with Tailwind CSS and is organized into the following functional modules:

---

**Module 1: Authentication Module**
- **File:** LoginForm.jsx, AuthContext.jsx
- **Responsibility:** Manages all user authentication interactions including login form rendering, role selection, registration form handling, token storage, and session management across all four user roles
- **Key Functions:**
  - Render multi-role login and registration forms
  - Submit authentication requests to backend API
  - Store and manage JWT tokens in local storage
  - Provide authentication context to all child components
  - Handle session expiry and automatic logout

---

**Module 2: Admin Dashboard Module**
- **File:** AdminDashboard.jsx
- **Responsibility:** Provides the complete administrative interface for system management including institute management, student monitoring, verifier management, verification oversight, feedback management, and report generation
- **Key Functions:**
  - Display system-wide analytics and statistics
  - Manage institute records with add, edit, and delete operations
  - Monitor all verification activities and flag suspicious events
  - Generate and display AI-powered visual reports
  - Manage verifier accounts and feedback records

---

**Module 3: Institute Dashboard Module**
- **File:** InstituteDashboard.jsx
- **Responsibility:** Provides the complete institute management interface including student enrollment, certificate issuance, profile management, and AI chatbot interaction
- **Key Functions:**
  - Display institute-specific analytics dashboard
  - Add and manage student records with auto-generated IDs
  - Upload and issue certificates to registered students
  - View and edit institute profile information
  - Interact with AI assistant for institute-specific queries

---

**Module 4: Student Dashboard Module**
- **File:** StudentDashboard.jsx
- **Responsibility:** Provides the student-facing interface for credential management including profile viewing, certificate tracking, verification history monitoring, and certificate file downloading
- **Key Functions:**
  - Display student profile and personal information
  - List all issued certificates with status and hash details
  - View detailed certificate information including blockchain data
  - Download certificate PDF files from the server
  - Monitor verification history and verifier details

---

**Module 5: Verifier Dashboard Module**
- **File:** VerifierDashboard.jsx
- **Responsibility:** Provides the verifier interface for certificate authentication including file upload, verification result display, history tracking, feedback submission, and AI chatbot interaction
- **Key Functions:**
  - Upload certificate files for instant verification
  - Display detailed verification results with confidence scores
  - View complete verification history with timestamps
  - Submit structured feedback reports to administrators
  - Interact with AI assistant for verification-related queries

---

**Module 6: AI Assistant Module**
- **File:** AIAssistantWidget.jsx, ChatbotOverlay.jsx
- **Responsibility:** Provides a floating AI chatbot widget accessible across all dashboards, enabling users to interact with live system data through natural language queries
- **Key Functions:**
  - Render floating chat interface with open and close states
  - Send natural language queries to role-specific AI endpoints
  - Display AI responses with message history and timestamps
  - Maintain session-based conversation context
  - Provide suggested queries for common user interactions

---

**Module 7: Report Module**
- **File:** ReportDialog.jsx
- **Responsibility:** Handles the display of AI-generated visual reports including key metrics, AI insights, chart visualization, and report download functionality
- **Key Functions:**
  - Render report dialog with loading and data states
  - Display key metrics in formatted grid layout
  - Show AI-generated textual insights and summaries
  - Render chart images fetched from the backend file system
  - Provide chart download functionality for offline use

---

**Module 8: UI Components Module**
- **File:** UIComponents.jsx, Layout.jsx
- **Responsibility:** Provides a library of reusable UI components and layout structures used consistently across all dashboards to maintain visual consistency and reduce code duplication
- **Key Functions:**
  - StatCard component for displaying metric statistics
  - InfoCard component for content panel containers
  - Button component with variant and size configurations
  - Badge component for status and label indicators
  - Layout component for consistent navigation and header structure

---

**3.5.2 Backend Modules**

The backend of CertiSense AI is built using FastAPI with SQLAlchemy and is organized into the following functional modules:

---

**Module 1: Main Application Module**
- **File:** certisense_main.py
- **Responsibility:** Serves as the central entry point of the backend application, registering all API routes, configuring middleware, mounting static file directories, and initializing the database schema on startup
- **Key Functions:**
  - Initialize FastAPI application instance
  - Configure CORS middleware for cross-origin requests
  - Mount static file directories for uploads and frontend build
  - Register all API route handlers for all user roles
  - Include external routers from admin and other route modules
  - Serve React frontend build as static files in production

---

**Module 2: Authentication Module**
- **File:** auth_db.py
- **Responsibility:** Manages all authentication and authorization operations including user credential verification, JWT token generation, token validation, and password hashing across all four user roles
- **Key Functions:**
  - authenticate_admin() — Verify admin credentials and generate token
  - authenticate_institute() — Verify institute email and password
  - authenticate_student() — Verify student ID and password
  - authenticate_verifier() — Verify verifier username and password
  - register_institute() — Hash password and create institute record
  - register_student() — Generate student ID and create student record
  - register_verifier() — Hash password and create verifier record
  - verify_token() — Decode and validate JWT token payload

---

**Module 3: Database Module**
- **File:** database.py
- **Responsibility:** Defines all SQLAlchemy ORM models, database connection configuration, session management, and table creation for the six core entities of the CertiSense AI database
- **Key Functions:**
  - Define Institute, Student, Verifier, Certificate, Verification, and Feedback ORM models
  - Configure SQLite database connection and engine
  - Provide get_db() dependency for session injection into route handlers
  - Define CertificateStatusEnum and VerificationStatusEnum enumerations
  - Initialize all database tables on application startup

---

**Module 4: Blockchain Service Module**
- **File:** blockchain_service.py
- **Responsibility:** Manages all blockchain-related operations including certificate hash storage, hash verification, chain hash generation, verification recording, and certificate chain retrieval
- **Key Functions:**
  - generate_file_hash() — Compute SHA-256 hash of certificate file content
  - store_certificate_hash() — Record certificate hash on blockchain ledger
  - verify_certificate_hash() — Cross-reference hash against blockchain registry
  - get_certificate_chain() — Retrieve complete certificate chain data
  - add_verification() — Record verification event on blockchain

---

**Module 5: AI Validation Service Module**
- **File:** ai_service.py
- **Responsibility:** Provides AI-powered certificate content validation including format analysis, keyword detection, confidence score computation, and validation result generation for uploaded certificate files
- **Key Functions:**
  - validate_certificate_content() — Analyze certificate file content and format
  - compute_confidence_score() — Generate numerical confidence assessment
  - generate_validation_token() — Create unique validation identifier
  - detect_anomalies() — Identify irregularities in certificate content
  - generate_explanation() — Produce human-readable validation explanation

---

**Module 6: Admin API Module**
- **File:** admin_api.py
- **Responsibility:** Handles all administrative API endpoints including institute management, student monitoring, verifier management, verification oversight, feedback management, and system analytics
- **Key Functions:**
  - GET /admin/analytics — Return system-wide statistics and metrics
  - GET /admin/institutes — List all registered institutes with statistics
  - POST /admin/institutes — Create new institute account
  - PUT /admin/institutes/{id} — Update institute information
  - DELETE /admin/institutes/{id} — Remove institute from system
  - GET /admin/students — List all students across all institutes
  - GET /admin/verifiers — List all registered verifiers
  - GET /admin/verifications — List all verification events
  - GET /admin/feedback — List all submitted feedback records

---

**Module 7: Institute Service Module**
- **File:** institute_service.py, institute_routes.py
- **Responsibility:** Handles all institute-specific business logic and API endpoints including student management, certificate issuance, dashboard analytics, and profile management
- **Key Functions:**
  - GET /institute/dashboard — Return institute analytics data
  - GET /institute/students — List all students for the institute
  - POST /institute/students — Register new student with auto-generated ID
  - POST /institute/certificates — Issue certificate with AI validation and blockchain recording
  - GET /institute/profile — Retrieve institute profile information
  - PUT /institute/profile — Update institute profile details

---

**Module 8: Student Service Module**
- **File:** student_service.py, student_routes.py
- **Responsibility:** Handles all student-specific business logic and API endpoints including profile management, certificate retrieval, certificate detail viewing, and file download operations
- **Key Functions:**
  - GET /student/profile — Retrieve student profile information
  - PUT /student/profile — Update student name and email
  - GET /student/certificates — List all certificates for the student
  - GET /student/certificate/{hash} — Retrieve detailed certificate and blockchain data
  - GET /student/certificates/{id}/download — Stream certificate PDF file

---

**Module 9: Verifier Service Module**
- **File:** verifier_service.py, verifier_routes.py
- **Responsibility:** Handles all verifier-specific business logic and API endpoints including certificate verification, verification history, feedback submission, and dashboard statistics
- **Key Functions:**
  - POST /verifier/verify — Process certificate file and return verification result
  - GET /verifier/dashboard — Return verifier statistics and performance metrics
  - GET /verifier/history — List all verification events for the verifier
  - POST /verifier/feedback — Submit structured feedback record
  - GET /verifier/feedback — List all feedback submitted by the verifier

---

**Module 10: AI Query Service Module**
- **File:** ai_query_service.py, institute_chatbot.py, verifier_chatbot.py
- **Responsibility:** Provides role-specific AI chatbot query processing for administrators, institutes, and verifiers, enabling natural language interaction with live database records and system statistics
- **Key Functions:**
  - process_admin_query() — Handle admin natural language queries with database context
  - InstituteChatbot.process_query() — Handle institute queries about students and certificates
  - VerifierChatbot.process_query() — Handle verifier queries about verification history
  - Generate contextual responses based on live database data
  - Maintain session-based conversation history

---

**Module 11: Report Service Module**
- **File:** report_service.py, report_visualizer.py
- **Responsibility:** Handles AI-powered report generation including data aggregation, chart creation, AI summary generation, and report file storage for all four report types
- **Key Functions:**
  - generate_institute_report() — Produce institute performance analytics report
  - generate_certificate_report() — Produce certificate issuance analytics report
  - generate_verification_report() — Produce verification success rate report
  - generate_system_report() — Produce system-wide activity report
  - create_chart() — Generate matplotlib visualization charts
  - save_report_image() — Store generated chart images to file system

---

**Module 12: Data Models Module**
- **File:** models.py
- **Responsibility:** Defines all Pydantic request and response models used for API input validation, serialization, and documentation across all endpoints of the CertiSense AI backend
- **Key Functions:**
  - LoginRequest — Validate username and password login inputs
  - RegisterRequest — Validate verifier registration inputs
  - InstituteRegisterRequest — Validate institute registration inputs
  - ChatMessage — Validate chatbot message inputs
  - Response models for all API endpoints

---

**3.5.3 Modular Design Summary**

| Layer | Module | Primary File | Responsibility |
|-------|--------|-------------|----------------|
| Frontend | Authentication | LoginForm.jsx | Login, registration, session management |
| Frontend | Admin Dashboard | AdminDashboard.jsx | System management and analytics |
| Frontend | Institute Dashboard | InstituteDashboard.jsx | Student and certificate management |
| Frontend | Student Dashboard | StudentDashboard.jsx | Certificate tracking and download |
| Frontend | Verifier Dashboard | VerifierDashboard.jsx | Certificate verification and feedback |
| Frontend | AI Assistant | AIAssistantWidget.jsx | Natural language chatbot interface |
| Frontend | Report Display | ReportDialog.jsx | AI report visualization |
| Frontend | UI Components | UIComponents.jsx | Reusable component library |
| Backend | Main Application | certisense_main.py | App initialization and routing |
| Backend | Authentication | auth_db.py | JWT auth and password hashing |
| Backend | Database | database.py | ORM models and session management |
| Backend | Blockchain Service | blockchain_service.py | Hash storage and verification |
| Backend | AI Validation | ai_service.py | Certificate content validation |
| Backend | Admin API | admin_api.py | Administrative endpoints |
| Backend | Institute Service | institute_service.py | Institute business logic |
| Backend | Student Service | student_service.py | Student business logic |
| Backend | Verifier Service | verifier_service.py | Verifier business logic |
| Backend | AI Query Service | ai_query_service.py | Chatbot query processing |
| Backend | Report Service | report_service.py | Report generation and charts |
| Backend | Data Models | models.py | Pydantic request validation |

The modular design of CertiSense AI ensures that each functional component of the platform is clearly defined, independently maintainable, and collectively integrated into a cohesive and well-structured system architecture that supports the long-term scalability, reliability, and extensibility of the certificate verification platform.

---

---

The context window is almost full (73%) and exceeding it will clear your history. Amazon Q can compact your history instead.