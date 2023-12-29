#!/usr/bin/emacs --script
(require 'htmlize "/home/kris/.emacs.d/elpa/htmlize-20210825.2150/htmlize.el")
(setq org-safe-remote-resources (list "https://blog.kpiecuch.pl"))
(find-file (car command-line-args-left))
(setq resultfile (org-html-export-to-html))
(setq outputfile (car (cdr command-line-args-left)))
(make-directory (file-name-parent-directory outputfile) t)
(rename-file resultfile outputfile t)
