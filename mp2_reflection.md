# MP2 Reflection — complete after running the project

**Corpus used:** Ten original research-summary text documents based on my three papers about social-media depression and suicide-risk text analysis. 

## What worked

**To fill in after I actually test the program:** Which source match succeeded? Question (blank to finish):
What is the role of TF-IDF in depression detection?

TF-IDF (Term Frequency–Inverse Document Frequency) plays a role in depression detection by describing the importance of terms within the collected text data. It is used in the preprocessing step of the SADDSM pipeline to generate information that helps in identifying relevant features associated with depression-related content in social media texts [Source: Depression and Suicide Features and Fusion — Part 1].
Retrieved: 06_depression_and_suicide_features_and_fusion.txt, 02_data_sources,_collection_and_label_quality.txt, 01_research_scope_and_motivation.txt

## What didn't work

 How do the IDCNN -squeezenet model and the DU-POA optimizd ensemble differ in their approach to depression detect

I cannot find specific information comparing the IDCNN-SqueezeNet model and the DU-POA optimized ensemble in their approaches to depression detection. The excerpts provided mention both models and their components but do not detail their differences in approach. [Source: IDCNN–SqueezeNet Hybrid Method — Part 5]

Retrieved: 07_du-poa_ensemble,_results_and_ablation.txt, 01_research_scope_and_motivation.txt, 08_idcnn-squeezenet_hybrid_method.txt

## What I'd change

With more time, I would try paragraph-based chunking instead of only using fixed 500-character chunks. I would then compare the retrieval results using the same golden questions to see whether paragraph-aware chunks improve source matching and answer quality.

## One surprise
I was surprised that the system was able to ingest all 10 research documents and create 61 chunks successfully with a simple 500-character chunking method. I expected the setup to be more complicated, but once the API and Qdrant connections were configured correctly, the ingestion process was straightforward.
## Validation output

Validating 2 questions from predefined_questions.jsonl
PASS p1_stacked_components
 Question: Which three deep learning classifiers are combined in the stacked ensemble research?
 Answer: The three deep learning classifiers combined in the stacked ensemble research are Bidirectional Gated Recurrent Unit (Bi-GRU), Deep Maxout, and Improved Convolutional Neural Network (ICNN) [Source: Stacked Ensemble Classifier and SASSOA — Part 1].
 Retrieved sources: 05_stacked_ensemble_classifier_and_sassoa.txt, 06_depression_and_suicide_features_and_fusion.txt, 07_du-poa_ensemble,_results_and_ablation.txt
 Expected source: 05_stacked_ensemble_classifier_and_sassoa.txt
 Expected phrases: 3 / 3
 Time: 2097 ms

PASS p2_hybrid_layers
 Question: Which feature types does the IDCNN-SqueezeNet hybrid take from the social media text?
 Answer: The IDCNN-SqueezeNet hybrid takes the following feature types from the social media text: TF-IDF, n-grams, and Bag of Words (BoW) [Source: IDCNN–SqueezeNet Hybrid Method — Part 1].
 Retrieved sources: 08_idcnn-squeezenet_hybrid_method.txt, 09_comparative_evaluation_and_reported_metrics.txt
 Expected source: 08_idcnn-squeezenet_hybrid_method.txt
 Expected phrases: 3 / 3
 Time: 1953 ms

Source-match: 2/2

Validating 3 questions from learner_questions.jsonl
PASS q3_easy
 Question: What does SASSOA optimize in the first journal study?
 Answer: I cannot find information regarding what SASSOA specifically optimizes in the first journal study. [Source: Stacked Ensemble Classifier and SASSOA — Part 3]
 Retrieved sources: 05_stacked_ensemble_classifier_and_sassoa.txt, 09_comparative_evaluation_and_reported_metrics.txt
 Expected source: 05_stacked_ensemble_classifier_and_sassoa.txt
 Expected phrases: 0 / 2
 Time: 2391 ms

PASS q4_medium
 Question: Which features are combined by modified mutual information fusion before the DU-POA ensemble classifies social media text?
 Answer: I cannot find the specific features that are combined by modified mutual information fusion before the DU-POA ensemble classifies social media text in the provided excerpts. [Source: Depression and Suicide Features and Fusion — Part 3]
 Retrieved sources: 06_depression_and_suicide_features_and_fusion.txt
 Expected source: 06_depression_and_suicide_features_and_fusion.txt
 Expected phrases: 0 / 3
 Time: 1870 ms

PASS q5_hard
 Question: Why should the three different accuracy numbers reported for the DU-POA study not be treated as one single result?
 Answer: The three different accuracy numbers reported for the DU-POA study should not be treated as one single result because they come from different contexts and experimental setups. The abstract reports an accuracy of 0.962 at 90% training data, while Table 4 shows an accuracy of 0.975229 for the proposed model in a conventional-classifier comparison, and Table 5 presents an accuracy of 96.40% in its ablation setting. Each of these figures reflects distinct aspects of the study and should be retained with their specific contexts rather than averaged or incorrectly described as the same experiment [Source: Comparative Evaluation and Reported Metrics — Part 3].
 Retrieved sources: 07_du-poa_ensemble,_results_and_ablation.txt, 09_comparative_evaluation_and_reported_metrics.txt, 10_limitations,_ethics_and_retrieval_guide.txt
 Expected source: 09_comparative_evaluation_and_reported_metrics.txt
 Expected phrases: 3 / 3
 Time: 3264 ms

Source-match: 3/3
