from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class TridanApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(
            text='TRIDAN CONNECTION',
            size_hint=(1, 0.2),
            font_size='28sp'
        )
        
        self.chat = TextInput(
            text='¡Bienvenido a Tridan Connection!\n',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.6)
        )
        
        self.input = TextInput(
            hint_text='Escribe un mensaje...',
            size_hint=(1, 0.1),
            multiline=False
        )
        
        btn = Button(text='Enviar', size_hint=(1, 0.1))
        btn.bind(on_press=self.send)
        
        layout.add_widget(title)
        layout.add_widget(self.chat)
        layout.add_widget(self.input)
        layout.add_widget(btn)
        
        return layout
    
    def send(self, instance):
        msg = self.input.text
        if msg:
            self.chat.text += f'Tú: {msg}\n'
            self.input.text = ''

if __name__ == '__main__':
    TridanApp().run()
