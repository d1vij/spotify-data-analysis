import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Plots:
    @staticmethod
    def plot_1(obj: pd.Series, rows, title, xlabel, ylabel):
        __obj_slice = obj.iloc[:rows]

        plt.figure(figsize=(15, 0.16 * rows))
        plt.grid(axis='y', linestyle=':')

        ax = sns.barplot(y=__obj_slice.index, x=__obj_slice.values, #type: ignore
                        orient='h',
                        width=0.8,
                        palette="viridis",
                        hue=__obj_slice.index) 

        plt.xlabel(xlabel)
        plt.xscale("log", base=np.e)


        plt.ylabel(ylabel, rotation=0)
        plt.tight_layout()


        for container in ax.containers:
            plt.bar_label(container) #type: ignore

        sns.despine(top=True, bottom=True, right=True, left=True)

        plt.tight_layout()
        plt.title(title)
        plt.show()

    @staticmethod
    def plot_2(y:pd.Series, title:str, xlabel, ylabel):
        plt.figure(figsize=(7,5))
        ax = sns.barplot(x=y.index, y=y.values, palette="pastel", hue=y.index) #type: ignore
        
        for container in ax.containers:
            plt.bar_label(container) #type: ignore
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        plt.grid(linestyle=":", axis="y")
        
        sns.despine(top=True, right=True)
        plt.tight_layout()
        plt.show()