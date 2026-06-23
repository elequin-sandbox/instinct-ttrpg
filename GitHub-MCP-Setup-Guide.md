# GitHub MCP Setup Guide for Claude Cowork
*Based on your earlier session — everything you need in one place.*

---

## What we're doing and why

You want Claude to be able to push `index.html` directly to your GitHub repo (`Nathan-Elequin/act-tactics`) so deploys are one command instead of a manual file upload. That requires wiring up the **GitHub MCP server**, which runs locally on your computer via Docker.

**Key thing to understand:** This is a *local* MCP server, not a remote one. Baserow has a "Connect" button in the Claude UI — GitHub via Docker does NOT. Editing the config file and restarting Claude *is* the entire setup. There's no extra button to click.

---

## Before you start

Make sure you have:
- ✅ **Docker Desktop** installed, open, and showing "Engine running" in green (bottom-left of the Docker window, or check the whale icon in your system tray)
- ✅ **A GitHub fine-grained personal access token** — see Step 0 below if you don't have one yet

---

## Step 0 — Get your GitHub token

1. Go to [github.com](https://github.com) and make sure you're logged in as Nathan-Elequin
2. Click your **profile photo** (top-right corner) → **Settings**
3. Scroll all the way down the left sidebar → click **Developer settings** (very bottom)
4. In the left sidebar → **Personal access tokens** → **Fine-grained tokens**
5. Click **Generate new token** (top-right)
6. Fill in the form:
   - **Token name:** `Claude Cowork - act-tactics` (or anything descriptive)
   - **Expiration:** 90 days or No expiration (your call — no expiration means you never have to redo this)
   - **Resource owner:** Nathan-Elequin
   - **Repository access:** select **Only select repositories** → choose `Nathan-Elequin/act-tactics`
7. Under **Permissions**, find **Repository permissions** → scroll to **Contents** → set it to **Read and write**
8. Click **Generate token** at the bottom
9. **Copy the token immediately** — GitHub only shows it once. It starts with `github_pat_`. Paste it somewhere safe (like a note) until you add it to the config file.

⚠️ If you close the page without copying it, you'll need to delete it and generate a new one.

---

## Step 1 — Open your config file

The file is at:
```
C:\Users\Natha\AppData\Roaming\Claude\claude_desktop_config.json
```

Open it in any text editor (Notepad works fine).

---

## Step 2 — Add the `mcpServers` block

You **don't need to replace anything** — just add one block at the end. Find the very last two lines of the file, which currently look like this:

```json
  }
}
```

Replace those two lines with this (it adds a comma after the closing `preferences` brace, then appends the new block):

```json
  },
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "PASTE_YOUR_GITHUB_PAT_HERE"
      }
    }
  }
}
```

Replace `PASTE_YOUR_GITHUB_PAT_HERE` with your real token (keep the quotes). **Do not paste your token in chat — only in this file.**

Your complete file should now end like this:

```json
      ...
      "epitaxy-perm-mode-acks.39bfeaf3-1023-4688-b031-b30adfeb20ee": [
        "C:\\Users\\Natha\\Claude\\Projects\\Instinct RPG - Design Cowork Project:auto"
      ]
    }
  },
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

Save the file.

---

## Step 3 — Fully quit Claude (important!)

Closing the window is NOT enough — Claude hides in the system tray. You must fully quit it:

1. Find the **Claude icon in your system tray** (bottom-right, near the clock)
2. **Right-click** it → **Quit**

Then reopen Claude normally.

---

## Step 4 — Start a brand-new chat

The GitHub tools only load in chats that start *after* the config was set. Any chat that was open before the restart won't see them.

In your new chat, say:
> "Check that you can see my repo Nathan-Elequin/act-tactics."

Claude will list the repo to confirm the connection is live. The very first call may take a few extra seconds while Docker pulls the GitHub server image — that's normal, and it only happens once.

---

## Troubleshooting

**GitHub tools aren't showing up in the new chat**
- Most likely cause: Docker isn't running. Check the whale icon in the system tray — it should be steady (not animated), and Docker Desktop should say "Engine running" in green.
- Second most likely: a JSON error in the config. Open the file and look for a missing comma or mismatched brace. Paste it in chat (with token blanked as `github_pat_REDACTED`) and ask Claude to validate it.
- Make sure you fully quit Claude via the system tray, not just closed the window.

**"Engine running" shows but still not working**
- Try quitting Docker Desktop completely and relaunching it, then quit/reopen Claude again.

---

## Every time you want to deploy

Once set up, the recipe for any future session is:

1. Open **Docker Desktop** (just needs to be running in the background)
2. Start a **new Cowork task inside the Instinct RPG Project**
3. Say: *"Read HANDOFF-read-me-first.md and continue the deploy"*

Claude will confirm it can see the repo and push `index.html` for you. If Docker ever isn't running, the fallback is always the [manual GitHub upload](https://github.com/Nathan-Elequin/act-tactics) (drag file → commit → done in 2 min).
