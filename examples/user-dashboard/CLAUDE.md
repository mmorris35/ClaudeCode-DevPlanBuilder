# CLAUDE.md - User Dashboard

## Project Overview

User Dashboard is a minimal Next.js 14 application demonstrating modern React patterns with TypeScript and Tailwind CSS.

## Directory Structure

```
user-dashboard/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
├── postcss.config.js
├── src/
│   ├── app/
│   │   ├── layout.tsx        # Root layout with theme provider
│   │   ├── page.tsx          # Home page (dashboard)
│   │   └── globals.css       # Global styles with Tailwind
│   ├── components/
│   │   ├── Header.tsx        # Header with theme toggle
│   │   ├── ProfileCard.tsx   # User profile display
│   │   ├── EditModal.tsx     # Profile edit modal
│   │   └── ThemeToggle.tsx   # Light/dark mode toggle
│   ├── context/
│   │   ├── ThemeContext.tsx  # Theme state management
│   │   └── UserContext.tsx   # User state management
│   ├── types/
│   │   └── index.ts          # TypeScript type definitions
│   └── lib/
│       └── mockData.ts       # Mock user data
└── __tests__/
    ├── components/
    │   └── ProfileCard.test.tsx
    └── setup.ts
```

## Commands

```bash
# Development
npm run dev          # Start dev server at localhost:3000

# Build
npm run build        # Production build
npm run start        # Start production server

# Quality
npm run lint         # ESLint check
npm run type-check   # TypeScript check

# Testing
npm run test         # Run Jest tests
npm run test:watch   # Watch mode
```

## Coding Standards

### TypeScript
- Strict mode enabled
- Explicit return types on functions
- Interface over type where possible
- No `any` types

### React/Next.js
- Functional components only
- Use React hooks (useState, useContext, useEffect)
- Server components by default, 'use client' only when needed
- Proper error boundaries

### Tailwind CSS
- Use utility classes, no custom CSS unless necessary
- Dark mode with `dark:` prefix
- Responsive with `sm:`, `md:`, `lg:` prefixes
- No arbitrary values (`[]`) unless required

### File Naming
- Components: PascalCase (`ProfileCard.tsx`)
- Utilities: camelCase (`mockData.ts`)
- Types: PascalCase in files (`User`, `Theme`)

## Key Patterns

### Theme Context
```tsx
'use client';

import { createContext, useContext, useState } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

### Component Pattern
```tsx
interface ProfileCardProps {
  user: User;
  onEdit: () => void;
}

export function ProfileCard({ user, onEdit }: ProfileCardProps): JSX.Element {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
      {/* content */}
    </div>
  );
}
```

## Session Checklist

Before starting work:
- [ ] Run `npm install` to install dependencies
- [ ] Run `npm run dev` to verify dev server works
- [ ] Read current subtask in DEVELOPMENT_PLAN.md

After completing work:
- [ ] Run `npm run lint` - no errors
- [ ] Run `npm run type-check` - no errors
- [ ] Run `npm run test` - all pass
- [ ] Run `npm run build` - successful
- [ ] Commit with descriptive message
