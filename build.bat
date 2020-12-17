rmdir dist /s /q
python setup.py sdist
twine upload dist/*