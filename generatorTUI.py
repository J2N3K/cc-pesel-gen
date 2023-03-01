import curses
from curses.textpad import Textbox, rectangle
import random

menu = ["Credit card generator", "PESEL generator", "About", "Exit"]
exit_menu = ["Yes", "No"]
logo1 = '   _____            __  _____                      __          '
logo2 = '  / ___/__ ________/ / / ___/__ ___  ___ _______ _/ /____  ____'
logo3 = ' / /__/ _ `/ __/ _  / / (_ / -_) _ \/ -_) __/ _ `/ __/ _ \/ __/'
logo4 = ' \___/\_,_/_/  \_,_/  \___/\__/_//_/\__/_/  \_,_/\__/\___/_/   '


def print_menu(stdscr, selected_row_index):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    text = "Use arrow keys to navigate ↑←↓→"
    stdscr.addstr(h//4, w//2 - len(text)//2, text, curses.A_REVERSE)

    for index, row in enumerate(menu):
        if index == selected_row_index:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(h//2 - len(menu)//2 + index, w//2 - len(row)//2, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(h//2 - len(menu)//2 + index, w//2 - len(row)//2, row)
    stdscr.refresh()


def print_credit_card_menu(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    text = "Type in Visa/Mastercard/Mir and press CTRL+G or ENTER"
    stdscr.addstr(h//3, w//2 - len(text)//2, text)
    stdscr.addstr(h//5, w//2 - len(logo1)//2, logo1)
    stdscr.addstr(h//5+1, w//2 - len(logo2)//2, logo2)
    stdscr.addstr(h//5+2, w//2 - len(logo3)//2, logo3)
    stdscr.addstr(h//5+3, w//2 - len(logo4)//2, logo4)
    stdscr.refresh()

    curses.curs_set(1)
    input_window = curses.newwin(1, 15, 2, 2)
    box = Textbox(input_window)
    rectangle(stdscr, 1, 1, 3, 17)
    stdscr.refresh()
    box.edit()
    input_text = box.gather()
    input_text = input_text[:-1]
    curses.curs_set(0)

    issuing_networks = [("Visa", random.randrange(4000, 4999)),
                        ("Mastercard", random.randrange(2221, 2720)),
                        ("Mir", random.randrange(2200, 2204))]
    issuing_networks = dict(issuing_networks)

    try:
        credit_card_number = str(issuing_networks[input_text]) + str(random.randrange(10000000000, 99999999999))
    except KeyError:
        exit()

    def luna_check():
        sum_digits = 0
        for i in range(len(credit_card_number)):
            if i % 2 == 0:
                s = (int(credit_card_number[-1 - i]) * 2)
                if s >= 10:
                    s -= 9
                elif s < 10:
                    s = s
                sum_digits += s
            else:
                sum_digits += (int(credit_card_number[-1 - i]))
        return str((10 - (sum_digits % 10)) % 10)

    cc_w_luna = credit_card_number + luna_check()

    stdscr.addstr(h//2 + 1, w//2 - 20, "Credit card number: " + cc_w_luna)
    stdscr.addstr(h//2 + 2, w//2 - 17, "Expiration date: " + str(random.randint(1, 12)) + "/" + str(random.randint(2024, 2028)))
    stdscr.addstr(h//2 + 3, w//2 - 9, "CVC/CVV: " + str(random.randint(100, 999)))


def print_pesel_menu(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    text = "PESEL generator coming soon..."
    stdscr.addstr(h//2, w//2 - len(text)//2, text)
    stdscr.addstr(0, 0, "Press any key (other than ENTER) to continue")
    stdscr.refresh()


def print_about_menu(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    text = "Credit card and PESEL generator program utilising curses library. For educational purposes only."
    stdscr.addstr(h//2, w//2 - len(text)//2, text)
    stdscr.addstr(0, 0, "Press any key (other than ENTER) to continue")
    stdscr.refresh()


def print_exit_menu(stdscr, selected_column_index):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    text = "Are you sure you want to exit?"
    stdscr.addstr(h//3, w//2 - len(text)//2, text)

    for index, column in enumerate(exit_menu):
        if index == selected_column_index:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(h//2, w//2 - w//20 + w//10*index, column)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(h//2, w//2 - w//20 + w//10*index, column)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)
    selected_row_index = 0
    selected_column_index = 0
    print_menu(stdscr, selected_row_index)

    menu_running = 1
    credit_running = 0
    pesel_running = 0
    about_running = 0
    exit_running = 0
    debug_mode = 0

    while True:
        while menu_running:
            key = stdscr.getch()

            if key == curses.KEY_UP and selected_row_index != 0:
                selected_row_index -= 1
            elif key == curses.KEY_DOWN and selected_row_index != len(menu)-1:
                selected_row_index += 1
            elif key == curses.KEY_ENTER or key in [10,13]:
                if selected_row_index == len(menu)-4:
                    menu_running = 0
                    credit_running = 1
                if selected_row_index == len(menu)-3:
                    menu_running = 0
                    pesel_running = 1
                if selected_row_index == len(menu)-2:
                    menu_running = 0
                    about_running = 1
                if selected_row_index == len(menu)-1:
                    menu_running = 0
                    exit_running = 1
                if debug_mode == 1:
                    stdscr.addstr(0,0,"You pressed {}".format(menu[selected_row_index]))
                    stdscr.refresh()
                    stdscr.getch()

            print_menu(stdscr, selected_row_index)
            stdscr.refresh()

        while credit_running:
            print_credit_card_menu(stdscr)
            stdscr.refresh()
            menu_running = 1
            credit_running = 0

        while pesel_running:
            print_pesel_menu(stdscr)
            stdscr.refresh()
            menu_running = 1
            pesel_running = 0

        while about_running:
            print_about_menu(stdscr)
            stdscr.refresh()
            menu_running = 1
            about_running = 0

        while exit_running:
            print_exit_menu(stdscr, selected_column_index)
            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_RIGHT and selected_column_index != 1:
                selected_column_index += 1
            elif key == curses.KEY_LEFT and selected_column_index != 0:
                selected_column_index -= 1
            elif key == curses.KEY_ENTER or key in [10,13]:
                if selected_column_index == len(exit_menu)-2:
                    exit()
                else:
                    menu_running = 1
                    exit_running = 0


curses.wrapper(main)
