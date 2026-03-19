from manim import *
from fractions import Fraction

class ConversionTable(Scene):
    def construct(self):

        conversion_table_1 = Table(
            [["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]],
            row_labels=[Text("Encoding")],
            col_labels=[Text("A"), Text("B"), Text("C"), Text("D"), Text("E"), Text("F"), Text("G"), Text("H"), Text("I"), Text("J"), Text("K"), Text("L"), Text("M")])
        conversion_table_1.scale(0.4)

        conversion_table_2 = Table(
            [["13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]],
            row_labels=[Text("Encoding")],
            col_labels=[Text("N"), Text("O"), Text("P"), Text("Q"), Text("R"), Text("S"), Text("T"), Text("U"), Text("V"), Text("W"), Text("X"), Text("Y"), Text("Z")])
        conversion_table_2.scale(0.4)
        
        conversion_table_2.next_to(conversion_table_1, DOWN, buff=0.5)
        tables_group = VGroup(conversion_table_1, conversion_table_2)
        tables_group.move_to(ORIGIN)

        # Display the Table on screen
        self.play(Create(conversion_table_1), run_time=3)
        self.play(Create(conversion_table_2), run_time=3)
        self.wait(2)

class MatrixMultiplication(MovingCameraScene):
    def construct(self):
        def tex_number(x):
            if isinstance(x, Fraction):
                if x.denominator == 1:
                    return str(x.numerator)
                return rf"\frac{{{x.numerator}}}{{{x.denominator}}}"
            return str(x)

        key_data = [
            [18, 17, 10],
            [4, 4, 4],
            [2, 19, 24]
        ]

        word_data = [
            [2, 5, 4, 8],
            [14, 8, 13, 0],
            [13, 3, 19, 11]
        ]

        key_matrix = Matrix(key_data).scale(0.8)
        word_matrix = Matrix(word_data).scale(0.8)

        key_matrix.next_to(word_matrix, LEFT, buff=0.5)

        equal_sign = MathTex("=")

        product_matrix = Matrix([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]).scale(0.8)

        product_matrix.get_entries().set_color(BLACK)

        equal_sign.next_to(word_matrix, RIGHT, buff=0.5)
        product_matrix.next_to(equal_sign, RIGHT, buff=0.5)

        # Labels
        key_label = Text("Key Matrix", font_size=24)
        word_label = Text("Word Matrix", font_size=24)

        group = VGroup(key_matrix, word_matrix, equal_sign, product_matrix)
        group.move_to(ORIGIN)
        key_label.next_to(key_matrix, DOWN)
        word_label.next_to(word_matrix, DOWN)

        # Show matrices
        self.play(Create(key_matrix))
        self.play(Create(word_matrix))
        self.play(Create(equal_sign))
        self.play(Create(product_matrix))
        self.play(FadeIn(key_label), FadeIn(word_label))

        # Dimensions
        rows = len(key_data)          # 3
        key_cols = len(key_data[0])   # 3
        word_cols = len(word_data[0]) # 4

        key_entries = key_matrix.get_entries()
        word_entries = word_matrix.get_entries()
        product_entries = product_matrix.get_entries()

        for i in range(rows):

            # Highlight row
            row_group = VGroup(
                *[key_entries[i * key_cols + j] for j in range(key_cols)]
            )

            row_highlight = SurroundingRectangle(row_group, color=RED, buff=0.15)
            self.play(Create(row_highlight), run_time=0.5)

            for j in range(word_cols):

                # Highlight column
                col_group = VGroup(
                    *[word_entries[k * word_cols + j] for k in range(rows)]
                )

                col_highlight = SurroundingRectangle(col_group, color=BLUE, buff=0.15)
                self.play(Create(col_highlight), run_time=0.5)

                # Compute dot product
                cell_value = sum(
                    key_data[i][k] * word_data[k][j]
                    for k in range(key_cols)
                )

                # Product cell
                cell = product_entries[i * word_cols + j]

                # Show multiplication expression
                multiplication = MathTex(
                    f"{key_data[i][0]}", r"\cdot", f"{word_data[0][j]}", "+",
                    f"{key_data[i][1]}", r"\cdot", f"{word_data[1][j]}", "+",
                    f"{key_data[i][2]}", r"\cdot", f"{word_data[2][j]}"
                ).scale(0.8)

                # Color row vs column
                multiplication[0].set_color(RED)
                multiplication[4].set_color(RED)
                multiplication[8].set_color(RED)

                multiplication[2].set_color(BLUE)
                multiplication[6].set_color(BLUE)
                multiplication[10].set_color(BLUE)

                multiplication.next_to(equal_sign, UP, buff=2)

                self.play(FadeIn(multiplication))
                self.wait(0.15)

                # Fill product cell
                new_text = Text(str(cell_value), font_size=28).move_to(cell.get_center())

                self.play(FadeIn(new_text), run_time=0.5)

                self.play(FadeOut(multiplication), run_time=0.1)
                self.play(FadeOut(col_highlight), run_time=0.5)

            self.play(FadeOut(row_highlight), run_time=0.5)

        # Final zoom
        self.play(
            FadeOut(key_label),
            FadeOut(word_label),
            FadeOut(equal_sign),
            FadeOut(key_matrix),
            FadeOut(word_matrix)
        )

        self.play(
            self.camera.frame.animate
            .move_to(product_matrix)
            .set(width=product_matrix.width * 2),
            run_time=2
        )
        
        # Column-wise indices
        ordered_indices = []
        for j in range(word_cols):
            for i in range(rows):
                ordered_indices.append((i,j))  # store (row,col) instead of flat index

        # Create final entries with actual values
        final_values = [
            MathTex(tex_number(sum(key_data[i][k] * word_data[k][j] for k in range(key_cols)))).set_color(WHITE)
            for (i,j) in ordered_indices
        ]

        # Arrange as a single horizontal string (scale down if needed)
        final_group = VGroup(*final_values).arrange(RIGHT, buff=0.4).scale(0.4)
        final_group.next_to(product_matrix, DOWN, buff=0.7)

        encrypted_label = Text("Encrypted Message:", font_size=24, color=WHITE)
        encrypted_label.next_to(final_group, UP, buff=0.2)

        # Animate
        self.play(
            *[TransformFromCopy(product_entries[i * word_cols + j], final_values[k])
            for k,(i,j) in enumerate(ordered_indices)],
            FadeIn(encrypted_label),
            run_time=2
        )

class InverseMatrixMultiplication(MovingCameraScene):
    def construct(self):
        def tex_number(x):
            if isinstance(x, Fraction):
                if x.denominator == 1:
                    return str(x.numerator)
                return rf"\frac{{{x.numerator}}}{{{x.denominator}}}"
            return str(x)

        key_inverse = [
            [Fraction(-5,114), Fraction(109,228), Fraction(-7,114)],
            [Fraction(11,57), Fraction(-103,114), Fraction(4,57)],
            [Fraction(-17,114), Fraction(77,114), Fraction(-1,114)]
        ]

        message = [
            [404, 256, 483, 254],
            [116, 64, 144, 76],
            [582, 234, 711, 280]
        ]

        key_inverse_matrix = Matrix(
            key_inverse,
            v_buff=1.5,
            element_to_mobject=lambda x: MathTex(tex_number(x)).scale(0.8)
        ).scale(0.8)

        encrypted_message_matrix = Matrix(message).scale(0.8)

        key_inverse_matrix.next_to(encrypted_message_matrix, LEFT, buff=0.5)

        equal_sign = MathTex("=")

        product_matrix = Matrix(
            [[0 for _ in range(4)] for _ in range(3)],
            element_to_mobject=lambda x: MathTex(str(x))
        ).scale(0.8)

        product_matrix.get_entries().set_color(BLACK)

        equal_sign.next_to(encrypted_message_matrix, RIGHT, buff=0.5)
        product_matrix.next_to(equal_sign, RIGHT, buff=0.5)

        key_label = Text("Key Inverse Matrix", font_size=24)
        encrypted_message_label = Text("Encrypted Message Matrix", font_size=24)

        group = VGroup(
            key_inverse_matrix,
            encrypted_message_matrix,
            equal_sign,
            product_matrix
        )

        group.move_to(ORIGIN)

        key_label.next_to(key_inverse_matrix, DOWN)
        encrypted_message_label.next_to(encrypted_message_matrix, DOWN)

        self.play(Create(key_inverse_matrix))
        self.play(Create(encrypted_message_matrix))
        self.play(Create(equal_sign))
        self.play(Create(product_matrix))
        self.play(FadeIn(key_label), FadeIn(encrypted_message_label))

        rows = len(key_inverse)
        key_cols = len(key_inverse[0])
        word_cols = len(message[0])

        key_entries = key_inverse_matrix.get_entries()
        word_entries = encrypted_message_matrix.get_entries()
        product_entries = product_matrix.get_entries()

        for i in range(rows):
            row_group = VGroup(
                *[key_entries[i * key_cols + j] for j in range(key_cols)]
            )

            row_highlight = SurroundingRectangle(
                row_group,
                color=RED,
                buff=0.15
            )

            self.play(Create(row_highlight), run_time=0.5)

            for j in range(word_cols):
                col_group = VGroup(
                    *[word_entries[k * word_cols + j] for k in range(rows)]
                )

                col_highlight = SurroundingRectangle(
                    col_group,
                    color=BLUE,
                    buff=0.15
                )

                self.play(Create(col_highlight), run_time=0.5)

                cell_value = sum(
                    key_inverse[i][k] * message[k][j]
                    for k in range(key_cols)
                )

                cell = product_entries[i * word_cols + j]

                multiplication = MathTex(
                    tex_number(key_inverse[i][0]), r"\cdot", str(message[0][j]), "+",
                    tex_number(key_inverse[i][1]), r"\cdot", str(message[1][j]), "+",
                    tex_number(key_inverse[i][2]), r"\cdot", str(message[2][j])
                ).scale(0.8)

                multiplication[0].set_color(RED)
                multiplication[4].set_color(RED)
                multiplication[8].set_color(RED)

                multiplication[2].set_color(BLUE)
                multiplication[6].set_color(BLUE)
                multiplication[10].set_color(BLUE)

                multiplication.next_to(equal_sign, UP, buff=2)

                self.play(FadeIn(multiplication))
                self.wait(0.15)

                result_tex = MathTex(tex_number(cell_value)).move_to(
                    cell.get_center()
                )

                self.play(FadeIn(result_tex), run_time=0.5)

                self.play(FadeOut(multiplication), run_time=0.1)
                self.play(FadeOut(col_highlight), run_time=0.5)

            self.play(FadeOut(row_highlight), run_time=0.5)

        self.play(
            FadeOut(key_label),
            FadeOut(encrypted_message_label),
            FadeOut(equal_sign),
            FadeOut(key_inverse_matrix),
            FadeOut(encrypted_message_matrix)
        )

        self.play(
            self.camera.frame.animate
            .move_to(product_matrix)
            .set(width=product_matrix.width * 2),
            run_time=2
        )

        # Column-wise indices
        ordered_indices = []
        for j in range(word_cols):
            for i in range(rows):
                ordered_indices.append((i,j))  # store (row,col) instead of flat index

        # Create final entries with actual values
        final_values = [
            MathTex(tex_number(sum(key_inverse[i][k] * message[k][j] for k in range(key_cols)))).set_color(WHITE)
            for (i,j) in ordered_indices
        ]

        # Arrange as a single horizontal string (scale down if needed)
        final_group = VGroup(*final_values).arrange(RIGHT, buff=0.4).scale(0.7)
        final_group.next_to(product_matrix, DOWN, buff=0.7)

        decrypted_label = Text("Decrypted Message:", font_size=24, color=WHITE)
        decrypted_label.next_to(final_group, UP, buff=0.2)

        # Animate
        self.play(
            *[TransformFromCopy(product_entries[i * word_cols + j], final_values[k])
            for k,(i,j) in enumerate(ordered_indices)],
            FadeIn(decrypted_label),
            run_time=2
        )

class InverseMatrix(Scene):
    def construct(self):
        self.title_label = Text("Finding the Inverse of the Key Matrix", font_size=20).to_edge(UP)
        self.play(Write(self.title_label))
        self.wait(0.1)

        self.current_stage = self.create_stage(
             to_latex_matrix([
                [18, 17, 10 , 1, 0, 0],
                [4, 4, 4, 0, 1, 0],
                [2, 19, 24, 0, 0, 1]
                ])
        )
        self.play(Create(self.current_stage))
        self.wait(.1)
        self.key_label = Text("Key         Identity", font_size=24)
        self.key_label.next_to(self.current_stage, DOWN)
        
        self.play(Write(self.key_label))
        self.wait(.1)

        self.play(FadeOut(self.title_label), FadeOut(self.key_label))

        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [4, 4, 4, 0, 1, 0],
                [2, 19, 24, 0, 0, 1]
                ],
            r"R_1 \rightarrow R_1 - 9R_3")

        self.wait(.1)
        
        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [4, 4, 4, 0, 1, 0],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_3 \rightarrow R_3 - \frac{1}{2} R_2")

        self.wait(.1)
        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [4, 0, Fraction(-20,17), 0, Fraction(19,17), Fraction(-4,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_2 \rightarrow R_2 - \frac{4}{17} R_3")

        self.wait(.1)
        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_2 / 4")

        self.wait(.1)
        self.rows(
            [[0, 0, Fraction(-114,17) , 1, Fraction(-77,17), Fraction(1,17)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_1 \rightarrow R_1 + \frac{154}{17} R_3")
            
        self.wait(.1)
        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_1 \rightarrow R_1 \cdot \left(-\frac{17}{114}\right)")

        self.wait(.1)
        
        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 0, Fraction(374,114), Fraction(-1751,114), Fraction(136,114)]
                ],
            r"R_3 \rightarrow R_3 - 22R_1")

        self.wait(.1)

        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)]
                ],
            r"R_3 / 17")

        self.wait(.1)

        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, 0, Fraction(-5,114), Fraction(109,228), Fraction(-7,114)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)]
                ],
            r"R_2 \rightarrow R_2 + 5/17R_1")

        self.wait(.1)

        self.rows(
            [[1, 0, 0, Fraction(-5,114), Fraction(109,228), Fraction(-7,114)],
                [0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)]
                ],
            r"R_1 \leftrightarrow R_2")

        self.wait(.1)
        self.rows([[1, 0, 0, Fraction(-5,114), Fraction(109,228), Fraction(-7,114)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)],
                [0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)]
                ],
            r"R_2 \leftrightarrow R_3")

        self.wait(.1)
        final_label = Text("Identity     Key Inverse", font_size=24)
        final_label.next_to(self.current_stage, DOWN, buff=0.5)
        self.play(Write(final_label))
        self.wait(.1)

    def create_stage(self, matrix):
        key_matrix = Matrix(
            matrix,
            h_buff=2.0,
            v_buff=1.4,
            element_to_mobject_config={"font_size": 34},
        )

        line = Line(
            key_matrix.get_columns()[2].get_top() +RIGHT*0.7,
            key_matrix.get_columns()[2].get_bottom() +RIGHT*0.7,
        )

        line.next_to(key_matrix.get_columns()[2], RIGHT, buff =0.5)
        return VGroup(key_matrix,line)

    def rows(self, matrix, row_operation):
        new_stage = self.create_stage(matrix)

        row_operations = MathTex(row_operation).next_to(self.current_stage, UP)

        if hasattr(self, "op"):
            self.play(FadeOut(self.op))
            
        self.play(Write(row_operations))
        self.play(Transform(self.current_stage, new_stage))

        self.op = row_operations
        
        self.wait(.1)


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


### Helper functions

## Helper functions for formatting
def frac_to_latex(x):
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        # fixing issues with negative fractions
        num, den = x.numerator, x.denominator
        if num < 0:
            return rf"-\frac{{{abs(num)}}}{{{den}}}"
        return rf"\frac{{{num}}}{{{den}}}"
    return str(x)

def to_latex_matrix(matrix):
    return [[frac_to_latex(x) for x in row] for row in matrix]

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