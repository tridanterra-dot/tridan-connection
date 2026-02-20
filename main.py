from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import sys

class TridanApp(App):
    def build(self):
        return self.create_main_layout()
    
    def create_main_layout(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Header con logo pequeño + título
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10, padding=10)
        with header.canvas.before:
            Color(0.05, 0.2, 0.4, 0.9)
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=self._update_header_bg, pos=self._update_header_bg)
        
        # Logo pequeño (puede fallar sin crashear)
        try:
            logo_small = Image(
                source='tridan_logo_icon.png',
                size_hint=(None, 1),
                width=50,
                allow_stretch=True,
                keep_ratio=True
            )
            header.add_widget(logo_small)
        except:
            pass  # Si falla el logo, continúa sin él
        
        title = Label(
            text='TRIDAN CONNECTION',
            font_size='24sp',
            bold=True,
            color=(1, 0.84, 0, 1),
            size_hint=(1, 1),
            halign='left',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        
        header.add_widget(title)
        layout.add_widget(header)
        
        # Área de chat
        self.chat = TextInput(
            text='¡Bienvenido a Tridan Connection! 🌳\n\n',
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
        
        # Versión
        version = Label(
            text='v1.2 - Bluetooth Mesh',
            size_hint=(1, 0.05),
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(version)
        
        # Solicitar permisos después de mostrar UI
        Clock.schedule_once(self.request_permissions, 2)
        
        return layout
    
    def _update_header_bg(self, instance, value):
        self.header_bg.size = instance.size
        self.header_bg.pos = instance.pos
    
    def log(self, mensaje):
        """Agregar línea al chat"""
        self.chat.text += f'{mensaje}\n'
        Clock.schedule_once(lambda dt: setattr(self.chat, 'cursor', (0, len(self.chat.text))), 0.1)
    
    def request_permissions(self, dt):
        """Solicitar permisos en Android"""
        if 'ANDROID_BOOTLOGO' not in sys.environ:
            self.log('ℹ️ No es Android - omitiendo permisos')
            return
            
        try:
            from android.permissions import request_permissions, Permission, check_permission
            
            self.log('📋 Verificando permisos...')
            
            permisos_solicitar = []
            permisos_basicos = [
                Permission.BLUETOOTH,
                Permission.BLUETOOTH_ADMIN,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ]
            
            # Android 12+ permisos
            try:
                permisos_basicos.append(Permission.BLUETOOTH_SCAN)
                permisos_basicos.append(Permission.BLUETOOTH_CONNECT)
            except AttributeError:
                pass
            
            for permiso in permisos_basicos:
                try:
                    if not check_permission(permiso):
                        permisos_solicitar.append(permiso)
                except:
                    pass
            
            if permisos_solicitar:
                self.log(f'📋 Solicitando {len(permisos_solicitar)} permisos...')
                request_permissions(permisos_solicitar)
                self.log('✅ Acepta los permisos en el diálogo')
            else:
                self.log('✅ Permisos ya concedidos')
                
        except Exception as e:
            self.log(f'⚠️ Error permisos: {str(e)}')
    
    def buscar_bluetooth(self, instance):
        """Buscar dispositivos Bluetooth"""
        self.log('\n🔍 Buscando dispositivos...')
        self.btn_buscar.text = '⏳ Buscando...'
        self.btn_buscar.disabled = True
        
        if 'ANDROID_BOOTLOGO' not in sys.environ:
            self.log('⚠️ Solo funciona en Android')
            self._reset_buscar_btn()
            return
        
        try:
            from jnius import autoclass
            
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            adapter = BluetoothAdapter.getDefaultAdapter()
            
            if not adapter:
                self.log('❌ Sin adaptador Bluetooth')
                self._reset_buscar_btn()
                return
            
            if not adapter.isEnabled():
                self.log('⚠️ Bluetooth desactivado')
                self._reset_buscar_btn()
                return
            
            self.log('✅ Bluetooth activo')
            
            paired = adapter.getBondedDevices().toArray()
            
            if not paired:
                self.log('📴 Sin dispositivos emparejados')
            else:
                self.log(f'\n📱 {len(paired)} dispositivos:')
                self.log('─' * 40)
                for i, dev in enumerate(paired, 1):
                    name = dev.getName() or '(sin nombre)'
                    addr = dev.getAddress()
                    self.log(f'{i}. {name}')
                    self.log(f'   {addr}')
                self.log('─' * 40)
            
        except Exception as e:
            self.log(f'❌ Error: {str(e)}')
        
        self._reset_buscar_btn()
    
    def _reset_buscar_btn(self):
        self.btn_buscar.text = '🔵 Buscar dispositivos Bluetooth'
        self.btn_buscar.disabled = False
    
    def send(self, instance):
        msg = self.input.text.strip()
        if msg:
            self.chat.text += f'💬 Tú: {msg}\n'
            self.input.text = ''
            Clock.schedule_once(lambda dt: setattr(self.chat, 'cursor', (0, len(self.chat.text))), 0.1)

if __name__ == '__main__':
    TridanApp().run()
