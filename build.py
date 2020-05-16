import glob
import os
import shutil

from pybuilder.core import use_plugin, init, Author, task
from pybuilder.utils import assert_can_execute

use_plugin("python.core")
# use_plugin("python.unittest")
# use_plugin("python.flake8")
# use_plugin("python.coverage")
use_plugin("python.distutils")


name = "watchman"
default_task = "publish"


@init
def set_properties(project):
    install_dependencies(project)

@task
def install_dependencies(project):
    project.depends_on('aiogrpc', '1.4')
    project.depends_on('cryptography')
    project.depends_on('flask')
    project.depends_on('googleapis-common-protos')
    project.depends_on('numpy','1.11')
    project.depends_on('Pillow','3.3')
    project.depends_on('python-dateutil')
    project.depends_on('pypubsub','4.0.3')
    project.depends_on('requests')
    project.depends_on('nrql-simple')
    project.depends_on('simpleaudio')
    project.depends_on('gTTS')