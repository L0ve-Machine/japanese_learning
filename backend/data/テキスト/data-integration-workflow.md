# Data Integration Workflow for Interactive Textbook Content

## Overview
This document outlines the step-by-step process for integrating client CSV data into interactive HTML chapter files with clickable vocabulary and translation features.

## Data Sources Required
1. **テキスト５．コンテンツテキスト.csv** - Main text content with Japanese/Indonesian pairs
2. **テキスト６．語彙データ.csv** - Vocabulary definitions for clickable words
3. **テキスト４．章データ.csv** - Chapter metadata (optional for context)

## Step-by-Step Integration Process

### Step 1: Analyze Content Text Data
```csv
subject_key,item_key,chapter_key,page_number,text_order,japanese,indonesian
介護試験対策,介護保険,chapter_1,1,1,介護保険制度は、高齢者の介護を社会全体で支える仕組みです。,Sistem asuransi perawatan jangka panjang adalah mekanisme untuk mendukung perawatan lansia oleh seluruh masyarakat.
```

**Actions:**
- Extract Japanese sentences by `text_order` for the target chapter
- Extract corresponding Indonesian translations
- Group by `page_number` if multiple pages exist

### Step 2: Analyze Vocabulary Data
```csv
subject_key,item_key,chapter_key,japanese_word,indonesian_translation,usage_context
介護試験対策,介護保険,chapter_1,介護保険制度,Sistem asuransi perawatan jangka panjang,制度名
```

**Actions:**
- Extract vocabulary words for the target chapter (`chapter_key`)
- Create mapping: `japanese_word` → `indonesian_translation`
- Identify which vocabulary words appear in each sentence

### Step 3: HTML Structure Setup
Add required CSS classes and popup element:

```css
/* Vocabulary word styling */
.vocabulary-word {
    cursor: pointer;
    border-bottom: 1px dotted #9ca3af;
    transition: border-color 0.2s;
}
.vocabulary-word:hover {
    border-color: #374151;
}
#translation-popup {
    max-width: 250px;
    line-height: 1.5;
    position: absolute;
    z-index: 50;
    padding: 12px;
    background-color: #1f2937;
    color: white;
    border-radius: 8px;
    box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    font-size: 0.875rem;
    display: none;
}
```

### Step 4: Create Interactive Text Blocks
For each sentence from the CSV:

```html
<div class="text-block">
    <div class="text-container">
        <p class="japanese-text-container" style="flex-grow: 1; padding-right: 1rem;">
            <!-- Insert processed Japanese text with vocabulary spans -->
        </p>
        <button class="translation-toggle" title="全文翻訳">
            <i class="fa-solid fa-chevron-down"></i>
        </button>
    </div>
    <div class="indonesian-text-wrapper">
        <p class="indonesian-text">
            <!-- Insert Indonesian translation (full sentence) -->
        </p>
        <div class="indonesian-text" style="margin-top: 10px; overflow-x: auto; max-height: 300px; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; min-width: 500px;">
                <thead>
                    <tr style="background-color: #f3f4f6;">
                        <th style="padding: 8px; border: 1px solid #d1d5db; text-align: left;">日本語</th>
                        <th style="padding: 8px; border: 1px solid #d1d5db; text-align: left;">インドネシア語</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Insert vocabulary words that appear in this sentence -->
                    <tr>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">[Japanese word]</td>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">[Indonesian translation]</td>
                    </tr>
                    <!-- Repeat for each vocabulary word in the sentence -->
                </tbody>
            </table>
        </div>
    </div>
</div>
```

### Step 5: Create Vocabulary Tables for Each Text Block
For each text block, create a vocabulary table containing only the words that appear in that specific sentence:

**Process:**
1. Identify all vocabulary words from the CSV that appear in the sentence
2. Create table rows for each vocabulary word found
3. Include both the Japanese word and its Indonesian translation
4. Make tables scrollable for better viewing on all screen sizes

**Table Scrollability Features:**
- **Horizontal scrolling**: `overflow-x: auto` allows users to scroll horizontally on narrow screens
- **Vertical scrolling**: `max-height: 300px; overflow-y: auto` limits table height and adds vertical scroll for long vocabulary lists
- **Minimum width**: `min-width: 500px` ensures table maintains readable column widths

**Example for first sentence:**
```html
<table style="width: 100%; border-collapse: collapse;">
    <thead>
        <tr style="background-color: #f3f4f6;">
            <th style="padding: 8px; border: 1px solid #d1d5db; text-align: left;">日本語</th>
            <th style="padding: 8px; border: 1px solid #d1d5db; text-align: left;">インドネシア語</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 8px; border: 1px solid #d1d5db;">介護保険制度</td>
            <td style="padding: 8px; border: 1px solid #d1d5db;">Sistem asuransi perawatan jangka panjang</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #d1d5db;">高齢者</td>
            <td style="padding: 8px; border: 1px solid #d1d5db;">Lansia</td>
        </tr>
        <!-- Continue for all vocabulary words in the sentence -->
    </tbody>
</table>
```

### Step 6: Process Vocabulary Words in Sentences
For each Japanese sentence:

1. **Identify vocabulary matches**: Find all vocabulary words that appear in the sentence
2. **Sort by length**: Process longer words first to avoid partial matches
3. **Wrap with spans**: Replace vocabulary words with clickable spans

```javascript
// Example processing logic
function processVocabulary(sentence, vocabularyList) {
    let processedSentence = sentence;

    // Sort vocabulary by length (longest first to avoid partial matches)
    const sortedVocab = vocabularyList.sort((a, b) => b.japanese_word.length - a.japanese_word.length);

    sortedVocab.forEach(vocab => {
        if (sentence.includes(vocab.japanese_word)) {
            const regex = new RegExp(vocab.japanese_word, 'g');
            processedSentence = processedSentence.replace(regex,
                `<span class="vocabulary-word" data-translation="${vocab.indonesian_translation}">${vocab.japanese_word}</span>`
            );
        }
    });

    return processedSentence;
}
```

### Step 6: Add JavaScript Functionality
Include the complete popup and toggle JavaScript:

```javascript
// Translation popup functionality
const translationPopup = document.getElementById('translation-popup');

document.body.addEventListener('click', (e) => {
    const wordSpan = e.target.closest('.vocabulary-word');

    if (wordSpan) {
        // Show popup with smart positioning
        const translation = wordSpan.dataset.translation;
        translationPopup.innerHTML = translation;

        // Position popup above or below word
        const rect = wordSpan.getBoundingClientRect();
        // ... positioning logic
    } else if (!e.target.closest('.translation-toggle')) {
        // Hide popup when clicking elsewhere
        translationPopup.style.display = 'none';
    }

    // Handle translation toggles
    handleToggle(e, '.translation-toggle', '.indonesian-text-wrapper');
});
```

## Chapter Count Display

### Updating Chapter Numbers in Subject Pages
When adding new chapters to items, update the display in subject listing pages to show the correct chapter count:

1. **Count actual chapters**: Check the directory structure under `frontend/2_科目学習/科目(Subject)/項目(Item)/[ItemName]/章(Chapter)/`
2. **Count method**: Count directories matching pattern `第*章` (e.g., 第1章, 第2章, etc.)
3. **Update display logic**: Modify JavaScript in subject pages to show correct count instead of default "0章"

**Example for 介護試験対策.html:**
```javascript
// Replace generic chapter count with specific counts
<div class="nav-badge">${item.name === '介護保険' ? 5 : (item.chapters?.length || 0)} 章</div>
```

**Directory structure example:**
```
介護保険/
├── 介護保険.html
└── 章(Chapter)/
    ├── 第1章/
    ├── 第2章/
    ├── 第3章/
    ├── 第4章/
    └── 第5章/
```
= 5 chapters total

### Items and Their Current Chapter Counts:
- **介護保険**: 5章 (第1章 through 第5章)
- **コミュニケーション**: 0章 (no chapter structure yet)
- **その他の項目**: 0章 (no chapter structure yet)

## Implementation Checklist

### Before Starting:
- [ ] Verify CSV data exists for target chapter
- [ ] Check vocabulary words are properly mapped
- [ ] Confirm chapter HTML file exists and is accessible

### During Implementation:
- [ ] Add Font Awesome CSS for icons
- [ ] Add vocabulary and popup CSS styles
- [ ] Create translation popup HTML element
- [ ] Process each sentence with vocabulary wrapping
- [ ] Create vocabulary tables for each text block with words from that sentence
- [ ] Add complete JavaScript functionality
- [ ] Test popup positioning on different screen sizes
- [ ] Add quiz section HTML with questions from テキスト７
- [ ] Implement quiz JavaScript with feedback from テキスト９
- [ ] Test quiz correct/incorrect answer behavior

### After Implementation:
- [ ] Test all vocabulary words show correct translations
- [ ] Verify popup doesn't go off-screen
- [ ] Confirm translation toggles still work
- [ ] Test on mobile devices
- [ ] Check for any JavaScript errors in console
- [ ] Test quiz functionality on all questions
- [ ] Verify correct answers are only highlighted when user gets them right
- [ ] Confirm feedback displays correctly for both correct and incorrect answers

## File Locations

### Input Data:
```
backend/data/テキスト/
├── テキスト５．コンテンツテキスト.csv     # Main text content
├── テキスト６．語彙データ.csv           # Vocabulary definitions
├── テキスト４．章データ.csv             # Chapter metadata
├── テキスト７．クイズ問題.csv           # Quiz questions
├── テキスト８．クイズ選択肢.csv         # Quiz multiple choice options
└── テキスト９．フィードバック.csv       # Quiz feedback explanations
```

### Output Files:
```
frontend/2_科目学習/科目(Subject)/項目(Item)/[subject_name]/章(Chapter)/[chapter_folder]/[chapter_name].html
```

## Example Complete Implementation

### Original sentence:
```
介護保険制度は、高齢者の介護を社会全体で支える仕組みです。
```

### After vocabulary processing:
```html
<span class="vocabulary-word" data-translation="Sistem asuransi perawatan jangka panjang">介護保険制度</span>は、<span class="vocabulary-word" data-translation="Lansia">高齢者</span>の<span class="vocabulary-word" data-translation="Perawatan">介護</span>を<span class="vocabulary-word" data-translation="Seluruh masyarakat">社会全体</span>で<span class="vocabulary-word" data-translation="Mendukung">支える</span><span class="vocabulary-word" data-translation="Mekanisme / Sistem">仕組み</span>です。
```

### Complete text block with full translation and vocabulary table:
```html
<div class="text-block">
    <div class="text-container">
        <p class="japanese-text-container" style="flex-grow: 1; padding-right: 1rem;">
            <span class="vocabulary-word" data-translation="Sistem asuransi perawatan jangka panjang">介護保険制度</span>は、<span class="vocabulary-word" data-translation="Lansia">高齢者</span>の<span class="vocabulary-word" data-translation="Perawatan">介護</span>を<span class="vocabulary-word" data-translation="Seluruh masyarakat">社会全体</span>で<span class="vocabulary-word" data-translation="Mendukung">支える</span><span class="vocabulary-word" data-translation="Mekanisme / Sistem">仕組み</span>です。
        </p>
        <button class="translation-toggle" title="全文翻訳">
            <i class="fa-solid fa-chevron-down"></i>
        </button>
    </div>
    <div class="indonesian-text-wrapper">
        <p class="indonesian-text">
            Sistem asuransi perawatan jangka panjang adalah mekanisme untuk mendukung perawatan lansia oleh seluruh masyarakat.
        </p>
        <div class="indonesian-text" style="margin-top: 10px; overflow-x: auto; max-height: 300px; overflow-y: auto;">
            <table style="width: 100%; border-collapse: collapse; min-width: 500px;">
                <thead>
                    <tr style="background-color: #f3f4f6;">
                        <th style="padding: 8px; border: 1px solid #d1d5db; text-align: left;">日本語</th>
                        <th style="padding: 8px; border: 1px solid #d1d5db; text-align: left;">インドネシア語</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">介護保険制度</td>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">Sistem asuransi perawatan jangka panjang</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">高齢者</td>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">Lansia</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">介護</td>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">Perawatan</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">社会全体</td>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">Seluruh masyarakat</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">支える</td>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">Mendukung</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">仕組み</td>
                        <td style="padding: 8px; border: 1px solid #d1d5db;">Mekanisme / Sistem</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
```

## Quiz Integration (Steps 7-9)

After implementing the interactive text content, add quiz functionality using data from テキスト７ and テキスト８.

### Step 7: Read Quiz Data Sources
Required CSV files:
1. **テキスト７．クイズ問題.csv** - Quiz questions with Japanese/Indonesian text
2. **テキスト８．クイズ選択肢.csv** - Multiple choice options with correct answer flags
3. **テキスト９．フィードバック.csv** - Feedback explanations for each option

### Step 8: Add Quiz Section HTML
Insert quiz section after the text content:

```html
<!-- Quiz Section -->
<div class="quiz-section" style="margin-top: 40px; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
    <h3 style="color: #007bff; margin-bottom: 20px;">📝 確認問題</h3>

    <!-- Question Template -->
    <div class="quiz-question" style="margin-bottom: 30px; padding: 20px; background: white; border-radius: 6px; border-left: 4px solid #007bff;">
        <h4 style="color: #333; margin-bottom: 15px;">問題[question_number]</h4>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 20px;">
            [japanese_question]
        </p>
        <div class="quiz-options">
            <!-- Option Template -->
            <div class="option" style="margin-bottom: 10px; padding: 12px; border: 1px solid #dee2e6; border-radius: 4px; cursor: pointer; transition: background-color 0.2s;" data-question="[question_number]" data-option="[option_number]">
                <label style="cursor: pointer; width: 100%; display: block;">
                    <input type="radio" name="question[question_number]" value="[option_number]" style="margin-right: 10px;">
                    [option_number]. [japanese_option]
                </label>
            </div>
            <!-- Repeat for all 5 options -->
        </div>
        <button class="check-answer-btn" onclick="checkAnswer([question_number])" style="margin-top: 15px; padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px;">答えを確認</button>
        <div class="feedback" id="feedback[question_number]" style="margin-top: 15px; padding: 15px; border-radius: 4px; display: none;"></div>
    </div>
</div>
```

### Step 9: Add Quiz JavaScript Functionality

```javascript
// Quiz functionality
function checkAnswer(questionNumber) {
    const selectedOption = document.querySelector(`input[name="question${questionNumber}"]:checked`);
    const feedbackDiv = document.getElementById(`feedback${questionNumber}`);

    if (!selectedOption) {
        alert('選択肢を選んでください。');
        return;
    }

    const selectedValue = parseInt(selectedOption.value);
    let feedbackData = getFeedbackData(questionNumber, selectedValue);
    let isCorrect = isAnswerCorrect(questionNumber, selectedValue);

    // Show feedback
    feedbackDiv.style.display = 'block';
    feedbackDiv.innerHTML = `
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: bold; color: ${isCorrect ? '#28a745' : '#dc3545'};">
                ${isCorrect ? '✓ 正解' : '✗ 不正解'}
            </span>
        </div>
        <div style="background-color: #f8f9fa; padding: 12px; border-radius: 4px; border-left: 3px solid ${isCorrect ? '#28a745' : '#dc3545'};">
            <strong>解説:</strong><br>
            ${feedbackData.japanese}
        </div>
        <div style="background-color: #f1f3f4; padding: 12px; border-radius: 4px; margin-top: 10px; border-left: 3px solid #6c757d;">
            <strong>インドネシア語:</strong><br>
            ${feedbackData.indonesian}
        </div>
    `;

    // Only highlight correct answer if user got it right
    if (isCorrect) {
        highlightCorrectAnswer(questionNumber);
    }
}

function getFeedbackData(questionNumber, optionNumber) {
    // Create object from テキスト９．フィードバック.csv data
    const feedbackData = {
        [questionNumber]: {
            [optionNumber]: {
                japanese: '[japanese_feedback from CSV]',
                indonesian: '[indonesian_feedback from CSV]'
            }
            // ... all options for this question
        }
        // ... all questions
    };
    return feedbackData[questionNumber][optionNumber];
}

function isAnswerCorrect(questionNumber, optionNumber) {
    // Create object from テキスト８．クイズ選択肢.csv where is_correct = true
    const correctAnswers = {
        [questionNumber]: [correct_option_number]
        // ... map all questions to their correct answer numbers
    };
    return correctAnswers[questionNumber] === optionNumber;
}

function highlightCorrectAnswer(questionNumber) {
    const correctAnswers = {[questionNumber]: [correct_option_number]};
    const correctOptionNumber = correctAnswers[questionNumber];
    const correctOption = document.querySelector(`input[name="question${questionNumber}"][value="${correctOptionNumber}"]`).closest('.option');

    // Remove any existing highlights
    document.querySelectorAll(`input[name="question${questionNumber}"]`).forEach(input => {
        input.closest('.option').style.backgroundColor = '';
        input.closest('.option').style.borderColor = '#dee2e6';
    });

    // Highlight correct answer
    correctOption.style.backgroundColor = '#d4edda';
    correctOption.style.borderColor = '#28a745';
}
```

### Quiz Implementation Process:

1. **Extract question data** from テキスト７．クイズ問題.csv for the target chapter
2. **Extract choice data** from テキスト８．クイズ選択肢.csv matching question numbers
3. **Extract feedback data** from テキスト９．フィードバック.csv for all question/option combinations
4. **Build quiz HTML** with proper question numbers and choice options
5. **Implement JavaScript objects** with feedback and correct answer mappings
6. **Test quiz functionality** ensuring correct/incorrect behavior works properly

### Quiz Behavior:
- **Correct Answer**: Shows green checkmark, explanation, and highlights correct option
- **Incorrect Answer**: Shows red X and explanation but does NOT reveal correct answer
- **User must keep trying** until they select the correct option to see the highlight

## Notes for Future Implementations

1. **Performance**: For chapters with many vocabulary words, consider debouncing popup positioning
2. **Accessibility**: Add ARIA labels for screen readers
3. **Mobile**: Test touch interactions on mobile devices
4. **Localization**: Support for additional languages beyond Indonesian
5. **Advanced Features**: Consider adding vocabulary lists, progress tracking, or quiz integration
6. **Quiz Scaling**: For chapters with many questions, consider pagination or section grouping

## Troubleshooting

### Common Issues:
- **Overlapping spans**: Ensure vocabulary words are sorted by length
- **Popup positioning**: Check viewport boundaries and scroll position
- **Missing translations**: Verify vocabulary CSV has correct chapter_key
- **JavaScript errors**: Check for missing popup element or CSS classes

### Debug Tips:
- Use browser console to check for JavaScript errors
- Inspect element to verify spans have correct data-translation attributes
- Test popup positioning at different scroll positions
- Verify CSV data encoding (UTF-8) for Japanese characters