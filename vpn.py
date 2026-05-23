
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
import random

# =========================
# Красивый Popup
# =========================
class RoundedPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.content.canvas.before:
            Color(0.12, 0.12, 0.16, 1)
            self.rect = RoundedRectangle(
                radius=[25],
                pos=self.content.pos,
                size=self.content.size
            )

        self.content.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.content.pos
        self.rect.size = self.content.size


# =========================
# Главное приложение
# =========================
class VPNSubscriptionApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Стандартные сервера
        self.vpn_links = {
            "🇳🇱 Нидерланды":
                "vless://example1",
            "🇪🇪 Эстония":
                "vless://example2"
        }

        self.user_keys = {}
        self.server_ping = {}

    # =========================
    # Красивые кнопки
    # =========================
    def create_button(self, text, color):
        btn = Button(
            text=text,
            size_hint=(1, None),
            height=dp(60),
            background_normal='',
            background_color=color,
            color=(1, 1, 1, 1),
            font_size=18
        )

        with btn.canvas.before:
            Color(*color)
            btn.rect = RoundedRectangle(
                radius=[20],
                pos=btn.pos,
                size=btn.size
            )

        btn.bind(pos=self.update_btn, size=self.update_btn)

        return btn

    def update_btn(self, instance, *args):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    # =========================
    # Интерфейс
    # =========================
    def build(self):

        self.root_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        with self.root_layout.canvas.before:
            Color(0.08, 0.08, 0.1, 1)
            self.bg = RoundedRectangle(
                pos=self.root_layout.pos,
                size=self.root_layout.size
            )

        self.root_layout.bind(pos=self.update_bg, size=self.update_bg)

        # Заголовок
        title = Label(
            text='[b]SecureVPN[/b]',
            markup=True,
            font_size=38,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.15)
        )

        self.root_layout.add_widget(title)

        # Контейнер серверов
        self.servers_layout = BoxLayout(
            orientation='vertical',
            spacing=12,
            size_hint=(1, 0.6)
        )

        self.root_layout.add_widget(self.servers_layout)

        # Загрузка серверов
        self.refresh_servers()

        # Кнопка добавить сервер
        add_btn = self.create_button(
            "➕ Добавить сервер",
            (0.3, 0.7, 1, 1)
        )
        add_btn.bind(on_press=self.show_add_server)

        self.root_layout.add_widget(add_btn)

        # Профиль
        profile_btn = self.create_button(
            "👤 Профиль",
            (0.55, 0.25, 1, 1)
        )

        profile_btn.bind(on_press=self.show_profile)

        self.root_layout.add_widget(profile_btn)

        return self.root_layout

    def update_bg(self, *args):
        self.bg.pos = self.root_layout.pos
        self.bg.size = self.root_layout.size

    # =========================
    # Обновление серверов
    # =========================
    def refresh_servers(self):

        self.servers_layout.clear_widgets()

        for server in self.vpn_links.keys():

            btn = self.create_button(
                server,
                (0.15, 0.55, 1, 1)
            )

            btn.bind(
                on_press=lambda instance, s=server:
                self.copy_link(s)
            )

            self.servers_layout.add_widget(btn)

    # =========================
    # Копирование ссылки
    # =========================
    def copy_link(self, server):

        link = self.vpn_links.get(server)

        Clipboard.copy(link)

        self.user_keys[server] = link
        self.server_ping[server] = random.randint(20, 150)

        popup_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        popup_layout.add_widget(
            Label(
                text="✅ Ссылка скопирована!\nВставьте её в VPN приложение.",
                font_size=18,
                color=(1, 1, 1, 1)
            )
        )

        close_btn = self.create_button(
            "OK",
            (0.2, 0.6, 1, 1)
        )

        popup_layout.add_widget(close_btn)

        popup = RoundedPopup(
            title="Уведомление",
            content=popup_layout,
            size_hint=(0.8, 0.35),
            separator_height=0,
            background_color=(0, 0, 0, 0)
        )

        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    # =========================
    # Добавление сервера
    # =========================
    def show_add_server(self, instance):

        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        title = Label(
            text="Добавить свой сервер",
            font_size=22,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2)
        )

        layout.add_widget(title)

        # Название сервера
        server_name = TextInput(
            hint_text="Название сервера",
            multiline=False,
            size_hint=(1, 0.2),
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )

        layout.add_widget(server_name)

        # VLESS ссылка
        server_link = TextInput(
            hint_text="VLESS/Vmess/Trojan ссылка",
            multiline=False,
            size_hint=(1, 0.2),
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )

        layout.add_widget(server_link)

        # Кнопки
        btns = BoxLayout(
            spacing=10,
            size_hint=(1, 0.25)
        )

        save_btn = self.create_button(
            "Сохранить",
            (0.2, 0.8, 0.4, 1)
        )

        cancel_btn = self.create_button(
            "Отмена",
            (0.9, 0.25, 0.25, 1)
        )

        btns.add_widget(save_btn)
        btns.add_widget(cancel_btn)

        layout.add_widget(btns)

        popup = RoundedPopup(
            title="",
            content=layout,
            size_hint=(0.9, 0.55),
            separator_height=0,
            background_color=(0, 0, 0, 0)
        )

        # Сохранение
        def save_server(instance):

            name = server_name.text.strip()
            link = server_link.text.strip()

            if name and link:

                self.vpn_links[name] = link

                self.refresh_servers()

                popup.dismiss()

        save_btn.bind(on_press=save_server)
        cancel_btn.bind(on_press=popup.dismiss)

        popup.open()

    # =========================
    # Профиль
    # =========================
    def show_profile(self, instance):

        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        layout.add_widget(
            Label(
                text="Ваши VPN ключи",
                font_size=24,
                color=(1, 1, 1, 1),
                size_hint=(1, 0.15)
            )
        )

        scroll = ScrollView(size_hint=(1, 0.7))

        keys_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )

        keys_layout.bind(
            minimum_height=keys_layout.setter('height')
        )

        if not self.user_keys:

            keys_layout.add_widget(
                Label(
                    text="Нет подключений",
                    color=(1, 1, 1, 1)
                )
            )

        else:

            best_server = min(
                self.server_ping,
                key=self.server_ping.get
            )

            for server, key in self.user_keys.items():

                ping = self.server_ping.get(server, 0)

                card = BoxLayout(
                    orientation='vertical',
                    padding=15,
                    spacing=5,
                    size_hint_y=None,
                    height=140
                )

                with card.canvas.before:
                    Color(0.16, 0.16, 0.22, 1)
                    card.rect = RoundedRectangle(
                        radius=[20],
                        pos=card.pos,
                        size=card.size
                    )

                card.bind(pos=self.update_card, size=self.update_card)

                card.add_widget(
                    Label(
                        text=server,
                        bold=True,
                        color=(1, 1, 1, 1),
                        font_size=18
                    )
                )

                card.add_widget(
                    Label(
                        text=f"Ping: {ping} ms",
                        color=(0.6, 1, 0.6, 1)
                    )
                )

                if server == best_server:

                    card.add_widget(
                        Label(
                            text="🔥 Лучший сервер",
                            color=(1, 0.9, 0.3, 1)
                        )
                    )

                keys_layout.add_widget(card)

        scroll.add_widget(keys_layout)

        layout.add_widget(scroll)

        close_btn = self.create_button(
            "Закрыть",
            (0.9, 0.25, 0.25, 1)
        )

        layout.add_widget(close_btn)

        popup = RoundedPopup(
            title="",
            content=layout,
            size_hint=(0.92, 0.85),
            separator_height=0,
            background_color=(0, 0, 0, 0)
        )

        close_btn.bind(on_press=popup.dismiss)

        popup.open()

    def update_card(self, instance, *args):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


if __name__ == '__main__':
    VPNSubscriptionApp().run()