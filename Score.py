def load_score() -> int:
    with open('score.txt', 'r') as file:
         return int(file.read().strip())

def save_score(score: int) -> None:
    with open('score.txt', 'w') as file:
        file.write(str(score))