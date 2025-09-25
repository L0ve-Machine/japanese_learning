# 介護試験対策_chapters Branch

## Overview

This branch adds chapter structure and navigation for the 介護保険 (Long-term Care Insurance) section of the Japanese learning platform.

## Changes Made

- Added 介護保険 章 (Chapters) Structure and Navigation
- Enhanced Japanese Learning Platform with 科目学習 (Subject Learning) System
- Integrated past exam data import functionality

## Features Added

### Chapter Navigation System
- Structured learning paths for 介護保険 topics
- Chapter-based content organization
- Navigation between different sections

### Subject Learning Enhancement
- Improved 科目学習 (Subject Learning) system
- Better content categorization
- Enhanced user learning experience

## Technical Implementation

- Built on existing Django + React architecture
- Maintains compatibility with current database structure
- Follows established coding patterns and conventions

## 科目学習 Content Management System

### Excel Import Approach for Content Management

#### Data Flow Overview
**Excel → Management Command → Django Models → Database**

#### Current Model Hierarchy
```
Subject (科目)
├── SubjectItem (項目)
│   ├── Chapter (章)
│   │   ├── Page (ページ)
│   │   │   └── StudyText (テキスト)
```

#### Excel Data Mapping Strategy
Single Sheet Approach with the following columns:

| Excel Column | Django Model | Field | Purpose |
|--------------|--------------|-------|---------|
| `subject_name` | Subject | name | 介護保険, 医学一般 etc. |
| `item_name` | SubjectItem | name | 制度の概要, 保険給付 etc. |
| `chapter_name` | Chapter | name | 介護保険制度の目的 etc. |
| `page_name` | Page | name | Page 1, Page 2 etc. |
| `text_title` | StudyText | title | Individual text section title |
| `content` | StudyText | content | The actual study content |
| `translation_en` | StudyText | translations['en'] | English translation |
| `translation_vi` | StudyText | translations['vi'] | Vietnamese translation |
| `order` | StudyText | order | Display order |
| `is_premium` | StudyText | is_premium | Premium content flag |

#### Implementation Plan

**File Structure:**
```
backend/
├── apps/
│   └── learning/
│       └── management/
│           └── commands/
│               ├── __init__.py
│               ├── import_excel_content.py
│               └── generate_template.py
│       └── utils/
│           ├── __init__.py
│           ├── excel_processor.py
│           └── content_validator.py
```

**Components to Build:**
1. **Management Command** (`import_excel_content.py`)
   - Read Excel file using pandas
   - Create/update hierarchy objects automatically
   - Handle translations JSON field
   - Validate data integrity
   - Progress reporting and error handling

2. **Data Validation Logic**
   - Check required fields
   - Ensure hierarchy consistency
   - Validate translation JSON structure
   - Handle duplicate content

3. **Error Handling**
   - Skip invalid rows with detailed logging
   - Rollback on critical errors
   - Generate import summary report

**Key Benefits:**
- **Automatic Hierarchy Creation**: Missing levels created automatically
- **Bulk Processing**: Handle thousands of rows efficiently
- **Translation Support**: JSON field handles multiple languages
- **Order Management**: Proper sequencing of content
- **Rollback Safety**: Transaction-based imports

**Usage:**
```bash
cd backend
python manage.py import_excel_content --file /path/to/content.xlsx
python manage.py generate_template
```

#### Questions for Implementation:
1. Do you have separate sheets or everything in one sheet?
2. How many languages need translation support?
3. Should the system auto-create missing hierarchy levels or validate they exist?

## Next Steps

- Implement Excel import system for 科目学習 content
- Merge into main branch after review
- Extend chapter system to other subjects
- Add progress tracking for chapter completion

## Branch Status

- **Current Status**: Ready for review
- **Base Branch**: main
- **Commits**: 1 commit adding chapter structure
- **Files Changed**: Frontend components and backend models related to chapter navigation