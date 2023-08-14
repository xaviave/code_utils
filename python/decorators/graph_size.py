import pandas as pd


def graph_size(slice_size: int, slice_column: str):
    """
    Allow abstract slicing of dataframe following parameters to avoid unreadable graphs

    Parameters
    ----------
    slice_size: number of graphs displayed on the same figure
    slice_column: column name where the dataframe will be sliced

    Examples
    --------

    class Visualizer:
        graph_instances: list

        def __init__(self):
            graph_instances = []

        def _visualize(p: p9.ggplot, title: str):
            \"""
            Default visualize function with predefined theme and handle the visualization and file saving
            Save plot in graph_instance to do a batch drawing
            \"""
            self.graph_instances.append(
                p
                + p9.ggtitle(title)
                + p9.theme(
                    figure_size=(20, 20),
                    plot_title=p9.element_text(size=18, face="bold"),
                    text=p9.element_text(size=10),
                    axis_text_x=p9.element_text(colour="black", size=6),
                    axis_text_y=p9.element_text(colour="black", size=6),
                    panel_spacing=0.5,
                )
            )

        @graph_size(4, "col1")
        def visualize_global_data(self, data: pd.DataFrame, title_name: str = "EXAMPLE"):
            \"""
            visualize 4 graphs per figure
            \"""
             p = (
                 p9.ggplot(data, mapping=p9.aes(x="X", y="Y"))
                 + p9.geom_line(color="red")
                 + p9.facet_wrap("NAME", scales="free", ncol=4)
                 + p9.theme(subplots_adjust={"top": 0.95, "bottom": 0.06, "wspace": 0.5, "hspace": 0.5})
             )
             self._visualize(p, title=f"{title_name} over X & Y")

    def main():
        d = {'col1': [1, 2, 3, 4, 5, 6], 'col2': [3, 4, 5, 6, 7, 8]}
        df = pd.DataFrame(data=d)

        v = Visualizer()
        # will iterate two times over 'col1'
        v.visualize_global_data(d, "name")

        # Generate the graph in different window
        for p in v.graph_instances:
            p.draw()

        # Save graphs in PDF
        p9.save_as_pdf_pages(self.graph_instances[::-1], "path.pdf")
    """

    def _graph_size(func):
        def wrapper(*args, **kwargs):
            c_list = pd.unique(args[1][slice_column])
            _args = list(args)
            for n in range(0, len(c_list), slice_size):
                _args[1] = args[1][args[1][slice_column].isin(c_list[n : n + slice_size])]
                func(*_args, **kwargs)

        return wrapper

    return _graph_size
