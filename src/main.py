import flet as ft
import flet_video as ftv


class VideoPlayer(ft.Container):
    DEFAULT_MARGIN = ft.Margin(left=200, right=15, top=60, bottom=15)
    FULLSCREEN_MARGIN = ft.Margin(left=0, right=0, top=0, bottom=0)
    DEFAULT_BORDER_RADIUS = 12
    FULLSCREEN_BORDER_RADIUS = 0
    SIZES = ['contain', 'cover', 'fill', 'fitHeight', 'fitWidth', 'scaleDown']

    def __init__(self, fit=1, **kwargs):
        super().__init__(**kwargs)
        self.fullscreen = False
        self.fit = fit
        self.margin = self.DEFAULT_MARGIN
        self.border_radius = self.DEFAULT_BORDER_RADIUS
        self.animate = ft.Animation(400, ft.AnimationCurve.EASE)
        self.bgcolor = ft.Colors.BLACK
        self.on_click = self.toggle_fullscreen
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color=ft.colors.SHADOW,
            offset=ft.Offset(-1, 3)
        )
        self.content = ftv.Video(
            playlist=[
                ftv.VideoMedia(
                    resource='https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
                )
            ],
            playlist_mode=ftv.PlaylistMode.SINGLE,
            fill_color='#202020',
            fit=ft.ImageFit(self.SIZES[self.fit]),
            autoplay=True,
            show_controls=False,
            wakelock=True,
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
        self.content.fit = ft.ImageFit(self.SIZES[self.fit])
        self.content.update()

    @classmethod
    def set_margin(cls):
        cls.DEFAULT_MARGIN = ft.Margin(left=320, right=20, top=70, bottom=20)

    def update_margin(self):
        self.margin = self.DEFAULT_MARGIN
        self.update()


class TVSphereApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.video_player = VideoPlayer()
        self.sidebar_width = self.calculate_sidebar_width()
        self.setup_page()

    def calculate_sidebar_width(self):
        return 320 if self.page.width > 768 else 200

    def setup_page(self):
        self.configure_page_properties()
        self.add_video_player_to_overlay()
        self.add_sidebar_container()
        self.adjust_video_player_margin()

    def configure_page_properties(self):
        self.page.title = 'TVSphere'
        self.page.padding = 0
        self.page.spacing = 0

    def add_video_player_to_overlay(self):
        self.page.overlay.append(self.video_player)

    def add_sidebar_container(self):
        sidebar_content = ft.Text(
            f'width: {self.page.width}\nheight: {self.page.height}', size=10
        )
        sidebar_container = ft.Container(
            content=sidebar_content,
            bgcolor='#604000',
            width=self.sidebar_width,
            expand=True
        )
        self.page.add(sidebar_container)

    def adjust_video_player_margin(self):
        if self.page.width > 768:
            self.video_player.set_margin()
            self.video_player.update_margin()


def main(page: ft.Page):
    TVSphereApp(page)


if __name__ == '__main__':
    ft.app(main)
