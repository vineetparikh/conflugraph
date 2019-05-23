conflugraph
=====================

Graph visualizer for page hierarchy of a Confluence space

Uses Confluence REST API for fetching information on spaces. Authorized with NTLM (although it's possible to change authorization methods easily)
Uses graphviz for graphical presentation

Requirements:
=============
* Python 2.7+
* [requests](http://docs.python-requests.org/en/master/)
* [ntlm-auth](https://pypi.org/project/ntlm-auth/)
* [requests-ntlm](https://pypi.org/project/requests_ntlm/)
* [graphviz](https://pypi.org/project/graphviz/)

Docker support is still a work in progress

Usage:
======
```bash
$ git clone https://github.com/vineetparikh/conflugraph.git
$ cd conflugraph
$ sudo -H pip install -r requirements.txt
$ python confluence-graph.py --user=your-username --password=your-password --confluence=url-of-your-confluence-site --space=your-confluence-space-key
```

Advanced Usage:
===============

List of all configuration options with descriptions:

```
python jira-dependency-graph.py --help
```

### Configuring Splines
While this doesn't matter as much with small graphs, as graphs scale with nodes and edges, edges tend to overlap nodes rather annoyingly. Fixing this, especially for bigger graphs, means configuring splines, but this vastly increases rendering time.

```bash
$ python jira-dependency-graph.py --user=your-jira-username --password=your-jira-password --jira=url-of-your-jira-site --exclude-link 'is required by' --exclude-link 'duplicates' issue-key
```


### Authentication

This tool configures NTLM authentication, as this was required for testing with Cornell's Confluence system. However, it's fairly easy to port between authentication types.

