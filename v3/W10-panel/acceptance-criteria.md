# Commit Book: 30 actionable criteria

**SYNTHETIC REQUIREMENTS, NOT REAL USER FEEDBACK. ALL 30 NOT TESTED.**

P0 = proposed release blocker. P1 = proposed next-priority requirement. These priorities are author judgment, not participant voting. WCAG-related checks are proposed tests, not certification or legal advice. Parent IDs link to fictional scenarios in synthetic-parent-panel.md.

## CB-01: Sport selection
- Source scenario: P01, synthetic.
- Priority: P0.
- Requirement: Support a neutral sport selector with football, soccer, basketball, baseball, softball, volleyball, track, cross-country, swimming, tennis, golf, wrestling, adaptive sport and Other.
- Acceptance test: Select every option, including Other; it persists on reload and never silently maps to another sport.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-02: Sport-specific dates
- Source scenario: P02, synthetic.
- Priority: P0.
- Requirement: Keep recruiting milestones keyed to sport, program category, governing association and season.
- Acceptance test: Two synthetic sports with different fixture dates display their own dates; no default date leaks into the other profile.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-03: Source and freshness
- Source scenario: P01, synthetic.
- Priority: P0.
- Requirement: Show the source, checked date and uncertainty for every rule-derived deadline.
- Acceptance test: Open a deadline: source link, checked date and applicable scope are present; unsourced fixture is visibly Unverified.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-04: Athlete separation
- Source scenario: P03, synthetic.
- Priority: P0.
- Requirement: Scope tasks, contacts, results and reminders to one athlete.
- Acceptance test: Create two fictional athletes; switching profiles cannot reveal or edit the other athlete’s records.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-05: Inclusive program categories
- Source scenario: P03, synthetic.
- Priority: P1.
- Requirement: Allow relevant program categories without inferring gender, ability or eligibility from the sport.
- Acceptance test: Change category explicitly; displayed scope updates and eligibility remains unverified until backed by a source.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-06: Season conflicts
- Source scenario: P02, synthetic.
- Priority: P1.
- Requirement: Differentiate school, club, camp and recruiting events.
- Acceptance test: Add overlapping fixtures; agenda names each type and flags the overlap without deleting either event.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-07: Performance context
- Source scenario: P06, synthetic.
- Priority: P1.
- Requirement: Store event-specific performance units and measurement context.
- Acceptance test: Save a track time and a swimming time; each retains event, distance, units, date and timing context; no cross-event ranking is inferred.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-08: Adaptive pathway
- Source scenario: P10, synthetic.
- Priority: P0.
- Requirement: Offer adaptive-sport and Other pathways without automatic exclusion.
- Acceptance test: Select adaptive sport: program search stays usable, classification is optional and no medical disclosure is required.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-09: Time zones
- Source scenario: P04, synthetic.
- Priority: P0.
- Requirement: Display event time zone and preserve the actual instant when travel changes the viewing zone.
- Acceptance test: A synthetic event near daylight-saving change retains its UTC instant across two zones; ambiguous local times require explicit offset selection.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-10: Costs and travel
- Source scenario: P05, synthetic.
- Priority: P1.
- Requirement: Separate known fees, travel estimates and unknown expenses.
- Acceptance test: A camp fixture with missing lodging shows Unknown, not zero; cancellation policy is linked or marked unavailable.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-11: Plain-language next action
- Source scenario: P01, synthetic.
- Priority: P1.
- Requirement: Pair each milestone with a concrete next step and jargon explanation.
- Acceptance test: A first-time reader can locate the action, reason and optional glossary without leaving the agenda; no offer guarantee appears.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-12: No invented guarantees
- Source scenario: P01, synthetic.
- Priority: P0.
- Requirement: Distinguish planning guidance from recruiting, scholarship and eligibility decisions.
- Acceptance test: Review generated guidance fixtures: all unsupported promises are absent; uncertainty and responsible source are shown.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-13: Reminders with control
- Source scenario: P04, synthetic.
- Priority: P1.
- Requirement: Let families preview, enable, change and disable reminders per athlete.
- Acceptance test: Create a fixture reminder, inspect recipient/time/zone, cancel it, and verify no subsequent delivery is queued.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-14: Calendar interoperability
- Source scenario: P02, synthetic.
- Priority: P1.
- Requirement: Export events with stable identifiers, time zones and updates/cancellations.
- Acceptance test: Import fixture ICS into a test calendar, update then cancel; the original event changes rather than creating duplicates.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-15: Offline truthfulness
- Source scenario: P04, synthetic.
- Priority: P1.
- Requirement: Provide a cached agenda with explicit offline and last-sync status.
- Acceptance test: Disconnect after a sync: cached events remain readable; unsaved edits show Pending and rule updates are never described as current.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-16: Sharing boundaries
- Source scenario: P02, synthetic.
- Priority: P0.
- Requirement: Support independent household access and least-privilege sharing.
- Acceptance test: Invite a fixture viewer: private notes are absent, edits are denied, and revocation removes access on a fresh session.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-17: Minor privacy
- Source scenario: P10, synthetic.
- Priority: P0.
- Requirement: Keep athlete profiles private by default and require explicit preview before sharing.
- Acceptance test: New fictional minor profile is inaccessible to unauthenticated visitors; preview lists exactly the fields included in a shared view.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-18: Consent and correction
- Source scenario: P10, synthetic.
- Priority: P0.
- Requirement: Provide optional sensitive fields plus correction, export and deletion controls.
- Acceptance test: Skip disability/medical fields and finish onboarding; export contains only fixture data; deletion removes it from normal access and states retention limits.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-19: Keyboard completeness
- Source scenario: P09, synthetic.
- Priority: P0.
- Requirement: Support all core workflows without a pointer, including alternatives to dragging.
- Acceptance test: Using keyboard only, add/edit/move/delete a task and switch athletes; no trap occurs and focus returns logically after dialogs.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-20: Focus and semantics
- Source scenario: P09, synthetic.
- Priority: P0.
- Requirement: Use persistent visible focus, meaningful headings, landmarks and named controls.
- Acceptance test: Inspect the accessibility tree and tab through controls: each has a useful name, focus is visible and not hidden by sticky content.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-21: Screen-reader agenda
- Source scenario: P07, synthetic.
- Priority: P0.
- Requirement: Provide a chronological agenda alternative with understandable dates and context.
- Acceptance test: With VoiceOver/Safari and NVDA/Firefox, read and create a fixture event; date, athlete, sport, time zone and status are announced in sensible order.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-22: Dynamic announcements
- Source scenario: P07, synthetic.
- Priority: P0.
- Requirement: Announce save errors, loading completion and successful changes without stealing focus.
- Acceptance test: Trigger validation and save a fixture task with a screen reader; each relevant status is announced once and entered data is retained.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-23: Contrast and noncolor meaning
- Source scenario: P08, synthetic.
- Priority: P0.
- Requirement: Meet WCAG 2.2 AA contrast and never rely on color alone.
- Acceptance test: Measure normal text at least 4.5:1, large text 3:1 and required UI/state indicators 3:1; grayscale still exposes priority/status in text or shape.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-24: Zoom and reflow
- Source scenario: P08, synthetic.
- Priority: P0.
- Requirement: Keep core content and controls available at 200 percent text resize and 320 CSS-pixel width.
- Acceptance test: Test both conditions: no clipped labels, inaccessible controls or horizontal page scrolling except genuinely two-dimensional content with an agenda alternative.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-25: Touch and dexterity
- Source scenario: P09, synthetic.
- Priority: P0.
- Requirement: Provide targets at least 24 by 24 CSS pixels or documented WCAG-compliant spacing; prefer 44 by 44 for primary mobile actions.
- Acceptance test: Measure primary and secondary targets on mobile; all satisfy the minimum or valid spacing exception, and risky adjacent actions remain distinguishable.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-26: Motion control
- Source scenario: P08, synthetic.
- Priority: P1.
- Requirement: Respect reduced-motion preferences and avoid flashing or compulsory animation.
- Acceptance test: Enable prefers-reduced-motion: nonessential transitions stop; no content flashes more than three times per second; workflow remains complete.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-27: Media equivalents
- Source scenario: P10, synthetic.
- Priority: P0.
- Requirement: Provide accurate captions for meaningful video and text alternatives for meaningful visuals/audio.
- Acceptance test: Inspect a fixture explainer: captions include meaningful sound, transcript covers audio content and diagram has equivalent text; no information requires hearing.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-28: Accessible forms
- Source scenario: P07, synthetic.
- Priority: P0.
- Requirement: Use explicit labels, format hints, linked errors and preserved inputs.
- Acceptance test: Submit invalid dates with a screen reader: the error identifies the field and correction, focus reaches the problem and other entries remain intact.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-29: Cognitive clarity
- Source scenario: P01, synthetic.
- Priority: P1.
- Requirement: Break onboarding into short steps with saved progress and a review screen.
- Acceptance test: Leave midway and return: prior fixture answers remain; progress is named in text and review allows correction before any sharing.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

## CB-30: Authentication and recovery
- Source scenario: P09, synthetic.
- Priority: P0.
- Requirement: Allow password-manager use, paste and an accessible recovery path without cognitive-only puzzles.
- Acceptance test: Complete sign-in and recovery using keyboard and a password manager; paste works; any anti-bot challenge has an accessible alternative and errors disclose no other account data.
- Status: NOT TESTED.
- Evidence required: Executed test steps plus observed result and relevant screenshot or accessibility-tree evidence; fixtures are synthetic.

