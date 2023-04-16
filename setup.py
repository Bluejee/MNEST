import setuptools

with open('README.md', 'r') as f:
    long_disc = f.read()

setuptools.setup(
    include_package_data=True,
    name='mnest',
    version='0.1.0',
    author='Balakrishna Prabhu B N',
    author_email='balakrishnaprabhu1999@gmail.com',
    description='MNEST (Multi-agent Neuro Evolution Simulation Toolkit) is a software framework designed to model and study emergent behavior in complex systems',
    long_description=long_disc,
    long_description_content_type="text/markdown",
    keywords=['simulation', 'multi-agent', 'neuro-evolution', 'AI', 'ML', 'Biology', 'Physics', 'Computation',
              'Complex Systems'],
    url='https://github.com/Bluejee/SEAN',
    packages=['mnest'],
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
