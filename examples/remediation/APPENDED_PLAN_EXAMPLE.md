# Development Plan - MyApp (with Remediation Phases)

> This example shows a DEVELOPMENT_PLAN.md with remediation phases (R.X) appended after the original development phases.

---

## Progress Tracking

### Original Development
- [x] Phase 0: Foundation (0.1.1 - 0.1.4)
- [x] Phase 1: Core Features (1.1.1 - 1.2.3)
- [x] Phase 2: User Interface (2.1.1 - 2.2.2)
- [x] Phase 3: Testing & Polish (3.1.1 - 3.1.3)
- [x] Phase 4: Distribution (4.1.1 - 4.1.2)

### Post-Release Remediation
- [ ] Phase R.1: Fix authentication token expiry (Issue #803)
  - [ ] R.1.1.1: Fix token refresh logic
  - [ ] R.1.1.2: Add regression tests
- [ ] Phase R.2: Add dark mode support (Issue #815)
  - [ ] R.2.1.1: Implement theme context
  - [ ] R.2.1.2: Update components
  - [ ] R.2.1.3: Add theme toggle

**Current Phase**: R.1 (Remediation)
**Next Subtask**: R.1.1.1

---

## Original Development Phases (Completed)

### Phase 0: Foundation
*[Completed - details omitted for brevity]*

### Phase 1: Core Features
*[Completed - details omitted for brevity]*

### Phase 2: User Interface
*[Completed - details omitted for brevity]*

### Phase 3: Testing & Polish
*[Completed - details omitted for brevity]*

### Phase 4: Distribution
*[Completed - details omitted for brevity]*

---

## Remediation Phases (Post-Release)

---

## Phase R.1: Fix authentication token expiry (Issue #803)

**Type**: Bug Fix
**Severity**: high
**Goal**: Resolve issue #803 - Authentication token expires during long operations
**Added**: 2024-01-15

### Task R.1.1: Fix authentication token expiry

**Git Strategy**:
- **Branch**: `fix/803-auth-token-expiry` (from `main`)
- **Commit Prefix**: `fix`
- **Merge**: squash when task complete

---

#### Subtask R.1.1.1: Fix: Token refresh logic (Quick Fix)

**Prerequisites**: None (post-release fix)

**Deliverables**:
- [ ] Add `refresh_token_if_needed()` method to TokenManager
- [ ] Implement proactive refresh (trigger at 80% of TTL)
- [ ] Add retry logic for refresh failures
- [ ] Add logging for token refresh events

**Files to Modify**:
- `src/auth/token_manager.py`
- `src/upload/file_uploader.py`

**Success Criteria**:
- [ ] Token refreshes automatically during long operations
- [ ] No auth failures during 30+ minute uploads
- [ ] Existing tests still pass

**Completion Notes**:
```
Session Date:
Completed By:
Key Decisions:
```

---

#### Subtask R.1.1.2: Test: Token expiry regression tests

**Prerequisites**: R.1.1.1

**Deliverables**:
- [ ] Add test case simulating long operation
- [ ] Test refresh failure handling
- [ ] Achieve >90% coverage on modified files

**Files to Create**:
- `tests/test_token_refresh.py`

**Success Criteria**:
- [ ] Test reproduces original issue (fails without fix)
- [ ] Test passes with fix applied
- [ ] Edge cases covered

**Completion Notes**:
```
Session Date:
Completed By:
Key Decisions:
```

---

### Task R.1.1 Complete - Squash Merge

- [ ] All subtasks complete
- [ ] All tests pass
- [ ] PR created: `gh pr create --title "fix: token refresh" --body "Fixes #803"`
- [ ] Squash merged to main
- [ ] Issue #803 closed

---

## Phase R.2: Add dark mode support (Issue #815)

**Type**: Enhancement
**Severity**: medium
**Goal**: Resolve issue #815 - Add dark mode theme option
**Added**: 2024-01-18

### Task R.2.1: Implement dark mode

**Git Strategy**:
- **Branch**: `feat/815-dark-mode` (from `main`)
- **Commit Prefix**: `feat`
- **Merge**: squash when task complete

---

#### Subtask R.2.1.1: Implement: Theme context and provider

**Prerequisites**: None

**Deliverables**:
- [ ] Create ThemeContext with light/dark modes
- [ ] Add ThemeProvider component
- [ ] Implement useTheme hook
- [ ] Persist theme preference to localStorage

**Files to Create**:
- `src/contexts/ThemeContext.tsx`
- `src/hooks/useTheme.ts`

**Success Criteria**:
- [ ] Theme context accessible throughout app
- [ ] Theme persists across page reloads
- [ ] Default follows system preference

**Completion Notes**:
```
Session Date:
Completed By:
Key Decisions:
```

---

#### Subtask R.2.1.2: Update: Component styling for themes

**Prerequisites**: R.2.1.1

**Deliverables**:
- [ ] Update CSS variables for light/dark themes
- [ ] Modify all components to use theme variables
- [ ] Ensure sufficient contrast in both modes
- [ ] Handle images/icons that need theme variants

**Files to Modify**:
- `src/styles/globals.css`
- `src/components/*.tsx` (all components)

**Success Criteria**:
- [ ] All components render correctly in both themes
- [ ] WCAG AA contrast requirements met
- [ ] No hardcoded colors remaining

**Completion Notes**:
```
Session Date:
Completed By:
Key Decisions:
```

---

#### Subtask R.2.1.3: Add: Theme toggle component

**Prerequisites**: R.2.1.2

**Deliverables**:
- [ ] Create ThemeToggle component
- [ ] Add toggle to header/settings
- [ ] Include smooth transition animation
- [ ] Add keyboard shortcut (Ctrl+Shift+D)

**Files to Create**:
- `src/components/ThemeToggle.tsx`

**Files to Modify**:
- `src/components/Header.tsx`

**Success Criteria**:
- [ ] Toggle visible in header
- [ ] Smooth transition between themes
- [ ] Keyboard shortcut works
- [ ] Accessible (ARIA labels)

**Completion Notes**:
```
Session Date:
Completed By:
Key Decisions:
```

---

### Task R.2.1 Complete - Squash Merge

- [ ] All subtasks complete
- [ ] All tests pass
- [ ] Visual QA in both themes
- [ ] PR created: `gh pr create --title "feat: dark mode support" --body "Fixes #815"`
- [ ] Squash merged to main
- [ ] Issue #815 closed

---

## Notes

### Why R.X Notation?

The `R.X` prefix indicates remediation phases added after the initial release:
- **R.1, R.2, R.3**: Sequential remediation phases
- No conflict with original phases (0, 1, 2, 3, 4)
- Clear distinction between initial development and maintenance

### Execution Order

Remediation phases should generally be executed in priority order:
1. **Security issues** (critical) - Immediate
2. **Regressions** (high) - Same day
3. **Bugs** (medium-high) - Within sprint
4. **Enhancements** (medium) - Backlog prioritization

In this example:
- R.1 (bug, high severity) should be completed before R.2
- R.2 (enhancement, medium severity) can wait for the next sprint
