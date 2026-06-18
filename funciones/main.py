from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation
from kivy.clock import Clock
from controlador import ControladorCalculadora

class PantallaInicio(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(1, 0.92, 0.94, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)
        
        self.logo = Label(
            text="Calculadora del Yavirac",
            font_size=38,
            font_name="Georgia",
            color=(0.85, 0.35, 0.45, 1),
            bold=True,
            halign='center',
            line_height=1.2
        )
        self.add_widget(self.logo)
        self.on_enter = self.iniciar_animacion

    def actualizar_fondo(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def iniciar_animacion(self):
        anim = Animation(font_size=46, duration=0.6) + Animation(font_size=34, duration=0.6)
        anim.repeat = True
        anim.start(self.logo)
        
        Clock.schedule_once(self.cambiar_a_calculadora, 2.5)

    def cambiar_a_calculadora(self, dt):
        self.manager.current = 'calculadora'


class BotonLindo(Button):
    def __init__(self, texto, color_fondo, **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0) 
        self.font_size = 24
        self.font_name = "Georgia"
        self.bold = True
        self.color = (1, 1, 1, 1)
        
        self.color_base = color_fondo
        
        with self.canvas.before:
            self.color_canvas = Color(*self.color_base)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[18])
            
        self.bind(pos=self.actualizar_geometria, size=self.actualizar_geometria)

    def actualizar_geometria(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_state(self, instance, value):
        if value == 'down':
            self.color_canvas.rgba = (self.color_base[0]*0.8, self.color_base[1]*0.8, self.color_base[2]*0.8, 1)
        else:
            self.color_canvas.rgba = self.color_base


class Calculadora(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 12
        
        self.controlador = ControladorCalculadora()
        
        with self.canvas.before:
            Color(1, 0.94, 0.96, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)

        self.pantalla = TextInput(
            text='0',
            font_size=42,
            font_name="Georgia",
            halign='right',
            readonly=True,
            size_hint_y=0.18,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.85, 0.35, 0.45, 1)
        )
        self.add_widget(self.pantalla)

        rejilla = GridLayout(cols=4, spacing=10)
        
        botones = [
            ('7', (1, 0.72, 0.77, 1), 'num', '7'),
            ('8', (1, 0.72, 0.77, 1), 'num', '8'),
            ('9', (1, 0.72, 0.77, 1), 'num', '9'),
            ('+', (0.9, 0.45, 0.55, 1), 'op', '+'),
            
            ('4', (1, 0.72, 0.77, 1), 'num', '4'),
            ('5', (1, 0.72, 0.77, 1), 'num', '5'),
            ('6', (1, 0.72, 0.77, 1), 'num', '6'),
            ('-', (0.9, 0.45, 0.55, 1), 'op', '-'),
            
            ('1', (1, 0.72, 0.77, 1), 'num', '1'),
            ('2', (1, 0.72, 0.77, 1), 'num', '2'),
            ('3', (1, 0.72, 0.77, 1), 'num', '3'),
            ('x', (0.9, 0.45, 0.55, 1), 'op', '*'),
            
            ('C', (0.8, 0.35, 0.4, 1), 'c', 'C'),
            ('0', (1, 0.72, 0.77, 1), 'num', '0'),
            ('=', (0.85, 0.35, 0.45, 1), 'igual', '='),
            ('/', (0.9, 0.45, 0.55, 1), 'op', '/')
        ]

        for texto, color, tipo, valor_logico in botones:
            btn = BotonLindo(texto=texto, color_fondo=color)
            
            if tipo == 'num':
                btn.bind(on_press=lambda instance, v=valor_logico: self.pantalla_num(v))
            elif tipo == 'op':
                btn.bind(on_press=lambda instance, v=valor_logico: self.pantalla_op(v))
            elif tipo == 'c':
                btn.bind(on_press=lambda instance: self.pantalla_c())
            elif tipo == 'igual':
                btn.bind(on_press=lambda instance: self.pantalla_igual())
                
            rejilla.add_widget(btn)

        self.add_widget(rejilla)

    def actualizar_fondo(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def pantalla_num(self, digito):
        self.pantalla.text = self.controlador.presionar_digito(self.pantalla.text, digito)

    def pantalla_op(self, operacion):
        self.pantalla.text = self.controlador.presionar_operacion(self.pantalla.text, operacion)

    def pantalla_c(self):
        self.pantalla.text = self.controlador.presionar_c()

    def pantalla_igual(self):
        self.pantalla.text = self.controlador.presionar_igual(self.pantalla.text)


class PantallaCalculadora(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Calculadora())


class MainApp(App):
    def build(self):
        self.title = "Calculadora del Yavirac"
        sm = ScreenManager()
        sm.add_widget(PantallaInicio(name='inicio'))
        sm.add_widget(PantallaCalculadora(name='calculadora'))
        return sm

if __name__ == '__main__':
    MainApp().run()