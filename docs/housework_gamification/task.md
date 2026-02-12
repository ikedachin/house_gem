# 家事分担アプリ (Housework Gamification) - Task List

## フェーズ 1: 設計とセットアップ
- [x] 要件定義と基本設計 (docs/housework_gamification/implementation_plan.md 作成)

- [x] Djangoプロジェクトのセットアップ
    - [x] `django-admin startproject`
    - [x] 共通設定 (日本語、タイムゾーン、SQLite)
    - [x] カスタムUserモデルの準備
- [x] スタイリング基盤の整備
    - [x] CSS設計 (ポップで明るいテーマ)
    - [x] ベーステンプレート作成

## フェーズ 2: コア機能実装 (MVP)

- [x] アカウントとグループ管理 (Accounts App)
    - [x] ユーザー登録・ログイン画面
    - [x] 家グループ (HouseGroup) 作成・招待・参加機能

- [x] 家事タスク管理 (Chores App - Part 1)
    - [x] 家事タスク (Chore) モデル作成
    - [x] [カテゴリ/属性] マスタ作成 (JSONFieldで対応)
    - [x] タスク作成・編集・削除画面
    - [x] タスク一覧画面 (フィルタリング)

- [x] 家事実行とポイント (Chores App - Part 2)
    - [x] 家事実行記録 (ChoreExecution) モデル
    - [x] 「完了」アクションの実装 (ポイント付与ロジック)
    - [x] 履歴表示 (ダッシュボードに追加)
- [x] 週次集計とランキング (Gamification App)
    - [x] 週次集計ロジック (WeeklyScore)
    - [x] ランキング画面
    - [ ] 週リセット/締め処理の実装

## フェーズ 3: 分析と拡張


- [x] 分析ダッシュボード
    - [x] ユーザー別貢献度グラフ
    - [x] 家事属性別分析
- [x] UI/UX ブラッシュアップ
    - [x] アニメーション追加 (完了時の演出など)
    - [x] レスポンシブ確認 (CSSでrem/percentage使用済)

## フェーズ 4: ドキュメントと検証

- [x] テスト実施
- [x] Walkthrough作成 (docs/housework_gamification/walkthrough.md)
