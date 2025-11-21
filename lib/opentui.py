#!/usr/bin/env python3
"""
Minimal OpenTui-style helper (curses-backed) for kawaimux.
This is a lightweight shim until the real OpenTui/Jolitui is wired in.
"""
import curses
from typing import List, Callable

class MenuItem:
    def __init__(self, label: str, action: Callable[[], None]):
        self.label = label
        self.action = action

class MenuApp:
    def __init__(self, title: str, items: List[MenuItem]):
        self.title = title
        self.items = items
        self.index = 0

    def run(self):
        curses.wrapper(self._run)

    def _run(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_MAGENTA, -1)
        curses.init_pair(2, curses.COLOR_CYAN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)

        while True:
            stdscr.clear()
            self._render(stdscr)
            ch = stdscr.getch()
            if ch in (curses.KEY_UP, ord('k')):
                self.index = (self.index - 1) % len(self.items)
            elif ch in (curses.KEY_DOWN, ord('j')):
                self.index = (self.index + 1) % len(self.items)
            elif ch in (curses.KEY_ENTER, ord('\n')):
                stdscr.clear()
                stdscr.refresh()
                self.items[self.index].action()
            elif ch in (ord('q'), ord('Q')):
                break

    def _render(self, stdscr):
        h, w = stdscr.getmaxyx()
        title = f"🎀 {self.title} 🎀"
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(1, max(0, (w - len(title)) // 2), title)
        stdscr.attroff(curses.color_pair(1))
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(3, 2, "Hello Kitty mode: choose an action (q to quit)")
        stdscr.attroff(curses.color_pair(2))

        for i, item in enumerate(self.items):
            prefix = "➤ " if i == self.index else "  "
            color = curses.color_pair(3 if i == self.index else 0)
            stdscr.attron(color)
            stdscr.addstr(5 + i, 4, prefix + item.label)
            stdscr.attroff(color)

        stdscr.refresh()
