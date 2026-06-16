all:
	latexmk -pdflatex -g -interaction=nonstopmode -outdir=build hw.tex

# For live previewing on macOS with the Skim PDF reader
watch:
	latexmk -pdflatex -pvc -e '$$pdf_previewer=q[open -a Skim]' -outdir=build hw.tex

clean:
	rm -rf build
