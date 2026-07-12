""" This script handles the import of csv files. """
import csv
from io import TextIOWrapper
from datetime import datetime


class CSVImporter:

    MAX_ROWS = 5000

    REQUIRED_COLUMNS = {
        "customer_name",
        "customer_id",
        "order_number",
        "comment",
        "survey_type",
        "score",
        "source",
        "feedback_date",
    }

    def import_feedback(self, file):
        """Import feedback from a CSV file."""

        if not file or file.filename == "":
            raise ValueError("Please select a CSV file.")

        if not file.filename.lower().endswith(".csv"):
            raise ValueError("Only CSV files are allowed.")

        csv_file = TextIOWrapper(file.stream, encoding="utf-8-sig")

        # Helper to detect the file delimiter automatically
        sample = csv_file.read(1024)
        csv_file.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel

        reader = csv.DictReader(csv_file, dialect=dialect)

        if not reader.fieldnames:
            raise ValueError("The uploaded file is empty.")

        # Normalize the column headers
        reader.fieldnames = [
            header.strip().lower()
            for header in reader.fieldnames
        ]

        # Validate required columns
        missing = self.REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(sorted(missing))}"
            )

        records = []

        for row_number, row in enumerate(reader, start=2):

            # Validate row count
            if row_number - 1 > self.MAX_ROWS:
                raise ValueError(
                    f"CSV files are limited to {self.MAX_ROWS} rows."
                )

            # Validate customer name
            customer_name = row["customer_name"].strip()

            if not customer_name:
                raise ValueError(
                    f"Missing customer_name on row {row_number}."
                )

            try:
                # Validate score format
                score = int(row["score"])
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid score on row {row_number}."
                )

            try:
                # Validate datetime format
                feedback_date = datetime.strptime(
                    row["feedback_date"].strip(),
                    "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                raise ValueError(
                    f"Invalid feedback_date on row {row_number}. "
                    f"Expected YYYY-MM-DD HH:MM:SS."
                )

            records.append({
                "customer_name": customer_name,
                "customer_id": row["customer_id"].strip(),
                "order_number": row["order_number"].strip(),
                "comment": row["comment"].strip(),
                "survey_type": row["survey_type"].strip(),
                "score": score,
                "source": row["source"].strip(),
                "feedback_date": feedback_date,
            })

        # Check if file contains data
        if not records:
            raise ValueError(
                "The CSV file contained no data."
            )

        return records