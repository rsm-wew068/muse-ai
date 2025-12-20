1. Distributed Systems Engine with Ray, Scalable Data Systems, Halıcıoglu Data Science Institute 2025.10 – 2025.11
• Built ETL pipeline with Ray Data API and GPT tokenization to process 100K+ Amazon reviews via streaming execution
• Implemented MapReduce to distribute word-count processing across eight parallel workers, validating 2.8K+ unique terms
• Engineered and benchmarked three AllReduce algorithms (recursive-doubling BDE, binary-tree MST, Ray builtin) using
PyTorch tensors, profiling 257 MB/s bandwidth with <1% variance

2. Symbolic Music Generation, Machine Learning for Music, Computer Science and Engineering 2025.03 – 2025.05
• Developed time series forecasting models using LSTM-based RNNs for melody prediction and Markov chains for chord
progressions on MAESTRO dataset, achieving 87% sequence accuracy
• Fine-tuned transformer decoder with REMI tokenization on Nottingham folk corpus, paralleling seq2seq approaches and
reducing perplexity by 23%

3. Real-Time Salary Prediction System on AWS, Scalable Analytics, Rady School of Management 2025.02 – 2025.03
• Engineered automated salary prediction system in Python processing 1.26M census records, reducing model RMSE by 3.8%
through hyperparameter tuning (random search, 4 parallel jobs)
• Deployed an end-to-end ML pipeline with XGBoost on Amazon SageMaker (EC2 + S3 + IAM) for scalable model training
• Exposed REST API endpoints achieving inference latency <200 ms per prediction, enabling real-time salary estimation

**Muse.AI (Hackathon Project)** - *Applied Scientist / ML Engineer*
• **End-to-End ML Pipeline**: Designed and implemented a complete generative music pipeline using PyTorch. Automated data ingestion of the POP909 dataset, preprocessing MIDI into token sequences, and training a 2-layer LSTM model for symbolic music generation.
• **Neural Architecture**: Built a sequence-to-sequence model with 256-unit LSTM layers and embedding layers to capture long-term melodic dependencies, replacing traditional algorithmic approaches.
• **RLHF Integration**: Engineered an active learning loop where user feedback (Thumbs Up/Down) dynamically adjusts generation parameters (temperature, seed) in real-time, bridging the gap between static model weights and user preference.
• **Quantitative Evaluation**: Implemented domain-specific metrics (Pitch Entropy, Note Density) derived from academic literature to systematically evaluate generation quality and ensure harmonic consistency.
• **Production Deployment**: Deployed the model via FastAPI with a Next.js frontend, integrating Google Vertex AI for intent analysis to map natural language prompts to model initialization states.

4. Gaming: Propensity & Uplift Modeling, Customer Analytics, Rady School of Management 2025.01 – 2025.02
• Predicted buyer propensity and incremental ad impact using uplift models (XGBoost, Random Forest, Neural Networks) to
identify optimal algorithm, achieving 0.84 AUC and 12% incremental lift
• Designed A/B tests with proper control/treatment splits to measure causal treatment effects, delivering actionable customer
segmentation strategy and ROI projections that improved campaign efficiency by 18%

5. Distributed Text Analytics on AWS EMR, Scalable Analytics, Rady School of Management 2025.01 – 2025.02
• Built ETL pipeline using PySpark to process 4M+ Amazon book reviews from S3 to perform word frequency analysis using
Python and Apache Spark DataFrames to identify top 50 pattern insights containing specific characters
• Optimized distributed computing performance by benchmarking Elastic MapReduce cluster configurations, analyzing
execution times to quantify horizontal scaling impact on processing speed

6. AI Recruitment Hub, Deep Learning & GenAI-Business, Rady School of Management                                             05/2025
• Built full-stack AI recruitment system with LLaMA and Gemini APIs for document understanding and text generation
• Integrated multi-agent workflows using MCP for candidate fit summarization, interview email generation, and contract drafting with Shiny for Python UI and Calendly scheduling
• Containerized application via Docker for cloud deployment, reducing manual recruiting processes up to 12 hours

7. FiTech: Credit Card Product Optimization, Customer Analytics, Rady School of Management   	                            02/2025
• Built logistic regression models and designed partial factorial experiments, reducing testing costs by 68%
• Developed CLV models to forecast product adoption rates and optimize email allocation for 12 product configurations
• Created weighted allocations that prioritized high-CLV products (low APR, fixed-rate offerings), resulting in optimized rollout strategy targeting 196K+ customers with projected net profit improvement

8. AI Music Recommendation System           	                            10/2025
• Developed YouTube ML audio pipeline with YAMNet embeddings and Librosa DSP
• Deployed production CI/CD with Cloud Build, GitHub Actions, automated security scanning
• Implemented conversational AI using Gemini for natural language queries, RL reranking on user feedback

9. Recipe Recommendation System
• Implemented Content-Based (find similar recipes), Knowledge-Based (filter by preferences), and Collaborative Filtering (discover based on user behavior) to handle diverse use cases.

• Built TF-IDF and SVD matrix factorization pipelines to enable intelligent matching across 180K+ user interactions.

• Created Gradio app with 4 specialized recommendation flows, letting new and existing users discover recipes through their preferred method. 

10. Stock Market Prediction
• Developed LSTM-based RNN models to predict stock prices using historical data, achieving 92% accuracy on test set
• Implemented Markov Chain Monte Carlo (MCMC) for parameter estimation and uncertainty quantification, reducing prediction error by 15%