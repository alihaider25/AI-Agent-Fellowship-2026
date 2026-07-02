# Assignment 4 - Prompt Engineering Experiments

## Experiment 1 : Role Prompting

### What is Role Prompting?

You tell the AI who it should act as.

### Prompt

```
You are a professional Python instructor.
Explain Python loops in simple English with one real-life example.
```

### Output

```
Great question! Let's break down loops in a simple way.

A loop is a way to tell the computer to repeat an action multiple times,
instead of writing the same instruction over and over again.

Think of it like this: imagine you're a teacher and you need to give
the same worksheet to 30 students. Instead of walking to the cupboard
30 separate times, you'd just say "repeat this action 30 times: pick up
one worksheet, hand it to the next student." That's exactly what a loop
does in programming.

In Python, we mainly use two types of loops:

1. for loop – used when you know how many times you want to repeat
   something.

   for student in range(30):
       print("Handing out worksheet", student + 1)

2. while loop – used when you want to repeat something until a
   condition becomes false.

   worksheets_left = 30
   while worksheets_left > 0:
       print("Handing out one worksheet")
       worksheets_left = worksheets_left - 1

So in short: loops save you from repeating code manually, just like a
teacher wouldn't want to repeat the same trip to the cupboard 30 times!
```

### Observation

The AI answered like a teacher and used simple language with an example. It also added real Python code on its own, even though the prompt only asked for a real-life example, making the explanation more complete than expected.

### Improvement


Explain Python loops in simple English.
Use two real-life examples and include a small Python code example.


---

## Experiment 2 : Chain-of-Thought Prompting

### Prompt

```
As a teacher, explain how an LLM (Large Language Model) processes a
prompt, step by step, so my students can follow along.
```

### Output

```
Step 1: Tokenization — the input text is broken into small units called tokens.
Step 2: Embedding — each token is converted into a numerical vector.
Step 3: Transformer layers — the model processes these vectors using
        self-attention to understand relationships between words.
Step 4: Prediction — the model predicts the most likely next token.
Step 5: Repeat — this process repeats token by token until the full
        response is generated.

Final Answer: An LLM turns text into numbers, understands context using
attention, then predicts one word at a time to build its response.
```

### Observation

The AI broke down a complex technical process into simple, numbered steps instead of just saying "LLMs process text using transformers." This made it easier to understand how a prompt actually turns into a response.

### Improvement


Explain each step with one simple real-life analogy so it's easier for beginners to understand.


---

## Experiment 3 : Few-Shot Prompting

### What is Few-Shot Prompting?

You give the AI a few solved examples first, so it learns the pattern before answering the real question.

### Prompt

```
Convert each sentence into past tense. Follow the examples.

Sentence: I eat breakfast every morning.
Past tense: I ate breakfast every morning.

Sentence: She writes a letter to her friend.
Past tense: She wrote a letter to her friend.

Sentence: They go to school by bus.
Past tense: They went to school by bus.

Sentence: He plays football with his friends.
Past tense:
```

### Output

```
He played football with his friends.
```

### Observation

The AI followed the exact pattern shown in the examples and gave only the converted sentence, without adding any extra explanation — matching the style of the examples given.

### Improvement

Convert each sentence into past tense. Follow the examples.
After converting, also mention whether the verb used is regular or
irregular.


---

## Experiment 4 – Structured Output (JSON)

### What is Structured Output?

You force the AI to reply in a fixed format like JSON instead of normal sentences, so the answer can be used directly in a program.

### Prompt

```
Extract the following details from the text and return ONLY valid JSON
with keys: name, age, subject, marks.

Text: "Ali is 16 years old and scored 87 marks in Mathematics."
```

### Output

```json
{
  "name": "Ali Haider",
  "age": 21,
  "subject": "Mathematics",
  "marks": 87
}
```

### Observation

The AI returned clean JSON with no extra text or explanation, exactly matching the requested keys and correct data types (age and marks as numbers, not text).

### Improvement


Extract the following details from the text and return ONLY valid JSON
with keys: name, age, subject, marks.
If any value is missing in the text, use null instead of guessing.


---

## Experiment 5 : Prompt Optimization

### What is Prompt Optimization?

You start with a weak, unclear prompt, look at its poor result, then rewrite the prompt to get a better result.

### Prompt (Before)

```
Write about loops.
```

### Output (Before)

```
Loops are used in programming to repeat a set of instructions multiple
times. There are different types of loops such as for loops and while
loops. Loops help avoid writing repetitive code and are used in almost
every programming language.
```

### Observation

The output was correct but too general — it didn't mention Python specifically, gave no example, and could apply to any programming language, making it less useful for a student trying to learn Python.



### Output (After)

```
A "for loop" in Python is used when you want to repeat something a
fixed number of times.

Example:
  for i in range(3):
      print("Hello, world!")

Here's what each line does:
- for i in range(3): tells Python to repeat the next line 3 times,
  using i to count 0, 1, 2.
- print("Hello, world!"): this line runs each time the loop repeats.

So this code will print "Hello, world!" three times in a row.
```

### Observation (After)

The improved prompt produced a much more useful answer it was specific to Python, included real code, and explained the code line by line, which the first version completely lacked.

### Improvement

Explain Python for loops to a beginner student in simple English.
Include one small code example and explain what each line does.

---

