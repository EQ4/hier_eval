#!/usr/bin/env python
"""
Converts a lab file to a jams file.

Example:


"""

__author__ = "Oriol Nieto"
__copyright__ = "Copyright 2014, Music and Audio Research Lab (MARL)"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "oriol@nyu.edu"

import argparse
import jams
import json
import logging
import time


def fill_global_metadata(jam, lab_file):
    """Fills the global metada into the JAMS jam."""
    jam.metadata.artist = "Unknown"
    jam.metadata.duration = "Unknown"  # In seconds
    jam.metadata.title = "Unknown"

    # TODO: extra info
    #jam.metadata.genre = metadata[14]


def fill_annoatation_metadata(annot, attribute):
    """Fills the annotation metadata."""
    annot.annotation_metadata.attribute = attribute
    annot.annotation_metadata.corpus = "Unknown"
    annot.annotation_metadata.version = "1.0"
    annot.annotation_metadata.annotation_tools = "Unknown"
    annot.annotation_metadata.annotation_rules = "Unknown"
    annot.annotation_metadata.validation_and_reliability = "Unknown"
    annot.annotation_metadata.origin = "Unknown"
    annot.annotation_metadata.annotator.name = "Unknown"
    annot.annotation_metadata.annotator.email = "Unknown"


def fill_section_annotation(lab_file, annot):
    """Fills the JAMS annot annotation given a lab file."""

    # Annotation Metadata
    fill_annoatation_metadata(annot, "sections")

    # Open lab file
    try:
        f = open(lab_file, "r")
    except IOError:
        logging.warning("Annotation doesn't exist: %s", lab_file)
        return

    # Convert to JAMS
    lines = f.readlines()
    for line in lines:
        section_raw = line.strip("\n").split("\t")
        start_time = section_raw[0]
        end_time = section_raw[1]
        label = section_raw[3]
        section = annot.create_datapoint()
        section.start.value = float(start_time)
        section.start.confidence = 1.0
        section.end.value = float(end_time)
        section.end.confidence = 1.0
        section.label.value = label
        section.label.confidence = 1.0
        section.label.context = "function"  # Only function level of annotation

    f.close()


def create_JAMS(lab_file, out_file):
    """Creates a JAMS file given the lab file."""

    # New JAMS and annotation
    jam = jams.Jams()

    # Global file metadata
    fill_global_metadata(jam, lab_file)

    # Create Section annotations
    annot = jam.sections.create_annotation()
    fill_section_annotation(lab_file, annot)

    # Save JAMS
    f = open(out_file, "w")
    json.dump(jam, f, indent=2)
    f.close()


def process(lab_file, jams_file=None):
    """Converts the lab file to a JAMS file."""

    if jams_file is None:
        jams_file = lab_file.replace(lab_file.split(".")[-1], "jams")

    #Create a JAMS file for this track
    create_JAMS(lab_file, jams_file)


def main():
    """Main function to convert lab file to JAMS."""
    parser = argparse.ArgumentParser(description=
                                     "Converts a lab file to JAMS.",
                                     formatter_class=
                                     argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("lab_file",
                        action="store",
                        help="Input lab file")
    parser.add_argument("-o",
                        action="store",
                        dest="jams_file",
                        default=None,
                        help="Output JAMS file")
    args = parser.parse_args()
    start_time = time.time()

    # Setup the logger
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)

    # Run the parser
    process(args.lab_file, args.jams_file)

    # Done!
    logging.info("Done! Took %.2f seconds." % (time.time() - start_time))

if __name__ == '__main__':
    main()
