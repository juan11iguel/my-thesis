# Thesis title

## How to use

The best way to interact with the document is via a `devcontainer` and using the
provided workspace. Following the _following_ steps:

1. Clone or download the repository
2. Open it with VSCode
3. Reopen in devcontainer (requires Docker)
4. Open workpsace
5. That's it! Try building the PDF (the build gets automatically triggered after
   every save)

Most of the writing environment customizations were done following a [guide from Paul Wintz](https://paulwintz.com/latex-in-vscode/)

There are a lot of snippets for including attachments in the document, make sure
to check them out in [latex.code-snippets](.vscode/latex.code-snippets).

![Snippets](./assets/snippets.mp4)


## Compiling the document

The document is compiled using `latexmk` which uses the configuration file
`latexmkrc`. This file in turn uses `lualatex` as the interpreter. Output build
files including the [manuscript PDF](./out_dir/main.pdf) are saved in the [out_dir](./out_dir/) folder.

This build process is defined as a "recipe" in LaTeX workshop, and as the
default in the devcontainer.

## Document customizations and additions

This thesis is done in LaTeX using the [kaobook class]() with some modifications
inspired by... In particular:

(Fill here all the changes and which files have been changed)

- TODO Changed colors for paragraphs in the margins (margin@par) to a lighter gray (`kao.sty`)
- TODO Changed font to Fira Sans, as used in TheoWinterhalter-PhD (`main.tex`)
- Changed side citations to a dark gray, as used in TheoWinterhalter-PhD (`main.tex`)

### Components

Some are listed here, check the [kaobox class repository](https://github.com/fmarotta/kaobook) for more.


```latex
\begin{definition}
\labdef{openset}
Let $(X, d)$ be a metric space. A subset $U \subset X$ is an open set 
if, for any $x \in U$ there exists $r > 0$ such that $B(x, r) \subset 
U$. We call the topology associated to d the set $\tau\textsubscript{d}$ 
of all the open subsets of $(X, d).$
\end{definition}

\begin{remark}
Let $(X, d)$ be a metric space. A subset $U \subset X$ is an open set 
if, for any $x \in U$ there exists $r > 0$ such that $B(x, r) \subset 
U$. We call the topology associated to d the set $\tau\textsubscript{d}$ 
of all the open subsets of $(X, d).$
\end{remark}
```

![](assets/definition-remark.png)

#### Margin figures

```latex
\begin{marginfigure}[-5.5cm]
    \includegraphics[]{figures/shareholders-driven-apocalysis.png}
    \caption{``Yes, the planet got destroyed. But for a beautiful moment in time, we created a lot of value for shareholders''}
    % \labfig{}
\end{marginfigure}
```

![margin-figure](./assets/margin-figure.png)

#### Too Long Didn't Read box

![tldr-box](assets/tldr-box.png)

#### Work in progress box
Useful to indicate to yourself or your supervisors that the section is not
  completed.

```latex
\wipbox{Additional text to add}
```

![WIP box showcase](assets/wip-box.png)



#### Kaobox with custom color

```latex
\begin{kaobox}[title=Kaobox with custom color,colback=MediumPurple2!25!white,colbacktitle=MediumPurple2!25!white]
    What is thiiiis
    \begin{enumerate}
      \item Enumerations
      \item should
      \item be
      \item okay
    \end{enumerate}

    Even fancy figures\texttrademark{}. \\

    \begin{minipage}{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{figures/cc-intro-hybrid-cooler-diagram-no-bg.png}\\
    \small Hybrid cooler
    \end{minipage}
    \hfill
    \begin{minipage}{0.48\linewidth}
    \centering
    \includegraphics[width=\linewidth]{figures/cc-intro-combined-cooler-diagram-no-bg.png}\\
    \small Combined cooler
    \end{minipage}
\end{kaobox}
```

![kaobox-custom-color](./assets/kaobox-custom-color.png)

#### Annotation and margin annotation

Just a command for kaobox with some custom color

```latex
\annotation{Process \textit{vs} waste heat take on efficiency}{
    In a process heat driven system, between two plants that produce the same
    amount of useful product, the most efficient one is the one that uses the
    least external heat to do so, whereas in a waste heat driven system, the
    two plants would be considered as efficient since the unused heat would be
    \textit{wasted} to the environment. A more intuitive definition would be:
    \\
    Given two plants that consume the same waste heat, the most efficient one
    is the one that produces more product with the available heat. 
}
```

![](assets/annotation.png)

```latex
\marginannotation[*-5]{Title of the annotation}{
	Is everything in this life just a wrapped kaobox? What if I told you that a
	kaobox is just a wrapper of tcolorbox?
}
```

![](assets/margin-annotation.png)

#### Countered model and problem boxes

They are defined in [kao.sty](./kao.sty) and not only are customized boxes, but
also they have their own counter like figures or tables which can be used to
reference them and create a _list of_ at the beginning of the manuscript.
Support for referencing them must be added in [kaorefs.sty](./kaorefs.sty)


```latex
\begin{modelcounter}{Test}
	\begin{align*}
    T_{cc,out},\,C_{e}&,\,C_{w},\,T_{c,out} = \mathrm{combined\:cooler\:model}(q_{c}, R_{p}, R_{s}, \omega_{dc}, \omega_{wct},T_{amb},HR_i,T_{v},\dot{m}_{v}) \\
    & T_{cc,in}=T_{c,out} \\
    & T_{dc,in}=T_{cc,in} \\
    % three-way valves
    & q_{dc} = q_{c} \cdot (1-R_{p}) \\
    & q_{wct,p} = q_{c} \cdot R_{p} \\
    & q_{wct,s} = q_{dc} \cdot R_{s} \\
    % dc model
    & T_{dc,out},\,C_{e,dc} = \mathrm{dc\:model}(q_{dc},\, \omega_{\text{dc}},\, T_{\text{amb}},\, T_{dc,in}) \\
    % first mixer
    & q_{wct},\,T_{wct,in} = \mathrm{mixer\:model}(q_{wct,p},\,T_{T{cc,in}},\, q_{wct,s},\, T_{dc,out}) \\
    \end{align*}
	\labmod{test}
\end{modelcounter}

As can be seen in \refmod{test}, the counter is working.
As can be seen in \refprob{test}, the counter is working.

\begin{problemcounter}{Test}
	\blindtext
  \begin{equation*}
	\min_{\mathbf{x},\, \mathbf{e};\, \boldsymbol{\theta}} \quad J = f(\mathbf{x}, \mathbf{e}; \boldsymbol{\theta}) = f(x)
  \end{equation*}

  \textbf{with}:
  \begin{itemize}
	\item Model name model
	\[
	  out_1,\, out_2 = f(in_1,\, in_2,\, \ldots,\, in_N)
	\]
	\item Decision variables
	\[
	  \mathbf{x} = [x_1,\, x_2]
	\]
	\item Environment variables
	\[
	  \mathbf{e} = [e_1,\, e_2,\, \ldots,\, e_3]
	\]
	\item Fixed parameters
	\[
	  \boldsymbol{\theta} = [\theta_1 = X,\, \theta_2 = Y]
	\]
  \end{itemize}

  \textbf{subject to}:
  \begin{itemize}
	\item Box-bounds
	\begin{itemize}
	  \item \( x_{1} \in [\underline{x}_{1}, \overline{x}_{1}] \)
	  \item \( x_{2} \in [\underline{x}_{2}, \overline{x}_{2}] \)
	\end{itemize}
	\item Constraints
	\begin{itemize}
	  \item \( \left| out_X - out_Y \right| \leq \epsilon_1 \)
	  \item \( out_X \leq out_Z - \Delta Z \)
	\end{itemize}
  \end{itemize}
  \labprob{test}
\end{problemcounter}
```

![](assets/model-problem-countered.png)


#### Reminder and margin reminder

```latex
\reminder{Optimization problem definition}{
    The general optimization function is defined as:\footnote{See \nrefsec{intro:optimization}}
    \begin{equation*}
    \min_{\mathbf{x},\, \mathbf{e};\, \boldsymbol{\theta}} \quad J = f(\mathbf{x}, \mathbf{e}; \boldsymbol{\theta}) 
        \quad \text{s.t.} \quad g_i(\mathbf{x}) \leq 0, \quad i = 1, \ldots, m
    \end{equation*}

    where \(x\) is the decision vector, \(e\) represents the environment, and \(\theta\) contains the fixed parameters.
}
```

![](./assets/reminder.png)

```latex
The problem is designed as an optimization problem with a shrinking
horizon\marginreminder[*-2]{Shrinking horizon optimization}{
An optimization where the horizon end is fixed, and as time progresses, the
start of the horizon moves forward.\footnote{See
\nrefch{intro:optimization}}
}. The horizon size should be large enough so that
decisions on how to operate the system are made with perspective...
```

![](./assets/margin-reminder.png)



## TODOs

- [ ] Añadir List of open-source software used. Not an extensive list but the
  main ones.
- [ ] Add \listofcontributions
- [ ] Add \listofmodels
- [ ] Add \listofproblems
- [ ] Glosary is not being printed
- [ ] Mirar la posibilidad de incluir citas en páginas en blanco entre
  capítulos
- [x] Caja TL;DR para inicio de cada capítulo


Si finalmente se hace un capíutlo de instalaciones experimentales, se puede
hacer una introducción donde se ponga esta imagen con marcas:

![](temp/PXL_20220805_071840783.jpg)

Indicando el campo solar, el circuito de intercambio, generación de vapor,
refrigeración combinada, etc. y la MED


![alt text](image.png)