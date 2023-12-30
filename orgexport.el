#!/usr/bin/emacs --script
(require 'htmlize "/home/kris/.emacs.d/elpa/htmlize-20210825.2150/htmlize.el")
(setq org-safe-remote-resources (list "https://blog.kpiecuch.pl"))
(setq basepwd default-directory)
(find-file (car command-line-args-left))
(setq resultfilename (org-html-export-to-html))
(setq resultfilepath default-directory)
(setq outputfile (car (cdr command-line-args-left)))
(cd basepwd)

; (make-directory (file-name-parent-directory outputfile) t)
(rename-file (concat resultfilepath resultfilename) outputfile t)
