from manim import *

class MatrixExamples(Scene):
    def construct(self):
        # Define a 2x2 matrix
        matrix = Matrix([
            [1, 2],
            [3, 4]
        ])
        
        # Display the matrix on screen
        self.play(Create(matrix))
        self.wait(2)