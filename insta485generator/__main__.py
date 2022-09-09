"""Build static HTML site from directory of HTML templates and plain files."""

import pathlib
import json
import sys
import click
import jinja2
import os
import shutil


@click.command()
@click.argument('input_dir')
@click.option('-o','--output', help='Output directory.')
@click.option('-v','--verbose', is_flag=True,default=False, help='Print more output.')


def main(input_dir,verbose,output):
    """Templated static website generator."""

    input_dir_string = input_dir
    input_dir = pathlib.Path(input_dir)  # convert str to Path object
    if not input_dir.exists():
        print("Input Directory does not exist")
        exit(1)


    infile_path = pathlib.Path(input_dir_string+ "/config.json")
    url = ""
    template = ""
    context = ""
    with infile_path.open() as fh:
        data = json.load(fh)
        for entry in data:
            url += f"{entry['url']}"
            template += f"{entry['template']}"
            context += f"{entry['context']}"
            context2 = entry['context']

    url = url.lstrip("/")  # remove leading slash
    output_dir = input_dir/"html"  # default, can be changed with --output option
    if output:
        output_dir = pathlib.Path(output)
    output_path = output_dir/url/"index.html"


    from jinja2 import Environment, PackageLoader, select_autoescape
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(input_dir)+"/templates"),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )


    template = env.get_template(template)

    if output_dir.exists():
        print("Output Directory already exists")
        exit(1)

    s = pathlib.Path(input_dir_string + "/static")
    t = pathlib.Path(output_dir)
    if s.exists():
        shutil.copytree(s,t,dirs_exist_ok=True)
        if verbose:
            print("Copied "+str(input_dir) + " -> "+str(output_dir))

    q = pathlib.Path(output_dir)
    q.mkdir(parents=False,exist_ok=True)

    p = pathlib.Path(output_path)
    p.touch(exist_ok=False)
    p.write_text(template.render(**context2))
    if verbose:
        print("Rendered "+str(template) + " -> "+str(output_path))



if __name__ == "__main__":
    main()
