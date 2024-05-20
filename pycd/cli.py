#!/usr/bin/env python3

import click
from pathlib import Path
from pycd.db import DB
import os

class DefaultCommandGroup(click.Group):

    def __init__(self, *args, **kwargs):
        self.default_command = kwargs.pop('default_command', None)
        super().__init__(*args, **kwargs)
    
    def resolve_command(self, ctx, args):
        try:
            return super().resolve_command(ctx, args)
        except click.UsageError:
            args.insert(0, self.default_command)
            return super().resolve_command(ctx, args)

@click.group(cls=DefaultCommandGroup, default_command="cd")
@click.pass_context
def entry_point(ctx):
    db_path = Path(os.getenv("HOME"))/".config"/"pycd"
    ctx.obj = DB(db_path)


@entry_point.command()
@click.argument("dir",nargs=-1)
@click.pass_context
def cd(ctx,dir):
    obj = ctx.obj
    print(obj.script(dir))

@entry_point.command()
@click.argument("dir")
@click.pass_context
def add(ctx,dir):
    obj = ctx.obj
    obj.add(dir)

@entry_point.command()
@click.option("--view","-v",help="View config data",is_flag=True)
@click.option("--all-matches","-a",multiple=True)
@click.pass_context
def config(ctx,view,all_matches):
    obj = ctx.obj
    display_only_path = True

    if view:
        print(obj.lf.load())
        display_only_path = False

    if all_matches:
        print(obj.lf.get_all_matches_by_rank(all_matches))
        display_only_path = False

    if display_only_path:
        print(obj.lf.fname)

if __name__ == "__main__":
    entry_point()
