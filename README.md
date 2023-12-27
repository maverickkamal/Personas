# ZENTiDE

Zentide uniquely guides your path to self-growth and purpose by revealing AI-powered insights personalized to your DNA, chronorhythm, and higher consciousness through an integrated framework of neural networks, ancient wisdoms and bio-algorithms.



## Problem 

Lack of self-awareness and effective personal growth tools tailored to each individual. People often find themselves stuck in cycles but don't understand the root causes or paths forward.

## Solution

Zentide guides users' self-discovery through daily AI-generated insights personalized to one's chronorhythm, DNA, and higher consciousness. Our app synthesizes the wisdom of astrology, I-Ching, psychology, epigenetics, and neural networks into an integrated framework powering motivational content unique to each person's energies and archetypes.

## Technologies

- **Llamaindex:** Semantic search framework indexing and querying our LLM's knowledge
- **Gemini LLM:** Generative AI model producing personalized guidances with three distinct pipeline which are Google AI studio, Llamaindex Gemini pipeline for Gemini pro vision and Gemini pro
- **Graph Neural Networks:** Encode users' birthdate details to model personality vectors
- **TruLens:** Metrics to evaluate and improve LLM response quality
- **Vectara:** Vector database and embeddings

## Evaluations

TruLens provides quantifiable assessments on gemini content across relevance, grounding and other axes helping us refine model performances.

## Next Steps  

- Expand motivational content modules including journaling
- Grow user community enabling sharing of insights
- Enhance TruLens Triad metrics checks 
- Iterate on neural graph representations of chronobiological patterns


# Notes for Contributors

We welcome contributions across all areas of the Zentide app! As an open project, we aim to foster collaboration pushing personalized AI guidance technology forward. 

A key focus is tightening integration between our Graph Neural Network (GNN) for encoding birthdate data and persona vectors with our Gemini LLM that generates users' daily motivational insights. 

## Challenges and Opportunities

We faced challenges personalizing Gemini's outputs based on the GNN user representations. Limitations included:

- **Lack of prompt engineering frameworks** reducing ability to inject persona vectors into prompts
- **No chat history** due to Google API restrictions hampering multi-turn coherence
- **Custom schema needed** to map GNN embeddings into Gemini prompts

For contributors interested in tackling these problems, potential solutions could explore:

- Researching methods for fine-tuning or prompting LLMs with graph embeddings
- Architecting external memory systems to retain user context across queries
- Creating schema to structure persona vectors as inputs to Gemini 

Exciting opportunities exist here to advance state-of-the-art AI!

Additionally, any contributions on the app frontend, integrations, testing and infrastructure are also highly welcomed. Please reach out or submit a PR!

Let's keep pushing personalized AI to the next level!

## Directory Structure

- main/: Streamlit frontend code
- context/: GNN
- image_processing/: LLM pipelines
- data/: Birthdate datasets and persona vectors
- eval/: TruLens evaluators 
