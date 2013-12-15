import time

from golpy.gol import translate_cfg


def curses_animator(gol, delay=50, alive_char="*"):
    """
    Animate the given configurations on the screen.
    """
    # import curses here to allow any other animator to work even if the curses
    # module is not installed
    import curses

    wnd = curses.initscr()
    wnd.nodelay(True)
    curses.cbreak()
    curses.noecho()
    wnd.keypad(1)

    translation_x, translation_y = 0, 0

    # drop 5 rows/cols of padding
    start_x, start_y = wnd.getyx()[1], wnd.getyx()[0]
    stop_x, stop_y = wnd.getmaxyx()[1] - 5, wnd.getmaxyx()[0] - 5

    def print_cfg(cfg):
        for y in range(start_y, stop_y + 1):
            for x in range(start_x, stop_x + 1):
                val = (x, y) in cfg and alive_char or " "
                wnd.addch(y, x, val)

    def print_iteration(it):
        iteration = str(it)
        wnd.addstr(0, stop_x - len(iteration), iteration)

    try:
        for config in gol:
            print_cfg(translate_cfg(config, translation_x, translation_y))
            print_iteration(gol.iteration)
            wnd.refresh()

            key = wnd.getch()
            if key:
                if key == curses.KEY_UP:
                    translation_y -= 1
                elif key == curses.KEY_DOWN:
                    translation_y += 1
                elif key == curses.KEY_LEFT:
                    translation_x -= 1
                elif key == curses.KEY_RIGHT:
                    translation_x += 1

            time.sleep(delay / 100.0)
    except KeyboardInterrupt:
        curses.nocbreak()
        wnd.keypad(0)
        curses.endwin()