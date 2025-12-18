# PROJECT_BRIEF.md - User Dashboard

## Project Overview

| Field | Value |
|-------|-------|
| **Project Name** | User Dashboard |
| **Project Type** | web_app |
| **Timeline** | 1 week |
| **Team Size** | 1 |

## Goal

A minimal Next.js dashboard that displays user profile information with theme toggle (light/dark mode).

## Target Users

- Developers learning Next.js patterns
- Users needing a simple profile dashboard template

## Features (MVP)

1. **User Profile Display** - Show user name, email, and avatar
2. **Theme Toggle** - Switch between light and dark mode
3. **Responsive Layout** - Works on mobile and desktop
4. **Profile Edit Modal** - Edit user name and email

## Nice-to-Have (v2)

- OAuth authentication
- Activity feed
- Settings persistence to backend

## Tech Stack

### Must Use
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Context for theme state

### Cannot Use
- External CSS frameworks (Bootstrap, etc.)
- Redux or other state management libraries
- Server-side database (use mock data)

## Constraints

- Must use App Router (not Pages Router)
- Must be fully typed with TypeScript
- Must pass ESLint with no warnings
- Must have loading states for async operations
- Must be accessible (ARIA labels, keyboard navigation)
