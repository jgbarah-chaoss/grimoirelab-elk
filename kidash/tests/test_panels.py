#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Alvaro del Castillo <acs@bitergia.com>
#

import logging
import json
import os.path
import sys
import unittest

if '..' not in sys.path:
    sys.path.insert(0, '..')

from grimoire_elk.panels import get_search_from_vis_json, Panel, \
    Panel_File_Not_Found, Panel_File_Wrong_Format

class TestPanel(unittest.TestCase):
    """Unit tests for Panel class."""

    def setUp(self):
        self.git_panel_file = os.path.join('data', 'git_panel.json')
        with open(self.git_panel_file) as file:
            self.git_panel = json.load(file)

        self.github_panel_file = os.path.join('data', 'github_panel.json')
        with open(self.github_panel_file) as file:
            self.github_panel = json.load(file)

        file_name = os.path.join('data', 'git_panel_elements.json')
        with open(file_name) as file:
            self.git_panel_elements = json.load(file)

        file_name = os.path.join('data', 'github_panel_elements.json')
        with open(file_name) as file:
            self.github_panel_elements = json.load(file)

        file_name = os.path.join('data', 'git_panel_elements_index.json')
        with open(file_name) as file:
            self.git_panel_elements_index = json.load(file)

    def test_read_from_file(self):
        """test read_from_file reading from file."""

        panel = Panel()
        panel.read_from_file(self.git_panel_file)
        self.assertDictEqual(panel.panel, self.git_panel)
        self.assertEqual(panel.source, 'dir')

        panel = Panel()
        panel.read_from_file(self.github_panel_file)
        self.assertDictEqual(panel.panel, self.github_panel)
        self.assertEqual(panel.source, 'dir')

        with self.assertRaises(Panel_File_Not_Found):
            panel.read_from_file('data/git_panel2.json')

    def test_read_from_module(self):
        """test read_from_file reading from module.

        File names in this test do not exist, therefore they will be
        found in the panels module. Look for files in panels module
        with the two conventions supported: just the file name,
        or the file name prefixed by panels/json.
        """

        panel = Panel()
        panel.read_from_file('git.json')
        self.assertDictEqual(panel.panel, self.git_panel)
        self.assertEqual(panel.source, 'module')
        panel = Panel()
        panel.read_from_file('panels/json/git.json')
        self.assertDictEqual(panel.panel, self.git_panel)
        self.assertEqual(panel.source, 'module')

    def test_read_from_file_wrong(self):
        """test read_from_file reading from wrong file."""

        panel = Panel()
        with self.assertRaises(Panel_File_Wrong_Format):
            # Incorrect format, missing 'id' field
            panel.read_from_file('data/git_panel_wrong.json')
        panel = Panel()
        with self.assertRaises(Panel_File_Wrong_Format):
            # Incorrect JSON, extra ',' after first 'searchSourceJSON' field
            panel.read_from_file('data/git_panel_wrong2.json')

    def test_build_elements(self):
        """test _build_elements."""

        panel = Panel()
        panel.read_from_file(self.git_panel_file)
        elements = panel._build_elements()
#        json.dump(elements, open('data/git_panel_elements.json','w'), sort_keys=True, indent=2)
        self.assertDictEqual(elements, self.git_panel_elements)

        panel = Panel()
        panel.read_from_file(self.github_panel_file)
        elements = panel._build_elements()
#        json.dump(elements, open('data/github_panel_elements.json','w'), sort_keys=True, indent=2)
        self.assertDictEqual(elements, self.github_panel_elements)

    def test_add_index_elements(self):
        """test _add_index_elements."""

        panel = Panel()
        panel.read_from_file(self.git_panel_file)
        elements = panel._build_elements()
        panel._add_index_elements(elements)
        json.dump(elements, open('data/git_panel_elements_index.json','w'), sort_keys=True, indent=2)
        self.assertDictEqual(elements, self.github_panel_elements_index)

class TestPanels(unittest.TestCase):
    """Functional tests for Kibana panels.py misc methods."""

    visualizations = [
        {
            "id": "jira_main_metrics",
            "value": {
                "description": "",
                "kibanaSavedObjectMeta": {
                    "searchSourceJSON": "{\"index\":\"jira\",\"query\":{\"query_string\":{\"query\":\"*\",\"analyze_wildcard\":true}},\"filter\":[]}"
                },
                "title": "jira_main_metrics",
                "uiStateJSON": "{}",
                "version": 1,
                "visState": "{\"title\":\"jira_main_metrics\",\"type\":\"metric\",\"params\":{\"fontSize\":\"12\"},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{\"customLabel\":\"# Issues\"}},{\"id\":\"2\",\"type\":\"cardinality\",\"schema\":\"metric\",\"params\":{\"field\":\"author_uuid\",\"customLabel\":\"# Submitters\"}},{\"id\":\"3\",\"type\":\"cardinality\",\"schema\":\"metric\",\"params\":{\"field\":\"project_name\",\"customLabel\":\"# Projects\"}}],\"listeners\":{}}"
            }
        },
        {
            "id": "github_issues_main_metrics",
            "value": {
                "description": "",
                "kibanaSavedObjectMeta": {
                    "searchSourceJSON": "{\"filter\":[]}"
                },
                "savedSearchId": "Search:_pull_request:false",
                "title": "github_issues_main_metrics",
                "uiStateJSON": "{}",
                "version": 1,
                "visState": "{\"title\":\"github_issues_main_metrics\",\"type\":\"metric\",\"params\":{\"fontSize\":\"12\"},\"aggs\":[{\"id\":\"1\",\"type\":\"count\",\"schema\":\"metric\",\"params\":{\"customLabel\":\"Issues\"}},{\"id\":\"2\",\"type\":\"cardinality\",\"schema\":\"metric\",\"params\":{\"field\":\"author_uuid\",\"customLabel\":\"# Submitters\"}},{\"id\":\"3\",\"type\":\"cardinality\",\"schema\":\"metric\",\"params\":{\"field\":\"repository\",\"customLabel\":\"# Repositories\"}}],\"listeners\":{}}"
            }
        }
    ]
    def test_init(self):
        pass

    def test_get_search_from_vis_json(self):
        """Test get_search_from_vis_json"""

        good_searchs = [None, 'Search:_pull_request:false']
        for i,vis in enumerate(self.visualizations):
            computed_search = get_search_from_vis_json(vis['value'])
            self.assertEqual(computed_search, good_searchs[i])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    unittest.main()
