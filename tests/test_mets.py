#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from lxml import etree
import os
import pytest
import re

from mets2iiif.mets import main
from mets2iiif.mets import try10



here = os.path.abspath(os.path.dirname(__file__))

def readfile(filepath):
    with open(filepath, 'r') as f:
        data = f.read()

    return data

#doc_id = '5981093'
doc_id = '4771822'



@pytest.fixture
def mets_xmlstring():
    """sample mets xml from hul
    """
    filename = os.path.join(here, 'files/{}.xml'.format(doc_id))
    return readfile(filename)


@pytest.fixture
def drs_solr_jsonstring():
    filename = os.path.join(here, 'files/{}-object-query.json'.format(doc_id))
    return readfile(filename)

@pytest.fixture
def mets_range_json():
    filename = os.path.join(here, 'files/ranges-{}.json'.format(doc_id))
    content = readfile(filename)
    return json.loads(content)

@pytest.mark.usefixtures('mets_xmlstring')
def test_readfile(mets_xmlstring):
    assert mets_xmlstring is not None


#@pytest.mark.usefixtures('mets_xmlstring')
#def test_translate(mets_xmlstring):
#    response = main(
#        mets_xmlstring, doc_id, 'mets', 'iiif.lib.harvard.edu')
#
#    assert response is not None


@pytest.mark.usefixtures('mets_range_json')
def test_range(mets_range_json):
    r = mets_range_json['result'][0]

    iiif_range, r_list = try10(r, 0, 'iiif.lib.harvard.edu/manifests')

    assert iiif_range is not None
    assert r_list is not None

    print(json.dumps(iiif_range, sort_keys=True, indent=4))
    print('-------------------------------------------------------------')
    print(json.dumps(r_list, sort_keys=True, indent=4))
    print('-------------------------------------------------------------')
    assert iiif_range == 'hahahaha'

