workspace(name = "aoc2022")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# PYTHON

http_archive(
    name = "rules_python",
    sha256 = "bc4e59e17c7809a5b373ba359e2c974ed2386c58634819ac5a89c0813c15705c",
    strip_prefix = "rules_python-0.15.1",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.15.1.tar.gz",
)

load("@rules_python//python:pip.bzl", "pip_parse")
pip_parse(
    name = "py_deps",
    requirements_lock = "//3rd_party/python:requirements.txt",
)

load("@py_deps//:requirements.bzl", "install_deps")

install_deps()

# GO
http_archive(
    name = "io_bazel_rules_go",
    sha256 = "ae013bf35bd23234d1dea46b079f1e05ba74ac0321423830119d3e787ec73483",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.36.0/rules_go-v0.36.0.zip",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.36.0/rules_go-v0.36.0.zip",
    ],
)


# GAZELLE
http_archive(
    name = "bazel_gazelle",
    sha256 = "448e37e0dbf61d6fa8f00aaa12d191745e14f07c31cabfa731f0c8e8a4f41b97",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.28.0/bazel-gazelle-v0.28.0.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.28.0/bazel-gazelle-v0.28.0.tar.gz",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

load("//:3rd_party/go/deps.bzl", "go_dependencies")

# gazelle:repository_macro 3rd_party/go/deps.bzl%go_dependencies
go_dependencies()

go_rules_dependencies()

go_register_toolchains(version = "1.19.3")

gazelle_dependencies()

# BUILDTOOLS
http_archive(
    name = "com_github_bazelbuild_buildtools",
    sha256 = "ae34c344514e08c23e90da0e2d6cb700fcd28e80c02e23e4d5715dddcb42f7b3",
    strip_prefix = "buildtools-4.2.2",
    urls = [
        "https://github.com/bazelbuild/buildtools/archive/refs/tags/4.2.2.tar.gz",
    ],
)
