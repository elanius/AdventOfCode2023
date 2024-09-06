from seeds import Interval, Mapping, Map


def test_merge_wide_to_narrow():
    # input  +-------------------+
    # input         +----+
    #        _____________________
    # result +------+----+-------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(20, 60), destination_range=Interval(30, 70))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(40, 50), destination_range=Interval(10, 20))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(20, 29), destination_range=Interval(30, 39)),
            Map(source_range=Interval(30, 40), destination_range=Interval(10, 20)),
            Map(source_range=Interval(41, 60), destination_range=Interval(51, 70)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_narrow_to_wide():
    # input         +----+
    # input  +-------------------+
    #        _____________________
    # result +------+----+-------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(15, 20), destination_range=Interval(60, 65))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(55, 70), destination_range=Interval(30, 45))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(55, 59), destination_range=Interval(30, 34)),
            Map(source_range=Interval(15, 20), destination_range=Interval(35, 40)),
            Map(source_range=Interval(66, 70), destination_range=Interval(41, 45)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_wide_to_narrow_on_left():
    # input  +-------------------+
    # input  +----+
    #        _____________________
    # result +----+--------------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(30, 60), destination_range=Interval(40, 70))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(40, 50), destination_range=Interval(10, 20))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(30, 40), destination_range=Interval(10, 20)),
            Map(source_range=Interval(41, 60), destination_range=Interval(51, 70)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_narrow_to_wide_on_left():
    # input  +----+
    # input  +-------------------+
    #        _____________________
    # result +----+--------------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(30, 40), destination_range=Interval(50, 60))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(50, 70), destination_range=Interval(0, 20))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(30, 40), destination_range=Interval(0, 10)),
            Map(source_range=Interval(61, 70), destination_range=Interval(11, 20)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_wide_to_narrow_on_right():
    # input  +-------------------+
    # input                 +----+
    #        _____________________
    # result +--------------+----+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(30, 60), destination_range=Interval(40, 70))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(40, 50), destination_range=Interval(10, 20))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(30, 40), destination_range=Interval(10, 20)),
            Map(source_range=Interval(41, 60), destination_range=Interval(51, 70)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_narrow_to_wide_on_right():
    # input                 +----+
    # input  +-------------------+
    #        _____________________
    # result +--------------+----+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(10, 20), destination_range=Interval(30, 40))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(20, 40), destination_range=Interval(50, 70))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(20, 29), destination_range=Interval(50, 59)),
            Map(source_range=Interval(10, 20), destination_range=Interval(60, 70)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_wide_to_one():
    # input  +-------------------+
    # input         +
    #        _____________________
    # result +------+------------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(20, 60), destination_range=Interval(30, 70))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(65, 65), destination_range=Interval(10, 10))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(20, 54), destination_range=Interval(30, 64)),
            Map(source_range=Interval(55, 55), destination_range=Interval(10, 10)),
            Map(source_range=Interval(56, 60), destination_range=Interval(66, 70)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_one_to_wide():
    # input              +
    # input  +-------------------+
    #        _____________________
    # result +-----------+-------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(90, 90), destination_range=Interval(15, 15))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(10, 20), destination_range=Interval(50, 60))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(10, 14), destination_range=Interval(50, 54)),
            Map(source_range=Interval(90, 90), destination_range=Interval(55, 55)),
            Map(source_range=Interval(16, 20), destination_range=Interval(56, 60)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_left_shifted_narrow_to_wide_on_left():
    # input  +---+
    # input   +-------------------+
    #        _____________________
    # result ++---+--------------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(0, 10), destination_range=Interval(30, 40))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(31, 50), destination_range=Interval(71, 90))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(0, 0), destination_range=Interval(30, 30)),
            Map(source_range=Interval(1, 10), destination_range=Interval(71, 80)),
            Map(source_range=Interval(41, 50), destination_range=Interval(81, 90)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def test_merge_right_shifted_narrow_to_wide_on_left():
    # input   +---+
    # input  +-------------------+
    #        _____________________
    # result ++---+--------------+

    upper = Mapping(name="one-to-second", maps=[Map(source_range=Interval(0, 10), destination_range=Interval(30, 40))])

    lower = Mapping(
        name="second-to-third", maps=[Map(source_range=Interval(29, 50), destination_range=Interval(69, 90))]
    )

    merged_expected = Mapping(
        name="one-to-third",
        maps=[
            Map(source_range=Interval(29, 29), destination_range=Interval(69, 69)),
            Map(source_range=Interval(0, 10), destination_range=Interval(70, 80)),
            Map(source_range=Interval(41, 50), destination_range=Interval(81, 90)),
        ],
    )

    merged = upper.merge(lower)
    assert merged_expected.name == merged.name
    assert merged_expected == merged


def create_mapping_from_text(name: str, text: str) -> Mapping:
    lines = text.split("\n")
    maps = []
    for line in lines:
        line = line.replace(" ", "")
        if not line:
            continue
        # remove spaces
        source, destination = line.split("->")
        source_start, source_end = source.split("-")
        destination_start, destination_end = destination.split("-")
        maps.append(
            Map(
                source_range=Interval(int(source_start), int(source_end)),
                destination_range=Interval(int(destination_start), int(destination_end)),
            )
        )
    return Mapping(name=name, maps=maps)


def test_complex_merge():
    # input   +---+
    # input  +-------------------+
    #        _____________________
    # result ++---+--------------+

    upper = create_mapping_from_text(
        "seed-to-fertilizer",
        """
         0 - 14 -> 39 - 53
        15 - 49 ->  0 - 34
        98 - 99 -> 35 - 36
        50 - 51 -> 37 - 38
        52 - 97 -> 54 - 99
        """
    )

    lower = create_mapping_from_text(
        "fertilizer-to-water",
        """
         0 -  6 -> 42 - 48
         7 - 10 -> 57 - 60
        11 - 52 ->  0 - 41
        53 - 60 -> 49 - 56
        """
    )

    # problematic 14 - 14 -> 53 - 53

    # merged_expected = Mapping(
    #     name="one-to-third",
    #     maps=[
    #         Map(source_range=Interval(29, 29), destination_range=Interval(69, 69)),
    #         Map(source_range=Interval(0, 10), destination_range=Interval(70, 80)),
    #         Map(source_range=Interval(41, 50), destination_range=Interval(81, 90)),
    #     ],
    # )

    merged = upper.merge(lower)
    pass
    # assert merged_expected.name == merged.name
    # assert merged_expected == merged
