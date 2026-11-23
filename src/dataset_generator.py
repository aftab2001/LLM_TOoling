from pathlib import Path
from tool import OPERATIONS
import random
import argparse
import json

PREFIX = "What is"
POSTFIX = "? Answer:"
LIMIT = 1000
MAX_OPS = 3
SEED = 0
SAVE_PATH = Path(__file__).resolve().parent.parent / "data" / "samples.json"
NUM_SAMPLES = 1000
SYMBOLS = {"add": "+", "sub": "-", "mul": "*", "div": "/", "mod": "%"}


class DatasetGenerator:

    def __init__(self, prefix=None, postfix=None, limit=None, max_ops=None, seed=SEED):
        self.prefix = prefix or PREFIX
        self.postfix = postfix or POSTFIX
        self.limit = limit or LIMIT
        self.max_ops = max_ops or MAX_OPS
        self.rng = random.Random(seed)

    def generate(self, num_samples: int = NUM_SAMPLES) -> list[dict]:
        samples = []
        for _ in range(num_samples):
            k = self.rng.randint(1, self.max_ops)
            ops = [self.rng.choice(OPERATIONS) for _ in range(k)]
            nums = [self.rng.randint(1, self.limit) for _ in range(k + 1)]
            expression = str(nums[0]) + "".join(
                f" {SYMBOLS[op]} {n}" for op, n in zip(ops, nums[1:])
            )
            # eval is safe: the string holds only our own ints and operator symbols.
            # No parentheses, so every divisor is a literal >= 1 and % never sees a negative operand.
            answer = float(eval(expression, {"__builtins__": {}}))
            samples.append({
                "question": f"{self.prefix} {expression}{self.postfix}",
                "answer": answer,
                "expression": expression,
                "ops": ops,
                "num_ops": k,
            })
        return samples

    @staticmethod
    def save_as_json(samples: list[dict], save_path: Path):
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w") as f:
            json.dump(samples, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Dataset Generator')
    parser.add_argument('--save_path', type=Path, default=SAVE_PATH)
    parser.add_argument('--prefix', default=PREFIX)
    parser.add_argument('--postfix', default=POSTFIX)
    parser.add_argument('--limit', type=int, default=LIMIT)
    parser.add_argument('--num_samples', type=int, default=NUM_SAMPLES)
    parser.add_argument('--max_ops', type=int, default=MAX_OPS)
    parser.add_argument('--seed', type=int, default=SEED)

    args = parser.parse_args()
    dg = DatasetGenerator(args.prefix, args.postfix, args.limit, args.max_ops, args.seed)
    dg.save_as_json(dg.generate(args.num_samples), args.save_path)
