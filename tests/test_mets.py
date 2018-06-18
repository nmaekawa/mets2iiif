#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from lxml import etree
import os
import pytest
import re

from mets2iiif.mets import main
from mets2iiif.mets import translate_range
from mets2iiif.mets import translate_ranges



here = os.path.abspath(os.path.dirname(__file__))

def readfile(filepath):
    with open(filepath, 'r') as f:
        data = f.read()

    return data

doc_id = 'sample'

@pytest.fixture
def mets_xmlstring():
    """sample mets xml."""
    filename = os.path.join(here, 'files/{}.xml'.format(doc_id))
    return readfile(filename)

@pytest.fixture
def mets_range_json():
    """sample json input for translate_ranges()."""
    filename = os.path.join(here, 'files/ranges-{}.json'.format(doc_id))
    content = readfile(filename)
    return json.loads(content)


@pytest.mark.usefixtures('mets_xmlstring')
def test_readfile(mets_xmlstring):
    assert mets_xmlstring is not None


@pytest.mark.usefixtures('mets_range_json')
def test_range(mets_range_json):
    r = mets_range_json['result'][0]

    iiif_range, r_list = translate_range(r, '0', 'iiif.lib.harvard.edu/manifests')

    assert iiif_range is not None
    assert r_list is not None
    assert r_list[0] == iiif_range


@pytest.mark.usefixtures('mets_range_json')
def test_ranges(mets_range_json):
    r = mets_range_json['result']

    iiif_range = translate_ranges(r, 'iiif.lib.harvard.edu/manifests')

    assert iiif_range is not None
    assert len(iiif_range) == 8
    assert 'viewingHint' in iiif_range[0]


#@pytest.mark.skip(reason='skip processing whole mets xml')
@pytest.mark.usefixtures('mets_xmlstring')
def test_translate(mets_xmlstring):
    response = main(
        mets_xmlstring, doc_id, 'mets', 'iiif.lib.harvard.edu')

    assert response is not None

    # main() returns a string, so back to json
    iiif_range = json.loads(response)

    assert 'structures' in iiif_range
    assert len(iiif_range['structures']) == 2
    assert 'viewingHint' in iiif_range['structures'][0]

    #print('---------------------------------------------')
    #print(response)
    #print('---------------------------------------------')
    #assert response == 'hahahaha'

