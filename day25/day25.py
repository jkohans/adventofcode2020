def calculate_public_key(subject_key=7):
    value = 1

    while True:
        value = (value * subject_key) % 20201227
        yield value


if __name__ == "__main__":
    public_key1 = 6930903
    public_key2 = 19716708

    # generator = calculate_public_key()
    #
    # for loop_size in range(1, 100000000):
    #     value = next(generator)
    #
    #     if value == public_key1:
    #         print(loop_size, "matches pk1")
    #     elif value == public_key2:
    #         print(loop_size, "matches pk2")

    # 11893237 matches pk2
    # 16190552 matches pk1

    for pk in [public_key1, public_key2]:
        for loop_size in [11893237, 16190552]:
            # card pk + door loop size
            generator = calculate_public_key(subject_key=pk)
            value = None
            for _ in range(loop_size):
                value = next(generator)
            print(f"pk={pk}, loop_size={loop_size}, {value}")

# handshake: transform subject number
# - 1 x loop size
#   - itself * subject number, remainder of / 20201227

# card uses specific secret loop size, door uses different secret loop size

# card transforms subject number 7 --> card's public key
# door transforms subject number 7 --> door's public key
# card and door transmit public keys to each other
# card transforms door public key according to its loop size --> encryption key
# door transforms card public key according to its loop size --> same encryption key as above

# reverse engineer loop size to calculate secret encryption key
