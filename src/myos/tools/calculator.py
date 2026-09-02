class CalculatorTool:
    def call(self, expression: str) -> str:
        return str(eval(expression))