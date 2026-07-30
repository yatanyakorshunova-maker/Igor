from __future__ import annotations

from pathlib import Path
import json

from kivy.config import Config

# Размер используется только при запуске на компьютере. На Android окно занимает экран устройства.
Config.set("graphics", "width", "420")
Config.set("graphics", "height", "820")
Config.set("graphics", "resizable", "1")

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

from game_logic import PetModel


COLORS = {
    "background": get_color_from_hex("0B0D1C"),
    "panel": get_color_from_hex("171A33"),
    "panel_light": get_color_from_hex("222746"),
    "outline": get_color_from_hex("363D68"),
    "text": get_color_from_hex("F7F8FF"),
    "muted": get_color_from_hex("AEB7D8"),
    "purple": get_color_from_hex("9B6CFF"),
    "purple_dark": get_color_from_hex("6844CF"),
    "cyan": get_color_from_hex("39D4F3"),
    "green": get_color_from_hex("4DE0A2"),
    "orange": get_color_from_hex("FF9D55"),
    "yellow": get_color_from_hex("FFD166"),
    "red": get_color_from_hex("FF6687"),
    "white_card": get_color_from_hex("F5F5FF"),
    "dark_text": get_color_from_hex("28213D"),
}


class RoundedPanel(BoxLayout):
    bg_color = ListProperty(COLORS["panel"])
    border_color = ListProperty(COLORS["outline"])
    radius = NumericProperty(dp(22))
    border_width = NumericProperty(1.1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_color_instruction = Color(*self.bg_color)
            self._bg_rectangle = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            self._border_color_instruction = Color(*self.border_color)
            self._border_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius),
                width=self.border_width,
            )
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            bg_color=self._update_canvas,
            border_color=self._update_canvas,
            radius=self._update_canvas,
            border_width=self._update_canvas,
        )

    def _update_canvas(self, *_args):
        self._bg_color_instruction.rgba = self.bg_color
        self._bg_rectangle.pos = self.pos
        self._bg_rectangle.size = self.size
        self._bg_rectangle.radius = [self.radius]
        self._border_color_instruction.rgba = self.border_color
        self._border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius)
        self._border_line.width = self.border_width


class RoundedButton(Button):
    fill_color = ListProperty(COLORS["purple"])
    pressed_color = ListProperty(COLORS["purple_dark"])
    disabled_fill_color = ListProperty(get_color_from_hex("424760"))
    radius = NumericProperty(dp(18))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_disabled_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = COLORS["text"]
        self.bold = True
        self.font_size = sp(16)
        with self.canvas.before:
            self._fill_instruction = Color(*self.fill_color)
            self._fill_rectangle = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            fill_color=self._update_canvas,
            pressed_color=self._update_canvas,
            disabled_fill_color=self._update_canvas,
            radius=self._update_canvas,
            state=self._update_canvas,
            disabled=self._update_canvas,
        )

    def _update_canvas(self, *_args):
        if self.disabled:
            color = self.disabled_fill_color
        elif self.state == "down":
            color = self.pressed_color
        else:
            color = self.fill_color
        self._fill_instruction.rgba = color
        self._fill_rectangle.pos = self.pos
        self._fill_rectangle.size = self.size
        self._fill_rectangle.radius = [self.radius]


class Meter(Widget):
    value = NumericProperty(50)
    track_color = ListProperty(get_color_from_hex("343956"))
    fill_color = ListProperty(COLORS["purple"])
    radius = NumericProperty(dp(8))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self._track_color_instruction = Color(*self.track_color)
            self._track_rectangle = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            self._fill_color_instruction = Color(*self.fill_color)
            self._fill_rectangle = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            value=self._update_canvas,
            track_color=self._update_canvas,
            fill_color=self._update_canvas,
            radius=self._update_canvas,
        )

    def _update_canvas(self, *_args):
        self._track_color_instruction.rgba = self.track_color
        self._track_rectangle.pos = self.pos
        self._track_rectangle.size = self.size
        self._track_rectangle.radius = [self.radius]
        fill_width = max(0, self.width * max(0, min(100, self.value)) / 100)
        self._fill_color_instruction.rgba = self.fill_color
        self._fill_rectangle.pos = self.pos
        self._fill_rectangle.size = (fill_width, self.height)
        self._fill_rectangle.radius = [self.radius]


class StatRow(RoundedPanel):
    def __init__(self, title: str, fill_color, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(72)
        self.padding = (dp(14), dp(9))
        self.spacing = dp(7)
        self.bg_color = COLORS["panel_light"]
        self.border_color = get_color_from_hex("303657")
        self.radius = dp(17)

        top = BoxLayout(size_hint_y=None, height=dp(25))
        self.title_label = Label(
            text=title,
            halign="left",
            valign="middle",
            color=COLORS["text"],
            bold=True,
            font_size=sp(14),
        )
        self.title_label.bind(size=lambda widget, _value: setattr(widget, "text_size", widget.size))
        self.value_label = Label(
            text="50 / 100",
            size_hint_x=None,
            width=dp(76),
            halign="right",
            valign="middle",
            color=COLORS["muted"],
            bold=True,
            font_size=sp(13),
        )
        self.value_label.bind(size=lambda widget, _value: setattr(widget, "text_size", widget.size))
        top.add_widget(self.title_label)
        top.add_widget(self.value_label)
        self.meter = Meter(value=50, fill_color=fill_color, size_hint_y=None, height=dp(11))
        self.add_widget(top)
        self.add_widget(self.meter)

    def set_value(self, value: int) -> None:
        self.meter.value = value
        self.value_label.text = f"{value} / 100"


class DigitalPetRoot(FloatLayout):
    def __init__(self, model: PetModel, asset_dir: Path, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.asset_dir = asset_dir
        self.sleep_event = None
        self.images = {
            "normal": str(asset_dir / "pet_normal.png"),
            "happy": str(asset_dir / "pet_happy.png"),
            "sad": str(asset_dir / "pet_sad.png"),
            "hungry": str(asset_dir / "pet_hungry.png"),
            "tired": str(asset_dir / "pet_tired.png"),
            "sleep": str(asset_dir / "pet_sleep.png"),
        }

        with self.canvas.before:
            self._bg_color = Color(*COLORS["background"])
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
            self._glow_color = Color(0.17, 0.10, 0.35, 0.42)
            self._glow_rect = RoundedRectangle(pos=self.pos, size=(dp(280), dp(280)), radius=[dp(140)])
        self.bind(pos=self._update_background, size=self._update_background)

        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            bar_width=dp(3),
            bar_color=COLORS["purple"],
            bar_inactive_color=(0, 0, 0, 0),
        )
        self.content = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=(dp(16), dp(18), dp(16), dp(24)),
            spacing=dp(14),
        )
        self.content.bind(minimum_height=self.content.setter("height"))
        scroll.add_widget(self.content)
        self.add_widget(scroll)

        self._build_header()
        self._build_pet_card()
        self._build_stats()
        self._build_actions()
        self._build_footer()
        self.refresh(message=self.model.status_message())

        Clock.schedule_interval(self._passive_update, 15)

    def _update_background(self, *_args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._glow_rect.pos = (self.width * 0.5 - dp(140), self.height - dp(250))
        self._glow_rect.size = (dp(280), dp(280))

    @staticmethod
    def _fit_text(label: Label) -> None:
        label.text_size = label.size

    def _build_header(self) -> None:
        header = BoxLayout(size_hint_y=None, height=dp(58), spacing=dp(9))
        title_box = BoxLayout(orientation="vertical")
        title = Label(
            text="ЦИФРОВОЙ ПИТОМЕЦ",
            halign="left",
            valign="bottom",
            color=COLORS["text"],
            bold=True,
            font_size=sp(19),
        )
        subtitle = Label(
            text="Python + Kivy",
            halign="left",
            valign="top",
            color=COLORS["cyan"],
            font_size=sp(12),
        )
        title.bind(size=lambda widget, _value: self._fit_text(widget))
        subtitle.bind(size=lambda widget, _value: self._fit_text(widget))
        title_box.add_widget(title)
        title_box.add_widget(subtitle)

        self.status_label = Label(
            text="Уровень 1\nМонеты: 0",
            size_hint_x=None,
            width=dp(98),
            color=COLORS["yellow"],
            bold=True,
            halign="right",
            valign="middle",
            font_size=sp(12),
        )
        self.status_label.bind(size=lambda widget, _value: self._fit_text(widget))
        help_button = RoundedButton(text="?", size_hint_x=None, width=dp(44), fill_color=COLORS["panel_light"])
        help_button.bind(on_release=lambda *_args: self.show_help())
        settings_button = RoundedButton(text="...", size_hint_x=None, width=dp(44), fill_color=COLORS["panel_light"])
        settings_button.bind(on_release=lambda *_args: self.show_settings())

        header.add_widget(title_box)
        header.add_widget(self.status_label)
        header.add_widget(help_button)
        header.add_widget(settings_button)
        self.content.add_widget(header)

    def _build_pet_card(self) -> None:
        card = RoundedPanel(
            orientation="vertical",
            size_hint_y=None,
            height=dp(465),
            padding=(dp(13), dp(13)),
            spacing=dp(9),
            bg_color=COLORS["panel"],
            border_color=get_color_from_hex("423C70"),
            radius=dp(27),
        )
        self.name_label = Label(
            text=self.model.name.upper(),
            size_hint_y=None,
            height=dp(43),
            color=COLORS["text"],
            bold=True,
            font_size=sp(27),
        )
        self.pet_image = Image(
            source=self.images["normal"],
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=None,
            height=dp(330),
        )
        message_card = RoundedPanel(
            size_hint_y=None,
            height=dp(68),
            padding=(dp(14), dp(8)),
            bg_color=COLORS["white_card"],
            border_color=get_color_from_hex("D3C5FF"),
            radius=dp(19),
        )
        self.message_label = Label(
            text="",
            color=COLORS["dark_text"],
            bold=True,
            font_size=sp(14),
            halign="center",
            valign="middle",
        )
        self.message_label.bind(size=lambda widget, _value: self._fit_text(widget))
        message_card.add_widget(self.message_label)
        card.add_widget(self.name_label)
        card.add_widget(self.pet_image)
        card.add_widget(message_card)
        self.content.add_widget(card)

    def _build_stats(self) -> None:
        stats = RoundedPanel(
            orientation="vertical",
            size_hint_y=None,
            height=dp(254),
            padding=dp(12),
            spacing=dp(8),
            bg_color=COLORS["panel"],
            border_color=get_color_from_hex("30375C"),
            radius=dp(23),
        )
        heading = Label(
            text="СОСТОЯНИЕ ПИТОМЦА",
            size_hint_y=None,
            height=dp(25),
            halign="left",
            color=COLORS["muted"],
            bold=True,
            font_size=sp(12),
        )
        heading.bind(size=lambda widget, _value: self._fit_text(widget))
        self.satiety_row = StatRow("Сытость", COLORS["orange"])
        self.mood_row = StatRow("Настроение", COLORS["purple"])
        self.energy_row = StatRow("Энергия", COLORS["cyan"])
        stats.add_widget(heading)
        stats.add_widget(self.satiety_row)
        stats.add_widget(self.mood_row)
        stats.add_widget(self.energy_row)
        self.content.add_widget(stats)

    def _build_actions(self) -> None:
        action_row = BoxLayout(size_hint_y=None, height=dp(74), spacing=dp(9))
        self.feed_button = RoundedButton(text="Кормить", fill_color=COLORS["orange"], pressed_color=get_color_from_hex("D66F34"))
        self.play_button = RoundedButton(text="Играть", fill_color=COLORS["purple"], pressed_color=COLORS["purple_dark"])
        self.sleep_button = RoundedButton(text="Спать", fill_color=COLORS["cyan"], pressed_color=get_color_from_hex("1A9FBC"))
        self.sleep_button.color = get_color_from_hex("061B22")
        self.feed_button.bind(on_release=lambda *_args: self.perform_action("feed"))
        self.play_button.bind(on_release=lambda *_args: self.perform_action("play"))
        self.sleep_button.bind(on_release=lambda *_args: self.perform_action("sleep"))
        action_row.add_widget(self.feed_button)
        action_row.add_widget(self.play_button)
        action_row.add_widget(self.sleep_button)
        self.content.add_widget(action_row)

    def _build_footer(self) -> None:
        self.goal_label = Label(
            text="Цель: поднимите все показатели до 80 и получите 100 монет.",
            size_hint_y=None,
            height=dp(46),
            color=COLORS["muted"],
            halign="center",
            valign="middle",
            font_size=sp(12),
        )
        self.goal_label.bind(size=lambda widget, _value: self._fit_text(widget))
        self.content.add_widget(self.goal_label)

    def perform_action(self, action: str) -> None:
        if self.model.sleeping:
            self.refresh(message="Питомец спит. Подождите несколько секунд.")
            return

        if action == "feed":
            message = self.model.feed()
            self._animate_pet("bounce")
            self._after_change(message)
        elif action == "play":
            message = self.model.play()
            self._animate_pet("flash")
            self._after_change(message)
        elif action == "sleep":
            message = self.model.start_sleep()
            self._set_actions_disabled(True)
            self.refresh(message=message, force_state="sleep")
            self._animate_pet("fade")
            self._save()
            self.sleep_event = Clock.schedule_once(self._wake_up, 3)

    def _wake_up(self, _dt) -> None:
        message = self.model.finish_sleep()
        self._set_actions_disabled(False)
        self._after_change(message)
        self.sleep_event = None

    def _after_change(self, message: str) -> None:
        reward_now = self.model.check_reward()
        self.refresh(message=message)
        self._save()
        if reward_now:
            Clock.schedule_once(lambda _dt: self.show_reward(), 0.2)

    def _passive_update(self, _dt) -> None:
        message = self.model.passive_tick()
        reward_now = self.model.check_reward()
        self.refresh(message=message)
        self._save()
        if reward_now:
            self.show_reward()

    def refresh(self, message: str | None = None, force_state: str | None = None) -> None:
        self.name_label.text = self.model.name.upper()
        self.status_label.text = f"Уровень {self.model.level}\nМонеты: {self.model.coins}"
        self.satiety_row.set_value(self.model.satiety)
        self.mood_row.set_value(self.model.mood)
        self.energy_row.set_value(self.model.energy)
        state = force_state or self.model.image_state()
        self.pet_image.source = self.images[state]
        self.pet_image.reload()
        self.message_label.text = message or self.model.status_message()
        if self.model.reward_received:
            self.goal_label.text = "Награда получена. Продолжайте заботиться о питомце!"
            self.goal_label.color = COLORS["green"]
        else:
            self.goal_label.text = "Цель: поднимите все показатели до 80 и получите 100 монет."
            self.goal_label.color = COLORS["muted"]

    def _set_actions_disabled(self, disabled: bool) -> None:
        self.feed_button.disabled = disabled
        self.play_button.disabled = disabled
        self.sleep_button.disabled = disabled

    def _animate_pet(self, kind: str) -> None:
        Animation.cancel_all(self.pet_image)
        if kind == "bounce":
            animation = Animation(opacity=0.65, duration=0.08) + Animation(opacity=1, duration=0.18)
        elif kind == "flash":
            animation = Animation(opacity=0.35, duration=0.06) + Animation(opacity=1, duration=0.2)
        else:
            animation = Animation(opacity=0.7, duration=0.25) + Animation(opacity=1, duration=0.25)
        animation.start(self.pet_image)

    def _save(self) -> None:
        app = App.get_running_app()
        if app:
            app.save_model(self.model)

    def show_help(self) -> None:
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        text = (
            "Заботьтесь о питомце и следите за тремя показателями.\n\n"
            "Кормить: сытость +20, настроение +5.\n"
            "Играть: настроение +20, энергия -15, сытость -5.\n"
            "Спать: энергия +30, сытость -10.\n\n"
            "Показатели понемногу снижаются каждые 15 секунд. "
            "Поднимите все три значения до 80, чтобы получить награду."
        )
        label = Label(text=text, color=COLORS["text"], halign="left", valign="top", font_size=sp(15))
        label.bind(size=lambda widget, _value: self._fit_text(widget))
        close = RoundedButton(text="Понятно", size_hint_y=None, height=dp(52))
        content.add_widget(label)
        content.add_widget(close)
        popup = Popup(
            title="Как играть",
            content=content,
            size_hint=(0.9, 0.68),
            background_color=COLORS["panel"],
            separator_color=COLORS["purple"],
        )
        close.bind(on_release=popup.dismiss)
        popup.open()

    def show_settings(self) -> None:
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        hint = Label(
            text="Можно изменить имя персонажа или начать игру заново.",
            size_hint_y=None,
            height=dp(54),
            color=COLORS["muted"],
            halign="left",
            valign="middle",
            font_size=sp(14),
        )
        hint.bind(size=lambda widget, _value: self._fit_text(widget))
        name_input = TextInput(
            text=self.model.name,
            multiline=False,
            size_hint_y=None,
            height=dp(52),
            padding=(dp(12), dp(14)),
            background_color=COLORS["panel_light"],
            foreground_color=COLORS["text"],
            cursor_color=COLORS["cyan"],
        )
        save_button = RoundedButton(text="Сохранить имя", size_hint_y=None, height=dp(52))
        reset_button = RoundedButton(
            text="Сбросить прогресс",
            size_hint_y=None,
            height=dp(52),
            fill_color=COLORS["red"],
            pressed_color=get_color_from_hex("CC405E"),
        )
        close_button = RoundedButton(
            text="Закрыть",
            size_hint_y=None,
            height=dp(50),
            fill_color=COLORS["panel_light"],
            pressed_color=COLORS["outline"],
        )
        content.add_widget(hint)
        content.add_widget(name_input)
        content.add_widget(save_button)
        content.add_widget(reset_button)
        content.add_widget(close_button)
        popup = Popup(
            title="Настройки",
            content=content,
            size_hint=(0.9, 0.65),
            background_color=COLORS["panel"],
            separator_color=COLORS["purple"],
        )

        def save_name(*_args):
            clean_name = name_input.text.strip()[:16]
            if clean_name:
                self.model.name = clean_name
                self.refresh(message=f"Теперь питомца зовут {clean_name}.")
                self._save()
                popup.dismiss()

        def reset_progress(*_args):
            self.model.reset(keep_name=True)
            self._set_actions_disabled(False)
            self.refresh(message="Игра началась заново.")
            self._save()
            popup.dismiss()

        save_button.bind(on_release=save_name)
        reset_button.bind(on_release=reset_progress)
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def show_reward(self) -> None:
        content = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        label = Label(
            text=(
                "ЦЕЛЬ ДОСТИГНУТА!\n\n"
                "Все показатели подняты до 80.\n"
                "Питомец счастлив, а вы получаете 100 монет."
            ),
            color=COLORS["text"],
            bold=True,
            halign="center",
            valign="middle",
            font_size=sp(19),
        )
        label.bind(size=lambda widget, _value: self._fit_text(widget))
        close = RoundedButton(text="Продолжить", size_hint_y=None, height=dp(54), fill_color=COLORS["green"])
        close.color = get_color_from_hex("08261B")
        content.add_widget(label)
        content.add_widget(close)
        popup = Popup(
            title="Награда",
            content=content,
            size_hint=(0.88, 0.55),
            background_color=COLORS["panel"],
            separator_color=COLORS["yellow"],
            auto_dismiss=False,
        )
        close.bind(on_release=popup.dismiss)
        popup.open()


class DigitalPetApp(App):
    title = "Мой цифровой питомец"

    def build(self):
        Window.clearcolor = COLORS["background"]
        Window.softinput_mode = "below_target"
        self.asset_dir = Path(__file__).resolve().parent / "assets"
        self.model = self.load_model()
        self.root_widget = DigitalPetRoot(self.model, self.asset_dir)
        return self.root_widget

    @property
    def save_path(self) -> Path:
        return Path(self.user_data_dir) / "pet_save.json"

    def load_model(self) -> PetModel:
        try:
            if self.save_path.exists():
                data = json.loads(self.save_path.read_text(encoding="utf-8"))
                return PetModel.from_dict(data)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
        return PetModel()

    def save_model(self, model: PetModel) -> None:
        try:
            self.save_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = self.save_path.with_suffix(".tmp")
            temp_path.write_text(
                json.dumps(model.to_dict(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            temp_path.replace(self.save_path)
        except OSError:
            # Игра продолжит работать, даже если устройство временно не позволило сохранить файл.
            pass

    def on_stop(self):
        self.save_model(self.model)

    def on_pause(self):
        self.save_model(self.model)
        return True


if __name__ == "__main__":
    DigitalPetApp().run()
