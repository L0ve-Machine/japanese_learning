# 科目学習 Chapter Migration Instructions

## Current Status (as of 2025-10-07)

### ✅ Completed - Database Structure
- **第1章 (介護保険制度とは？)** - Fully migrated with content
  - URL: http://127.0.0.1:8000/chapter-db/1/
  - All text, vocabulary, and quiz data stored in database
  - Editable through Django admin panel

- **第2章-第5章** - Database structure created (NO CONTENT)
  - URLs: http://127.0.0.1:8000/chapter-db/2/ through /5/
  - Pages exist in database but have no text blocks, vocabulary, or quizzes
  - Ready for content population

### ⚠️ Content Status - Chapters 2-5

**IMPORTANT:** Chapters 2-5 have NO actual content in either:
- HTML files (showing "コンテンツ準備中" placeholder)
- CSV files (only chapter_1 data exists)

#### 介護保険 Item - Content Needed
1. **第2章** - `2. 被保険者（保険に加入する人）` - Page ID: 2
2. **第3章** - `3. 要介護認定（サービス利用までの流れ）` - Page ID: 3
3. **第4章** - `4. 介護保険のサービス` - Page ID: 4
4. **第5章** - `5. 保険料と利用料` - Page ID: 5

#### Other Items (all hardcoded)
- ごみの分別
- コミュニケーション
- 介護分野
- 先輩との会話
- 公共交通機関の利用
- 緊急時の報告
- 趣味を聞く
- 食事に誘う
- 飲食料品製造業分野

---

## Adding Content to Chapters 2-5

Since chapters 2-5 have database structure but NO content, you have two options:

### Option 1: Create CSV Data
Add content to the CSV files in `backend/data/テキスト/`:
1. **テキスト５．コンテンツテキスト.csv** - Add text blocks
2. **テキスト６．語彙データ.csv** - Add vocabulary
3. **テキスト７．クイズ問題.csv** - Add quiz questions
4. **テキスト８．クイズ選択肢.csv** - Add quiz options
5. **テキスト９．フィードバック.csv** - Add feedback

Use `chapter_2`, `chapter_3`, `chapter_4`, `chapter_5` as the `chapter_key` values.

Then run the chapter_learning_view which will read from CSV automatically.

### Option 2: Create Django Management Commands
Create population scripts like `populate_chapter2.py` following the pattern from `populate_chapter1.py`:

```bash
cd backend
python manage.py populate_chapter2
python manage.py populate_chapter3
# etc.
```

---

## Migration Process (Follow these steps for EACH chapter)

### Step 1: Read the HTML file
```
Read the hardcoded HTML file located at:
frontend/2_科目学習/科目(Subject)/項目(Item)/[ITEM_NAME]/章(Chapter)/[CHAPTER_NUMBER]/[CHAPTER_FILE].html
```

### Step 2: Extract the data
From the HTML file, extract:
1. **Text blocks** - Japanese text with Indonesian translations
2. **Vocabulary entries** - Individual words with translations (found in the vocabulary tables)
3. **Quiz questions** - Question text
4. **Quiz options** - Answer choices with explanations in Japanese and Indonesian

### Step 3: Create a management command
Create a new management command file:
```
backend/apps/learning/management/commands/populate_chapter[N].py
```

Use `populate_chapter1.py` as a template. The command should:
1. Get or create the Subject → SubjectItem → Chapter → Page hierarchy
2. Create TextBlock entries with Japanese and Indonesian text
3. Create VocabularyEntry entries linked to each TextBlock
4. Create QuizQuestion entries
5. Create QuizOption entries with correct answers and explanations

### Step 4: Run the management command
```bash
cd backend
python manage.py populate_chapter[N]
```

Verify the data was created:
```bash
python manage.py shell -c "from apps.learning.models import Page, TextBlock; page = Page.objects.get(name='[PAGE_NAME]'); print(f'Text Blocks: {TextBlock.objects.filter(page=page).count()}')"
```

### Step 5: Update navigation
Edit: `backend/templates/subjects/subject_detail.html`

Change the chapter item from:
```html
<div class="chapter-item" onclick="startChapter('第N章', '[TITLE]', event)">
```

To:
```html
<div class="chapter-item" onclick="window.location.href='{% url 'chapter_page' page_id=[PAGE_ID] %}'; event.stopPropagation();">
    <div class="chapter-info">
        <div class="chapter-title">第N章 (DB版)</div>
```

### Step 6: Get the page ID
```bash
python manage.py shell -c "from apps.learning.models import Page; page = Page.objects.get(name='[PAGE_NAME]'); print(f'Page ID: {page.id}')"
```

### Step 7: Test the new page
Visit: http://127.0.0.1:8000/chapter-db/[PAGE_ID]/

Verify:
- All text blocks display correctly
- Vocabulary words are clickable and show translations
- Quiz questions and options work
- Explanations show in both Japanese and Indonesian

### Step 8: Delete the old hardcoded HTML file
```bash
rm "frontend/2_科目学習/科目(Subject)/項目(Item)/[PATH_TO_FILE].html"
```

---

## Database Models Reference

### TextBlock
- `page` - ForeignKey to Page
- `japanese_text` - TextField (full Japanese text)
- `indonesian_translation` - TextField (full Indonesian translation)
- `order` - IntegerField

### VocabularyEntry
- `text_block` - ForeignKey to TextBlock
- `japanese_word` - CharField
- `indonesian_translation` - CharField
- `order` - IntegerField

### QuizQuestion
- `page` - ForeignKey to Page
- `question_number` - IntegerField
- `question_text` - TextField
- `order` - IntegerField

### QuizOption
- `question` - ForeignKey to QuizQuestion
- `option_number` - IntegerField
- `option_text` - TextField
- `is_correct` - BooleanField
- `explanation_japanese` - TextField
- `explanation_indonesian` - TextField

---

## Important Notes

1. **Keep exact text** - Do NOT change any wording when migrating. Copy text exactly as it appears in the HTML files.

2. **Vocabulary order matters** - List vocabulary in the order they appear in the Japanese text to ensure proper marking.

3. **Quiz option numbers** - Must match the option numbers in the original HTML (typically 1-5).

4. **Page IDs** - Get the page ID from the database after creating the page, don't guess it.

5. **Test before deleting** - Always test the new database-driven page before deleting the old hardcoded HTML file.

---

## Template Location
The Django template that renders all chapters is:
```
backend/templates/subjects/chapter_page.html
```

This template is reusable for all chapters - no need to modify it.

---

## Admin Panel
Access the admin panel to edit content:
http://127.0.0.1:8000/admin/

Navigate to **Learning** section:
- Text blocks
- Vocabulary entries
- Quiz questions
- Quiz options

---

## Progress Tracking

### 介護保険
- [x] 第1章 - 介護保険制度とは？ (CONTENT COMPLETE)
- [x] 第2章 - 被保険者（保険に加入する人）(STRUCTURE ONLY - NO CONTENT)
- [x] 第3章 - 要介護認定（サービス利用までの流れ）(STRUCTURE ONLY - NO CONTENT)
- [x] 第4章 - 介護保険のサービス (STRUCTURE ONLY - NO CONTENT)
- [x] 第5章 - 保険料と利用料 (STRUCTURE ONLY - NO CONTENT)

### Other Items
- [ ] ごみの分別
- [ ] コミュニケーション
- [ ] 介護分野
- [ ] 先輩との会話
- [ ] 公共交通機関の利用
- [ ] 緊急時の報告
- [ ] 趣味を聞く
- [ ] 食事に誘う
- [ ] 飲食料品製造業分野

---

## Commands Quick Reference

```bash
# Start server
cd backend && python manage.py runserver

# Create migration
cd backend && python manage.py makemigrations learning

# Run migration
cd backend && python manage.py migrate learning

# Run population command
cd backend && python manage.py populate_chapter[N]

# Get page ID
cd backend && python manage.py shell -c "from apps.learning.models import Page; page = Page.objects.get(name='PAGE_NAME'); print(f'Page ID: {page.id}')"

# Verify data
cd backend && python manage.py shell -c "from apps.learning.models import Page, TextBlock, VocabularyEntry, QuizQuestion; page = Page.objects.get(name='PAGE_NAME'); print(f'Blocks: {TextBlock.objects.filter(page=page).count()}, Vocab: {VocabularyEntry.objects.filter(text_block__page=page).count()}, Quiz: {QuizQuestion.objects.filter(page=page).count()}')"
```

---

**Ready to continue? Start with 第2章!**
