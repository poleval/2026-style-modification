
# Task 3: Adversarial Style Modification: Probing the Human–AI Perception Gap

## Introduction

We often recognize a writer's style before we can explain what makes it distinctive. A characteristic rhythm, choice of words, or way of constructing sentences can be enough for us to recognize an author's voice. Computational models can also identify authors from patterns in their writing, often with remarkable accuracy. Yet human perception of authorial style and computational authorship attribution have largely been studied separately.

But how closely are the two connected? If a text is modified until a model can no longer identify its author, will human readers lose recognition at the same point?

Our shared task, **Adversarial Style Modification: Probing the Human–AI Perception Gap**, investigates this question experimentally. Participants modify texts to reduce automatic author recognition while preserving the author's style for human readers. Rather than treating adversarial modification solely as a way of fooling a classifier, we use it to probe human and machine sensitivity to stylistic change.

Understanding this relationship matters in at least two contexts. For **authorship obfuscation and privacy**, transformations that successfully conceal identity from automatic systems may still leave users identifiable to human readers. Conversely, **creative protection** may require the opposite: preserving an author's distinctive style for human readers while making it harder for models to learn, imitate, or reproduce that style.

To the best of our knowledge, Adversarial Style Modification is the first benchmark specifically designed to quantify the relationship between automatic authorship recognition and human perception of authorial style under adversarial modification.

The task addresses three central questions:

1. Can automatic author recognition be disrupted while the author's style remains recognizable to humans?
2. How robust are human and machine judgments to the same stylistic modifications?
3. Which types of stylistic changes affect human and machine judgments differently?

## Task

Participants are given short Polish literary fragments written by one of four authors. Their goal is to automatically produce modified versions that:

1. Cause the official authorship classifier to misidentify the original author.
2. Preserve the original meaning of the fragment.
3. Preserve the author's writing style as perceived by human readers.

Participants may apply lexical, syntactic, grammatical, or punctuation modifications, use LLM-based rewriting, adversarial optimization, rule-based transformations, or combinations of these approaches.

## Dataset

The dataset consists of short prose fragments extracted from Polish Wikisource, representing four authors:

- **Bolesław Prus**
- **Henryk Sienkiewicz**
- **Eliza Orzeszkowa**
- **Stefan Żeromski**

Participants will receive two datasets: **Test A** (development) and **Test B** (final evaluation). The **Train** dataset will not be released, as it was used to train the official baseline authorship classifier whose accuracy participants aim to reduce.

> **Important:** The Train, Test A, and Test B datasets are **work-disjoint**: fragments from the same literary work never appear in more than one split. This reduces the influence of work-specific vocabulary, characters, events, and topics on authorship recognition.

## Evaluation

The evaluation consists of two stages: **Test A** (development) and **Test B** (final ranking).

### Test A: Automatic Evaluation

During Test A, participants submit transformed fragments and receive feedback from the official authorship classifier.

The leaderboard reports the classifier's **accuracy on the transformed texts**:

$$
A_{\text{adv}} = \frac{\text{correct automatic author predictions}}{\text{all evaluated transformed texts}}
$$

**Lower accuracy indicates better adversarial performance.** Participants should aim to reduce this value relative to the baseline accuracy measured on the original, unmodified fragments.

Test A does not include official human evaluation. Participants are encouraged to assess stylistic preservation within their own teams.

### Test B: Final Evaluation

During Test B, the official authorship classifier evaluates all valid transformed fragments. In addition, a fixed, stratified sample of **100 transformed texts per team** is evaluated by multiple independent human annotators.

For each transformed fragment, human annotators answer two questions:

1. **Authorial style:** Which of the four candidate authors' writing styles does the fragment most closely resemble?
2. **Semantic preservation:** Has the meaning changed compared with the original fragment?

Both judgments support the evaluation process, but **only the authorial-style judgment contributes to the human accuracy component of the final leaderboard score**. Semantic preservation is treated as a validity requirement (see Rules).

**Human accuracy (H)** measures the proportion of valid human authorial-style judgments that correctly identify the original author:

$$
H = \frac{\text{human judgments correctly identifying the original author}}{\text{all valid human authorial-style judgments}}
$$

The final score combines the reduction in automatic authorship recognition accuracy with human accuracy:

$$
\boxed{\text{FinalScore} = 100 \times (A_{\text{orig}} - A_{\text{adv}}) \times H}
$$

where:

- $A_{\text{orig}}$ is the official classifier's accuracy on the original, unmodified Test B fragments.
- $A_{\text{adv}}$ is the official classifier's accuracy on the valid transformed Test B fragments.
- $H$ is **human accuracy**, calculated from human judgments of authorial style.

A higher final score is better. The score rewards transformations that reduce automatic authorship recognition while keeping the original author's style recognizable to human readers.

## Rules

### 1. Semantic preservation

Transformations must preserve the meaning of the original fragment. Changes that alter factual content, events, relationships, or the intentions of characters are not permitted.

Examples of unacceptable modifications include:

- **Reversing an action:** changing "She opened the door" to "She closed the door."
- **Changing negation:** changing "He did not recognize her" to "He recognized her."
- **Reversing participant roles:** changing "Anna helped Maria" to "Maria helped Anna."
- **Changing factual details:** replacing a character's destination, identity, or other information essential to the original meaning.
- **Adding or removing events:** introducing an action that did not occur in the original fragment or omitting an event that changes its interpretation.

Semantic preservation will be assessed using the official **bidirectional Natural Language Inference (NLI) model** and manual verification.

If more than **30%** of a team's submitted transformations fail the automatic NLI check, the flagged transformations will undergo additional manual verification. An NLI failure alone does not automatically invalidate a transformation.

Organizers may also manually inspect randomly selected transformations from any submission, regardless of their NLI results. Systematic or serious semantic violations confirmed through manual inspection may lead to disqualification.

Semantic preservation is a **validity constraint**, not a component of the ranking score.

### 2. Length restriction

Each transformed fragment must not exceed **400 characters**.

### 3. Automatic transformation

All submitted transformations must be generated automatically. Manual modification of individual test instances is prohibited.

### 4. Human annotation

Teams participating in the final **Test B** evaluation must annotate approximately **200 texts** generated by other systems. Annotation is expected to require approximately **3–4 hours per team**.

Annotators must provide informed consent before participating. For each assigned text, they will assess:

1. Whether the original meaning has been preserved.
2. Which of the four candidate authors' styles the transformed fragment most closely resembles.

Reference writing samples from all four authors will be provided to support style judgments.

Each text will receive **two independent assessments** from participating teams. In cases of disagreement, a **third annotator from the organizing team** will review the text and resolve the conflict.

Annotation will begin only after final submissions have been received and locked. Teams will not evaluate their own transformations.

Teams may involve external human annotators (e.g., recruited through Prolific), provided this is disclosed to the organizers. LLM-based or other automated annotation is prohibited.

Completion of the assigned human annotation is required for inclusion in the final ranking. Failure to complete it may result in disqualification.

Detailed annotation guidelines will be published in the second half of November.
