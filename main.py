from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

# Solo importar en Android
if 'android' in str(platform):
    from jnius import autoclass
    from android.permissions import request_permissions, Permission, check_permission
    from android.permissions import PermissionStatus

class SplashScreen(FloatLayout):
    """Pantalla de splash con logo completo"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Fondo negro
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Logo centrado
        self.logo = Image(
            source='tridan_logo_full.png',
            size_hint=(None, None),
            size=(400, 400),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0
        )
        self.add_widget(self.logo)
        
        # Fade in
        anim_in = Animation(opacity=1, duration=1.5)
        anim_in.start(self.logo)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class TridanApp(App):
    def build(self):
        self.splash = SplashScreen()
        Clock.schedule_once(self.show_main_screen, 3)  # 3 segundos de splash
        return self.splash
    
    def show_main_screen(self, dt):
        """Transición suave del splash a la pantalla principal"""
        # Fade out del splash
        anim_out = Animation(opacity=0, duration=0.5)
        anim_out.bind(on_complete=lambda *_: self.root.clear_widgets())
        anim_out.start(self.splash)
        
        # Agregar main después del fade
        Clock.schedule_once(self._add_main_layout, 0.6)
    
    def _add_main_layout(self, dt):
        self.root.clear_widgets()
        main_layout = self.create_main_layout()
        self.root.add_widget(main_layout)
        
        # Solicitar permisos poco después de mostrar la interfaz
        Clock.schedule_once(self.request_permissions, 1.0)
    
    def create_main_layout(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Header con logo pequeño + título (fondo sutil)
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10, padding=10)
        with header.canvas.before:
            Color(0.05, 0.2, 0.4, 0.9)  # Azul oscuro semitransparente
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header_bg, pos=self._update_header_bg)
        
        logo_small = Image(
            source='tridan_logo_icon.png',
            size_hint=(None, 1),
            width=50,
            allow_stretch=True,
            keep_ratio=True
        )
        
        title = Label(
            text='TRIDAN CONNECTION',
            font_size='24sp',
            bold=True,
            color=(1, 0.84, 0, 1),  # Dorado
            size_hint=(1, 1),
            halign='left',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        
        header.add_widget(logo_small)
        header.add_widget(title)
        layout.add_widget(header)
        
        # Área de chat (con scroll automático)
        self.chat = TextInput(
            text='¡Bienvenido a Tridan Connection! 🌳\nChat offline vía Bluetooth mesh en desarrollo.\n\n',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.55),
            background_color=(0.03, 0.12, 0.25, 1),
            foreground_color=(0.9, 0.9, 0.9, 1)
        )
        layout.add_widget(self.chat)
        
        # Botón buscar Bluetooth
        self.btn_buscar = Button(
            text='🔵 Buscar dispositivos Bluetooth',
            size_hint=(1, 0.08),
            background_color=(0.05, 0.4, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        self.btn_buscar.bind(on_press=self.buscar_bluetooth)
        layout.add_widget(self.btn_buscar)
        
        # Input de mensaje
        self.input = TextInput(
            hint_text='Escribe un mensaje...',
            size_hint=(1, 0.08),
            multiline=False,
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1)
        )
        layout.add_widget(self.input)
        
        # Botón enviar
        btn_enviar = Button(
            text='📤 Enviar',
            size_hint=(1, 0.08),
            background_color=(1, 0.84, 0, 1),
            color=(0, 0, 0, 1)
        )
        btn_enviar.bind(on_press=self.send)
        layout.add_widget(btn_enviar)
        
        # Versión abajo
        version = Label(
            text='v1.1 - Prueba offline Bluetooth',
            size_hint=(1, 0.05),
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(version)
        
        return layout
    
    def _update_header_bg(self, instance, value):
        self.header_bg.size = instance.size
        self.header_bg.pos = instance.pos
    
    def log(self, mensaje):
        """Agregar línea al chat y auto-scroll"""
        self.chat.text += f'{mensaje}\n'
        # Mejor scroll: forzar al final
        Clock.schedule_once(lambda dt: setattr(self.chat, 'cursor', (0, len(self.chat.text.splitlines()))), 0.1)
    
    def request_permissions(self, dt):
        """Solicitar permisos Bluetooth/ubicación en Android"""
        try:
            from android.permissions import request_permissions, Permission, check_permission
            
            self.log('📋 Verificando permisos...')
            
            permisos = [
                Permission.BLUETOOTH,
                Permission.BLUETOOTH_ADMIN,
                Permission.BLUETOOTH_SCAN,
                Permission.BLUETOOTH_CONNECT,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ]
            
            faltantes = [p for p in permisos if not check_permission(p)]
            
            if faltantes:
                self.log(f'📋 Solicitando {len(faltantes)} permisos...')
                request_permissions(permisos, self.permission_callback)
                self.log('✅ Permisos solicitados. Por favor acepta el diálogo.')
            else:
                self.log('✅ Todos los permisos ya están concedidos')
                self.log('Puedes usar Bluetooth ahora.')
                
        except ImportError:
            self.log('⚠️ No es Android → permisos no solicitados')
        except Exception as e:
            self.log(f'⚠️ Error al solicitar permisos: {str(e)}')
    
    def permission_callback(self, permissions, grant_results):
        """Callback después de respuesta del usuario"""
        concedidos = sum(grant_results)
        total = len(grant_results)
        self.log(f'📊 Permisos concedidos: {concedidos}/{total}')
        
        if concedidos == total:
            self.log('🎉 ¡Permisos completos! Listo para Bluetooth mesh.')
            # Aquí podrías activar funciones BLE
        else:
            self.log('⚠️ Algunos permisos denegados. Ve a Ajustes → Permisos para permitirlos manualmente.')
    
    def buscar_bluetooth(self, instance):
        """Buscar dispositivos Bluetooth emparejados (versión simple)"""
        self.log('\n🔍 Iniciando búsqueda de dispositivos...')
        self.btn_buscar.text = 'Buscando...'  # Feedback visual
        self.btn_buscar.disabled = True
        
        try:
            adapter = autoclass('android.bluetooth.BluetoothAdapter').getDefaultAdapter()
            
            if not adapter:
                self.log('❌ No se detectó adaptador Bluetooth')
                self._reset_buscar_btn()
                return
            
            if not adapter.isEnabled():
                self.log('⚠️ Bluetooth está apagado. Actívalo en ajustes.')
                self._reset_buscar_btn()
                return
            
            self.log('✅ Bluetooth activo')
            
            paired = adapter.getBondedDevices().toArray()
            
            if not paired:
                self.log('📴 No hay dispositivos emparejados aún.')
            else:
                self.log(f'📱 {len(paired)} dispositivos emparejados encontrados:')
                self.log('─' * 40)
                for dev in paired:
                    name = dev.getName() or '(sin nombre)'
                    addr = dev.getAddress()
                    self.log(f'• {name}')
                    self.log(f'  MAC: {addr}')
                self.log('─' * 40)
            
        except Exception as e:
            self.log(f'❌ Error al buscar: {str(e)}')
        
        self._reset_buscar_btn()
    
    def _reset_buscar_btn(self):
        self.btn_buscar.text = '🔵 Buscar dispositivos Bluetooth'
        self.btn_buscar.disabled = False
    
    def send(self, instance):
        msg = self.input.text.strip()
        if msg:
            self.chat.text += f'Tú: {msg}\n'
            self.input.text = ''
            Clock.schedule_once(lambda dt: setattr(self.chat, 'cursor', (0, len(self.chat.text.splitlines()))), 0.1)

if __name__ == '__main__':
    TridanApp().run()
