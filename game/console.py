CONSOLE_AUTO = "Auto"
CONSOLE_DESKTOP = "Desktop"
CONSOLE_CLASSIC = "Classic Touch"
CONSOLE_MODERN = "Modern Touch"
CONSOLE_TABLET_PLUS = "Tablet Plus"


CONSOLE_OPTIONS = [
    CONSOLE_AUTO,
    CONSOLE_DESKTOP,
    CONSOLE_CLASSIC,
    CONSOLE_MODERN,
    CONSOLE_TABLET_PLUS,
]


CONSOLE_DESCRIPTIONS = {
    CONSOLE_AUTO: "Automatically choose the best control layout.",
    CONSOLE_DESKTOP: "Keyboard controls for desktop play.",
    CONSOLE_CLASSIC: "Touch D-pad with 2 action buttons.",
    CONSOLE_MODERN: "Touch joystick with 4 action buttons.",
    CONSOLE_TABLET_PLUS: "Two joysticks: movement + combat plane.",
}


def get_default_console():
    return CONSOLE_AUTO


def is_touch_console(console_name):
    return console_name in [
        CONSOLE_CLASSIC,
        CONSOLE_MODERN,
        CONSOLE_TABLET_PLUS,
    ]