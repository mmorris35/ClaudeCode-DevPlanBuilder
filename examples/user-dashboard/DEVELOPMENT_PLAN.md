# DEVELOPMENT_PLAN.md - User Dashboard

> **Haiku-Executable Plan**: Every subtask contains complete, copy-pasteable code. Claude Haiku can execute this mechanically without inference.

## Project Summary

| Field | Value |
|-------|-------|
| **Project** | User Dashboard |
| **Goal** | Minimal Next.js dashboard with user profile and theme toggle |
| **Phases** | 2 |
| **Tasks** | 4 |
| **Subtasks** | 7 |

---

## Phase Overview

| Phase | Name | Tasks | Status |
|-------|------|-------|--------|
| 1 | Project Setup | 2 | Pending |
| 2 | Dashboard Implementation | 2 | Pending |

---

# Phase 1: Project Setup

## Task 1.1: Initialize Next.js Project

**Branch:** `feature/1.1-project-init`

### Subtask 1.1.1: Create package.json and Configuration

**Prerequisites:** None

**Deliverables:**
- [ ] `package.json` - Project dependencies
- [ ] `tsconfig.json` - TypeScript configuration
- [ ] `next.config.js` - Next.js configuration
- [ ] `tailwind.config.ts` - Tailwind configuration
- [ ] `postcss.config.js` - PostCSS configuration

**Complete Code:**

Create file `package.json`:
```json
{
  "name": "user-dashboard",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/react": "^14.0.0",
    "@types/jest": "^29.5.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "autoprefixer": "^10.4.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "14.0.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.0.0"
  }
}
```

Create file `tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

Create file `next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
```

Create file `tailwind.config.ts`:
```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
};

export default config;
```

Create file `postcss.config.js`:
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

**Verification:**
```bash
# Install dependencies
npm install
# Expected: Packages installed successfully

# Verify TypeScript
npx tsc --noEmit
# Expected: No errors (may warn about missing files, that's OK)
```

**Success Criteria:**
- [ ] `npm install` succeeds
- [ ] All config files exist
- [ ] TypeScript configured with strict mode

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `package.json`, `tsconfig.json`, `next.config.js`, `tailwind.config.ts`, `postcss.config.js`
- **Verification**: [To be filled]

---

### Subtask 1.1.2: Create App Structure and Types

**Prerequisites:** 1.1.1 complete

**Deliverables:**
- [ ] `src/app/layout.tsx` - Root layout
- [ ] `src/app/page.tsx` - Home page placeholder
- [ ] `src/app/globals.css` - Global styles
- [ ] `src/types/index.ts` - Type definitions

**Complete Code:**

Create file `src/types/index.ts`:
```typescript
export interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
}

export type Theme = 'light' | 'dark';

export interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

export interface UserContextType {
  user: User;
  updateUser: (user: Partial<User>) => void;
}
```

Create file `src/app/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-rgb: 255, 255, 255;
}

.dark {
  --foreground-rgb: 255, 255, 255;
  --background-rgb: 17, 24, 39;
}

body {
  color: rgb(var(--foreground-rgb));
  background: rgb(var(--background-rgb));
}
```

Create file `src/app/layout.tsx`:
```tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'User Dashboard',
  description: 'A minimal user profile dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

Create file `src/app/page.tsx`:
```tsx
export default function Home(): JSX.Element {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-2xl font-bold">User Dashboard</h1>
      <p className="text-gray-600">Coming soon...</p>
    </main>
  );
}
```

**Verification:**
```bash
# Run dev server
npm run dev &
sleep 5

# Check if server responds
curl -s http://localhost:3000 | grep -q "User Dashboard"
echo "Server check: $?"
# Expected: 0 (success)

# Stop dev server
pkill -f "next dev"

# Lint check
npm run lint
# Expected: No errors
```

**Success Criteria:**
- [ ] Dev server starts without errors
- [ ] Page renders "User Dashboard"
- [ ] No lint errors

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/types/index.ts`, `src/app/globals.css`, `src/app/layout.tsx`, `src/app/page.tsx`
- **Verification**: [To be filled]

---

### Task 1.1 Complete - Squash Merge

**When all subtasks (1.1.1, 1.1.2) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/1.1-project-init

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/1.1-project-init
git commit -m "feat(setup): initialize Next.js project

- Add package.json with dependencies
- Configure TypeScript, Tailwind, PostCSS
- Create app layout and home page
- Add type definitions"
git push origin main

# Delete feature branch
git branch -d feature/1.1-project-init
git push origin --delete feature/1.1-project-init
```

**Checklist:**
- [ ] All subtasks complete (1.1.1, 1.1.2)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 1.2: Create Context Providers

**Branch:** `feature/1.2-context-providers`

### Subtask 1.2.1: Implement Theme and User Contexts

**Prerequisites:** Task 1.1 complete

**Deliverables:**
- [ ] `src/context/ThemeContext.tsx` - Theme state management
- [ ] `src/context/UserContext.tsx` - User state management
- [ ] `src/lib/mockData.ts` - Mock user data
- [ ] Update `src/app/layout.tsx` - Add providers

**Complete Code:**

Create file `src/lib/mockData.ts`:
```typescript
import type { User } from '@/types';

export const mockUser: User = {
  id: '1',
  name: 'Jane Doe',
  email: 'jane.doe@example.com',
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jane',
};
```

Create file `src/context/ThemeContext.tsx`:
```tsx
'use client';

import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from 'react';
import type { Theme, ThemeContextType } from '@/types';

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }): JSX.Element {
  const [theme, setTheme] = useState<Theme>('light');

  useEffect(() => {
    const stored = localStorage.getItem('theme') as Theme | null;
    if (stored) {
      setTheme(stored);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark');
    }
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = (): void => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
```

Create file `src/context/UserContext.tsx`:
```tsx
'use client';

import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from 'react';
import type { User, UserContextType } from '@/types';
import { mockUser } from '@/lib/mockData';

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }): JSX.Element {
  const [user, setUser] = useState<User>(mockUser);

  const updateUser = (updates: Partial<User>): void => {
    setUser((prev) => ({ ...prev, ...updates }));
  };

  return (
    <UserContext.Provider value={{ user, updateUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser(): UserContextType {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}
```

Replace `src/app/layout.tsx` with:
```tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ThemeProvider } from '@/context/ThemeContext';
import { UserProvider } from '@/context/UserContext';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'User Dashboard',
  description: 'A minimal user profile dashboard',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider>
          <UserProvider>{children}</UserProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
```

**Verification:**
```bash
# Type check
npm run type-check
# Expected: No errors

# Lint check
npm run lint
# Expected: No errors

# Build check
npm run build
# Expected: Build successful
```

**Success Criteria:**
- [ ] Type check passes
- [ ] Lint passes
- [ ] Build succeeds
- [ ] Contexts provide theme and user state

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/lib/mockData.ts`, `src/context/ThemeContext.tsx`, `src/context/UserContext.tsx`
- **Files Modified**: `src/app/layout.tsx`
- **Verification**: [To be filled]

---

### Task 1.2 Complete - Squash Merge

**When all subtasks (1.2.1) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/1.2-context-providers

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/1.2-context-providers
git commit -m "feat(context): add theme and user providers

- Add ThemeContext with dark mode support
- Add UserContext with mock data
- Integrate providers in root layout"
git push origin main

# Delete feature branch
git branch -d feature/1.2-context-providers
git push origin --delete feature/1.2-context-providers
```

**Checklist:**
- [ ] All subtasks complete (1.2.1)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Phase 2: Dashboard Implementation

## Task 2.1: Create UI Components

**Branch:** `feature/2.1-ui-components`

### Subtask 2.1.1: Create Header and ThemeToggle

**Prerequisites:** Task 1.2 complete

**Deliverables:**
- [ ] `src/components/ThemeToggle.tsx` - Theme toggle button
- [ ] `src/components/Header.tsx` - App header

**Complete Code:**

Create file `src/components/ThemeToggle.tsx`:
```tsx
'use client';

import { useTheme } from '@/context/ThemeContext';

export function ThemeToggle(): JSX.Element {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      {theme === 'light' ? (
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
          />
        </svg>
      ) : (
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
          />
        </svg>
      )}
    </button>
  );
}
```

Create file `src/components/Header.tsx`:
```tsx
import { ThemeToggle } from './ThemeToggle';

export function Header(): JSX.Element {
  return (
    <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
      <h1 className="text-xl font-bold">User Dashboard</h1>
      <ThemeToggle />
    </header>
  );
}
```

**Verification:**
```bash
# Type check
npm run type-check
# Expected: No errors

# Lint check
npm run lint
# Expected: No errors
```

**Success Criteria:**
- [ ] ThemeToggle renders correct icon for current theme
- [ ] Header includes title and theme toggle
- [ ] Accessible with aria-label

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/components/ThemeToggle.tsx`, `src/components/Header.tsx`
- **Verification**: [To be filled]

---

### Subtask 2.1.2: Create ProfileCard and EditModal

**Prerequisites:** 2.1.1 complete

**Deliverables:**
- [ ] `src/components/ProfileCard.tsx` - User profile display
- [ ] `src/components/EditModal.tsx` - Profile edit modal

**Complete Code:**

Create file `src/components/ProfileCard.tsx`:
```tsx
'use client';

import { useUser } from '@/context/UserContext';

interface ProfileCardProps {
  onEdit: () => void;
}

export function ProfileCard({ onEdit }: ProfileCardProps): JSX.Element {
  const { user } = useUser();

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 max-w-md mx-auto">
      <div className="flex items-center space-x-4">
        <img
          src={user.avatar}
          alt={`${user.name}'s avatar`}
          className="w-16 h-16 rounded-full"
        />
        <div className="flex-1">
          <h2 className="text-xl font-semibold">{user.name}</h2>
          <p className="text-gray-600 dark:text-gray-400">{user.email}</p>
        </div>
      </div>
      <button
        onClick={onEdit}
        className="mt-4 w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
        aria-label="Edit profile"
      >
        Edit Profile
      </button>
    </div>
  );
}
```

Create file `src/components/EditModal.tsx`:
```tsx
'use client';

import { useState, useEffect, useRef } from 'react';
import { useUser } from '@/context/UserContext';

interface EditModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function EditModal({ isOpen, onClose }: EditModalProps): JSX.Element | null {
  const { user, updateUser } = useUser();
  const [name, setName] = useState(user.name);
  const [email, setEmail] = useState(user.email);
  const [isLoading, setIsLoading] = useState(false);
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      setName(user.name);
      setEmail(user.email);
    }
  }, [isOpen, user.name, user.email]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent): void => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      modalRef.current?.focus();
    }

    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 500));

    updateUser({ name, email });
    setIsLoading(false);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={(e) => e.target === e.currentTarget && onClose()}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        ref={modalRef}
        tabIndex={-1}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md"
      >
        <h2 id="modal-title" className="text-xl font-semibold mb-4">
          Edit Profile
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="name"
              className="block text-sm font-medium mb-1"
            >
              Name
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:ring-2 focus:ring-blue-500 outline-none"
              required
            />
          </div>
          <div className="mb-6">
            <label
              htmlFor="email"
              className="block text-sm font-medium mb-1"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:ring-2 focus:ring-blue-500 outline-none"
              required
            />
          </div>
          <div className="flex space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 py-2 px-4 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-400 text-white rounded-lg transition-colors"
            >
              {isLoading ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

**Verification:**
```bash
# Type check
npm run type-check
# Expected: No errors

# Lint check
npm run lint
# Expected: No errors
```

**Success Criteria:**
- [ ] ProfileCard displays user info and edit button
- [ ] EditModal opens/closes correctly
- [ ] Form saves changes to user context
- [ ] Loading state shows during save
- [ ] Escape key closes modal

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `src/components/ProfileCard.tsx`, `src/components/EditModal.tsx`
- **Verification**: [To be filled]

---

### Task 2.1 Complete - Squash Merge

**When all subtasks (2.1.1, 2.1.2) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/2.1-ui-components

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/2.1-ui-components
git commit -m "feat(ui): add dashboard components

- Add Header with ThemeToggle
- Add ProfileCard with user display
- Add EditModal for profile editing
- Dark mode support throughout"
git push origin main

# Delete feature branch
git branch -d feature/2.1-ui-components
git push origin --delete feature/2.1-ui-components
```

**Checklist:**
- [ ] All subtasks complete (2.1.1, 2.1.2)
- [ ] All verification passes
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

## Task 2.2: Integrate Dashboard and Tests

**Branch:** `feature/2.2-integration`

### Subtask 2.2.1: Complete Dashboard Page

**Prerequisites:** Task 2.1 complete

**Deliverables:**
- [ ] Update `src/app/page.tsx` - Complete dashboard

**Complete Code:**

Replace `src/app/page.tsx` with:
```tsx
'use client';

import { useState } from 'react';
import { Header } from '@/components/Header';
import { ProfileCard } from '@/components/ProfileCard';
import { EditModal } from '@/components/EditModal';

export default function Home(): JSX.Element {
  const [isEditOpen, setIsEditOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      <Header />
      <main className="p-8">
        <ProfileCard onEdit={() => setIsEditOpen(true)} />
        <EditModal isOpen={isEditOpen} onClose={() => setIsEditOpen(false)} />
      </main>
    </div>
  );
}
```

**Verification:**
```bash
# Build check
npm run build
# Expected: Build successful

# Run dev server and manual test
npm run dev
# Visit http://localhost:3000
# Expected: Dashboard with profile card, theme toggle works, edit modal works
```

**Success Criteria:**
- [ ] Dashboard renders with header and profile
- [ ] Theme toggle switches colors
- [ ] Edit button opens modal
- [ ] Changes save to profile

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Modified**: `src/app/page.tsx`
- **Verification**: [To be filled]

---

### Subtask 2.2.2: Add Tests

**Prerequisites:** 2.2.1 complete

**Deliverables:**
- [ ] `jest.config.js` - Jest configuration
- [ ] `__tests__/setup.ts` - Test setup
- [ ] `__tests__/components/ProfileCard.test.tsx` - Component tests

**Complete Code:**

Create file `jest.config.js`:
```javascript
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/__tests__/setup.ts'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testPathIgnorePatterns: ['<rootDir>/__tests__/setup.ts'],
};

module.exports = createJestConfig(customJestConfig);
```

Create file `__tests__/setup.ts`:
```typescript
import '@testing-library/jest-dom';
```

Create file `__tests__/components/ProfileCard.test.tsx`:
```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ProfileCard } from '@/components/ProfileCard';
import { UserProvider } from '@/context/UserContext';

const renderWithProviders = (ui: React.ReactElement) => {
  return render(<UserProvider>{ui}</UserProvider>);
};

describe('ProfileCard', () => {
  it('renders user information', () => {
    const onEdit = jest.fn();
    renderWithProviders(<ProfileCard onEdit={onEdit} />);

    expect(screen.getByText('Jane Doe')).toBeInTheDocument();
    expect(screen.getByText('jane.doe@example.com')).toBeInTheDocument();
  });

  it('renders avatar with alt text', () => {
    const onEdit = jest.fn();
    renderWithProviders(<ProfileCard onEdit={onEdit} />);

    const avatar = screen.getByAltText("Jane Doe's avatar");
    expect(avatar).toBeInTheDocument();
  });

  it('calls onEdit when edit button clicked', () => {
    const onEdit = jest.fn();
    renderWithProviders(<ProfileCard onEdit={onEdit} />);

    const editButton = screen.getByRole('button', { name: /edit profile/i });
    fireEvent.click(editButton);

    expect(onEdit).toHaveBeenCalledTimes(1);
  });

  it('has accessible edit button', () => {
    const onEdit = jest.fn();
    renderWithProviders(<ProfileCard onEdit={onEdit} />);

    const editButton = screen.getByRole('button', { name: /edit profile/i });
    expect(editButton).toHaveAttribute('aria-label', 'Edit profile');
  });
});
```

**Verification:**
```bash
# Run tests
npm run test
# Expected: 4 tests passing

# Type check
npm run type-check
# Expected: No errors

# Lint check
npm run lint
# Expected: No errors

# Build check
npm run build
# Expected: Build successful
```

**Success Criteria:**
- [ ] All 4 tests pass
- [ ] Type check passes
- [ ] Lint passes
- [ ] Build succeeds

**Completion Notes:**
- **Implementation**: [To be filled by executor]
- **Files Created**: `jest.config.js`, `__tests__/setup.ts`, `__tests__/components/ProfileCard.test.tsx`
- **Tests**: 4 tests passing
- **Verification**: [To be filled]

---

### Task 2.2 Complete - Squash Merge

**When all subtasks (2.2.1, 2.2.2) are complete, execute:**

```bash
# Push feature branch
git push -u origin feature/2.2-integration

# Switch to main and merge
git checkout main
git pull origin main
git merge --squash feature/2.2-integration
git commit -m "feat(dashboard): complete integration and tests

- Integrate all components in dashboard page
- Add Jest configuration
- Add ProfileCard tests
- 4 tests passing"
git push origin main

# Delete feature branch
git branch -d feature/2.2-integration
git push origin --delete feature/2.2-integration
```

**Checklist:**
- [ ] All subtasks complete (2.2.1, 2.2.2)
- [ ] All tests pass
- [ ] Squash merged to main
- [ ] Feature branch deleted

---

# Project Complete Checklist

- [ ] Phase 1: Project Setup complete
- [ ] Phase 2: Dashboard Implementation complete
- [ ] All tests pass (4 tests)
- [ ] Type check passes
- [ ] Lint passes
- [ ] Build succeeds
- [ ] Dashboard works: profile display, theme toggle, edit modal
- [ ] Clean git history (squash merges only)
