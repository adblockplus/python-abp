# python-abp

This repository contains the script that is used for building Adblock Plus
filter lists from the form in which they are authored into the format suitable
for consumption by the adblocking software.

## Installation

Prerequisites:

* Linux, Mac OS X or Windows (any modern Unix should work too),
* Python (2.7 or 3.5),
* pip.

To install:

    $ pip install -U python-abp

## Rendering of filter lists

The filter lists are originally authored in relatively smaller parts focused
on a particular type of filters, related to a specific topic or relevant
for particular geographical area.
We call these parts _filter list fragments_ (or just _fragments_)
to distinguish them from full filter lists that are
consumed by the adblocking software such as Adblock Plus.

Rendering is a process that combines filter list fragments into a filter list.
It starts with one fragment that can include other ones and so forth.
The produced filter list is marked with a version, a timestamp and 
a [checksum](https://adblockplus.org/filters#special-comments).

Python-abp contains a script that can do this called `flrender`:

    $ flrender fragment.txt filterlist.txt

This will take the top level fragment in `fragment.txt`, render it and save into
`filterlist.txt`.

Fragments might reference other fragments that should be included into them.
The references come in two forms: http(s) includes and local includes:

    %include http://www.server.org/dir/list.txt%
    %include easylist:easylist/easylist_general_block.txt

The first instruction contains a URL that will be fetched and inserted at the
point of reference. 
The second one contains a path inside easylist repository.
`flrender` needs to be able to find a copy of the repository on the local
filesystem. We use `-i` option to point it to to the right directory:

    $ flrender -i easylist=/home/abc/easylist input.txt output.txt

Now the second reference above will be resolved to
`/home/abc/easylist/easylist/easylist_general_block.txt` and the fragment will
be read from this file.

Directories that contain filter list fragments that are used during rendering
are called sources.
They are normally working copies of the repositories that contain filter list
fragments.
Each source is identified by a name: that's the part that comes before ":"
in the include instruction and it should be the same as what comes before "="
in the `-i` option.

Commonly used sources have generally accepted names. For example the main
EasyList repository is referred to as `easylist`.
If you don't know all the source names that are needed to render some list,
just run `flrender` and it will report what it's missing:

    $ flrender easylist.txt output/easylist.txt
    Unknown source: 'easylist' when including 'easylist:easylist/easylist_gener
    al_block.txt' from 'easylist.txt'

You can clone the necessary repositories to a local directory and add `-i`
options accordingly.

## Testing

Unit tests for `python-abp` are located in the `/tests` directory.
[Pytest](http://pytest.org/) is used for quickly running the tests
during development.
[Tox](https://tox.readthedocs.org/) is used for testing in different
environments (Python 2.7, Python 3.5 and PyPy) and code quality
reporting.

In order to execute the tests, first create and activate development
virtualenv:

    $ python setup.py devenv
    $ . devenv/bin/activate

With the development virtualenv activated use pytest for a quick test run:

    (devenv) $ py.test tests

and tox for a comprehensive report:

    (devenv) $ tox
