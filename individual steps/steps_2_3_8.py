from manim import *

def letter_to_number(ch: str) -> int:
    return ord(ch.upper()) - ord("A")

def number_to_letter(n: int) -> str:
    return chr((n % 26) + ord("A"))

def create_matrix_brackets(target: Mobject, width: float = 0.3) -> tuple[VGroup, VGroup]:
    half_height = target.height / 2

    # Left bracket
    left_vertical = Line(UP * half_height, DOWN * half_height)
    left_top = Line(UP * half_height, UP * half_height + RIGHT * width)
    left_bottom = Line(DOWN * half_height, DOWN * half_height + RIGHT * width)
    left_bracket = VGroup(left_vertical, left_top, left_bottom)

    # Right bracket
    right_vertical = Line(UP * half_height, DOWN * half_height)
    right_top = Line(UP * half_height, UP * half_height + LEFT * width)
    right_bottom = Line(DOWN * half_height, DOWN * half_height + LEFT * width)
    right_bracket = VGroup(right_vertical, right_top, right_bottom)

    left_bracket.next_to(target, LEFT, buff=0.25)
    right_bracket.next_to(target, RIGHT, buff=0.25)

    return left_bracket, right_bracket


class TextToMatrixScene(Scene):
    """
    1. Showing a word/key
    2. Converting each letter to a number
    3. Filling a matrix column-by-column
    """

    source_text = ""
    intro_label = ""
    matrix_label = ""
    matrix_size = ""

    # Animation/layout tuning
    letter_buff = 0.35
    number_buff = 0.45
    letter_lag = 0.08
    arrow_lag = 0.06
    number_lag = 0.08

    def construct(self):
        self.show_intro_text(self.source_text, self.intro_label)
        values, number_row = self.show_conversion(self.source_text)
        self.show_matrix_fill(values, number_row)
        self.wait(2)

    def show_intro_text(self, text: str, label: str):
        # Display the original word/key
        title = Text(f"{label} is {text}", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

    def show_conversion(self, text: str):
        # Show letters, numeric values, and animate arrows from letters to numbers.

        title = Text(f"Convert {text} using conversion table", font_size=36).to_edge(UP)

        letters = VGroup(
            *[Text(ch, font_size=34, color=BLUE) for ch in text]
        ).arrange(RIGHT, buff=self.letter_buff)

        values = [letter_to_number(ch) for ch in text]
        numbers = VGroup(
            *[Text(str(value), font_size=34, color=GREEN) for value in values]
        ).arrange(RIGHT, buff=self.number_buff)

        letters.next_to(title, DOWN, buff=0.8)
        numbers.next_to(letters, DOWN, buff=0.8)

        arrows = VGroup(*[
            Arrow(
                letters[i].get_bottom(),
                numbers[i].get_top(),
                buff=0.1,
                stroke_width=2,
            )
            for i in range(len(text))
        ])

        self.play(Write(title))
        self.play(
            LaggedStart(
                *[FadeIn(letter, shift=UP) for letter in letters],
                lag_ratio=self.letter_lag,
            )
        )
        self.play(
            LaggedStart(
                *[GrowArrow(arrow) for arrow in arrows],
                lag_ratio=self.arrow_lag,
            )
        )
        self.play(
            LaggedStart(
                *[FadeIn(number, shift=DOWN) for number in numbers],
                lag_ratio=self.number_lag,
            )
        )
        self.wait(1)

        self.play(FadeOut(title), FadeOut(letters), FadeOut(arrows))
        self.play(numbers.animate.to_edge(UP))

        return values, numbers

    def show_matrix_fill(self, values: list[int], number_row: VGroup):
        # Animate the numbers into a 3×n matrix. Top-to-bottom, then left-to-right.

        cols = len(values) // 3

        title = Text(f"Put into {self.matrix_size} matrix", font_size=36)
        title.next_to(number_row, DOWN, buff=0.6)

        col_spacing = 1.2
        row_spacing = 0.9

        # Invisible anchor points for each matrix entry.
        positions = VGroup(*[
            Dot(radius=0).move_to([
                (col - (cols - 1) / 2) * col_spacing,
                (1 - row) * row_spacing,
                0,
            ])
            for col in range(cols)
            for row in range(3)
        ])
        positions.next_to(title, DOWN, buff=1.0)

        left_bracket, right_bracket = create_matrix_brackets(positions)

        label = MathTex(self.matrix_label, "=")
        label.next_to(left_bracket, LEFT, buff=0.25)

        self.play(Write(title))
        self.play(FadeIn(label), FadeIn(left_bracket), FadeIn(right_bracket))

        # Move each number into the matrix one at a time.
        for i, value in enumerate(values):
            moving_num = number_row[i].copy()
            target_num = Text(str(value), font_size=34, color=GREEN)
            target_num.move_to(positions[i].get_center())

            self.add(moving_num)
            self.play(Transform(moving_num, target_num), run_time=0.45)

        self.play(FadeOut(number_row))


class KeyToMatrix(TextToMatrixScene):
    source_text = "SECRETKEY"
    intro_label = "Key"
    matrix_label = "A"
    matrix_size = "3x3"

    # Spacing
    letter_buff = 0.35
    number_buff = 0.45
    letter_lag = 0.08
    arrow_lag = 0.06
    number_lag = 0.08


class MessageToMatrix(TextToMatrixScene):
    source_text = "CONFIDENTIAL"
    intro_label = "Word"
    matrix_label = "W"
    matrix_size = "3xn"

    # Spacing
    letter_buff = 0.28
    number_buff = 0.35
    letter_lag = 0.06
    arrow_lag = 0.04
    number_lag = 0.06


class GetOriginalMessage(Scene):
    def construct(self):
        values = [2, 14, 13, 5, 8, 3, 4, 13, 19, 8, 0, 11]
        self.convert_back(values)
        self.wait(2)

    def convert_back(self, values: list[int]):
        title = Text("Convert using conversion table", font_size=36).to_edge(UP)

        numbers = VGroup(
            *[Text(str(v), font_size=34, color=GREEN) for v in values]
        ).arrange(RIGHT, buff=0.35)

        letters = VGroup(
            *[Text(number_to_letter(v), font_size=34, color=BLUE) for v in values]
        ).arrange(RIGHT, buff=0.35)

        numbers.next_to(title, DOWN, buff=0.8)
        letters.next_to(numbers, DOWN, buff=0.8)

        arrows = VGroup(*[
            Arrow(
                numbers[i].get_bottom(),
                letters[i].get_top(),
                buff=0.1,
                stroke_width=2,
            )
            for i in range(len(values))
        ])

        recovered_word = "".join(number_to_letter(v) for v in values)
        word_text = Text(recovered_word, font_size=42, color=YELLOW)
        word_text.next_to(letters, DOWN, buff=1.0)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(num, shift=DOWN) for num in numbers], lag_ratio=0.06))
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.04))
        self.play(LaggedStart(*[FadeIn(letter, shift=UP) for letter in letters], lag_ratio=0.06))
        self.wait(0.5)
        self.play(Write(word_text))