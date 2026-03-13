from manim import *

class KeyToMatrix(Scene):
    def construct(self):
        key = "SECRETKEY"

        self.show_key(key)
        values, number_row = self.show_conversion(key)
        self.show_matrix_fill(values, number_row)

        self.wait(2)

    def letter_to_number(self, ch: str) -> int:
        return ord(ch.upper()) - ord("A")

    def show_key(self, key: str):
        title = Text(f"Key is {key}", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

    def show_conversion(self, key: str):
        title = Text("Convert SECRETKEY using conversion table", font_size=36).to_edge(UP)

        letters = VGroup(*[
            Text(ch, font_size=34, color=BLUE) for ch in key
        ]).arrange(RIGHT, buff=0.35)

        numbers = VGroup(*[
            Text(str(self.letter_to_number(ch)), font_size=34, color=GREEN)
            for ch in key
        ]).arrange(RIGHT, buff=0.45)

        letters.next_to(title, DOWN, buff=0.8)
        numbers.next_to(letters, DOWN, buff=0.8)

        arrows = VGroup(*[
            Arrow(
                letters[i].get_bottom(),
                numbers[i].get_top(),
                buff=0.1,
                stroke_width=2
            )
            for i in range(len(key))
        ])

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(letter, shift=UP) for letter in letters], lag_ratio=0.08))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06))
        self.play(LaggedStart(*[FadeIn(num, shift=DOWN) for num in numbers], lag_ratio=0.08))
        self.wait(1)

        values = [self.letter_to_number(ch) for ch in key]

        self.play(FadeOut(title), FadeOut(letters), FadeOut(arrows))
        self.play(numbers.animate.to_edge(UP))

        return values, numbers

    def show_matrix_fill(self, values, number_row: VGroup):
        title = Text("Put into 3×3 matrix", font_size=36)
        title.next_to(number_row, DOWN, buff=0.6)

        # Invisible 3x3 positions for the matrix entries
        positions = VGroup(*[
            Dot(radius=0).move_to([
                (i % 3 - 1) * 1.2,
                (1 - i // 3) * 0.9,
                0
            ])
            for i in range(9)
        ])
        positions.next_to(title, DOWN, buff=1.0)

        # Brackets around the imaginary matrix area
        left_bracket, right_bracket = create_matrix_brackets(positions)
        label = MathTex("A", "=")
        label.next_to(left_bracket, LEFT, buff=0.25)

        self.play(Write(title))
        self.play(FadeIn(label), FadeIn(left_bracket), FadeIn(right_bracket))

        placed_numbers = VGroup()

        # Fill left to right first, then top to bottom
        for i, value in enumerate(values):
            moving_num = number_row[i].copy()
            target_num = Text(str(value), font_size=34, color=GREEN)
            target_num.move_to(positions[i].get_center())

            self.add(moving_num)
            self.play(Transform(moving_num, target_num), run_time=0.5)
            placed_numbers.add(moving_num)

        self.play(FadeOut(number_row))

class MessageToMatrix(Scene):
    def construct(self):
        word = "CONFIDENTIAL"

        self.show_word(word)
        values, number_row = self.show_conversion(word)
        self.show_matrix_fill(values, number_row)

        self.wait(2)

    def letter_to_number(self, ch: str) -> int:
        return ord(ch.upper()) - ord("A")

    def show_word(self, word: str):
        title = Text(f"Word is {word}", font_size=42)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

    def show_conversion(self, word: str):
        title = Text(f"Convert {word} using conversion table", font_size=36).to_edge(UP)

        letters = VGroup(*[
            Text(ch, font_size=34, color=BLUE) for ch in word
        ]).arrange(RIGHT, buff=0.28)

        numbers = VGroup(*[
            Text(str(self.letter_to_number(ch)), font_size=34, color=GREEN)
            for ch in word
        ]).arrange(RIGHT, buff=0.35)

        letters.next_to(title, DOWN, buff=0.8)
        numbers.next_to(letters, DOWN, buff=0.8)

        arrows = VGroup(*[
            Arrow(
                letters[i].get_bottom(),
                numbers[i].get_top(),
                buff=0.1,
                stroke_width=2
            )
            for i in range(len(word))
        ])

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(letter, shift=UP) for letter in letters], lag_ratio=0.06))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.04))
        self.play(LaggedStart(*[FadeIn(num, shift=DOWN) for num in numbers], lag_ratio=0.06))
        self.wait(1)

        values = [self.letter_to_number(ch) for ch in word]

        self.play(FadeOut(title), FadeOut(letters), FadeOut(arrows))
        self.play(numbers.animate.to_edge(UP))

        return values, numbers

    def show_matrix_fill(self, values, number_row: VGroup):
        cols = len(values) // 3
        title = Text("Put into 3×n matrix", font_size=36)
        title.next_to(number_row, DOWN, buff=0.6)

        col_spacing = 1.2
        row_spacing = 0.9

        positions = VGroup(*[
            Dot(radius=0).move_to([
                (c - (cols - 1) / 2) * col_spacing,
                (1 - r) * row_spacing,
                0
            ])
            for c in range(cols)
            for r in range(3)
        ])
        positions.next_to(title, DOWN, buff=1.0)

        left_bracket, right_bracket = create_matrix_brackets(positions)

        label = MathTex("W", "=")
        label.next_to(left_bracket, LEFT, buff=0.25)

        self.play(Write(title))
        self.play(FadeIn(label), FadeIn(left_bracket), FadeIn(right_bracket))

        placed_numbers = VGroup()

        # Fill top to bottom first, then left to right
        for i, value in enumerate(values):
            moving_num = number_row[i].copy()
            target_num = Text(str(value), font_size=34, color=GREEN)
            target_num.move_to(positions[i].get_center())

            self.add(moving_num)
            self.play(Transform(moving_num, target_num), run_time=0.45)
            placed_numbers.add(moving_num)

        self.play(FadeOut(number_row))

def create_matrix_brackets(target, width=0.3):
    h = target.height / 2

    # Left bracket
    left_v = Line(UP*h, DOWN*h)
    left_t = Line(UP*h, UP*h + RIGHT*width)
    left_b = Line(DOWN*h, DOWN*h + RIGHT*width)

    left = VGroup(left_v, left_t, left_b)

    # Right bracket
    right_v = Line(UP*h, DOWN*h)
    right_t = Line(UP*h, UP*h + LEFT*width)
    right_b = Line(DOWN*h, DOWN*h + LEFT*width)

    right = VGroup(right_v, right_t, right_b)

    left.next_to(target, LEFT, buff=0.25)
    right.next_to(target, RIGHT, buff=0.25)

    return left, right

class GetOriginalMessage(Scene):
    def construct(self):
        values = [2, 14, 13, 5, 8, 3, 4, 13, 19, 8, 0, 11]

        self.convert_back(values)

        self.wait(2)

    def number_to_letter(self, n: int) -> str:
        return chr((n % 26) + ord("A"))

    def convert_back(self, values):
        title = Text("Convert using conversion table", font_size=36).to_edge(UP)

        numbers = VGroup(*[
            Text(str(v), font_size=34, color=GREEN) for v in values
        ]).arrange(RIGHT, buff=0.35)

        letters = VGroup(*[
            Text(self.number_to_letter(v), font_size=34, color=BLUE) for v in values
        ]).arrange(RIGHT, buff=0.35)

        numbers.next_to(title, DOWN, buff=0.8)
        letters.next_to(numbers, DOWN, buff=0.8)

        arrows = VGroup(*[
            Arrow(
                numbers[i].get_bottom(),
                letters[i].get_top(),
                buff=0.1,
                stroke_width=2
            )
            for i in range(len(values))
        ])

        word_text = Text("CONFIDENTIAL", font_size=42, color=YELLOW)
        word_text.next_to(letters, DOWN, buff=1.0)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(num, shift=DOWN) for num in numbers], lag_ratio=0.06))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.04))
        self.play(LaggedStart(*[FadeIn(letter, shift=UP) for letter in letters], lag_ratio=0.06))
        self.wait(0.5)

        self.play(Write(word_text))