import math

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


# -----------------------------
# BASIC CALCULATOR
# -----------------------------

def clean_text(text):
    text = text.lower().strip()

    replacements = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "times": "*",
        "multiply": "*",
        "multiplied by": "*",
        "divide": "/",
        "divided by": "/",
        "over": "/",
        "mod": "%",
        "modulus": "%",
        "power": "**",
        "x": "*",
    }

    for word, symbol in replacements.items():
        text = text.replace(word, symbol)

    return text


def basic_calc(text):
    text = clean_text(text)

    allowed = set(
        "0123456789+-*/().% "
    )

    if not all(ch in allowed for ch in text):
        raise ValueError("Invalid characters in expression")

    if not text:
        raise ValueError("Enter a calculation")

    return eval(text, {"__builtins__": None}, {})


# -----------------------------
# SCIENTIFIC CALCULATOR
# -----------------------------

def scientific_calc(text):
    p = clean_text(text).split()

    if not p:
        raise ValueError("Enter a scientific command")

    cmd = p[0]

    # power 2 5
    if cmd == "power":
        if len(p) != 3:
            raise ValueError("Example: power 2 5")

        a = float(p[1])
        b = float(p[2])

        return a ** b

    # modulus 10 3
    if cmd == "modulus":
        if len(p) != 3:
            raise ValueError("Example: modulus 10 3")

        a = float(p[1])
        b = float(p[2])

        return a % b

    if len(p) != 2:
        raise ValueError(
            "Example: sqrt 144 or sin 30"
        )

    x = float(p[1])

    if cmd == "sin":
        return math.sin(math.radians(x))

    if cmd == "cos":
        return math.cos(math.radians(x))

    if cmd == "tan":
        return math.tan(math.radians(x))

    if cmd == "sqrt":
        if x < 0:
            raise ValueError(
                "Negative square root is not real"
            )
        return math.sqrt(x)

    if cmd == "square":
        return x ** 2

    if cmd == "cube":
        return x ** 3

    if cmd == "exponential":
        return math.exp(x)

    if cmd == "log":
        if x <= 0:
            raise ValueError(
                "Log value must be positive"
            )
        return math.log10(x)

    if cmd == "ln":
        if x <= 0:
            raise ValueError(
                "Ln value must be positive"
            )
        return math.log(x)

    if cmd == "factorial":
        if x < 0 or x != int(x):
            raise ValueError(
                "Factorial needs a non-negative integer"
            )
        return math.factorial(int(x))

    raise ValueError(
        "Unknown scientific command"
    )


# -----------------------------
# APP
# -----------------------------

class SpeakToCalsi(App):

    def build(self):

        self.mode = "Basic"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(7)
        )

        # TITLE
        title = Label(
            text="[b]SPEAK TO CALSI[/b]",
            markup=True,
            font_size=dp(25),
            size_hint_y=None,
            height=dp(50)
        )

        root.add_widget(title)

        # STATUS
        self.status = Label(
            text="Ready • Tap MIC or type below",
            font_size=dp(14),
            size_hint_y=None,
            height=dp(35)
        )

        root.add_widget(self.status)

        # INPUT
        self.input = TextInput(
            hint_text="Say or type: 25 plus 10",
            multiline=False,
            font_size=dp(20),
            size_hint_y=None,
            height=dp(55)
        )

        root.add_widget(self.input)

        # ANSWER
        self.answer = Label(
            text="Answer: --",
            font_size=dp(24),
            size_hint_y=None,
            height=dp(55)
        )

        root.add_widget(self.answer)

        # MAIN BUTTONS
        g = GridLayout(
            cols=2,
            spacing=dp(7),
            size_hint_y=None,
            height=dp(110)
        )

        self.add_btn(
            g,
            "🎤 SPEAK",
            self.voice
        )

        self.add_btn(
            g,
            "CALCULATE",
            self.calculate
        )

        self.add_btn(
            g,
            "CLEAR",
            self.clear
        )

        root.add_widget(g)

        # MODE BUTTONS
        modes = GridLayout(
            cols=3,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(55)
        )

        for m in ("Basic", "Scientific", "Matrix"):
            self.add_btn(
                modes,
                m,
                lambda x, mm=m: self.set_mode(mm)
            )

        root.add_widget(modes)

        # HISTORY
        sv = ScrollView()

        self.history = Label(
            text="History:",
            halign="left",
            valign="top",
            size_hint_y=None,
            font_size=dp(15)
        )

        self.history.bind(
            texture_size=self.history.setter("size")
        )

        sv.add_widget(self.history)
        root.add_widget(sv)

        return root

    # -----------------------------
    # BUTTON CREATOR
    # -----------------------------

    def add_btn(self, parent, text, fn):

        b = Button(
            text=text,
            font_size=dp(16)
        )

        b.bind(on_press=fn)

        parent.add_widget(b)

    # -----------------------------
    # MODE
    # -----------------------------

    def set_mode(self, m):

        self.mode = m

        self.status.text = f"Mode: {m}"

        if m == "Basic":

            self.input.hint_text = (
                "Try: 25 plus 10"
            )

        elif m == "Scientific":

            self.input.hint_text = (
                "Try: sqrt 144 or sin 30"
            )

        else:

            self.input.hint_text = (
                "Matrix mode: use matrix commands"
            )

    # -----------------------------
    # CLEAR
    # -----------------------------

    def clear(self, *args):

        self.input.text = ""

        self.answer.text = "Answer: --"

        self.status.text = (
            f"Mode: {self.mode}"
        )

    # -----------------------------
    # CALCULATE
    # -----------------------------

    def calculate(self, *args):

        t = self.input.text.strip()

        if not t:
            self.status.text = (
                "Please enter a calculation"
            )
            return

        try:

            if self.mode == "Basic":

                r = basic_calc(t)

            elif self.mode == "Scientific":

                r = scientific_calc(t)

            else:

                raise ValueError(
                    "Matrix mode is not available yet"
                )

            # Remove .0 for integer answers
            if isinstance(r, float) and r.is_integer():
                r = int(r)

            # SHOW ANSWER ON SCREEN ONLY
            self.answer.text = f"Answer: {r}"

            self.status.text = (
                "Calculation successful"
            )

            self.history.text += (
                f"\n{t} = {r}"
            )

        except Exception as e:

            self.answer.text = "Answer: Error"

            self.status.text = str(e)

    # -----------------------------
    # SPEAK BUTTON
    # -----------------------------

    def voice(self, *args):

        # This does NOT speak the answer.
        # It simply opens the Android keyboard
        # so that the user can use the keyboard
        # microphone for speech-to-text.

        self.status.text = (
            "Tap the 🎤 microphone on the keyboard, "
            "then speak."
        )

        self.input.focus = True

        self.input.cursor = (
            len(self.input.text), 0
        )


# -----------------------------
# START APP
# -----------------------------

SpeakToCalsi().run()
