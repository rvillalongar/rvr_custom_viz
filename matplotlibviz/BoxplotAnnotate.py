
class BoxplotAnnotate():
    def __init__(self) -> None:
        return 


    def box_annotate(name: str,
                    boxpdict: dict,
                    field_dict: str,
                    y_offset: float,
                    x_loc: int = 0,
                    x_offset_string: float = 0.1,
                    y_offset_string: float = 0.1):
        """
        ejemplo de 
        http://blog.rtwilson.com/automatically-annotating-a-boxplot-in-matplotlib/
        """
        # el xloc + 1 coloca el punto x en el primer boxplot como referencia 1 no 0

        ax.annotate(
            name,
            xy=(x_loc + 1, y_offset + bpdict[field_dict][x_loc].get_ydata()[0]),
            xytext=(
                x_loc + 1 + x_offset_string,
                y_offset_string + bpdict[field_dict][x_loc].get_ydata()[0]
            ),
            arrowprops={'arrowstyle': '->', 'color': 'gray'}
        )
