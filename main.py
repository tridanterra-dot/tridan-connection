from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle

class SplashScreen(FloatLayout):
    """Pantalla de inicio con logo"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Fondo negro
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Logo con texto
        self.logo = Image(
            source='tridan_logo_full.png',
            size_hint=(None, None),
            size=(400, 400),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0
        )
        self.add_widget(self.logo)
        
        # Animación fade in
        anim = Animation(opacity=1, duration=1.5)
        anim.start(self.logo)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class TridanApp(App):
    def build(self):
        # Mostrar splash screen primero
        self.splash = SplashScreen()
        Clock.schedule_once(self.show_main_screen, 3)  # 3 segundos
        return self.splash
    
    def show_main_screen(self, dt):
        """Cambiar a la pantalla principal"""
        self.root.clear_widgets()
        main_layout = self.create_main_layout()
        self.root.add_widget(main_layout)
        
        # Solicitar permisos
        Clock.schedule_once(self.request_permissions, 0.5)
    
    def create_main_layout(self):
        """Crear interfaz principal"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Header con logo pequeño
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        
        logo_small = Image(
            source='tridan_logo_icon.png',
            size_hint=(None, 1),
            width=60,
            allow_stretch=True
        )
        
        title = Label(
            text='TRIDAN CONNECTION',
            font_size='20sp',
            bold=True,
            size_hint=(1, 1),
            halign='left',
            valign='middle',
            color=(1, 0.84, 0, 1)  # Dorado
        )
        title.bind(size=title.setter('text_size'))
        
        header.add_widget(logo_small)
        header.add_widget(title)
        
        # Área de chat/log
        self.chat = TextInput(
            text='¡Bienvenido a Tridan Connection! 🌳\n',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.5),
            background_color=(0.05, 0.15, 0.3, 1)  # Azul oscuro Tridan
        )
        
        # Botón buscar Bluetooth
        btn_buscar = Button(
            text='🔵 Buscar dispositivos Bluetooth',
            size_hint=(1, 0.1),
            background_color=(0.05, 0.4, 0.7, 1),  # Azul Tridan
            color=(1, 1, 1, 1)
        )
        btn_buscar.bind(on_press=self.buscar_bluetooth)
        
        # Input de mensaje
        self.input = TextInput(
            hint_text='Escribe un mensaje...',
            size_hint=(1, 0.1),
            multiline=False,
            background_color=(0.9, 0.9, 0.9, 1)
        )
        
        # Botón enviar
        btn_enviar = Button(
            text='📤 Enviar',
            size_hint=(1, 0.1),
            background_color=(1, 0.84, 0, 1),  # Dorado Tridan
            color=(0, 0, 0, 1)
        )
        btn_enviar.bind(on_press=self.send)
        
        # Versión en la esquina
        version = Label(
            text='v1.1',
            size_hint=(1, 0.05),
            font_size='10sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        
        layout.add_widget(header)
        layout.add_widget(self.chat)
        layout.add_widget(btn_buscar)
        layout.add_widget(self.input)
        layout.add_widget(btn_enviar)
        layout.add_widget(version)
        
        return layout
    
    def log(self, mensaje):
        """Agregar mensaje al chat/log"""
        self.chat.text += f'{mensaje}\n'
        # Auto-scroll al final
        self.chat.cursor = (0, len(self.chat.text))
    
    def request_permissions(self, dt):
        """Solicitar permisos de Android"""
        try:
            from android.permissions import request_permissions, Permission, check_permission
            
            self.log('📋 Verificando permisos...')
            
            permisos_necesarios = []
            
            # Lista de permisos a verificar
            permisos = [
                Permission.BLUETOOTH,
                Permission.BLUETOOTH_ADMIN,
                Permission.BLUETOOTH_SCAN,
                Permission.BLUETOOTH_CONNECT,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ]
            
            # Verificar cuáles faltan
            for permiso in permisos:
                if not check_permission(permiso):
                    permisos_necesarios.append(permiso)
            
            if permisos_necesarios:
                self.log(f'📋 Solicitando {len(permisos_necesarios)} permisos...')
                request_permissions(permisos_necesarios)
                self.log('✅ Permisos solicitados. Por favor acepta.')
            else:
                self.log('✅ Todos los permisos ya otorgados')
                
        except ImportError:
            self.log('⚠️ No se puede solicitar permisos (no es Android)')
        except Exception as e:
            self.log(f'⚠️ Error permisos: {e}')
    
    def buscar_bluetooth(self, instance):
        """Buscar dispositivos Bluetooth"""
        self.log('\n🔍 Iniciando búsqueda Bluetooth...')
        
        try:
            from jnius import autoclass
            
            # Importar clases de Android
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            
            # Obtener adaptador
            adapter = BluetoothAdapter.getDefaultAdapter()
            
            if adapter is None:
                self.log('❌ Este dispositivo no tiene Bluetooth')
                return
            
            if not adapter.isEnabled():
                self.log('⚠️ Bluetooth desactivado')
                self.log('Por favor activa Bluetooth e intenta de nuevo')
                return
            
            self.log('✅ Bluetooth activo')
            
            # Dispositivos emparejados
            paired_devices = adapter.getBondedDevices().toArray()
            
            if len(paired_devices) == 0:
                self.log('📱 No hay dispositivos emparejados')
                self.log('Empareja dispositivos en Configuración primero')
            else:
                self.log(f'\n📱 Dispositivos emparejados: {len(paired_devices)}')
                self.log('─' * 40)
                for i, device in enumerate(paired_devices, 1):
                    name = device.getName()
                    address = device.getAddress()
                    self.log(f'{i}. {name}')
                    self.log(f'   MAC: {address}')
                self.log('─' * 40)
            
            self.log('✅ Búsqueda completada\n')
            
        except ImportError:
            self.log('❌ Error: pyjnius no disponible')
        except Exception as e:
            self.log(f'❌ Error: {e}')
    
    def send(self, instance):
        """Enviar mensaje local"""
        msg = self.input.text.strip()
        if msg:
            self.chat.text += f'Tú: {msg}\n'
            self.input.text = ''
            # Auto-scroll
            self.chat.cursor = (0, len(self.chat.text))

if __name__ == '__main__':
    TridanApp().run()
