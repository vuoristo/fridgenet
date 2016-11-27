import urwid
import requests
import recipe_recommender

class FridgeNetClient(object):
    def __init__(self):
        self.recipes = {}
        self.items = requests.get('https://fridgenet.herokuapp.com/inventory').json()
        self.fetch_recipes()

    def item_list(self, title):
        text = urwid.Text(title)
        header = urwid.AttrWrap(text, 'streak')
        body = [header, urwid.Divider()]
        for item in self.items:
            text = "{count}x {name}".format(count=item['count'], name=item['name'])
            text = urwid.Text(text)
            body.append(urwid.AttrMap(text, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def fetch_recipes(self):
        recipe_ids = recipe_recommender.get_recipes_for_items(['tomato'])
        fetched_recipes = [recipe_recommender.get_recipe(id) for id in recipe_ids[0:10]]
        for recipe in fetched_recipes:
            try:
                self.recipes[recipe['recipe']['title']] = recipe
            except KeyError:
                pass

    def parse_items(self):
        data = {}
        for item in self.items:
            count = data.get(item, 0)
            data[item] = count + 1
        result = []
        for item_name, count in data.items():
            result.append({'name': item_name, 'count': count})
        return result

    def on_recipe_selected(self, recipe_data):
        pass

    def right_panel(self, items):
        header = urwid.AttrWrap(urwid.Text(u"Recipes"), 'streak')
        body = [header, urwid.Divider()]

        for title, recipe in self.recipes.items():
            button = urwid.Button(title)
            urwid.connect_signal(button, 'click', self.on_recipe_selected, recipe)
            body.append(button)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def run(self):
        items = self.parse_items()
        header = urwid.AttrWrap(urwid.Text(u"Fridgenet"), 'banner')

        left_panel =  self.item_list(u'Fridge Contents')
        right_panel = self.right_panel(items)

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


if __name__ == "__main__":
    FridgeNetClient().run()


