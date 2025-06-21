"""高考英语作文提示词生成器主入口"""

import tkinter as tk
from gui import PromptGenerator

if __name__ == "__main__":
    root = tk.Tk()
    app = PromptGenerator(root)
    root.mainloop()
