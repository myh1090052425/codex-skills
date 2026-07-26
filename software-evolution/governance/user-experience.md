# User Experience Governance

Apply the selected mode contract first. In a read-only mode, use this guidance only to inspect, prove, and report; do not execute the repair, convergence, or check-creation steps.

Evaluate whether real users can understand, complete, and recover from tasks—not merely whether UI elements exist.

## Evidence order

1. Browser-observed behavior in a safe local/test environment.
2. Automated UI tests and screenshots/traces.
3. API behavior and state transitions supporting the flow.
4. Source inspection when runtime execution is unavailable.

State the evidence limitation when relying on lower-order evidence. Do not claim end-to-end UX quality from static code alone when the app can be run.

## Build the journey inventory

For each critical actor, identify:

- Goal and trigger.
- Entry point and discoverability.
- Main steps and decision points.
- Required data and permissions.
- Success feedback and resulting state.
- Empty, loading, partial, error, timeout, retry, and permission-denied paths.
- Recovery/cancellation path.

Prioritize revenue, safety, compliance, onboarding, frequent, and support-heavy journeys.

## Browser procedure

When browser automation is available:

1. Use documented local start commands and seeded/test credentials.
2. Verify the environment is non-production. Read-only modes must not mutate application data; use existing fixtures/read-only journeys or record the blocked coverage.
3. Traverse navigation before deep-linking so findability is tested.
4. Only in a writable mode, or init with a disposable isolated test environment, exercise a representative create/read/update/delete or equivalent business flow.
5. Inspect visible feedback, keyboard/focus behavior when relevant, console errors, failed requests, and stale UI state.
6. Capture screenshots or traces for material visual/flow findings.
7. In a writable mode, repeat the repaired flow after automated checks pass; read-only modes stop at evidence and handoff.

Do not bypass authentication. If credentials are unavailable, test public flows and record the blocked authenticated coverage.

## Inspection checklist

### Information architecture and navigation

- Page/module grouping matches user tasks and business language.
- Menu labels are distinct, predictable, permission-aware, and not duplicated.
- Primary actions are visible at the right stage.
- Users can understand location, context, and how to go back.
- Deep links, refresh, and browser history preserve valid state.

### Workflow efficiency

- Remove repeated entry, redundant confirmations, unnecessary page changes, and hidden prerequisites.
- Keep destructive actions deliberate while routine actions remain efficient.
- Preserve user input on recoverable failures.
- Avoid modal chains and workflows that cannot be paused or resumed.

### Forms and dialogs

- Labels, defaults, constraints, required fields, and examples are clear.
- Validation occurs at useful times and points to the exact correction.
- Submission prevents accidental duplicate actions and shows progress.
- Dialogs have one clear primary action, safe cancellation, focus management, and meaningful titles.

### Tables and data presentation

- Columns support the user's decision rather than expose raw schema.
- Sorting, filtering, pagination, selection, density, truncation, and responsive behavior match data size.
- Units, dates, statuses, ownership, and freshness are unambiguous.
- Empty results explain whether there is no data, no permission, or an active filter.

### Feedback and recovery

- Loading states distinguish initial load from refresh or mutation.
- Success feedback confirms the business result, not only “operation successful.”
- Errors explain what failed, what was preserved, and what the user can do next.
- Timeouts/retries do not create duplicate side effects.
- Permission denial is explicit and offers the correct next step without leaking restricted data.

### Accessibility and resilience

- Essential tasks work with keyboard/focus patterns when applicable.
- Labels, semantics, contrast, error association, and dynamic announcements are adequate.
- Layout survives realistic content length, localization, zoom, and narrow viewports.

## UX finding evidence

Record:

- Actor, route/page, business goal, and preconditions.
- Reproduction steps.
- Expected versus actual behavior.
- Frequency/affected users and task impact.
- Browser screenshot/trace/console/network evidence when available.
- Owning frontend/backend rules and call chain.
- Repair and post-fix validation.

## Safe autonomous UX repairs

Usually safe when verified:

- Missing loading/empty/error/success states.
- Incorrect disabled state, label, validation message, focus, or post-action feedback.
- Duplicate submission prevention.
- Clearly broken navigation or stale state caused by a localized bug.
- Table/form clarity changes that do not alter business semantics or permissions.

Treat navigation redesign, workflow removal, permission visibility, and business terminology changes as medium/high risk unless authoritative product evidence exists.
