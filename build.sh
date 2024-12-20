#!/bin/sh

tsc && \
java -jar closure-compiler-v20220301.jar --js 'ts/build/**.js' --js_output_file ./primes/static/app.js --language_in ECMASCRIPT_2020 --language_out ECMASCRIPT_2020 --compilation_level ADVANCED

pipenv run pip list --format=freeze | grep -v site-primes > pip-packages.txt
