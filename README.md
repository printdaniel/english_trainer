# 🎓 English Trainer

A structured, CLI-based English learning system built in Python with Spaced Repetition System (SRS).

This project implements a 30-day intensive English learning plan with vocabulary tracking, spaced repetition, practice sessions, and progress analytics.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![SQLite](https://img.shields.io/badge/database-SQLite-green.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Objective

The goal of this project is twofold:

1. **Build a real-world Python application** with clean architecture and best practices
2. **Implement a structured one-month English learning system** focused on:
   - 📚 Vocabulary acquisition with SRS
   - ✍️ Grammar reinforcement
   - 📝 Writing practice
   - 🗣️ Speaking consistency
   - 📊 Daily progress tracking

This is not just a CRUD app—it's a **personal language training system** that adapts to your learning pace.

---

## ✨ Features

### ✅ Implemented Features

- **Vocabulary Management**
  - Add, list, and delete words with translations and examples
  - Organize by difficulty level (beginner, intermediate, advanced)
  - Track learning progress for each word

- **Spaced Repetition System (SRS)**
  - Smart review scheduling based on performance
  - Adaptive intervals: 1 day → 3 days → exponential growth
  - Reset on incorrect answers for better retention

- **Practice Sessions**
  - Full practice mode with multiple words
  - Real-time feedback and accuracy tracking
  - Session statistics (reviewed, correct, accuracy, duration)
  - Daily progress persistence

- **Progress Analytics**
  - View total vocabulary size
  - Track daily practice statistics
  - Monitor accuracy and session duration

### 🚧 Planned Features

- Grammar topic tracking and exercises
- Writing practice module with feedback
- Speaking session logging
- Weekly performance reports
- Import/export vocabulary lists
- Multi-language support

---

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/printdaniel/english_trainer.git
   cd english_trainer
   ```

2. **No dependencies required!**
   Python 3.8+ with SQLite (included in standard library) is all you need.

3. **Initialize with sample data (optional):**
   ```bash
   python3 quickstart.py
   ```
   This loads 30 sample words across all difficulty levels.

---

## 📖 Usage

### Basic Commands

```bash
# Add a new word
python3 main.py add beautiful -t 'hermoso' -e 'What a beautiful day!' -l intermediate

# List all vocabulary
python3 main.py list

# Practice a random word (simple mode)
python3 main.py practice

# Start a full practice session (recommended)
python3 main.py session -n 10

# View your statistics
python3 main.py stats

# Delete a word by ID
python3 main.py delete 5

# Get help
python3 main.py --help
```

### Practice Session Example

```bash
$ python3 main.py session -n 5

==================================================
  Starting Practice Session (5 words)
==================================================

[1/5] Translate: beautiful
   Example: What a beautiful day!
   Your answer: hermoso
   ✓ Correct!

[2/5] Translate: goodbye
   Your answer: adios
   ✗ Incorrect (correct answer: adiós)

...

==================================================
  Session Complete!
==================================================
  Reviewed:  5 words
  Correct:   4
  Incorrect: 1
  Accuracy:  80.0%
  Duration:  45 seconds
==================================================
```

---

## 🧠 One-Month English Learning Plan

**Target level:** Low-Intermediate → Solid Intermediate Foundation
**Duration:** 30 days
**Commitment:** 60–90 minutes daily

### Weekly Structure Overview

#### 📅 Week 1 – Foundation & Core Structures

**Focus:**
- Present Simple / Present Continuous
- Daily vocabulary (20–25 words/day)
- Basic sentence construction
- Short daily writing (100–150 words)

**Daily Tasks:**
- Add 20 new words to English Trainer
- Practice with `session` command
- Write 10 original sentences
- 10-minute speaking practice

**Goal:** Build sentence confidence and reduce fear of writing.

---

#### 📅 Week 2 – Control of Time (Past & Future)

**Focus:**
- Past Simple & Future tenses
- Basic connectors (because, although, however)
- Structured short texts (150–200 words)

**Daily Tasks:**
- Add 15–20 new words
- Review due words with SRS
- Rewrite past experiences
- 15-minute speaking session

**Goal:** Narrate past events and describe future plans confidently.

---

#### 📅 Week 3 – Functional Communication

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

**Goal:** Express opinions and abstract ideas.

---

#### 📅 Week 4 – Fluency & Consolidation

**Focus:**
- Mixed tenses
- Complex sentences
- Debate-style responses
- Structured argument writing

**Daily Tasks:**
- Review all vocabulary with SRS
- 250–300 word essays
- 20–30 minutes speaking
- Weekly self-evaluation using `stats` command

**Goal:** Produce independent, structured English with minimal hesitation.

---

## 🛠️ How This Project Implements the Plan

The system supports all learning components:

| Learning Component | Project Feature | Status |
|-------------------|-----------------|--------|
| Vocabulary tracking | `vocabulary` table | ✅ Complete |
| Spaced repetition | `services/srs.py` | ✅ Complete |
| Practice sessions | `session` command | ✅ Complete |
| Progress tracking | `daily_progress` table | ✅ Complete |
| Statistics | `stats` command | ✅ Complete |
| Grammar topics | `grammar_topics` table | 🚧 Planned |
| Writing practice | `writing_practice` table | 🚧 Planned |
| Speaking sessions | `speaking_sessions` table | 🚧 Planned |

---

## 🏗️ Project Architecture

```
english_trainer/
├── app/
│   ├── __init__.py
│   ├── cli.py                  # Command-line interface
│   ├── database.py             # Database initialization & connection
│   │
│   ├── models/                 # Data models (CRUD operations)
│   │   ├── __init__.py
│   │   └── vocabulary.py       # Vocabulary management
│   │
│   └── services/               # Business logic
│       ├── __init__.py
│       ├── srs.py              # Spaced Repetition System
│       └── practice_engine.py  # Practice session logic
│
├── data/
│   └── english_trainer.db      # SQLite database (auto-created)
│
├── main.py                     # Application entry point
├── quickstart.py               # Sample data loader
├── README.md                   # This file
└── requirements.txt            # No external dependencies!
```

### Architecture Layers

```
┌─────────────────────────────────────┐
│         CLI Layer (cli.py)          │  ← User interaction
├─────────────────────────────────────┤
│   Service Layer (srs, practice)     │  ← Learning logic
├─────────────────────────────────────┤
│    Model Layer (vocabulary)         │  ← CRUD operations
├─────────────────────────────────────┤
│   Database Layer (database.py)      │  ← SQLite persistence
└─────────────────────────────────────┘
```

---

## 📊 Database Schema

### Tables

**vocabulary** - Stores words with SRS metadata
```sql
id, word, translation, example_sentence, level,
next_review, interval, ease_factor, repetitions
```

**daily_progress** - Tracks daily practice statistics
```sql
id, date, words_reviewed, words_correct,
accuracy, session_duration
```

**grammar_topics** - Grammar exercises (planned)
**writing_practice** - Writing entries (planned)
**speaking_sessions** - Speaking logs (planned)

---

## 🔧 Development

### Running Tests

```bash
# Test database initialization
python3 -c "from app.database import init_db; init_db(); print('✓ DB OK')"

# Test vocabulary model
python3 -c "from app.models.vocabulary import Vocabulary; Vocabulary.add_word('test', 'prueba', 'test', 'beginner'); print('✓ Model OK')"

# Test CLI
python3 main.py list
```

### Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

**Priority areas:**
- Grammar practice module
- Writing feedback system
- Speaking session timer
- Import/export functionality
- Web interface

---

## 📝 Tips for Success

1. **Be consistent:** Practice daily, even if just 10 minutes
2. **Use real examples:** Add sentences relevant to your life
3. **Review regularly:** Let the SRS guide your review schedule
4. **Track progress:** Check `stats` weekly to stay motivated
5. **Escape special characters:** Use quotes for words with accents
   ```bash
   # Correct
   python3 main.py add goodbye -t 'adiós' -l beginner

   # Will work but without accent
   python3 main.py add goodbye -t adios -l beginner
   ```

---

## 🙏 Acknowledgments

Built with ❤️ for language learners everywhere.

**Tech Stack:**
- Python 3.8+
- SQLite3
- argparse (CLI)
- Standard library only!

---

## 📄 License

MIT License - feel free to use this project for learning!

---

## 🎯 Roadmap

- [x] Vocabulary CRUD operations
- [x] Spaced Repetition System
- [x] Practice sessions with feedback
- [x] Progress tracking and statistics
- [ ] Grammar practice module
- [ ] Writing practice with AI feedback
- [ ] Speaking session timer
- [ ] Weekly/monthly reports
- [ ] Web interface
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Import/export to Anki/CSV

---

**Happy Learning! 🎉**

*Remember: Consistency beats intensity. 10 minutes daily is better than 2 hours once a week.*
