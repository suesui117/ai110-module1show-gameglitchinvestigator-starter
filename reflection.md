# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it? target was 75, when i entered 76, it prompt me to go higher.
- List at least two concrete bugs you noticed at the start 
  (for example: "the hints were backwards").
  attempt started at 1 when I haven't started.
  click on new game after winning doesn't give me a new game


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|-75| should accept only integers between 1 and 100 | accepted it and counted as one attempt | GO HIGHER! |
|76| prompt me to go lower | prompt me to go higher | GO HIGHER! |
| clicked on New Game | New Game should reset | New Game didn't reset | You already won. Start a new game to play again. |
| attempt was at 1 before starting the game | attempt count to be 0 before the game | attempt count is 1 before the game | attempt count is off by 1 |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

When an even integer was entered, it's casted to a string, so even if it matches thes target, it doesn't return True.
AI suggested to remove the conditional check e.g. if input % 2 == 0:...else... and removing the casting to string. It passed with the test case and I replayed the game.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I pointed out to AI that it accepts decimals, it initially fixed the one example I gave e.g. 6.6 was accepted when it shouldn't. So I tested it after the fix, and it was still accepting 6.1, so I had Claude Code fix again. It passed with the test case and I replayed the game.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed? replay the game with the same error deliberately and see if it's fixed.
  
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
    def test_6_point_6_is_rejected(self):
        ok, value, err = parse_guess("6.6", 1, 20)
        assert ok is False
        assert value is None
        assert err is not None

    def test_91_point_1_is_rejected(self):
        ok, value, err = parse_guess("91.1", 1, 100)
        assert ok is False
        assert value is None

- Did AI help you design or understand any tests? How?
It helped me design, but didn't explain it unless I specially ask for it.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit? Streamlit is dynamic because it reruns the script and uses session state as persistent memory, unlike react and Django, rather than requiring you to spin up a new session or portal.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - prompt AI to do one thing at a time, instead of multiple bugs because often times, they are interleaved. and doing multiple things might break everything and it becomes more difficult to debug.
- What is one thing you would do differently next time you work with AI on a coding task? I'd like ask it to shorten the explanation, and explain to me in layman's term. It gets verbose and I lose patience when reading it.
- In one or two sentences, describe how this project changed the way you think about AI generated code. It's very interactive and it has control if I allow it, instead of me searching and copying codes into ChatGPT, Claude Code works side by side with me, and it could run Bash commands, this really caught me by surprise. I find this powerful. I'm actually pretty pleased it could do that, often times its the virtual env setup or python library versions being incompatible threw me off. I ended up spending alot of time troubleshooting it. I didn't need to do that this time.
