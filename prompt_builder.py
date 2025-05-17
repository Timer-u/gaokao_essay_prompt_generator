class PromptBuilder:
    @staticmethod
    def build_prompt(params):
        # 公共模板
        prompt = [
            "Please act as an expert English writing tutor "
            "specializing in Chinese high school education.",
            f"Analyze the following {params['input_type'].value} "
            "and provide detailed polishing suggestions:",
        ]

        # 具体要求
        spec = {
            "argumentative": {
                "structure": (
                    "- Logical flow between paragraphs\n"
                    "- Thesis statement clarity"
                ),
                "vocabulary": (
                    "- Academic vocabulary enhancement\n"
                    "- Proper collocations"
                ),
                "grammar": (
                    "- Complex sentence structures\n"
                    "- Subject-verb agreement"
                ),
            },
            "continuation": {
                "coherence": (
                    "- Plot continuity with original story\n"
                    "- Character consistency"
                ),
                "vividness": (
                    "- Sensory descriptions\n" "- Dialogue naturalness"
                ),
                "climax": ("- Suspense building\n" "- Meaningful ending"),
            },
        }[params["essay_type"]]

        # 添加选择维度
        prompt.append("\n【Focus Areas】")
        for opt in params["options"]:
            if opt in spec:
                prompt.append(spec[opt])

        # 添加内容
        prompt.extend(
            [
                f"\n【Content to Analyze】\n{params['content']}",
                "\n【Output Requirements】",
                "1. 修改建议 (中文)",
                "2. Revised version",
                "3. 修改说明 (英文)",
            ]
        )

        return "\n".join(prompt)
