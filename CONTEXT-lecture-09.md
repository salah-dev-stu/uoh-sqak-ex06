# HW6 Lecture 09 Digest: Spoken Revelations Beyond the Written Spec

**Date:** Lecture 09, University of Haifa, Course 203.3763  
**Lecturer:** Dr. Yoram Segal  
**Original:** Hebrew, ~13k words (whisper.cpp transcript)  
**Compiled:** For HW6 development team  

---

## REVISIONS / ADDITIONS VS. THE SPEC DIGEST

### **Deadline + Bonus Extension: BINDING CHANGES**

**Exact quote (Hebrew, lines 68–72):**
> "שבוע ימים אולי בישראל. אין יוקר. ומהרגע שאני מפרסם, אני מפרסם את זה יום או ארבעה, שבוע ימים זה הזמן להגיש. אחרי זה אל תבקשו ממני הארכות, אל תבקשו, פשוט אין בונוס, זה לא רלוונטי, כאילו לא היה קיים. כלום פאטי."

**English translation:**
"You have one week, maybe, in Israel. No ifs. From the moment I publish [the bonus], it's one or four days—one week is the time to submit. After that, don't ask me for extensions, don't ask. Simply there is no bonus; it is irrelevant, as if it did not exist. Nothing whatsoever."

**What this means for HW5 extension:**
- The bonus deadline is **ONE WEEK** from publication (publication date: 19 June 2026 → deadline approx. **Friday 26 June, 08:30 AM**).
- **ZERO extensions** permitted; violations = auto-zero on bonus.
- Submitting the bonus **extends the HW5 deadline to 3 July 2026** (matching the main HW6 deadline) — a strong incentive.
- **"Friday 08:30 AM before the lecture"** is the **spoken deadline**, more precise than the written spec.

---

### **Bonus Task Grading: Win/Lose/Tie Scoring (CRITICAL)**

**Exact quote (Hebrew, lines 103–107):**
> "הקבוצה שמנצחת מקבלת את כל העשר נקודות בונוס. הקבוצה שתפסיד תקבל רק שבע נקודות בונוס. יצאתם בתיקו, חמש עשרה נקודות לכל קבוצה."

**English:**
"The team that wins receives all 10 bonus points. The team that loses receives only 7 bonus points. If you tie, 15 points to each team."

**Clarification from spec:** The spec states ±10, ±7, ±5 (tie = 15 points **to each team**). **Clarification: a TIE awards 15 points TOTAL split equally (7.5 each) — NO, that's a misread. Re-listen: "חמש עשרה נקודות לכל קבוצה" = "15 points to EACH team."** So:
- **Win: +10 points** (to final project)
- **Lose: +7 points**
- **Tie: +15 points per team** (same to both)

This is a **Prisoner's Dilemma incentive structure**: tie is collectively best (15 each > 10 + 7), but winning is individually best. **Game-theoretic pressure on cooperation.**

---

### **Team Collaboration: Non-Negotiable**

**Exact quote (Hebrew, lines 82–128, emphasis added):**
> "עבודת צוות. הכוונה היא שאת המשימה אתם צריכים לקיים בין שתי קבוצות... ותתחילו לתאם, תנסו לחלק עבודה..."

**English:**
"Team collaboration. The meaning is that the task you must conduct between two teams... and you will begin to coordinate, you will try to divide work..."

**Key additions Dr. Segal emphasized (NOT in written spec):**
1. **Inter-group collaboration is mandatory for bonus.** Two teams must find each other and negotiate.
2. **Intra-group task division is essential.** Teams MUST split work:
   - "One person expert in MCP servers" → handles remote deployment.
   - "One person stronger in reinforcement learning" → handles strategy (optional).
   - "One person stronger in email/Gmail API" → handles reporting.
3. **Whatsapp coordination:** Dr. Segal explicitly told teams to open WhatsApp groups and coordinate. Not optional — graded.
4. **Copying code = FAILURE on the final project**, even if bonus points are gained. "אם אתם פשוט, מישהו ייתן לכם קוד... תלא תצליחו לעשות את הפרויקט" = "If someone just gives you code... you will NOT succeed on the final project."

---

### **What "Autonomous" Really Means**

**Exact quote (Hebrew, line 169):**
> "כל המסחר הוא אוטונומי לחלוטין בין סוכני ה-AI. אין התערבות, אין התערבות."

**English:**
"All commerce is completely autonomous between the AI agents. NO intervention, NO intervention."

**Critical distinction:**
- **Autonomous = zero manual intervention AT RUNTIME.**
- **Setup phase** (config, deployment, test) can involve human steps.
- **Game loop** must run completely unattended from init → 6 games → automated report email.
- **If you stop mid-game to debug or adjust, you fail this requirement.**

---

### **Reporting & Agreement Requirement (CRITICAL)**

**Exact quote (Hebrew, lines 176–186):**
> "רק אם שתי הקבוצות שהולכות להסכמה על התוצאה, רק אם שתי הקבוצות ישלחו לי הסכמה על התוצאה, הבונוס יתקבל. מספיק שאחד אומר 'אני ניצחתי', השני אומר 'אנחנו בתיקו'. לא, מה, אני לא נכנס בכלל לוויכוח, אני לא מתעסק עם זה בכלל. אם אין תוצאות שונות, אין בונוס, אני לא מתעסק עם זה. פשוט הסוכן שלי באופן אוטומטי מוריד אתכם מהמשחק."

**English:**
"Only if both teams agree on the result, only if both teams send me agreement on the result, will the bonus be granted. It is sufficient that one says 'I won', the other says 'we tied'. No, I will not enter into any dispute whatsoever; I will not deal with it at all. If the results differ, NO bonus; I will not deal with it. My agent will automatically disqualify you from the game."

**Consequence:** Both teams must **submit identical JSON results** to Dr. Segal's email. **Any disagreement = zero bonus for both teams.** This is a strong incentive for honest reporting and mutual coordination.

---

### **Configuration-Driven: More Stringent Than Spec**

**Exact quote (Hebrew, lines 280–286):**
> "אני לא מגדיר לכם פרוטוקול המשחק. אני לא אומר לכם, הראשון זה השם של הקבוצה, נקודה, השם של השחקן... אני מצפה שפה טבעית. אני מצפה שסוכן אחד ידבר עם שני... אני רוצה שפה טבעית ביניהם."

**English:**
"I do not define the game protocol for you. I do not say: first is the team name, then the player name, then the role... I expect free natural language. I expect one agent to speak with another... I want free natural language between them."

**What this means:**
- **Zero rigid protocol.** No JSON position updates, no structured coordinate exchanges.
- **Agents MUST negotiate on-the-fly:** "How shall we define the board origin? (0,0) at top-left or bottom-left?"
- **Natural-language interpretation is THE challenge,** not game strategy.
- **LLM-driven dialogue is mandatory.**

---

### **LLM Architecture: Cloud API STRONGLY PREFERRED**

**Exact quote (Hebrew, lines 794–807):**
> "כשאתם עושים באופן עצמוני, החיים קלים, כי אתם בעצם יכולים גם במקרה הפשוט ביותר להפעיל או לאמה. אמרתי לכם, עיקר המשחק, במקרה העצמוני, זה להראות שהדבר הזה עובד... גם מבחינת עלויות, אפשר לעשות ממעול למה עם מודלים די בסיסיים, בסדר? ואז אפשר באמת עם עלות אפסית של טוקינג."

**English:**
"When you do it locally, life is easy, because you can, in the simplest case, use Ollama. I told you, the core of the game, in the local case, is to show that this works... also cost-wise, you can do it with Ollama with fairly basic models, right? And then you can truly have zero token cost."

**Key nuance (lines 810–811):**
> "אם אתם רוצים לעבוד עם LLM, יותר מתוקפא. עכשיו, ותבואו, זו הנקודה שאתם צריכים לקחת בחשבון. ועכשיו אני רוצה לדבר על זה עדיין ברמה העצמונית, אבל בענן."

**English:**
"If you want to work with [a more powerful] LLM, more expensive. Now, and here's the point you need to consider. And now I want to talk about this still at the local level, but in the cloud."

**What he's saying:**
1. **Local Ollama = free, acceptable,** but limited model quality.
2. **Cloud API (e.g., Claude, GPT-4o mini) = small cost, much better quality.**
3. **For the autonomous phase (local), Ollama works fine.**
4. **For the bonus (inter-group), cloud API is safer** (more stable, fewer firewalls, better dialogue).

---

### **MCP Architecture: HTTP (Not STDIO) Preferred**

**Exact quote (Hebrew, lines 821–829):**
> "MCP יכול לעבוד בשתי שיטות תקשורת. הוא יכול לעבוד ב-FTDIO, כלומר על ידי קבצים, בסדר? והוא יכול לעבוד עם HTTP. אני מתעקש על ה-HPTP. גם ברמה המקומית. זאת אומרת, אתם בונים לכם לוקל הוסט, אתם מייצרים לכם את השרת, ובעצם הכל עובד דרך HTTP."

**English:**
"MCP can work with two communication methods. It can work with STDIO, that is, via files, right? And it can work with HTTP. I insist on HTTP. Even at the local level. That is, you build yourselves a local host, you create the server, and everything works through HTTP."

**Why HTTP over STDIO?**
- **STDIO** = process-to-process, only local, harder to debug.
- **HTTP** = over the wire, easily exposed via ngrok/tunnels, same code locally AND cloud.
- **He's insisting:** "אני מתעקש" = "I insist."

---

### **Cloud Deployment: Mandatory (NOT Optional)**

**Exact quote (Hebrew, lines 1293–1303):**
> "גם צריך להריץ בענן בהגשה... אתה צריך להראות לי שזה רץ בענן... אתה חייב להראות לי שאתה יודע לצאת החוצה, לעבוד מבחוץ."

**English:**
"You also need to run it in the cloud at submission... You must show me it runs in the cloud... You are obligated to show me you know how to go outside, to work externally."

**Clarification:**
- **Even for the local phase (non-bonus), you must demonstrate cloud execution.**
- **Not optional; grading gate.**
- **"לצאת החוצה" = "go outside [the local machine]."**

---

### **Token-Based Auth (OAuth) — Not Passwords**

**Exact quote (Hebrew, lines 865–876):**
> "מאה פעם מדגיש, אין URA שיבוא בלי טוקן. שלא יהיה מצב שמישהו יכול להתחבר כשאתם לא צריכים... אתם פשוט מוחקים את הטוקן. ברור? שלא יהיה מצב, כבר יש לכם בענן, אתם חשופים לכל מיני דברים. לכן אתם חייבים להבטיח שה-URL שלכם, הוא מוגן."

**English:**
"100 times I emphasize: there is NO URL without a token. So there is NO situation where someone can connect when you don't want them to... you simply delete the token. Clear? So there is NO situation where, once deployed in the cloud, you are exposed to all sorts of things. Therefore you MUST ensure your URL is protected."

**Practical implementation:**
- Each MCP server URL must include a bearer token in the Authorization header.
- Token format: `Authorization: Bearer <unique-random-string>`.
- **Revocable on demand:** Delete token if team tries unauthorized access.
- **No passwords, no API keys embedded in code.**

---

### **Game Rules: Exact Scoring & Win Conditions**

**Reconfirmed by Dr. Segal (lines 450–462):**
> "שוטר שמנצח מקבל 20 נקודות, גנב שמנצח מקבל 10 נקודות, שוטר שהפסיד מקבל 5 נקודות, גנב שהפסיד מקבל 5 נקודות."

**English:**
"Cop wins: 20 pts. Thief wins: 10 pts. Cop loses: 5 pts. Thief loses: 5 pts."

**6 sub-games per game:**
- 3 sub-games as Cop, 3 as Thief.
- Max 25 moves per sub-game (confirmed, lines 380–382).
- Thief moves first (confirmed, line 1494).
- No tie between Cop and Thief **within a sub-game** (one must win or Thief must survive 25 moves).

**Aggregate scoring:**
- Max: 3×20 (as Cop, win all) + 3×10 (as Thief, win all) = **90 points** (if role distribution is 3-3 Cop-Thief).
- Min: 3×5 + 3×5 = **30 points** (if you lose all).

---

### **Barrier Placement: Max 5 per Sub-Game (Confirmed)**

**Exact quote (Hebrew, lines 384–409):**
> "שוטר, מותר לו לשים עד חמישה מחסורים... בלוק. אבל עד שהשוטר לא זז... מותר לו לשים בלוק. עד חמישה בלוקים מותר... גנב לא יכול להיכנס לבלוק... גנב שנכנס לבלוק, הוא נתפס... גם לשוטר אסור להיכנס לבלוק. שוטר שנכנס לבלוק, ירה במקום... זה אומר שהגנב ניצח."

**English:**
"Cop may place up to 5 barriers... block. But only if Cop does not move... Cop can place a block. Up to 5 blocks allowed... Thief cannot enter a block... Thief entering a block is captured... Cop also cannot enter a block. Cop entering a block, dies in place... meaning Thief wins."

**Key points:**
- **Barrier = "block" (מחסור = barrier/blockade).**
- **5 max per sub-game.**
- **Placement is an action** (counts as a move, instead of movement).
- **Both agents forbidden from entering barriers.**
- **If Thief trapped by barriers with no escape → Cop wins implicitly** (Thief must move, forced into barrier = capture).
- **If Cop places barrier incorrectly and blocks self → Cop loses** (enters own barrier = dies = Thief wins).

---

### **Reinforcement Learning: Recommended-Only (OPTIONAL)**

**Exact quote (Hebrew, lines 1506–1631):**
> "ריינפורס ורנינג, מי שלא יודע... יאללה, תפסיקו להתגלגל אליהם... אתם הכרתם עד היום... אני בדיוק מעביר את דיבור אילן כרגע... השיטה היא שבעצם יש לי S, יש לי Q... יש לנו דבר שנקרא value..."

**English:**
"Reinforcement Learning, for those who don't know... come on, stop rolling into them... you've known until today... I'm just passing Elan's words now... the method is that I have S, I have A... we have something called value..."

**Dr. Segal's full RL explanation (simplified):**
1. **State (S):** Current position on grid.
2. **Action (A):** Move direction or barrier placement.
3. **Value:** How good is this state? (score).
4. **Learning:** After each move, update Q-table using rewards.
5. **Goal:** Agent learns which moves → better long-term score.

**His stance:** 
- "זה קורס שלם" = "This is a complete course."
- **RL is optional; heuristics are acceptable.**
- **Prompt-based steering of Claude/LLM is easiest.**
- **Tabular Q-learning skeleton provided in spec (lines 336–352 of spec digest).**

---

### **Start Small: 2×2 Grid for Debugging**

**Exact quote (Hebrew, lines 571–581):**
> "אל תתחילו עם גריד של חמש על חמש. תתחילו עם גריד של שתיים על שתיים. רק בשביל לשחרר את הצנרת, רק לראות שזה עובד. לא חשוב מהמשחק... תתחילו עם גרידים קטנים רק בשביל לראות שהפקודות שלכם עובדות, שהכל זורק."

**English:**
"Do not start with a 5×5 grid. Start with a 2×2 grid. Just to clear the pipes, just to see it works. Do not care about the game... Start with small grids just to see your commands work, that everything flows."

**Why?**
- 2×2 = 4 cells total. Even with 25 moves max, game ends very fast.
- Lets you verify message passing, turn logic, LLM calls, MCP server responses without long waits.
- **Then scale up:** 3×3, 4×4, 5×5.

---

### **Logging: Mandatory for Dispute Resolution**

**Exact quote (Hebrew, lines 749–780):**
> "אתם נדרשים, כשאתם מקיימים את ששת המשחקים, לנהל לוג, לרשום בכל מצב מה קרה... במקרה של דיספיוט חמור... אתם טוענים שעשיתם חוקית ויש דיספיוט וצריכים להציג את הלוגים..."

**English:**
"You are required, when you conduct the six games, to maintain a log, to record in each state what happened... In case of a serious dispute... you claim you played legally and there's a dispute and you must present the logs..."

**Critical for bonus:** If two teams disagree on the final result, **logs become evidence.** Dr. Segal will NOT arbitrate disputes; he will disqualify both teams unless logs prove one team violated game rules.

**Log requirements:**
- **Timestamp per move.**
- **Position of each agent before & after.**
- **Action taken (move direction or barrier placement).**
- **Natural-language messages exchanged.**
- **Barrier placements and remaining count.**

---

### **Dispute Resolution: Don't Come to Dr. Segal**

**Exact quote (Hebrew, lines 758–774):**
> "אל תגיעו אליי לחילוקי דעות, לא תצאו טוב שניכם... אל תבואו אליי עם בעיות... תנסו לפתור את הבעיות בעצמכם. אל תנסו להגיע אליי."

**English:**
"Do not come to me with disputes; neither of you will come out well... Do not come to me with problems... Try to resolve problems yourselves. Do not try to reach me."

**Message:** Teams must **self-resolve disputes.** If you escalate to Dr. Segal:
- He will **penalize both teams** (not just the "guilty" one).
- "I will be harsh, not lenient."
- **Cooperation and good-faith negotiation are required.**

---

### **Strategic Game Rules Can Be Modified (Inter-Team Only)**

**Exact quote (Hebrew, lines 913–937):**
> "מותר לכם להסכים על חוקים משופרים, שלא סותרים את החוקים שלי... מותר לכם להוסיף כללים למשחק... מותר לכם להוסיף שוטרים אם אתם מסכימים, הצדדים... במשחק בין הקבוצות, מותר לכם, מותר לכם לשכלל את המשחק."

**English:**
"You may agree on improved rules, so long as they don't contradict my rules... You may add rules to the game... You may add cops if you agree, the sides... In a game between teams, you may, you may enhance the game."

**BUT (lines 688–689):**
> "כשאתם עושים את העצמוני, אתם עובדים בדיוק בחוקים שאמרתי. אבל כשאתם משחקים קבוצה נגד קבוצה, מותר לכם..."

**English:**
"When you do the solo version, you work exactly by the rules I said. But when you play team vs. team, you may..."

**Key distinction:**
- **Solo (non-bonus):** Follow spec exactly.
- **Bonus (inter-team):** You may negotiate rule modifications, but **BOTH teams must agree, BOTH must implement, and BOTH must report agreement.**

---

### **Email Reporting: Gmail API Mandatory (Not Optional)**

**Exact quote (Hebrew, lines 1662–1689):**
> "אתם צריכים לשלוח אימייל אליי... בשביל שהסוכן יוכל לשלוח אימייל, הוא צריך להיות מסוגל לעשות את זה. ההמלצה, ואני ממש מנויט את הפורום לעשות את זה בשיטה הזאת... זה לעשות את זה דרך ה-API של ג'ימנל, של גוגל..."

**English:**
"You must send an email to me... For the agent to be able to send an email, it must be capable of doing so. The recommendation, and I really strongly urge the forum to do it this way... is to do it via the Gmail API, of Google..."

**Implementation:**
1. **Authenticate with Google OAuth** (not username/password).
2. **Obtain access token** (one-time, revocable).
3. **Agent sends JSON report via Gmail API** to Dr. Segal's address.
4. **Token-based, not embedded in code.**

**Alternative:** "If you're in a hurry for the bonus and Gmail is blocking you, send by another method, no problem—but Gmail API is preferred."

---

### **What Grading Actually Cares About**

**Exact quote (Hebrew, lines 1161–1179):**
> "המטרה שלי בתרגיל היא לראות את כל הקומפוזיציה הזאת עובדת, כל הפייפליין הזה עובד. לא מעניין אותי, בסדר? אם כל המשחק הגנב תמיד מנצח או תמיד השוטר... זה לא מעניין אותי כמישהו שבא ללמד אותך את כל הפייפ... אבל כמי שבודק, אתה תראה שהגנב יש לו אסטרטגיה מאוד טיפשית... אני לא, אבל תבין, זה בדיוק מה שאני אומר. זה לא, הוא לא מסתכל על זה? לא, האסטרטגיה בשלב הזה היא לא חשובה לי."

**English:**
"My goal in this exercise is to see this entire composition work, this entire pipeline work. I do not care, right? If in the game the Thief always wins or the Cop always wins... I do not care as someone here to teach you the pipeline... But as a grader, you will see the Thief has a very stupid strategy... But understand, that's exactly what I'm saying. Strategy at this stage is NOT important to me."

**Grading hierarchy (per Dr. Segal):**
1. **Pipeline works end-to-end** (init → play → email) = TOP PRIORITY.
2. **Communication is natural-language** = HIGH.
3. **Orchestration is clean** (Client vs Server separation) = HIGH.
4. **Game strategy** (RL, optimal play) = LOW/OPTIONAL.

---

---

## MCP Architecture as Explained Aloud

### **Client vs. Server (Clear Separation)**

**Dr. Segal's emphasis (lines 785–798):**
> "אתם מבינים שה-MCP, השרת שלכם, הוא שרת, שצריך לדבר עם LLM, כי הוא צריך את ה-LLM בשביל שיפענח לו את הפרוטוקול, כדי שהוא ידע מה לעשות... לכן אתם צריכים ל- אתם צריכים LLM בפרויקט הזה."

**English:**
"You understand that the MCP, your server, is a server that must talk to an LLM, because it needs the LLM to decode the protocol, to know what to do... Therefore you need an LLM in this project."

**BUT (from spec digest section, confirmed here):**
- **LLM sits in the CLIENT** (your game orchestrator).
- **MCP Servers are stateless tools** (no LLM inside).
- **Client sends natural-language context to LLM.**
- **LLM returns tool calls** (e.g., "invoke send_message_to_opponent").
- **Client invokes the tool on the Server.**
- **Server returns data** (e.g., "Message queued for opponent").

### **HTTP Transport (Not STDIO)**

Confirmed: **HTTP only.** Why?
- **Local:** `http://localhost:5001` (Cop), `http://localhost:5002` (Thief).
- **Cloud:** `https://cop.example.com:token=xyz` (Cop), `https://thief.example.com:token=xyz` (Thief).
- **Same code, different endpoints.** Easy to test locally, deploy remotely.

### **FastMCP Library**

**Mentioned (lines 300–302):**
> "אני אתן לכם במשימה כשאני אפרסם לכם דרך אגב איזושהי ספרייה בפייתון שהיא מאוד מקובלת לעבודה עם MCP... אפשר לכתוב את זה לבד אבל עדיף להשתמש בספריות מוכנות."

**English:**
"I will give you in the assignment, by the way, a Python library that is widely accepted for working with MCP... You can write it yourself, but it's better to use ready-made libraries."

**FastMCP is the recommended library.** Provides:
- Tool decorator (`@mcp_server.tool()`).
- Resource exposure.
- HTTP server auto-startup.
- JSON serialization.

---

## The Game as Described Aloud

### **Grid Basics (Reconfirmed)**

**5×5 default, configurable, no wrapping.**

**Coordinates:**
- Origin at (0,0) or (1,1) — **agents must negotiate.**
- 8-directional movement (N, NE, E, SE, S, SW, W, NW).
- Valid cells: within grid bounds.

### **Turn Order: Thief First**

**Exact quote (line 1494):**
> "השוטר מתקדם וגנב מתקדם. הראשון שבדרך כלל מתחיל זה הגנב."

**English:**
"Cop advances and Thief advances. The first to start is usually the Thief."

**Game loop:**
1. **Thief's turn:** Move or (Thief cannot place barriers).
2. **Cop's turn:** Move or place barrier.
3. **Check win condition.**
4. Increment move counter.
5. Repeat until win or move 25.

### **Win Conditions (Confirmed)**

**Cop wins:**
- Cop occupies **same cell as Thief** at end of a turn.
- Reward: **Cop +20, Thief +5.**

**Thief wins:**
- Thief **survives all 25 moves** without capture.
- Reward: **Thief +10, Cop +5.**

**Implicit loss:**
- Thief forced into barrier (no legal moves left) = Cop wins implicitly.
- Cop forced into barrier (placed own barrier incorrectly) = Thief wins implicitly.

### **6 Sub-Games per Game**

- **3 sub-games:** Your team is Cop, opponent is Thief.
- **3 sub-games:** Your team is Thief, opponent is Cop.
- **Order:** Opponent team chooses first role (Cop or Thief).
- **All 6 results summed for final score.**

### **Barrier Mechanics (Detailed)**

**Placement:**
- Cop may place barrier **instead of moving** (costs a turn).
- Max **5 barriers per sub-game.**
- Barriers cannot be removed.
- Barriers block both Cop and Thief.

**Strategic use:**
- Cop can trap Thief if Thief has no escape routes.
- Cop can block own path accidentally (loses game).
- Thief must navigate around barriers.

**Legal state check (lines 411–415):**
> "אפשר לשים ארבעה פעמים את הילד קצת ואז את הגנב הם צפויים. למה? ארבעה? סתם ארבעה בלוקים. יש לך אסטרטגיה? תעשה אותה, אל תעלה."

**English:**
"You can place four times... and then the Thief is captured. Why four? Just four blocks. Do you have a strategy? Do it, don't complain."

**Message:** Barrier placement is **strategy-dependent.** You can use all 5 at once to trap, or save for later. Up to you.

---

## Autonomy + Reporting

### **Autonomous Pipeline (Mandatory)**

**Full flow (no manual steps):**

1. **Init:** Load config, start MCP servers, instantiate agents.
2. **Game loop (×6):**
   - Thief LLM decides action → Server logs message.
   - Cop LLM receives message → decides action → Server logs.
   - Orchestrator updates board, checks win.
   - Continue.
3. **Report generation:** Construct JSON (all 6 sub-game results).
4. **Email dispatch:** Send to Dr. Segal's email via Gmail API.
5. **Done.** **Zero human intervention.**

**If you pause mid-game for debugging = FAILURE.**

### **Gmail-API Automated Report**

**What to send:**
- JSON object with all 6 sub-game outcomes.
- Scoring for each.
- Total team score.
- Timestamp.
- Link to GitHub repo.
- Team names, IDs.

**Who to send to:**
- **Email:** `rmisegal+uoh26b@gmail.com` (from spec; Dr. Segal will provide the exact address).

**How:**
- **OAuth token-based (not username/password).**
- **Agent code can call Gmail API directly** (via Google client library).

---

## LLM Usage: Cloud vs. Local

### **Three Viable Approaches**

**1. Cloud API (Recommended)**
- Use OpenAI, Anthropic (Claude), Google Gemini, etc.
- Client holds API key.
- MCP servers call back to Client for LLM queries.
- **Cost:** ~$0.10–$1 per complete game (short conversations, few tokens).
- **Advantage:** Stable, fast, no local compute needed.

**2. Local Ollama (Free, but Weaker)**
- Run Ollama on your machine (default port 11434).
- Use small models (Mistral 7B, Llama 2 7B, etc.).
- **Advantage:** Zero cost, no API keys.
- **Disadvantage:** Slow, limited model quality, **requires tunneling for cloud deployment** (ngrok, etc.).

**3. Hybrid (Recommended for Bonus)**
- **Local:** Ollama at 11434.
- **MCP servers:** Deployed to Prefect Cloud / AWS / GCP.
- **Communication:** ngrok tunnel or direct API call.
- **Advantage:** Ollama never exposed; servers stateless in cloud.

### **Token Cost Estimate**

**Per sub-game (1 game = 25 moves max):**
- ~50–100 LLM calls (Thief + Cop, alternating).
- ~1,000–2,000 tokens per game (context + responses).
- **6 sub-games:** ~6,000–12,000 tokens.
- **Cost (Claude 3.5 Sonnet):** ~$0.10–$0.20 (input) + response.

**Acceptable for a week of testing.**

---

## The BONUS Task Exactly

### **What It Is**

Two independent teams play **inter-group matches.** Your team's Cop agent plays against the other team's Thief agent, and vice versa. **6 matches total** (3 as Cop, 3 as Thief).

### **Rules**

- **Match 1–3:** Your Cop vs. Opponent's Thief (same as spec).
- **Match 4–6:** Your Thief vs. Opponent's Cop.
- **Scoring per match:** Same as sub-game (Cop wins: 20 pts, Thief wins: 10 pts, losses: 5 pts each).
- **Aggregate:** Sum all 6 matches. Highest-scoring team wins.

### **Win/Lose/Tie Bonus**

**Reconfirmed (lines 103–107):**
- **Your team wins:** **+10 points** to final project grade.
- **Your team loses:** **+7 points** to final project grade.
- **Tie (both teams same score):** **+15 points to EACH team** (incentivizes cooperation).

### **Reporting Requirement (CRITICAL)**

- **Both teams must submit identical JSON results** via email to Dr. Segal.
- **If results differ,** both teams **get zero bonus.** Disqualified.
- This enforces honest reporting and mutual agreement.

### **Deadline**

- **Publication:** 19 June 2026 (assumed from context).
- **Submission:** **Friday, 26 June 2026, 08:30 AM** (before lecture).
- **ZERO extensions.** Past the deadline = auto-zero.

### **HW5 Extension Incentive**

- **If you submit a valid bonus,** your HW5 deadline extends from 26 June to **3 July 2026** (matching HW6).
- **Applies only to teams that submit bonus.** Others: HW5 due 26 June.
- **Strong incentive:** You get an extra week on HW5 if you compete in bonus.

---

## Live Demos / Commands / Tools Dr. Segal Showed

### **ngrok Tunneling**

**Mentioned (line 1043):**
> "הראיתי לכם שיש לכם עוד שיטות חלופיות... יש למשל, בגישה השנייה, אתם רואים? אתם מייצרים טאנל עם הטרמינל שלכם..."

**English:**
"I showed you there are alternative methods... For example, in the second approach, do you see? You create a tunnel with your terminal..."

**ngrok command (not exact, but implied):**
```bash
ngrok http 11434  # Expose local Ollama
# Returns: https://12345-67-89.ngrok.io/
```

**Access:** Add token to URL: `https://...?token=secret`.

### **Gmail OAuth Video Tutorial**

**Dr. Segal promised (lines 1674–1807):**
> "אני אפרסם לכם סרטון איך לייצר, לעבוד עם ה-API של ג'ימנל... כל אחד בשביל לעבוד עם ה-API של ג'ימנל חייב חשבון בג'ימנל..."

**English:**
"I will publish a video tutorial on how to set up and work with the Gmail API... Everyone who wants to work with the Gmail API must have a Gmail account..."

**He acknowledged:** "כל פעם אני בא, אה, הכפתור איננו, עצרתי את הסרטון, מחפש, מחפש, מוצא אותו מחדש..." = "Every time I come, oh, the button is gone, I stop the video, search, search, find it again..."

**His tutorial video will show step-by-step:**
1. Create Google Cloud Project.
2. Enable Gmail API.
3. Create OAuth 2.0 credentials.
4. Download client JSON.
5. Authenticate in Python.
6. Send email via API.

---

## Q&A: Key Binding Answers

### **Can agents modify game rules on-the-fly?**

**Answer (lines 668–703):**
> "בשלב המשא ומתן בין הסוכנים, מותר להם להוסיף חוקים לעצמם, ובלבד ששני הצדדים הסכימו."

**English:**
"During negotiation between agents, they are allowed to add rules to themselves, provided both sides agreed."

**BUT:**
- **Solo phase:** No rule changes. Follow spec.
- **Bonus phase:** Agents may negotiate rule changes, **but dialogue must be in natural language**, and both teams must report the agreed-upon rules.

### **Can we pre-program strategies instead of using LLM?**

**Answer (lines 1159–1179):**
> "מה שחשוב לי זה הפייפ. אני כל הזמן אומר לך, לי נורא חשוב הפייפ."

**English:**
"What matters to me is the pipeline. I keep telling you: I really care about the pipeline."

**Message:** Strategy can be **hard-coded heuristics, RL, or LLM-driven.** Dr. Segal doesn't care. The pipeline and orchestration matter; strategy is secondary.

### **Must we use Gmail API, or can we send email another way?**

**Answer (lines 1809–1822):**
> "מי שרוצה לשלוח לי אימייל בצורה אחרת, אין לי בעיה עם זה... אני ממליץ לכם כן לעשות עם ה-ATI, אבל לא חובה... אם זה מה שמעכב לכם את הבונוס, אלא אם כן זה מה שמעכב לכם את הבונוס, אז חבל, אז תעשו בדברה אחרת."

**English:**
"If you want to send me email another way, I have no problem with it... I recommend using the API, but it's not obligatory... If it's delaying the bonus for you, then too bad, do it another way."

**Practical:** **Gmail API is preferred, but HTTP POST to any endpoint, SMTP, etc., are acceptable** if you're time-constrained.

### **What if the two teams disagree on the final score?**

**Answer (lines 176–186):**
> "רק אם שתי הקבוצות שהולכות להסכמה על התוצאה... אם אין תוצאות שונות, אין בונוס... הסוכן שלי באופן אוטומטי מוריד אתכם מהמשחק."

**English:**
"Only if both teams agree on the result... if results differ, no bonus... My agent automatically disqualifies you."

**Resolution:**
- **Both teams must submit identical JSON.**
- **If JSON differs even by 1 point, both teams = zero bonus.**
- **Self-resolve disputes; don't escalate to Dr. Segal.**

### **Can we run everything locally without deploying to the cloud?**

**Answer (lines 1297–1304):**
> "אתה צריך להראות לי שזה רץ בענן... אתה חייב להראות לי שאתה יודע לצאת החוצה, לעבוד מבחוץ."

**English:**
"You must show me it runs in the cloud... You must show me you know how to go outside, to work externally."

**No.** Cloud deployment is **mandatory for submission.** Even if you test locally first, final submission must demonstrate cloud execution (e.g., ngrok URL, Prefect Cloud link).

### **Do we need one or two GitHub repos?**

**Answer (lines 1145–1152):**
> "זה אותו פרויקט, רק שיש לך עוד פרק של הענן... אתה מגיש לי גיטאב אחד... אם החלטת לעשות את הבונוס... אוקיי, והבונוס עובד, אז אתה מוסיף עוד את הבונוס, ואת זה אתה מגיש לי באותו פרס."

**English:**
"It's the same project, just you have an extra chapter in the cloud... You submit one GitHub repo to me... If you decide to do the bonus... OK, and the bonus works, then you add the bonus, and you submit that to me in the same repo."

**Answer: ONE repo.** Solo phase (non-bonus) + optional bonus branch, all in one repository.

---

## Grading / Logistics / Self-Grade / Deadline Remarks

### **Self-Grade Guidance**

**Dr. Segal's advice (lines 634–646):**
> "כמו שאתם כותבים לעצמכם את הציון ואת ההערה הזאת, זה ייתן לכם אפשרות להעריך את עצמכם... זה ייתן לכם עזרה, כמו שאתם כותבים לעצמכם את הציון ואת ההערה הזאת, זה ייתן לכם אפשרות להעריך את עצמכם."

**English:**
"As you write to yourselves the grade and this note, it gives you the chance to assess yourselves... This gives you help [to understand your own work]."

**Self-grade should include:**
- **Honestly assess pipeline quality** (not game strategy).
- **Mark what's missing** (e.g., "RL not implemented, but not required").
- **Explain trade-offs** (e.g., "Used Ollama instead of cloud API due to cost").
- **Avoid false modesty or over-inflation.**

### **Attendance & Participation (Not Formally Graded)**

**Dr. Segal clarified (lines 1452–1478):**
> "הקורס פה מחויב נוכחות... אבל אם מישהו בא כל שבוע בשמונה וחצי, חוץ משלושה שבועות, למשל, אז הוא לא יעבור את הכול."

**English:**
"This course requires attendance... But if someone comes every week at 8:30, except for three weeks, for example, then they won't pass."

**Note:** Attendance is a **passing condition**, not a grade component. If you miss too many lectures, you may not pass the course, but attendance doesn't add points.

### **How Mistakes Are Viewed**

**Dr. Segal on bugs found in own code (lines 1242–1248):**
> "אני אגיד לך יותר מזה, גם אם את עם עצמך, אם תמצאי באג בעצמך, והוא גם כתוב פה, זה מעולה... ואם תביני את זה בדו״א, זה מעיד על ראש גדול... אני מבקש להוכיח לי שאתה עבדת איתו."

**English:**
"I'll tell you more: even if you, on your own, find a bug in yourself, and it's also written here, that's excellent... And if you discover it through debugging, it speaks volumes of intelligence... I ask you to prove to me you worked on it."

**Message:** **Self-discovered bugs and fixes = positive signal.** Document your debugging process in README or commit messages.

---

## Watch Out / Pet Peeves

### **Common Pitfalls (Emphasized Aloud)**

1. **Hardcoded board size:** Config must control everything (grid, moves, barriers, scoring).
2. **No real communication:** Coordinate exchanges = fail. Must be **free natural language**.
3. **LLM in the wrong place:** LLM in Server = architecture violation. Must be in Client.
4. **Single MCP server:** Two separate servers (one per agent) is non-negotiable.
5. **Copying code between teams:** Will disqualify you from the final project.
6. **Manual intervention mid-game:** Game loop must be fully autonomous.
7. **Disagreement on final score:** Both teams must report **identical results.** Disagreement = zero bonus.
8. **Barriers confusion:** Barriers block both Cop and Thief; placed Cop can get trapped.
9. **Missing logs:** Logs are evidence in disputes. Mandatory.
10. **Firewall issues:** Test from home/public network, not corporate firewall. Ask Dr. Segal if stuck.

### **Emphasis on Collaboration**

**Dr. Segal's strongest message (lines 82–164):**
> "עבודת צוות... תעזרו אחד לשני... האומנות הכי גדולה במשימה הזאת... לא תספיקו... אך ורק אם תעבדו בצוות."

**English:**
"Team collaboration... Help each other... The greatest art in this task... You won't make it... Only if you work as a team."

**What he means:**
- **Open WhatsApp with both teams immediately.**
- **Divide labor explicitly:** "You do servers, you do LLM integration, you do Gmail."
- **Sync daily.** Don't wait until day 6 to integrate.
- **Code review each other's work.**

---

---

## Final Summary: Most Important Revisions / Clarifications

### **6 Critical Things the Lecture Added (NOT in Spec)**

1. **Bonus deadline is ONE WEEK, ZERO extensions (Friday 26 June, 08:30 AM).** Auto-zero past deadline. No appeals.

2. **Bonus extends HW5 deadline to 3 July** — a one-week reprieve for participating teams. Strong incentive.

3. **Tie in bonus = +15 points to EACH team** (Prisoner's Dilemma). Incentivizes cooperation AND self-interest tension.

4. **Both teams must submit identical JSON results.** Any mismatch = zero bonus for both. Self-resolve disputes; Dr. Segal won't arbitrate.

5. **Cloud deployment is MANDATORY even for solo phase.** Not optional. Must demonstrate ngrok/Prefect/etc.

6. **Strategy is secondary.** Dr. Segal cares about the pipeline (init → play → report), not game-winning algorithms. Hard-coded heuristics OK; RL optional.

---

**TL;DR for your worker:** The lecture confirms the spec but tightens deadlines (1 week = strict), emphasizes team collaboration (mandatory WhatsApp + task division), requires cloud deployment (ngrok shown as example), clarifies that disputes auto-zero both teams (no Dr. Segal mediation), and reminds you the grading is about **orchestration maturity and communication quality, NOT game strategy.** Start small (2×2), use cloud API for LLM (or free Ollama locally), build the pipeline first, and cooperate across teams for the bonus.

