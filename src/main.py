import flet as ft
import flet_video as ftv
import re

class VideoPlayer(ft.Container):
    DEFAULT_MARGIN = ft.Margin(left=200, right=15, top=60, bottom=15)
    FULLSCREEN_MARGIN = ft.Margin(left=0, right=0, top=0, bottom=0)
    DEFAULT_BORDER_RADIUS = 16
    FULLSCREEN_BORDER_RADIUS = 0
    SIZES = ['contain', 'cover', 'fill', 'fitHeight', 'fitWidth', 'scaleDown']

    def __init__(self, fit=0, **kwargs):
        super().__init__(**kwargs)
        self.fullscreen = False
        self.fit = fit
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
        self.margin = self.DEFAULT_MARGIN
        self.border_radius = self.DEFAULT_BORDER_RADIUS
        self.animate = ft.Animation(400, ft.AnimationCurve.EASE)
        self.bgcolor = '#000000'
        self.video_player = self._create_video_player()
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color=ft.Colors.BLACK45,
            offset=ft.Offset(-1, 3)
        )
        self.content = ft.Container(
            content=self.video_player,
            on_click=self.toggle_fullscreen
        )

    def _create_video_player(self):
        return ftv.Video(
            playlist=[
                ftv.VideoMedia(
                    resource='https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
                )
            ],
            playlist_mode=ftv.PlaylistMode.SINGLE,
            fill_color='#000000',
            fit=ft.ImageFit(self.SIZES[self.fit]),
            autoplay=True,
            show_controls=False,
            wakelock=True,
            resume_upon_entering_foreground_mode=True,
            pause_upon_entering_background_mode=True,
            on_loaded=lambda e: print("Video loaded successfully!")
        )

    def toggle_fullscreen(self, e):
        self.fullscreen = not self.fullscreen
        self.update_player_state()

    def update_player_state(self):
        if self.fullscreen:
            self.margin = self.FULLSCREEN_MARGIN
            self.border_radius = self.FULLSCREEN_BORDER_RADIUS
        else:
            self.margin = self.DEFAULT_MARGIN
            self.border_radius = self.DEFAULT_BORDER_RADIUS

        self.update()

    def change_ratio(self, e):
        self.fit = (self.fit + 1) % len(self.SIZES)
        self.video_player.fit = ft.ImageFit(self.SIZES[self.fit])
        self.video_player.update()

    @classmethod
    def set_margin(cls, margin: ft.Margin):
        cls.DEFAULT_MARGIN = margin

    def update_margin(self):
        self.margin = self.DEFAULT_MARGIN
        self.update()


class SideBar(ft.Stack):
    def __init__(self, header_height, file_picker, **kwargs):
        super().__init__(**kwargs)
        self.expand_loose = True
        self.header_height = header_height
        self.file_picker = file_picker
        self.file_picker.on_result = self.pick_files_result
        self.playlist_container = self.create_playlis_container()
        self.main_container = self.create_main_container()
        self.sub_container = self.create_sub_conatainer()
        self.controls = [
            self.sub_container,
            self.main_container
        ]

    def did_mount(self):
        self.load_playlists()

    def load_playlists(self):
        playlists = self.page.client_storage.get_keys("playlist.")
        if not playlists:
            return

        for playlist in playlists:
            playlist_name = playlist.split('.')[-1]
            self.add_playlist(playlist_name)

    def create_main_container(self):
        icon_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(6),
            padding=0,
            icon_size=26
        )
        add_button = ft.IconButton(
            ft.Icons.ADD,
            style=icon_style,
            on_click=lambda _: self.file_picker.pick_files(
                allow_multiple=False,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["m3u", "m3u8"]
            )
        )
        channel_list_text = ft.Text(value='Channel Lists', size=24)
        header_row = ft.Row(
            controls=[add_button, channel_list_text],
            spacing=0,
            width=self.width,
            height=self.header_height
        )
        divider = ft.Divider(height=3, thickness=1, leading_indent=6, trailing_indent=6)
        column_content = ft.Column(controls=[header_row, divider, self.playlist_container], spacing=0)
        return ft.Container(
            content=column_content,
            padding=ft.padding.symmetric(horizontal=6),
            bgcolor=ft.Colors.GREY_900,
            expand=True,
            offset=ft.Offset(x=0, y=0),
            animate_offset=ft.Animation(400, ft.AnimationCurve.EASE)
        )

    def create_sub_conatainer(self):
        return ft.Container(expand=True)

    def show_sub_container(self, e):
        self.main_container.offset = ft.Offset(x=-1, y=0)
        self.main_container.update()

    def create_playlis_container(self):
        return ft.ListView(controls=[], expand=True)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            playlist_name = e.files[0].name.split('.', maxsplit=1)[0]
            self.add_playlist(playlist_name)

            playlist = self.parse_playlist_file(e.files[0].path)
            self.page.client_storage.set(f'playlist.{playlist_name}', playlist)
            # print(self.page.client_storage.get(f'playlist.{playlist_name}'))
            # print(self.page.client_storage.get_keys("playlist."))
            # self.page.client_storage.clear()

    def parse_playlist_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if not lines or not lines[0].startswith("#EXTM3U"):
            raise ValueError("Invalid M3U/M3U8 file: Missing #EXTM3U header")

        pattern = re.compile(r'^#EXTINF|http|rtmp|rtsp|mmsh|://')
        filtered = filter(lambda x: re.match(pattern, x), lines)
        return [{'name': name.split(',')[-1].strip(), 'url': url.strip()} for name, url in zip(filtered, filtered)]

    def add_playlist(self, playlist_name: str):
        list_title = ft.ListTile(
            title=ft.Text(playlist_name),
            bgcolor=ft.Colors.GREY_900,
            hover_color=ft.Colors.TRANSPARENT,
            on_click=self.show_sub_container
        )
        dismissible = ft.Dismissible(
            key=playlist_name,
            height=46,
            content=list_title,
            dismiss_direction=ft.DismissDirection.END_TO_START,
            secondary_background=ft.Container(bgcolor=ft.Colors.ORANGE_ACCENT),
            on_dismiss=self.handle_dismiss,
            dismiss_thresholds={ft.DismissDirection.END_TO_START: 0.5}
        )
        self.playlist_container.controls.append(dismissible)
        self.playlist_container.update()

    def handle_dismiss(self, e):
        e.control.parent.controls.remove(e.control)
        self.page.client_storage.remove(f'playlist.{e.control.key}')
        self.update()



class HeaderBar(ft.Container):
    def __init__(self, header_height, platform, **kwargs):
        super().__init__(**kwargs)
        self.platform = platform
        self.padding = ft.padding.only(right=20)
        self.height = header_height
        # self.bgcolor = ft.Colors.PURPLE
        self.content = self.create_header()

    def create_header(self):
        header_indicator = ft.WindowDragArea(content=ft.Container(), expand=True)
        header_controls = self.create_app_controls()
        return ft.Row(controls=[header_indicator, header_controls])

    def create_app_controls(self):
        icon_style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(6), padding=0, icon_size=26)
        controls = [
            ft.IconButton(ft.Icons.REPEAT_ROUNDED, style=icon_style, on_click=lambda e: print('REPEAT_ROUNDED')),
            ft.IconButton(ft.Icons.ASPECT_RATIO, style=icon_style, on_click=lambda e: e.page.overlay[0].change_ratio(e)),
            ft.IconButton(ft.Icons.TIMER_OUTLINED, style=icon_style, on_click=lambda e: print('TIMER')),
            ft.IconButton(ft.Icons.CLOSE, style=icon_style, on_click=self.close_app)
        ]
        if self.platform != 'android':
            controls.insert(-1, ft.IconButton(ft.Icons.FULLSCREEN, style=icon_style, on_click=self.toggle_fullscreen))
        return ft.Row(controls=controls, spacing=0)

    def toggle_fullscreen(self, e):
        self.page.window.full_screen = not self.page.window.full_screen
        self.page.update()

    def close_app(self, e):
        if self.platform == 'android':
            import sys
            sys.exit()
        else:
            self.page.window.close()

class TVSphereApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.platform = self.page.platform.value
        self.video_player = VideoPlayer()
        self.file_picker = ft.FilePicker()
        self.sidebar_width = self.calculate_sidebar_width()
        self.header_height = self.calculate_header_height()
        self.setup_page()

    def calculate_sidebar_width(self):
        return 360 if self.page.width > 768 else 200

    def calculate_header_height(self):
        return 70 if self.page.width > 768 else 60

    def setup_page(self):
        self.configure_page_properties()
        self.add_video_player_to_overlay()
        self.add_file_picker_to_overlay()
        self.add_controls_to_page()
        self.adjust_video_player_margin()

    def configure_page_properties(self):
        self.page.window.title_bar_hidden = True
        self.page.window.title_bar_buttons_hidden = True
        self.page.title = 'TVSphere'
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = ft.Colors.GREY_900
        self.page.theme = ft.Theme(color_scheme_seed=ft.Colors.ORANGE_ACCENT)

    def add_video_player_to_overlay(self):
        self.page.overlay.append(self.video_player)

    def add_file_picker_to_overlay(self):
        self.page.overlay.append(self.file_picker)

    def add_controls_to_page(self):
        sidebar_container = SideBar(width=self.sidebar_width, header_height=self.header_height, file_picker=self.file_picker)
        header_bar = HeaderBar(header_height=self.header_height, platform=self.platform)
        controls = [sidebar_container, ft.Column(controls=[header_bar], expand=True)]
        self.page.add(ft.Row(controls=controls, expand=True, spacing=0))

    def adjust_video_player_margin(self):
        if self.page.width > 768:
            self.video_player.set_margin(ft.Margin(left=self.sidebar_width, right=20, top=self.header_height, bottom=20))
            self.video_player.update_margin()


def main(page: ft.Page):
    TVSphereApp(page)


if __name__ == '__main__':
    ft.app(main)
