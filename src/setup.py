from setuptools import setup
from distutils.command.sdist import sdist
import os
import sys

class lmi_sdist(sdist):
    """
    Custom 'setup.py sdist' command, which regenerates documentation
    sources when creating a tarball.
    """

    def run(self):
        """
        Regenerate documentation source files and create tarball.
        """
        ret = os.system("make -C doc/admin src")
        if ret:
            print "Failed to compile documentation sources, exiting."
            sys.exit(ret)
        # sdist is old-style class
        sdist.run(self)

setup(
    name='openlmi-storage',
    description='Anaconda Storage Provider',
    author='Jan Safranek',
    author_email='jsafrane@redhat.com',
    url='https://fedorahosted.org/openlmi/',
    version='0.7.0',
    package_dir={'': 'src'},
    namespace_packages = ['lmi'],
    packages=['lmi', 'lmi.storage', 'lmi.storage.util'],
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Systems Administration',
    ],

    cmdclass={
        'sdist': lmi_sdist
    }
)
