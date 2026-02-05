# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
The hint was incorect. It would show the opposite of what the user should have noted to help themselves guess correctly. For example if you need to choose a lower number it would say "GO HIGHER" instead of Lower which is misleading. Also the "new game" button didnt work on my first run through.


- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I primarily used GitHub Copilot in VS Code as my AI teammate to analyze the codebase, explain logic, refactor functions, and suggest fixes. I also used ChatGPT only to help me word clearer prompts for Copilot when I needed to be more specific about what I was asking.
- Give one example of an AI suggestion you accepted and why.
Copilot suggested refactoring core game logic such as check_guess and parse_guess out of app.py and into logic_utils.py to separate UI and logic. This suggestion was correct because it made the code more readable and allowed me to write pytest tests that directly verified the game logic. I confirmed the suggestion was successful by running pytest and seeing all tests pass after the refactor.
- Give one example of an AI suggestion you changed or rejected and why.
At first, Copilot suggested that the incorrect hints were caused only by comparison logic inside check_guess, which was partially misleading. Although fixing the logic made the tests pass, the live Streamlit app still behaved incorrectly due to persistent widget state and how Streamlit reruns scripts. I verified this by comparing pytest results with live gameplay and then adjusted Copilot’s approach by clearing widget state on “New Game” instead of continuing to change the logic itself.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I considered a bug fixed only after both automated tests and the live Streamlit app behaved as expected. In this project, passing pytest alone was not sufficient because the app could still behave incorrectly due to Streamlit session state. I verified fixes by restarting the Streamlit server and playing multiple rounds to ensure the hints, score updates, and “New Game” behavior were consistent.
- Describe at least one test you ran (manual or using pytest)  
I ran pytest tests that directly called check_guess() with known inputs, such as a guess of 60 against a secret of 50. These tests showed that the function correctly returned the "Too High" outcome and a hint instructing the user to go lower. This confirmed that the game logic itself was correct and that any remaining issues were related to UI or session state rather than logic errors.
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
Copilot helped by suggesting simple, targeted pytest cases that isolated the logic from the UI, allowing me to verify behavior without relying on the Streamlit interface. It also helped clarify what inputs and expected outputs were most important to test, which made it easier to identify the difference between logic bugs and UI state issues.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret number appeared to change because Streamlit reruns the entire script whenever a user interacts with the app, and the “New Game” button regenerated the secret without clearing the existing input widget state. As a result, the same guess could be compared against a newly generated secret, making the hints appear inconsistent or reversed even when the logic was correct.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns the Python script from top to bottom every time the user clicks a button or submits input. Session state acts like short-term memory that lets the app remember values such as scores, attempts, or a secret number across those reruns. If something is not stored or reset properly in session state, the app can behave unpredictably even though the code looks correct.
- What change did you make that finally gave the game a stable secret number?
I fixed the issue by carefully controlling session state during “New Game” events and separating widget state from game state. Specifically, I reset the secret number only when starting a new game and updated the input widget key so old guesses were not reused after a rerun, which kept the secret and user input aligned.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  I want to continue writing small, targeted tests to verify core logic separately from the UI. This helped me quickly confirm whether a bug was in the logic or in the interface, which saved time during debugging.
- What is one thing you would do differently next time you work with AI on a coding task?
Next time, I would more quickly question AI explanations that focus only on logic bugs and actively consider environment or framework behavior, especially for stateful tools like Streamlit. I would also restart long-running processes earlier to rule out stale code issues.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project taught me that AI-generated code can appear correct and even pass tests while still behaving incorrectly in real applications. It reinforced that AI is best used as a collaborator whose suggestions must be verified through testing, inspection, and an understanding of the runtime environment.