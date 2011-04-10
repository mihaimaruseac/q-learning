#!/bin/bash
#
# Call with output_image [filename title]

files="./ql.py cmp $2"

out=$1
shift

c=2
plotcmd="set term png; plot \"tmp\" using :$c title \"$2\" with lines"
shift
shift


while [ $# -ne 0 ]; do
    files="$files $1"
    shift

    c=$(($c+1))
    plotcmd="$plotcmd, \"tmp\" using :$c title \"$1\" with lines"
    shift
done

$files > tmp
echo "$plotcmd" | gnuplot > $out
rm tmp

