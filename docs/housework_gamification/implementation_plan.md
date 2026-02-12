# 家事分担アプリ 実装計画書 (Implementation Plan)

## 1. 要件の整理 (Requirements)

### 用語定義
- **HouseGroup (家グループ)**: 家事を共有する単位（家族、ルームシェアなど）。
- **Chore (家事タスク)**: 実施すべき家事のテンプレート（例：「ゴミ出し」「風呂掃除」）。
- **Execution (実行記録)**: 誰がいつどのタスクを実施したかの記録。
- **Point (ポイント)**: 家事を実施することで得られるスコア。
- **Cycle (サイクル)**: ランキングを集計する期間（基本は1週間）。

### ユーザーストーリー
- **AS A** 同居人 **I WANT TO** 家事をタスクとして登録・共有したい **SO THAT** 言わなくてもやるべきことがわかるようにする。
- **AS A** ユーザー **I WANT TO** 完了した家事を記録してポイントを貯めたい **SO THAT** 目に見える成果として承認欲求を満たしたい・勝負に勝ちたい。
- **AS A** ユーザー **I WANT TO** 週次で誰が一番頑張ったかを知りたい **SO THAT** お互いの貢献を称え合い、モチベーションを維持したい。

---

## 2. 画面一覧と要素 (Screens)

| 画面名 | URL | 主要機能・導線 | 必要な要素 |
| :--- | :--- | :--- | :--- |
| **LP / Login** | `/login/` | アプリ説明、ログイン、新規登録 | ロゴ、キャッチコピー、Login Form, Signup Link |
| **Signup** | `/signup/` | アカウント作成 -> グループ参加/作成へ | Username, Email, Password Form |
| **Onboarding** | `/setup/` | 所属グループの作成または招待コード入力 | "Create Group" or "Join Group" forms |
| **Dashboard** | `/` | 現在のポイント状況、注目のタスク、クイックアクション | 今週のランキング(簡易)、未完了タスクリスト、「やった！」ボタン |
| **Chore List** | `/chores/` | 全タスクの管理・編集・実行 | タスク一覧、フィルタ(自分/全員)、追加ボタン |
| **Chore Detail** | `/chores/<id>/` | タスク詳細、履歴、属性編集 | タスク説明、ポイント、担当者、過去の実施履歴 |
| **Chore Add/Edit**| `/chores/add/` | 家事の登録・編集 | タイトル、説明、ポイント、頻度、属性入力 |
| **Weekly Report** | `/ranking/` | 週次集計結果、過去の勝敗 | 今週のグラフ、過去のウィナー、サイクル切り替え |
| **Analysis** | `/analysis/` | 個人の傾向分析 | 属性別貢献度（パイチャート）、月次推移 |

### デザインイメージ (Pop & Bright)
- **カラーパレット**:
    - Primary: `Orange/Coral` (元気、活動的)
    - Secondary: `Teal/Mint` (清潔感、安心)
    - Text: `Dark Grey` (視認性確保)
    - Background: `Off-white` / Card: `White` with soft shadow
- **コンポーネント**:
    - 角丸の大きいカード (Card UI)
    - わかりやすいアイコン (Material Symbols Rounded)
    - ポイント獲得時のポップアップ演出 (Confetti animation)

---

## 3. データモデル設計 (Data Models)

### ER図（概念）
`User` --(N:1)--> `HouseGroup`
`Chore` --(N:1)--> `HouseGroup`
`ChoreExecution` --(N:1)--> `Chore`, `User`
`WeeklyScore` --(N:1)--> `User`, `Cycle`

### 定義詳細

#### 1. CustomUser
- Django標準の `AbstractUser` を継承
- `nickname`: 表示名
- `icon`: プロフィールアイコン画像

#### 2. HouseGroup
- `name`: 家の名前（例：「田中家」）
- `invite_code`: 招待用コード（一意）
- `members`: `User` との ManyToMany または User側に ForeignKey（今回はシンプルにUserにgroupIDをもたせるか、M2Mで複数所属可にするか。MVPは **UserにForeignKey** で1人1グループ所属とする）

#### 3. Chore (家事タスク)
- `group`: FK(HouseGroup)
- `title`: タスク名
- `description`: 詳細
- `base_points`: 基本ポイント (Int)
- `difficulty`: 難易度 (1-5) - ポイント係数に利用
- `category`: カテゴリ (掃除, 料理, 名もなき家事, etc) - 分析用
- `attributes`: JSONField or M2M (属性タグ: "力仕事", "時間かかる")
- `frequency`: 推奨頻度 (毎日, 週1 etc) - リマインド用(将来拡張)

#### 4. ChoreExecution (実行履歴)
- `chore`: FK(Chore)
- `performer`: FK(User)
- `completed_at`: DateTime (Auto Now)
- `points_earned`: Int (記録時の計算結果を固定で保持)
- `status`: (APPROVED, PENDING) - MVPは基本APPROVED(即時承認)

#### 5. WeeklyScore (集計)
- `group`: FK(HouseGroup)
- `user`: FK(User)
- `year`: Int
- `week_number`: Int (ISO週番号)
- `total_points`: Int
- `rank`: Int (その週の順位)

---

## 4. 主要ユースケースのシーケンス

### A. 家事の実行とポイント付与
1. **User** logs in and views **Dashboard**.
2. **User** clicks "Done" on a specific **Chore**.
3. **Server** calculates points: `base_points * multipliers`.
4. **Server** creates `ChoreExecution` record with status `APPROVED`.
5. **Server** updates (or increments) `WeeklyScore` for the current week.
6. **Server** returns success response with animation trigger.
7. **Client** shows "You earned 100 pts!" popup.

### B. 週次リセット（バッチ/アクセス時判定）
1. User accesses the **Dashboard**.
2. System checks if the current date is in a new week compared to the last access.
3. If new week:
    - Finalize previous week's `WeeklyScore`.
    - Create new `WeeklyScore` records for this week (0 points).
    - Display "Last Week's Winner: [User]!" notification.

---

## 5. 未解決課題への設計案

### A. ポイントの付け方
**推奨案: 基準点 + 属性係数システム**
- **Base**: 全タスク一律ではなく、ユーザー入力の「難易度(1-3)」または「所要時間(分)」をベースにする。
    - 例: `Time(min) * 10`pts。 15分の皿洗い = 150pts。
- **Multiplier**: 属性タグによるボーナス。
    - 「力仕事」: x1.2
    - 「汚い/嫌われ」: x1.5
    - 「名もなき家事」: x2.0 (発見してやったことを称賛)
- **Rationale**: 時間ベースは客観的で納得感が高い。「嫌なこと」にボーナスをつけることで不公平感を減らす。

### B. ポイントのリセットタイミング
**推奨案: 月曜午前4時切り替え (ISOカレンダー準拠)**
- 日曜夜に追い込み家事が発生するため、日曜24時(月曜0時)だと深夜の活動が分断される。
- Djangoの `isocalendar()` は月曜始まり。
- **実装**:
    - DBには「実施日時」が正確に残る。
    - 表示/集計時に `(date - timedelta(hours=4)).isocalendar()[1]` を週番号として扱うことで、月曜未明4時までを前週の日曜扱いにするロジックを組み込む。（「深夜残業」扱い）
    - 過去週のスコアは動的に集計せず `WeeklyScore` テーブルに確定させる。

### C. 家事属性の自動設定
**推奨案: キーワード辞書マッチング (Rule-based) [MVP]**
- タスク名に含まれる単語から属性を自動タグ付けする。
- 辞書例:
    - `{ "洗": ["水仕事"], "掃除": ["体力"], "ゴミ": ["汚れ"], "買い": ["外出"] }`
- **User Experience**:
    - タスク名入力時、リアルタイムまたは保存時にタグが提案される。「これでいいですか？」-> User承認。
    - 完全に隠蔽せず、初期値入力の補助として使うことでストレスを軽減。

---

## 6. ルーティング/URL設計と権限制御

### URL Patterns
- `/accounts/login/`, `/accounts/logout/`
- `/group/new/`, `/group/join/`
- `/dashboard/` (Home)
- `/tasks/` (List), `/tasks/new/`, `/tasks/<id>/edit/`
- `/tasks/<id>/complete/` (Action)
- `/stats/weekly/`, `/stats/history/`

### Permissions
- **LoginRequired**: 全ページ必須。
- **GroupMembership**:
    - カスタムMixin `UserPassesTestMixin` を作成し、アクセスしようとしている `Chore` や `Execution` が `request.user.group` と一致するか常にチェックする。
    - 異なるグループのデータは絶対に見せない（404 or 403）。

---

## 7. MVPの実装手順

1. **Project Init**: Django install, Settings (JA, Timezone).
2. **Auth & Group**: Custom User Model, HouseGroup Model, Login View.
3. **Core Chore Models**: Chore Model, Tag Model.
4. **Task UI**: Create/Edit/List views.
5. **Execution Logic**: "Done" button implementation, Point calculation method.
6. **Ranking Logic**: Weekly aggregation view.
7. **Polish**: CSS styling (Pop theme), Charts using Chart.js (simple).

---

## 8. 将来の拡張性 (Future Roadmap)


- **Local Network Support**:
    - `ALLOWED_HOSTS = ['*']` またはローカルIP範囲を指定し、家庭内LANの他端末（スマホ等）からアクセス可能にする。
    - 起動コマンド: `python manage.py runserver 0.0.0.0:8000`
    - (将来): 固定IP化やmDNS (bonjour) の利用検討。
- **PostgreSQL移行**:
    - 現状のモデルは標準的なフィールドのみなので、`dumpdata` / `loaddata` で容易に移行可能。
    - JSONFieldを使用する場合、SQLiteでもサポートされているが、Postgresの方が検索性能が高い。
- **通知機能**:
    - 誰かがタスクを完了したらLINE Notify / Slack連携 / Push通知。
- **家事カレンダー**:
    - 実施履歴をカレンダー形式で表示（FullCalendar.js統合）。
- **レコメンド/AI**:
    - 「このタスクは○○さんがやると効率が良いです（過去実績より）」
    - 「最近○○さんの負担が高いです」というアラート。
- **報酬システム**:
    - ポイントを「Amazonギフト券」や「マッサージ券」などのリアル報酬と交換する機能（家庭内通貨化）。
