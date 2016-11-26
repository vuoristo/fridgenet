import urwid
import requests

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for choice in choices:
        text = "{count}x {name}".format(count=choice['count'], name=choice['name'])
        button = urwid.Button(text)
        urwid.connect_signal(button, 'click', item_chosen, choice['name'])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()

items = requests.get('https://fridgenet.herokuapp.com/inventory').json()

def parse_items(items):
    data = {}
    for item in items:
        count = data.get(item, 0)
        data[item] = count + 1
    result = []
    for item_name, count in data.items():
        result.append({'name': item_name, 'count': count})
    return result

main = urwid.Padding(menu(u'Fridgenet', parse_items(items)), left=2, right=2)

palette = [
    ('banner', '', '', '', '#ffa', '#60d'),
    ('streak', '', '', '', 'g50', '#60a'),
    ('inside', '', '', '', 'g38', '#808'),
    ('outside', '', '', '', 'g27', '#a06'),
    ('bg', '', '', '', 'g7', '#d06')]

top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)

loop = urwid.MainLoop(top, palette=[('reversed', 'standout', '')])
loop.screen.set_terminal_properties(colors=256)
loop.run()




