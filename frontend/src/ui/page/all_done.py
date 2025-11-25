"""All done page - Setup completion confirmation."""
import flet as ft
from core import ClientStorage


class AllDonePage:
    """All done page showing setup completion."""

    # Success message content
    SUCCESS_MESSAGE = """
### 🎉 Setup Complete!

Your E-Voting application has been successfully configured. 

#### What's Next?

✅ **Admin Account Created** - You can now login with your credentials

✅ **Institution Setup** - Your organization details have been saved

✅ **Ready to Use** - All features are now available

#### Getting Started

1. **Create Elections** - Set up your first election
2. **Add Voters** - Import or manually add voter data
3. **Configure Settings** - Customize your election parameters
4. **Monitor Results** - Track voting in real-time

---

**Need Help?** Check the documentation or contact support.
"""

    def __init__(
            self,
            page: ft.Page,
            content_column: ft.Column,
            storage: ClientStorage,
    ):
        """Initialize all done page.

        Args:
            page: Flet page instance
            content_column: Content column
            storage: Storage manager
        """
        self.page = page
        self.content_column = content_column
        self.storage = storage
        self.checkbox_terms: ft.Checkbox = None
        self.continue_button: ft.Container = None

    def render(self) -> None:
        """Render the all done page."""
        # Create continue button (initially disabled)
        self.continue_button = self._create_continue_button()

        # Create checkbox
        self.checkbox_terms = ft.Checkbox(
            label="I have read and understand the above information.",
            value=False,
            adaptive=True,
            on_change=self._on_checkbox_change,
        )

        # Build content
        self.content_column.controls = [
            ft.Column(
                [
                    # Header
                    self._create_header(),

                    # Success message
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Markdown(
                                    value=self.SUCCESS_MESSAGE,
                                    selectable=True,
                                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                    code_theme="atom-one-dark",
                                ),
                                width=400,
                                border=ft.border.all(1, ft.Colors.BLUE_200),
                                border_radius=10,
                                padding=20,
                                bgcolor=ft.Colors.BLUE_50,
                            ),

                            # Checkbox and button
                            ft.Column(
                                [
                                    self.checkbox_terms,
                                    ft.Row(
                                        [self.continue_button],
                                        width=450,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ],
                                width=400,
                                spacing=30,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        width=450,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                    ),
                ],
                width=450,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                key="top",
            ),

            # Scroll to top button
            ft.Column(height=20),
            self._create_scroll_button(),
        ]

        self.content_column.expand = True
        self.content_column.scroll = ft.ScrollMode.ADAPTIVE
        self.page.update()

    def _create_header(self) -> ft.Row:
        """Create page header."""
        return ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.CHECK_CIRCLE_ROUNDED,
                    size=45,
                    color=ft.Colors.GREEN,
                ),
                ft.Text(
                    value="All Done!",
                    size=35,
                    weight=ft.FontWeight.W_600,
                ),
            ],
            width=450,
            height=70,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _create_continue_button(self) -> ft.Container:
        """Create continue button (initially disabled)."""
        return ft.Container(
            width=300,
            height=50,
            border_radius=10,
            bgcolor="#bae6fd",
            opacity=0.5,
            disabled=True,
            tooltip="Please read and accept the information above",
            content=ft.Text(
                value="Continue to Dashboard",
                size=18,
                weight=ft.FontWeight.W_500,
                color=ft.Colors.WHITE,
            ),
            alignment=ft.alignment.center,
            animate=ft.Animation(100, ft.AnimationCurve.DECELERATE),
            on_click=self._on_continue_click,
        )

    def _create_scroll_button(self) -> ft.Row:
        """Create scroll to top button."""
        return ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_CIRCLE_UP_ROUNDED,
                    tooltip="Back to Top",
                    icon_size=30,
                    icon_color=ft.Colors.BLUE_700,
                    on_click=lambda _: self.content_column.scroll_to(
                        key="top",
                        duration=1000
                    ),
                ),
            ],
            width=450,
            alignment=ft.MainAxisAlignment.END,
        )

    def _on_hover_color(self, e: ft.HoverEvent) -> None:
        """Handle button hover effect."""
        if not self.continue_button.disabled:
            self.continue_button.bgcolor = "#0369a1" if e.data == "true" else "#0ea5e9"
            self.continue_button.update()

    def _on_checkbox_change(self, e: ft.ControlEvent) -> None:
        """Handle checkbox state change."""
        if self.checkbox_terms.value:
            # Enable button
            self.continue_button.disabled = False
            self.continue_button.tooltip = None
            self.continue_button.bgcolor = "#0ea5e9"
            self.continue_button.opacity = 1
            self.continue_button.on_hover = self._on_hover_color
        else:
            # Disable button
            self.continue_button.disabled = True
            self.continue_button.tooltip = "Please read and accept the information above"
            self.continue_button.bgcolor = "#bae6fd"
            self.continue_button.opacity = 0.5
            self.continue_button.on_hover = None

        self.continue_button.update()

    def _on_continue_click(self, e: ft.ControlEvent) -> None:
        """Handle continue button click."""
        # Show success snackbar
        snackbar = ft.SnackBar(
            content=ft.Text("Welcome to E-Voting! 🎉"),
            bgcolor=ft.Colors.GREEN,
            duration=2000,
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()

        # TODO: Navigate to dashboard or main app
        print("Navigate to: Dashboard")
        # Example: Navigate to admin dashboard
        # from .dashboard import DashboardPage
        # dashboard = DashboardPage(self.page, self.content_column, self.storage)
        # dashboard.render()


# Backward compatibility function
def all_done_page(
        page: ft.Page,
        content_column: ft.Column,
        storage: ClientStorage,
) -> None:
    """Create and render all done page (legacy function).

    Args:
        page: Flet page instance
        content_column: Content column
        storage: Storage manager
    """
    done_page = AllDonePage(page, content_column, storage)
    done_page.render()
