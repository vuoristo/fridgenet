import urwid
import requests
import recipe_recommender

recipes = {}

def item_list(title, items):
    text = urwid.Text(title)
    header = urwid.AttrWrap(text, 'streak')
    body = [header, urwid.Divider()]
    for item in items:
        text = "{count}x {name}".format(count=item['count'], name=item['name'])
        text = urwid.Text(text)
        body.append(urwid.AttrMap(text, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def exit_program(button):
    raise urwid.ExitMainLoop()

def fetch_recipes():
    recipe_ids = recipe_recommender.get_recipes_for_items(['tomato'])
    fetched_recipes = [recipe_recommender.get_recipe(id) for id in recipe_ids[0:10]]
    for recipe in fetched_recipes:
        try:
            recipes[recipe['recipe']['title']] = recipe
        except KeyError:
            pass

items = requests.get('https://fridgenet.herokuapp.com/inventory').json()
fetch_recipes()

def parse_items(items):
    data = {}
    for item in items:
        count = data.get(item, 0)
        data[item] = count + 1
    result = []
    for item_name, count in data.items():
        result.append({'name': item_name, 'count': count})
    return result

def on_recipe_selected():
    pass

def right_panel(items):
    header = urwid.AttrWrap(urwid.Text(u"Recipes"), 'streak')
    body = [header, urwid.Divider()]

    for title, recipe in recipes.items():
        button = urwid.Button(title)
        urwid.connect_signal(button, 'click', on_recipe_selected)
        body.append(button)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

items = parse_items(items)
header = urwid.AttrWrap(urwid.Text(u"Fridgenet"), 'banner')

left_panel =  item_list(u'Fridge Contents', items)
right_panel = right_panel(items)

main = urwid.Columns([left_panel, right_panel])
view = urwid.Frame(urwid.AttrWrap(main, 'body'), header=header)

palette = [
    ('banner', '', '', '', 'g50', '#60a'),
    ('streak', '', '', '', '#ffa', '#60d'),
    ('inside', '', '', '', 'g38', '#808'),
    ('outside', '', '', '', 'g27', '#a06'),
    ('bg', '', '', '', 'g7', '#d06')]

top = urwid.Overlay(view, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)

loop = urwid.MainLoop(top, palette=palette)
loop.screen.set_terminal_properties(colors=256)
loop.run()




