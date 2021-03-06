#!/bin/bash

cd output/

for teacher in */ ; do
	echo "$teacher"
	cd "$teacher"
	for d in */ ; do
		echo "	$d"
		pdftk ${d}current.pdf ${d}solution_rel.pdf ${d}solution_abs.pdf ../legend.pdf cat output voorstel_${d%/}.pdf
	done
	ln -s ../../simulatie.xlsx .
	cd ..
done

