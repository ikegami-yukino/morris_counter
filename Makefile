singlehtml:
	rm -rf doc
	mkdir -p doc/html
	sphinx-apidoc -A "Yukino Ikegami" -H MorrisCounter -V 0.1 -F -o doc morris_counter
	sed -i -e 's/# import os/import os/' doc/conf.py
	sed -i -e 's/# import sys/import sys/' doc/conf.py
	sed -i -e 's/# sys.path.insert/sys.path.insert/' doc/conf.py
	echo "extensions = ['sphinx.ext.napoleon']" >> doc/conf.py
	sphinx-build -b singlehtml -a doc doc/html
