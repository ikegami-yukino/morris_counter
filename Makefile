singlehtml:
	rm -rf sphinx docs
	mkdir docs sphinx
	sphinx-apidoc -A "Yukino Ikegami" -H MorrisCounter -V 0.1 -F -o sphinx morris_counter
	sed -i -e 's/# import os/import os/' sphinx/conf.py
	sed -i -e 's/# import sys/import sys/' sphinx/conf.py
	sed -i -e 's/# sys.path.insert/sys.path.insert/' sphinx/conf.py
	echo "extensions = ['sphinx.ext.napoleon']" >> sphinx/conf.py
	sphinx-build -b singlehtml -a sphinx docs
