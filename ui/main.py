import urwid
import requests
import recipe_recommender

class FridgeNetClient(object):
    def __init__(self):
        self.recipes = {}
        self.items = self.parse_items(requests.get('https://fridgenet.herokuapp.com/inventory').json())
        self.fetch_recipes()
        self.selected_recipe = None

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
        if len(self.items) > 0:
            recipe_ids = recipe_recommender.get_recipes_for_items(self.items[-1])
        else:
            recipe_ids = recipe_recommender.get_recipes_for_items('tomato')
        fetched_recipes = [recipe_recommender.get_recipe(id) for id in recipe_ids[0:10]]
        for recipe in fetched_recipes:
            try:
                self.recipes[recipe['recipe']['title']] = recipe
            except KeyError:
                pass

    def parse_items(self, items):
        data = {}
        for item in items:
            count = data.get(item, 0)
            data[item] = count + 1
        result = []
        for item_name, count in data.items():
            result.append({'name': item_name, 'count': count})
        return result

    def on_recipe_selected(self, button, recipe_data):
        self.selected_recipe = recipe_data['recipe']
        self.rerender()

    def recipe_list(self):
        header = urwid.AttrWrap(urwid.Text(u"Recipes"), 'streak')
        body = [header, urwid.Divider()]

        for title, recipe in self.recipes.items():
            button = urwid.Button(title)
            urwid.connect_signal(button, 'click', self.on_recipe_selected, recipe)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def close_recipe(self, button):
        self.selected_recipe = None
        self.rerender()

    def recipe_single_view(self):
        header = urwid.AttrMap(urwid.Text(self.selected_recipe['title']), 'streak')
        button = urwid.Button("Back")
        urwid.connect_signal(button, "click", self.close_recipe)
        body = [
                header,
                urwid.Divider(),
                urwid.Text("\n".join(self.selected_recipe['ingredients'])),
                button
                ]
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def render(self):
        header = urwid.AttrWrap(urwid.Text(u"Fridgenet"), 'banner')

        left_panel =  self.item_list(u'Fridge Contents')
        if self.selected_recipe is None:
            right_panel = self.recipe_list()
        else:
            right_panel = self.recipe_single_view()

        main = urwid.Columns([left_panel, right_panel])
        main.focus_position = 1
        frame = urwid.Frame(urwid.AttrWrap(main, 'body'), header=header)
        view = urwid.Overlay(frame, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
        return view

    def run(self):
        palette = [
            ('banner', '', '', '', 'g50', '#60a'),
            ('streak', '', '', '', '#ffa', '#60d'),
            ('inside', '', '', '', 'g38', '#808'),
            ('outside', '', '', '', 'g27', '#a06'),
            ('bg', '', '', '', 'g7', '#d06')]

        self.loop = urwid.MainLoop(self.render(), palette=palette)
        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.run()

    def rerender(self):
        self.loop.widget = self.render()


if __name__ == "__main__":
    FridgeNetClient().run()


