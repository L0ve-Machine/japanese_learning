#!/usr/bin/env python3
"""
Japanese Learning Platform Dashboard
Flask application for previewing the dashboard interface
"""

from flask import Flask, render_template_string
from datetime import datetime
from dataclasses import dataclass
from typing import List

app = Flask(__name__)

@dataclass
class StatCard:
    """Data class for dashboard statistics"""
    title: str
    value: str
    progress: int
    color: str

@dataclass
class LearningOption:
    """Data class for learning menu options"""
    id: str
    title: str
    description: str
    icon: str
    color: str
    route: str

class DashboardData:
    """Dashboard data provider"""

    @staticmethod
    def get_user_stats() -> List[StatCard]:
        """Generate user statistics for dashboard"""
        return [
            StatCard(
                title="今週の学習時間",
                value="12時間",
                progress=60,
                color="#4caf50"
            ),
            StatCard(
                title="完了した問題",
                value="234問",
                progress=45,
                color="#2196f3"
            ),
            StatCard(
                title="正答率",
                value="78%",
                progress=78,
                color="#ff9800"
            )
        ]

    @staticmethod
    def get_learning_options() -> List[LearningOption]:
        """Get available learning options"""
        return [
            LearningOption(
                id="past-exams",
                title="過去問題",
                description="過去5年分の問題を練習\n125問 × 5択の実践問題",
                icon="assignment",
                color="#4caf50",
                route="/past-exams"
            ),
            LearningOption(
                id="subjects",
                title="科目学習",
                description="13科目から学習\nテキスト→問題→解説の流れ",
                icon="school",
                color="#2196f3",
                route="/subjects"
            ),
            LearningOption(
                id="vocabulary",
                title="ことば",
                description="重要単語を学習\n医療・介護用語を中心に",
                icon="translate",
                color="#ff9800",
                route="/vocabulary"
            ),
            LearningOption(
                id="flashcards",
                title="暗記カード",
                description="フラッシュカードで復習\n効率的な記憶定着",
                icon="quiz",
                color="#9c27b0",
                route="/flashcards"
            ),
            LearningOption(
                id="videos",
                title="解説動画",
                description="動画で詳しく学習\nVimeo統合の高品質動画",
                icon="video_library",
                color="#f44336",
                route="/videos"
            ),
            LearningOption(
                id="progress",
                title="学習進捗",
                description="進捗状況を確認\n詳細な学習データ分析",
                icon="trending_up",
                color="#00bcd4",
                route="/progress"
            )
        ]

@app.route('/')
def dashboard():
    """Main dashboard route"""
    stats = DashboardData.get_user_stats()
    learning_options = DashboardData.get_learning_options()

    return render_template_string(DASHBOARD_TEMPLATE,
                                stats=stats,
                                learning_options=learning_options,
                                current_time=datetime.now())

@app.route('/<path:route>')
def learning_section(route):
    """Handle learning section routes"""
    learning_options = DashboardData.get_learning_options()

    # Find the selected option
    selected_option = None
    for option in learning_options:
        if route in option.route:
            selected_option = option
            break

    if not selected_option:
        return render_template_string(ERROR_TEMPLATE, route=route)

    return render_template_string(LEARNING_SECTION_TEMPLATE,
                                option=selected_option)

# HTML Templates using Jinja2
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本語学習 - ダッシュボード</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #fafafa;
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
            color: white;
            padding: 30px 20px;
            margin-bottom: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 300;
            margin-bottom: 10px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            transition: transform 0.2s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);
        }

        .stat-title {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 10px;
            text-transform: uppercase;
        }

        .stat-value {
            font-size: 2.2rem;
            font-weight: 500;
            margin-bottom: 15px;
        }

        .progress-bar {
            width: 100%;
            height: 6px;
            background-color: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4caf50, #66bb6a);
            transition: width 0.3s ease;
        }

        .learning-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
        }

        .learning-card {
            background: white;
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 3px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
        }

        .learning-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            text-decoration: none;
            color: inherit;
        }

        .card-icon {
            width: 60px;
            height: 60px;
            margin: 0 auto 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 28px;
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 500;
            margin-bottom: 8px;
        }

        .card-description {
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 20px;
            white-space: pre-line;
        }

        .card-button {
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            color: white;
        }

        .section-title {
            font-size: 1.8rem;
            font-weight: 500;
            margin-bottom: 25px;
        }

        .timestamp {
            text-align: center;
            color: #999;
            font-size: 0.8rem;
            margin-top: 40px;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .learning-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>こんにちは、学習者さん</h1>
            <p>今日も頑張りましょう！介護資格取得に向けて一歩ずつ進んでいきましょう。</p>
        </div>

        <div class="stats-grid">
            {% for stat in stats %}
            <div class="stat-card">
                <h3 class="stat-title">{{ stat.title }}</h3>
                <div class="stat-value" style="color: {{ stat.color }}">{{ stat.value }}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ stat.progress }}%;"></div>
                </div>
            </div>
            {% endfor %}
        </div>

        <h2 class="section-title">学習メニュー</h2>
        <div class="learning-grid">
            {% for option in learning_options %}
            <a href="{{ option.route }}" class="learning-card">
                <div class="card-icon" style="background-color: {{ option.color }};">
                    <span class="material-icons">{{ option.icon }}</span>
                </div>
                <h3 class="card-title">{{ option.title }}</h3>
                <p class="card-description">{{ option.description }}</p>
                <button class="card-button" style="background-color: {{ option.color }};">開始</button>
            </a>
            {% endfor %}
        </div>

        <div class="timestamp">
            <p>Flask Dashboard Generated: {{ current_time.strftime('%Y年%m月%d日 %H:%M:%S') }}</p>
        </div>
    </div>
</body>
</html>
'''

LEARNING_SECTION_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ option.title }} - 日本語学習</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #fafafa;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            background: {{ option.color }};
            color: white;
            padding: 40px 20px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 30px;
        }
        .back-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            margin-bottom: 20px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .content {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="/" class="back-btn">← ダッシュボードに戻る</a>
            <h1><span class="material-icons" style="font-size: 3rem; display: block; margin-bottom: 10px;">{{ option.icon }}</span>{{ option.title }}</h1>
            <p>{{ option.description }}</p>
        </div>

        <div class="content">
            <h2>機能説明</h2>
            {% if option.id == 'subjects' %}
            <p><strong>科目学習機能：</strong></p>
            <ul>
                <li>13科目のカテゴリー別学習</li>
                <li>グループA/B/C分類システム</li>
                <li>学習テキスト → 問題演習 → 詳細解説の流れ</li>
                <li>多言語翻訳対応</li>
                <li>進捗追跡機能</li>
            </ul>
            {% elif option.id == 'past-exams' %}
            <p><strong>過去問題機能：</strong></p>
            <ul>
                <li>過去5年分の実際の試験問題</li>
                <li>125問 × 5択問題形式</li>
                <li>年度別・科目別選択可能</li>
                <li>詳細解説付き</li>
                <li>ランダム出題機能</li>
            </ul>
            {% else %}
            <p>この機能は開発中です。近日公開予定です。</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

ERROR_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ページが見つかりません</title>
    <style>
        body { font-family: 'Roboto', sans-serif; text-align: center; padding: 50px; }
        .error { color: #f44336; }
    </style>
</head>
<body>
    <div class="error">
        <h1>404 - ページが見つかりません</h1>
        <p>要求されたページ "{{ route }}" は存在しません。</p>
        <a href="/">ダッシュボードに戻る</a>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    print("Japanese Learning Platform Dashboard")
    print("=" * 50)
    print("Starting Flask application...")
    print("Dashboard URL: http://localhost:5000")
    print("Subject Learning: http://localhost:5000/subjects")
    print("Past Exams: http://localhost:5000/past-exams")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)