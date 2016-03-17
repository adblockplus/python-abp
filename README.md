# python-abp

A library for working with Adblock Plus filter lists

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
