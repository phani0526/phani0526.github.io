---
title: Selected work
nav: Work
layout: entries
lead: A closer look at a few projects. Internal systems, so no screenshots, but the problems will be familiar.
---

### Build Failure Analysis platform

Juniper Networks · Python, Django, Jenkins, MySQL
{: .meta }

Failed builds were investigated one at a time, and the same problems kept
coming back. I built a platform that classifies failures into 30+ recurring
types and tracks patterns across runs, so teams could fix causes instead of
symptoms. Over two years, monthly failures went from 40–60 to under 20.

### Self-service release platform

Juniper Networks · Django, REST APIs, SSO/SAML, RHEL
{: .meta }

Release requests used to arrive by email. I designed a multi-module platform
that brings together build histories, PR mappings and branch metadata, with
APIs other teams use to trigger release workflows. It grew through eight major
versions over 18 months and now handles thousands of requests a year.

### Making legacy release data trustworthy

Juniper Networks · SQL, Python
{: .meta }

Dashboards and automation were only as good as years of incomplete records.
I wrote SQL validation checks and Python repair utilities that corrected tens
of thousands of gaps, and built validation into new workflows so the data
stays correct.

### Intelligent Automation Program

CGI · Python, Ansible
{: .meta }

As one of four core engineers, I helped build reusable automation for
infrastructure checks, database validation and UI health monitoring, then
took it through requirements, reviews, dry runs and rollout across 30
applications.
