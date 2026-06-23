# HW6 Spec Digest: Dual AI Agent Conversation via MCP Servers
## University of Haifa, Course 203.3763 "Orchestration of AI Agents" — Lecture 09

**Compiled from:** L09 v1.0 (19-06-2026) by Dr. Yoram Segal, IDEA-raw.txt  
**For:** HW6 development team  
**Target Audience:** Implementation lead/architect

---

## HW6 in One Paragraph

**HW6** ("EX06 — Dual AI Agent Conversation via MCP Servers") requires students to design, implement, and autonomously execute a complete end-to-end pipeline enabling two independent LLM agents—a **Cop** and a **Thief**—to play a turn-based chase game on a configurable 2D grid, communicating entirely in **free natural language** over isolated **MCP (Model Context Protocol) servers**. The system must initialize autonomously, play exactly 6 complete sub-games (max 25 moves each), and send an automated JSON report via Gmail API with zero manual intervention. **Core grading metric:** communication quality and orchestration maturity, NOT game strategy or algorithm optimization. **Due:** Friday, 3 July 2026, submitted to Moodle (id=282206). **Bonus:** A 10-point final-project bonus is available for inter-group competitive matches (deadline: Friday 8:30 AM, one week from assignment publication). Submitting the bonus extends the standard HW5 deadline by one week as a courtesy to teams managing both tasks.

---

## The Game: Structure, Rules, Scoring

### Two-Level Game Architecture

**Sub-Game (Meshkak):**
- A single chase encounter, limited to a maximum of **25 moves** per game
- Each move: player may change position OR place a barrier (cop only)
- Turn order: **Thief moves first, then Cop, alternating**
- Ends when: (a) Cop captures Thief, (b) Thief survives 25 moves, or (c) technical failure

**Game (Mishkak):**
- A complete series of exactly **6 consecutive sub-games** played sequentially
- All sub-game results are accumulated and reported together at the end
- Scores from all 6 sub-games are summed for final group score

### Grid Layout and Movement

**Grid Specification:**
- Default size: **5×5** (configurable via `config.json`/`config.yaml`, **never hardcoded**)
- Each cell has integer coordinates
- Cop and Thief start at designated positions (random or strategy-selected)
- **Movement directions:** All 8 directions supported (including diagonals)
- **State machine:** Board state updates after each move
- No wrapping; walls at edges

### Win Conditions and Barriers

**Cop Victory:**
- Cop occupies the exact same cell as the Thief (capture/arrest)
- Rewards Cop with **20 points**, Thief with **5 points**

**Thief Victory:**
- Thief survives all 25 moves without being captured
- Rewards Thief with **10 points**, Cop with **5 points**

**Barrier Placement (Optional Action):**
- Instead of moving, Cop may place a **barrier** on current cell
- Barrier action counts as 1 move but prevents Cop from advancing that turn
- Once placed, barrier blocks both Cop and Thief (like a wall or grid edge)
- Cop is limited to **max 5 barriers per sub-game**
- Thief cannot place barriers

### Scoring Summary

| Outcome | Cop Score | Thief Score |
|---------|-----------|-------------|
| Cop Wins (Capture) | 20 | 5 |
| Thief Wins (Survives 25) | 5 | 10 |

**Aggregate Scoring:**
- Max possible per game (6 sub-games): **90 points** (3×20 as Cop + 3×10 as Thief, if all sub-games are cop wins)
- Min possible per game: **30 points** (3×5 + 3×5, all losses)
- **Group score = sum of all 6 sub-game scores**

### Sanity-Check Progression (Recommended)

| Stage | Grid Size | Purpose | Complexity |
|-------|-----------|---------|-----------|
| 1 | 2×2 | Algorithmic sanity, basic pipeline integration, message passing validation | Very Low |
| 2 | 3×3 / 3×2 | Convergence of coordination mechanisms, hyperparameter tuning, failure detection | Medium |
| 3 | 4×4 / 4×3 | Partial observability impact; initial distance exceeds vision radius | High |
| 4 | 5×5 | Final test run; graph generation; full game analysis | Maximum |

---

## MCP Architecture and Protocol

### Core Philosophy: MCP as Communication Backbone

**MCP (Model Context Protocol)** is an open standard enabling LLMs to interact with external data sources, tools, and servers. For HW6:

- **Two independent MCP servers:** One for Cop, one for Thief (separate processes, separate ports)
- **No rigid protocol:** Agents communicate in **free natural language**, not structured position updates
- **Framework:** Built with **FastMCP** library, which exposes tools/resources/prompts to external clients
- **Key principle:** Both agents are autonomous; they don't share code or state. They only "see" what the other writes in text

### How Agents Talk to Each Other

**Communication Flow:**

1. **Agent A (e.g., Cop) decides on next action** via its MCP server's exposed tools
2. **Agent A generates a natural-language message** describing intent, observations, or deception (e.g., "I'm moving northeast; I can see the thief at roughly (3,3)")
3. **Game orchestrator (MCP Client)** reads message from Cop server, stores it
4. **Agent B (Thief) receives message via tool call** on its own MCP server
5. **Agent B processes message using LLM** to interpret it, estimate opponent position, and plan counter-move
6. **Agent B outputs decision in natural language**, which Thief's MCP server logs
7. **Orchestrator executes moves** on grid, updates board state
8. **Cycle repeats** for 25 moves or until terminal condition

### MCP Client vs. MCP Server

**Critical Distinction:**

| Aspect | MCP Client | MCP Server |
|--------|-----------|-----------|
| **What it is** | Your game orchestrator code; manages LLM invocations, game loop, decision logic | Stateless tool/resource provider (fastMCP); exposes tools like "send_message", "read_message", "get_position" |
| **Where LLM lives** | Client holds/manages LLM connection (cloud API or local Ollama) | Server does NOT hold LLM; only exposes tools/prompts |
| **Workflow** | Client sends query to LLM → LLM returns tool-call → Client invokes tool on Server → Server returns result → Client updates game state | Server waits for tool invocations; executes deterministic logic; returns data |
| **Responsibility** | Orchestration, state machine, turn logic, LLM prompting | Tool execution, validation, resource management |

**Concrete Flow:**
```
Client → LLM (with context) 
    ↓ (Tool Call: "send_message_to_opponent")
Client → Server (execute tool)
    ↓ (Tool returns confirmation)
Client ← Server
Client → LLM (with result)
    ↓ (Next decision)
```

---

## Full Required Pipeline: Initialization → Play → Automated Report

### Phase 1: Initialization (Autonomous)

- **Config loading:** Read `config.json` (grid size, max moves, num games, barriers limit, scoring rules)
- **MCP server startup:** Boot Cop server (port A), Thief server (port B) on localhost
- **Agent instantiation:** Create Cop agent, Thief agent, with assigned roles
- **Board setup:** Place Cop and Thief at starting positions
- **LLM connection:** Connect to cloud API or local Ollama (depending on architecture choice)
- **System ready:** No user input required

### Phase 2: Autonomous Play (Turn-Based Loop)

For each of 6 sub-games:
1. Reset board to starting positions
2. For move 1 to 25:
   - **Thief's turn:** LLM decides action → MCP Server logs natural-language message
   - **Cop's turn:** LLM receives Thief's message → decides action → logs response
   - **Orchestrator:** Updates grid state, checks win conditions
   - **Continue** until Cop captures Thief OR move 25 is reached
3. Record sub-game outcome (winner, score, move count)
4. **NO MANUAL INTERVENTION AT ANY POINT**

### Phase 3: Automated Report and Email

After all 6 sub-games complete:
- **JSON generation:** Construct structured report (defined below)
- **Gmail API:** Authenticate via OAuth token (not password)
- **Email dispatch:** Single email to `rmisegal+uoh26b@gmail.com` with JSON in body
- **Validation:** JSON must be properly formed and parseable

### Configuration-Driven Design (Mandatory)

**CRITICAL:** No hardcoding of game parameters. All must be externalized to a single config file:

**File:** `config.json` or `config.yaml`

**Required Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `grid_size` | [5, 5] | 2D grid dimensions |
| `max_moves` | 25 | Max moves per sub-game |
| `num_games` | 6 | Number of sub-games in sequence |
| `max_barriers` | 5 | Max barriers Cop can place per sub-game |
| `scoring.cop_win` | 20 | Points if Cop captures Thief |
| `scoring.thief_win` | 10 | Points if Thief survives |
| `scoring.cop_loss` | 5 | Points Cop gets if Thief escapes |
| `scoring.thief_loss` | 5 | Points Thief gets if captured |

**GUI (Optional but Recommended):**
- Visual display of grid, Cop position, Thief position, barriers, move counter
- Real-time update after each move
- Show natural-language messages exchanged (optional)

---

## LLM Architecture: Three Approaches

### Approach 1: Public Cloud API (Simple, Recommended)

**Implementation:**
- Game orchestrator (Client) connects directly to public cloud LLM API (OpenAI, Anthropic, Gemini, etc.)
- Send API key securely
- MCP servers remain on localhost or cloud without LLM embedded

**Advantages:**
- Stable, fast, no local compute burden
- Extremely low token cost (short conversations, low request volume)
- No firewall/networking hassles
- Can use free or low-cost API tiers

**Providers:** OpenAI (GPT-4, GPT-4o mini), Anthropic (Claude 3), Google Gemini, etc.

---

### Approach 2: Local Ollama with Secure Tunneling (Advanced)

**Setup:**
- Run Ollama on local machine (default port 11434, loopback only)
- Ollama is NOT natively exposed to internet → security risk if attempted
- Use tunneling tool to securely expose Ollama:

**Option A: ngrok with Traffic Policy**
```bash
ngrok http 11434 --config ollama.yaml
# ollama.yaml contains Basic Auth (username/password)
# Returns public HTTPS URL with authentication required
```

**Option B: Localtonet**
```
# Similar to ngrok, easier HTTP Auth setup via web UI
```

**Option C: Nginx Reverse Proxy (Full Engineering)**
```
# Self-hosted on local machine or VPS
# Handles SSL/TLS (Certbot/Let's Encrypt), Basic Auth (htpasswd)
# Firewall rules (UFW/nftables) block Ollama port locally
```

**Workflow:**
- MCP Server calls tunneled Ollama URL with Authorization header
- Ollama returns LLM response
- Game continues

---

### Approach 3: Hybrid Architecture (Recommended for Development)

**Setup:**
- **Locally:** Game Client + LLM (Ollama at localhost:11434) + stays on machine
- **Cloud:** Both MCP servers deployed (on Prefect Cloud, AWS, GCP, etc.)
- **Communication:** Client makes OUTBOUND HTTPS calls to cloud MCP servers (no inbound ports needed)

**Why Safer:**
- Ollama never exposed to internet
- No incoming firewall rules required
- Only outbound HTTPS (standard, trusted)
- MCP servers in cloud are stateless (no secrets/keys inside)

---

## Natural Language Communication Requirement

**Binding Requirement:** Agents must NOT exchange numeric coordinates, position tuples, or structured JSON commands. Instead:

- **Cop to Thief:** "I'm advancing north-east; last known position was near your starting corner"
- **Thief to Cop:** "I've moved away from the center; the area is too exposed"

**Why?** Tests orchestration and autonomous reasoning under partial observability, mimicking real distributed multi-agent systems.

---

## MCP Server Deployment & Security

### Local Phase (Localhost)

1. **Start Cop MCP server:** `python cop_server.py --port 5001`
2. **Start Thief MCP server:** `python thief_server.py --port 5002`
3. **Game Client connects:** `http://localhost:5001`, `http://localhost:5002`
4. **Verify:** Both servers respond to tool calls; game plays successfully

### Cloud Phase (Post-Validation)

- Deploy both MCP servers to cloud platform (Prefect Cloud recommended; also AWS Lambda, GCP, Azure, etc.)
- Each server gets a public HTTPS URL
- **Critical:** Must implement **token-based authentication** (OAuth or API key)

**Security Measures:**

- **Authentication:** Token-based (Bearer tokens or API keys), not passwords
- **Revocation:** Ability to revoke/invalidate tokens on demand
- **Firewall:** Ensure URLs are publicly accessible (not blocked by corporate firewall)
- **HTTPS:** All communication encrypted
- **No Sensitive Data in MCP Server:** Servers contain only game logic, not API keys or secrets

**Network Topology Warning:**
Dr. Segal emphasizes: Do NOT test from behind restrictive corporate firewalls or local networks that block outbound traffic on non-standard ports. Use home/public networks or cloud instances for deployment testing.

---

## Optional but Recommended: Q-Learning (Reinforcement Learning)

### Philosophy

RL is **recommended-only, not mandatory**. Teams may use heuristics, distance-based strategies, or prompt engineering instead. However, RL enables adaptive, learning-based policies that improve over game episodes.

### Fundamentals

**Three Building Blocks:**
- **State (s):** Current position of agent (row, col) and relative position of opponent (if known)
- **Action (a):** One of 4 cardinal directions + barrier placement (Cop only)
- **Reward (r):** Immediate score signal (0 for neutral moves, +20 for capture, -1 for inefficient moves, etc.)

**Example:** Agent learns that moving closer to opponent in certain grid configurations yields better long-term returns than random movement.

### Q-Table (Tabular Q-Learning)

**Data Structure:**
```
Q[state, action] = estimated future reward for taking action a in state s
```

**Dimensions (for 5×5 grid):**
- 25 states (grid cells)
- 4 actions (or 5 with barriers)
- Table: 25×4 or 25×5 matrix of floats

**Learning:** Update table after each move using **Bellman Equation:**

```
Q(s, a) ← Q(s, a) + α * [r + γ * max Q(s', a') - Q(s, a)]
```

Where:
- **α (alpha)** = Learning Rate (0.01 to 0.5) — How much new info overrides old
- **γ (gamma)** = Discount Factor (0 to 1) — Weight of future rewards
- **r** = Immediate reward
- **max Q(s', a')** = Best estimated future value from next state

**Epsilon-Greedy Policy:**
- Explore with probability ε: pick random action
- Exploit with probability 1-ε: pick highest Q-value action
- Decay ε over episodes to focus on learned policy

**Code Skeleton (from spec):**
```python
import numpy as np

num_states = 25
num_actions = 4
q_table = np.zeros((num_states, num_actions))

learning_rate = 0.1
discount_factor = 0.9

def update_q_table(state, action, reward, next_state, done):
    best_next_q = 0.0 if done else np.max(q_table[next_state])
    td_target = reward + discount_factor * best_next_q
    td_error = td_target - q_table[state, action]
    q_table[state, action] += learning_rate * td_error
```

**Advantage:** Enables agents to learn adaptive strategies without deep neural networks; simple, interpretable, low compute.

---

## Bonus Task: Inter-Group Competitive Matches

### What It Is

An optional competitive tournament where two independent teams (each with Cop + Thief servers) play against each **other's** agents (cross-team). Bonus points awarded based on aggregate performance.

### Rules

**Role Assignment (3+3 matches):**
- **Matches 1–3:** Team A's Cop vs. Team B's Thief
- **Matches 4–6:** Team B's Cop vs. Team A's Thief

**Scoring:**
- **Winner (higher aggregate score):** +10 points to final project grade
- **Loser:** +7 points to final project grade
- **Tie (identical scores):** +5 points each

**Multiple Matches Allowed:**
- Teams may compete against multiple opponents
- Bonus score = average of all completed matches
- Example: Team X plays 2 matches (wins 10, loses 7) → Bonus = (10+7)/2 = 8.5 points

**Report Requirements:**
- Both teams must submit separate email reports confirming exact same JSON results
- Disagreement/mismatch → 0 points to both teams for that series

### Deadline and Extension Incentive

- **Submission Deadline:** One week after assignment publication (approx. Friday, 26 June 2026, or adjusted per Moodle)
- **Earlier Deadline:** Friday 08:30 AM (before lecture) to allow in-class discussion
- **HW5 Extension:** Any team submitting a valid bonus match receives a +1 week extension on their HW5 deadline (applies only to those engaging in bonus)

---

## Mandatory Deliverables and Submission

### GitHub Repository Requirements

**Public repository on GitHub:**
- All source code (client, both MCP servers, game engine, config, utilities)
- Clear directory structure (recommended below)
- **README.md** (scientific documentation, see next section)

### README.md: Scientific Technical Report

**Language:** English, academic tone  
**Length:** Approx. 2–4 pages (not enforced, but comprehensive)

**Required Sections:**

#### 1. Formal Problem Modeling (Dec-POMDP)

Define the chase game as a **Decentralized Partially Observable Markov Decision Process:**

General tuple:
```
⟨n, S, {Ai}, P, R, {Ωi}, O, γ⟩
```

Where:
- **n:** Number of agents (2: Cop + Thief)
- **S:** State space (all valid grid configurations with both agents + barriers)
- **{Ai}:** Action sets for each agent (4 directions + barrier placement)
- **P:** State transition function (deterministic movement + barrier physics)
- **R:** Reward function (scoring table from spec)
- **{Ωi}:** Observation spaces (what each agent perceives locally; partial observability due to communication-only sensing)
- **O:** Observation function (maps state to observations per agent)
- **γ:** Discount factor (for RL, if used)

**Discuss:**
- Why it's a Dec-POMDP (agents operate independently with incomplete information)
- Partial observability challenge: agents only know opponent state from natural-language reports

#### 2. Orchestration Challenges

- Communication via free natural language (ambiguity, interpretation challenges)
- Ensuring mutual understanding between autonomous agents without rigid protocol
- Handling network latency / cloud deployment
- Synchronization between MCP servers

#### 3. Visualizations & Proof-of-Concept

- **Learning curves:** Q-table convergence over episodes (if RL used)
- **Game traces:** Screenshots of GUI showing board state progression
- **CLI logs:** Evidence of tool calls, message exchanges, successful completion
- **Statistical summary:** Win rates, average move counts, scoring trends

---

### Recommended Repository Structure

```
marl-cop-thief/
├── README.md                      # Scientific report
├── config.json                    # Game parameters (grid, moves, etc.)
├── requirements.txt               # Python dependencies
│
├── src/
│   ├── game_engine.py            # Core grid logic, win conditions
│   ├── game_client.py            # Main orchestrator (MCP Client)
│   ├── llm_interface.py          # LLM API calls (cloud or Ollama)
│   ├── q_learning.py             # Optional RL module
│   └── utils.py                  # Helpers, logging
│
├── mcp_servers/
│   ├── cop_server.py             # FastMCP server for Cop
│   ├── thief_server.py           # FastMCP server for Thief
│   └── mcp_common.py             # Shared MCP utilities
│
├── gui/
│   ├── grid_display.py           # Pygame/Tkinter visualization
│   └── assets/                   # Optional graphics
│
├── tests/
│   ├── test_game_logic.py        # Unit tests
│   ├── test_mcp_integration.py   # Integration tests
│   └── test_scenarios.py         # Specific game scenarios
│
├── reports/
│   └── game_reports.json         # Automatically generated reports
│
└── .github/workflows/            # Optional CI/CD

```

---

## Core Tasks & Engineering Priorities

**Recommended Development Order:**

| Stage | Focus | Deliverable |
|-------|-------|-------------|
| **1** | Game Engine & Grid Logic | Move validation, capture detection, barrier placement, state machine |
| **2** | MCP Infrastructure | Two separate FastMCP servers (Cop, Thief) with basic tools |
| **3** | Local Orchestration | Full game loop on localhost; agents communicating via MCP on different ports |
| **4** | Decision Mechanism | Heuristic strategy OR Q-Table OR prompt-based steering |
| **5** | Natural Language Integration | Replace position tuples with free-text message exchange |
| **6** | GUI (Optional) | Visual representation of grid, moves, messages |
| **7** | Cloud Deployment | Deploy MCP servers to Prefect Cloud / AWS; ensure public accessibility |
| **8** | Gmail Integration | Automated report generation and email dispatch |

---

## What Dr. Segal Emphasizes (Grading Focus)

### Central Value Proposition
> "The assignment's worth lies in the **orchestration capability**—the setup of two autonomous AI agents that coordinate a natural-language dialogue over remote MCP servers—NOT in the game outcome or optimal strategy."

### Grading Criteria (Ranked by Importance)

1. **Communication & Natural-Language Dialogue (Highest Weight)**
   - Agents exchange meaningful, contextual messages in free natural language
   - Messages demonstrate understanding (e.g., responses reference prior statements)
   - Avoid hardcoded, templated, or nonsensical text

2. **Orchestration Maturity (High Weight)**
   - Full end-to-end autonomous pipeline (init → play → report)
   - Two agents operate independently across isolated MCP servers
   - Proper separation of concerns (Client vs. Server, LLM vs. Tools)
   - Handles edge cases, errors, timeouts gracefully

3. **Modular, Configurable Architecture**
   - Game parameters driven by config file, not hardcoding
   - MCP servers are stateless and swappable
   - Code is clean, documented, testable

4. **Cloud Deployment & Security**
   - Agents can operate remotely (not just localhost)
   - Token-based authentication, no embedded secrets
   - Proper error handling for network conditions

5. **Game Strategy** (Lower Weight)
   - Winning or optimizing score is NOT the primary goal
   - Heuristic "dumb" agents are acceptable
   - RL is optional; emphasis is on the learning framework, not performance

---

## Watch Out / Common Pitfalls

- **Hardcoded board size:** Config must control grid dimensions
- **No real communication:** If agents exchange coordinates as JSON/tuples, mark as non-compliant
- **LLM in Server:** LLM must be in Client; Server only exposes tools
- **Single MCP server:** Two agents MUST have separate servers (design requirement, not optional)
- **Manual intervention required:** System must be fully autonomous; any need for user input = failure
- **Incomplete reports:** JSON must include all 6 sub-games, URLs, GitHub link, student names
- **Missing email dispatch:** Gmail integration is mandatory, not optional
- **No handling of partial observability:** Agents should struggle with incomplete info; natural-language interpretation is the challenge

---

## Standard Envelope & Rules

- **Moodle submission deadline:** Fri, 3 July 2026, 23:59 Israel time
- **Bonus deadline:** Fri, 26 June 2026, 08:30 (one week prior)
- **Late submission:** Standard course policy (check syllabus)
- **Resubmission:** Allowed until deadline; only latest version graded
- **Collab & Code Reuse:** Standard university integrity policy applies; cite any external libraries or inspiration

---

## Key Takeaway for Implementation

**Focus ruthlessly on orchestration, not game theory.** Build two agents that talk to each other via MCP in natural language, deploy them to the cloud, and let the pipeline run autonomously end-to-end. That alone is worth most of the grade. Strategy is a bonus.

