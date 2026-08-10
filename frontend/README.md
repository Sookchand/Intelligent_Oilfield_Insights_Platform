# 🎨 Intelligent Oilfield Insights - Frontend

Modern, enterprise-grade Next.js frontend for the Intelligent Oilfield Insights Platform.

## 🚀 Features

### ✅ **Implemented (Core Features)**

#### 1. **Query Dashboard** (`/`)
- 🔍 Natural language query interface with autocomplete
- 📊 Real-time database connectivity status
- 💾 Query history and bookmarks (localStorage)
- 🎯 Demo queries for quick testing
- ⚡ Real-time results with typewriter effect
- 📈 Quick stats and metrics display

#### 2. **Explainability Dashboard** (`/explainability`)
- 🧠 **Agent Workflow Visualization** - Visual representation of multi-agent processing
- ⏱️ **Detailed Reasoning Timeline** - Step-by-step execution trace with SQL/Cypher queries
- 📊 **Confidence Analysis** - Breakdown of confidence factors and evolution
- 🗄️ **Data Source Attribution** - Visual attribution of data sources with weights
- 🕸️ **Knowledge Graph Visualization** - Interactive graph of asset relationships
- 📥 Export functionality for reports

### 🚧 **Placeholder Pages** (Coming Soon)
- `/business` - Business Impact Analytics (Downtime costs, ROI, Safety risk)
- `/data` - Data Explorer (Browse PostgreSQL, Neo4j, Qdrant, MinIO)
- `/system` - System Monitor (Real-time metrics and health checks)

## 🛠️ Tech Stack

- **Framework**: Next.js 14.2 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand + React Query
- **Data Fetching**: Axios + TanStack Query
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Graph Visualization**: Custom SVG rendering

## 📦 Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local to point to your backend
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🏃 Running the Application

```bash
# Development mode (with hot reload)
npm run dev

# Production build
npm run build
npm start

# Type checking
npm run lint
```

The application will be available at:
- **Development**: http://localhost:3000
- **Production**: http://localhost:3000 (after build)

## 📁 Project Structure

```
frontend/
├── app/                          # Next.js App Router pages
│   ├── layout.tsx               # Root layout with navigation
│   ├── page.tsx                 # Query Dashboard (/)
│   ├── explainability/          # Explainability page
│   │   └── page.tsx
│   ├── business/                # Business Impact (placeholder)
│   ├── data/                    # Data Explorer (placeholder)
│   └── system/                  # System Monitor (placeholder)
│
├── components/                   # React components
│   ├── Navigation.tsx           # Main navigation bar
│   ├── QueryInput.tsx           # Query input with history
│   ├── ResultsDisplay.tsx       # Query results display
│   ├── DemoQueries.tsx          # Demo query cards
│   ├── DatabaseStatus.tsx       # Database connectivity status
│   └── explainability/          # Explainability components
│       ├── AgentWorkflow.tsx    # Agent workflow visualization
│       ├── ReasoningTimeline.tsx # Detailed reasoning steps
│       ├── ConfidenceBreakdown.tsx # Confidence analysis
│       ├── DataSourceAttribution.tsx # Data source weights
│       └── GraphVisualization.tsx # Knowledge graph viz
│
├── lib/                         # Utilities and API client
│   └── api.ts                   # Axios client + TypeScript types
│
├── public/                      # Static assets
├── styles/                      # Global styles
└── package.json                 # Dependencies
```

## 🔌 API Integration

The frontend connects to the backend API at `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`).

### Available Endpoints:

```typescript
// Query Processing
POST /api/query
GET  /api/status/databases

// Business Metrics (backend ready, frontend placeholder)
GET  /api/business/downtime-cost/{rig_name}
GET  /api/business/maintenance-roi/{equipment_id}
GET  /api/business/safety-risk/{rig_name}
GET  /api/business/forecast/{rig_name}

// System Monitoring (backend ready, frontend placeholder)
GET  /api/system/metrics
```

## 🎨 Key Components

### Query Dashboard
- **QueryInput**: Smart input with history, bookmarks, and autocomplete
- **DemoQueries**: Pre-built demo queries for testing
- **DatabaseStatus**: Real-time database connectivity monitoring
- **ResultsDisplay**: Beautiful results with typewriter effect

### Explainability Dashboard
- **AgentWorkflow**: Visual workflow of Parser → SQL → Graph → Reasoning agents
- **ReasoningTimeline**: Expandable timeline with SQL/Cypher queries
- **ConfidenceBreakdown**: Confidence score with factor breakdown
- **DataSourceAttribution**: Visual attribution of PostgreSQL, Neo4j, etc.
- **GraphVisualization**: Interactive knowledge graph with SVG

## 🚀 Next Steps

To complete the platform, implement these placeholder pages:

1. **Business Impact Page** (`/business`)
   - Downtime cost calculator
   - Maintenance ROI analysis
   - Safety risk scoring
   - Production forecasting charts

2. **Data Explorer** (`/data`)
   - PostgreSQL table browser
   - Neo4j graph explorer
   - Qdrant vector search
   - MinIO object browser

3. **System Monitor** (`/system`)
   - Real-time metrics dashboard
   - Agent performance monitoring
   - Database health checks
   - Query performance analytics

## 📝 Development Notes

- All components are fully typed with TypeScript
- Uses Next.js App Router (not Pages Router)
- Client components marked with `'use client'`
- Responsive design (mobile-first)
- Dark mode support (system preference)
- Accessibility features included

## 🐛 Known Issues

- Next.js 14.2.0 has a security vulnerability (upgrade to latest when ready)
- Some npm packages have deprecation warnings (non-critical)

## 📄 License

Part of the Intelligent Oilfield Insights Platform

