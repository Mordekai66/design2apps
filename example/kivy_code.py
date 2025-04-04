from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput


image_ref = []

Window.size = (594,423)
Window.clearcolor = (0.08235294371843338, 0.0235294122248888, 0.0235294122248888)

class Kivy_app(App):
    def build(self):

        layout = FloatLayout()

        label = Label(
        text = 'python test',
        font_name = 'Arial',
        font_size = 12,
        size_hint = (None, None),
        pos_hint = {'x': 0.005050505050505051, 'y': 0.8865248226950355},
        halign="left",  
        valign="top"
        )

        layout.add_widget(label)


        entry = TextInput(
        hint_text="Enter text here",
        pos_hint={'x': 0.04040404040404041, 'y': 1 - (137 / 423)},
        size_hint=(0.9074074074074074, 0.13711583924349882),
        background_color=(0.8509804010391235, 0.8509804010391235, 0.8509804010391235, 1),
        font_size=14)

        layout.add_widget(entry)



        img = Image(
        source=r'D:/build/image/43.png',
        pos_hint={'x': 0.4057239057239057, 'y': 0.43262411347517726},
        size_hint=(87 / 594, 84 / 423))

        layout.add_widget(img)



        btn = Button(
        text='Button',
        size_hint=(113 / 594, 21 / 423),
        pos_hint={'x': 39 / 594, 'y': 1 - (326 / 423)}
        )
        layout.add_widget(btn)


        btn = Button(
        text='ahmed',
        size_hint=(113 / 594, 21 / 423),
        pos_hint={'x': 39 / 594, 'y': 1 - (326 / 423)}
        )
        layout.add_widget(btn)


        with layout.canvas:
            Color(0.8509804010391235,0.8509804010391235,0.8509804010391235)
            Ellipse(pos=(429, 70),
            size=(102, 39))
    

        return layout

Kivy_app().run()