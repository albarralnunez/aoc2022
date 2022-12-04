"""Wrap pytest"""

load("@rules_python//python:defs.bzl", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

def pytest_test(name, srcs, deps = [], args = [], data = [], **kwargs):
    """
        Call pytest
    """
    py_test(
        name = name,
        srcs = [
            "//tools/pytest:pytest_wrapper.py",
        ] + srcs,
        main = "//tools/pytest:pytest_wrapper.py",
        args = [
            "--junitxml=/tmp/junit/report_{}.xml".format(name),
            "--capture=no",
            "--black",
            "--mypy",
        ] + args + ["$(location :%s)" % x for x in srcs],
        python_version = "PY3",
        srcs_version = "PY3",
        deps = deps + [
            requirement("pytest"),
            requirement("pytest-black"),
            requirement("pytest-mypy"),
        ],
        data = [
            "//:pyproject.toml",
            "//:pytest.ini",
        ] + data,
        **kwargs
    )
