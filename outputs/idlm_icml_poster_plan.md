# IDLM ICML Poster Plan

## 0. Objective

Create a 36 in (H) x 60 in (W) ICML main-conference poster for:

**IDLM: Inverse-distilled Diffusion Language Models**

The poster should make one claim memorable within 5 seconds:

> **IDLM turns pretrained many-step Diffusion Language Models into few-step generators while keeping the teacher's generation quality target.**

The slightly more technical tagline should be:

> **From 1024 reverse steps to 16 steps for masked diffusion, with a valid inverse-distillation objective and stable discrete relaxations.**

I recommend 36 x 60 in because ICML 2026 lists 36 x 48, 36 x 60, and 36 x 72 in as suggested main-conference poster sizes. The 60 in width is the best compromise: wide enough for a three-column technical story, less sparse and harder to miss than 72 in.

Sources used:

- Paper source: Overleaf clone, `main.tex`, `sec/*.tex`, `appendix/*.tex`
- Presentation: `/Users/david.li/Downloads/IDLM.pptx` and `/Users/david.li/Downloads/IDLM.pptx.pdf`
- Code: `https://github.com/David-cripto/IDLM`
- Project page: `https://david-cripto.github.io/idlm-project-page/`
- Blog post: `https://david-cripto.github.io/Bio-page/blog/idlm/`
- arXiv: `https://arxiv.org/abs/2602.19066`
- ICML poster instructions: `https://icml.cc/Conferences/2026/PosterInstructions`

## 1. Scientific Story

### Core problem

Diffusion Language Models can generate high-quality text but need many reverse diffusion steps. This creates slow inference, even though each denoising step can update a whole sequence.

### Core idea

Instead of training a diffusion model from data:

```latex
f^* = \arg\min_f \mathcal L(f, p^*)
```

IDLM fixes a pretrained teacher `f^*` and learns a student distribution `p_theta` such that training a diffusion model on student samples would recover the teacher.

The central loss is:

```latex
\mathcal L_{\mathrm{IDLM}}(\theta)
=
\mathbb E_{p_\theta(x_0)}[\mathcal L(f^*,x_0)]
-
\min_{\widehat f}
\mathbb E_{p_\theta(x_0)}[\mathcal L(\widehat f,x_0)].
```

The fake model `\widehat f` is trained on student samples. The generator is updated by the teacher-fake loss gap. In the code, this is visible as the frozen teacher, trainable fake model, and generator loss `teacher_loss - fake_loss`.

### Core theorem

For SEDD, MDLM, and Duo in the low-temperature limit:

```latex
\mathcal L_{\mathrm{IDLM}}(\theta)
\ge
D_{\mathrm{KL}}(p_\theta \| p^*) \ge 0,
\qquad
\mathcal L_{\mathrm{IDLM}}(\theta)=0
\iff
p_\theta=p^*.
```

This theorem is the poster's trust anchor. It answers the likely reviewer question: "Why is this inverse objective valid rather than just another heuristic?"

### Core practical contribution

The discrete setting creates two training problems:

1. The student output is discrete, so direct gradients are unstable.
2. The forward noising sample `x_t ~ p_{t|0}(x_t | x_0)` may depend on the generated `x_0`.

IDLM handles this with:

- Simplex relaxation: `G_theta` outputs points in the probability simplex.
- Loss extension: the teacher losses remain valid on simplex inputs because `x_0` appears through scalar products or matrix-vector forward distributions.
- MDLM/SUBS case: nonzero loss terms occur at mask states where sampling does not require backpropagating through token identity.
- Duo case: the Gaussian relaxation gives a reparameterization trick, isolating randomness in `epsilon`.

### Core empirical message

Use only the most poster-readable numbers:

| Setting | Teacher / baseline | IDLM result | Message |
|---|---:|---:|---|
| OpenWebText, masked diffusion | MDLM: 1024 steps, GenPPL 41.29, entropy 5.28 | IDLM-MDLM: 16 steps, GenPPL 32.75, entropy 5.42 | 64x fewer steps with comparable or better quality/diversity tradeoff |
| OpenWebText, uniform greedy | Duo^g teacher: 1024 steps, GenPPL 71.72, entropy 5.22 | IDLM-DCD^g: 4 steps, GenPPL 77.47, entropy 5.28 | extreme low-step regime remains competitive |
| TinyGSM/GSM8K | MDLM teacher: 1024 steps, 18.0% | IDLM-MDLM: 128 steps, 19.86% | conditional correctness survives distillation |
| TinyGSM/GSM8K | Duo teacher: 1024 steps, 17.2% | IDLM-Duo: 64 steps, 19.03%; 128 steps, 21.38% | teacher-level reasoning with far fewer steps |

I would keep the public headline conservative as **4x-64x fewer steps**, matching the arXiv abstract and project page. Inside the results panel, we can separately annotate the IDLM-DCD 4-step point as "4-step uniform-DCD setting" or "256x relative to the original 1024-step Duo trajectory" if we include the caveat.

## 2. Poster Layout

### Format

- Size: 36 in H x 60 in W, landscape.
- Grid: 12 columns with 0.6 in outer margins and 0.35 in gutters.
- Reading path: title -> hero claim -> method -> theorem/practice -> results -> links.
- Minimum body size: 28 pt. Main equations: 32-38 pt. Section headers: 42-48 pt. Title: 82-96 pt.

### Header: 10% height

Content:

- Title and authors.
- ICML 2026 badge.
- One-line takeaway: **"Few-step language diffusion by inverse distillation."**
- Small QR cluster: paper, code, project page, blog, checkpoints.

Decision:

- Keep author list complete but compact.
- Do not put a full abstract. The poster must start with the result, not the paper prose.

### Hero band: 18% height, full width

Visual:

```text
Standard DLM:   1024 reverse calls  ->  high quality, slow
IDLM student:     16 reverse calls  ->  teacher-level quality, fast
```

Use a simplified token-denoising strip inspired by the blog/project animation:

- Left: many small denoising blocks fading across a long path.
- Right: four or sixteen larger jumps in a compressed path.
- Center callout: **"Compress the chain, not the distribution."**

Decision:

- This is the hook for passersby. It should be readable from several meters away.
- Use "1024 -> 16" as the visual anchor because it is concrete and supported by IDLM-MDLM.

### Left column: Motivation and inverse problem, 22% width

Sections:

1. **Why DLMs Are Slow**
   - DLMs update full sequences but require many sequential denoising steps.
   - Naive skipping is fragile because factorized large jumps can break token correlations.

2. **Inverse Distillation**
   - Forward training: given `p^*`, find `f^*`.
   - IDLM: given `f^*`, find `p_theta`.

Visual:

- Redraw the current teaser in a cleaner two-row version:
  - top row: "data -> teacher"
  - bottom row: "teacher -> student distribution"

Decision:

- The history of inverse distillation from the slides should be omitted or moved to one small citation line. It is not essential for a first-time ICML viewer.

### Center column: Method and theorem, 38% width

Main figure:

Redraw the method pipeline from `method_idlm_pipeline_cropped.pdf`, but simplify:

```text
student G_theta -> student samples x_0
        |
        +-> frozen teacher f^* -> teacher loss
        |
        +-> train fake model \hat f -> fake loss

student update = teacher loss - fake loss
fake update    = train on student samples with the DLM loss
```

The current figure is scientifically useful but too visually dense for a poster. The poster version should:

- Remove repeated distribution blocks.
- Use three consistent colors:
  - Teacher: blue
  - Fake: green
  - Student/generator: orange
- Show the alternating optimization as two numbered arrows.
- Put the IDLM loss directly below the figure.

Theorem box:

```latex
\mathcal L_{\mathrm{IDLM}}(\theta)
\ge D_{\mathrm{KL}}(p_\theta\|p^*) \ge 0,
\qquad
\mathcal L_{\mathrm{IDLM}}=0 \iff p_\theta=p^*.
```

Caption:

> The inverse objective has a unique global optimum at the data distribution; minimizing it cannot prefer a different distribution in the population limit.

Practice box:

Two mini-cards below the theorem:

- **Masked diffusion:** SUBS makes nonzero loss contributions occur at mask states; no unstable hard Gumbel route is needed.
- **Uniform diffusion:** Gaussian relaxation gives a smooth reparameterized input; full intermediate gradients are more stable than the stop-gradient variant.

Decision:

- Method + theorem deserve the largest central area because they are the main novelty and the part most likely to trigger technical questions.

### Right column: Results, 32% width

Use three evidence blocks:

1. **OpenWebText: masked diffusion**
   - Bar chart: MDLM 1024 vs SDTT 128 vs IDLM-MDLM 16.
   - Highlight GenPPL and entropy together.

2. **OpenWebText: uniform diffusion**
   - Bar chart: Duo^g 1024, Duo-DCD^g 8, IDLM-Duo^g 16, IDLM-DCD^g 4.
   - Make the caveat explicit: IDLM-DCD is a distillation of Duo-DCD.

3. **TinyGSM/GSM8K conditional generation**
   - Tiny horizontal bar table:
     - MDLM teacher 18.0 at 1024 vs IDLM-MDLM 19.86 at 128.
     - Duo teacher 17.2 at 1024 vs IDLM-Duo 19.03 at 64 and 21.38 at 128.

Small inset:

- GenPPL-entropy frontier.
- Use only as a compact validation that lower GenPPL is not simply entropy collapse.
- If space is tight, remove the full frontier and replace it with a two-line note:
  "We report GenPPL with entropy/MAUVE; low-step gains do not come from collapsed low-entropy sampling."

Decision:

- Prefer bars over full tables. The full OWT table is excellent for the paper, but too dense for a poster. Bars let viewers decode the speed-quality story in under 10 seconds.

### Footer: 5% height

Content:

- Code, models, paper, blog, project page QR codes.
- Minimal citation.
- "Ask me about: uniqueness proof, simplex relaxation, MDLM vs Duo gradients."

Decision:

- The footer is a call to action, not a methods appendix.

## 3. What To Remove From The Poster

Remove or compress:

- Full roadmap slides.
- Team photo slide.
- Long inverse-distillation history slide.
- Detailed DMD/DMD-like derivation.
- Full references list.
- Detailed appendix ablations.
- Full qualitative samples unless there is extra space.

Keep only:

- One-line motivation.
- IDLM objective.
- Theorem.
- Discrete-relaxation trick.
- Results.
- Links.

This is not loss of rigor. It is moving detail into the conversation and QR-linked paper/code, while keeping the poster readable.

## 4. 90-Second Poster Walkthrough

1. **Problem, 15 seconds**
   - "Diffusion language models can update many tokens in parallel, but sampling is slow because the reverse chain still has hundreds or thousands of sequential denoising calls."

2. **Idea, 20 seconds**
   - "We take a pretrained DLM teacher and ask the inverse question: what student distribution would make this teacher optimal if the teacher were trained on student samples?"

3. **Method, 25 seconds**
   - "We train a student generator and a fake model. The fake model learns the DLM loss on student samples. The student is updated by the teacher-fake loss gap, which pulls it toward samples that the teacher explains better than the fake model."

4. **Theory, 15 seconds**
   - "The key result is that this IDLM objective lower-bounds KL to the data distribution and has a unique optimum at `p_theta = p^*` for the DLM families we consider."

5. **Practice, 10 seconds**
   - "The discrete gradients are handled by simplex outputs and process-specific reparameterizations: SUBS for masked diffusion and Gaussian relaxation for Duo."

6. **Results, 15 seconds**
   - "On OWT, IDLM-MDLM compresses 1024 steps to 16 steps with comparable or better GenPPL/entropy tradeoff. On TinyGSM, teacher-level conditional accuracy survives with far fewer steps."

## 5. Mathematical Proof Of The Plan's Optimality

No poster layout is universally optimal without an objective function. I define the objective below and prove that the recommended layout and content selection are optimal or near-optimal under that objective.

### 5.1 Content selection as a constrained coverage problem

Let the poster need to communicate six claims:

```text
C1 = slow-inference problem
C2 = inverse-distillation idea
C3 = IDLM training mechanism
C4 = uniqueness/theory guarantee
C5 = discrete optimization/practical relaxations
C6 = empirical speed-quality evidence
```

Each candidate content unit `i` has:

- relevance vector `r_i in [0,1]^6`,
- area cost `a_i > 0`,
- cognitive complexity `c_i >= 0`,
- visual salience `s_i >= 0`.

For a selected set `S`, define poster utility:

```latex
F(S)
=
\sum_{k=1}^6 \alpha_k
\min\left(1, \sum_{i \in S} r_{ik}\right)
-
\lambda \sum_{i \in S} c_i,
```

subject to the area constraint:

```latex
\sum_{i \in S} a_i \le A.
```

The first term rewards covering each essential claim. The `min` creates diminishing returns: once a claim is covered, repeating it gives little value. The second term penalizes cognitive load.

The coverage term is monotone submodular because each claim contribution is a concave cap applied to a modular sum. A standard greedy rule that repeatedly selects the feasible unit with largest marginal gain per area has the `(1 - 1/e)` approximation guarantee for monotone submodular maximization under a cardinality/knapsack-style budget, with the usual small correction for costs. Therefore, selecting high marginal-utility units first is mathematically justified.

Under this model:

- Hero "1024 -> 16" has high relevance for `C1` and `C6`, low complexity, high salience.
- Method pipeline has high relevance for `C2` and `C3`.
- The theorem box has high relevance for `C4`.
- Simplex/SUBS/Duo cards have high relevance for `C5`.
- Bar charts and TinyGSM mini-table have high relevance for `C6`.
- QR links provide low-area reproducibility support.

After these units are selected, the marginal gains of the removed material are small:

- History slides mostly repeat `C2` and add high complexity.
- DMD derivation mostly deepens `C4` but exceeds the poster attention budget.
- Full tables repeat `C6` with lower salience than charts.
- Full references and appendices add little first-pass coverage.

Thus, the selected content set is the greedy near-optimal set under `F`.

### 5.2 Area allocation

Let `a_j` be the area assigned to section `j`, and let `w_j` be its importance weight. Assume the comprehension contribution of a section is logarithmic in area:

```latex
U(a_1,\ldots,a_m)
=
\sum_{j=1}^m w_j \log a_j,
\qquad
\sum_{j=1}^m a_j = A,
\quad a_j>0.
```

The logarithm encodes diminishing returns: doubling an already-large section helps less than rescuing an undersized one.

The Lagrangian is:

```latex
\mathcal J(a,\mu)
=
\sum_j w_j \log a_j
-
\mu \left(\sum_j a_j - A\right).
```

The first-order condition gives:

```latex
\frac{\partial \mathcal J}{\partial a_j}
=
\frac{w_j}{a_j} - \mu = 0
\quad\Longrightarrow\quad
a_j = \frac{w_j}{\mu}.
```

Using `sum_j a_j = A`:

```latex
\mu = \frac{\sum_j w_j}{A},
\qquad
a_j^* =
A\frac{w_j}{\sum_l w_l}.
```

So the optimal area is proportional to importance. The proposed poster uses approximately:

| Section | Weight | Area implication |
|---|---:|---|
| Header and identity | 0.10 | compact but readable |
| Hero claim | 0.18 | large enough to catch attention |
| Method pipeline | 0.25 | largest technical object |
| Theorem and practical relaxations | 0.22 | large enough for equations and trust |
| Results | 0.30 | largest evidence block |
| Footer links | 0.05 | small but present |

These proportions match the KKT optimum for the chosen weights up to grid discretization. The results and method receive the most area because they carry the highest decision value for an ICML audience: "what is new?" and "does it work?"

### 5.3 Reading order

Define a prerequisite graph:

```text
Problem -> Idea -> Method -> Theory -> Results
Problem -> Results
Method -> Practice
Practice -> Results
```

Suppose content unit `j` depends on prerequisite `i`. If a viewer reads `j` before `i`, its comprehension probability is multiplied by `q_ij in [0,1)`. If `i` appears before `j`, no such penalty is applied.

For any adjacent inverted pair `(j,i)` where `i` is a prerequisite of `j`, swapping them increases expected utility by:

```latex
\Delta
=
w_j p_j (1 - q_{ij}) \ge 0.
```

Therefore, every inversion of the prerequisite graph can be removed without decreasing utility. A topological ordering of the graph is optimal. The proposed reading path is exactly such a topological ordering:

```text
problem -> inverse idea -> method -> theorem/practice -> results
```

### 5.4 Visual choice

For a visual unit, model probability of being noticed as:

```latex
P_i = 1 - \exp\left(-\kappa \frac{s_i a_i}{1+d_i}\right),
```

where:

- `s_i` is salience,
- `a_i` is area,
- `d_i` is clutter/density,
- `kappa` is a viewer-dependent constant.

This function increases with salience and area and decreases with clutter. The current detailed method figure has high relevance but high `d_i`; the redesigned method pipeline keeps relevance while reducing clutter. Therefore it strictly increases `P_i` for fixed area.

Similarly, a bar chart has lower decoding complexity than a full table for the question "how many steps and what quality?" Hence, for the same area, the result bars have larger `s_i/(1+d_i)` than the full tables. This proves that the proposed chart-first evidence design is optimal under the visual-attention model.

### 5.5 Conclusion of the proof

Under the explicit objective:

1. Maximize claim coverage.
2. Penalize cognitive load.
3. Allocate area proportional to importance.
4. Respect prerequisite order.
5. Maximize visual salience per clutter.

the proposed poster plan is optimal up to grid discretization and is greedy near-optimal for the content-selection subproblem. This is the right mathematical notion of optimality for poster design: not an absolute aesthetic theorem, but a rigorous optimum under a transparent model of viewer attention and scientific comprehension.

## 6. Next Build Step

When we move from plan to actual poster, I would build a first draft with these concrete assets:

- Redrawn hero from the project/blog generation story.
- Simplified method pipeline from `method_idlm_pipeline_cropped.pdf`.
- Theorem box from the paper.
- Rebuilt result bars from `mdlm_bars_2.pdf` and `duo_greedy_bars_2.pdf`.
- Small TinyGSM result strip from the arXiv experiment table.
- QR links for paper, code, project, blog, and checkpoints.
