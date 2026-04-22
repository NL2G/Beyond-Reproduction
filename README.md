# Beyond-Reproduction <br><sub><sup>A Paired-Task Framework for Assessing LLM Comprehension and Creativity in Literary Translation</sup></sub>

[![📄 arXiv](https://img.shields.io/badge/View%20on%20arXiv-B31B1B?logo=arxiv&labelColor=gray)](https://arxiv.org/abs/2604.18169)

## 📁 Repository Structure
```
beyond_imitation/
├── prompt_openrouter.py      # fast API call for efficient and scalable generation and evaluation
├── model_list_full.txt       # Evaluated model list
├── task1_comprehension/                    # Claim-evaluation benchmark
│   ├── task1_dataset/            # task 1 dataset & megred model benchmark outputs (to prevent data label leakage, please download separately; See instructions below)
│   ├── task1_plot/               # generated plots
│   ├── step1_task1_prompt_gen.py # generate prompt
│   ├── step2_task1_batch_run.py  # batch evaluation of models
│   ├── utils.py              # JSON/text for parsing model response
│   └── *.ipynb               # Result analysis and plots generation for results reproducibility
└── task2_ucp/                    # Translational creativity benchmark
    ├── task2_dataset/              # task 2 dataset (annotated En-Zh/En-Nl parallel corpus, file with few-shot examples for prompt generation; model meta + folder intermediate with generated csv during the running + folder result with auto-annotation result by Qwen3-80b)
    ├── step1_task2_TransPrompt_gen.py     # generate prompt for task 1 translation
    ├── step2_batch_task2_translation.py   # batch translation generation of models
    ├── task2_evaluator.py    # batch auto-annotation of models
    └── *.ipynb               # Auto-eval pipeline and human-eval analysis
```

---

## 🚀 Usage

- **Two benchmark tasks**:
  - Task 1 model benchmark and adversarial test, see [task1](task1_comprehension/)
  - Task 2 analysis of human annotation and automatic annotation, see [task2](task2_ucp/)
 
- Instructions to run translation generation and evaluation with the shared runner
- All experiments use a unified interface (we also upload batch run .py for each separate task):
```bash
# Step 1: Build prompts from datasets
## for task 1:
python step1_task1_prompt_gen.py
## for task 2:
python step1_task2_TransPrompt_gen.py
```
```bash
# Step 2: run translation generation and evaluation with the shared runner separately or in batch
python prompt_openrouter.py \
  --file path/to/prompt.csv \
  --model anthropic/claude-3.7-sonnet:thinking \
  --temperature 0.3 \ # (for Task 1 benchmark: 0.3 for less randomness while preserving literary reasoning; for task 2 auto-annotation: 0 for reproducibility; for task 2 literary translation: 0.7 for creative freedom)
  --content-column prompt \
  --output-dir path/to/output.csv

Key arguments:
--file: input CSV with prompts
--model: OpenRouter model ID
--content-column: column sent as input
--temperature: sampling temperature
--output-dir: output location
```

```bash
#Step 2: run evaluation/translation in batch
## for task1:
python step2_task1_batch_run.py
## for task2 translation:
python step2_batch_task2_translation.py
## for task2 evaluation:
# Run step3_1_AutoEval_pipeline.ipynb for prompt and data preparation, and when instructed run: 
python step3_2_task2_evaluator.py
```

- **Instructions to reproduce results** in Tasks 1 and 2, see .ipynb in Task 1 and 2 folders.
- **To download annotated datasets** upon agreeing on the following conditions: This dataset is intended for academic purposes only. To present label leakage, please do not upload/redistribute this data without the author's consent. The use of this dataset requires agreement to the conditions listed in the [form]([https://forms.gle/tGi64MBt59HL4QBQ7](https://forms.gle/UeVjEPrrnJx7D4Yv5)). The dataset will be available for downloading after filling out the form. 

## 📊 Dataset Overview
![Task summary](Fig/figure1.png)

## 🤝 Contributing

Feel free to contribute by submitting a pull request.

```bash
# Fork the repository
# Create a new branch for your feature or fix
# Commit your changes with a clear message
# Push to your fork and submit a PR
```

---

## 📜 License

Specify the license under which this code is shared.

> This project is licensed under the CC License - see the [LICENSE](LICENSE) file for details.

---

## 📖 Citation

If you use this work in your research, please cite it as:

```bibtex
@misc{zhang2026reproductionpairedtaskframeworkassessing,
      title={Beyond Reproduction: A Paired-Task Framework for Assessing LLM Comprehension and Creativity in Literary Translation}, 
      author={Ran Zhang and Steffen Eger and Arda Tezcan and Wei Zhao and Simone Paolo Ponzetto and Lieve Macken},
      year={2026},
      eprint={2604.18169},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2604.18169}, 
}
```

---
