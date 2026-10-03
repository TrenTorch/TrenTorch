---
name: production-synthetic-data-templated-pair-generation
title: Generate Synthetic Examples From Templates
tags: [production-systems, synthetic-data]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Hand-writing thousands of training or eval examples is slow. If a whole family of examples shares the same structure -- "What is {n1} + {n2}?" with different numbers plugged in -- a template plus a list of values to substitute generates as many examples as needed, mechanically and consistently.

### The task

Write `generate_pairs(templates, variable_sets)` that fills in every template with every variable set (a cross product), in template-major order: all of the first template's fills before moving to the second template.

## Theory

### The simple version

A template is a pattern; a variable set is one concrete filling of that pattern. Generating the full cross product -- every template paired with every variable set -- is the most straightforward way to turn a handful of templates and a handful of value sets into a much larger set of concrete examples.

### Why the cross product, not just one substitution per template

If each template were paired with only one variable set, adding new value sets wouldn't multiply the dataset's coverage the way it should -- you'd have to write a new template for every new set of values. The cross product is what makes a small number of templates scale into a broad range of examples as more variable sets are added, without touching the templates themselves.

### How this shows up in real systems

This is a standard first step in generating a synthetic training or eval set: define a handful of templates covering the _shape_ of the task, then generate many concrete instances by substituting different values -- a technique used to bootstrap datasets in domains where real labeled examples are scarce or expensive to collect.

## Explanation

Nesting the loop with templates on the outside and variable sets on the inside produces exactly the template-major order asked for: every value set is applied to the first template before the loop advances to the second one, and `str.format(**variables)` does the actual placeholder substitution for each combination.
