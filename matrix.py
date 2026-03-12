from manim import *

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
        self.wait(0.5)
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
            self.play(Create(row_highlight))

            for j in range(word_cols):

                # Highlight column
                col_group = VGroup(
                    *[word_entries[k * word_cols + j] for k in range(rows)]
                )

                col_highlight = SurroundingRectangle(col_group, color=BLUE, buff=0.15)
                self.play(Create(col_highlight))

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
                self.wait(0.2)

                # Fill product cell
                new_text = Text(str(cell_value), font_size=28).move_to(cell.get_center())

                self.play(FadeIn(new_text))

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
            .set(width=product_matrix.width * 1.5),
            run_time=2
        )