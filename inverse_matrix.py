from manim import *
from fractions import Fraction

### Helper functions for formatting
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

class InverseMatrix(Scene):
    def construct(self):
        self.title_label = Text("Finding the Inverse of the Key Matrix", font_size=20).to_edge(UP)
        self.play(Write(self.title_label))
        self.wait(0.5)

        self.current_stage = self.create_stage(
             to_latex_matrix([
                [18, 17, 10 , 1, 0, 0],
                [4, 4, 4, 0, 1, 0],
                [2, 19, 24, 0, 0, 1]
                ])
        )
        self.play(Create(self.current_stage))
        self.wait()
        self.key_label = Text("Key         Identity", font_size=24)
        self.key_label.next_to(self.current_stage, DOWN)
        
        self.play(Write(self.key_label))
        self.wait()

        self.play(FadeOut(self.title_label), FadeOut(self.key_label))

        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [4, 4, 4, 0, 1, 0],
                [2, 19, 24, 0, 0, 1]
                ],
            r"R_1 \rightarrow R_1 - 9R_3")

        self.wait(.5)
        
        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [4, 4, 4, 0, 1, 0],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_3 \rightarrow R_3 - \frac{1}{2} R_2")

        self.wait(.5)
        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [4, 0, Fraction(-20,17), 0, Fraction(19,17), Fraction(-4,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_2 \rightarrow R_2 - \frac{4}{17} R_3")

        self.wait(.5)
        self.rows(
            [[0, -154, -206 , 1, 0, -9],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_2 / 4")

        self.wait(.5)
        self.rows(
            [[0, 0, Fraction(-114,17) , 1, Fraction(-77,17), Fraction(1,17)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_1 \rightarrow R_1 + \frac{154}{17} R_3")
            
        self.wait(.5)
        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 22, 0, Fraction(-1,2), 1]
                ],
            r"R_1 \rightarrow R_1 \cdot \left(-\frac{17}{114}\right)")

        self.wait(.5)
        
        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 17, 0, Fraction(374,114), Fraction(-1751,114), Fraction(136,114)]
                ],
            r"R_3 \rightarrow R_3 - 22R_1")

        self.wait(.5)

        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, Fraction(-5,17), 0, Fraction(19,68), Fraction(-1,17)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)]
                ],
            r"R_3 / 17")

        self.wait(.5)

        self.rows(
            [[0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [1, 0, 0, Fraction(-5,114), Fraction(109,228), Fraction(-7,114)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)]
                ],
            r"R_2 \rightarrow R_2 + 5/17R_1")

        self.wait(.5)

        self.rows(
            [[1, 0, 0, Fraction(-5,114), Fraction(109,228), Fraction(-7,114)],
                [0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)]
                ],
            r"R_1 \leftrightarrow R_2")

        self.wait(.5)
        self.rows([[1, 0, 0, Fraction(-5,114), Fraction(109,228), Fraction(-7,114)],
                [0, 1, 0, Fraction(11,57), Fraction(-103,114), Fraction(4,57)],
                [0, 0, 1 , Fraction(-17,114), Fraction(77,114), Fraction(-1,114)]
                ],
            r"R_2 \leftrightarrow R_3")
        

        self.wait(1)
        final_label = Text("Identity     Key Inverse", font_size=24)
        final_label.next_to(self.current_stage, DOWN, buff=0.5)
        self.play(Write(final_label))
        self.wait(2)

    def create_stage(self, matrix):
        key_matrix = Matrix(
            matrix,
            h_buff=2.0,
            v_buff=1.4,
            element_to_mobject_config={"font_size": 34},
        )

        # key_matrix = Matrix(matrix)
        

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
        
        self.wait()
