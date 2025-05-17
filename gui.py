import tkinter as tk
from tkinter import ttk, messagebox
from enums import InputType
from prompt_builder import PromptBuilder

class PromptGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("高考英语作文提示词生成器")
        self.setup_geometry()
        self.create_widgets()
        self.setup_variables()

    def setup_geometry(self):
        window_width = 1000
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(
            f"{window_width}x{window_height}+"
            f"{(screen_width//2 - window_width//2)}+"
            f"{(screen_height//2 - window_height//2)}"
        )

    def setup_variables(self):
        self.essay_type = tk.StringVar(value="argumentative")
        self.polish_level = tk.StringVar(value="medium")
        self.input_type = tk.StringVar(value=InputType.PARAGRAPH.value)

        self.optimize_options = {
            "structure": tk.BooleanVar(value=True),
            "vocabulary": tk.BooleanVar(value=True),
            "grammar": tk.BooleanVar(value=True),
            "coherence": tk.BooleanVar(),
            "vividness": tk.BooleanVar(),
            "climax": tk.BooleanVar()
        }

    def create_widgets(self):
        self.create_input_section()
        self.create_config_section()
        self.create_output_section()

    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.root, text="输入内容", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        type_frame = ttk.Frame(input_frame)
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(type_frame, text="输入类型:").pack(side=tk.LEFT)
        for itype in InputType:
            ttk.Radiobutton(
                type_frame,
                text=itype.value,
                variable=self.input_type,
                value=itype.value,
            ).pack(side=tk.LEFT, padx=5)

        self.input_text = tk.Text(input_frame, height=10, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)

    def create_config_section(self):
        config_frame = ttk.Frame(self.root)
        config_frame.pack(fill=tk.X, padx=10, pady=5)

        left_pane = ttk.Frame(config_frame)
        left_pane.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        type_frame = ttk.LabelFrame(left_pane, text="作文类型")
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(
            type_frame, text="议论文", variable=self.essay_type, value="argumentative"
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            type_frame, text="读后续写", variable=self.essay_type, value="continuation"
        ).pack(side=tk.LEFT)

        level_frame = ttk.LabelFrame(left_pane, text="润色级别")
        level_frame.pack(fill=tk.X, pady=5)
        levels = [("基础", "basic"), ("中等", "medium"), ("高级", "advanced")]
        for text, val in levels:
            ttk.Radiobutton(
                level_frame, text=text, variable=self.polish_level, value=val
            ).pack(side=tk.LEFT, padx=5)

        right_pane = ttk.LabelFrame(config_frame, text="优化维度")
        right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        options_mapping = {
            "argumentative": [
                ("文章结构", "structure"),
                ("词汇提升", "vocabulary"),
                ("语法优化", "grammar"),
            ],
            "continuation": [
                ("连贯性", "coherence"),
                ("生动性", "vividness"),
                ("高潮处理", "climax"),
            ],
        }

        self.option_checks = {}
        for text, var in options_mapping["argumentative"]:
            cb = ttk.Checkbutton(
                right_pane,
                text=text,
                variable=self.optimize_options[var],
                command=self.update_options_visibility,
            )
            cb.pack(anchor=tk.W)
            self.option_checks[var] = cb

        self.update_options_visibility()

    def update_options_visibility(self):
        is_argumentative = self.essay_type.get() == "argumentative"
        for var, cb in self.option_checks.items():
            cb.pack_forget() if var in ["coherence", "vividness", "climax"] else None

        options_mapping = {
            "argumentative": ["structure", "vocabulary", "grammar"],
            "continuation": ["coherence", "vividness", "climax"],
        }
        for var in options_mapping[self.essay_type.get()]:
            self.option_checks[var].pack(anchor=tk.W)

    def create_output_section(self):
        ttk.Button(self.root, text="生成提示词", command=self.generate_prompt).pack(
            pady=5
        )

        output_frame = ttk.LabelFrame(self.root, text="生成的提示词", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.output_text = tk.Text(output_frame, height=15, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="复制提示词", command=self.copy_to_clipboard).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="清空内容", command=self.clear_content).pack(
            side=tk.LEFT
        )

    def generate_prompt(self):
        if not self.validate_input():
            return

        params = {
            "content": self.input_text.get("1.0", tk.END).strip(),
            "essay_type": self.essay_type.get(),
            "polish_level": self.polish_level.get(),
            "input_type": next(
                it for it in InputType if it.value == self.input_type.get()
            ),
            "options": [k for k, v in self.optimize_options.items() if v.get()],
        }

        prompt = PromptBuilder.build_prompt(params)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", prompt)

    def validate_input(self):
        content = self.input_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "请输入要润色的内容！")
            return False
        if not any(v.get() for v in self.optimize_options.values()):
            messagebox.showwarning("警告", "请至少选择一个优化维度！")
            return False
        return True

    def copy_to_clipboard(self):
        prompt = self.output_text.get("1.0", tk.END).strip()
        if prompt:
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt)
            messagebox.showinfo("成功", "提示词已复制到剪贴板！")

    def clear_content(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        