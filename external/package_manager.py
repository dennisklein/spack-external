# Copyright 2020 GSI Helmholtz Centre for Heavy Ion Research GmbH, Darmstadt
# Copyright 2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

import llnl.util.tty as tty
from llnl.util.lang import memoized, list_modules

import spack.error as serr
from spack.util.naming import mod_to_class

import paths


class NoSystemPackageManagerError(serr.SpackError):
    def __init__(self):
        super(NoSystemPackageManagerError, self).__init__(
            "Could not determine a system package manager for this machine")


class PackageManager(object):
    """Abstract base class for platform-specific package manager"""

    priority = None

    @classmethod
    def detect(cls):
        """ Subclass is responsible for implementing this method.
            Returns True if the PackageManager class detects that
            it is the current system package manager and False if
            it's not.
        """
        raise NotImplementedError('abstract method called')

    def __init__(self, exe, version):
        self._exe = exe
        self._version = version

    def __repr__(self):
        return '%s %s' % (self.exe, self.version)

    @property
    def exe(self):
        return self._exe

    @property
    def version(self):
        return self._version


@memoized
def all_package_managers():
    classes = []
    mod_path = paths.package_managers_path
    parent_module = "package_managers"

    for name in list_modules(mod_path):
        mod_name = '%s.%s' % (parent_module, name)
        class_name = mod_to_class(name)
        mod = __import__(mod_name, fromlist=[class_name])
        if not hasattr(mod, class_name):
            tty.die('No class %s defined in %s' % (class_name, mod_name))
        cls = getattr(mod, class_name)
        if not inspect.isclass(cls):
            tty.die('%s.%s is not a class' % (mod_name, class_name))

        classes.append(cls)

    return classes


@memoized
def system_package_manager():
    """Detects the system package manager for this machine"""

    package_managers_list = all_package_managers()
    package_managers_list.sort(key=lambda a: a.priority)

    for package_manager_cls in package_managers_list:
        if package_manager_cls.detect():
            return package_manager_cls()

    raise NoSystemPackageManagerError()
