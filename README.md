# Amplifier

---
A engine to enhance/compliment LLMs to enable complex reasoning/logic, explainability, and steerability.
The purpose of this project is to explore the potential for incremental problem-solving in LLMs through more rigidly
defined reasoning loops.

### Complex Reasoning
Complex Reasoning is a process that is recursive/infinite, it's essentially a search of all accessible information necessary
to solve a problem. To solve a problem with 100% confidence requires access to all information, every piece of information has at least
some relevance to every problem with the right context, even if only to ensure reality is always coherent (assuming that it is). 
For example the knowledge the planets orbit the sun is necessary to validating the claim that gravity exists, because although
gravity works here on earth, it may be that only earth has gravity. Or more abstractly, the knowledge that I
went to the bathroom and nothing unusual happened yesterday is necessary to prove with 100% accuracy that the universe obeys logical rules. As unless you check
there is no absolute guarantee that I ate dinner with a T-Rex.

Therefor, to solve a problem, you have to have a confidence level and a confidence heuristic, something that says how accurate
this needs to be, and something that estimates how likely our answer is to be correct. This project's goal is to implement
this 'problem space' search for LLMs. Although most information is continuous and doesn't come in discrete concepts like language
we assume that enough problems that humans would need to solve can be solved through this medium.

The specific search/accumulate mechanism is the important theoretical part of the project, and is outlined next:

### The Loop

---

I have such a process described in my notes but they're a bit scattered right now so 
// TODO [image]

```math

```
