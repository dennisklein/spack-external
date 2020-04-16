# Copyright 2020 GSI Helmholtz Centre for Heavy Ion Research GmbH, Darmstadt
# Copyright 2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#  import llnl.util.tty as tty

from spack.architecture import platform
from spack.platforms.linux import Linux
from spack.version import Version
from spack.util.executable import which

from package_manager import PackageManager


class Dnf(PackageManager):
    """Represents the dnf package manager on Fedora Linux distros"""

    priority = 90

    def __init__(self):
        dnf = which('dnf', required=True)
        dnf_version = Version(
            dnf('--version', output=str).splitlines()[0].strip())
        super(Dnf, self).__init__(dnf, dnf_version)

    @classmethod
    def detect(cls):
        os = str(platform().operating_system('default_os'))
        return isinstance(platform(), Linux) and os.startswith('fedora')
