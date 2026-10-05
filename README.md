# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

Users enter a description, size, and maximum price for a clothing item they are looking for. The system searches through available thrift listings, filters and scores the results, and stops gracefully if no matches are found. For valid matches, it automatically passes the item into an outfit suggestion tool that pairs the find with the user's existing wardrobe.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** 
               Search the listings data for items matching a description, and optionally a
               size and a price ceiling.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
               description: str,
               size: str | None = None,
               max_price: float | None = None,
- **Returns:** 
               A list of matching listing dicts, best match first.
- **When it has nothing:**
               Returns an empty list when nothing matches — an empty list, not None,
               and not an exception.** Your loop branches on this.

### `suggest_outfit`

- **What it does:**
               Given a thrifted item and the user's wardrobe, suggest one or two outfits.
- **Inputs:**
               new_item: dict
               wardrobe: dict
- **Returns:**
               A non-empty string with outfit suggestions.
- **When it has nothing:**
               With an empty wardrobe, return general styling advice rather than
               raising or returning "". Unit 4 has you trigger the empty wardrobe on
               purpose, so decide now what it should do.

### `create_fit_card`

- **What it does:**
             Creates a formatted text-based fit card combining an existing outfit 
             description with a newly added clothing item.
- **Inputs:**
             outfit: str
             new_item: dict
- **Returns:**
             A two-to-four sentence caption with a full outfit.
- **When it has nothing:**
             If `outfit` is empty or whitespace, return a descriptive message rather
             than raising.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
        If search_listings returns an empty list, put a message in
        session["error"] naming what the user could change, and return the
        session without calling suggest_outfit. Otherwise take the first
        result, put it in session["selected_item"], and continue

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
        Regex pattern matching and string splitting (parse_query()) extracts size and maximum price constraints while isolating the remaining keywords for listing search.

**What moves through the session:** <!-- which fields, in what order -->
       1. session["parsed"] — structured breakdown of the user's request.
       2. session["search_results"] — list of matching item dicts returned by search.
       3. session["selected_item"] — the top-ranking item dict chosen from the results (if any match).
       4. session["outfit_suggestion"] — string containing outfit advice combining the new item and wardrobe.
       5. session["fit_card"] — final social media caption string.
       6. session["error"] — error string populated if the search returns empty or the model is unavailable.
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'
python app.py ask 'vintage graphic tee under $30'
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 9 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print … +6 more
      →    9 match(es)
[3] select_item
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] suggest_outfit
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Since you didn’t list the specific items you own, I’ve put together two versatile outfit formulas using classi…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Scored this ultimate 2003 tour bootleg tee and I am obsessed with the faded vintage wash! Throw it on with som…

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Since you didn’t list the specific items you own, I’ve put together two versatile outfit formulas using classic pieces that pair effortlessly with a vintage 2003 bootleg-style graphic tee. 

You can easily swap these in for the equivalent items in your wardrobe!

### Outfit 1: Effortless & Edgy (Streetwear Vibe)
*Since the tee has a slightly boxy, worn-in fit, this look leans into that relaxed, effortless aesthetic.*

* **Top:** The Graphic Tee (let it hang loose for that authentic vintage drape).
* **Bottoms:** Relaxed-fit straight-leg jeans (light wash or vintage wash to match the faded tee).
* **Outerwear:** An oversized black leather biker jacket or a distressed denim jacket.
* **Shoes:** Retro sneakers (like Nike Dunks, Adidas Sambas, or chunky New Balances).
* **Accessories:** A minimalist silver chain necklace and a canvas crossbody bag.

### Outfit 2: Casual & Cool (Elevated Everyday)
*This look balances the casual nature of the graphic tee with cleaner lines for a put-together, smart-casual finish.*

* **Top:** The Graphic Tee (tucked in loosely with a "French tuck" at the front).
* **Bottoms:** Tailored wide-leg trousers or pleated chinos (in black, charcoal, or beige).
* **Outerwear:** A structured blazer (oversized) to add a cool high-low contrast against the bootleg tee.
* **Shoes:** Classic loafers or retro running shoes (depending on how dressy you want to go).
* **Accessories:** A leather belt with a simple buckle and a minimalist tote bag. 

*If you’d like to share the specific items you currently own from your list, let me know and I can tailor these exact combinations for you!*

  Fit card: Scored this ultimate 2003 tour bootleg tee and I am obsessed with the faded vintage wash! Throw it on with some relaxed denimand a leather jacket for instant off-duty edge, or dress it up with tailored trousers. Grab this piece now on my Depop for just $24.00 before it's gone! 🎸✨

2 model calls this session, 592 prompt + 465 output tokens

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

$ python -c "from tools import suggest_outfit; ..."
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Since you didn't list the specific items in your wardrobe, I have created a **classic, versatile, and effortlessly cool everyday outfit**built around the vintage Levi's 501s. 

Whenever you are ready, feel free to reply with the exact items in your closet (e.g., "a white tee, a black leather jacket, and Converse sneakers"), and I will tailor this specific to your wardrobe!

### The Outfit: **"The Effortless Casual-Cool Look"**

*   **The Base:** **Vintage Levi's 501 Jeans** (Medium wash with knee fading)
*   **Top:** A classic tucked-in **white t-shirt** (or a simple neutral top) to let the high-waisted vintage silhouette shine.
*   **Outerwear:** An **oversized blazer** or a **denim/leather jacket** layered on top for structure and contrast.
*   **Shoes:** **Retro sneakers** (like Adidas Sambas or white leather tennis shoes) or **classic loafers** to dress it up slightly.
*   **Accessories:** A **leather belt** (brown or black to match your shoes) tucked through the 501 loops, paired with a simple **gold necklace** or **crossbody bag**.

**Why it works:** Medium-wash 501s have an inherent casual, timeless vibe. Pairing them with a simple top, a structured layer (like a blazer or jacket), and defined accessories (like a belt) instantly elevates the vintage denim from "just running errands" to a chic, put-together street-style look. 

*Want a customized recommendation? Just reply with your actual items!*

```

```
$ python -c "from tools import create_fit_card; ..."
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
The search for the ultimate vintage 501s is officially over. Just paired these broken-in medium wash blues with my favorite white sneakers for that effortless 90s off-duty look. Snagged them on Depop for just $38 and I honestly might never take them off.

***

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* 
               I asked for the implementation of search_listings including the size filtering logic.
- *What came back:* 
               The initial implementation used a basic string replacement (item_size.replace('/', ' ').split()),  which failed to correctly parse comma-separated sizes or multi-space formats like "W30 L30" or "M, L".
- *What I changed:*
               I updated the size tokenization helper to use a regex split (re.split(r"[/,\s]+", cleaned)) so it robustly handles diverse listing formats without false negatives.

**Moment 2**

- *What I asked for:*
               Guidance on structuring the fallback prompt inside suggest_outfit when a user has a completely empty wardrobe.
- *What came back:*
               A basic fallback string like "Wardrobe is empty. Style this item.", which caused the language model to produce confusing output asking where the user's clothes went or complaining about missing data.
- *What I changed:*
               I rewrote the prompt branch to explicitly frame the model as a personal stylist giving standalone styling advice for the thrifted item alone, keeping the conversational persona intact even without existing wardrobe items to cross-reference.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
