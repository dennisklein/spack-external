# Copyright 2020 GSI Helmholtz Centre for Heavy Ion Research GmbH, Darmstadt
# Copyright 2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#  import llnl.util.tty as tty

from spack.architecture import platform
from spack.platforms.linux import Linux

from package_manager import PackageManager


class Dnf(PackageManager):
    """Represents the DNF package manager on Fedora Linux distros"""

    priority = 90

    def __repr__(self):
        return 'dnf'

    @classmethod
    def detect(cls):
        os = str(platform().operating_system('default_os'))
        return isinstance(platform(), Linux) and os.startswith('fedora')
