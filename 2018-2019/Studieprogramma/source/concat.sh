#!/bin/bash

cd output/

mkdir -p courses

for d in */ ; do
	if [[ "$d" == "courses/" ]]; then
		continue
	fi
	echo $d
	pdftk ${d}current.pdf ${d}solution_rel.pdf ${d}solution_abs.pdf legend.pdf cat output courses/proposal_${d%/}.pdf
done
