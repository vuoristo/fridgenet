extern crate ncurses;

use ncurses::*;
extern crate rustc_serialize;
use rustc_serialize::json::Json;

struct Inventory {

}

impl Inventory {
    fn get_items(&self) -> Vec<&str> {
        // let inventory = "[\"apple\",\"tofu\", \"dog\"]";
        // let data = Json::from_str(inventory).unwrap();
        // let items: Vec<&str> = data.as_array();
        // items;
        vec!["apple", "tofu", "dog"]
    }
}

fn render_menu() {
    let inventory: Inventory = Inventory{};

    start_color();
    cbreak();
    noecho();
    curs_set(CURSOR_VISIBILITY::CURSOR_INVISIBLE);
    keypad(stdscr, true);
    init_pair(1, COLOR_RED, COLOR_BLACK);

    /* Create items */
    let mut items: Vec<ITEM> = Vec::new();
    for item in inventory.get_items() {
        items.push(new_item(item, "1"));
    }
    items.push(new_item("Exit", "Exit description"));

    /* Crate menu */
    let my_menu = new_menu(&mut items);
    menu_opts_off(my_menu, O_SHOWDESC);

    let my_menu_win = newwin(9, 18, 4, 4);
    keypad(my_menu_win, true);

    /* Set main window and sub window */
    set_menu_win(my_menu, my_menu_win);
    set_menu_sub(my_menu, derwin(my_menu_win, 5, 0, 2, 2));

    /* Set menu mark to the string " * " */
    set_menu_mark(my_menu, " * ");

    /* Print a border around the main window */
    box_(my_menu_win, 0, 0);
    mvprintw(LINES - 3, 0, "Press <ENTER> to see the option selected");
    mvprintw(LINES - 2, 0, "F1 to exit");
    refresh();

    /* Post the menu */
    post_menu(my_menu);
    wrefresh(my_menu_win);

    let mut ch = getch();
    while ch != KEY_F(1)
        {
            match ch
                {
                    KEY_UP => {
                        menu_driver(my_menu, REQ_UP_ITEM);
                    },
                    KEY_DOWN => {
                        menu_driver(my_menu, REQ_DOWN_ITEM);
                    },
                    10 => {/* Enter */
                        mv(20, 0);
                        clrtoeol();
                        mvprintw(20, 0, &format!("Item selected is : {}", item_name(current_item(my_menu)))[..]);
                        pos_menu_cursor(my_menu);
                    },
                    _ => {}
                }
            wrefresh(my_menu_win);
            ch = getch();
        }

    unpost_menu(my_menu);

    /* free items */
    for &item in items.iter() {
        free_item(item);
    }

    free_menu(my_menu);

}

fn main()
{
    /* If your locale env is unicode, you should use `setlocale`. */
    let locale_conf = LcCategory::all;
    setlocale(locale_conf, "en_US.UTF-8");

    render_menu();

    /* Start ncurses. */
    initscr();
    /* Terminate ncurses. */
    endwin();
}

