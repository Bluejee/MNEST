import setuptools

with open('README.md', 'r') as f:
    long_disc = f.read()

setuptools.setup(
    include_package_data=True,
    name='sean',
    version='0.1.0',
    author='Balakrishna Prabhu B N',
    author_email='balakrishnaprabhu1999@gmail.com',
    description='SEAN (A Simulation Environment for Agent-based Neuro-evolution) is a Python package for building and simulating artificial intelligence in multi agent-based models.',
    long_description=long_disc,
    long_description_content_type="text/markdown",
    keywords=['simulation', 'multi-agent', 'neuro-evolution', 'AI', 'ML', 'Biology', 'Physics', 'Computaion',
              'Complex Systems'],
    url='https://github.com/Bluejee/SEAN',
    packages=['sean'],
    install_requires=['numpy==1.24.2', 'pygame==2.3.0', 'scipy==1.10.1'],
    python_requires='>=3.7',
    license='GPL-3.0-or-later',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ]
)
