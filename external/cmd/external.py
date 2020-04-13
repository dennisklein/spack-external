# Copyright 2020 GSI Helmholtz Centre for Heavy Ion Research GmbH, Darmstadt
# Copyright 2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty

import spack
import spack.environment as ev


description = "manipulate external package config files"
section = "system"
level = "short"

subcommands = [
    ['status', 'st'],
]


def external_status_setup_parser(subparser):
    """show which external packages are used"""
    pass


def external_status(args):
    """spack external status"""
    env = ev.get_env(args, 'env status')
    if env:
        env.concretize()

        def _tree_to_display(spec):
            return spec.tree(
                recurse_dependencies=True,
                status_fn=spack.spec.Spec.install_status,
                hashlen=8, hashes=True, show_external=True)

        for user_spec, concrete_spec in env.concretized_specs():
            tty.msg('Concretized {0}'.format(user_spec))
            sys.stdout.write(_tree_to_display(concrete_spec))
            print('')
    else:
        tty.msg('No active environment')


#: Dictionary mapping subcommand names and aliases to functions
subcommand_functions = {}


def setup_parser(subparser):
    """spack external"""
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='external_command')

    for name in subcommands:
        if isinstance(name, (list, tuple)):
            name, aliases = name[0], name[1:]
        else:
            aliases = []

        # add commands to subcommands dict
        function_name = 'external_%s' % name
        function = globals()[function_name]
        for alias in [name] + aliases:
            subcommand_functions[alias] = function

        # make a subparser and run the command's setup function on it
        setup_parser_cmd_name = 'external_%s_setup_parser' % name
        setup_parser_cmd = globals()[setup_parser_cmd_name]

        subsubparser = sp.add_parser(
            name, aliases=aliases, help=setup_parser_cmd.__doc__)
        setup_parser_cmd(subsubparser)


def external(parser, args):
    """Look for a function called external_<name> and call it."""
    action = subcommand_functions[args.external_command]
    action(args)
