# UX/UI Body of Knowledge

The methodology this skill applies in both **Design mode** (create UX/UI) and **Audit mode** (evaluate UX/UI). Each topic below has three parts:

- **Concept** — what it is and why it matters.
- **Design (apply)** — how to use it when designing.
- **Audit (check)** — what to look for when evaluating an existing interface.

These ten topics are the dimensions used by [audit-rubric.md](audit-rubric.md).

---

## 1. UX and UI Foundations

**Concept.** UX (User Experience) is the overall experience of using a product: it must be useful, usable, and aligned with both user goals and business goals. UI (User Interface) is the visible, interactive layer (buttons, menus, layout, typography) that users see and touch. A good UI is intuitive, familiar, navigable, and coherent. UI is a core component of UX; a poor UI makes interaction slow, confusing, inconsistent, and hard to read.

**Design (apply).** Start every decision from the user's goal and the business goal together. Treat visual choices as servants of the task, not decoration. Keep interaction consistent across screens so users can transfer learning.

**Audit (check).** Is the primary user and task identifiable from the interface alone? Does the visual style serve the task or fight it? Is the same action performed the same way everywhere?

---

## 2. Design Thinking (5 Iterative Steps)

**Concept.** A repeatable, iterative problem-solving process: Empathize -> Define -> Ideate -> Prototype -> Test. It is a loop, not a line; resilience matters (fall, get up quickly, iterate).

**Design (apply).**
- **Empathize** — observe and interview to learn what users *say, do, think, and feel*.
- **Define** — analyze findings, identify pain points, write a clear problem statement.
- **Ideate** — generate as many options as possible (brainstorm, mind-map); no idea is wrong at this stage.
- **Prototype** — turn the best ideas into fast, cheap models (e.g., wireframes).
- **Test** — put the prototype in front of real users, collect feedback, and revise.

**Audit (check).** Does the product look like it was built from evidence of real users, or from assumptions? Is there any trace of tested flows, or does it feel like a first guess shipped to production? Flag interfaces that ignore obvious pain points the Define step would have caught.

---

## 3. User Research — Persona, Empathy Map, Affinity Diagram

**Concept.**
- **Persona** — a fictional character built from real (quantitative + qualitative) research, representing a target segment. One persona should have a name, picture, demographics, goals, and pain points. Keep the count sensible (about 2-7).
- **Empathy Map** — captures a user's *Say, Do, Think, Feel* in a given moment. Unlike a persona, it is built from purely qualitative data to reveal attitude and emotion.
- **Affinity Diagram** — organizes a large volume of brainstormed data by grouping ideas into related themes.

**Design (apply).** Build 2-7 personas from research, not imagination. For each key task, sketch an empathy map to expose hidden feelings and fears. Cluster raw research with an affinity diagram before deciding on features.

**Audit (check).** Can you infer who the product is for? Is the interface trying to serve too many personas at once (clutter)? Are pain points that a persona/empathy map would reveal still present in the live UI?

---

## 4. Information Architecture (IA)

**Concept.** IA is the skeleton of the product: how content is structured, categorized, and sequenced so users find what they need with the least effort.

**Core elements.**
- **Sitemap** — the map of pages and how they connect.
- **User Flow Diagram** — the path a user takes to reach a goal.
- **Taxonomy** — how content is grouped and labeled.

**8 Principles of IA (apply the ones that fit).**
- **Disclosure** — reveal information progressively, not all at once.
- **Choices** — limit options so users are not overwhelmed.
- **Front Doors** — design every page as if it could be an entry point (deep-linkable).
- Plus: *objects, growth, multiple classification, focused navigation, gradual reveal.*

**Design (apply).** Decide navigation, hierarchy, grouping, and labeling *before* visual styling. Lead with the primary task. Use cards only for repeated items, modals, or genuinely bounded tools; never nest cards inside cards.

**Audit (check).** Can a user reach the primary task in few steps? Is the labeling consistent? Is navigation deeper than ~3 levels for common tasks? Are choices overwhelming on key screens?

---

## 5. Wireframe, Mockup, Prototype

**Concept.** Three fidelity stages of a design artifact.
- **Wireframe** — a low-detail blueprint focused on structure and placement; usually black-and-white so viewers are not distracted by color. Levels: *Low-fidelity* (rough sketch), *Mid-fidelity*, *High-fidelity* (more detail). Often uses placeholder text (Lorem Ipsum) to model text space.
- **Mockup** — a realistic, styled image with color, fonts, logo, and brand identity, but not clickable.
- **Prototype** — an interactive model: clickable buttons, typed input, near-real behavior, used to test flow and simulate UX.

**Design (apply).** Move fidelity upward only as confidence grows. Test a wireframe before investing in a mockup; test a mockup before building a clickable prototype.

**Audit (check).** Does the *built* product still reflect its intended structure, or did implementation drift? Are there screens that look like a high-fidelity mockup but lost the structure of the wireframe (clutter, displaced priority)?

---

## 6. Visual Hierarchy and UI Design Patterns

**Concept.** Visual hierarchy arranges elements by importance to guide the eye: what to focus on first, second, third.

**Reading patterns.**
- **F-Pattern** — for text-heavy pages; the eye sweeps left-to-right, then top-to-bottom, forming an F.
- **Z-Pattern / Zig-Zag** — for sparse pages that emphasize imagery or a call-to-action (CTA); the eye sweeps in a Z.

**Tools to direct the eye.**
- **Size** — large draws first.
- **Color and Contrast** — bright/light stands out.
- **White Space** — spacing isolates and elevates focus; rests the eye.
- **Proximity (Gestalt)** — group related things together.

**UI Design Patterns (standard solutions to common problems).**
- **Breadcrumbs** — show the user's current location.
- **Progressive Disclosure** — show only what is needed now.
- **Lazy Registration** — let users try the product before forcing sign-up.

**Design (apply).** Match the reading pattern to content density. Use one dominant element per screen. Group with proximity; separate with white space.

**Audit (check).** When you squint, does hierarchy survive? Is the primary CTA the most prominent element? Are related items grouped? Is there a "flat" screen where everything competes for attention?

---

## 7. Color and Typography

**Typography.** Text must be readable (*readability*) and hierarchy must be clear through size and spacing. Iron rule: **do not use more than 2 fonts per page**, and keep type **consistent**.

**Color.** Color drives emotion and accessibility. Use a **color scheme** and **contrast** to navigate users and emphasize key buttons (e.g., the primary action button should stand out more than the cancel button).

**Design (apply).**
- Set a legible base size (commonly 16px) with line-height around 1.5.
- Pair at most one heading font with one body font.
- Choose a small color scheme; reserve one accent for primary actions.
- Ensure semantic colors (success/warning/error) stay distinct and accessible.

**Audit (check).**
- Body text smaller than ~12px.
- More than two font families on one screen.
- Gray-on-gray or low-contrast text.
- Primary and secondary buttons with equal visual weight.
- Raw hex colors scattered in components instead of tokens.
- Relying on color alone to convey state.

---

## 8. Responsive Website Design

**Concept.** Design so the layout, structure, and sizing adapt automatically to every device (mobile, tablet, desktop).

**Key techniques.**
- **Flexible layouts** — CSS Grid (two-dimensional) or Flexbox (one-dimensional).
- **Responsive navigation** — simplify complex menus, e.g., a **hamburger menu** on mobile.
- **Media queries** — CSS that hides, shows, or rearranges content at **breakpoints** by screen size.
- **Responsive text** — adjust font size for comfortable reading on each device.

**Common breakpoints.** mobile (0), tablet (~768px), desktop (~1024px), wide (~1280px). Use a **mobile-first** approach.

**Design (apply).** Start from the narrowest viewport. Use a viewport meta tag. Avoid fixed pixel container widths. Reserve space for async media to prevent layout shift.

**Audit (check).** Inspect at least one narrow mobile, one desktop, and one wide viewport. Look for horizontal scrolling, overlap, text overflow, fixed elements covering content, and disabled zoom. Touch targets should be at least 44x44px.

---

## 9. Moodboard

**Concept.** A moodboard is an idea board (images, colors, fonts, materials) used to communicate the **concept, mood, and style** of a design so the team and the client share the same picture *before* real design begins. It can be **Physical** (you can touch material textures) or **Digital** (can include sound and video).

**Design (apply).** Before high-fidelity work, assemble a moodboard that fixes the emotional direction. Reference concrete brands, palettes, and type pairings rather than abstract adjectives.

**Audit (check).** Does the product express a coherent mood, or does it feel like mixed intentions? A missing or ignored moodboard often shows up as inconsistent tone across screens.

---

## 10. Usability Testing

**Concept.** Put the product in front of target users to find defects and see whether they can use it smoothly. **Test early, test often.**

**Critical discipline on questions.**
- Use **open-ended questions**.
- Avoid **leading questions** that bias answers.
- Do **not** ask "Is this button easy to use?" — instead ask "What would you expect this button to do?"

**Design (apply).** Plan a test script with open-ended tasks. Test from the wireframe stage onward. Record where users hesitate, backtrack, or fail.

**Audit (check).** Look for signals that real testing did or did not happen: obvious task failures, ambiguous labels, missing states (empty/loading/error), and copy that assumes knowledge the user does not have. Recommend a concrete usability test for any flow with high user impact and high uncertainty.
