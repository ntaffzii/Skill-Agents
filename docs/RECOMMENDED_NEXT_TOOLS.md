# Recommended Next Tools

This document lists tool ideas found from MCP community patterns and how they compare to the current repo.

## Already Covered

- Filesystem and file inspection
- Git read-only operations
- Controlled Git branch/stage/commit operations
- Tool registry and toolsets
- Audit and policy inspection
- Project/docs/package/config/API/database/test inspection
- Dependency risk inspection
- Browser readiness and Playwright page inspection
- Backup snapshots
- Memory
- Prompt improvement
- Web/media/system helpers
- MCP security audit
- Repository security scanner
- Typed memory context and context pack generation
- Basic Playwright actions
- CI inspection
- GitHub API read tools
- Playwright accessibility snapshots
- Dockerfile and Compose inspection
- Lightweight repository indexing
- Persistent Playwright sessions
- Provider-neutral public web capture
- Finance market data and research tools
- External MCP catalog discovery
- Browser page mapping
- Lightweight vector memory
- Read-only Postgres query support
- Figma design inspection
- Notion workspace integration
- Slack/Discord workspace summaries
- Obsidian-Notion bridge planning
- Calendar and meeting-prep planning
- Email inbox summarization and reply drafting
- Issue tracker planning for GitHub/Linear/Jira-style work
- Provider-neutral RAG planning and chunking

## Recently Added High-Value Tools

### `ci.py`

Purpose: inspect CI systems deeply.

Suggested tools:

- `find_ci_files` - done
- `inspect_github_actions_jobs` - done
- `list_ci_validation_commands` - done
- `summarize_ci_surface` - done

Why: the repo already has GitHub workflow discovery, validation, and release tools. CI is the missing bridge.

### `github_api.py`

Purpose: inspect GitHub issues, PRs, files, and checks through API when a token is available.

Suggested tools:

- `check_github_api_auth` - done
- `get_repo_info` - done
- `get_issue` - done
- `get_pull_request` - done
- `list_pr_files` - done
- `get_pr_checks` - done
- `draft_pr_review` - done

Why: current `github.py` is local-only. API support would make real PR review workflows stronger.

### `playwright_actions.py`

Purpose: interact with pages, not only inspect them.

Suggested tools:

- `playwright_click` - done
- `playwright_fill` - done
- `playwright_assert_visible_text` - done
- `playwright_get_console_errors` - done
- `playwright_get_network_failures` - done
- `playwright_accessibility_snapshot` - done
- persistent browser sessions - done

Why: current `playwright-actions` supports basic interaction. The next layer is accessibility snapshots and persistent sessions.

### `docker.py`

Purpose: inspect Docker and Compose projects safely.

Suggested tools:

- `check_docker_available` - done
- `find_docker_files` - done
- `inspect_dockerfile` - done
- `inspect_docker_compose` - done
- `plan_docker_validation` - done

Why: many modern repos use Docker for local services. Start read-only before exposing runtime commands.

### `repo_index.py`

Purpose: create a searchable local project index for large repositories.

Suggested tools:

- `build_repo_index` - done
- `search_repo_index` - done
- `find_related_files` - done
- `summarize_index` - done

Why: as repos grow, repeated file scanning becomes noisy. A local index makes agents faster and more consistent.

### Persistent Playwright sessions

Purpose: keep browser state across related UI checks.

Suggested tools:

- `playwright_start_session` - done
- `playwright_use_session` - done
- `playwright_close_session` - done
- `playwright_list_sessions` - done

Why: repeated login/setup flows are expensive. Persistent sessions should come after read-only and single-shot UI tooling is stable.

## Recently Added Workspace And Agent Tools

### `vector_memory.py`

Purpose: make long-running project memory easier to search semantically.

Suggested tools:

- `build_vector_memory_index` - done
- `search_vector_memory` - done
- `find_related_memories` - done
- `summarize_memory_clusters` - done

### `external_mcp_catalog.py`

Purpose: track useful open-source MCP tools without manually searching each time.

Suggested tools:

- `list_mcp_catalog_sources` - done
- `search_mcp_catalogs` - done
- `summarize_mcp_repo` - done
- `compare_mcp_tool_patterns` - done
- `draft_local_tool_adaptation` - done

### `browser_page_map.py`

Purpose: make browser/HTML pages easier for agents to inspect without relying only on screenshots.

Suggested tools:

- `capture_page_map_from_html` - done
- `summarize_page_structure` - done
- `list_interactive_elements` - done
- `find_element_by_label` - done

### `postgres.py`

Purpose: support private data research without allowing destructive SQL.

Suggested tools:

- `check_postgres_config` - done
- `explain_sql_risk` - done
- `plan_readonly_query` - done
- `run_readonly_sql` - done
- `inspect_query_result` - done

### `figma.py`

Purpose: connect design context to frontend implementation.

Suggested tools:

- `check_figma_auth` - done
- `plan_figma_inspection` - done
- `get_figma_file_summary` - done
- `extract_design_tokens` - done
- `inspect_components` - done
- `draft_frontend_implementation_plan` - done

### `notion.py`

Purpose: connect personal/team notes with agent research and handoffs.

Suggested tools:

- `check_notion_auth` - done
- `search_notion_pages` - done
- `read_notion_page` - done
- `create_notion_note_plan` - done
- `append_notion_block_plan` - done

### `slack_discord.py`

Purpose: summarize workspace messages and extract follow-up work without hiding send actions.

Suggested tools:

- `check_chat_integrations` - done
- `search_slack_messages` - done
- `summarize_channel_messages` - done
- `draft_chat_reply` - done
- `extract_action_items` - done

### `obsidian_notion_bridge.py`

Purpose: move personal knowledge between Obsidian and Notion without silent overwrites.

Suggested tools:

- `inspect_obsidian_note_for_notion` - done
- `plan_obsidian_to_notion` - done
- `plan_notion_to_obsidian` - done
- `create_knowledge_sync_checklist` - done

### `calendar.py`

Purpose: make the personal agent useful for daily planning and meeting prep.

Suggested tools:

- `check_calendar_config` - done
- `summarize_calendar_events` - done
- `build_daily_plan` - done
- `draft_meeting_prep` - done
- `extract_calendar_followups` - done

### `email_inbox.py`

Purpose: summarize inbox context and draft replies without sending.

Suggested tools:

- `check_email_config` - done
- `plan_email_search` - done
- `summarize_email_messages` - done
- `extract_email_action_items` - done
- `draft_email_reply` - done

### `issue_tracker.py`

Purpose: turn personal notes, messages, and requirements into issue/task plans.

Suggested tools:

- `check_issue_tracker_config` - done
- `parse_issue_reference` - done
- `draft_issue_from_context` - done
- `break_down_issue` - done
- `plan_issue_update` - done

### `rag_adapter.py`

Purpose: prepare selected notes, docs, and memories for local or provider-backed RAG.

Suggested tools:

- `list_rag_providers` - done
- `check_rag_config` - done
- `chunk_text_for_rag` - done
- `plan_rag_index` - done
- `build_embedding_request_plan` - done

## Lower Priority Ideas

- Live `jira.py` or `linear.py` API readers - optional when issue tracking becomes daily.
- Live Gmail/Google Calendar readers - optional when you want direct provider pull instead of supplied exports.
- `cloud.py` - AWS/GCP/Azure inspection.
- `kubernetes.py` - cluster and manifest inspection.
- Calendar provider API adapter - optional direct Google/Outlook reads.
- Email provider API adapter - optional direct Gmail/Outlook/IMAP reads.

## Decision Rule

Add a new tool only when:

1. The action repeats often.
2. Code can do it more reliably than prompt instructions.
3. Inputs and outputs can be structured.
4. Safety policy is clear.
5. It fits an existing workflow or toolset.
