---
title: "Designing for Forty Million Contacts a Month"
date: 2026-10-25
description: "What building an AWS orchestration platform for roughly 40 million Amazon Connect contacts a month taught me about throughput, correctness, and teams."
slug: designing-for-forty-million-contacts
---

# Designing for Forty Million Contacts a Month

Roughly 40 million. That is how many contacts the Amazon Connect orchestration platform I helped design and build carried each month, across multiple regions, while I worked on it. It is an easy number to put on a slide and a hard one to keep true.

The gap between those two things is most of what I know about building large systems.

## Throughput is not a request rate

When people say a system handles 40 million of anything a month, the first instinct is to divide by seconds and treat the result as a capacity target. That math is necessary, but it is not the problem. The platform models a contact as work that moves through steps, and each step has to know where the contact is, what has already happened, and what comes next. The platform is omni-channel, so the work arrives from more than one direction and has to converge on one consistent view of the customer's journey.

At that volume, the rare cases stop being rare. A retry that happens once in ten thousand normal operations happens thousands of times a month. A race that needs two events to land in the same millisecond still finds a way to happen. Throughput is not the speed of the happy path. It is the rate at which the system can keep thousands of small, ugly edge cases from turning into lost or duplicated work.

That reframing changes what you build first.

## A state machine is a promise

I worked on core components of the state machine that coordinates this flow. The interesting problems were not in the normal transitions. They were in the places where distributed systems usually break their promises: dual writes, where two stores can disagree about what happened; concurrent requests, where two workers can act on the same contact at the same time; and high availability, where the system has to keep accepting work while part of it is unhealthy.

Each of those is solvable in isolation. The difficulty is that they overlap. A retry during a partial outage can become a concurrent request. A concurrent request can turn one write into two. A state machine that is correct only when the network is healthy is not correct at all, because the network is never healthy everywhere at once.

So the design work was less about adding features and more about making failure boring. Every transition needed a defensible answer to three questions: what happens if this is delivered twice, what happens if two of these arrive at once, and what happens if the store behind it is temporarily unavailable. If the answer was "that should not happen", it was not an answer. At 40 million contacts a month, "should not" is a schedule, not a guarantee.

## Operations are part of the design

I also led work on deployment safety, customer-specific throttling, and automated load testing. Those sound like operational chores next to architecture. They are not. They are how you find out whether the design is true.

A load test that does not resemble production traffic will happily certify a system that falls over on its first real Monday. Throttling is not just a protective valve; it is an explicit statement about which customers get which share of a shared system under pressure. Deployment safety is the difference between a bad change costing you a rollback and a bad change costing you a region. None of this is separate from throughput. Throughput is a property of the whole system in motion, including the people and processes that change it.

That lesson followed me into management.

## The team is part of the system

Since September 2023 I have managed an organization of 20 engineers across 4 pods, delivering mission-critical customer experience features for Amazon Connect. The numbers I care about now look different from the ones I watched as an engineer, but they describe the same underlying property: whether the system can be trusted to keep its promises as it grows and changes.

Onboarding time came down by 50%. Test coverage went from 60% to 90%. Production incidents fell by 40% while system reliability held at 99.99%. Four engineers moved into technical leadership roles, and the team held 90% retention through high-growth phases. We bar-raised more than 20 operational readiness reviews and worked across 5+ partner teams.

None of those is a throughput metric in the narrow sense. All of them are throughput metrics in the sense that matters. A team that cannot onboard quickly, cannot test confidently, and cannot operate calmly will not sustain a system that handles tens of millions of contacts a month. Scale exposes the organization as much as it exposes the code.

## What I would tell someone starting this work

Do not design for the average day. The average day is not why the system is hard. Design for the day when a region is degraded, a retry storm is building, and two workers disagree about which step a contact is on. If the system behaves then, the number on the slide is real.

Forty million is the output. Correctness under load is the product. Everything else, including the org chart, is in service of that distinction.
