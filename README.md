# 🚴 SERVICE COMMAND - Specialized Bicycles IBP Platform

## Interview Demo for Planning Manager, Service & Warranty

**Candidate:** Trevor Carlton  
**Interviewer:** Brendan Lynch, Worldwide Logistics Leader  
**Role:** Planning Manager, Service and Warranty | Salt Lake City, UT

---

## 🎯 EXECUTIVE SUMMARY

Service Command is an Integrated Business Planning (IBP) proof-of-concept that demonstrates how data-driven decision-making can transform Specialized's Service & Warranty operations. This platform addresses **real challenges** facing Specialized:

1. **7-Year Right-to-Repair Obligations** vs. 18-month parts obsolescence
2. **EU Battery Passport Compliance** (February 2027 deadline)
3. **Production vs. Service Allocation Conflicts**
4. **Dealer Network Cash Flow Stress** from warranty reimbursement delays
5. **NPI Readiness Gaps** between product launches and service capability

---

## 🔑 KEY TALKING POINTS (By Module)

### Module 1: Executive Dashboard
**JD Alignment:** *"Track and report on team KPIs to ensure alignment with strategic goals"*

> "This dashboard gives me real-time visibility into our global service health. I can see fill rates, warranty liability exposure, and parts inventory health at a glance. The key metric here is the 94.2% fill rate against our 95% target—that gap represents riders waiting for repairs."

### Module 2: Right-to-Repair Liability Forecaster
**JD Alignment:** *"Develop and execute spare parts planning strategies that support global business objectives"*

> "Here's our fundamental challenge: we legally must support bikes for 7 years, but parts become obsolete in 18 months. This Weibull-based forecasting model helps me calculate the exact capital lock-up required to meet our legal obligations while minimizing scrap risk. The 'last-time buy' simulation ensures we order optimally before suppliers discontinue parts."

**Challenge his logic:** Ask him why 7 years specifically, and whether different product categories should have different horizons.

### Module 3: EU Battery Passport Compliance
**JD Alignment:** *"Identify and implement process improvements that elevate rider support"*

> "EU Regulation 2023/1542 requires a digital passport for every battery over 2kWh by February 2027. That's 426 days from now. This module tracks our compliance progress and individual battery traceability. What's powerful here is that compliance becomes competitive advantage—we can position Specialized as the premium sustainable brand because we can prove our supply chain integrity."

**Mention:** Specialized's existing Redwood Materials and Call2Recycle partnerships make this achievable.

### Module 4: Dealer Network Health
**JD Alignment:** *"Collaborate with purchasing, quality engineering, and global customer support teams"*

> "Our dealers are the front line of rider experience. When I see $1.8M in pending reimbursements, that's cash flow stress that degrades service quality. This dashboard helps me identify friction points before they become escalations. The fill rate heatmap shows where we're underperforming—LATAM is struggling at 89%."

**Key insight:** Dealer experience = Rider experience. Fix dealer problems proactively.

### Module 5: Allocation War Room
**JD Alignment:** *"Own escalation pathways and develop proactive solutions for risks identified in the supply plan"*

> "This is the hardest conversation in supply chain: Production wants parts for new bikes; Service needs them for warranty. This simulator shows the concrete trade-offs. If I move allocation to 70% Production, we'll have 200+ service stockouts affecting 600 riders. But if I go 70% Service, we risk delaying the Levo Gen 5 launch. My job is to find the sweet spot—and this tool gives me data to influence stakeholders."

### Module 6: S&OP Command Center
**JD Alignment:** *"Collaborate with product teams and communicate NPI milestones"*

> "Service readiness must happen BEFORE launch, not after. This Gantt view shows our NPI pipeline—Turbo Levo Gen 5 is at high risk with only 35% parts readiness. I also track team KPIs here: MAPE by region, planner workload, escalation counts. When I see David C. with 22 open escalations, that's a coaching opportunity."

---

## 💡 STRATEGIC INSIGHTS FOR BRENDAN LYNCH

Based on research, Brendan has:
- **20+ years supply chain experience** — he'll appreciate quantitative rigor
- **Taiwan base** — he's close to manufacturing; understands APAC complexity
- **Military background (Lt. Col, USMCR)** — values discipline, clear escalation paths, accountability
- **University of Manchester** — operations research training; will appreciate the Weibull modeling

**Tailor your pitch to:**
1. Show you understand global complexity (not just US-centric)
2. Demonstrate financial impact awareness (capital lock-up, not just operational metrics)
3. Connect everything back to **rider experience** (Specialized's brand promise)
4. Reference their sustainability commitments (Redwood Materials, Call2Recycle)

---

## 🚀 HOW TO RUN THE DEMO

```bash
# Navigate to the app directory
cd service_command

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py --server.port 8501
```

The app will open in your browser at `http://localhost:8501`

---

## 📋 INTERVIEW PREPARATION CHECKLIST

- [ ] Practice navigating each module smoothly
- [ ] Know the KPI targets (95% fill rate, 14-day resolution, 50% recycling rate)
- [ ] Be ready to explain Weibull distribution in simple terms
- [ ] Prepare for "what would you do differently" questions
- [ ] Have backup if screen-share fails (screenshots, PDF export)

---

## 🎤 CLOSING STATEMENT

> "What excites me about this role is the opportunity to transform service from a cost center into a brand retention engine. Specialized has 50 years of rider trust—my job would be to ensure that every rider who needs a repair gets the part they need, when they need it, whether their bike is 1 year old or 7. This platform is how I would approach that challenge: data-driven, proactive, and always connected to the rider experience."

---

## 📊 DATA NOTES

All data in this prototype is **simulated** but modeled on realistic scenarios:
- Battery serial numbers follow Specialized naming conventions
- Product catalog uses actual Turbo model names
- Warranty periods match Specialized's published policies
- EU regulation deadlines are accurate (Regulation 2023/1542)

---

*Built with ❤️ for the Planning Manager interview at Specialized Bicycles*
