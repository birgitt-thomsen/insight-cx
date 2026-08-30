"""This script handles the import and validation of CSV feedback files."""

import csv
from io import TextIOWrapper
from datetime import datetime


class CSVImporter:
    """Handles importing and validating customer feedback CSV files."""

    # Maximum number of data rows allowed in a single upload.
    MAX_ROWS = 5000

    # These columns must exist in every uploaded CSV.
    # Additional columns are allowed and will simply be ignored.
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

    def calculate_nps_category(self, score):
        """Return the NPS category for a score."""

        if score >= 9:
            return "Promoter"

        if score >= 7:
            return "Passive"

        return "Detractor"

    def calculate_csat_category(self, score):
        """Return the CSAT category for a score."""

        if score >= 4:
            return "Satisfied"

        if score == 3:
            return "Neutral"

        return "Dissatisfied"

    def import_feedback(self, file):
        """Import feedback records from a CSV file."""

        # -------------------------------------------------------------
        # Basic file validation
        # -------------------------------------------------------------

        # Ensure a file was selected.
        if not file or file.filename == "":
            raise ValueError("Please select a CSV file.")

        # Only allow CSV uploads.
        if not file.filename.lower().endswith(".csv"):
            raise ValueError("Only CSV files are allowed.")

        # Create a text wrapper around the uploaded file.
        #
        # utf-8-sig:
        #   Automatically removes the UTF-8 BOM that Excel sometimes
        #   inserts at the beginning of CSV files.
        #
        # newline="":
        #   Recommended by Python's csv module to correctly handle
        #   different operating systems and embedded newlines.
        csv_file = TextIOWrapper(
            file.stream,
            encoding="utf-8-sig",
            newline=""
        )

        reader = None
        detected_delimiter = None

        # -------------------------------------------------------------
        # Determine which delimiter the CSV uses.
        #
        # German Excel typically exports semicolon-separated CSVs.
        # English Excel typically exports comma-separated CSVs.
        #
        # Instead of relying on csv.Sniffer() (which can make incorrect
        # guesses), simply try both delimiters and choose the one whose
        # headers contain all required columns.
        # -------------------------------------------------------------

        for delimiter in (",", ";"):

            # Reset the file pointer before reading again.
            csv_file.seek(0)

            test_reader = csv.DictReader(
                csv_file,
                delimiter=delimiter
            )

            # Skip if no header row exists.
            if not test_reader.fieldnames:
                continue

            # Normalize headers so comparisons become case-insensitive
            # and are unaffected by accidental whitespace.
            fieldnames = [
                header.strip().lower()
                for header in test_reader.fieldnames
                if header
            ]

            # If every required column exists, we've found
            # the correct delimiter.
            if self.REQUIRED_COLUMNS.issubset(fieldnames):
                test_reader.fieldnames = fieldnames
                reader = test_reader
                detected_delimiter = delimiter
                break

        # Neither comma nor semicolon produced the expected columns.
        if reader is None:
            raise ValueError(
                "The CSV file is missing one or more required columns.\n\n"
                f"Required columns:\n"
                f"{', '.join(sorted(self.REQUIRED_COLUMNS))}"
            )

        # Development logging.
        # Replace with the logging module in production if desired.
        print(f"Detected delimiter: '{detected_delimiter}'")
        print(f"Detected columns: {reader.fieldnames}")

        records = []

        # -------------------------------------------------------------
        # Process each row of the CSV.
        #
        # DictReader returns each row as a dictionary:
        #
        # {
        #     "customer_name": "...",
        #     "score": "...",
        #     ...
        # }
        #
        # Each row is validated before being converted into the format
        # expected by the database.
        # -------------------------------------------------------------

        for row_number, row in enumerate(reader, start=2):

            # The header occupies row 1, so the first data row is row 2.
            # Stop processing if the upload exceeds the configured limit.
            if row_number - 1 > self.MAX_ROWS:
                raise ValueError(
                    f"CSV files are limited to {self.MAX_ROWS} rows."
                )

            # ---------------------------------------------------------
            # Validate customer name
            # ---------------------------------------------------------

            customer_name = row["customer_name"].strip()

            if not customer_name:
                raise ValueError(
                    f"Missing customer_name on row {row_number}."
                )

            # ---------------------------------------------------------
            # Validate survey score
            # ---------------------------------------------------------

            try:
                score = int(row["score"])
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid score on row {row_number}."
                )

            # ---------------------------------------------------------
            # Validate feedback date
            # ---------------------------------------------------------

            try:
                feedback_date = datetime.strptime(
                    row["feedback_date"].strip(),
                    "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                raise ValueError(
                    f"Invalid feedback_date on row {row_number}. "
                    "Expected YYYY-MM-DD HH:MM:SS."
                )

            # Normalize survey type so "nps", "NPS", and "Nps"
            # are all treated identically.
            survey_type = row["survey_type"].strip().upper()

            # ---------------------------------------------------------
            # Build the validated record.
            #
            # This dictionary is what gets returned to the calling
            # service and ultimately saved to the database.
            #
            # Derived values (NPS and CSAT categories) are calculated
            # here rather than stored in the CSV.
            # ---------------------------------------------------------

            records.append({
                "customer_name": customer_name,
                "customer_id": row["customer_id"].strip(),
                "order_number": row["order_number"].strip(),
                "comment": row["comment"].strip(),
                "survey_type": survey_type,
                "score": score,
                "nps_category": (
                    self.calculate_nps_category(score)
                    if survey_type == "NPS"
                    else None
                ),
                "csat_category": (
                    self.calculate_csat_category(score)
                    if survey_type == "CSAT"
                    else None
                ),
                "source": row["source"].strip(),
                "feedback_date": feedback_date,
            })

        # Prevent importing a CSV that contains only a header row.
        if not records:
            raise ValueError(
                "The CSV file contained no data."
            )

        # Return the validated records to the calling service.
        return records