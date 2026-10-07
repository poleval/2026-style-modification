# Adversarial Style Modification: Probing the Human–AI Perception Gap

## Introduction

We often recognize a writer's style before we can explain what makes it distinctive. A characteristic rhythm, choice of words, or way of constructing sentences can be enough for us to recognize an author's voice. Computational models can also identify authors from patterns in their writing, often with remarkable accuracy. Yet human perception of authorial style and computational authorship attribution have largely been studied separately.

But how closely are the two connected? If a text is modified until a model can no longer identify its author, will human readers lose recognition at the same point?

Our shared task, **Adversarial Style Modification: Probing the Human–AI Perception Gap**, investigates this question experimentally. Participants modify texts to reduce automatic author recognition while preserving the author's style for human readers. Rather than treating adversarial modification solely as a way of fooling a classifier, we use it to probe human and machine sensitivity to stylistic change.

Understanding this relationship matters in at least two contexts. For **authorship privacy**, transformations that successfully conceal identity from automatic systems may still leave users identifiable to human readers. Conversely, **creative protection** may require the opposite: preserving an author's distinctive style for human readers while making it harder for models to learn, imitate, or reproduce that style.

To the best of our knowledge, **Adversarial Style Modification** is the first benchmark specifically designed to quantify the relationship between automatic authorship recognition and human perception of authorial style under adversarial modification.

The task addresses three central questions:

1. Can automatic author recognition be disrupted while the author's style remains recognizable to humans?
2. How robust are human and machine judgments to the same stylistic modifications?
3. Which types of stylistic changes affect human and machine judgments differently?

## Task

Given a short literary fragment written by one of four Polish authors, participants must automatically produce a modified version that:

- causes the official authorship classifier to misidentify the original author;
- preserves the meaning of the original fragment;
- preserves the author's style as perceived by human readers.

Participants may apply lexical, syntactic, grammatical, punctuation-related, or other transformations using LLM-based rewriting, adversarial optimization, search-based strategies, rule-based methods, or combinations thereof.

## Dataset

The dataset contains short fragments of Polish literary prose by:

- **Bolesław Prus**
- **Henryk Sienkiewicz**
- **Eliza Orzeszkowa**
- **Stefan Żeromski**

The texts are obtained from Polish Wikisource.

> **Important:** Train, Test A, and Test B sets are **work-disjoint**: fragments from the same literary work never occur in more than one split.

This reduces reliance on work-specific vocabulary, characters, events, or topics rather than general characteristics of authorial style.

## Evaluation

Evaluation consists of **Test A** for development and **Test B** for the final ranking.

### Test A

Test A provides automatic feedback through the PolEval system. Participants can observe the reduction in accuracy of the official authorship classifier.

Let:

- $A_{orig}$ denote classifier accuracy on the original fragments;
- $A_{adv}$ denote classifier accuracy on the transformed fragments.

The model accuracy drop is:

$$
D_{model} = A_{orig} - A_{adv}
$$

No official human evaluation is performed on Test A. Participants should therefore assess within their own teams whether transformations preserve recognizable authorial style.

### Test B

Test B combines machine and human evaluation. The authorship classifier is evaluated on all valid transformed fragments.

In addition, a fixed stratified sample of **100 transformed texts per team** is evaluated by multiple independent human annotators, who identify which of the four authors the text most resembles stylistically.

Human Style Recognition is defined as:

$$
H =
\frac{\text{correct human author judgments}}
{\text{all valid human author judgments}}
$$

The final score is:

$$
\boxed{
FinalScore = 100 \times (A_{orig} - A_{adv}) \times H
}
$$

Thus, a high score requires both a substantial reduction in machine recognition and high human recognition of the original author's style.

Human annotators will additionally assess naturalness/quality to identify transformations that achieve adversarial success by producing corrupted or unnatural language.

## Rules

### 1. Semantic preservation

The transformed text must preserve the meaning of the original fragment.

Semantic preservation will be screened using the official **bidirectional NLI model** and will also be assessed during manual annotation. Independently of the NLI results, the organizers may randomly sample and manually inspect transformations from any submission to verify compliance with this requirement.

In addition, if more than **30% of a team's examples fail the automatic NLI criterion**, the flagged transformations will undergo additional manual verification.

Semantic preservation is **not part of the ranking score**; it serves as a validity constraint to prevent systems from reducing authorship-classification accuracy by altering content rather than style.

NLI failure alone does not invalidate a submission. However, systematic or serious violations of the semantic-preservation requirement confirmed through manual inspection may result in disqualification.

### 2. Length

A transformed fragment must not exceed **400 characters**.

### 3. Automatic transformation

Manual modification of individual test instances is prohibited.

### 4. Human annotation

Teams participating in the final **Test B** evaluation must annotate approximately **200 texts** generated by other systems (estimated time: **3–4 hours per team**).

Annotators must consent to participation and to the use of their judgments for research purposes.

For each text, annotators will:

- assess semantic preservation;
- identify which candidate author's style it most closely resembles.

Reference samples from all authors will be available throughout the evaluation.

Each text will receive **two independent team assessments**, with an organizer resolving disagreements.

Annotation begins only after a team's final submission, which is then **locked**. Teams will not evaluate their own outputs.

Annotation may be delegated to external human annotators (e.g., via Prolific), provided this is disclosed in the system paper. **LLM-assisted or automated annotation is prohibited.**

Completion of all assigned annotations is required for inclusion in the final ranking; failure to submit them will result in disqualification.

Detailed annotation guidelines will be released in the **second half of November**.
