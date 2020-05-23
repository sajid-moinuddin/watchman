import glob
import os
import shutil
import logging

from pybuilder.core import use_plugin, init, Author, task
from pybuilder.utils import assert_can_execute

use_plugin("python.core")
# use_plugin("python.unittest")
# use_plugin("python.flake8")
# use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("copy_resources")

description = "Night gathers, and now my watch begins..."
name = "watchman"
default_task = ['publish']


@task
def run():
    from watchman import main
    main.begin(logging.DEBUG)        

@init
def set_properties(project):
    install_dependencies(project)
    project.get_property("copy_resources_glob").append("src/main/resources/vector_alert.wav")
    project.get_property("copy_resources_glob").append("src/main/resources/vector_bell_whistle.wav")
    project.set_property("copy_resources_target", "$dir_dist")

    project.install_file('/usr/local/share/vector_bell_whistle.wav', "src/main/resources/vector_bell_whistle.wav")
    project.install_file('/usr/local/share/vector_alert.wav', "src/main/resources/vector_alert.wav")
    
#TODO: find a way to install brew install mpg321
@task
def install_dependencies(project):
    project.depends_on('docopt')
    project.depends_on('aiogrpc', '1.4')
    project.depends_on('cryptography')
    project.depends_on('flask')
    project.depends_on('googleapis-common-protos')
    project.depends_on('numpy','1.11')
    project.depends_on('Pillow','3.3')
    project.depends_on('PyYAML')
    project.depends_on('simplejson')
    project.depends_on('python-dateutil')
    project.depends_on('pypubsub','4.0.3')
    project.depends_on('requests')
    project.depends_on('nrql-simple')
    project.depends_on('simpleaudio')
    project.depends_on('gTTS')
    project.depends_on('anki_vector')
    project.depends_on('text-to-image')
    project.depends_on('kubernetes')