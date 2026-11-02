---
title: "CS50 Week 1: Talking to the Machine"
date: 2026-11-03
categories:
  - CS Fundamentals
description: "My notes from CS50 Week 1: how source code becomes machine code, why reading the docs is a skill, and the building blocks of C: variables, conditionals, loops and functions."
reading_time: 6
icon: lucide/graduation-cap
tags:
  - CS50
  - C
share_image: assets/cs50/week1/share.jpg   # link preview (LinkedIn, X, WhatsApp) instead of the generated card
share_lead: "How source code becomes machine code, and the building blocks of C."
share_image_alt: "CS50 Week 1: Talking to the Machine, with a stack of handwritten notebook pages"
social:
  cards: false
notes:
  path: assets/cs50/week1
  pages:
    - "Source code, machine code, the compiler, GUI and CLI, hello.c and header files"
    - "Headers, reading the docs, cs50.h and get_string"
    - "Linux, terminal commands and conditionals"
    - "If, else if, else, types and format codes"
    - "Operators, variables and loops"
    - "Functions, scope, prototypes, correctness, design and style"
---

> Computers only speak zeros and ones. Week 1 is about learning to talk to them anyway.

These are my notes from Week 1 of [CS50x](https://cs50.harvard.edu/x/), taken by hand and typed up here. Week 0 was about ideas; this week, we finally write C.

---

## From source code to machine code

We write **source code**, text that humans can read. But as Week 0 showed, the computer only understands 0 and 1, its **machine code**. Something has to translate between the two, and that's the **compiler**:

```
source code (C)  →  [ compiler ]  →  machine code
```

The first program is the classic one:

```c
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
}
```

Then, in the terminal:

```
code hello.c    open the file to write it
make hello      compile hello.c into a program called hello
./hello         run it
```

A detail I noted: you `make hello`, not `make hello.c`. You name the program you want, and `make` finds the source file.

---

## Header files and reading the docs

That first line, `#include <stdio.h>`, is a **header file**: code someone else wrote that you can use. It tells the compiler that `printf` exists and is defined somewhere else, so you're not the one who wrote it. Collections of that code are called **libraries**.

The habit David insisted on, and the one I want to keep: **always check the official documentation**. That's where libraries and headers are defined and explained.

- [CS50 Manual](https://manual.cs50.io/), friendlier pages for the functions used in the course.
- [cppreference](https://en.cppreference.com/w/c), one of the best C references out there.

CS50 also has its own library, `cs50.h`, because some things in C are annoying to do at the start, like reading text from the user. It lets you focus on solving the problem first:

```c
string answer = get_string("What's your name? ");
printf("hello, %s\n", answer);
```

`string` is the **type**, `answer` the **variable**, and `%s` a placeholder that `printf` fills with the value of `answer`.

---

## GUI, CLI and Linux

Software mostly comes in two flavors: a **GUI** (graphical user interface) with icons and buttons, and a **CLI** (command-line interface), a terminal where you type commands.

The course runs on **Linux**, an operating system, the software that handles the basics of a device: booting, shutting down, managing windows, talking to the printer. Linux can have a GUI, but on servers and in the cloud, it often doesn't: a GUI is for humans, and servers don't need one. So you use commands like `ls`, `cd`, `code` and `make`.

---

## Conditionals, variables and loops

**Conditionals** let a program take a different road depending on the answer to a question, a **boolean expression**:

```c
if (x < y)
{
    printf("Codelogium sucks.\n");
}
else if (x > y)
{
    printf("Nah! Codelogium can be better, with a bunch of mistakes.\n");
}
else
{
    printf("Codelogium is just right.\n");
}
```

The trap: `=` is **assignment** (put this value in that variable), while `==` **compares** two values.

**Variables** keep track of data while the program runs. The type tells the computer how many bits to set aside:

```c
int counter = 0;   // declare and initialize
counter = counter + 1;
counter += 1;
counter++;         // all three add one
```

**Loops** do something again and again, possibly forever. `while` repeats as long as its condition is true, `for` packs the counter, the condition and the step into one line, and `do while` runs at least once before checking, handy for asking a user again until they cooperate.

One warning from the lecture I wrote in red: copying and pasting the same lines is a very bad habit. If you're repeating yourself, you probably want a loop or a function.

---

## Types have limits

Each type uses a fixed number of bits:

- `int`: 32 bits, about 4 billion values, so roughly −2 billion to +2 billion.
- `long`: 64 bits, a much bigger range.
- `float`: a real number in 32 bits; `double` uses 64 for more precision.
- `char`: a single character; `string`: text; `bool`: true or false.

Real numbers are infinite, but bits are not. The lecture ended on what that means in practice, and it was my favorite part.

- **Floating-point imprecision:** a `float` can only approximate most values. Print `1.0 / 3.0` with enough decimal places and, instead of 3s forever, the digits go wrong after a few places. Close enough for many uses, not for money or science.
- **Integer overflow:** an integer that grows past its last value wraps around, just like the counter in Week 0.
- **The Boeing 787:** after 248 days of running nonstop, a counter could overflow and the plane could lose all electrical power. The fix, until a software update: reboot it from time to time ([Engadget, 2015](https://www.engadget.com/2015-05-01-boeing-787-dreamliner-software-bug.html)).
- **The year 2000 problem:** to save memory, years were long stored with only two digits, so after 99 came 00, and 2000 looked like 1900.
- **The year 2038 problem, still to come:** many systems count time as seconds since January 1, 1970, in a 32-bit integer. That runs out on January 19, 2038, and the date jumps back to 1901 unless the software moves to 64 bits first.

Same lesson every time: someone picked a number of bits, and the world outgrew it.

---

## Functions, scope and good code

**Functions** let you abstract an idea away: solve a problem once, then reuse it over and over, and eventually package it into a library of your own.

- **Scope:** a variable lives inside the area where it's created. Outside its function, it can't be reached; it's "out of scope".
- **Prototype:** a promise to the compiler that a function will be defined later in the file, like `void hello(void);`. The one place where copy and paste is recommended.
- **Comments:** well-commented code is easier to read and to remember years later.

CS50 judges code on three axes, each with its own tool: **correctness** (does it work, `check50`), **design** (is it done well, `design50`) and **style** (is it readable for other humans, `style50`).

---

## My takeaway

Week 1 is the introduction to C and to solving problems with it. Variables, conditionals, loops, scope, functions and prototypes are the real building blocks of writing programs. And behind all of them is the same lesson as Week 0: the machine only has a fixed number of bits, so it's on us to know where the limits are.

For the full walkthrough with every example from the lecture, see the [official CS50 Week 1 notes](https://cs50.harvard.edu/x/notes/1/).

---

<small>Based on [CS50x](https://cs50.harvard.edu/x/) by David J. Malan, Harvard University, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). These notes are my own summary.</small>
