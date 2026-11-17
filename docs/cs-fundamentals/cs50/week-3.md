---
title: "CS50 Week 3: Thinking in Big O"
date: 2026-11-17
categories:
  - CS Fundamentals
description: "My notes from CS50 Week 3: searching and sorting, how big O, omega and theta describe an algorithm's cost, custom types with structs, and why merge sort wins."
reading_time: 4
icon: lucide/graduation-cap
tags:
  - CS50
  - C
  - Algorithms
share_image: assets/cs50/week3/share.jpg   # link preview (LinkedIn, X, WhatsApp) instead of the generated card
share_image_alt: "CS50 Week 3: Thinking in Big O, with a stack of handwritten notebook pages"
social:
  cards: false
notes:
  path: assets/cs50/week3
  pages:
    - "Algorithms, growth curves, cost, linear and binary search, pseudocode"
    - "Running time, big O, omega and theta, structs and sorting algorithms"
    - "Selection sort and bubble sort costs, recursion and merge sort"
---

> Correct is the minimum. The smarter the design, the slower the cost grows.

These are my notes from Week 3 of [CS50x](https://cs50.harvard.edu/x/), taken by hand and typed up here. Week 0 defined an algorithm as step-by-step instructions for solving a problem. This week was about comparing them: which ones scale, and how to say so precisely.

---

## Growth is what matters

The picture that opened the week, and the one I drew first:

- **n** (red): one step per item. Double the problem, double the time.
- **n/2** (black): two items at a time. Twice as fast, but still a straight line.
- **log₂ n** (blue): cut the problem in half again and again. The curve flattens out, so even a huge input barely adds time.

The lesson I marked: correctness isn't enough, design matters too. The smarter the algorithm, the slower its **cost** grows, and cost means any limited resource: time, money, people, storage.

---

## Searching

A human can glance at a list and spot what they want. A computer can only look at **one location at a time**.

- **Linear search:** check each item, left to right (or right to left).
- **Binary search:** on a sorted list, look in the middle, throw away the half that can't contain it, repeat.

Writing **pseudocode** first, an amalgam of English and C, helps: it's easier to translate into real code once you've thought at that level of detail.

---

## Big O, omega and theta

**Running time** is how many steps an algorithm takes, and we describe it in the order of the input size:

- **Big O**, the **upper bound**: how bad it can get.
- **Ω (omega)**, the **lower bound**: how lucky we might get.
- **Θ (theta)**, when the two are the same.

The rule I wrote twice: ignore the lower-order terms and keep only the **dominant term** as n gets bigger and bigger. So O(n) and O(n/2) are both just O(n).

| | Worst case (O) | Best case (Ω) |
|---|---|---|
| Linear search | O(n) | Ω(1), found first |
| Binary search | O(log n) | Ω(1), found in the middle |

From fastest to slowest: O(1), O(log n), O(n), O(n log n), O(n²). The family name for these is **asymptotic notation**: describing what happens as n gets very large.

---

## Custom types with structs

An array is the simplest data structure, values back to back, but it holds only one type. To bundle different fields together, C lets you define your own type:

```c
typedef struct
{
    string name;
    string codelogium;
}
user;
```

Now `user` works like any built-in type, and `u.name` or `u.codelogium` reaches each field. How you organize data in memory is what **data structures** are about, and it's where the course goes next.

---

## Sorting

- **Selection sort:** on each pass, find the smallest remaining element and put it in place.
- **Bubble sort:** compare neighbors and swap them, so the biggest values bubble up to the end, one at a time.
- **Merge sort:** sort the left half, sort the right half, merge the two sorted halves. If there's only one number, stop.

Working out the steps is what made big O click for me:

```
selection sort:  (n−1) + (n−2) + … + 1  =  n(n−1)/2  =  n²/2 − n/2   →  O(n²)
bubble sort:     (n−1) × (n−1)          =  n² − 2n + 1                →  O(n²)
```

Drop everything but the dominant term and both are O(n²). The difference is the best case: selection sort keeps scanning even when the list is already sorted, so it's Ω(n²), while bubble sort stops when a pass makes no swaps, so it's Ω(n).

Merge sort uses **recursion**: a function that calls itself on a smaller version of the problem. It's O(n log n) and Ω(n log n), so **Θ(n log n)**, much faster than n² on big lists.

---

## My takeaway

A problem can often be solved by several algorithms, and all of them may work. It's still worth reaching for the most efficient one, whatever the limited resource is: time, people or money. Big O is how you tell them apart before you've written a line.

For the full walkthrough with every example from the lecture, see the [official CS50 Week 3 notes](https://cs50.harvard.edu/x/notes/3/).

---

<small>Based on [CS50x](https://cs50.harvard.edu/x/) by David J. Malan, Harvard University, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). These notes are my own summary.</small>
