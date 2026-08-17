import math

from game.settings import HEIGHT, WIDTH


ACTIONS = ("triangle", "circle", "square", "cross")


class MobileInput:
    JOYSTICK_CENTER = (95, HEIGHT - 105)
    JOYSTICK_HIT_RADIUS = 58
    JOYSTICK_TRAVEL = 30
    BUTTON_RADIUS = 32

    def __init__(self):
        center_x = WIDTH - 130
        center_y = HEIGHT - 120
        self.button_centers = {
            "triangle": (center_x, center_y - 48),
            "circle": (center_x + 48, center_y),
            "square": (center_x - 48, center_y),
            "cross": (center_x, center_y + 48),
        }
        self.reset()

    def reset(self):
        self.joystick_touch_id = None
        self.joystick_vector = (0.0, 0.0)
        self.active_touches = {}

    @property
    def pressed_actions(self):
        return {
            target
            for target in self.active_touches.values()
            if target in ACTIONS
        }

    @property
    def joystick_knob_position(self):
        x, y = self.JOYSTICK_CENTER
        dx, dy = self.joystick_vector
        return (
            int(x + dx * self.JOYSTICK_TRAVEL),
            int(y + dy * self.JOYSTICK_TRAVEL),
        )

    def pointer_down(self, pointer_id, position, action_callback):
        if pointer_id in self.active_touches:
            return False

        action = self._action_at(position)
        if action:
            self.active_touches[pointer_id] = action
            action_callback(action)
            return True

        if self.joystick_touch_id is None and self._inside_circle(
            position, self.JOYSTICK_CENTER, self.JOYSTICK_HIT_RADIUS
        ):
            self.joystick_touch_id = pointer_id
            self.active_touches[pointer_id] = "joystick"
            self._update_joystick(position)
            return True

        return False

    def pointer_motion(self, pointer_id, position):
        if pointer_id != self.joystick_touch_id:
            return False
        self._update_joystick(position)
        return True

    def pointer_up(self, pointer_id):
        target = self.active_touches.pop(pointer_id, None)
        if target == "joystick":
            self.joystick_touch_id = None
            self.joystick_vector = (0.0, 0.0)
        return target is not None

    def _action_at(self, position):
        for action, center in self.button_centers.items():
            if self._inside_circle(position, center, self.BUTTON_RADIUS):
                return action
        return None

    def _update_joystick(self, position):
        center_x, center_y = self.JOYSTICK_CENTER
        dx = position[0] - center_x
        dy = position[1] - center_y
        distance = math.hypot(dx, dy)
        if distance > self.JOYSTICK_HIT_RADIUS:
            scale = self.JOYSTICK_HIT_RADIUS / distance
            dx *= scale
            dy *= scale
        self.joystick_vector = (
            dx / self.JOYSTICK_HIT_RADIUS,
            dy / self.JOYSTICK_HIT_RADIUS,
        )

    @staticmethod
    def _inside_circle(position, center, radius):
        dx = position[0] - center[0]
        dy = position[1] - center[1]
        return dx * dx + dy * dy <= radius * radius
