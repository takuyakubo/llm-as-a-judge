# Pydantic AI Integration Guide

このドキュメントでは、LLM-as-a-JudgeフレームワークでのPydantic AI統合について説明します。

## 概要

Pydantic AIは、型安全でプロダクション対応のAIアプリケーションを構築するためのPythonエージェントフレームワークです。LLM-as-a-Judgeでは、Pydantic AIを通じて複数のLLMプロバイダーにアクセスできます。

### サポートされているアプローチ

1. **Pydantic AIフレームワーク経由** (デフォルト・推奨)
   - OpenAI、Anthropic、Google Geminiなど複数のLLMモデルをサポート
   - 型安全で構造化された応答
   - 依存性注入システム
   
2. **直接API呼び出し** (フォールバックオプション)
   - OpenAI API
   - Anthropic API

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成し、使用するプロバイダーのAPIキーを設定：

```bash
# OpenAIモデルを使用する場合
OPENAI_API_KEY=your_openai_api_key_here

# Anthropicモデルを使用する場合
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# デフォルトモデルの設定（オプション）
DEFAULT_MODEL=gpt-4o-mini
```

## 使用方法

### CLIでの使用

```bash
# デフォルト（Pydantic AIフレームワーク経由でGPT-4o-mini使用）
python -m src.cli evaluate tests/rubric.json -f document.txt

# Pydantic AI経由でClaude-3.5を使用
python -m src.cli evaluate tests/rubric.json -f document.txt \
  --provider pydantic_ai --model claude-3-5-sonnet-latest

# 直接OpenAI APIを使用（Pydantic AIを使わない）
python -m src.cli evaluate tests/rubric.json -f document.txt \
  --provider openai --model gpt-4o

# カスタム設定
python -m src.cli evaluate tests/rubric.json -f document.txt \
  --temperature 0.5 --max-tokens 2000
```

### Pythonコードでの使用

```python
from src.criteria import Criteria
from src.evaluator import Evaluator
from src.llm_providers import create_llm_provider, LLMConfig

# 評価基準を読み込み
criteria = Criteria.from_json_file('tests/rubric.json')

# 方法1: デフォルトのPydantic AIフレームワークを使用
evaluator = Evaluator(criteria)

# 方法2: カスタム設定でPydantic AIフレームワークを使用
config = LLMConfig(
    model_name="claude-3-5-haiku-latest",
    temperature=0.3,
    max_tokens=2000
)
provider = create_llm_provider("pydantic_ai", config)
evaluator = Evaluator(criteria, llm_provider=provider)

# 文書を評価
result = evaluator.evaluate_document("評価する文書のテキスト")

# 結果を表示
print(f"Overall score: {result.overall_score:.2f}")
for score in result.scores:
    print(f"{score.criterion_name}: {score.score}/5")
```

## サポートされているモデル

### Pydantic AIフレームワーク経由で使用可能なモデル

Pydantic AIは以下のLLMプロバイダーとモデルをサポートしています：

**OpenAI:**
- gpt-4o
- gpt-4o-mini  
- gpt-4-turbo
- gpt-3.5-turbo

**Anthropic:**
- claude-3-5-sonnet-latest
- claude-3-5-haiku-latest
- claude-3-opus-latest

**Google (Gemini):**
- gemini-1.5-pro
- gemini-1.5-flash

**その他:**
- Groq
- Ollama (ローカルモデル)

## 高度な使用方法

### 非同期評価

```python
import asyncio

async def evaluate_async():
    config = LLMConfig(model_name="gpt-4o")
    provider = create_llm_provider("pydantic_ai", config)
    evaluator = Evaluator(criteria, llm_provider=provider)
    
    # 非同期で評価を実行
    result = await evaluator.evaluate_document_async("文書テキスト")
    return result

# 実行
result = asyncio.run(evaluate_async())
```

### バッチ評価（実装予定）

```python
# 複数の文書を同時に評価
documents = ["文書1", "文書2", "文書3"]
results = evaluator.evaluate_batch(documents)
```

## トラブルシューティング

### API キーエラー

```
Error: Failed to initialize LLM provider: OpenAI API key not provided
```

解決方法：
1. `.env`ファイルに適切なAPIキーを設定
2. または環境変数として直接設定：
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

### モデルが見つからない

最新のモデル名は各プロバイダーのドキュメントを確認してください。

## 例

完全な使用例は`examples/example_with_pydantic_ai.py`を参照してください：

```bash
python examples/example_with_pydantic_ai.py
```

## Pydantic AIフレームワークの利点

1. **型安全性**: Pydanticの型検証により、LLMの応答が期待する形式であることを保証
2. **モデル非依存**: 一つのコードで複数のLLMプロバイダーを切り替え可能
3. **構造化出力**: LLMの応答を構造化されたPydanticモデルとして受け取れる
4. **エラーハンドリング**: 堅牢なエラー処理とリトライメカニズム

## 今後の改善予定

- バッチ処理機能の実装
- Pydantic AIのストリーミングレスポンスサポート活用
- Pydantic AIの依存性注入システムを使った動的プロンプト生成
- 評価結果の詳細分析機能
- Pydantic Logfireとの統合によるモニタリング