def is_valid_passphrase(passphrase):
    """Should only contain unique words.

    >>> is_valid_passphrase('aa bb cc dd ee')
    True
    >>> is_valid_passphrase('aa bb cc dd aa')
    False
    >>> is_valid_passphrase('aa bb cc dd aaa')
    True
    """
    words = passphrase.split(' ')
    return len(words) == len(set(words))


def count_valid_passphrases(passphrases):
    return sum(1 for p in passphrases if is_valid_passphrase(p))


def normalize_phrases(passphrases):
    for p in passphrases:
        words = p.split(' ')
        yield ' '.join(''.join(sorted(word)) for word in words)


if __name__ == '__main__':
    with open('day04.in') as f:
        print(count_valid_passphrases(l.rstrip('\n') for l in f))
    with open('day04x.in') as f:
        phrases = normalize_phrases(l.rstrip('\n') for l in f)
        print(count_valid_passphrases(phrases))
