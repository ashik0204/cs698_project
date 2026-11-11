#!/usr/bin/env bash
# Builds slides.pdf (for the projector) and notes.pdf (speaker notes) from deck.tex
set -e
cd "$(dirname "$0")"
for i in 1 2; do pdflatex -interaction=nonstopmode -halt-on-error -jobname=slides deck.tex >/dev/null; done
for i in 1 2; do pdflatex -interaction=nonstopmode -halt-on-error -jobname=notes "\def\NOTESONLY{1}\input{deck.tex}" >/dev/null; done
rm -f slides.{aux,log,nav,out,snm,toc} notes.{aux,log,nav,out,snm,toc}
echo "Built slides.pdf and notes.pdf"
