#!/usr/bin/env bash

PDF="$1"
THRESHOLD="${2:-0.005}"

if [ -z "$PDF" ]; then
  echo "Usage: $0 file.pdf [color_threshold]"
  exit 1
fi

gs -q -o - -sDEVICE=inkcov "$PDF" | \
awk -v t="$THRESHOLD" '
{
  c=$1; m=$2; y=$3; k=$4;
  page++;
  if ((c + m + y) <= t) {
    bw++;
    if (bw_list == "")
      bw_list = page;
    else
      bw_list = bw_list "," page;
  } else {
    color++;
    if (color_list == "")
      color_list = page;
    else
      color_list = color_list "," page;
  }
}
END {
  print "B&W pages:", bw;
  if (bw > 0)
    print "  Pages:", bw_list;
  print "";
  print "Color pages:", color;
  if (color > 0)
    print "  Pages:", color_list;
  print "";
  print "Threshold (C+M+Y):", t;
}'
