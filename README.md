# English Trainer

A structured, CLI-based English learning system built in Python.
This project is designed to implement a 30-day intensive English learning plan with vocabulary tracking, grammar reinforcement, writing practice, speaking logs, and (soon) spaced repetition.

---

## 🎯 Project Objective

The goal of this project is twofold:

1. Build a real-world Python application with clean architecture.
2. Implement a structured one-month English learning system focused on:
   - Vocabulary acquisition
   - Grammar reinforcement
   - Writing practice
   - Speaking consistency
   - Daily progress tracking

This is not just a CRUD app. It is a personal language training system.

---

# 🧠 One-Month English Learning Plan (Structured & Intensive)

**Target level:** Low-Intermediate → Solid Intermediate Foundation
**Duration:** 30 days
**Commitment:** 60–90 minutes daily

---

## Weekly Structure Overview

### Week 1 — Foundation & Core Structures

**Focus:**
- Present Simple / Present Continuous
- Daily vocabulary (20–25 words/day)
- Basic sentence construction
- Short daily writing (100–150 words)

**Daily Tasks:**
- Learn 20 new words
- Write 10 original sentences
- 10-minute speaking practice
- 1 short paragraph about your day

**Goal:**
Build sentence confidence and reduce fear of writing.

---

### Week 2 — Control of Time (Past & Future)

**Focus:**
- Past Simple
- Future (will / going to)
- Basic connectors (because, although, however)
- Structured short texts (150–200 words)

**Daily Tasks:**
- 15–20 new words
- Rewrite past experiences
- 15-minute speaking session
- Controlled grammar drills

**Goal:**
Narrate past events and describe future plans confidently.

---

### Week 3 — Functional Communication

**Focus:**
- Present Perfect
- Comparatives & Superlatives
- Modal verbs (must, should, can, might)
- Opinion paragraphs

**Daily Tasks:**
- Vocabulary refinement
- 200–250 word writing
- Timed speaking sessions (20 minutes)
- Error correction analysis

**Goal:**
Express opinions and abstract ideas.

---

### Week 4 — Fluency & Consolidation

**Focus:**
- Mixed tenses
- Complex sentences
- Debate-style responses
- Structured argument writing

**Daily Tasks:**
- Review vocabulary (SRS)
- 250–300 word essays
- 20–30 minutes speaking
- Weekly self-evaluation

**Goal:**
Produce independent, structured English with minimal hesitation.

---

# 🛠 How This Project Implements the Plan

The system supports:

| Learning Component | Project Feature |
|-------------------|-----------------|
| Vocabulary tracking | `vocabulary` table |
| Grammar topics | `grammar_topics` table |
| Writing practice | `writing_practice` table |
| Speaking sessions | `speaking_sessions` table |
| Daily tracking | `daily_progress` table |
| Practice sessions | CLI practice command |
| Spaced repetition | `services/srs.py` (in progress) |

The CLI allows you to:

- Add vocabulary
- Practice words
- Track sessions
- Build a structured daily routine

This project turns the learning plan into measurable progress.

---

# 🏗 Project Architecture


### Architecture Layers

- **Database Layer** → SQLite persistence
- **Model Layer** → CRUD operations
- **Service Layer** → Learning logic (SRS, tracking)
- **CLI Layer** → User interaction
- **Entry Point** → `main.py`

---


