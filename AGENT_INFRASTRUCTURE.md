Agent Infrastructure Documentation
Version: 1.0 Last Updated: 2025-12-07 Project: Sequel Security Posture Assessor (whag-1)

This document describes the custom agent system, NATS-based inter-agent communication, and persistent memory infrastructure used in this project. It provides everything needed to port this infrastructure to other projects.

Quick Start
Want to port this to your project in 10 minutes? Jump to Porting to a New Project.

Just want to understand how it works? Read Overview and Architecture.

Having problems? See Troubleshooting.

Table of Contents
Overview
Architecture
Custom Agents
NATS Messaging System
Agent Memory MCP Server
Setup Guide
Porting to a New Project
Troubleshooting
Advanced Features
Overview
This project uses a multi-agent architecture where specialized AI agents collaborate via NATS messaging to complete complex development tasks. Each agent has a specific role (TDD coding, QA testing, DevOps deployment, documentation) and can communicate with other agents to request reviews, share results, and coordinate work.

Communication Layer

Agent Layer

MCP Protocol

MCP Protocol

MCP Protocol

MCP Protocol

MCP Protocol

MCP Protocol

Publish/Subscribe

Store/Retrieve

tdd-coder

tdd-qa

qa-engineer

devops

docs-specialist

docs-qa

Agent Memory
MCP Server

NATS Server
JetStream

SQLite
Memory DB

Key Benefits
Specialized Expertise: Each agent is optimized for a specific role
Asynchronous Collaboration: Agents work independently but coordinate through messaging
Persistent Learning: Agents learn from past reviews and mistakes
Scalable: Multiple agents can work in parallel
Reproducible: All agent communication is logged and auditable
Architecture
Components
Custom Agents - Markdown files defining agent behavior, tools, and permissions
NATS Server - Message broker for inter-agent communication
Agent Memory MCP Server - Model Context Protocol server exposing NATS and SQLite to agents
SQLite Database - Persistent storage for reviews, learnings, and activity logs
Claude Code - Execution environment for agents
Message Flow States
Agent starts

broadcast_status("working")

get_pending_reviews()

Found reviews

No reviews

Code complete

request_review()

Review complete

submit_review()

broadcast_status("completed")

Idle

Working

CheckingReviews

Reviewing

Coding

RequestingReview

SubmittingReview

Completed

Data Flow
TDD QA
SQLite DB
NATS JetStream
MCP Server
TDD Coder
TDD QA
SQLite DB
NATS JetStream
MCP Server
TDD Coder
broadcast_status("working")
Publish to INTEGRATION stream
request_review("tdd-qa", "code", "/path/to/file")
Store review request
Publish to REVIEWS stream
get_pending_reviews("tdd-qa")
Fetch from REVIEWS stream
Review requests
Pending reviews
get_review_context("tdd-qa", "/path/to/file")
Query past reviews
Historical data
Context with learnings
submit_review(...)
Store review response & extract learnings
Publish to REVIEWS stream
File Organization
project-root/
├── .claude/
│   ├── agents/
│   │   ├── _shared-nats.md       # NATS protocol docs (all agents include)
│   │   ├── tdd-coder.md          # TDD coding agent
│   │   ├── tdd-qa.md             # Test quality agent
│   │   ├── qa-engineer.md        # Integration testing agent
│   │   ├── devops.md             # Infrastructure agent
│   │   ├── docs-specialist.md    # Documentation writer
│   │   ├── docs-qa.md            # Documentation accuracy
│   │   └── web-designer.md       # Web design agent
│   └── settings.local.json       # MCP server configuration
├── scripts/
│   ├── agent_memory_server.py    # MCP server (FastMCP)
│   ├── agent_memory_core.py      # Business logic (testable)
│   └── agent_memory_db.py        # SQLite persistence
├── data/
│   └── agent_memory.db           # SQLite database (auto-created)
├── tests/
│   └── unit/
│       ├── test_agent_memory_server.py
│       ├── test_agent_memory_core.py
│       └── test_agent_memory_db.py
└── requirements.txt              # nats-py, fastmcp
Custom Agents
Agent Definition Format
Agents are defined in .claude/agents/*.md files with YAML frontmatter:

---
name: agent-name
color: blue
description: Brief description of agent's role
tools: Read, Edit, Write, Bash, Grep, Glob, TodoWrite
model: sonnet
permissionMode: bypassPermissions  # optional
---

# Agent Name

Agent instructions in markdown...
Agent Configuration Fields
Field	Required	Description	Example
name	Yes	Unique identifier for the agent	tdd-coder
color	No	Visual identifier in Claude Code UI	green, blue, red
description	Yes	Brief description of agent's purpose	Autonomous TDD coder agent
tools	Yes	Comma-separated list of tools agent can use	Read, Edit, Write, Bash
model	Yes	Claude model to use	sonnet, opus, haiku
permissionMode	No	Permission handling mode	bypassPermissions
Available Tools
Common tools agents use:

File Operations: Read, Edit, Write, Glob, Grep
Execution: Bash
Web: WebSearch, WebFetch
Utilities: TodoWrite, NotebookEdit
MCP Tools: Any tool exposed by MCP servers (e.g., mcp__agent-memory__*)
Existing Agents in This Project
Agent	Role	Key Responsibilities	When to Use
tdd-coder	TDD Development	Write tests first, implement code, quality gates, commit	Building new features, refactoring existing code
tdd-qa	Test Quality Assurance	Audit test coverage, identify weak assertions, enforce TDD	After code completion, before merging to main
qa-engineer	Integration Testing	Deploy to devtest, run browser tests, verify runtime	Before deployments, after major changes
devops	Infrastructure	Deploy AWS resources, Lambda functions, verify deployments	Infrastructure changes, new environments
docs-specialist	Documentation Writing	Create/improve docs, add Mermaid diagrams, maintain accuracy	New features needing docs, documentation improvements
docs-qa	Documentation Accuracy	Verify docs match codebase, check links, find outdated info	After code changes, quarterly doc audits
web-designer	Web Design	Analyze brand, create landing pages, responsive HTML/CSS	Marketing pages, landing pages, UI components
value-chain-expert	Business Analysis	Analyze features, strategic impact, value chain mapping	Feature planning, strategic decisions
Agent Collaboration Patterns
Common workflows showing how agents work together:

Feature Development Flow

request_review

changes_requested

approved

request_review

approved

tests pass

deployed

tdd-coder
writes code

tdd-qa
reviews tests

docs-specialist
documents

docs-qa
verifies docs

qa-engineer
integration tests

devops
deploys

Done

Agent Instruction Best Practices
Clear Mission: State the agent's purpose in the first paragraph
Structured Workflow: Use numbered steps or phases
Decision Trees: Provide clear if/then logic for common scenarios
Examples: Include code snippets, command examples, and output formats
Quality Gates: Define success criteria and verification steps
Error Handling: Describe what to do when things fail
NATS Integration: Include the standard NATS communication block (see below)
Standard NATS Communication Block
All agents should include this section:

## Inter-Agent Communication (NATS)

You have access to MCP tools for communicating with other agents. **USE THESE TOOLS.**

### At Start of Work
1. `mcp__agent-memory__broadcast_status("YOUR_AGENT_NAME", "working", "task description", 0)`
2. `mcp__agent-memory__get_pending_reviews("YOUR_AGENT_NAME")` - Check for review requests
3. `mcp__agent-memory__get_messages("INTEGRATION", null, 10)` - Check for coordination messages

### During Work
- Update status periodically: `mcp__agent-memory__broadcast_status("YOUR_AGENT_NAME", "working", "current task", progress_pct)`

### At End of Work
1. Share results: `mcp__agent-memory__share_result("result_type", "title", "summary", "YOUR_AGENT_NAME", ["tags"])`
2. Request review if needed: `mcp__agent-memory__request_review("reviewer_agent", "item_type", "path", "description", "YOUR_AGENT_NAME", "normal")`
3. Complete: `mcp__agent-memory__broadcast_status("YOUR_AGENT_NAME", "completed", "summary", 100)`

### Review Workflow
- To request: `mcp__agent-memory__request_review(reviewer, item_type, item_path, description, requester, priority)`
- To check pending: `mcp__agent-memory__get_pending_reviews("YOUR_AGENT_NAME")`
- To submit: `mcp__agent-memory__submit_review(requester, item_path, "YOUR_AGENT_NAME", status, findings, summary)`

See `.claude/agents/_shared-nats.md` for full documentation.
NATS Messaging System
What is NATS?
NATS is a lightweight, high-performance message broker. We use NATS JetStream for persistent, replay-able messaging between agents.

Message Streams
Agents communicate via four primary streams:

Stream	Purpose	Subjects	Retention
REQUIREMENTS	Task specifications	requirements.*	7 days
INTEGRATION	Agent coordination	integration.status.*, integration.*	7 days
RESULTS	Work outputs	results.<type>.<agent>	30 days
REVIEWS	Code/doc reviews	reviews.request.*, reviews.response.*	30 days
Subject Naming Convention
<stream>.<category>.<target>
Examples:

integration.status.tdd-coder - TDD coder's status updates
reviews.request.tdd-qa - Review requests for TDD QA agent
results.test_report.qa-engineer - Test reports from QA engineer
Message Format
All messages are JSON with this structure:

{
  "sender": "agent-name",
  "timestamp": "2025-12-07T12:00:00Z",
  "message": "Human-readable message or payload",
  "metadata": {
    "key": "value"
  }
}
For reviews, the message contains a review_request or review_response object.

Agent Memory MCP Server
What is the Agent Memory Server?
The Agent Memory MCP Server is a Model Context Protocol (MCP) server that exposes NATS messaging and SQLite database operations as tools that Claude agents can use.

MCP Server Location
Server Script: scripts/agent_memory_server.py
Core Logic: scripts/agent_memory_core.py (testable business logic)
Database: scripts/agent_memory_db.py (SQLite schema and queries)
Tests: tests/unit/test_agent_memory_server.py, tests/unit/test_agent_memory_db.py
Available MCP Tools
Status & Coordination
mcp__agent-memory__broadcast_status(agent, status, current_task, progress)
# Broadcast agent status to all other agents
# status: "idle", "working", "blocked", "completed"
# progress: 0-100

mcp__agent-memory__get_all_agent_statuses()
# Get the latest status from all agents
Messaging
mcp__agent-memory__publish_message(stream, subject, message, sender, metadata)
# Publish a message to a NATS stream

mcp__agent-memory__get_messages(stream, subject, limit)
# Get recent messages from a NATS stream
# subject: Optional filter (e.g., "requirements.qa")
Reviews
mcp__agent-memory__request_review(reviewer, item_type, item_path, description, requester, priority)
# Request a review from another agent
# item_type: "code", "documentation", "test", "config"
# priority: "low", "normal", "high", "urgent"

mcp__agent-memory__submit_review(original_requester, item_path, reviewer, status, findings, summary)
# Submit a review response
# status: "approved", "changes_requested", "needs_discussion"
# findings: List of {severity, location, message, suggestion}

mcp__agent-memory__get_pending_reviews(agent)
# Get pending review requests for an agent
Results
mcp__agent-memory__share_result(result_type, title, content, sender, tags)
# Share a work result with other agents
# result_type: "test_report", "deployment", "analysis", "documentation"

mcp__agent-memory__get_agent_results(agent, result_type, limit)
# Get results shared by agents
Memory & Learning
mcp__agent-memory__get_review_context(reviewer, item_path)
# Get context about a file before reviewing it
# Returns: past reviews, known issues, common findings

mcp__agent-memory__get_coder_context(coder, item_path)
# Get warnings before modifying a file
# Returns: previous review feedback, known issues

mcp__agent-memory__get_my_learnings(agent, category)
# Get learnings/patterns discovered from past reviews
# category: "testing", "security", "code_quality", etc.

mcp__agent-memory__get_common_issues(category)
# Get frequently occurring issues across all reviews

mcp__agent-memory__get_file_history(item_path)
# Get review history for a specific file
Database Schema
The SQLite database (data/agent_memory.db) stores:

reviews - Review requests and responses
review_findings - Individual findings from reviews
learnings - Extracted patterns and recommendations
results - Shared work results
activity_log - Agent activity history
Key features:

Automatic learning extraction from review findings
Pattern recognition for common issues
File-level review history
Agent-specific learning retrieval
Setup Guide
Prerequisites
Python 3.11+
NATS Server (with JetStream enabled)
Claude Code or Claude API access
Step 1: Install NATS Server
Option A: Docker (Recommended)

docker run -d --name nats-server \
  -p 4222:4222 \
  -p 8222:8222 \
  nats:latest \
  -js
Option B: Native Installation

# macOS
brew install nats-server

# Linux (from source)
wget https://github.com/nats-io/nats-server/releases/download/v2.10.7/nats-server-v2.10.7-linux-amd64.tar.gz
tar -xzf nats-server-v2.10.7-linux-amd64.tar.gz
sudo mv nats-server-v2.10.7-linux-amd64/nats-server /usr/local/bin/
Start NATS with JetStream:

nats-server -js
Verify it's running:

curl http://localhost:8222/varz
Step 2: Install Python Dependencies
# Add to requirements.txt
nats-py>=2.7.0

# Add to requirements-dev.txt
fastmcp>=0.4.0

# Install
pip install nats-py fastmcp
Step 3: Create NATS Streams
# Option 1: Use NATS CLI
nats stream add REQUIREMENTS --subjects "requirements.*" --storage file --retention limits --max-age 7d
nats stream add INTEGRATION --subjects "integration.*" --storage file --retention limits --max-age 7d
nats stream add RESULTS --subjects "results.*" --storage file --retention limits --max-age 30d
nats stream add REVIEWS --subjects "reviews.*" --storage file --retention limits --max-age 30d

# Option 2: Streams are auto-created by the MCP server on first use (recommended)
Step 4: Configure MCP Server in Claude Code
Create or update .claude/settings.local.json:

{
  "permissions": {
    "allow": [
      "mcp__agent-memory__*"
    ]
  },
  "mcpServers": {
    "agent-memory": {
      "type": "stdio",
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/scripts/agent_memory_server.py"],
      "env": {
        "NATS_URL": "nats://localhost:4222",
        "AGENT_MEMORY_DB": "/path/to/data/agent_memory.db"
      }
    }
  }
}
Important: Use absolute paths for:

Python interpreter (/path/to/venv/bin/python)
Server script (/path/to/scripts/agent_memory_server.py)
Database path (/path/to/data/agent_memory.db)
Step 5: Create Agent Definitions
Create .claude/agents/_shared-nats.md with the communication protocol (see example in this repo).

Create individual agent files (.claude/agents/agent-name.md) with YAML frontmatter and instructions.

Step 6: Test the Setup
Test NATS connectivity:

python3 << 'EOF'
import asyncio
from agent_memory_core import get_nats, publish_message

async def test():
    nc, js = await get_nats()
    print(f"Connected to NATS: {nc.is_connected}")
    result = await publish_message("INTEGRATION", "integration.test", "Hello from test", "system")
    print(result)
    await nc.close()

asyncio.run(test())
EOF
Test MCP server:

# Start the server manually
export NATS_URL="nats://localhost:4222"
python scripts/agent_memory_server.py
Test from Claude Code:

Open Claude Code, select an agent, and run:

@tdd-coder Please broadcast your status as "testing" with progress 0
The agent should use mcp__agent-memory__broadcast_status(...).

Porting to a New Project
Checklist
[ ] Install NATS server
[ ] Copy agent infrastructure files
[ ] Update agent definitions for new project
[ ] Configure MCP server in Claude settings
[ ] Create project-specific NATS streams (or let them auto-create)
[ ] Test communication between agents
Files to Copy
Source Project                    → Destination Project
──────────────────────────────────────────────────────────
scripts/agent_memory_server.py    → scripts/agent_memory_server.py
scripts/agent_memory_core.py      → scripts/agent_memory_core.py
scripts/agent_memory_db.py        → scripts/agent_memory_db.py
.claude/agents/_shared-nats.md    → .claude/agents/_shared-nats.md
tests/unit/test_agent_memory_*.py → tests/unit/test_agent_memory_*.py
10-Minute Quick Start
For those who just want to get it working fast:

# 1. Install NATS (Docker)
docker run -d --name nats -p 4222:4222 -p 8222:8222 nats:latest -js

# 2. Install Python dependencies
pip install nats-py fastmcp

# 3. Copy files from source project
SOURCE=/path/to/whag-1
DEST=/path/to/new-project

mkdir -p $DEST/scripts $DEST/.claude/agents $DEST/data
cp $SOURCE/scripts/agent_memory_*.py $DEST/scripts/
cp $SOURCE/.claude/agents/_shared-nats.md $DEST/.claude/agents/
cp $SOURCE/.claude/agents/tdd-coder.md $DEST/.claude/agents/  # Copy agents you need

# 4. Create MCP config (use ABSOLUTE PATHS!)
cat > $DEST/.claude/settings.local.json << 'EOF'
{
  "permissions": {"allow": ["mcp__agent-memory__*"]},
  "mcpServers": {
    "agent-memory": {
      "type": "stdio",
      "command": "/ABSOLUTE/PATH/TO/venv/bin/python",
      "args": ["/ABSOLUTE/PATH/TO/scripts/agent_memory_server.py"],
      "env": {
        "NATS_URL": "nats://localhost:4222"
      }
    }
  }
}
EOF

# 5. Test it
export NATS_URL="nats://localhost:4222"
python3 -c "import asyncio; from scripts.agent_memory_core import get_nats; asyncio.run(get_nats())"

# 6. Done! Open Claude Code and select an agent
Step-by-Step Porting Guide
1. Copy Infrastructure Scripts
# From source project
cd /path/to/source-project
mkdir -p /path/to/new-project/scripts
cp scripts/agent_memory_*.py /path/to/new-project/scripts/
2. Create Agent Configuration Directory
cd /path/to/new-project
mkdir -p .claude/agents
3. Copy Shared NATS Documentation
cp /path/to/source-project/.claude/agents/_shared-nats.md \
   /path/to/new-project/.claude/agents/_shared-nats.md
4. Create New Agent Definitions
Instead of copying all agents, create only the ones relevant to your new project:

# Example: Copy TDD-focused agents for a new backend project
cp /path/to/source/.claude/agents/tdd-coder.md /path/to/new/.claude/agents/
cp /path/to/source/.claude/agents/tdd-qa.md /path/to/new/.claude/agents/
cp /path/to/source/.claude/agents/devops.md /path/to/new/.claude/agents/
Customize agent instructions for the new project:

Update technology stack references (Python → Node.js, AWS → GCP, etc.)
Modify quality gates (coverage thresholds, linting tools)
Adjust file paths and directory structure
Update deployment procedures
5. Update Dependencies
cd /path/to/new-project

# Add to requirements.txt
echo "nats-py>=2.7.0" >> requirements.txt

# Add to requirements-dev.txt (or requirements.txt if dev)
echo "fastmcp>=0.4.0" >> requirements-dev.txt

pip install -r requirements.txt -r requirements-dev.txt
6. Configure Claude Code MCP Server
Create .claude/settings.local.json:

{
  "permissions": {
    "allow": [
      "mcp__agent-memory__*",
      "Bash(git:*)",
      "Bash(pytest:*)",
      "Bash(npm:*)"
    ]
  },
  "mcpServers": {
    "agent-memory": {
      "type": "stdio",
      "command": "/absolute/path/to/new-project/venv/bin/python",
      "args": ["/absolute/path/to/new-project/scripts/agent_memory_server.py"],
      "env": {
        "NATS_URL": "nats://localhost:4222",
        "AGENT_MEMORY_DB": "/absolute/path/to/new-project/data/agent_memory.db"
      }
    }
  }
}
Critical: Use absolute paths, not relative ones.

7. Create Data Directory
mkdir -p data
The SQLite database will be created automatically on first use.

8. Start NATS Server
# If using Docker
docker run -d --name nats-server \
  -p 4222:4222 \
  -p 8222:8222 \
  nats:latest -js

# If installed natively
nats-server -js
9. Verify Setup
# Test NATS connection
python3 << 'EOF'
import asyncio
from scripts.agent_memory_core import get_nats

async def test():
    nc, js = await get_nats()
    print(f"✓ Connected to NATS: {nc.is_connected}")
    await nc.close()

asyncio.run(test())
EOF

# Expected output: ✓ Connected to NATS: True
# Test MCP server startup
export NATS_URL="nats://localhost:4222"
python scripts/agent_memory_server.py &

# Should see: FastMCP server running...
10. Test Agent Communication
Open Claude Code, select an agent (e.g., tdd-coder), and ask:

Please broadcast your status as "idle" and check for any pending reviews.
The agent should execute:

mcp__agent-memory__broadcast_status("tdd-coder", "idle", "Waiting for tasks", 0)
mcp__agent-memory__get_pending_reviews("tdd-coder")
Customization for Different Project Types
Backend API Project (Python/FastAPI)
Key agents:

tdd-coder - Write API endpoints with tests
tdd-qa - Audit test coverage
devops - Deploy to AWS/GCP
docs-specialist - API documentation
Customize:

Update tech stack references (FastAPI, Pydantic, pytest)
Adjust deployment targets
Modify quality gates for API testing
Frontend Project (React/TypeScript)
Key agents:

web-designer - Design components and pages
tdd-coder - Write React components with tests
qa-engineer - Browser testing with Playwright
docs-specialist - Component documentation
Customize:

Replace Python references with TypeScript
Update test commands (pytest → jest)
Modify quality gates (eslint, prettier)
Infrastructure/DevOps Project (Terraform)
Key agents:

devops - Deploy infrastructure
docs-specialist - Infrastructure documentation
qa-engineer - Integration testing
Customize:

Focus on Terraform, CloudFormation, or Pulumi
Update deployment verification steps
Add infrastructure-specific quality gates
Data Science/ML Project (Python/Jupyter)
Key agents:

tdd-coder - Write data pipelines with tests
docs-specialist - Document models and experiments
qa-engineer - Validate model outputs
Customize:

Add notebook handling
Update test requirements (data validation)
Include model versioning and experiment tracking
Troubleshooting
NATS Connection Issues
Problem: Error connecting to NATS

Solutions:

Verify NATS is running:
curl http://localhost:8222/varz
Check the NATS URL:
echo $NATS_URL  # Should be nats://localhost:4222
Check firewall/port:
netstat -an | grep 4222
Restart NATS:
docker restart nats-server
# or
killall nats-server && nats-server -js
MCP Server Not Starting
Problem: MCP server fails to start in Claude Code

Solutions:

Check paths in .claude/settings.local.json are absolute
Verify Python has required packages:
/path/to/venv/bin/python -c "import fastmcp, nats"
Test server manually:
export NATS_URL="nats://localhost:4222"
/path/to/venv/bin/python scripts/agent_memory_server.py
Check Claude Code logs for errors
Ensure data/ directory exists and is writable
Agents Not Communicating
Problem: Agent calls MCP tools but messages don't appear

Solutions:

Verify streams exist:
nats stream ls
Check message flow:
nats stream info INTEGRATION
Monitor NATS in real-time:
nats sub "integration.>" --stream INTEGRATION
Check database for stored data:
sqlite3 data/agent_memory.db "SELECT * FROM reviews LIMIT 5;"
Database Locked Errors
Problem: database is locked errors

Solutions:

Ensure only one MCP server instance is running
Close any SQLite browser/editor connections
Reset the database:
mv data/agent_memory.db data/agent_memory.db.bak
Add timeout to database connections (already implemented in agent_memory_db.py)
Permission Denied Errors
Problem: Agent can't use MCP tools

Solutions:

Add MCP tool permissions to .claude/settings.local.json:
{
  "permissions": {
    "allow": ["mcp__agent-memory__*"]
  }
}
Use permissionMode: bypassPermissions in agent frontmatter (use with caution)
Restart Claude Code after changing settings
Advanced Features
Learning from Reviews
The agent memory system automatically extracts learnings from review findings. When an agent submits a review with findings, the system:

Analyzes finding severity, categories, and patterns
Stores learnings in the learnings table
Increments times_seen for recurring patterns
Makes learnings available via get_my_learnings() and get_common_issues()
Example: If tdd-qa repeatedly finds "missing edge case tests", agents can query this pattern before writing new tests.

Review Context
Before reviewing a file, agents should call get_review_context() to see:

Past reviews of this file
Known issues in this file
Common findings for this reviewer
Historical outcomes (approved, changes_requested)
This prevents repeating the same feedback and helps maintain consistency.

Coder Context
Before modifying a file, agents should call get_coder_context() to see:

Previous review feedback on this file
Known issues to avoid
Patterns that have caused problems
This helps avoid making mistakes that previous reviews flagged.

Custom Message Streams
You can create custom streams for specialized communication:

nats stream add CUSTOM_STREAM \
  --subjects "custom.*" \
  --storage file \
  --retention limits \
  --max-age 7d
Then publish/subscribe:

await publish_message("CUSTOM_STREAM", "custom.mysubject", "Message", "sender")
messages = await get_messages("CUSTOM_STREAM", "custom.mysubject", 10)
Agent Activity Analytics
Query the activity log for insights:

-- Most active agents
SELECT agent, COUNT(*) as activities
FROM activity_log
GROUP BY agent
ORDER BY activities DESC;

-- Review velocity
SELECT DATE(timestamp) as day, COUNT(*) as reviews
FROM reviews
GROUP BY DATE(timestamp)
ORDER BY day DESC;

-- Common issue categories
SELECT category, COUNT(*) as occurrences
FROM learnings
GROUP BY category
ORDER BY occurrences DESC;
Multi-Project Setup
To run multiple projects with separate agent memories:

Use different NATS ports:

# Project A
nats-server -js -p 4222

# Project B
nats-server -js -p 4223
Use separate databases:

{
  "mcpServers": {
    "agent-memory": {
      "env": {
        "NATS_URL": "nats://localhost:4222",
        "AGENT_MEMORY_DB": "/path/to/projectA/data/agent_memory.db"
      }
    }
  }
}
Or use NATS stream prefixes:

# In agent_memory_core.py
STREAM_PREFIX = os.getenv("STREAM_PREFIX", "")
streams = [f"{STREAM_PREFIX}REQUIREMENTS", f"{STREAM_PREFIX}INTEGRATION", ...]
References
External Documentation
NATS: https://docs.nats.io/
NATS JetStream: https://docs.nats.io/nats-concepts/jetstream
FastMCP: https://github.com/jlowin/fastmcp
Model Context Protocol: https://modelcontextprotocol.io/
Project Files
Agent definitions: .claude/agents/*.md
MCP server: scripts/agent_memory_server.py
Core logic: scripts/agent_memory_core.py
Database: scripts/agent_memory_db.py
Tests: tests/unit/test_agent_memory_*.py
Related Documentation
CLAUDE.md - Project development rules
DEVELOPMENT_PLAN.md - Task breakdown and progress
product-brief-security-assessment-platform.md - Product specifications
Real-World Examples
Example 1: Code Review Flow
Scenario: TDD Coder completes a new feature and requests a review from TDD QA.

# TDD Coder broadcasts status
mcp__agent-memory__broadcast_status(
    agent="tdd-coder",
    status="working",
    current_task="Implementing user authentication",
    progress=100
)

# TDD Coder requests review
mcp__agent-memory__request_review(
    reviewer="tdd-qa",
    item_type="code",
    item_path="src/auth/user_auth.py",
    description="New user authentication module with JWT tokens. Please review test coverage and edge cases.",
    requester="tdd-coder",
    priority="high"
)

# TDD Coder shares result
mcp__agent-memory__share_result(
    result_type="implementation",
    title="User Authentication Module Complete",
    content="Implemented JWT-based authentication with 95% test coverage. All tests passing.",
    sender="tdd-coder",
    tags=["authentication", "security", "jwt"]
)
TDD QA receives the review request:

# TDD QA checks for pending reviews
reviews = mcp__agent-memory__get_pending_reviews("tdd-qa")
# Returns: [{review_id: "review-abc123", item_path: "src/auth/user_auth.py", ...}]

# TDD QA gets context before reviewing
context = mcp__agent-memory__get_review_context(
    reviewer="tdd-qa",
    item_path="src/auth/user_auth.py"
)
# Returns: "No previous reviews for this file. Common issues in similar files:
# - Missing edge case tests for null/empty inputs
# - Weak assertions (assert result vs assert result == expected)"

# TDD QA submits review
mcp__agent-memory__submit_review(
    original_requester="tdd-coder",
    item_path="src/auth/user_auth.py",
    reviewer="tdd-qa",
    status="changes_requested",
    findings=[
        {
            "severity": "high",
            "location": "tests/test_user_auth.py:45",
            "message": "Missing test for expired token scenario",
            "suggestion": "Add test_authenticate_with_expired_token()"
        },
        {
            "severity": "medium",
            "location": "tests/test_user_auth.py:67",
            "message": "Weak assertion: only checks truthiness",
            "suggestion": "Change 'assert result' to 'assert result == expected_user_id'"
        }
    ],
    summary="Good coverage overall (95%), but missing critical security test case for expired tokens. Fix high priority finding before merge."
)
Example 2: DevOps Deployment with QA Verification
Scenario: DevOps deploys to staging and requests QA Engineer to verify.

# DevOps broadcasts deployment start
mcp__agent-memory__broadcast_status(
    agent="devops",
    status="working",
    current_task="Deploying to staging environment",
    progress=0
)

# DevOps shares deployment result
mcp__agent-memory__share_result(
    result_type="deployment",
    title="Staging Deployment Complete",
    content="Deployed release v1.2.0 to staging. All Lambdas updated, no errors in CloudWatch.",
    sender="devops",
    tags=["deployment", "staging", "v1.2.0"]
)

# DevOps requests verification
mcp__agent-memory__request_review(
    reviewer="qa-engineer",
    item_type="deployment",
    item_path="staging/v1.2.0",
    description="Please run integration tests on staging environment to verify deployment",
    requester="devops",
    priority="urgent"
)
QA Engineer verifies the deployment:

# QA Engineer gets pending reviews
reviews = mcp__agent-memory__get_pending_reviews("qa-engineer")

# QA Engineer runs tests and submits verification
mcp__agent-memory__submit_review(
    original_requester="devops",
    item_path="staging/v1.2.0",
    reviewer="qa-engineer",
    status="approved",
    findings=[],
    summary="All integration tests passed. 42/42 tests green. Page load times within acceptable range (<3s). Ready for production."
)

# QA Engineer shares test report
mcp__agent-memory__share_result(
    result_type="test_report",
    title="Staging Integration Tests - v1.2.0",
    content="All 42 tests passed. Coverage: 87%. Browser tests: PASS. Performance: PASS.",
    sender="qa-engineer",
    tags=["testing", "staging", "v1.2.0", "passing"]
)
Example 3: Documentation Workflow
Scenario: Docs Specialist creates documentation, Docs QA verifies accuracy.

# Docs Specialist broadcasts status
mcp__agent-memory__broadcast_status(
    agent="docs-specialist",
    status="working",
    current_task="Creating API documentation for user endpoints",
    progress=50
)

# Docs Specialist completes and requests review
mcp__agent-memory__request_review(
    reviewer="docs-qa",
    item_type="documentation",
    item_path="docs/api/user-endpoints.md",
    description="New API documentation for /users endpoints. Please verify accuracy against actual code.",
    requester="docs-specialist",
    priority="normal"
)
Docs QA verifies the documentation:

# Docs QA gets context (past issues with this file)
context = mcp__agent-memory__get_review_context(
    reviewer="docs-qa",
    item_path="docs/api/user-endpoints.md"
)

# Docs QA submits review after verification
mcp__agent-memory__submit_review(
    original_requester="docs-specialist",
    item_path="docs/api/user-endpoints.md",
    reviewer="docs-qa",
    status="changes_requested",
    findings=[
        {
            "severity": "high",
            "location": "Line 45",
            "message": "Incorrect endpoint path: documented as /api/users but code has /api/v1/users",
            "suggestion": "Update to /api/v1/users"
        },
        {
            "severity": "medium",
            "location": "Line 78",
            "message": "Response example shows 'username' field but actual API returns 'user_name'",
            "suggestion": "Update example to match actual response"
        }
    ],
    summary="Found 2 accuracy issues: incorrect endpoint path and mismatched field name. Fix before publishing."
)
Example 4: Learning from Past Reviews
Scenario: TDD QA reviews similar code and learns from past patterns.

# Before reviewing, TDD QA checks their learnings
learnings = mcp__agent-memory__get_my_learnings(
    agent="tdd-qa",
    category="testing"
)
# Returns: [
#   {
#     "pattern": "Missing edge case tests",
#     "recommendation": "Always test null, empty, and boundary values",
#     "severity": "high",
#     "times_seen": 15
#   },
#   {
#     "pattern": "Weak assertions using truthiness",
#     "recommendation": "Use specific equality checks instead of 'assert result'",
#     "severity": "medium",
#     "times_seen": 23
#   }
# ]

# TDD QA also checks common issues across all reviews
common_issues = mcp__agent-memory__get_common_issues(category="testing")
# Returns most frequent issues found by any reviewer

# TDD QA checks file history
history = mcp__agent-memory__get_file_history("src/auth/user_auth.py")
# Returns: [
#   {
#     "reviewer": "tdd-qa",
#     "outcome": "changes_requested",
#     "summary": "Missing timeout tests",
#     "timestamp": "2025-12-01T10:00:00Z"
#   }
# ]

# Armed with this context, TDD QA can:
# 1. Avoid repeating same feedback
# 2. Check if past issues were fixed
# 3. Apply learnings to new code
Example 5: Cross-Agent Coordination
Scenario: Multiple agents coordinate on a complex feature.

# TDD Coder checks what other agents are doing
statuses = mcp__agent-memory__get_all_agent_statuses()
# Returns: [
#   {"agent": "devops", "state": "working", "current_task": "Updating Lambda configs", "progress": 30},
#   {"agent": "docs-specialist", "state": "idle", "current_task": "", "progress": 0}
# ]

# TDD Coder publishes a coordination message
mcp__agent-memory__publish_message(
    stream="INTEGRATION",
    subject="integration.coordination",
    message="I'm updating the authentication module which will change the /login endpoint signature. Docs will need updating.",
    sender="tdd-coder",
    metadata={"affected_endpoints": ["/login", "/logout"], "breaking_change": True}
)

# Docs Specialist checks for coordination messages
messages = mcp__agent-memory__get_messages(
    stream="INTEGRATION",
    subject="integration.coordination",
    limit=10
)
# Sees the message and responds
mcp__agent-memory__publish_message(
    stream="INTEGRATION",
    subject="integration.coordination",
    message="Acknowledged. I'll update the authentication docs after your changes are merged.",
    sender="docs-specialist",
    metadata={"task_created": "Update auth docs"}
)
Changelog
Version 1.0 (2025-12-07)
Initial documentation
Covers NATS setup, MCP server, agent definitions
Includes porting guide and troubleshooting
Documents learning and memory features
Contributing
When updating this infrastructure:

Update this documentation
Add tests for new features
Update _shared-nats.md if communication protocol changes
Version the database schema if changing SQLite structure
Document breaking changes in changelog
End of Documentation
