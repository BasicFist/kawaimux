#!/usr/bin/env python3
"""
Kawaimux - Hello Kitty TUI (OpenTui shim)
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'lib'))

from lib.opentui import MenuApp, MenuItem
from lib.workflow_templates import KawaiiWorkflowTemplates
from lib.utils import validate_kawaii_environment, check_system_compatibility

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKDIR = Path.home() / 'LAB'
SESSION = 'tmuxai_dev'


def p(msg: str):
    print(msg)


def action_health():
    valid, issues = validate_kawaii_environment()
    if valid:
        p("✅ Environment OK — kawaii level MAXIMUM!")
    else:
        p("❌ Environment issues:")
        for i in issues:
            p(f"  • {i}")
    input("Press Enter...")


def action_list_templates():
    wt = KawaiiWorkflowTemplates()
    p("Available templates:\n")
    for t in wt.templates.values():
        p(f"- {t.name} [{t.id}] — {t.description[:80]}...")
    input("Press Enter...")


def action_show_template():
    wt = KawaiiWorkflowTemplates()
    p("Enter template id (default: academic_writing_sprint): ")
    tid = input().strip() or 'academic_writing_sprint'
    t = wt.get_template(tid)
    if not t:
        p("Template not found")
    else:
        p(f"\n{t.name}\n{'-'*len(t.name)}")
        p(t.description)
        p(f"Required agents: {t.required_agents}, est. hours: {t.estimated_duration_hours}")
        p("Steps:")
        for s in t.steps:
            p(f" • {s.name}: {s.description}")
            p(f"   Prompt: {s.ai_prompt}")
    input("Press Enter...")


def action_launch_pairai():
    # basic tmux pairing: session + ai window with two panes running tmuxai
    env = os.environ.copy()
    model = env.get('TMUXAI_MODEL', '')
    key = env.get('TMUXAI_API_KEY', '')
    base_cmd = ['tmux', 'new-session', '-As', SESSION, '-c', str(WORKDIR)]
    subprocess.run(base_cmd)
    # ensure ai window
    subprocess.run(['tmux', 'new-window', '-t', SESSION, '-n', 'ai', '-c', str(WORKDIR)])
    launch = f"TMUXAI_MODEL='{model}' TMUXAI_API_KEY='{key}' tmuxai || exec zsh"
    subprocess.run(['tmux', 'send-keys', '-t', f'{SESSION}:ai.0', launch, 'C-m'])
    subprocess.run(['tmux', 'split-window', '-h', '-t', f'{SESSION}:ai', '-c', str(WORKDIR)])
    subprocess.run(['tmux', 'send-keys', '-t', f'{SESSION}:ai.1', launch, 'C-m'])
    subprocess.run(['tmux', 'select-window', '-t', f'{SESSION}:ai'])
    p("Attached to tmux session. Use 'tmux attach -t tmuxai_dev' if needed.")
    input("Press Enter...")


def action_tmux_status():
    checks = check_system_compatibility()
    for k, v in checks.items():
        p(f"{k}: {'✅' if v else '❌'}")
    input("Press Enter...")


def main():
    menu = MenuApp(
        title="Hello Kitty Kawaimux",
        items=[
            MenuItem("Health Check", action_health),
            MenuItem("List Templates", action_list_templates),
            MenuItem("Show Template Details", action_show_template),
            MenuItem("Launch PairAI (tmux + tmuxai x2)", action_launch_pairai),
            MenuItem("Tmux/Env Status", action_tmux_status),
            MenuItem("Quit", lambda: exit(0)),
        ]
    )
    menu.run()


if __name__ == "__main__":
    import sys
    if not sys.stdout.isatty():
        print('This TUI requires a TTY. Please run in a terminal.')
        sys.exit(1)
    main()
