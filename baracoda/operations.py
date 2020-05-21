import logging
import re
from datetime import datetime
from typing import List, Optional

from baracoda.db import db
from baracoda.exceptions import InvalidPrefixError
from baracoda.formats import HeronFormatter
from baracoda.orm.barcode import Barcode
from baracoda.orm.barcodes_group import BarcodesGroup

logger = logging.getLogger(__name__)


class BarcodeOperations:
    def __init__(self, sequence_name: str, prefix: str):
        logger.debug("Instantiate....")
        self.sequence_name = sequence_name
        self.prefix = prefix

        self.__check_prefix()

        self.formatter = HeronFormatter(prefix=self.prefix)

    def create_barcode_group(self, count) -> BarcodesGroup:
        """Creates a new barcode group and the associated barcodes.

        Arguments:
            count {int} -- number of barcodes to create in the group

        Returns:
            BarcodeGroup -- the barcode group created
        """
        try:
            next_values = self.__get_next_values(self.sequence_name, count)

            barcodes_group = self.__build_barcodes_group()
            db.session.add(barcodes_group)

            barcodes = [
                self.__build_barcode(self.prefix, next_value, barcodes_group=barcodes_group)
                for next_value in next_values
            ]
            db.session.add_all(barcodes)

            db.session.commit()

            return barcodes_group
        except Exception as e:
            db.session.rollback()
            raise e

    def create_barcode(self) -> Barcode:
        """Generate and store a barcode using the Heron formatter.

        Returns:
            str -- the generated barcode in the Heron format
        """
        try:
            next_value = self.__get_next_value(self.sequence_name)
            barcode = self.__build_barcode(self.prefix, next_value, barcodes_group=None)

            db.session.add(barcode)

            db.session.commit()

            return barcode
        except Exception as e:
            db.session.rollback()
            raise e

    def get_last_barcode(self, prefix: str) -> Optional[Barcode]:
        """Get the last barcode generated for the specified sequence.

        Arguments:
            prefix {str} -- prefix to use query for the last barcode

        Returns:
            Barcode -- last barcode generated for prefix or None
        """
        results = (
            db.session.query(Barcode, Barcode.barcode)
            .filter_by(prefix=self.prefix)
            .order_by(Barcode.id.desc())
            .first()
        )

        if results is None:
            return results

        return results[0]

    def __check_prefix(self) -> None:
        """Checks the provided prefix.

        Raises:
            InvalidPrefixError: the prefix does not pass the regex test
        """
        if not self.__validate_prefix():
            raise InvalidPrefixError()

    def __validate_prefix(self) -> bool:
        """Validate the prefix used for the Heron barcodes. Currently accepting uppercase letters
        and numbers between 1 and 10 characters long.

        Returns:
            bool -- whether the prefix passed validation
        """
        if type(self.prefix) != str:
            return False

        pattern = re.compile(r"^[A-Z0-9]{1,10}$")

        return bool(pattern.match(self.prefix))

    def __build_barcode(
        self, prefix: str, next_value: int, barcodes_group: Optional[BarcodesGroup]
    ) -> Barcode:
        #  convert the next value to hexidecimal
        hex_str = format(next_value, "X")
        barcode = self.formatter.barcode(hex_str)
        return Barcode(
            prefix=prefix,
            barcode=barcode,
            created_at=datetime.now(),
            barcodes_group=barcodes_group,
        )

    def __build_barcodes_group(self) -> BarcodesGroup:
        return BarcodesGroup(created_at=datetime.now())

    def __get_next_value(self, sequence_name: str) -> int:
        """Get the next value from the sequence.

        Arguments:
            sequence_name {str} -- name of the sequence to query

        Returns:
            str -- next value in sequence
        """
        return int(db.session.execute(f"SELECT nextval('{sequence_name.lower()}');").fetchone()[0])

    def __get_next_values(self, sequence_name: str, count: int) -> List[int]:
        """Get the next count values from the sequence.

        Arguments:
            sequence_name {str} -- name of the sequence to query
            count {int} -- number of values from the sequence to generate

        Returns:
            str -- next value in sequence
        """
        return [
            int(val[0])
            for val in db.session.execute(
                f"SELECT nextval('{sequence_name.lower()}') FROM    generate_series(1, {count}) l;"
            ).fetchall()
        ]