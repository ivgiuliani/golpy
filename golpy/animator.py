import time


def curses_animator(gol, grid_top_left, grid_bottom_right, delay=50, alive_char="*"):
    """
    Animate the given configurations on the screen.
    """
    # import curses here to allow any other animator to work even if the curses
    # module is not installed
    import curses

    wnd = curses.initscr()

    def print_cfg(cfg):
        start_x, start_y = grid_top_left
        stop_x, stop_y = grid_bottom_right
        for y in range(start_y, stop_y + 1):
            for x in range(start_x, stop_x + 1):
                val = (x, y) in cfg and alive_char or " "
                wnd.addch(y, x, val)

    def print_iteration(it):
        max_w = grid_bottom_right[0]
        iteration = str(it)
        wnd.addstr(0, max_w - len(iteration), iteration)

    try:
        for config in gol:
            print_cfg(config)
            print_iteration(gol.iteration)
            wnd.refresh()

            time.sleep(delay / 100.0)
    except KeyboardInterrupt:
        curses.endwin()