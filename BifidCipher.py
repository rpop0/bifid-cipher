from __future__ import annotations

from textwrap import wrap
import random
import re


class Coordinate:

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    @staticmethod
    def from_list(values: list[int]) -> list[Coordinate]:
        """
        Function that takes in a list of integers representing coordinates and transforms it into a list of Coordinate
        objects by transforming each pair of integers into a Coordinate.
        :param values: List of integers, must be of even length.
        :return: List sent in values, but converted into Coordinate objects.
        """
        if len(values) % 2 != 0:
            raise ValueError("Length of the list to convert into coordinates must be even.")
        coordinates = list()

        # Looping with range, with a step of two and creating a Coordinate object with each pair of elements.
        for i in range(0, len(values), 2):
            coordinates.append(Coordinate(values[i], values[i + 1]))

        return coordinates

    @staticmethod
    def to_list(values: list[Coordinate]) -> list[int]:
        """
        Converts a list of Coordinate objects to a list of integers matching that initial list, where is pair is a
        coordinate.
        :param values: List of coordinate objects.
        :return: List of integers.
        """
        coordinates = list()
        for coordinate in values:
            coordinates.extend([coordinate.row, coordinate.col])
        return coordinates

    def __repr__(self) -> str:
        return f'Coordinate({self.row}, {self.col})'


class BifidCipher:

    # Alphabet to use in case no polybius square is defined. J is removed intentionally.
    ALPHABET = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

    def __init__(self, polybius_square_string: str | None = None, period=5):
        self.polybius_square = BifidCipher._process_polybius_square(polybius_square_string)
        self.period = period

    @staticmethod
    def _process_polybius_square(polybius_square_string: str) -> list[list]:
        """
        Method to transform the input polybius square string to the correct structure. It cleans up the input string
        then transforms it.
        :param polybius_square_string: Input string that represents the letters to form the polybius square.
        :return: List of lists, representing the square.
        """
        # If no polybius square is entered, shuffle the defined alphabet and use it.
        if polybius_square_string is None:
            polybius_square_string = ''.join(random.sample(BifidCipher.ALPHABET, len(BifidCipher.ALPHABET)))

        # Quickly transforms the string to upper and replaces the J with nothing since in the Polybius square, Js
        # Are replaced by Is, so generally an input Polybius square shouldn't contain a J.
        polybius_square_string = polybius_square_string.upper().replace('J', '')

        # _clean_input_string() also transforms the string to upper case internally, so this gets transformed twice,
        # Not really an issue but this is the simples solution.
        polybius_square_string = BifidCipher._clean_input_string(polybius_square_string)
        if len(polybius_square_string) != 25:
            raise ValueError("Polybius square has a different length than 25.")
        polybius_square = list()

        # Looping from 0 to 25 with a step of 5 since the square should have 25 characters;
        for i in range(0, 25, 5):
            # Get a segment string of 5 characters
            segment = polybius_square_string[i:i + 5]
            # Unpacking a string and adding it to a list makes each char of the string into a single list element.
            polybius_square.append([*segment])

        return polybius_square

    @staticmethod
    def _clean_input_string(input_string: str) -> str:
        """
        Cleans an input string by removing spaces, transforming it to upper characters and transforming the J character
        into I. This is used for both cleaning the input Polybius square and also the messages to encrypt.
        :param input_string: Strings to clean.
        :return: Cleaned string.
        """
        input_string = input_string.replace(' ', '')
        input_string = input_string.upper()
        input_string = input_string.replace('J', 'I')
        # The below regex matches any non word character in input_string and replaces it with nothing, essentially
        # leaving only characters from the alphabet.
        input_string = re.sub(r'[\W_]', '', input_string)
        return input_string

    def _get_coordinate(self, character: str) -> Coordinate:
        """
        Gets a Polybius coordinate from a character.
        :param character: Character to get the coordinate for.
        :return: A coordinate object matching the character.
        """
        # Character has to be of length 1 to get its coordinate.
        if len(character) != 1:
            raise ValueError("Cannot get coordinates of input with length different than one.")

        # Loops through the whole Polybius square item by item. Using enumerate to also get the index.
        for row_idx, row in enumerate(self.polybius_square):
            for col_idx, item in enumerate(row):
                # When we are getting to the correct item, simply create a Coordinate object with the indexes and return
                if item == character:
                    return Coordinate(row_idx, col_idx)

    def _get_character_from_coordinate(self, coordinate: Coordinate) -> str:
        """
        Searches for the received coordinate in the Polybius square and returns the character at that coordinate.
        :param coordinate: Coordinate to look up in the square.
        :return: Character matching that coordinate.
        """
        return self.polybius_square[coordinate.row][coordinate.col]

    @staticmethod
    def _get_encrypted_coordinates(coordinates: list[Coordinate]) -> list[Coordinate]:
        """
        Takes in a list of coordinates and transforms them into their encrypted version. This encryption is done
        by getting all the row values of the coordinates in a list and all the column values in another list. These
        two lists are then concatenated and transformed back into Coordinate objects.

        Example:
            [Coordinate(3, 2), Coordinate(5, 6)] gets transformed in:
                [3, 5] (row_values) and [2, 6] (column_values)
            These two lists are then concatenated to become:
                [3, 5, 2, 6]
            Finally, they are transformed back into Coordinate objects, two at a time:
                [Coordinate(3, 5), Coordinate(2, 6)]

        :param coordinates: List of non-encrypted coordinates.
        :return: List of encrypted coordinates.
        """
        row_values = list()
        column_values = list()
        for coordinate in coordinates:
            row_values.append(coordinate.row)
            column_values.append(coordinate.col)

        return Coordinate.from_list(row_values + column_values)

    @staticmethod
    def _get_decrypted_coordinates(coordinates: list[Coordinate]):
        """
        Takes in a list of encrypted Coordinate objects and turns them in their decrypted version. The whole decryption
        process is started by converting the list of Coordinate objects to a simple list of integers, in the same order
        of the received coordinates. Afterwards, this list of integers is split in two halves, which are then zipped
        together and created back into Coordinate objects.

        Example:
            [Coordinate(3, 5), Coordinate(2, 6)] gets transformed in:
                [3, 5, 2, 6] (coordinates)
            The above list then gets split into two halves:
                [3, 5] (first_half) and [2, 6] (second_half)
            Finally, they are zipped together, essentially creating a Coordinate with the row from the first_half and
            the column from the second_half, at a matching index:
                [Coordinate(3, 2), Coordinate(5, 6)]

        :param coordinates: List of encrypted coordinates.
        :return: List of decrypted coordinates.
        """
        coordinates = Coordinate.to_list(coordinates)

        mid_point = len(coordinates) // 2

        # Splits the coordinates in two halves.
        first_half = coordinates[:mid_point]
        second_half = coordinates[mid_point:]

        merged = list()
        # Merges them back at matching indexes.
        for first, second in zip(first_half, second_half):
            merged.append(Coordinate(first, second))

        return merged

    def _coordinates_to_message(self, coordinates: list[Coordinate]) -> str:
        """
        Takes in a list of Coordinate objects and converts it to characters from the Polybius square.
        :param coordinates: List of coordinates to transform.
        :return: Matching message of the input coordinates
        """
        message = str()
        # Loops through each coordinate and transforms each individual coordinate into a character and builds the
        # message.
        for coordinate in coordinates:
            character = self._get_character_from_coordinate(coordinate)
            message = f'{message}{character}'
        return message

    def _encrypt_period(self, period: str) -> str:
        """
        Takes in a message period of any size and encrypts it.
        :param period: A period/block of characters to encrypt.
        :return: The encrypted characters of the period/block
        """
        period_coordinates = list()
        # The first step is to get the coordinates in the Polybius square for each character in the period.
        for character in period:
            period_coordinates.append(self._get_coordinate(character))

        # The second step is to convert the normal coordinates in their encrypted versions.
        encrypted_coordinates = BifidCipher._get_encrypted_coordinates(period_coordinates)

        return self._coordinates_to_message(encrypted_coordinates)

    def _decrypt_period(self, period) -> str:
        """
        Takes in an encrypted period/block of any size and decrypts it.

        The first step in the decryption is translating the characters in the period to coordinates of
        the Polybius square.

        The second step in the decryption process is to translate the encrypted coordinates into their decrypted
        variants.

        :param period: A period/block of characters to decrypt.
        :return: The decrypted characters of the period/block.
        """
        period_coordinates = list()
        for character in period:
            period_coordinates.append(self._get_coordinate(character))

        decrypted_coordinates = BifidCipher._get_decrypted_coordinates(period_coordinates)
        return self._coordinates_to_message(decrypted_coordinates)

    def encrypt_message(self, message: str) -> str:
        """
        Encrypts a message using the Bifid Cipher, using the specified amount of periods.
        :param message: Message to encrypt.
        :return: Encrypted message.
        """
        # Message needs to be cleaned in order to be properly processed. Cleaning is making sure the message has ONLY
        # alphabetical characters and no spaces, also the character "J" replaced by "I"
        message = BifidCipher._clean_input_string(message)

        # In order to achieve a good encryption, it is necessary to split the message into periods. For example
        # the message HELLO gets split into the periods 'HEL' and 'LO', then each period gets encrypted individually.
        periods = wrap(message, self.period)
        message = ''

        # Loops through all the periods, encrypts each period and adds it to the final message.
        for period in periods:
            message = f'{message}{self._encrypt_period(period)}'
        return message

    def decrypt_message(self, message: str) -> str:
        periods = wrap(message, self.period)
        message = ''
        for period in periods:
            message = f'{message}{self._decrypt_period(period)}'
        return message
