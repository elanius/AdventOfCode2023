import sys
import re
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class CardData:
    winning_numbers: List[int]
    numbers: List[int]
    matching: int = 0
    multiplier: int = 1


def parse_file(filename: str) -> Dict[int, CardData]:
    cards: Dict[int, CardData] = {}
    with open(filename) as f:
        text = f.read()

    pattern = re.compile(r'Card\s+(?P<card_id>\d+):\s+(?P<winning_numbers>[0-9\s]+)\|\s+(?P<numbers>[0-9\s]+)')
    for match in pattern.finditer(text):
        card_id = int(match.group('card_id'))
        winning_numbers = [int(num) for num in match.group('winning_numbers').split()]
        numbers = [int(num) for num in match.group('numbers').split()]
        cards[card_id] = CardData(winning_numbers, numbers)

    return cards


def count_points(card_data: CardData) -> int:
    for win_num in card_data.winning_numbers:
        if win_num in card_data.numbers:
            card_data.matching += 1

    if card_data.matching == 0:
        return 0
    else:
        return pow(2, card_data.matching - 1)


def count_scratchcards_and_copies(cards: Dict[int, CardData]) -> int:
    for card_id, card_data in cards.items():
        for next_id in range(card_id + 1, card_id + card_data.matching + 1):
            cards[next_id].multiplier += card_data.multiplier

    return sum(card.multiplier for card in cards.values())


def main():
    sum = 0
    if len(sys.argv) != 2:
        print("Usage: python gear_ratios.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    cards = parse_file(filename)

    for card_id, card_data in cards.items():
        points = count_points(card_data)
        print(f"Card {card_id}: {points}")
        sum += points

    print(f"Sum: {sum}")

    count = count_scratchcards_and_copies(cards)
    print(f"Count: {count}")


if __name__ == "__main__":
    main()
