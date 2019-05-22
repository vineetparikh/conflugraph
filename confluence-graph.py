#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import sys
import getpass
import textwrap

import requests
from requests_ntlm import HttpNtlmAuth
from graphviz import Digraph

from collections import OrderedDict

def log(*args):
    print(*args, file=sys.stderr)

class PageContainer(object): # class to contain info about individual pages
    def __init__(self, page_id, page_title):
        self.page_id = page_id
        self.page_title = page_title

class ConfluSearch(object): # factory class to actually handle requests
    def __init__(self,base_url,session):
        self.base_url = base_url
        self.url = base_url + '/rest/api'
        self.session = session

    def get(self, uri, params):
        headers = {'Content-Type' : 'application/json'}
        url = self.url + uri
        return self.session.get(url,params=params)

    def get_root(self,space_key):
        log('Getting root page of ' + space_key)
        response = self.get('/space/%s/content/page' % space_key,params={'depth':'root'})
        response.raise_for_status()
        content = response.json()
        # we're assuming the space exists somewhere
        root = content["results"][0] # the first/only result
        return PageContainer(root["id"],root["title"])

    def get_children(self,page_object): # the object has the id and title in it
        # will return pageobjects, since we need to expand by page
        log('Getting children of page with id '+page_object.page_id)
        response = self.get('/content/%s/child' % page_object.page_id,params={'expand':'page'})
        response.raise_for_status()
        ret = []
        content = response.json()
        for x in content["page"]["results"]:
            y = PageContainer(x["id"],x["title"])
            ret.append(y)
        return ret

# Returns a digraph based on graphviz. We assume spacekey is a valid spacekey
def build_graph_data(spaceKey, conflu, splines):
    log('Creating graph from key %s' % spaceKey)
    graph = Digraph(comment = "Visualized space from key %s" % spaceKey, format='svg', engine='sfdp')
    graph.attr(overlap='false')
    graph.attr(splines=splines)
    root_node = conflu.get_root(spaceKey)
    graph.node(root_node.page_id, "%s: %s" % (root_node.page_id, root_node.page_title))
    num_nodes = 1
    num_edges = 0
    need_offspring=[root_node]
    while (len(need_offspring)!=0):
        num_nodes+=1
        node_to_consider = need_offspring.pop(0)
        kids = conflu.get_children(node_to_consider)
        for k in kids:
            graph.node(k.page_id, "%s: %s" % (k.page_id, k.page_title))
            graph.edge(node_to_consider.page_id,k.page_id)
            num_edges+=1
            need_offspring.append(k) # append the kid on
    log('Number of nodes made %s'%num_nodes)
    log('Number of edges made %s'%num_edges)
    return graph

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', dest='user', default=None, help='Username to access Confluence')
    parser.add_argument('-p', '--password', dest='password', default=None, help='Password to access Confluence')
    parser.add_argument('-k', '--confluence', dest='confluence_url', default='http://confluence.example.com', help='Confluence Base URL')
    parser.add_argument('-f', '--file', dest='image_file', default='conflu-graph', help='Filename to write image to')
    parser.add_argument('-s', '--space', dest='space_key', default=None, help='The Confluence space key')
    parser.add_argument('-l', '--splines', dest='splines', default='false', help='Boolean: whether to route edges around nodes or not (configurable for performance reasons)')
    return parser.parse_args()


def main():
    options = parse_args()

    user = options.user if options.user is not None \
                else raw_input('Username: ')
    password = options.password if options.password is not None \
                else getpass.getpass('Password: ')
    session = requests.Session()
    session.auth = HttpNtlmAuth('domain\\'+user,password) # Cornell uses ntlm auth, but this can be ported based on the requests library

    confluence = ConfluSearch(options.confluence_url, session)

    graph = build_graph_data(options.space_key,confluence,options.splines)
    graph.render(options.image_file,view=True)


if __name__ == '__main__':
    main()
