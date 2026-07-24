# Contributing

Thanks for helping improve `evidence-workflows`.

## Before opening a pull request

- Run `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Run the five synthetic scenarios and inspect the generated Markdown.
- Run `git diff --check`.
- Keep policy criteria visible and explain the intended decision they support.
- Add positive and negative synthetic fixtures for every new policy pack or check.

## Policy pack rules

A policy pack must state its purpose, minimum evidence, unknown behavior, privacy boundary, prohibited inferences, owner, and version. Do not add fields for hours, attendance, emotion, effort, loyalty, or an inferred employee score. If a condition cannot be checked safely, represent it as `unknown` and ask for a verifiable reference.

## Connector rules

Connector changes must preserve the `plan → human approval → apply → read-back` boundary. Tests must prove that local evaluation never makes a network call and never invents duration or credentials.

## Commit style

Use focused commits with an imperative subject, for example `Add incident investigation policy pack`. Keep generated scenario output synchronized with fixture changes.
