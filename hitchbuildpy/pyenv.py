from commandlib import CommandPath, Command
from path import Path
import hitchbuild


class PyenvBuild(hitchbuild.HitchBuild):
    def __init__(self, version):
        self.version = version

    @property
    def basepath(self):
        return self.build_path.joinpath("python{0}".format(self.version))

    @property
    def bin(self):
        return CommandPath(self.basepath/"bin")

    def fingerprint(self):
        return str(hash(self.version))

    def clean(self):
        self.basepath.rmtree(ignore_errors=True)

    def build(self):
        if not self.basepath.exists():
            self.basepath.mkdir()

            Command(
                Path(__file__).dirname().abspath().joinpath("bin", "python-build")
            )(self.version, self.basepath).run()

            self.bin.easy_install("--upgrade", "setuptools").run()
            self.bin.easy_install("--upgrade", "pip").run()
            self.bin.pip("install", "virtualenv", "--upgrade")\
                    .without_env("PIP_REQUIRE_VIRTUALENV").run()
        self.verify()

    def verify(self):
        assert self.version in self.bin.python("--version").output(), \
            "'{0}' expected to be found in python --version, got:\n{1}".format(
                self.version,
                self.bin.python("--version").output(),
            )
