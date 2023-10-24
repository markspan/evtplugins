import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="evt_plugin_collection", 
    version="1.00.00",
    author="M.M.Span, M.Stokroos",
    author_email="m.m.span@rug.nl",
    description="Plugin Package to communicate with RUG developed hardware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markspan/EvtPlugins",
    packages=setuptools.find_packages(),
	install_requires=[
          'pyEVT'
      ],
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 3',
	],
    python_requires='>=3.11',
	
	data_files=[
		# First target folder.
		('share/evt_plugin_collection/VAS2',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'evt_plugin_collection/VAS2/VAS2.md',
			'evt_plugin_collection/VAS2/VAS2.png',
			'evt_plugin_collection/VAS2/VAS2_large.png',
			'evt_plugin_collection/VAS2/VAS2.py',
			'evt_plugin_collection/VAS2/info.yaml',
			]
		),
		('share/evt_plugin_collection/VAS',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'evt_plugin_collection/VAS/VAS.md',
			'evt_plugin_collection/VAS/VAS.png',
			'evt_plugin_collection/VAS/VAS_large.png',
			'evt_plugin_collection/VAS/VAS.py',
			'evt_plugin_collection/VAS/info.yaml',
			]
		),
		# Corresponding Demo
		('share/opensesame_extensions/example_experiments/examples/VAS',
		['evt_plugin_collection/VAS/experiment.osexp',
			]
		),
		# Second target folder.
		('share/evt_plugin_collection/evt_xx',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'evt_plugin_collection/evt_xx/evt_xx.md',
			'evt_plugin_collection/evt_xx/evt_xx.png',
			'evt_plugin_collection/evt_xx/evt_xx_large.png',
			'evt_plugin_collection/evt_xx/evt_xx.py',
			'evt_plugin_collection/evt_xx/__init__.py',
			]
		),
		# Third target folder.
		('share/evt_plugin_collection/response_box',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'evt_plugin_collection/response_box/response_box.md',
			'evt_plugin_collection/response_box/response_box.png',
			'evt_plugin_collection/response_box/response_box_large.png',
			'evt_plugin_collection/response_box/response_box.py',
			'evt_plugin_collection/response_box/__init__.py',
			]
		),
		# Fourth target folder.
		('share/evt_plugin_collection/RGB_Led_Control',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'evt_plugin_collection/RGB_Led_Control/RGB_Led_Control.png',
			'evt_plugin_collection/RGB_Led_Control/RGB_Led_Control_large.png',
			'evt_plugin_collection/RGB_Led_Control/RGB_Led_Control.py',
			'evt_plugin_collection/RGB_Led_Control/info.yaml',
			]
		),
				# Fourth target folder.
		('share/evt_plugin_collection/tactile_stimulator',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'evt_plugin_collection/tactile_stimulator/tactile_stimulator.png',
			'evt_plugin_collection/tactile_stimulator/tactile_stimulator_large.png',
			'evt_plugin_collection/tactile_stimulator/tactile_stimulator.py',
			'evt_plugin_collection/tactile_stimulator/__init__.py',
			]
		)
	],)
	
