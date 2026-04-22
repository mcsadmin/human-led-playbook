# Project Initiation Protocol

### A Generic Process for Standing Up New Human-Led Projects

---

## 1. Purpose of This Document

This protocol defines the repeatable process for standing up a new project within the Human-Led Project Coaching framework.

The Project Coach expects to be instantiated with a complete set of founding documents: a Working Brief, a Scope Document, and a Domain Glossary. If these documents are not prepared rigorously, the Coach will build a plan on a flawed foundation.

This protocol provides the human team with a structured method for producing those founding documents *before* the Project Coach is engaged.

## 2. The Initiation Arc

Project initiation is a human-led process, often facilitated by a lightweight, single-session AI agent (an "Initiation Facilitator") or conducted entirely by the human project leads. It consists of four sequential steps.

### Step 1: Define the S5 Identity (The Working Brief)

The first step is to establish the project's identity, direction, and governance. This is captured in the **Working Brief**.

1. **Direction & Vision:** Define the 3–5 year North Star and the specific vision for the current project timeframe (e.g., the current quarter). What is the ultimate goal, and what slice of it are we delivering now?

2. **Decision Authority & RACI:** Explicitly state who has the authority to approve the final plan and who holds advisory roles. Map the team to the generic framework roles (Sponsor, Lead, Member).

3. **Project Repository:** Agree on the name of the GitHub repository where the project will live (e.g., `mcsadmin/project-name`).

*Output: A completed Working Brief (using the standard template).*

### Step 2: Establish the Vocabulary (The Domain Glossary)

Before defining scope, the team must agree on the terms they will use. This prevents ambiguity and scope creep later in the process.

1. **Identify Key Terms:** List the core concepts, systems, or entities the project will interact with.

2. **Define Explicitly:** Write a clear, unambiguous definition for each term.

3. **Include Framework Terms:** Ensure the glossary includes the standard terms required by the coaching framework (e.g., Task Register, Sprint State Document, Dependency Structure Matrix).

*Output: A draft Domain Glossary.*

### Step 3: Draw the Boundary (The Scope Document)

With the identity and vocabulary established, the team defines the project boundary using the MoSCoW method.

1. **Must Have:** What are the non-negotiable deliverables? If these are not met, the project fails.

2. **Should Have:** What is important and expected, but not strictly mandatory for baseline success?

3. **Could Have:** What are the desirable additions if time and capacity permit?

4. **Won't Have:** What is explicitly excluded from this project phase? (Recording this is critical for preventing scope creep).

*Output: A completed Scope Document.*

### Step 4: The Handoff to the Project Coach

Once the three founding documents are drafted and agreed upon by the project leads, the initiation phase is complete.

1. **Instantiate the Coach:** Start a new session with the Project Coach.

2. **Provide the Context:** Supply the Coach Master Prompt and attach the three founding documents.

3. **Confirm Repository:** The Coach will read the repository name from the Working Brief and ask for confirmation to create or clone it.

4. **Begin Planning:** The Coach takes over, moving the project into the formal Initiation & Planning phase (Step 1 of the Coaching Arc).

---

## 3. Common Pitfalls in Initiation

- **Skipping the Glossary:** Attempting to define scope before defining terms leads to "Scope Creep via Ambiguity." Always define the vocabulary first.

- **Vague 'Must Haves':** A Must Have must be testable. "Improve the system" is not a Must Have; "Reduce processing time by 20%" is.

- **Ignoring the 'Won't Have' Category:** The Won't Have list is the most powerful tool for protecting the project boundary. Use it aggressively to park good ideas that do not belong in the current phase.
