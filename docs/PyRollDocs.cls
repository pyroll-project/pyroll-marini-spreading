%! Package = PyRollDocs
%! Author = Max Weiner
%! Date = 11.02.22

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{PyRollDocs}[2022/02/22 Class for documentation of PyRoll]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrartcl}}
\ProcessOptions\relax
\LoadClass{scrartcl}

\RequirePackage[automark,headsepline]{scrlayer-scrpage}
\clearpairofpagestyles

\makeatletter

\ifoot*{\@author\ -- \@date}
\ofoot*{\pagemark}
\ihead{\@title}
\ohead{\headmark}

\makeatother

\pagestyle{scrheadings}

\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}

% Packages
\RequirePackage{amsmath}
\RequirePackage[backend=biber, maxcitenames=99, sorting=none]{biblatex}
\RequirePackage{booktabs}
\RequirePackage{graphicx}
\RequirePackage{siunitx}
\RequirePackage{subcaption}
\RequirePackage[hidelinks]{hyperref}

\RequirePackage{xcolor}
\RequirePackage{listings} % Quellcode darstellen
\definecolor{keywords}{HTML}{0F54D6}
\definecolor{comments}{HTML}{248700}
\definecolor{strings}{HTML}{8C6C41}
\definecolor{classes}{HTML}{6B2FBA}
\definecolor{ListingBackground}{rgb}{0.9,0.9,0.9}
\lstset{
    showspaces=false,
    showtabs=false,
    breaklines=true,
    showstringspaces=false,
    breakatwhitespace=true,
    commentstyle=\color{comments},
    keywordstyle=\color{keywords},
    stringstyle=\color{strings},
    basicstyle=\ttfamily\small,
    emphstyle=\color{classes},
    backgroundcolor=\color{ListingBackground},
    frame=tb,
    framexleftmargin=0.5em,
    framexrightmargin=0.5em,
    framextopmargin=0.5em,
    framexbottommargin=0.5em,
}

\lstnewenvironment{python}[1][]{\lstset{language=python,#1}}{}
\lstnewenvironment{shell}[1][]{\lstset{language=bash,#1}}{}

\providecommand{\abs}[1]{\lvert#1\rvert}