#!/usr/bin/env python
# -*- coding:utf-8 -*-
# The program reads from console and writes input into an XML file

import argparse
from glob import glob
import os
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET


def add_to_xml(xml_file, message):
    # parse the message
    message_tree = ET.fromstring(message)
    # parse the xml file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # try to find a similar node in xml
    results, _, _ = filter_by_string(root, message_tree.tag)
    # if found, add the new tag
    if results:
        # get a sample result
        result = results[0]
        # find the parent
        parent = list(result.values())[0]
        parent.append(message_tree)
    else:
        root.append(message_tree)
    tree.write(xml_file)


def create_xml(message):
    # let us assume that the file is called sample.xml and resides in current directory
    file_path = 'sample.xml'

    with open(file_path, 'w') as file_handle:
        file_handle.write(message)


def filter_by_element_and_value(root, element, value):
    results = []
    for parent in root.getiterator():
        for child in parent.findall(element):
            if child.text == value:
                results.append({child: parent})
    return results


def filter_by_string(root, message_filter):
    results = []
    element, value = '?', '?'
    # iterate through the tree and match each node and text
    for elem in root.getiterator():
        for subelem in elem:
            element_matches = (subelem.findall(message_filter))
            value_match = (subelem.text == message_filter)
            # save the match and its parent
            if element_matches:
                element = message_filter
                for element_match in element_matches:
                    results.append({element_match: subelem})
            elif value_match:
                results.append({subelem: elem})
                value = message_filter
    return results, element, value


def ui_pretty_print(out):
    line_length = len(out) + 3
    line = '\n{}\n'.format('*' * line_length)
    print(line, out, line)


def ui_show_xml(xml_file, string_mode=False):
    # read messages from XML
    if string_mode:
        dom = xml.dom.minidom.parseString(xml_file)
    else:
        dom = xml.dom.minidom.parse(xml_file)
    # customise indentation to make output seem less verbose
    pretty_xml = dom.toprettyxml(indent="  ")
    # show messages in console
    print(pretty_xml)


def ui_read_filter_and_show_results(tree, action='finding'):
    # read messages from XML
    root = tree.getroot()
    # read message filter (in any of these formats: element=value , element, value) from console
    message_filter = input('Please enter the filter you wish to use for {}: '.format(action))

    element = None
    value = None
    # if both tag and value have been specified, parse them
    eq_ind = message_filter.find('=')
    if eq_ind != -1:
        element = (message_filter[:eq_ind]).strip()
        value = (message_filter[eq_ind + 1:]).strip()

    results = []
    # filter messages by filter
    # if both tag and value present, perform an overall search
    if element and value:
        results = filter_by_element_and_value(root, element, value)
    else:
        results, element, value = filter_by_string(root, message_filter)

    query_str = '{} = {}'.format(element, value)
    if element == value == '?':
        query_str = message_filter
    ui_pretty_print('{} result(s) with {}'.format(len(results), query_str))
    # show matching messages in console
    for result in results:
        child_node = list(result.keys())[0]
        string_xml = ET.tostring(child_node)
        ui_show_xml(string_xml, True)
        # draw a line seperating results
        print('-' * len(string_xml))

    return results


no_xml_error = 'No XML file found!'

if __name__ == '__main__':
    # parse command line to detect mode
    # this approach has been chosen since it works with pipes, prudent for automation
    parser = argparse.ArgumentParser(description='Read from console and write into an XML file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='Add message to XML')
    group.add_argument('-d', '--delete', action='store_true', help='Delete message from XML')
    group.add_argument('-r', '--read', action='store_true', help='Read messages from XML')
    group.add_argument('-f', '--find', action='store_true', help='Find message in XML')

    # Print help in case of no arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # check if the XML file is present in default path (current directory)
    xml_file = glob('*.xml')
    if xml_file:
        # note: in case of multiple XMLs, only the first one is selected for simplicity
        xml_file = xml_file[0]

    if args.add:
        # read message
        message = input('Please enter your message\n')
        # add message to existing XML
        if xml_file:
            # add to the xml
            add_to_xml(xml_file, message)
        else:
            # or create new XML
            create_xml(message)

    if args.delete:
        # read message deletion filter from console and show matching results
        tree = ET.parse(xml_file)
        results = ui_read_filter_and_show_results(tree, action='deletion')
        # wait for delete-confirmation
        if results:
            choice = input('Are you sure you wish to delete the XML segment(s)? (y/n): ')
            if (choice.lower() == 'y'):
                # delete messages
                for result in results:
                    # find the parent
                    parent = list(result.values())[0]
                    child = list(result.keys())[0]
                    parent.remove(child)

                tree.write(xml_file)
                # show new remaining messages
                ui_show_xml(xml_file)
            else:
                print('No deletion done!')

    if args.read:
        # read messages from XML and show in console
        if xml_file:
            ui_show_xml(xml_file)
        else:
            print(no_xml_error)

    if args.find:
        # read find filter from console and show matching results
        if xml_file:
            tree = ET.parse(xml_file)
            results = ui_read_filter_and_show_results(tree)
        else:
            print(no_xml_error)