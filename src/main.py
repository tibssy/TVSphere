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
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
        self.margin = self.DEFAULT_MARGIN
        self.border_radius = self.DEFAULT_BORDER_RADIUS
        self.animate = ft.Animation(400, ft.AnimationCurve.EASE)
        self.bgcolor = ft.Colors.BLACK
        # self.on_click = self.toggle_fullscreen
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color=ft.colors.SHADOW,
            offset=ft.Offset(-1, 3)
        )
        self.content = ft.Container(
            content=ftv.Video(
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
            ),
            on_click=self.toggle_fullscreen
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


class SideBar(ft.Stack):
    def __init__(self, header_height, **kwargs):
        super().__init__(**kwargs)
        self.expand_loose = True
        self.header_height = header_height
        self.main_container = self.create_main_container()
        self.sub_container = self.create_sub_conatainer()
        self.controls = [
            self.sub_container,
            self.main_container
        ]

    def create_main_container(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.FilledButton(
                            text='Show Sub Container',
                            on_click=self.show_sub_container

                        ),
                        bgcolor=ft.Colors.DEEP_ORANGE_900,
                        padding=10,
                        width=self.width,
                        height=self.header_height,
                    ),
                ]
            ),
            bgcolor=ft.Colors.ORANGE,
            expand=True,
            offset=ft.Offset(x=0, y=0),
            animate_offset = ft.Animation(400, ft.AnimationCurve.EASE)
        )

    def create_sub_conatainer(self):
        return ft.Container(
            bgcolor=ft.Colors.BLUE,
            expand=True
        )

    def show_sub_container(self, e):
        self.main_container.offset = ft.Offset(x=-1, y=0)
        self.main_container.update()


class TVSphereApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.video_player = VideoPlayer()
        self.sidebar_width = self.calculate_sidebar_width()
        self.header_height = self.calculate_header_height()
        self.setup_page()

    def calculate_sidebar_width(self):
        return 320 if self.page.width > 768 else 200

    def calculate_header_height(self):
        return 70 if self.page.width > 768 else 60

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

        sidebar_container = SideBar(width=self.sidebar_width, header_height=self.header_height)
        self.page.add(
            ft.Row(
                controls=[
                    sidebar_container,
                    ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor=ft.Colors.PURPLE,
                                height=self.header_height
                            )
                        ],
                        expand=True
                    )
                ],
                expand=True,
                spacing=0
            )
        )

    def adjust_video_player_margin(self):
        if self.page.width > 768:
            self.video_player.set_margin()
            self.video_player.update_margin()


def main(page: ft.Page):
    TVSphereApp(page)


if __name__ == '__main__':
    ft.app(main)
