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