from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class TridanApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='TRIDAN CONNECTION v1.1',
            size_hint=(1, 0.15),
            font_size='24sp',
            bold=True
        )
        
        # Área de chat/log
        self.chat = TextInput(
            text='¡Bienvenido a Tridan Connection!\n',
            multiline=True,
            readonly=True,
            size_hint=(1, 0.5)
        )
        
        # Botón buscar Bluetooth
        btn_buscar = Button(
            text='🔵 Buscar dispositivos Bluetooth',
            size_hint=(1, 0.1),
            background_color=(0.05, 0.15, 0.3, 1)  # Azul Tridan
        )
        btn_buscar.bind(on_press=self.buscar_bluetooth)
        
        # Input de mensaje
        self.input = TextInput(
            hint_text='Escribe un mensaje...',
            size_hint=(1, 0.1),
            multiline=False
        )
        
        # Botón enviar
        btn_enviar = Button(
            text='Enviar',
            size_hint=(1, 0.1),
            background_color=(1, 0.84, 0, 1)  # Dorado Tridan
        )
        btn_enviar.bind(on_press=self.send)
        
        self.layout.add_widget(title)
        self.layout.add_widget(self.chat)
        self.layout.add_widget(btn_buscar)
        self.layout.add_widget(self.input)
        self.layout.add_widget(btn_enviar)
        
        # Solicitar permisos al iniciar
        Clock.schedule_once(self.request_permissions, 1)
        
        return self.layout
    
    def log(self, mensaje):
        """Agregar mensaje al chat/log"""
        self.chat.text += f'{mensaje}\n'
    
    def request_permissions(self, dt):
        """Solicitar permisos de Android"""
        try:
            from android.permissions import request_permissions, Permission
            self.log('📋 Solicitando permisos...')
            request_permissions([
                Permission.BLUETOOTH,
                Permission.BLUETOOTH_ADMIN,
                Permission.BLUETOOTH_SCAN,
                Permission.BLUETOOTH_CONNECT,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ])
            self.log('✅ Permisos solicitados')
        except Exception as e:
            self.log(f'⚠️ Error permisos: {e}')
    
    def buscar_bluetooth(self, instance):
        """Buscar dispositivos Bluetooth"""
        self.log('\n🔍 Buscando dispositivos Bluetooth...')
        
        try:
            from jnius import autoclass
            
            # Importar clases de Android
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            
            # Obtener adaptador Bluetooth
            adapter = BluetoothAdapter.getDefaultAdapter()
            
            if adapter is None:
                self.log('❌ Este dispositivo no tiene Bluetooth')
                return
            
            if not adapter.isEnabled():
                self.log('⚠️ Bluetooth está desactivado')
                self.log('Por favor activa Bluetooth e intenta de nuevo')
                return
            
            self.log('✅ Bluetooth activo')
            
            # Obtener dispositivos emparejados
            paired_devices = adapter.getBondedDevices().toArray()
            
            if len(paired_devices) == 0:
                self.log('📱 No hay dispositivos emparejados')
            else:
                self.log(f'\n📱 Dispositivos emparejados ({len(paired_devices)}):')
                for device in paired_devices:
                    name = device.getName()
                    address = device.getAddress()
                    self.log(f'  • {name} ({address})')
            
            self.log('\n✅ Búsqueda completada')
            
        except Exception as e:
            self.log(f'❌ Error: {e}')
    
    def send(self, instance):
        """Enviar mensaje local"""
        msg = self.input.text
        if msg:
            self.chat.text += f'Tú: {msg}\n'
            self.input.text = ''

if __name__ == '__main__':
    TridanApp().run()
