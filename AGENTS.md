# AGENTS.md — Port Said Archive

This file defines how AI coding agents should work in this repository. Follow it before making changes. If a more specific `AGENTS.md` exists in a subdirectory, follow both files; the more specific instructions take precedence for that directory.

## 1. Project context

Port Said Archive is a digital historical archive about the city of Port Said. Its content is organized into 17 historical periods/eras based on summaries and material supplied by the project owner.

The project is intended to present history through carefully curated, readable storytelling—not through raw scraping, generic AI-generated summaries, or a bare list of dates and events.

### Content rules

- Treat the project owner's supplied summaries, documents, and explicitly approved sources as the starting point for historical content.
- Never invent dates, people, events, quotations, locations, causes, or historical connections.
- Do not silently fill gaps in the historical record with plausible-sounding text. Mark gaps clearly and ask the project owner what source or wording should be used.
- Preserve the meaning and nuance of supplied material when restructuring or editing it.
- Distinguish documented facts, oral/family/local memories, interpretations, and uncertain claims where that distinction matters.
- Do not present an unverified claim as established fact. Flag conflicting or incomplete evidence for review.
- Keep source attribution and image credits wherever the content model supports them. Do not fabricate citations, source names, image origins, or usage permissions.
- Do not change the boundaries, titles, order, or meaning of the 17 periods unless the project owner explicitly approves the change.
- Preserve Arabic text correctly. Use UTF-8 and, for MySQL text data, a Unicode-capable character set/collation such as `utf8mb4` where appropriate to the existing schema.

## 2. Technology stack and version policy

The intended stack is:

- Next.js for the web application.
- Node.js as the runtime/tooling environment.
- MySQL for persistent data.
- Tailwind CSS for styling.

Important version rules:

- First inspect `package.json`, the lockfile, project configuration, and the installed environment. The repository's actual versions are the source of truth for the current implementation.
- Use compatible, currently installed dependencies. Do not assume that a library's newest release is compatible with this project.
- Do not upgrade Next.js, React, Node-related packages, Tailwind CSS, database drivers, or other dependencies just because a newer version exists.
- Do not run broad upgrade commands or replace the package manager/lockfile without explicit approval.
- Before proposing a new dependency, explain what it solves, why existing tools are insufficient, and the maintenance/performance cost. Ask for approval before adding it.
- Follow the repository's existing package manager, folder structure, naming conventions, and coding style. Do not assume npm, pnpm, or yarn until you inspect the lockfile.
- Do not assume App Router versus Pages Router, Server Actions versus Route Handlers, an ORM, or a database access pattern. Inspect the project first and ask before introducing or replacing an architectural choice.

## 3. How to collaborate with the project owner

The project owner is still learning software development. Explain important decisions in clear, direct language without being condescending. Do not hide complexity behind unexplained code or claim that something is secure merely because it runs.

### Clarification and assumptions

- Do not guess when a missing detail affects the visual identity, user experience, historical accuracy, data model, security, privacy, dependencies, or externally visible behavior.
- Ask a concise question when a blocking requirement is unclear. Prefer one focused question at a time.
- In particular, discuss the color palette and overall visual direction with the project owner in Plan Mode before committing to them.
- Do not invent project requirements, page content, features, user roles, database fields, or business rules.
- For a small implementation detail that does not affect product behavior or architecture, follow an established pattern already present in the repository. Mention the choice in the final report.
- If two requirements conflict, explain the conflict and ask which one takes priority. Do not silently choose.

### Required workflow

For every task:

1. Read this file and any relevant local instructions.
2. Inspect the repository before proposing changes. Check the relevant files, folder structure, package scripts, dependencies, and existing patterns.
3. Summarize what you found and identify anything important that is unknown.
4. For non-trivial work, use Plan Mode before implementation. This includes multi-file changes, new pages or major components, animations affecting several sections, database/schema changes, API changes, authentication, authorization, and security-sensitive work.
5. The plan must state:
   - The intended result and scope.
   - The files or areas likely to change.
   - The implementation approach and important decisions.
   - Any assumptions, risks, or unanswered questions.
   - How the work will be tested and what counts as done.
6. Wait for the project owner's approval before implementing a non-trivial plan. Do not treat a request to investigate or plan as permission to make the changes.
7. Implement in small, focused steps. Avoid unrelated refactors.
8. Run the relevant checks and tests. Inspect the resulting changes for regressions.
9. Report what changed, what was tested, the actual results, and what remains incomplete or uncertain.

For a small, isolated correction with an obvious expected result, a brief explanation followed by the fix is acceptable; a full planning cycle is not required.

## 4. Product and visual design principles

The visual direction should feel intentional, editorial, historically grounded, and human-made. Avoid generic templates and visual choices that make the archive look like an automatically generated AI landing page.

### Visual direction

- Prefer a restrained, cohesive palette. Avoid neon colors, excessively saturated accents, loud gradients, and unnecessary glow effects.
- Do not choose the final color palette unilaterally. Present a small number of reasoned palette directions in Plan Mode and get approval before applying one across the product.
- Prioritize typography, hierarchy, spacing, composition, readability, and meaningful imagery over decorative effects.
- Make historical material feel like an archive with a clear editorial identity, not a generic SaaS dashboard unless a specific screen genuinely needs dashboard patterns.
- Use visual elements only when they support the content or help users navigate it.
- Avoid excessive cards, pills, borders, shadows, glassmorphism, gradients, and decorative icons. Use them only when they serve a clear purpose.
- Keep layouts coherent across pages and reusable components. Do not create a new visual language for each page.
- Design responsively. Check narrow mobile screens as well as desktop layouts; do not merely shrink the desktop design.
- Preserve readable contrast, visible focus states, semantic HTML, keyboard access, and sensible heading order.

### Before building a page or major section

- Identify the page's purpose, primary audience task, content hierarchy, and primary call to action (if any).
- Reuse existing design tokens and components where suitable.
- If the content, imagery, layout, or intended interaction is not clear, ask instead of filling the page with invented copy or arbitrary decoration.
- Use realistic archive content supplied by the project owner. Clearly label temporary placeholders and do not let them appear as verified history.

## 5. Motion and interaction guidelines

Motion should support the reading experience and reinforce the editorial character of the archive. It must not compete with historical content or make the interface feel like a motion demo.

### Scroll-related animation

- The preferred motion style is scroll-aware: elements may animate when they enter the viewport, or their progress may be tied to the user's scroll position when that genuinely improves the experience.
- Use scroll-triggered reveals for suitable headings, text blocks, images, and section transitions. Do not animate every element by default.
- The preferred duration for ordinary entrance and interaction animations is approximately `0.4s` to `0.6s`.
- Use restrained easing and short, purposeful movement. Avoid large, bouncy, overshooting, or theatrical effects unless explicitly approved.
- Prefer animating `transform` and `opacity`. Avoid repeatedly animating layout-affecting properties such as width, height, top, and left when that could cause layout recalculation or visual instability.
- Do not make content invisible or unreadable while waiting for JavaScript or an animation library to initialize. The page must remain usable if animation code fails.
- Avoid scroll hijacking, forced scrolling, excessive parallax, long pinned sections, and effects that make reading or navigation difficult.
- Prevent duplicate triggers, memory leaks, and stale event listeners. Clean up observers, listeners, timelines, and scroll triggers when components unmount or relevant state changes.
- Respect the user's `prefers-reduced-motion` setting. Provide a reduced-motion experience that removes or substantially simplifies non-essential movement.
- Check motion on touch devices and smaller screens. Do not depend on hover for essential functionality.

### Animation tooling

- Inspect the existing project before choosing an animation tool.
- Prefer existing dependencies and established project patterns.
- Use GSAP/ScrollTrigger only if it is already available or has been explicitly approved for the project. Do not add it automatically for a simple reveal that can be handled appropriately with existing browser APIs or CSS.
- If an animation library is used, follow its current installed-version documentation and framework integration guidance. Avoid mixing multiple animation systems without a clear reason.

### Hover and button behavior

- Hover effects are secondary; do not over-engineer them.
- Where appropriate, a button or text link may include an arrow icon that moves diagonally by roughly 45 degrees on hover/focus. Keep the movement subtle and brief.
- Do not apply the arrow treatment to every control automatically. Use it where it improves affordance or visual consistency.
- Provide equivalent feedback for keyboard focus. Do not make an action discoverable only through hover.
- Keep tap targets usable on touch screens.

## 6. Frontend implementation standards

- Follow the rendering and data-fetching conventions already used by the project. Understand whether a component is a Server Component or Client Component before adding client-side behavior.
- Keep client components limited to places that need browser interaction, state, or effects. Do not mark whole sections as client components without a reason.
- Prefer small, reusable components with clear responsibilities. Avoid giant page components and unnecessary abstraction.
- Keep content separate from presentation when that improves maintainability. Do not duplicate the same historical content across multiple components.
- Use Tailwind CSS consistently with the project's existing configuration and conventions. Avoid long collections of contradictory utility classes and arbitrary one-off values when a shared token or component is appropriate.
- Do not use placeholder links such as `href="#"` for real navigation. Ensure buttons and links perform the action their labels promise.
- Implement loading, empty, and error states where asynchronous data or user actions make them relevant.
- Use semantic HTML elements and accessible names for interactive controls.
- Optimize images responsibly, preserve aspect ratios, provide useful alternative text, and avoid unnecessarily large assets.
- Do not put secrets, privileged database access, or server-only logic in browser-delivered code.

## 7. Backend, API, and database security

Security is a priority. Do not trade it for speed or convenience. No implementation can be declared perfectly secure; identify limitations and residual risks honestly.

### Secrets and configuration

- Never hardcode credentials, API keys, access tokens, private connection strings, or other secrets in source code.
- Never expose server-only environment variables to browser code. Use public-prefixed environment variables only for values that are intentionally safe to disclose.
- Do not commit `.env` files or secrets. Keep a safe `.env.example` with placeholder values only, if the project uses one.
- Validate required environment variables at startup or at the appropriate server boundary, and provide clear errors without printing secret values.
- Do not copy real secrets into logs, test fixtures, screenshots, documentation, or AI-generated output.

### Input validation and authorization

- Validate all untrusted input on the server, even when the frontend already validates it.
- Validate types, lengths, formats, ranges, allowed values, and required fields. Reject unexpected input safely.
- Enforce authorization on the server for every protected operation and every requested resource. Hiding a button in the UI is not authorization.
- Apply authentication only where the project requirements call for it. Do not invent user roles or access rules.
- Return safe, useful error responses. Do not reveal stack traces, SQL details, file paths, secrets, or internal implementation details to users.

### SQL and database access

- Use parameterized queries or the safe parameter-binding mechanism of the database library/ORM already in use. Never build SQL by concatenating untrusted input.
- Do not introduce an ORM or replace the database driver without explaining the trade-offs and obtaining approval.
- Keep database credentials on the server only.
- Use transactions for operations that must succeed or fail together.
- Handle database errors without leaking internal details to the client.
- Review indexes, constraints, nullability, and relationships before changing the schema.
- Treat migrations as deliberate, reviewable changes. Never drop tables, delete records, reset a database, or run destructive migrations without explicit approval.
- Preserve existing data and Arabic text. Consider backup and rollback implications before schema or data migrations.
- Do not use production data for tests unless explicitly authorized and properly protected.

### Common web risks

Evaluate relevant protections for SQL injection, cross-site scripting (XSS), cross-site request forgery (CSRF), broken access control, insecure direct object references, unsafe redirects, sensitive-data exposure, abuse/rate limiting, and insecure file handling.

Do not add security middleware mechanically without understanding the framework and the actual threat. Explain which risks apply, which protections are implemented, and what remains outside the current scope.

## 8. Testing and quality checks

Tests are part of implementation, not an optional final decoration.

- Inspect available scripts in `package.json` before choosing commands.
- Add or update tests for changed behavior, especially data transformations, API routes, validation, authorization, database operations, and interactive UI behavior.
- Test important success cases and failure cases, including invalid input and permission failures where applicable.
- For database work, use a safe test database or controlled test fixtures. Never run destructive tests against a real or production database.
- Run the relevant available checks, such as unit/integration tests, linting, type checking, and a production build.
- If a check is unavailable or cannot be run, say so explicitly. Do not claim that tests passed when they were not run.
- Do not silence lint, type, or test failures with broad ignores, `any`, disabled rules, or skipped tests merely to make the command pass. Explain and justify any narrow exception.
- Review browser behavior at relevant viewport sizes and inspect the browser console for errors when UI work is involved.
- Check animation performance and reduced-motion behavior when motion is added.

## 9. Performance and reliability

- Keep the initial page load lean. Avoid adding large dependencies for small visual effects.
- Avoid unnecessary client-side JavaScript, repeated database queries, avoidable re-renders, and unbounded data fetching.
- Use pagination or other bounded loading for large collections where appropriate.
- Use caching only when its invalidation and freshness behavior are understood. Historical content accuracy is more important than an incorrectly cached result.
- Handle network and database failures explicitly. Do not assume external services are always available.
- Avoid logging personal data or sensitive request content.

## 10. Git and change management

- Do not discard, overwrite, or reset the project owner's existing work.
- Inspect `git status` before making changes when Git is available. Preserve unrelated uncommitted changes.
- Do not run destructive Git commands such as `reset --hard`, forced checkout, or clean operations unless the project owner explicitly requests them.
- Keep changes focused on the task. Do not perform broad refactors or formatting changes across unrelated files.
- Do not commit, push, publish, deploy, or modify production resources unless explicitly asked.

## 11. Completion report

At the end of each implementation task, provide a concise report containing:

1. **What changed:** the behavior or UI delivered.
2. **Files changed:** the main files and why they changed.
3. **Checks run:** exact commands or tests that were run and whether they passed or failed.
4. **Known gaps:** unimplemented requirements, unresolved questions, limitations, or risks.
5. **Next decision:** only the most important decision needed from the project owner, if one remains.

Be precise. Separate verified results from assumptions. Never say that a feature is complete, tested, secure, responsive, or production-ready unless the relevant work and checks support that statement.

## 12. Priority order when instructions compete

When trade-offs arise, use this priority order:

1. Historical accuracy and preservation of supplied content.
2. Security, privacy, and data integrity.
3. Correct functionality and accessibility.
4. Clear information architecture and usable responsive design.
5. Maintainability and consistency with the existing codebase.
6. Visual polish and animation.

Do not sacrifice a higher-priority requirement to achieve a lower-priority effect.
