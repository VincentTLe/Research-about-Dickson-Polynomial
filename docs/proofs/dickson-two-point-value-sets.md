# Reversed Dickson Polynomials: Indices with Two-Point Value Sets over $\mathbb{F}_p$ (p > 3)
## Notation convention

We use reversed Dickson notation throughout: `D_n(a, x)`, with canonical focus on `D_n(1, x)`.
The exact recurrence is `D_0(a, x)=2`, `D_1(a, x)=a`, `D_n(a, x)=aD_{n-1}(a, x)-xD_{n-2}(a, x)` for `n\ge2`.


**Abstract.** For a prime $p>3$, the reversed Dickson polynomial $D_n(1,x)$ over $\mathbb{F}_p$ has image (value set) of cardinality two **iff**

$$
n \equiv 0,\ \frac{p^2+1}{2},\ \frac{p^2+2p-1}{2}\pmod{p^2-1}.
$$

In these three cases the value sets are, respectively, $\{1,2\}$ and $\{1,p-1\}$ (i.e. $\{\pm1\}$), with an explicit discriminant criterion $1-4x$ determining which of the two values occurs for a given $x\in\mathbb{F}_p$. We give a complete proof.

---

## 1. Setup and parametrization

For $x\in\mathbb{F}_p$, choose $y$ in an algebraic closure with $x=y(1-y)$. The reversed Dickson polynomial satisfies

$$
\boxed{\,D_n(1,x)=y^n+(1-y)^n\,}
$$

(which is independent of the chosen root since replacing $y$ by $1-y$ leaves the sum unchanged).

Let $\chi$ denote the quadratic character on $\mathbb{F}_p$, extended by $\chi(0)=0$.

**Lemma 1 (Period $p^2-1$).** For all $n\ge0$ and $x\in\mathbb{F}_p$,

$$
D_{n+p^2-1}(x,1)=D_n(1,x).
$$

*Proof.* If $y\notin\{0,1\}$ then $y,(1-y)\in\mathbb{F}_{p^2}^\times$ so raising to the $(p^2-1)$-st power is 1; if $y\in\{0,1\}$ the identity is immediate. ∎

Thus, as functions on $\mathbb{F}_p$, the polynomials depend only on $n\bmod (p^2-1)$.

**Lemma 2 (Frobenius and half-order exponent).** If $x\in\mathbb{F}_p$ and $y$ solves $y(1-y)=x$, then:

1) $y^p\in\{y,1-y\}$ (Frobenius permutes the two roots of $T^2-T+x$).  
2) For every $y\notin\{0,1\}$,

$$
\Big(\frac{1-y}{y}\Big)^{\frac{p^2-1}{2}}=1,\quad\text{so}\quad
y^{\frac{p^2-1}{2}}=(1-y)^{\frac{p^2-1}{2}}\in\{\pm1\}.
$$

*Proof.* (1) is $(y^p)^2-y^p+x=(y^2-y+x)^p=0$. For (2), either $y\in\mathbb{F}_p^\times$ giving $((1-y)/y)^{p-1}=1$, or $y^p=1-y$ so $((1-y)/y)^{p+1}=1$ (norm $1$ in $\mathbb{F}_{p^2}$), hence the $(p^2-1)/2$ power is 1. ∎

A convenient parametrization for $y\notin\{0,1\}$ is

$$
t=\frac{y}{1-y}\ \Longleftrightarrow\ y=\frac{t}{1+t},\ \ 1-y=\frac{1}{1+t},\ \ x=\frac{t}{(1+t)^2}.
$$

When $x$ varies over $\mathbb{F}_p$, the corresponding $t$ runs through

$$
\mathbb{F}_p^\times \quad\text{if } 1-4x \text{ is a square},\qquad
\mu_{p+1}\setminus\{-1\} \quad\text{if } 1-4x \text{ is a non-square},
$$

where $\mu_{p+1}=\{u\in\mathbb{F}_{p^2}^\times: u^{p+1}=1\}$ (the norm-1 subgroup).

---

## 2. The three two-point value sets

### Case I: $n=p^2-1$.  Value set $\{1,2\}$.
For any $y$, $D_{p^2-1}(x,1)=y^{p^2-1}+(1-y)^{p^2-1}$.
- If $y\in\{0,1\}$ (i.e. $x=0$), the value is $0+1=1$.
- If $y\notin\{0,1\}$, both terms equal $1$ in $\mathbb{F}_{p^2}^\times$, so the value is $2$.

Thus $D_{p^2-1}(x,1)=1$ at $x=0$ and $=2$ for $x\neq0$, yielding value set $\{1,2\}$.

---

### Case II: $n=\dfrac{p^2+1}{2}$.  Value set $\{1,p-1\}=\{\pm1\}$ with discriminant rule.

Write $k=\frac{p^2+1}{2}=\frac{p^2-1}{2}+1$. By Lemma 2,

$$
D_k(x,1)=y^k+(1-y)^k
= y^{\frac{p^2-1}{2}}y+(1-y)^{\frac{p^2-1}{2}}(1-y)
= \varepsilon\,(y+1-y)=\varepsilon,\quad \varepsilon\in\{\pm1\}.
$$

If $1-4x$ is a square, both roots $y,1-y$ lie in $\mathbb{F}_p$, forcing $\varepsilon=1$.  
If $1-4x$ is a non-square, then $y^p=1-y$ and $\varepsilon=-1$.

$$
\boxed{\,D_{\frac{p^2+1}{2}}(x,1)=
\begin{cases}
1,& 1-4x \text{ square in } \mathbb{F}_p\ (\text{including }0),\\
-1,& 1-4x \text{ non-square.}
\end{cases}}
$$

---

### Case III: $n=\dfrac{p^2+2p-1}{2}$.  Value set $\{1,p-1\}=\{\pm1\}$ with the same rule.

Write $m=\frac{p^2+2p-1}{2}=\frac{p^2-1}{2}+p$. Using Lemma 2 and $(1-y)^p=1-y^p$,

$$
D_m(x,1)=y^m+(1-y)^m
=\varepsilon\big(y^p+(1-y)^p\big)=\varepsilon\cdot 1=\varepsilon\in\{\pm1\},
$$

and the square/non-square dichotomy matches Case II:

$$
\boxed{\,D_{\frac{p^2+2p-1}{2}}(x,1)=
\begin{cases}
1,& 1-4x \text{ square in } \mathbb{F}_p\ (\text{including }0),\\
-1,& 1-4x \text{ non-square.}
\end{cases}}
$$

---

## 3. These are the only indices (mod $p^2-1$)
By Lemma 1 it suffices to determine which residues $n\bmod(p^2-1)$ give a two-point image.

**Step A (restriction to square fiber).**  

If $1-4x$ is a square, we can take $y\in\mathbb{F}_p$. Then $D_n(1,x)=y^n+(1-y)^n$ depends only on $n\bmod (p-1)$. As $y$ runs in $\mathbb{F}_p\setminus\{0,1\}$, the set $\{y^r+(1-y)^r\}$ has more than two values unless $r\in\{0,1\}$. Hence a two-point image forces

$$
\boxed{\,n\equiv 0\ \text{or}\ 1\pmod{p-1}.}
$$

**Step B1 ($n\equiv0\pmod{p-1}$).**  

Write $n=(p-1)k$. On the non-square fiber, with $t=\frac{y}{1-y}\in\mu_{p+1}\setminus\{-1\}$,

$$
D_n(1,x)=\Big(\frac{1}{1+t}\Big)^n\big(t^n+1\big).
$$

The set $\{t^k+t^{-k}:t\in\mu_{p+1}\}$ has size $>2$ unless $k\equiv0$ or $k\equiv\frac{p+1}{2}\pmod{p+1}$. The latter congruence produces at least three values overall; thus the only two-point possibility is $k\equiv0\pmod{p+1}$, i.e.

$$
\boxed{\,n\equiv 0\pmod{p^2-1}\,}
$$

which is Case I.

**Step B2 ($n\equiv1\pmod{p-1}$).**  

Write $n=1+k(p-1)$. On the non-square fiber one can use $(1+t)^{p-1}=t^{-1}$ (since $t^p=1/t$) to obtain the exact identity

$$
\boxed{\,D_n(1,x)= t^{\,1-k}\,\frac{1+t^{\,2k-1}}{1+t},\qquad t\in\mu_{p+1}\setminus\{-1\}.}
$$

The map $\phi_m(t)=\frac{1+t^m}{1+t}$ is constant on $\mu_{p+1}\setminus\{-1\}$ iff $m\equiv\pm1\pmod{p+1}$. Thus $D_n$ is constant on the non-square fiber (hence two-valued overall) exactly when

$$
2k-1\equiv \pm1\pmod{p+1}
\ \Longleftrightarrow\
k\equiv \frac{p+1}{2}\ \text{ or }\ \frac{p+3}{2}\pmod{p+1}.
$$

This yields the two residue classes

$$
\boxed{\,n\equiv \frac{p^2+1}{2}\ \text{ or }\ \frac{p^2+2p-1}{2}\pmod{p^2-1}\,}
$$

which are Cases II and III.

Combining B1, B2, and Lemma 1 proves the classification.

---

## 4. Final explicit formulas on $\mathbb{F}_p$

**Case 1:** If $n\equiv p^2-1\pmod{p^2-1}$ (e.g. $n=p^2-1$):

$$
D_n(1,x)=\begin{cases}
1,& x=0,\\
2,& x\ne 0
\end{cases}
\quad\Rightarrow\quad \mathrm{Im}(D_n)=\{1,2\}.
$$

**Case 2:** If $n\equiv \dfrac{p^2+1}{2}\pmod{p^2-1}$ or $n\equiv \dfrac{p^2+2p-1}{2}\pmod{p^2-1}$:

$$
D_n(1,x)=\begin{cases}
1,& 1-4x \text{ square in }\mathbb{F}_p\ (\text{including }0),\\
p-1,& 1-4x \text{ non-square}
\end{cases}
\quad\Rightarrow\quad \mathrm{Im}(D_n)=\{1,p-1\}.
$$

*Keywords:* Dickson polynomial, reversed Dickson, finite fields, value set, quadratic character.

