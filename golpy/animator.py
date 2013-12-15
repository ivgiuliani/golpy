import time


def curses_animator(gol, grid_top_left, grid_bottom_right, delay=50):
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
                val = (x, y) in cfg and "#" or " "
                wnd.addch(y, x, val)
        wnd.refresh()

    try:
        for config in gol:
            print_cfg(config)
            time.sleep(delay / 100.0)
    except KeyboardInterrupt:
        curses.endwin()