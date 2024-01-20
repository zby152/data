\LoadClass{article}
\RequirePackage{xeCJK}
\RequirePackage{CJKnumb}
\RequirePackage{ctex}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{enumitem}
\RequirePackage{listings}
\RequirePackage{xcolor}
\RequirePackage{array}
\RequirePackage{mathtools}
\RequirePackage{float}
\RequirePackage{indentfirst}
\RequirePackage{zhnumber}
\RequirePackage{booktabs}
\RequirePackage{amsmath,xparse}
\RequirePackage{caption}
\RequirePackage{pgfplots, pgfplotstable}
\RequirePackage{subfigure}
\RequirePackage{filecontents}
\RequirePackage{chronosys}
\RequirePackage{lipsum}
\RequirePackage{epstopdf}
\RequirePackage{multicol}
\RequirePackage{multirow}
\RequirePackage[colorlinks,linkcolor=blue]{hyperref}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=blue,      
    urlcolor=blue,
    citecolor=cyan,
}


\linespread{1.2}
\geometry{top=1in,bottom=1in,left=1in,right=1in}
\setcounter{secnumdepth}{3}
\renewcommand\thesection{\chinese{section}、}
\renewcommand\thesubsection{\arabic{section}\thinspace.\thinspace\arabic{subsection}}
\renewcommand\thesubsubsection{\thesubsection\thinspace.\thinspace\arabic{subsubsection}}
\newlist{clause}{enumerate}{1}
\setlist[clause]{fullwidth,itemindent=2em,label=(\arabic*)}
\newCJKfontfamily[song]\song{SimSun}[AutoFakeBold]


\titleformat*{\section}{\large\bfseries}
\titleformat*{\subsection}{\normalsize\bfseries}
\titleformat*{\subsubsection}{\normalsize\bfseries}
\graphicspath{{figures/}{figure/}{pictures/}{picture/}{pic/}{pics/}{image/}{images/}}
\titlespacing{\subsection}{0em}{*4}{*1.5}
\titlespacing{\subsubsection}{0em}{*4}{*1.5}



% c++模板
\RequirePackage{xcolor}
\definecolor{commentColor}{RGB}{53,129,34}
\definecolor{keywordColor}{RGB}{172, 62, 158}
\definecolor{stringColor}{RGB}{194, 62, 42}
\definecolor{preprocessorColor}{RGB}{114, 75, 48}
\definecolor{characterColor}{RGB}{31, 53, 207}
\definecolor{numberColor}{RGB}{166, 166, 166}
\definecolor{oglobalColor}{RGB}{97, 64, 154}
\definecolor{globalColor}{RGB}{89, 127, 134}
\definecolor{functionColor}{RGB}{56,36,124}

\RequirePackage{fontspec}
\RequirePackage[T1]{fontenc}
\RequirePackage[scaled=0.85]{beramono}
\newfontfamily\sff{SFMono-Regular}

\lstset{
language=C++,
basicstyle=\ttfamily,
keywordstyle=\color{keywordColor}\ttfamily\bfseries,
commentstyle=\color{commentColor}\ttfamily,
stringstyle=\color{stringColor}\ttfamily,
showstringspaces=false,
columns=flexible,
numbers=left,
numberstyle=\color{numberColor}\footnotesize\sf,
%morecomment=[s][\color{stringColor}\ttfamily]{<}{>},
morecomment=[s][\color{characterColor}\ttfamily]{'}{'},
moredelim        = [s][\color{commentColor}]{/*}{*/},
keywords=[2]{std, cout, cin},
keywordstyle = [2]{\color{oglobalColor}\ttfamily},
keywords=[3]{endl, printf, scanf, setw, setfill, setbase, setprecision, time, ctime, rand},
keywordstyle = [3]{\color{functionColor}\ttfamily},
keywords=[4]{\#include},
keywordstyle =[4]{\color{preprocessorColor}\ttfamily},
literate={
    {<<}{{{\color{black}<<}}}1
    {>>}{{{\color{black}>>}}}1
    {0}{{{\color{characterColor}0}}}1
    {1}{{{\color{characterColor}1}}}1
    {2}{{{\color{characterColor}2}}}1
    {3}{{{\color{characterColor}3}}}1
    {4}{{{\color{characterColor}4}}}1
    {5}{{{\color{characterColor}5}}}1
    {6}{{{\color{characterColor}6}}}1
    {7}{{{\color{characterColor}7}}}1
    {8}{{{\color{characterColor}8}}}1
    {9}{{{\color{characterColor}9}}}1},
tabsize=4
}


% 代码格式和颜色定义
\definecolor{dkgreen}{rgb}{0,0.6,0}
\definecolor{gray}{rgb}{0.5,0.5,0.5}
\definecolor{comment}{rgb}{0.56,0.64,0.68}
\lstset{
  frame=single,
  aboveskip=3mm,
  belowskip=3mm,
  xleftmargin=2em,
  belowcaptionskip=1\baselineskip,
  frameround=tttt,
  xrightmargin=\parindent,
  %showstringspaces=false,
  %columns=flexible,
  framerule=1pt,
  rulecolor=\color{gray!35},
  backgroundcolor=\color{gray!5},
  %basicstyle={\small\ttfamily},
  %numbers=none,
  %numberstyle=\tiny\color{gray},
  %keywordstyle=\color{blue},
  %commentstyle=\color{comment},
  %stringstyle=\color{dkgreen},
  breaklines=true,
  breakatwhitespace=true,
  %tabsize=2,
}

%\lstdefinestyle{customasm}{
%    belowcaptionskip=1\baselineskip,
%    frame=single, 
%    frameround=tttt,
%    xleftmargin=\parindent,
%    language=[x86masm]Assembler,
%    basicstyle=\footnotesize\ttfamily,
%    commentstyle=\itshape\color{green!60!black},
%    keywordstyle=\color{blue!80!black},
%    identifierstyle=\color{red!80!black},
%    tabsize=4,
%    numbers=left,
%    numbersep=8pt,
%    stepnumber=1,
%    numberstyle=\tiny\color{gray}, 
%    columns = fullflexible,
%}

% 页眉页脚
\pagestyle{fancy}
\fancyhead[L]{
\begin{minipage}[c]{0.06\textwidth}
  \includegraphics[height=3.5mm]{figures_DO_NOT_DELETE/whulogo}
\end{minipage}
\begin{minipage}[c]{0.4\textwidth}
  武汉大学
\end{minipage}
}
\fancyhead[R]{操作系统设计与实践}
\fancyfoot[C]{\thepage}

\title{\textbf{武汉大学国家网络安全学院实验报告}}
\date{}

\newcommand{\makeheader}{
\maketitle
\vspace{-2cm}
\begin{table}[htbp]
\centering
\setlength{\tabcolsep}{2.7mm}
\begin{tabular}{|c|ccc|c|c|c|c|}
\hline
\textbf{课程名称} & \multicolumn{3}{c|}{操作系统设计与实践}                                              & \textbf{成\quad\quad 绩}   &      & \textbf{教师签名} &            \\ \hline
\textbf{实验名称} & \multicolumn{3}{c|}{综合装配\&安全分析}                                             & \textbf{实验序号} & final    & \textbf{实验日期} & 2020.11.26 \\ \hline
\textbf{姓\quad\quad 名}   & \multicolumn{1}{c|}{彭雨昂} & \multicolumn{1}{c|}{\textbf{学号}} & 2019302140023 & \textbf{专\quad\quad 业}   & 信息安全 & \textbf{年级班级} & 19级8班      \\ \hline
\end{tabular}
\end{table}
}