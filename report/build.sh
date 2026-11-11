#!/usr/bin/env bash
# Builds report.pdf from report.tex
set -e
cd "$(dirname "$0")"
for i in 1 2; do pdflatex -interaction=nonstopmode -halt-on-error report.tex >/dev/null; done
rm -f report.aux report.log report.out report.toc
echo "Built report.pdf"
