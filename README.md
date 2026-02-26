
# About This Project (For Recruiters)
# Sadisfied

A LangGraph-based multi-node conversational agent with emotion analysis, risk routing, memory management, and persistence support.

---

## 1. Overview

Sadisfied is a state-driven conversational agent built on **LangGraph**.  
The system is centered around a structured `GraphState` and a directed execution graph composed of multiple functional nodes.

The project focuses on:

- Structured multi-node agent architecture  
- Risk-aware response routing  
- Session-level memory management  
- Modular and testable system design  

---

## 2. System Architecture

The agent is implemented as a directed state graph:
preprocess → emotion → risk
↘
safe_response / normal_response
↓
self_critique
↓
memory
↓
persist

### Node Responsibilities

| Node | Responsibility |
|------|---------------|
| preprocess | Build inference context (summary + recent messages) |
| emotion | Multi-language emotion classification |
| risk | Risk level assessment based on emotion distribution |
| safe_response | Crisis intervention template |
| normal_response | Standard LLM-generated reply |
| self_critique | Secondary response validation/modification |
| memory | Dialogue summarization and pruning |
| persist | State persistence and session isolation |

---

## 3. Technology Stack

### Core Framework

- **LangGraph** — State-based agent execution graph  
- **LangChain Core Messages** — Unified message abstraction  
- **Ollama (Local LLM)** — On-device language model inference  

---

### Emotion Analysis Module

The emotion classifier supports multilingual input:

- `langdetect` — Language detection  
- `SnowNLP` — Chinese sentiment analysis  
- `TextBlob` — English sentiment analysis  
- `textblob-fr` — French sentiment analysis  

Emotion output includes:

- Primary label  
- Secondary label  
- Confidence score  
- Probability distribution  

Keyword-weighted scoring enhances detection of:
- Despair  
- Anger  
- Sadness  

---

### Risk Assessment

Risk evaluation is implemented through `SafetyRules`:

- Multi-level risk scoring (0 / 1 / 2)
- Strong despair override mechanism
- Integrated routing control via conditional graph edges

---

### Memory Management

The memory system operates on two conceptual layers:

1. **Session-level GraphState** (full conversation state)
2. **Summary-level memory compression**

The `memory_node` supports:

- Periodic summarization
- Message pruning (retain last N messages)
- Controlled state compression

The design allows future separation of:

- Semantic memory
- Full snapshot state

---

### Persistence Layer

A custom `persist_node` replaces the default checkpointer mechanism.

Features:

- Emotion storage
- Risk storage
- Message storage
- Session isolation

Design considerations:

- Avoid mandatory full-state reload
- Enable selective loading (summary vs full messages)
- Support future Redis or semantic storage backends

---

## 4. Testing & Engineering Practices

The project includes structured test layers:

- Unit tests  
- Parameterized risk validation  
- LLM failure simulation (mocked tests)  
- Routing verification  
- Memory behavior validation  
- Safe-response behavioral tests  

Current coverage:
Total Coverage ≈ 70%+

Testing focuses on:

- State transitions  
- Routing logic  
- Side-effect validation  
- Failure handling  

---


## 5. Future Improvements

Planned enhancements include:

- Clear separation of semantic memory and full snapshot state  
- More advanced emotion modeling  
- Improved concurrency and session isolation  
- Extended self-critique logic  
- Increased test coverage (>80%)  

---

## 6. Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Start local LLM:
```bash
ollama serve
```
Launch application:
```bash
python app.py
```

## Project Scope

Sadisfied is an experimental structured-agent system focusing on:

Multi-node state-driven execution

Risk-aware response routing

Extensible memory architecture

Testable AI system design

It serves as a technical exploration of modular conversational agents built on graph-based state transitions.


# 个人废话
## 想法来源
从原本的专业转向计算机的过程中，我常常会怀疑自己是否真的适合这条路。
来到法国之后，语言的障碍和生活环境的改变，让这种不确定感更加明显。
于是我想要做一个可以持续记住对话、能在风险时给予支持的agent

## 关于名字
它来自 satisfied 的谐音，也包含 “sad” 的意味。
同时 S.A.D 也是 Seasonal Affective Disorder（季节性情感障碍）的缩写——
一种与季节变化显著相关的情绪障碍，通常被归类为重度抑郁障碍的一种季节性亚型。
也算一词多用了

## 关于记忆的设计
我不希望用户每次刷新页面后，对话记忆就全部丢失。
因此我设计了：

memory_repo —— session_id ↔ GraphState 的适配器

每个 session 都对应一个完整 GraphState。

同时，我刻意没有采用官方推荐的 checkpointer 机制，而是自己实现 persist_node，原因包括：

有些场景不希望每次加载完整 messages

有些任务只需要 summary

有些分析只读取 memory，不执行 graph

希望未来更灵活地拆分 semantic memory 与 full snapshot

目前数据库结构中依旧预留了：
semantic_repo.py  ← summary / emotion / preference
state_repo.py     ← 完整 GraphState
但由于时间问题 还未实现啦啦

## 成本说明！！💰
没有采用外部的llm，因为在这个阶段我不想花一分钱。所以项目目前基于本地的Ollama运行

## 其他
目前界面太难看了还没来得及优化，未来继续升级会重新设计交互体验
当前的情感分类比较简单（？，但因为数据集比较难找，不是我目前想要花时间的重点，所以就先保持这样了
未来想自训练一个textCNN


## 测试

| 文件 | 语句数 (Stmts) | 未覆盖 (Miss) | 覆盖率 (Cover) |
|----|----:|----:|----:|
| __init__.py | 0 | 0 | 100% |
| app.py | 60 | 60 | 0% |
| config.py | 11 | 0 | 100% |
| conftest.py | 3 | 0 | 100% |
| db/__init__.py | 0 | 0 | 100% |
| db/memory_repo.py | 50 | 50 | 0% |
| db/models.py | 33 | 0 | 100% |
| db/redis_client.py | 15 | 15 | 0% |
| db/repo.py | 22 | 0 | 100% |
| db/semantic_repo.py | 0 | 0 | 100% |
| db/state_repo.py | 0 | 0 | 100% |
| graph/__init__.py | 0 | 0 | 100% |
| graph/builder.py | 33 | 0 | 100% |
| graph/state.py | 14 | 0 | 100% |
| nodes/__init__.py | 0 | 0 | 100% |
| nodes/emotion.py | 3 | 0 | 100% |
| nodes/memory.py | 28 | 3 | 89% |
| nodes/normal_response.py | 7 | 0 | 100% |
| nodes/persist.py | 32 | 4 | 88% |
| nodes/preprocess.py | 11 | 1 | 91% |
| nodes/risk.py | 12 | 3 | 75% |
| nodes/safe_response.py | 6 | 0 | 100% |
| nodes/self_critique.py | 22 | 8 | 64% |
| services/__init__.py | 0 | 0 | 100% |
| services/emotion_classifier.py | 105 | 24 | 77% |
| services/llm.py | 16 | 4 | 75% |
| services/safety_rules.py | 28 | 6 | 79% |
| services/summarize.py | 9 | 1 | 89% |
| setup.py | 2 | 2 | 0% |
| test/test_emotion.py | 6 | 0 | 100% |
| test/test_graph.py | 11 | 0 | 100% |
| test/test_llm_fail.py | 8 | 0 | 100% |
| test/test_memory.py | 6 | 0 | 100% |
| test/test_para_risk.py | 7 | 0 | 100% |
| test/test_risk.py | 5 | 0 | 100% |
| test/test_route.py | 7 | 0 | 100% |
| test/test_saferesponse.py | 22 | 0 | 100% |
| test/test_sammarize.py | 6 | 0 | 100% |
| test/test_selfcritique.py | 6 | 0 | 100% |
| test/test_summary.py | 9 | 0 | 100% |
| **TOTAL** | **615** | **181** | **71%** |

