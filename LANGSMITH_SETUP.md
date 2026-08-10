# LangSmith LLMOps Setup Guide

## What is LangSmith?

**LangSmith** is a platform for LLM observability, debugging, and evaluation. It automatically traces:
- 🔍 Every LLM call (prompts, responses, tokens)
- 🤖 Agent decisions and reasoning steps
- 💰 Costs per query
- ⏱️ Latency breakdown
- 🐛 Errors and failures

**Perfect for debugging hallucinations and optimizing prompts!**

---

## Quick Setup (5 minutes)

### Step 1: Sign Up for LangSmith

1. Go to: **https://smith.langchain.com**
2. Click **"Sign Up"** (free tier available)
3. Create account with email or GitHub

**Free Tier Includes:**
- ✅ 5,000 traces/month
- ✅ 14-day trace retention
- ✅ Full debugging features
- ✅ No credit card required

---

### Step 2: Get Your API Key

1. Log in to LangSmith
2. Click your profile (top right)
3. Go to **Settings → API Keys**
4. Click **"Create API Key"**
5. Copy the key (starts with `lsv2_pt_...`)

---

### Step 3: Add API Key to `.env`

Open `.env` file and update:

```bash
# LangSmith LLMOps
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_your_actual_key_here
LANGCHAIN_PROJECT=oilfield-intelligence
```

**Replace** `lsv2_pt_your_actual_key_here` with your actual API key!

---

### Step 4: Restart Backend

```bash
cd backend
python main.py
```

You should see:
```
✅ LangSmith LLMOps Enabled!

Project: oilfield-intelligence
Endpoint: https://api.smith.langchain.com

View traces at: https://smith.langchain.com/o/default/projects/p/oilfield-intelligence
```

---

### Step 5: Run a Query

1. Go to **http://localhost:3000**
2. Ask: **"Why is production dropping at Rig Alpha?"**
3. Wait for response

---

### Step 6: View Trace in LangSmith

1. Go to: **https://smith.langchain.com**
2. Click **Projects** → **oilfield-intelligence**
3. You'll see your query trace!

**What you'll see:**
- 📊 Full conversation flow
- 🔍 Every LLM call with prompts/responses
- 💰 Token usage and cost
- ⏱️ Latency for each step
- 🐛 Any errors or warnings

---

## What Gets Traced?

### Automatically Traced:
- ✅ All OpenAI API calls
- ✅ LangGraph agent workflows
- ✅ Parser → SQL → Graph → Reasoning flow
- ✅ Prompt templates and variables
- ✅ Token counts and costs
- ✅ Errors and exceptions

### Example Trace:
```
Query: "Why is production dropping at Rig Alpha?"
├─ Parser Agent (10ms)
│  └─ Extracted: rigs=["Rig Alpha"], intent="production_drop"
├─ SQL Agent (50ms)
│  ├─ Generated SQL query
│  └─ Returned 80 records
├─ Graph Agent (30ms)
│  ├─ Generated Cypher query
│  └─ Found faulty sensor G-40
├─ Reasoning Agent (2000ms)
│  ├─ LLM Call: gpt-4o-mini
│  ├─ Tokens: 450 input, 120 output
│  ├─ Cost: $0.00008
│  └─ Generated concise answer
└─ Total: 2090ms, $0.00008
```

---

## Benefits for Your Project

### 1. Debug Hallucinations
- See exactly what data the LLM received
- Compare LLM output to actual database results
- Identify where hallucinations occur

### 2. Optimize Costs
- Track cost per query type
- Identify expensive queries
- Optimize prompts to reduce tokens

### 3. Improve Performance
- Find slow LLM calls
- Optimize prompt length
- Reduce latency

### 4. A/B Test Prompts
- Compare different prompt versions
- Measure quality improvements
- Roll back if needed

---

## Advanced Features

### Create Datasets for Testing

```python
# In LangSmith UI, create a dataset:
# 1. Go to Datasets → Create Dataset
# 2. Add test queries:
#    - "Why is production dropping at Rig Alpha?"
#    - "Show me all faulty equipment"
#    - "What is the safety risk at Well W-12?"
# 3. Run evaluations to test prompt changes
```

### Set Up Alerts

```python
# In LangSmith UI:
# 1. Go to Settings → Alerts
# 2. Create alert for:
#    - High cost queries (> $0.01)
#    - Slow queries (> 5s)
#    - Error rate (> 5%)
```

---

## Troubleshooting

### "LangSmith API key not configured"

**Solution:** Make sure `.env` has:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_your_actual_key_here
```

### "No traces appearing in LangSmith"

**Checklist:**
1. ✅ Backend restarted after adding API key?
2. ✅ API key is correct (starts with `lsv2_pt_`)?
3. ✅ Internet connection working?
4. ✅ Query actually ran (check backend logs)?

### "Rate limit exceeded"

**Solution:** Free tier has 5K traces/month. Upgrade to Plus ($39/mo) for 100K traces.

---

## Cost Comparison

| Tier | Price | Traces/Month | Retention |
|------|-------|--------------|-----------|
| **Free** | $0 | 5,000 | 14 days |
| **Plus** | $39/mo | 100,000 | 90 days |
| **Enterprise** | Custom | Unlimited | Custom |

**Recommendation:** Start with **Free tier**, upgrade if you exceed 5K traces/month.

---

## Next Steps

Once LangSmith is working:

1. ✅ **Add Phoenix** (open-source observability)
2. ✅ **Add Helicone** (caching to reduce costs 50%)
3. ✅ **Add MLflow** (experiment tracking)
4. ✅ **Create evaluation datasets**
5. ✅ **Set up cost alerts**

See `LLMOPS_ROADMAP.md` for full implementation plan.

---

## Support

- **LangSmith Docs:** https://docs.smith.langchain.com
- **Discord:** https://discord.gg/langchain
- **GitHub Issues:** https://github.com/langchain-ai/langsmith-sdk

---

**Ready to enable LangSmith? Just add your API key to `.env` and restart!** 🚀

