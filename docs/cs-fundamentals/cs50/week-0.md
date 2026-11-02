---
title: "CS50 Week 0: Thinking Before Coding"
date: 2026-10-27
categories:
  - CS Fundamentals
description: "My notes from CS50 Week 0: why foundations still matter in the age of AI, how computers represent information, and what makes an algorithm good."
reading_time: 5
icon: lucide/graduation-cap
tags:
  - CS50
share_image: assets/cs50/week0/share.jpg   # link preview (LinkedIn, X, WhatsApp) instead of the generated card
share_image_alt: "CS50 Week 0: Thinking Before Coding, with a stack of handwritten notebook pages"
social:
  cards: false
notes:
  path: assets/cs50/week0
  pages:
    - "Why foundations still matter"
    - "Computer science, problem solving and binary"
    - "Counting in binary, bytes and ASCII"
    - "Unicode, colors, video and music"
    - "Algorithms, design, code and pseudocode"
---

> You're still in the driver's seat: the conductor, the pilot.

These are my notes from Week 0 of [CS50x](https://cs50.harvard.edu/x/), Harvard's introduction to computer science, taken by hand and typed up here. I stopped before the Scratch section; the ideas below are what stuck with me.

---

## Why foundations still matter

Over the past few years, AI has been seen as a game changer for programming. That's true, and it will stay true. You can ask the computer to find bugs, spot mistakes or add a feature, and it does.

We humans have long been the bottleneck in this industry. There are only so many of us, and there are always more bugs to fix and more features to build.

So why learn the basics at all? Because introductory courses like CS50 or SICP were never really about programming. Programming is a byproduct. The real goal is learning how to think: how to take an input, turn it into the correct output, and master the tools along the way.

By the end, you don't just know a few languages. You can teach yourself new things and tell the computer, more and more precisely, what you want. With AI or without it, you're still the one who knows what you're talking about and what can actually be solved. Master the ideas, then lean on a copilot to help you solve the problems.

---

## Computer science is problem solving

Computer science is the study of **information**: how to represent it and how to process it. Computational thinking is taking those ideas and applying them to real problems.

Every problem has the same shape:

```
input (the problem)  →  [ black box: the algorithm ]  →  correct output (the result)
```

The rest of the course is about what goes inside that box.

---

## Everything is zeros and ones

Computers only have two symbols: 0 and 1. That's **binary**, base 2. A single binary digit is a **bit**: 0 is a switch off, 1 is a switch on. A computer is millions of tiny switches, transistors, each holding a bit.

Binary works like decimal, just with powers of 2 instead of 10:

```
123 (decimal) = 1×10² + 2×10¹ + 3×10⁰  =  100 + 20 + 3  =  123

011 (binary)  = 0×2² + 1×2¹ + 1×2⁰  =  0 + 2 + 1  =  3
100 (binary)  = 1×2² + 0×2¹ + 0×2⁰  =  4 + 0 + 0  =  4
```

To count to 8 you need a fourth bit. Run out of bits and the counter wraps back to zero, so more numbers literally means more hardware.

Eight bits make a **byte**, which counts from `00000000` (0) to `11111111` (255): 256 possible values.

### Text

Letters are just numbers everyone agreed on. In **ASCII**, `A` is 65, `B` is 66, and so on. So `72 73 33` spells **HI!**

The detail I liked: lowercase letters sit exactly 32 above uppercase (`A` = 65, `a` = 97). In binary, going from `H` to `h` flips a single bit:

<pre><code>H  01<span class="bit-flip">0</span>01000
h  01<span class="bit-flip">1</span>01000</code></pre>

ASCII only covers 256 characters. **Unicode** uses up to 32 bits, enough for every human language and every emoji, like 😂. Still just zeros and ones in the end.

### Colors, video and sound

- **Color:** RGB stores an amount of red, green and blue, 0–255 each, so 3 bytes per pixel.
- **Video:** images shown fast enough to trick our minds into seeing motion.
- **Music:** each note can be described by three numbers: frequency, duration and loudness.

The pattern behind all of it: you only have 0 and 1, so you agree on a way to arrange them.

---

## Algorithms: good, better, best

An **algorithm** is a set of step-by-step instructions for solving a problem, like finding a name in a sorted contact list.

Several algorithms can solve the same problem, but they're not equal. Some are faster or use less memory, and some are simply better designed. As David Malan put it, it's not just about getting the job done but solving the problem better, with whatever resource is limited: time, memory, people or money.

- **Good design:** logic that is correct *and* efficient.
- **Code:** an algorithm written in a language the computer understands.
- **Pseudocode:** the same steps in plain English. There's no official format; everyone writes it their own way.

Even instructions are standardized. Chip makers like Intel, AMD and NVIDIA decide which bit patterns mean "add these numbers" or "load this into memory".

---

## My takeaway

Week 0 has almost no code, and that's the point: before writing anything, you need to know what information you're working with and what steps will transform it. The languages come next.

---

## Wait, what is Scratch?

If you open CS50's Week 0, you'll see it's titled *Scratch*, and you might wonder what that is, since I skipped it. Well, [Scratch](https://scratch.mit.edu/) is a visual programming language from MIT: instead of typing code, you snap colored blocks together, a bit like puzzle pieces, and a cat on the screen does what they say.

It's how the course gets you building something before you have to worry about syntax. If you're curious, [CS50's own Week 0 notes](https://cs50.harvard.edu/x/notes/0/) pick up where mine stop.

---

<small>Based on [CS50x](https://cs50.harvard.edu/x/) by David J. Malan, Harvard University, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). These notes are my own summary.</small>
